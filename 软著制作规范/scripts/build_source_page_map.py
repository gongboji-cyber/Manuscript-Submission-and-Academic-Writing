#!/usr/bin/env python3
"""Build a deterministic virtual source-page map from confirmed first-party files.

This script never creates or pads code. It only maps real selected source lines to
nominal pages for later comparison with the rendered Word/PDF material.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('project')
    ap.add_argument('selection')
    ap.add_argument('--lines-per-page',type=int,default=50)
    ap.add_argument('--out',default='SOURCE_PAGE_MAP.csv')
    ap.add_argument('--meta-out',default='SOURCE_PAGE_MAP.json')
    args=ap.parse_args()
    if args.lines_per_page<1: raise SystemExit('lines-per-page must be >=1')
    root=Path(args.project).resolve()
    sp=Path(args.selection).resolve()
    data=json.loads(sp.read_text(encoding='utf-8'))
    streams=[]
    for rec in data.get('files',[]):
        if not rec.get('selected'): continue
        if rec.get('ownership_status') not in ('FIRST_PARTY','APPLICANT_CONFIRMED','VERIFIED_FIRST_PARTY'): continue
        p=root/rec['path']
        if not p.is_file(): raise SystemExit(f'missing selected file: {rec["path"]}')
        streams.append((rec['path'],p.read_text(encoding='utf-8',errors='replace').splitlines()))
    if not streams: raise SystemExit('no confirmed first-party selected files')
    pages=[]; page_no=1; used=0; pieces=[]
    def flush():
        nonlocal page_no,used,pieces
        if not pieces: return
        pages.append({'page':page_no,'rendered_code_lines':used,'segments':' | '.join(pieces),'continuity_status':'FINAL_PARTIAL_PAGE' if used<args.lines_per_page else 'FULL_PAGE'})
        page_no+=1; used=0; pieces=[]
    for path,lines in streams:
        i=0
        while i<len(lines):
            take=min(args.lines_per_page-used,len(lines)-i)
            start=i+1; end=i+take
            pieces.append(f'{path}:{start}-{end}')
            used+=take; i=end
            if used==args.lines_per_page: flush()
    flush()
    out=sp.parent/args.out
    with out.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=['page','rendered_code_lines','segments','continuity_status']); w.writeheader(); w.writerows(pages)
    meta={'schema_version':1,'nominal_lines_per_page':args.lines_per_page,'total_code_lines':sum(len(x[1]) for x in streams),'nominal_pages':len(pages),'deposit_mode':'ALL' if len(pages)<60 else 'FRONT30_BACK30','note':'Nominal map only; final DOCX/PDF pagination requires rendered QA.','files':[{'path':p,'lines':len(lines)} for p,lines in streams]}
    mo=sp.parent/args.meta_out
    mo.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    print(out); print(mo)
    return 0

if __name__=='__main__':
    raise SystemExit(main())
