#!/usr/bin/env python3
"""Check release artifact integrity before running the separate math checker."""
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

VERSION = '1.1.0'
ORIGINAL_SHA256 = 'b87956508f475622aff4e524c20b0119d37c35eed892b44b366e11e4c5c3429c'
RELATED = {
    'repository': 'artuskg/sidorenko-template-refinements',
    'commit': '9922b05bf2c3418e1a46378d4ebac60e8a34ce51',
    'repository_path': 'global-residual-dimension.md',
    'git_blob_sha1': 'dcc39f4f593460cbad663ab168e1e68bf9c0146d',
    'sha256': '4dab94055d9ede6751dd53728e17ecef27f4d461360fefcd30565e24310c4172',
    'url': 'https://github.com/artuskg/sidorenko-template-refinements/blob/9922b05bf2c3418e1a46378d4ebac60e8a34ce51/global-residual-dimension.md',
    'bundled': False,
}
REQUIRED = {
    'AUDIT.md', 'ATTRIBUTION.md', 'LICENSE', 'README.md', 'RELATED_WORK_REVIEW.md',
    'RELEASE_NOTES.md', 'STATUS.md', 'THEOREM.md', 'THIRD_PARTY_NOTICES.md',
    'VERIFICATION.md', 'certificate.json', 'checker.py', 'examples.json',
    'provenance.json', 'related-references.json', 'source-pins.json',
    'test_mutations.py', 'test_release_controls.py', 'validate_release.py',
    'sources/openai/LICENSE', 'sources/openai/planted.tex', 'sources/openai/tail.tex',
}
# Frozen v1 payload/source constants are inserted here during preparation.
PAYLOAD = {'THEOREM.md': '0123138eb178b42f26bf0884b03e6337edada97b2f5534fcdcc54ef9e588ae0a', 'AUDIT.md': '172b43fb68e2f54e95638519a8eea5112408342ccff17ed56a38801cf287bf65', 'certificate.json': '830862d68139584b24517ef9a03c9fb9c77d495bed5f94eff762d59df55ef276', 'examples.json': '98110ea16726863f63ebafedc0fa37bf96ce7497b5d783493c3133472a40ec33', 'test_mutations.py': '71fb1be986feb7ba5c4aac5b13b78fded5ac8357a8222abe6996135871fbf3fb', 'sources/openai/tail.tex': 'fd2417f6efa4394fc8ba410f0ecb79f260a204c911957c9789a7d9d1ae0e6150', 'sources/openai/planted.tex': '2336147f1d032c3d8b114883c593a2d98d03598d190256667ded2a4aee0c6c46', 'sources/openai/LICENSE': 'c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4'}
MATHEMATICAL_CODE = {'rational': 'ebaac4a01b98a4f85057adc6df97807a937f11b90e3de9e831fa4253130da6c4', 'Poly': 'f3bfcd70e97a7893acee9e942388fa5093a8e86720f5a69820e18bebf8321564', 'V': 'ca28c408fbec84878a22fcc72e3e10295bf0adc28f5847875e6d1f125a1a33bd', 'load_polynomial': '6a114a1918bedf055f70bc23922ec5bf0cdf1b8a14eeef3accecdc63ec03a4d7', 'Checks': 'a557fa46a7c24226da1f0aa7439736a514c2721d0601df620c1d65bc774674b2', 'bfun': '2f34161d390ee223e27b8bae7871e4190bb54f2ca739163cd9657f8bc9ebaa19', 'source_expressions': '1e6867f6612ad8be873cfa7a17e4001a6704bf7e33c037d60ca6f5fd238eaaa6', 'check_symbolic': '8b7313c0ec2734b841bc6a7a63ff9f7e237e38075b8da6e7bd65f8ff0282d7fb', 'check_examples': '0dad2b8f96d86539e21ffe70ab06a4900be3d01263f68f8ce0e61c3962189209'}
SOURCES = [{'path': 'sources/openai/tail.tex', 'repository': 'openai/math', 'commit': 'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb', 'repository_path': 'preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/tail.tex', 'sha256': 'fd2417f6efa4394fc8ba410f0ecb79f260a204c911957c9789a7d9d1ae0e6150', 'git_blob_sha1': 'dc11e07a592e70d3a13e3a005c72378c88edc351', 'url': 'https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/tail.tex'}, {'path': 'sources/openai/planted.tex', 'repository': 'openai/math', 'commit': 'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb', 'repository_path': 'preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/planted.tex', 'sha256': '2336147f1d032c3d8b114883c593a2d98d03598d190256667ded2a4aee0c6c46', 'git_blob_sha1': 'e1a4636e66361dae0f5918e1245950060535a83c', 'url': 'https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/planted.tex'}, {'path': 'sources/openai/LICENSE', 'repository': 'openai/math', 'commit': 'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb', 'repository_path': 'LICENSE', 'sha256': 'c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4', 'git_blob_sha1': '261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64', 'url': 'https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/LICENSE'}]
MIT_SHA256 = '04690d463ba7d13b6b853229a5b1eefefd0b346e063a55967ba2f75f06038a6c'

class ReleaseFailure(Exception):
    pass

