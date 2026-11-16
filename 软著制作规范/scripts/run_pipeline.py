#!/usr/bin/env python3
"""Safe stage runner for the software-copyright preparation scripts.

It stops at human/legal fact gates rather than guessing ownership, dates, publication
status or first-party code. Later stages automate DOCX generation, real pagination QA
and clean submission package construction.
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

    b=sub.add_parser('bootstrap')
    b.add_argument('project'); b.add_argument('--profile',choices=['auto','gui','cli','sdk'],default='auto')

    p=sub.add_parser('post-confirm')
    p.add_argument('project'); p.add_argument('selection')

    d=sub.add_parser('build-docx')
    d.add_argument('--project',required=True); d.add_argument('--facts',required=True); d.add_argument('--manual-md',required=True)
    d.add_argument('--selection',required=True); d.add_argument('--screenshots'); d.add_argument('--out-dir',required=True)
    d.add_argument('--code-lines-per-page',type=int,default=50)

    q=sub.add_parser('render-qa')
    q.add_argument('--docx',required=True); q.add_argument('--out-dir',required=True); q.add_argument('--kind',choices=['manual','source'],required=True)
    q.add_argument('--source-map'); q.add_argument('--header-text'); q.add_argument('--min-source-lines',type=int,default=50)

    a=sub.add_parser('audit')
    a.add_argument('--application',required=True); a.add_argument('--manual',action='append',default=[]); a.add_argument('--source-map')

    k=sub.add_parser('package')
    k.add_argument('--facts',required=True); k.add_argument('--manual-docx',required=True); k.add_argument('--manual-pdf')
    k.add_argument('--source-docx',required=True); k.add_argument('--source-pdf'); k.add_argument('--screenshots-dir')
    k.add_argument('--internal-dir',action='append',default=[]); k.add_argument('--out-dir',required=True); k.add_argument('--require-pdf',action='store_true')

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

    if args.stage=='build-docx':
        cmd=[sys.executable,str(HERE/'build_docx_materials.py'),'--project',args.project,'--facts',args.facts,'--manual-md',args.manual_md,'--selection',args.selection,'--out-dir',args.out_dir,'--code-lines-per-page',str(args.code_lines_per_page)]
        if args.screenshots: cmd += ['--screenshots',args.screenshots]
        print('+',' '.join(cmd)); return subprocess.run(cmd).returncode

    if args.stage=='render-qa':
        cmd=[sys.executable,str(HERE/'render_pagination_qa.py'),args.docx,'--out-dir',args.out_dir,'--kind',args.kind,'--min-source-lines',str(args.min_source_lines)]
        if args.source_map: cmd += ['--source-map',args.source_map]
        if args.header_text: cmd += ['--header-text',args.header_text]
        print('+',' '.join(cmd)); return subprocess.run(cmd).returncode

    if args.stage=='audit':
        cmd=[sys.executable,str(HERE/'final_consistency_audit.py'),'--application',args.application]
        for m in args.manual: cmd += ['--manual',m]
        if args.source_map: cmd += ['--source-map',args.source_map]
        print('+',' '.join(cmd)); return subprocess.run(cmd).returncode

    if args.stage=='package':
        cmd=[sys.executable,str(HERE/'build_submission_package.py'),'--facts',args.facts,'--manual-docx',args.manual_docx,'--source-docx',args.source_docx,'--out-dir',args.out_dir]
        if args.manual_pdf: cmd += ['--manual-pdf',args.manual_pdf]
        if args.source_pdf: cmd += ['--source-pdf',args.source_pdf]
        if args.screenshots_dir: cmd += ['--screenshots-dir',args.screenshots_dir]
        for d in args.internal_dir: cmd += ['--internal-dir',d]
        if args.require_pdf: cmd += ['--require-pdf']
        print('+',' '.join(cmd)); return subprocess.run(cmd).returncode

    return 0

if __name__=='__main__':
    raise SystemExit(main())
