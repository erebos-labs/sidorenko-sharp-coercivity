#!/usr/bin/env python3
"""Optional explicit read of the pinned external proof, outside this package."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--destination',type=Path,required=True)
    args=ap.parse_args();dst=args.destination.expanduser().resolve()
    if dst==ROOT or ROOT in dst.parents:
        raise SystemExit('Destination must be outside the handoff directory.')
    rec=json.loads((ROOT/'SOURCES.json').read_text())['external_retained_input']
    url='https://raw.githubusercontent.com/{}/{}/{}'.format(rec['repository'],rec['commit'],rec['repository_path'])
    try:
        with urllib.request.urlopen(url,timeout=30) as response:data=response.read()
    except (urllib.error.URLError,OSError) as exc:
        raise SystemExit('Pinned source retrieval failed: '+str(exc))
    sha=hashlib.sha256(data).hexdigest()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if sha!=rec['sha256'] or blob!=rec['git_blob_sha1']:
        raise SystemExit('Source hash mismatch; no output written.')
    if dst.exists() and dst.read_bytes()!=data:
        raise SystemExit('Destination exists with different bytes; no output overwritten.')
    dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
    print(json.dumps({'status':'PASS','path':str(dst),'bytes':len(data),'sha256':sha,'git_blob_sha1':blob},indent=2))
if __name__=='__main__':main()
