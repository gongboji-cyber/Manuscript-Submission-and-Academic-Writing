#!/usr/bin/env python3
"""Propose, never auto-confirm, first-party source candidates from scan_project output."""
from __future__ import annotations
import argparse, json
from pathlib import Path

EXCLUDE_TOKENS=('test/','tests/','__tests__/','fixtures/','vendor/','third_party/','third-party/','generated/','migrations/','examples/')
PROFILE_HINTS={
 'cli':('cli','command','main','core','benchmark','pipeline','io','config','report','visual','metric','service'),
 'gui':('main','app','page','view','screen','component','router','store','api','service','controller','model'),
 'sdk':('api','client','core','service','protocol','schema','model','types','util'),
 'auto':('main','app','core','service','controller','model','io','cli','api','report','pipeline')
}

def score(path:str,loc:int,profile:str)->tuple[int,list[str]]:
    low=path.lower(); s=0; why=[]
    if any(t in low for t in EXCLUDE_TOKENS): return -999,['test/example/vendor/generated path']
    if '/src/' in '/'+low or low.startswith('src/'): s+=6; why.append('src tree')
    if low.startswith(('app/','lib/','server/','client/','scripts/')): s+=2; why.append('software tree')
    for kw in PROFILE_HINTS[profile]:
        if kw in low: s+=2; why.append(f'profile:{kw}')
    if loc>=50: s+=2; why.append('substantive LOC')
    if loc>=200: s+=1
    if any(x in low for x in ('__init__.py','index.ts','index.js')): s+=1; why.append('entry/namespace')
    return s,why

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('inventory'); ap.add_argument('--profile',choices=PROFILE_HINTS,default='auto'); ap.add_argument('--max-files',type=int,default=80); ap.add_argument('--out-json',default='代码文件选择.json'); ap.add_argument('--out-md',default='代码文件候选清单.md'); args=ap.parse_args()
    inv_path=Path(args.inventory).resolve(); data=json.loads(inv_path.read_text(encoding='utf-8')); base=inv_path.parent
    cand=[]
    for r in data.get('files',[]):
        if r.get('kind')!='source': continue
        sc,why=score(r['path'],int(r.get('loc',0)),args.profile)
        cand.append({**r,'score':sc,'recommended':sc>=2,'reason':'; '.join(dict.fromkeys(why)) or 'source file; manual review needed','ownership_status':'UNVERIFIED'})
    cand.sort(key=lambda x:(x['score'],x.get('loc',0)),reverse=True); cand=cand[:args.max_files]
    selection={'schema_version':1,'profile':args.profile,'status':'PROPOSAL_ONLY_NOT_CONFIRMED','source_inventory':str(inv_path),'files':cand,
               'instructions':['Applicant/model must review first-party ownership and generated/third-party status.','Set selected=true only after review; this script never proves copyright ownership.']}
    for r in selection['files']: r['selected']=bool(r['recommended'])
    jout=base/args.out_json; jout.write_text(json.dumps(selection,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 代码文件候选清单','',f'- Profile: `{args.profile}`','- 状态：**PROPOSAL_ONLY_NOT_CONFIRMED**','', '|选择建议|文件|语言|LOC|分数|理由|权属|','|---|---|---:|---:|---:|---|---|']
    for r in cand:
        lines.append(f"|{'是' if r['recommended'] else '否'}|`{r['path']}`|{r.get('language','')}|{r.get('loc',0)}|{r['score']}|{r['reason']}|UNVERIFIED|")
    lines += ['', '> 此清单是技术候选，不是著作权归属结论。确认前不得据此生成“最终”鉴别材料。']
    mout=base/args.out_md; mout.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(jout); print(mout); return 0
if __name__=='__main__': raise SystemExit(main())
