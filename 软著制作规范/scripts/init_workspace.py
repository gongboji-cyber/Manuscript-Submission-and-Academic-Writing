#!/usr/bin/env python3
"""Create the standard software-copyright evidence workspace without overwriting files."""
from __future__ import annotations
import argparse, json
from pathlib import Path

DIRS=[
 '00_状态与索引','01_项目证据','02_草稿','03_截图/原始','03_截图/正式','04_正式资料/PDF','05_内部审计',
 '06_开发证据链_可选/provenance','06_开发证据链_可选/timeline','06_开发证据链_可选/tests','06_开发证据链_可选/regression','06_开发证据链_可选/release','06_开发证据链_可选/hashes'
]

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('project'); ap.add_argument('--name',default='软件著作权申请资料'); args=ap.parse_args()
    root=Path(args.project).resolve(); ws=root/args.name
    for d in DIRS: (ws/d).mkdir(parents=True,exist_ok=True)
    status=ws/'00_状态与索引'/'STATUS.json'
    if not status.exists():
        status.write_text(json.dumps({'schema_version':1,'state':'WORKSPACE_INITIALIZED','gates':{'BUSINESS_UNDERSTANDING_CONFIRMED':'PENDING','APPLICATION_FACTS_CONFIRMED':'PENDING','CODE_SELECTION_CONFIRMED':'PENDING','SCREENSHOT_PLAN_CONFIRMED':'PENDING','FINAL_DRAFT_CONFIRMED':'PENDING','MANUAL_RENDER_QA':'PENDING'}},ensure_ascii=False,indent=2),encoding='utf-8')
    readme=ws/'00_状态与索引'/'README.md'
    if not readme.exists():
        readme.write_text('# 软件著作权申请资料工作区\n\n正式资料与内部审计分离。此目录不会自动证明权属，也不会自动提交登记。\n',encoding='utf-8')
    print(ws); return 0
if __name__=='__main__': raise SystemExit(main())
