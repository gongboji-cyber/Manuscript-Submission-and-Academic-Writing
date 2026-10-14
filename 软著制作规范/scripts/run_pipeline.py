#!/usr/bin/env python3
"""Safe stage runner for the software-copyright preparation scripts.

It intentionally stops at human/legal fact gates rather than guessing ownership,
dates or publication status.
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent

def run(name,*args):
    cmd=[sys.executable,str(HERE/name),*map(str,args)]
    print('+',' '.join(cmd))
    subprocess.run(cmd,check=True)

def main()->int:
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='stage',required=True)
    b=sub.add_parser('bootstrap'); b.add_argument('project'); b.add_argument('--profile',choices=['auto','gui','cli','sdk'],default='auto')
    p=sub.add_parser('post-confirm'); p.add_argument('project'); p.add_argument('selection')
    a=sub.add_parser('audit'); a.add_argument('--application',required=True); a.add_argument('--manual',action='append',default=[]); a.add_argument('--source-map')
    args=ap.parse_args()
    if args.stage=='bootstrap':
        root=Path(args.project).resolve()
        run('init_workspace.py',root)
        run('scan_project.py',root)
        inv=root/'软件著作权申请资料/01_项目证据/project-inventory.json'
        run('propose_code_selection.py',inv,'--profile',args.profile)
        print('STOP_AT_GATE: review 业务理解/权属/代码候选，并把选中文件 ownership_status 标记为申请人确认的第一方状态。')
        return 0
    if args.stage=='post-confirm':
        sel=Path(args.selection).resolve(); data=json.loads(sel.read_text(encoding='utf-8'))
        bad=[r['path'] for r in data.get('files',[]) if r.get('selected') and r.get('ownership_status') not in ('FIRST_PARTY','APPLICANT_CONFIRMED','VERIFIED_FIRST_PARTY')]
        if bad: raise SystemExit('selected files still unverified: '+', '.join(bad[:10]))
        run('count_first_party_loc.py',Path(args.project).resolve(),sel)
        run('build_source_page_map.py',Path(args.project).resolve(),sel)
        return 0
    if args.stage=='audit':
        cmd=[sys.executable,str(HERE/'final_consistency_audit.py'),'--application',args.application]
        for m in args.manual: cmd += ['--manual',m]
        if args.source_map: cmd += ['--source-map',args.source_map]
        print('+',' '.join(cmd))
        return subprocess.run(cmd).returncode
    return 0
if __name__=='__main__': raise SystemExit(main())
