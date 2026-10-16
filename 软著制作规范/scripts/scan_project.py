#!/usr/bin/env python3
"""Scan a real software project into an evidence-oriented inventory.

Stdlib-only. The scanner deliberately does not decide copyright ownership; it only
collects reproducible file facts for later model/applicant review.
"""
from __future__ import annotations

import argparse, csv, hashlib, json
from pathlib import Path

EXCLUDED_DIRS={'.git','.hg','.svn','node_modules','venv','.venv','env','dist','build','target','__pycache__','.pytest_cache','.mypy_cache','.idea','.vscode','vendor'}
DOC_EXTS={'.md','.rst','.txt','.pdf','.doc','.docx','.odt','.wps'}
CONFIG_EXTS={'.json','.yaml','.yml','.toml','.ini','.cfg','.lock','.xml','.properties','.env'}
BINARY_EXTS={'.png','.jpg','.jpeg','.gif','.webp','.bmp','.ico','.pdf','.zip','.7z','.rar','.gz','.tar','.jar','.class','.dll','.exe','.so','.dylib','.bin','.woff','.woff2','.ttf','.otf','.mp3','.mp4','.avi','.mov','.npy','.npz','.h5','.hdf5','.parquet'}
LANG_BY_EXT={
 '.py':'Python','.js':'JavaScript','.jsx':'JavaScript','.ts':'TypeScript','.tsx':'TypeScript','.java':'Java','.kt':'Kotlin','.kts':'Kotlin',
 '.c':'C','.h':'C/C++','.cc':'C++','.cpp':'C++','.cxx':'C++','.hpp':'C++','.cs':'C#','.go':'Go','.rs':'Rust','.rb':'Ruby','.php':'PHP',
 '.swift':'Swift','.m':'Objective-C','.mm':'Objective-C++','.r':'R','.R':'R','.scala':'Scala','.dart':'Dart','.vue':'Vue','.svelte':'Svelte',
 '.html':'HTML','.css':'CSS','.scss':'SCSS','.sql':'SQL','.sh':'Shell','.bash':'Shell','.ps1':'PowerShell','.bat':'Batch','.cmd':'Batch'
}

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def text_probe(path:Path,limit:int=65536)->tuple[bool,str]:
    try: data=path.read_bytes()[:limit]
    except OSError: return False,''
    if b'\x00' in data: return False,''
    for enc in ('utf-8','utf-8-sig','gb18030','latin-1'):
        try: return True,data.decode(enc)
        except UnicodeDecodeError: pass
    return False,''

def classify(path:Path,text:str)->tuple[str,str]:
    ext=path.suffix; low=ext.lower()
    lang=LANG_BY_EXT.get(ext) or LANG_BY_EXT.get(low) or ''
    if low in DOC_EXTS: return 'document',lang
    if low in CONFIG_EXTS: return 'config',lang
    if low in BINARY_EXTS: return 'binary',lang
    if lang: return 'source',lang
    head=text.lstrip()[:200].lower()
    if head.startswith('#!') and 'python' in head: return 'source','Python'
    if head.startswith('#!') and any(x in head for x in ('bash','sh','zsh')): return 'source','Shell'
    if text: return 'text-unknown',''
    return 'binary',''

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('project')
    ap.add_argument('--out',default='软件著作权申请资料/01_项目证据/project-inventory.json')
    ap.add_argument('--csv-out',default='软件著作权申请资料/01_项目证据/project-inventory.csv')
    ap.add_argument('--max-file-mb',type=float,default=10.0)
    args=ap.parse_args()
    root=Path(args.project).resolve()
    if not root.is_dir(): raise SystemExit(f'project not found: {root}')
    rows=[]
    for p in sorted(root.rglob('*')):
        if not p.is_file(): continue
        rel=p.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts): continue
        try: size=p.stat().st_size
        except OSError: continue
        if size>args.max_file_mb*1024*1024:
            rows.append({'path':rel.as_posix(),'size':size,'sha256':'','kind':'oversize-skipped','language':'','loc':0,'nonblank_loc':0})
            continue
        is_text,preview=text_probe(p)
        kind,lang=classify(p,preview if is_text else '')
        loc=nonblank=0
        if is_text:
            try: txt=p.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                try: txt=p.read_text(encoding='gb18030')
                except Exception: txt=preview
            lines=txt.splitlines(); loc=len(lines); nonblank=sum(1 for x in lines if x.strip())
        rows.append({'path':rel.as_posix(),'size':size,'sha256':sha256(p),'kind':kind,'language':lang,'loc':loc,'nonblank_loc':nonblank})
    summary={'project_root':str(root),'file_count':len(rows),'source_files':sum(r['kind']=='source' for r in rows),'source_loc':sum(r['loc'] for r in rows if r['kind']=='source'),'languages':{}}
    for r in rows:
        if r['kind']=='source' and r['language']:
            summary['languages'][r['language']]=summary['languages'].get(r['language'],0)+r['loc']
    payload={'schema_version':1,'summary':summary,'files':rows,'limitations':['Inventory is technical evidence only; it does not prove ownership/authorship.','Unknown text files require model/applicant review before inclusion.']}
    out=root/args.out; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    cout=root/args.csv_out; cout.parent.mkdir(parents=True,exist_ok=True)
    with cout.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=['path','size','sha256','kind','language','loc','nonblank_loc']); w.writeheader(); w.writerows(rows)
    print(out); print(cout); return 0
if __name__=='__main__': raise SystemExit(main())
