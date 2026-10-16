#!/usr/bin/env python3
"""Recompute LOC and hashes for confirmed selected first-party files."""
from __future__ import annotations
import argparse, csv, hashlib, json
from pathlib import Path

def digest(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('project'); ap.add_argument('selection'); ap.add_argument('--out',default='FIRST_PARTY_LOC_AUDIT.json'); ap.add_argument('--csv-out',default='FIRST_PARTY_LOC_AUDIT.csv'); args=ap.parse_args()
    root=Path(args.project).resolve(); selp=Path(args.selection).resolve(); sel=json.loads(selp.read_text(encoding='utf-8'))
    rows=[]; missing=[]
    for rec in sel.get('files',[]):
        if not rec.get('selected'): continue
        if rec.get('ownership_status') not in ('FIRST_PARTY','APPLICANT_CONFIRMED','VERIFIED_FIRST_PARTY'): continue
        p=root/rec['path']
        if not p.is_file(): missing.append(rec['path']); continue
        txt=p.read_text(encoding='utf-8',errors='replace'); lines=txt.splitlines()
        rows.append({'path':rec['path'],'loc':len(lines),'nonblank_loc':sum(bool(x.strip()) for x in lines),'sha256':digest(p)})
    payload={'schema_version':1,'project_root':str(root),'selection':str(selp),'first_party_files':len(rows),'first_party_loc':sum(r['loc'] for r in rows),'first_party_nonblank_loc':sum(r['nonblank_loc'] for r in rows),'missing':missing,'files':rows}
    out=selp.parent/args.out; out.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    co=selp.parent/args.csv_out
    with co.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=['path','loc','nonblank_loc','sha256']); w.writeheader(); w.writerows(rows)
    print(out); print(co)
    if not rows:
        print('WARNING: no selected file marked FIRST_PARTY/APPLICANT_CONFIRMED')
        return 2
    return 1 if missing else 0
if __name__=='__main__': raise SystemExit(main())
