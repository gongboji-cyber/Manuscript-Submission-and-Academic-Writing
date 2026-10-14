#!/usr/bin/env python3
"""Render DOCX to PDF and perform real page-count / per-page text-line QA.

Backend order:
1. Microsoft Word COM on Windows (if pywin32 + Word available)
2. LibreOffice/soffice headless

PDF text extraction order:
1. PyMuPDF (fitz)
2. pypdf
3. pdftotext -layout

This script checks actual rendered pages. It still cannot replace human visual review.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

PAGE_PAT=re.compile(r"^(?:第\s*)?\d+(?:\s*页)?$")

def render_word(docx:Path,pdf:Path)->bool:
    if os.name!="nt": return False
    try:
        import win32com.client  # type: ignore
    except Exception:
        return False
    word=None; doc=None
    try:
        word=win32com.client.DispatchEx("Word.Application"); word.Visible=False; word.DisplayAlerts=0
        doc=word.Documents.Open(str(docx),ReadOnly=True); doc.Repaginate(); doc.SaveAs2(str(pdf),FileFormat=17)
        return pdf.is_file() and pdf.stat().st_size>0
    except Exception:
        return False
    finally:
        if doc is not None:
            try: doc.Close(False)
            except Exception: pass
        if word is not None:
            try: word.Quit()
            except Exception: pass

def render_libreoffice(docx:Path,pdf:Path)->bool:
    exe=shutil.which("soffice") or shutil.which("libreoffice")
    if not exe: return False
    with tempfile.TemporaryDirectory(prefix="softcopy_lo_") as tmp:
        profile=Path(tmp)/"profile"; profile.mkdir(); outdir=Path(tmp)/"out"; outdir.mkdir()
        cp=subprocess.run([exe,f"-env:UserInstallation={profile.as_uri()}","--headless","--convert-to","pdf","--outdir",str(outdir),str(docx)],
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        candidate=outdir/(docx.stem+".pdf")
        if cp.returncode==0 and candidate.is_file():
            pdf.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(candidate,pdf); return True
    return False

def extract_pages(pdf:Path)->tuple[str,list[str]]:
    try:
        import fitz  # type: ignore
        d=fitz.open(pdf); return "pymupdf",[p.get_text("text") for p in d]
    except Exception:
        pass
    try:
        from pypdf import PdfReader  # type: ignore
        r=PdfReader(str(pdf)); return "pypdf",[(p.extract_text() or "") for p in r.pages]
    except Exception:
        pass
    exe=shutil.which("pdftotext")
    if exe:
        with tempfile.TemporaryDirectory(prefix="softcopy_pdftext_") as tmp:
            out=Path(tmp)/"out.txt"
            cp=subprocess.run([exe,"-layout",str(pdf),str(out)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            if cp.returncode==0 and out.is_file():
                text=out.read_text(encoding="utf-8",errors="replace")
                return "pdftotext",text.split("\f")[:-1] if text.endswith("\f") else text.split("\f")
    raise SystemExit("No PDF text extraction backend available. Install PyMuPDF, pypdf, or pdftotext.")

def visible_lines(text:str,header_text:str|None=None)->list[str]:
    out=[]
    for raw in text.splitlines():
        s=raw.strip()
        if not s: continue
        if header_text and s==header_text: continue
        if PAGE_PAT.match(s): continue
        out.append(s)
    return out

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("docx"); ap.add_argument("--out-dir",required=True); ap.add_argument("--kind",choices=["manual","source"],required=True)
    ap.add_argument("--source-map"); ap.add_argument("--header-text"); ap.add_argument("--min-source-lines",type=int,default=50)
    args=ap.parse_args()
    docx=Path(args.docx).resolve(); outdir=Path(args.out_dir).resolve(); outdir.mkdir(parents=True,exist_ok=True); pdf=outdir/(docx.stem+".pdf")
    backend="word-com" if render_word(docx,pdf) else "libreoffice" if render_libreoffice(docx,pdf) else None
    if not backend: raise SystemExit("No DOCX renderer available. Use Microsoft Word + pywin32 on Windows, or install LibreOffice/soffice.")
    extractor,pages=extract_pages(pdf); rows=[]; issues=[]; expected=[]
    if args.source_map:
        with Path(args.source_map).resolve().open(encoding="utf-8-sig",newline="") as f: expected=list(csv.DictReader(f))
    for i,text in enumerate(pages,1):
        lines=visible_lines(text,args.header_text)
        rec={"page":i,"rendered_nonblank_text_lines":len(lines),"blank_page":len(lines)==0,"expected_code_lines":"","status":"PASS"}
        if rec["blank_page"]:
            rec["status"]="FAIL"; issues.append({"page":i,"code":"BLANK_PAGE","message":"Rendered page is blank"})
        if args.kind=="source":
            exp=None
            if i<=len(expected):
                try: exp=int(expected[i-1].get("expected_code_lines") or 0)
                except Exception: exp=None
            rec["expected_code_lines"]=exp if exp is not None else ""
            if i<len(pages) and len(lines)<args.min_source_lines:
                rec["status"]="WARN"; issues.append({"page":i,"code":"LOW_RENDERED_TEXT_LINES","message":f"Rendered page has {len(lines)} visible text lines (<{args.min_source_lines}); inspect for wrapping/spacing."})
        rows.append(rec)
    if args.kind=="source" and expected and len(pages)!=len(expected):
        issues.append({"page":None,"code":"PAGE_COUNT_MISMATCH","message":f"Rendered pages={len(pages)} but expected nominal pages={len(expected)}. Long-line wrapping or layout drift likely."})
    if args.kind=="manual":
        all_text="\n".join(pages)
        for pat in (r"\bTODO\b",r"\bTBD\b","待确认","提交前更新","截图待补",r"【图[^】]*】"):
            if re.search(pat,all_text,re.I): issues.append({"page":None,"code":"PLACEHOLDER_OR_INTERNAL_MARKER","message":f"Matched: {pat}"})
    csvp=outdir/(docx.stem+"_PAGINATION_QA.csv")
    with csvp.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=["page","rendered_nonblank_text_lines","blank_page","expected_code_lines","status"]); w.writeheader(); w.writerows(rows)
    blocking={"BLANK_PAGE","PAGE_COUNT_MISMATCH","PLACEHOLDER_OR_INTERNAL_MARKER"}
    status="AUTO_RENDER_QA_PASS" if not any(x["code"] in blocking for x in issues) else "HOLD_FOR_FIXES"
    report={"schema_version":1,"status":status,"docx":str(docx),"pdf":str(pdf),"renderer":backend,"extractor":extractor,"rendered_pages":len(pages),
            "nominal_pages":len(expected) if expected else None,"issues":issues,"manual_visual_qa_required":True}
    jp=outdir/(docx.stem+"_PAGINATION_QA.json"); jp.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    mdp=outdir/(docx.stem+"_PAGINATION_QA.md")
    md=["# 真实分页 QA","",f"- 状态：**{status}**",f"- 渲染器：{backend}",f"- PDF文本提取：{extractor}",f"- 实际页数：{len(pages)}",f"- 名义页数：{len(expected) if expected else 'N/A'}","","## 自动发现"]
    md += [f"- {x['code']}: {x['message']}" for x in issues] if issues else ["- 无阻断性自动问题。"]
    md += ["","## 必须人工确认","- 逐页查看渲染后的 PDF/PNG，确认无截断、重叠、字体异常、图片变形和页眉页脚问题。",
           "- 自动 PASS 不等于 READY_FOR_SUBMISSION；人工视觉 QA 完成后才可更新 canonical facts 中 manual_render_qa。"]
    mdp.write_text("\n".join(md)+"\n",encoding="utf-8")
    print(pdf); print(jp); print(csvp); print(mdp)
    return 0 if status=="AUTO_RENDER_QA_PASS" else 2

if __name__=="__main__": raise SystemExit(main())
