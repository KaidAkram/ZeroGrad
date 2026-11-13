"""Publish the reviewed export while retaining the remote's initial history.

Run in a user terminal with GitHub network access. No tokens are accepted or printed.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPOSITORY='https://github.com/KaidAkram/ZeroGrad.git'
EXPECTED_HEAD='a67c1420a89c64ec15b0846527f782b8b231d7ed'

def git(*args,cwd=None,capture=False):
    return subprocess.run(['git',*args],cwd=cwd,check=True,text=True,
                          stdout=subprocess.PIPE if capture else None).stdout

def publish(dry_run=False):
    export=(ROOT/'.publish/ZeroGrad').resolve()
    package_path=ROOT/'.publish/PACKAGE_MANIFEST.json'
    if not package_path.exists():raise RuntimeError('Run python scripts/package_release.py first.')
    package=json.loads(package_path.read_text(encoding='utf-8'))
    for item in package['artifacts']:
        source=(export/item['path']).resolve()
        if not source.is_relative_to(export):raise RuntimeError('Unsafe export path')
        if hashlib.sha256(source.read_bytes()).hexdigest()!=item['sha256']:
            raise RuntimeError('Export changed: '+item['path']+'; rebuild the package.')
    print(f"Verified {package['files']} exported files for KaidAkram/ZeroGrad.",flush=True)
    if dry_run:
        print('Dry run passed. No network requests, commits or pushes performed.');return
    if not shutil.which('git'):raise RuntimeError('Install Git from git-scm.com first.')
    checkout=Path(tempfile.mkdtemp(prefix='ZeroGrad-Publish-'))/'ZeroGrad'
    git('clone','--branch','main','--single-branch',REPOSITORY,str(checkout))
    actual=git('rev-parse','HEAD',cwd=checkout,capture=True).strip()
    if actual!=EXPECTED_HEAD:
        raise RuntimeError(f'Remote changed since inspection. Review {checkout}; nothing was pushed.')
    for item in package['artifacts']:
        target=(checkout/item['path']).resolve()
        if not target.is_relative_to(checkout.resolve()) or '.git' in Path(item['path']).parts:
            raise RuntimeError('Unsafe publication path')
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(export/item['path'],target)
    git('config','user.name','Akram Kaid',cwd=checkout)
    git('config','user.email','KaidAkram@users.noreply.github.com',cwd=checkout)
    git('add','--all',cwd=checkout)
    git('commit','-m','Build ZeroGrad-Sec research prototype, evidence studio and visual documentation',cwd=checkout)
    git('push','origin','main',cwd=checkout)
    local=git('rev-parse','HEAD',cwd=checkout,capture=True).strip()
    remote=git('ls-remote','origin','refs/heads/main',cwd=checkout,capture=True).strip().split()[0]
    if remote!=local:raise RuntimeError('Remote verification failed; check GitHub before retrying.')
    print(f'Verified published commit: https://github.com/KaidAkram/ZeroGrad/commit/{local}')
    print(f'Local publication checkout retained at: {checkout}')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    publish(parser.parse_args().dry_run)
