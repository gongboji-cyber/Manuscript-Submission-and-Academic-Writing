#!/usr/bin/env python3
"""Build a clean software-copyright submission package and separate internal archive.

The formal upload folder contains only applicant-facing materials. Internal audits,
evidence chains, development logs and hashes are kept under a separate folder that is
explicitly marked DO_NOT_UPLOAD_BY_DEFAULT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

BLOCKED_NAME_TOKENS=("audit","evidence","dev_log","timeline","regression","pytest","codex","chatgpt","backup","provenance","freeze")
PLACEHOLDER_RE=re.compile(r"(?:TODO|TBD|待确认|提交前更新|截图待补|placeholder|READY_FOR|HOLD_FOR)",re.I)

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def safe_copy(src:Path,dst:Path):
    dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)

def extract_docx_text(path:Path)->str:
    import zipfile
    from xml.etree import ElementTree as ET
    chunks=[]
    with zipfile.ZipFile(path) as z:
        names=["word/document.xml"] + sorted(n for n in z.namelist() if n.startswith("word/header") and n.endswith(".xml")) + sorted(n for n in z.namelist() if n.startswith("word/footer") and n.endswith(".xml"))
        for name in names:
            root=ET.fromstring(z.read(name))
            for node in root.iter():
                if node.tag.endswith("}t") and node.text: chunks.append(node.text)
                elif node.tag.endswith("}p"): chunks.append("\n")
    return "".join(chunks)

def text_of(path:Path)->str:
    if path.suffix.lower()==".docx": return extract_docx_text(path)
    if path.suffix.lower() in (".txt",".md",".json",".csv"): return path.read_text(encoding="utf-8",errors="replace")
    return ""

def application_txt(c:dict)->str:
    order=[
        ("软件全称","software_full_name"),("软件简称","software_short_name"),("版本号","version"),("软件分类","software_classification"),
        ("开发完成日期","completion_date"),("开发方式","development_mode"),("软件说明","software_description"),("发表状态","publication_status"),
        ("首次发表日期","first_publication_date"),("著作权人","copyright_owner"),("权利范围","rights_scope"),("权利取得方式","rights_acquisition"),
        ("开发的硬件环境","development_hardware"),("运行的硬件环境","runtime_hardware"),("开发该软件的操作系统","development_os"),
        ("软件开发环境/开发工具","development_tools"),("运行平台/操作系统","runtime_os"),("软件运行支撑环境/支持软件","runtime_support"),
        ("编程语言","programming_languages"),("源程序量","source_loc"),("开发目的","development_purpose"),("面向领域/行业","industry"),
        ("软件的主要功能","main_functions"),("软件的技术特点","technical_features"),("程序鉴别材料页数","source_material_pages"),
        ("文档鉴别材料页数","manual_material_pages")
    ]
    lines=[]
    for label,key in order:
        value=c.get(key,"")
        if isinstance(value,list): value=", ".join(map(str,value))
        lines.append(f"{label}：{value}")
    return "\n".join(lines)+"\n"

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--facts",required=True); ap.add_argument("--manual-docx",required=True); ap.add_argument("--manual-pdf")
    ap.add_argument("--source-docx",required=True); ap.add_argument("--source-pdf"); ap.add_argument("--screenshots-dir")
    ap.add_argument("--internal-dir",action="append",default=[]); ap.add_argument("--out-dir",required=True); ap.add_argument("--require-pdf",action="store_true",default=False)
    args=ap.parse_args()

    facts_path=Path(args.facts).resolve(); obj=json.loads(facts_path.read_text(encoding="utf-8")); c=obj.get("canonical",obj)
    required=("software_full_name","version","copyright_owner","completion_date","development_mode","rights_acquisition","publication_status")
    unresolved=[k for k in required if not str(c.get(k,"")).strip() or PLACEHOLDER_RE.search(str(c.get(k,"")))]
    if unresolved: raise SystemExit("canonical facts unresolved: "+", ".join(unresolved))
    if c.get("manual_render_qa") not in (True,"CONFIRMED"): raise SystemExit("manual_render_qa is not confirmed; package builder refuses READY package")

    manual_docx=Path(args.manual_docx).resolve(); source_docx=Path(args.source_docx).resolve()
    manual_pdf=Path(args.manual_pdf).resolve() if args.manual_pdf else None; source_pdf=Path(args.source_pdf).resolve() if args.source_pdf else None
    for p in (manual_docx,source_docx):
        if not p.is_file(): raise SystemExit(f"missing required file: {p}")
    if args.require_pdf and (not manual_pdf or not manual_pdf.is_file() or not source_pdf or not source_pdf.is_file()):
        raise SystemExit("PDFs required but missing")

    for p in (manual_docx,source_docx):
        txt=text_of(p)
        if PLACEHOLDER_RE.search(txt): raise SystemExit(f"formal document contains unresolved marker: {p}")
        if c["software_full_name"] not in txt or str(c["version"]) not in txt: raise SystemExit(f"name/version not found in formal document: {p}")

    out=Path(args.out_dir).resolve()
    if out.exists(): shutil.rmtree(out)
    formal=out/"01_正式上传"; internal=out/"02_内部归档_不上传"
    (formal/"01_申请表辅助").mkdir(parents=True); (formal/"02_文档鉴别材料").mkdir(); (formal/"03_程序鉴别材料").mkdir(); (formal/"04_截图_如需").mkdir()
    internal.mkdir(parents=True)
    (internal/"DO_NOT_UPLOAD_BY_DEFAULT.txt").write_text("本目录为内部审计/开发证据链，普通软著登记默认不上传。仅在补正、权属核验或明确需要时选择性提供。\n",encoding="utf-8")

    app_txt=formal/"01_申请表辅助"/"申请表信息.txt"; app_txt.write_text(application_txt(c),encoding="utf-8")
    safe_copy(manual_docx,formal/"02_文档鉴别材料"/manual_docx.name); safe_copy(source_docx,formal/"03_程序鉴别材料"/source_docx.name)
    if manual_pdf and manual_pdf.is_file(): safe_copy(manual_pdf,formal/"02_文档鉴别材料"/manual_pdf.name)
    if source_pdf and source_pdf.is_file(): safe_copy(source_pdf,formal/"03_程序鉴别材料"/source_pdf.name)
    if args.screenshots_dir:
        sd=Path(args.screenshots_dir).resolve()
        if sd.is_dir():
            for p in sd.iterdir():
                if p.is_file() and p.suffix.lower() in (".png",".jpg",".jpeg",".webp"): safe_copy(p,formal/"04_截图_如需"/p.name)
    for raw in args.internal_dir:
        src=Path(raw).resolve()
        if src.is_dir(): shutil.copytree(src,internal/src.name,dirs_exist_ok=True)
        elif src.is_file(): safe_copy(src,internal/src.name)
    safe_copy(facts_path,internal/"application-facts.json")

    violations=[]
    for p in formal.rglob("*"):
        if p.is_file() and any(tok in p.name.lower() for tok in BLOCKED_NAME_TOKENS): violations.append(str(p.relative_to(out)))
    if violations: raise SystemExit("internal-looking filenames leaked into formal package: "+", ".join(violations))

    files=[]
    for p in sorted(out.rglob("*")):
        if p.is_file():
            files.append({"path":p.relative_to(out).as_posix(),"size":p.stat().st_size,"sha256":sha256(p),"zone":"formal" if formal in p.parents else "internal"})
    manifest=out/"PACKAGE_MANIFEST.json"
    manifest.write_text(json.dumps({"schema_version":1,"status":"READY_FOR_SUBMISSION_PACKAGE","software":c["software_full_name"],"version":c["version"],"files":files},ensure_ascii=False,indent=2),encoding="utf-8")
    hashes=out/"FINAL_HASHES.sha256"; hashes.write_text("\n".join(f"{x['sha256']}  {x['path']}" for x in files)+"\n",encoding="utf-8")
    verdict=out/"FINAL_SUBMISSION_PACKAGE_VERDICT.md"
    verdict.write_text(f"# 最终提交包裁决\n\n**READY_FOR_SUBMISSION_PACKAGE**\n\n- 软件：{c['software_full_name']} {c['version']}\n- 正式上传目录：`01_正式上传/`\n- 内部归档目录：`02_内部归档_不上传/`\n- manual_render_qa：已确认\n- PDF要求：{'已强制' if args.require_pdf else '未强制；以当前官网上传要求为准'}\n\n正式上传时不要把内部归档目录整体上传。\n",encoding="utf-8")
    print(formal); print(manifest); print(hashes); print(verdict); return 0

if __name__=="__main__": raise SystemExit(main())
