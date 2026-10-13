#!/usr/bin/env python3
"""Verify manifest, then replay exact checks and mutation controls offline."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def verify_manifest(root=ROOT):
    root=Path(root).resolve()
    manifest=root/'SHA256SUMS'
    if manifest.is_symlink():raise RuntimeError('Symbolic link in package: SHA256SUMS')
    if not manifest.is_file():raise RuntimeError('Missing SHA256SUMS')
    listed=set()
    for line in manifest.read_text().splitlines():
        if '  ' not in line:raise RuntimeError('Malformed manifest entry')
        digest,rel=line.split('  ',1)
        if not re.fullmatch('[0-9a-f]{64}',digest):raise RuntimeError('Malformed manifest digest')
        logical=PurePosixPath(rel)
        if (not rel or logical.is_absolute() or '..' in logical.parts
                or '\\' in rel or logical.as_posix()!=rel):
            raise RuntimeError('Invalid manifest path: '+rel)
        if rel=='SHA256SUMS':raise RuntimeError('Manifest cannot list itself')
        if rel in listed:raise RuntimeError('Duplicate manifest entry: '+rel)
        path=root/rel
        if path.is_symlink():raise RuntimeError('Symbolic link in package: '+rel)
        if not path.resolve().is_relative_to(root):raise RuntimeError('Manifest path outside package')
        if not path.is_file():raise RuntimeError('Missing manifest file: '+rel)
        if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise RuntimeError('SHA256 mismatch: '+rel)
        listed.add(rel)
    actual=set()
    for path in root.rglob('*'):
        rel=path.relative_to(root).as_posix()
        if path.is_symlink():raise RuntimeError('Symbolic link in package: '+rel)
        if path.is_file() and path!=manifest:actual.add(rel)
        elif not path.is_dir() and path!=manifest:raise RuntimeError('Nonregular package entry: '+rel)
    if listed!=actual:raise RuntimeError('Manifest inventory mismatch')
    return len(listed)


def main():
    if not __debug__:raise RuntimeError('Run without -O or -OO.')
    manifest_files=verify_manifest()
    runs=[]
    with tempfile.TemporaryDirectory(prefix='sidorenko-defect-replay-') as td:
        for script,log in [('check_exact.py','primary'),('test_mutations.py','mutations')]:
            r=subprocess.run([sys.executable,'-I','-B',str(ROOT/script)],cwd=td,capture_output=True,timeout=180)
            if r.returncode!=0:raise RuntimeError(script+' failed: '+r.stderr.decode())
            if r.stdout!=(ROOT/f'logs/{log}.stdout.json').read_bytes():
                raise RuntimeError(script+' output differs from executed expectation.')
            if r.stderr!=(ROOT/f'logs/{log}.stderr.txt').read_bytes():
                raise RuntimeError(script+' stderr differs from executed expectation.')
            runs.append({'script':script,'exit_code':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),
                         'byte_identical':True})
        r=subprocess.run([sys.executable,'-I','-B',str(ROOT/'test_packaging.py')],cwd=td,capture_output=True,timeout=60)
        if r.returncode or r.stderr:raise RuntimeError('Packaging regressions failed: '+r.stderr.decode())
        packaging=json.loads(r.stdout)
        if packaging['status']!='PASS':raise RuntimeError('Packaging regression status failed.')
    print(json.dumps({'status':'PASS','manifest_files':manifest_files,'offline':True,'runs':runs,'packaging_controls':packaging,
          'scope':'This handoff only; not an upstream historical verifier or formal proof.'},indent=2))
if __name__=='__main__':main()
