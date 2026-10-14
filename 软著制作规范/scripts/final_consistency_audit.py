#!/usr/bin/env python3
"""Cross-check canonical application facts against formal text/DOCX materials.

Stdlib-only. This is a consistency gate, not a legal ownership determination and
not a replacement for final visual rendering in Word/WPS/PDF.
"""
from __future__ import annotations
import argparse, csv, json, re, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

INTERNAL_PATTERNS=(r'\bTODO\b',r'\bTBD\b','待确认','提交前更新','Codex','ChatGPT','READY_FOR','HOLD_FOR','submission_master')
PLACEHOLDER_PATTERNS=(r'【图[^】]*】','截图待补','placeholder')

def read_text(path:Path)->str:
    if path.suffix.lower()=='.docx':
        with zipfile.ZipFile(path) as z:
            xml=z.read('word/document.xml')
        root=ET.fromstring(xml)
        out=[]
        for node in root.iter():
            if node.tag.endswith('}t') and node.text: out.append(node.text)
            elif node.tag.endswith('}p'): out.append('\n')
        return ''.join(out)
    return path.read_text(encoding='utf-8',errors='replace')

def issue(level:str,code:str,message:str,source:str='')->dict:
    return {'level':level,'code':code,'message':message,'source':source}

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--application',required=True,help='JSON with canonical application facts')
    ap.add_argument('--manual',action='append',default=[],help='DOCX/TXT/MD formal document; repeatable')
    ap.add_argument('--source-map')
    ap.add_argument('--out-json',default='FINAL_CONSISTENCY_AUDIT.json')
    ap.add_argument('--out-md',default='FINAL_CONSISTENCY_AUDIT.md')
    args=ap.parse_args()

    appp=Path(args.application).resolve()
    facts=json.loads(appp.read_text(encoding='utf-8'))
    canonical=facts.get('canonical',facts)
    name=str(canonical.get('software_full_name','')).strip()
    version=str(canonical.get('version','')).strip()
    owner=str(canonical.get('copyright_owner','')).strip()
    issues=[]

    if not name: issues.append(issue('P1','MISSING_NAME','software_full_name missing',str(appp)))
    if not version: issues.append(issue('P1','MISSING_VERSION','version missing',str(appp)))

    for raw in args.manual:
        p=Path(raw).resolve()
        txt=read_text(p)
        if name and name not in txt:
            issues.append(issue('P1','NAME_NOT_FOUND',f'Canonical software name not found in {p.name}',str(p)))
        if version and version not in txt:
            issues.append(issue('P1','VERSION_NOT_FOUND',f'Canonical version not found in {p.name}',str(p)))
        if owner and '说明书' in p.name and owner not in txt:
            issues.append(issue('P2','OWNER_NOT_FOUND',f'Owner not found in likely manual {p.name}',str(p)))
        for pat in INTERNAL_PATTERNS:
            if re.search(pat,txt,re.I):
                issues.append(issue('P1','INTERNAL_MARKER',f'Internal marker matched: {pat}',str(p)))
        for pat in PLACEHOLDER_PATTERNS:
            if re.search(pat,txt,re.I):
                issues.append(issue('P1','PLACEHOLDER',f'Placeholder matched: {pat}',str(p)))

    if args.source_map:
        p=Path(args.source_map).resolve()
        with p.open(encoding='utf-8-sig',newline='') as f:
            rows=list(csv.DictReader(f))
        if not rows:
            issues.append(issue('P1','EMPTY_SOURCE_MAP','Source page map is empty',str(p)))
        for i,row in enumerate(rows):
            n=int(row.get('rendered_code_lines') or 0)
            status=row.get('continuity_status','')
            if i<len(rows)-1 and n<50:
                issues.append(issue('P1','LOW_MIDDLE_PAGE_LINES',f'Nominal page {row.get("page")} has {n}<50 code lines',str(p)))
            if i==len(rows)-1 and n<50 and status!='FINAL_PARTIAL_PAGE':
                issues.append(issue('P1','LAST_PAGE_STATUS','Last partial page not marked FINAL_PARTIAL_PAGE',str(p)))

    if canonical.get('manual_render_qa') not in (True,'CONFIRMED'):
        issues.append(issue('P1','MANUAL_RENDER_QA_REQUIRED','Word/WPS/PDF visual QA not confirmed',str(appp)))

    counts={'P0':0,'P1':0,'P2':0}
    for x in issues:
        counts[x['level']]=counts.get(x['level'],0)+1
    status='READY_FOR_SUBMISSION' if counts['P0']==0 and counts['P1']==0 else 'HOLD_FOR_FIXES'
    payload={'schema_version':1,'status':status,'counts':counts,'canonical':canonical,'issues':issues,'limitations':['Does not visually render DOCX/PDF.','Does not determine legal ownership.','Absence of a string conflict is not proof of substantive correctness.']}

    outj=appp.parent/args.out_json
    outj.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    md=['# 最终一致性审计','',f'**状态：{status}**','',f"P0={counts['P0']} / P1={counts['P1']} / P2={counts['P2']}",'','## 问题']
    if not issues:
        md.append('- 无自动检测问题。')
    else:
        for x in issues:
            md.append(f"- **{x['level']} {x['code']}** — {x['message']} `{x['source']}`")
    md += ['','## 边界','- 本脚本不替代 Word/WPS/PDF 视觉检查。','- 本脚本不作著作权归属法律判断。']
    outm=appp.parent/args.out_md
    outm.write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(outj); print(outm)
    return 0 if status=='READY_FOR_SUBMISSION' else 2

if __name__=='__main__':
    raise SystemExit(main())
