#!/usr/bin/env python3
"""Optional byte binding of an independently supplied retained manuscript.

MIT License, copyright (c) 2026 Erebos Labs. Reads one local file only.
No fetch, redistribution, source execution or theorem-sized allocation occurs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

def main():
    if not __debug__:raise RuntimeError('Optimized Python is refused.')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('path',type=Path)
    args=ap.parse_args()
    b=args.path.read_bytes()
    if len(b)!=80925:raise RuntimeError('External source length mismatch')
    if hashlib.sha256(b).hexdigest()!='20c917f8fbab9cc51a92d0a4c853ca2080541a9a15c116bd3343150993aaf031':
        raise RuntimeError('External source SHA256 mismatch')
    g=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if g!='e5f1aaef9c3020054f0221a5b5dedc8260d5d5e4':raise RuntimeError('External source Git blob mismatch')
    print(json.dumps({'status':'PASS','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha1':g,'source_executed':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
