#!/usr/bin/env python3
"""Verify this offline handoff from any working directory."""
import sys
if not __debug__:
    raise RuntimeError('Optimized Python is refused.')
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
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
    manifest_files=verify_manifest()
    replay=[]
    with tempfile.TemporaryDirectory(prefix='full-slack-replay-') as cwd:
        for script,log in [('checker.py','primary'),('test_mutations.py','mutations'),('audit_exact.py','audit')]:
            proc=subprocess.run([sys.executable,'-I','-B',str(ROOT/script)],cwd=cwd,capture_output=True,timeout=45)
            if proc.returncode or proc.stderr:raise RuntimeError(script+' failed: '+proc.stderr.decode(errors='replace'))
            data=json.loads(proc.stdout)
            expected=json.loads((ROOT/'logs'/f'{log}.stdout.json').read_text())
            if data!=expected:raise RuntimeError(script+' output differs from recorded successful JSON')
            replay.append({'script':script,'status':'PASS','recorded_JSON_matches':True})
        proc=subprocess.run([sys.executable,'-I','-B','-O',str(ROOT/'checker.py')],cwd=cwd,capture_output=True,timeout=45)
        if proc.returncode==0 or b'Optimized Python is refused' not in proc.stderr:raise RuntimeError('Optimized-run control failed')
        proc=subprocess.run([sys.executable,'-I','-B',str(ROOT/'test_packaging.py')],cwd=cwd,capture_output=True,timeout=45)
        if proc.returncode or proc.stderr:raise RuntimeError('test_packaging.py failed: '+proc.stderr.decode(errors='replace'))
        packaging=json.loads(proc.stdout)
        if packaging['status']!='PASS':raise RuntimeError('Packaging controls failed')
    print(json.dumps({'status':'PASS','manifest_files':manifest_files,'fresh_working_directory_replay':replay,'packaging_controls':packaging,'optimized_execution':'REJECTED_AS_EXPECTED','offline':True,'scope':'New handoff verification, not a full replay of the upstream historical verifier.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