def require(condition, message):
    if not condition:
        raise ReleaseFailure(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def json_file(root, name):
    return json.loads((root / name).read_text(encoding='utf-8'))

def check_artifact(root):
    require(sys.flags.optimize == 0, 'Optimized execution is not permitted')
    files = set()
    for path in root.rglob('*'):
        mode = path.lstat().st_mode
        require(not stat.S_ISLNK(mode), 'Symlink entry is not permitted')
        require(stat.S_ISREG(mode) or stat.S_ISDIR(mode), 'Nonregular entry is not permitted')
        if stat.S_ISREG(mode):
            files.add(path.relative_to(root).as_posix())
    require(REQUIRED <= files, 'Required release file is missing: ' + ', '.join(sorted(REQUIRED - files)))
    require(files == REQUIRED | {'SHA256SUMS'}, 'Release file inventory differs')
    manifest = {}
    for line in (root / 'SHA256SUMS').read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, 'Malformed manifest line')
        checksum, name = match.groups()
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts and '\\' not in name
                and path.as_posix() == name, 'Unsafe manifest path')
        require(name not in manifest, 'Duplicate manifest path')
        manifest[name] = checksum
    require(set(manifest) == REQUIRED, 'Manifest coverage differs')
    for name, checksum in manifest.items():
        require(digest((root / name).read_bytes()) == checksum, 'Manifest digest mismatch: ' + name)
    require(digest((root / 'LICENSE').read_bytes()) == MIT_SHA256, 'Original contribution LICENSE differs')
    for name, checksum in PAYLOAD.items():
        require(digest((root / name).read_bytes()) == checksum, 'Frozen payload digest differs: ' + name)
    source = (root / 'checker.py').read_text(encoding='utf-8')
    nodes = [n for n in ast.parse(source).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    code_hashes = {n.name: digest(ast.get_source_segment(source, n).encode())
                   for n in nodes if n.name in MATHEMATICAL_CODE}
    require(code_hashes == MATHEMATICAL_CODE, 'Mathematical checker code differs')
    pins = json_file(root, 'source-pins.json')
    require(pins['schema_version'] == 1 and pins['files'] == SOURCES, 'Required source pins differ')
    for entry in SOURCES:
        data = (root / entry['path']).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
        require(digest(data) == entry['sha256'] and blob == entry['git_blob_sha1'], 'Source binding differs')
    provenance = json_file(root, 'provenance.json')
    require(provenance['schema_version'] == 1 and provenance['version'] == VERSION,
            'Release provenance version differs')
    require(provenance['project'] == 'Erebos Labs' and provenance['original_contribution_license'] == 'MIT',
            'Project or contribution license differs')
    require(provenance['original_archive'] == {'filename': 'sidorenko_sharp_constant_v1.zip',
                                               'sha256': ORIGINAL_SHA256}, 'Original archive provenance differs')
    require(provenance['unchanged_original_payload'] == PAYLOAD, 'Payload provenance differs')
    require(provenance['third_party_files'] == [{**e, 'license': 'Apache-2.0', 'modified': False} for e in SOURCES],
            'Third-party licensing provenance differs')
    dev = provenance['development']
    require('GPT-6 Pro' in dev['original_package'] and 'Codex' in dev['local_review_and_release_preparation']
            and dev['human_mathematician_authorship_claimed'] is False
            and dev['proof_assistant_verification_claimed'] is False, 'AI attribution provenance differs')
    excluded = provenance['excluded_related_document']
    require(excluded == {'path': RELATED['repository_path'], **{k: RELATED[k] for k in
            ('repository', 'commit', 'git_blob_sha1', 'sha256', 'bundled')}}, 'Excluded-source provenance differs')
    refs = json_file(root, 'related-references.json')
    require(refs['schema_version'] == 1 and all(refs['related_document'][k] == v for k, v in RELATED.items()),
            'Related citation or pin differs')
    require(refs['related_pull_request'] == 'https://github.com/rohanarun/sidorenko-template-refinements/pull/4',
            'Related PR citation differs')
    notices = (root / 'THIRD_PARTY_NOTICES.md').read_text()
    attribution = (root / 'ATTRIBUTION.md').read_text()
    require(all(token in notices for token in ('MIT', 'Apache-2.0', 'sources/openai/LICENSE', 'OpenAI',
            'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb')), 'Required third-party notices differ')
    require(all(token in attribution for token in ('Erebos Labs', 'GPT-6 Pro', 'Codex', 'AI-assisted')),
            'Required attribution statement differs')
    print('PASS artifact integrity: manifest, licensing, attribution and provenance; '
          + str(len(manifest)) + ' files', flush=True)

def main():
    require(sys.version_info >= (3, 9), 'Python 3.9 or newer required')
    root = Path(__file__).resolve().parent
    check_artifact(root)
    print('BEGIN mathematical checks: exact arithmetic supports the conventional proof', flush=True)
    result = subprocess.run([sys.executable, '-I', '-B', str(root / 'checker.py')], cwd=root, timeout=30)
    require(result.returncode == 0, 'Mathematical checker failed')
    print('PASS release validation; artifact integrity is distinct from proof support')

if __name__ == '__main__':
    try:
        main()
    except (ReleaseFailure, ValueError, KeyError, TypeError, OSError, SyntaxError, subprocess.TimeoutExpired) as exc:
        print('FAIL artifact/release validation: ' + str(exc), file=sys.stderr)
        sys.exit(1)
