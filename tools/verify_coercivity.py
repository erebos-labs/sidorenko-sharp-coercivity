#!/usr/bin/env python3
"""Verify the frozen reviewed package, proof support, and optional release assets."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import zipfile

ARCHIVE = 'sidorenko_sharp_constant_v1.1.0.zip'
ARCHIVE_SHA256 = '058997f1e17a6c4298c9b62fd6b3a775f06769497c52f8e47e63288baf01fb60'
FIXED_DIGESTS = {
    'package/SHA256SUMS': '460ca12c2c8be1cf91e9633ba97e5b548e90c1e1c5a8fb3127c4e6eeed573c1a',
    'artifacts/sidorenko_sharp_constant_v1.1.0.sha256': '20724a962130191fe94c7d344918115a8e969f833bd76d77e3441ef8c835b1aa',
    'artifacts/sidorenko_sharp_constant_v1.1.0.release.json': 'fe5d8a42194ee8293a1c36a857ba8fcc7590e5036884304c7b7d2f026cc355ac',
}

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def verify_assets(root, folder):
    archive = folder / ARCHIVE
    require(digest(archive.read_bytes()) == ARCHIVE_SHA256, 'Downloaded ZIP hash differs')
    for name in (ARCHIVE.replace('.zip', '.sha256'), ARCHIVE.replace('.zip', '.release.json')):
        require((folder / name).read_bytes() == (root / 'artifacts' / name).read_bytes(),
                'Downloaded metadata differs: ' + name)
    seen = set()
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, 'ZIP CRC failed')
        for entry in z.infolist():
            path = PurePosixPath(entry.filename)
            require(not path.is_absolute() and '..' not in path.parts and '\\' not in entry.filename
                    and path.parts[0] == 'sidorenko_sharp_constant_v1.1.0'
                    and stat.S_ISREG(entry.external_attr >> 16) and not entry.flag_bits & 1,
                    'Unsafe ZIP member')
            name = PurePosixPath(*path.parts[1:]).as_posix()
            require(name not in seen, 'Duplicate ZIP member')
            seen.add(name)
            require(z.read(entry) == (root / 'package' / name).read_bytes(),
                    'ZIP member differs from repository package: ' + name)
    files = {p.relative_to(root / 'package').as_posix() for p in (root / 'package').rglob('*') if p.is_file()}
    require(files == seen, 'ZIP/repository file coverage differs')
    print('PASS fresh release assets: ZIP, checksum, receipt and all 23 package files', flush=True)

def main():
    require(sys.flags.optimize == 0, 'Use Python without -O/-OO')
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-dir', type=Path)
    args = parser.parse_args()
    for name, expected in FIXED_DIGESTS.items():
        require(digest((root / name).read_bytes()) == expected, 'Frozen metadata differs: ' + name)
    require((root / 'LICENSE').read_bytes() == (root / 'package/LICENSE').read_bytes(),
            'Repository original-contribution license differs')
    receipt = json.loads((root / 'artifacts' / ARCHIVE.replace('.zip', '.release.json')).read_text())
    require(receipt['archive']['sha256'] == ARCHIVE_SHA256 and receipt['remaining_decisions'] == [],
            'Release receipt differs')
    print('PASS repository bindings: reviewed manifest and release metadata', flush=True)
    for script in ('validate_release.py', 'test_release_controls.py', 'test_mutations.py'):
        result = subprocess.run([sys.executable, '-I', '-B', str(root / 'package' / script)], timeout=60)
        require(result.returncode == 0, 'Package check failed: ' + script)
    patterns = {
        'private filesystem path': r'/(?:Users|home|mnt|private|var)/',
        'credential marker': r'(?:BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY|sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|Bearer [A-Za-z0-9_.-]{20,})',
    }
    # Local coordination and Git internals are excluded from the published file set.
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if rel.parts[0] in {'.git', 'release-assets', '.agent-harness', 'thoughts'} or path.name in {'hey.md', 'publish.toml'}:
            continue
        require(not path.is_symlink(), 'Repository symlink entry')
        if path.is_file():
            text = path.read_text(encoding='utf-8')
            for label, pattern in patterns.items():
                require(not re.search(pattern, text), 'Privacy scan found ' + label + ': ' + rel.as_posix())
    print('PASS bounded public-file privacy scan', flush=True)
    if args.release_dir:
        verify_assets(root, args.release_dir.resolve())
    print('PASS repository verification; universal theorem remains a conventional real-domain proof')

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.TimeoutExpired, zipfile.BadZipFile) as exc:
        print('FAIL repository verification: ' + str(exc), file=sys.stderr)
        sys.exit(1)
