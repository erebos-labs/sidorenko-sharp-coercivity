#!/usr/bin/env python3
"""Regression controls for exact manifest inventory; temporary copies only."""
import sys
if not __debug__:
    raise RuntimeError('Optimized Python is refused.')
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('package_verifier',ROOT/'verify_package.py')
verifier=importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)

def main():
    controls=[]
    original=(ROOT/'SHA256SUMS').read_text()
    first=original.splitlines()[0]
    def reject(name,change,prefix):
        with tempfile.TemporaryDirectory(prefix='full-slack-inventory-control-') as tmp:
            root=Path(tmp)/'package';shutil.copytree(ROOT,root)
            change(root)
            # The actual CLI must stop before any mathematical subprocess.
            proc=subprocess.run([sys.executable,'-I','-B',str(root/'verify_package.py')],cwd=tmp,capture_output=True,timeout=10)
            if proc.returncode==0 or prefix.encode() not in proc.stderr:
                raise RuntimeError('Unexpected control result: '+name+' '+proc.stderr.decode(errors='replace'))
            if proc.stdout:raise RuntimeError('Rejected inventory emitted successful stdout: '+name)
            controls.append({'name':name,'expected_failure':prefix,'status':'REJECTED_AS_EXPECTED'})
    positive=verifier.verify_manifest(ROOT)
    def extra(rel):
        def change(root):
            path=root/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('unexpected\n')
        return change
    reject('duplicate manifest entry',lambda r:(r/'SHA256SUMS').write_text(original+first+'\n'),'Duplicate manifest entry:')
    reject('unexpected ordinary file',extra('unlisted.txt'),'Manifest inventory mismatch')
    reject('unexpected nested SHA256SUMS',extra('sources/SHA256SUMS'),'Manifest inventory mismatch')
    reject('unexpected file under __pycache__',extra('__pycache__/unlisted.txt'),'Manifest inventory mismatch')
    reject('unexpected nested cache file',extra('sources/__pycache__/unlisted.pyc'),'Manifest inventory mismatch')
    reject('missing manifest',lambda r:(r/'SHA256SUMS').unlink(),'Missing SHA256SUMS')
    reject('missing listed proof',lambda r:(r/'THEOREM.md').unlink(),'Missing manifest file: THEOREM.md')
    reject('changed listed proof',lambda r:(r/'THEOREM.md').write_bytes((r/'THEOREM.md').read_bytes()+b'\n'),'SHA256 mismatch: THEOREM.md')
    reject('invalid digest',lambda r:(r/'SHA256SUMS').write_text('g'*64+original[64:]),'Malformed manifest digest')
    reject('malformed line',lambda r:(r/'SHA256SUMS').write_text('malformed\n'),'Malformed manifest entry')
    reject('parent traversal',lambda r:(r/'SHA256SUMS').write_text('0'*64+'  ../outside\n'),'Invalid manifest path:')
    reject('absolute path',lambda r:(r/'SHA256SUMS').write_text('0'*64+'  /outside\n'),'Invalid manifest path:')
    reject('noncanonical path',lambda r:(r/'SHA256SUMS').write_text('0'*64+'  sources//openai/LICENSE\n'),'Invalid manifest path:')
    reject('backslash path',lambda r:(r/'SHA256SUMS').write_text('0'*64+'  sources\\openai\\LICENSE\n'),'Invalid manifest path:')
    reject('self-listed manifest',lambda r:(r/'SHA256SUMS').write_text('0'*64+'  SHA256SUMS\n'),'Manifest cannot list itself')
    reject('unexpected file symlink',lambda r:(r/'unlisted-link').symlink_to('THEOREM.md'),'Symbolic link in package:')
    reject('unexpected directory symlink',lambda r:(r/'unlisted-dir').symlink_to('sources',target_is_directory=True),'Symbolic link in package:')
    reject('symlinked manifest',lambda r:((r/'SHA256SUMS').rename(r/'manifest-data'),(r/'SHA256SUMS').symlink_to('manifest-data')),'Symbolic link in package: SHA256SUMS')
    print(json.dumps({'status':'PASS','clean_inventory_files':positive,'positive_controls':1,'rejection_controls':len(controls),'controls':controls,'scope':'Exact inventory regressions; no mathematical premises changed.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
