"""Create an audited publication export, excluding caches and generated duplicates."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','.venv','node_modules','__pycache__','.pytest_cache','.publish'}
SKIP_PREFIXES=('studio/dist/','studio/public/data/','studio/public/media/')

def public_files():
    for directory,dirs,files in os.walk(ROOT):
        dirs[:]=[d for d in dirs if d not in SKIP]
        for filename in sorted(files):
            p=Path(directory)/filename;rel=p.relative_to(ROOT).as_posix()
            if rel.startswith(SKIP_PREFIXES):continue
            if filename.startswith('.env') or p.suffix in {'.log','.pyc','.pyo','.ckpt','.safetensors','.pt','.pth'}:continue
            yield p,rel

def main():
    # Retain test outcomes while omitting an unnecessary private machine identifier.
    test_xml=ROOT/'outputs'/'test_results.xml'
    if test_xml.exists():
        tree=ET.parse(test_xml)
        for suite in tree.getroot().iter('testsuite'):suite.attrib.pop('hostname',None)
        tree.write(test_xml,encoding='utf-8',xml_declaration=True)
    # Manifest must describe the final source/export, including the redacted XML.
    subprocess.run([sys.executable,'run_all.py','--mode','release-check'],cwd=ROOT,check=True,timeout=180)
    export=ROOT/'.publish'/'ZeroGrad'
    export.mkdir(parents=True,exist_ok=True)
    # Refuse a stale export, so removed source files cannot quietly survive a rerun.
    allowed={rel for _,rel in public_files()}
    stale=[p.relative_to(export).as_posix() for p in export.rglob('*') if p.is_file() and p.relative_to(export).as_posix() not in allowed]
    if stale:raise RuntimeError('Stale export files need review: '+', '.join(stale))
    patterns=[('GitHub token',r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b'),
              ('fine-grained token',r'\bgithub_pat_[A-Za-z0-9_]{50,}\b'),
              ('private key',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
              ('cloud access key',r'\bAKIA[0-9A-Z]{16}\b')]
    failures=[];manifest=[]
    for source,rel in public_files():
        data=source.read_bytes()
        if len(data)>25*1024*1024:failures.append((rel,'over GitHub web-upload file limit'))
        if b'\x00' not in data[:4096]:
            text=data.decode('utf-8',errors='ignore')
            for name,pattern in patterns:
                if re.search(pattern,text):failures.append((rel,name))
        dest=export/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
        manifest.append(dict(path=rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    if failures:raise RuntimeError('Publication preflight stopped (values not displayed): '+repr(failures))
    archive=ROOT/'.publish'/'ZeroGrad-ready-to-publish.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for item in sorted(manifest,key=lambda v:v['path']):z.write(export/item['path'],item['path'])
    info=dict(repository='https://github.com/KaidAkram/ZeroGrad',files=len(manifest),bytes=sum(m['bytes'] for m in manifest),archive_bytes=archive.stat().st_size,archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),secret_pattern_matches=0,artifacts=manifest)
    (ROOT/'.publish'/'PACKAGE_MANIFEST.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
    print(f"Publication export: {len(manifest)} files, {info['bytes']} bytes; secret-pattern matches: 0")
    print('Archive: .publish/ZeroGrad-ready-to-publish.zip')

if __name__=='__main__':main()
