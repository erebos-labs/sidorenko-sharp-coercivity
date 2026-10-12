#!/usr/bin/env python3
"""Run bounded release omission/corruption controls on disposable copies."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def manifest(root):
    lines = [hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(root).as_posix()
             for p in sorted(root.rglob('*')) if p.is_file() and p.name != 'SHA256SUMS']
    (root / 'SHA256SUMS').write_text('\n'.join(lines) + '\n')

def edit_json(root, path, edit):
    data = json.loads((root / path).read_text())
    edit(data)
    (root / path).write_text(json.dumps(data, indent=2) + '\n')

def check(root, flags=()):
    return subprocess.run([sys.executable, '-I', '-B', *flags, str(root / 'validate_release.py')],
                          cwd=root, capture_output=True, text=True, timeout=30)

def main():
    require(sys.flags.optimize == 0, 'Use Python without -O/-OO')
    root = Path(__file__).resolve().parent
    baseline = check(root)
    require(baseline.returncode == 0, 'Baseline release failed: ' + baseline.stdout + baseline.stderr)
    require(baseline.stdout.index('PASS artifact integrity') < baseline.stdout.index('BEGIN mathematical checks'),
            'Artifact validation did not precede mathematical checking')
    print('PASS legitimate release; artifact validation precedes mathematical checks')
    cases = []
    for path in ('LICENSE', 'sources/openai/LICENSE', 'THIRD_PARTY_NOTICES.md', 'ATTRIBUTION.md',
                 'provenance.json', 'source-pins.json', 'related-references.json', 'SHA256SUMS'):
        cases.append(('omit_' + path.replace('/', '_'), lambda r, p=path: (r / p).unlink(),
                      'Required release file is missing' if path != 'SHA256SUMS' else 'Release file inventory differs', False))
    def omit_license_and_pin(r):
        (r / 'sources/openai/LICENSE').unlink()
        edit_json(r, 'source-pins.json', lambda j: j.update(files=[e for e in j['files'] if e['path'] != 'sources/openai/LICENSE']))
    cases.append(('omit_license_and_pin', omit_license_and_pin, 'Required release file is missing', False))
    def bad_digest(r):
        p = r / 'SHA256SUMS'; s = p.read_text(); p.write_text(('0' if s[0] != '0' else '1') + s[1:])
    cases.append(('manifest_digest', bad_digest, 'Manifest digest mismatch', False))
    def duplicate(r):
        p = r / 'SHA256SUMS'; s = p.read_text(); p.write_text(s + s.splitlines()[0] + '\n')
    cases.append(('manifest_duplicate', duplicate, 'Duplicate manifest path', False))
    def escape(r):
        (r / 'SHA256SUMS').write_text('0' * 64 + '  ../outside.txt\n')
    cases.append(('manifest_escape', escape, 'Unsafe manifest path', False))
    def drop_row(r):
        p = r / 'SHA256SUMS'; p.write_text('\n'.join(p.read_text().splitlines()[1:]) + '\n')
    cases.append(('manifest_omission', drop_row, 'Manifest coverage differs', False))
    def alter_license(r):
        p = r / 'LICENSE'; p.write_text(p.read_text() + '\nChanged terms.\n'); manifest(r)
    cases.append(('license_rehashed', alter_license, 'Original contribution LICENSE differs', False))
    def alter_upstream(r):
        p = r / 'sources/openai/LICENSE'; p.write_text(p.read_text() + '\nChanged terms.\n'); manifest(r)
    cases.append(('upstream_license_rehashed', alter_upstream, 'Frozen payload digest differs', False))
    def wrong_project(r):
        edit_json(r, 'provenance.json', lambda j: j.update(project='Wrong project')); manifest(r)
    cases.append(('project_rehashed', wrong_project, 'Project or contribution license differs', False))
    def wrong_third_party_license(r):
        edit_json(r, 'provenance.json', lambda j: j['third_party_files'][0].update(license='MIT')); manifest(r)
    cases.append(('third_party_license_rehashed', wrong_third_party_license, 'Third-party licensing provenance differs', False))
    def wrong_reference(r):
        edit_json(r, 'related-references.json', lambda j: j['related_document'].update(commit='0' * 40)); manifest(r)
    cases.append(('reference_rehashed', wrong_reference, 'Related citation or pin differs', False))
    def wrong_pin(r):
        edit_json(r, 'source-pins.json', lambda j: j['files'][-1].update(commit='0' * 40)); manifest(r)
    cases.append(('license_pin_rehashed', wrong_pin, 'Required source pins differ', False))
    def change_theorem(r):
        p = r / 'THEOREM.md'; p.write_text(p.read_text() + '\nChanged proof.\n'); manifest(r)
    cases.append(('theorem_rehashed', change_theorem, 'Frozen payload digest differs', False))
    def change_math_code(r):
        p = r / 'checker.py'; s = p.read_text(); s = s.replace('    return Fraction(value)', '    return Fraction(value) + 1'); p.write_text(s); manifest(r)
    cases.append(('math_code_rehashed', change_math_code, 'Mathematical checker code differs', False))
    def add_unexpected(r):
        (r / 'unlicensed-third-party.txt').write_text('Unexpected document.\n'); manifest(r)
    cases.append(('unexpected_file', add_unexpected, 'Release file inventory differs', False))
    def symlink(r):
        p = r / 'LICENSE'; p.unlink(); p.symlink_to(root / 'LICENSE')
    cases.append(('symlink', symlink, 'Symlink entry is not permitted', False))
    def failed_checker(r):
        p = r / 'checker.py'; s = p.read_text(); old = '        main()\n    except'; require(old in s, 'Unexpected checker wrapper'); p.write_text(s.replace(old, '        sys.exit(7)\n    except')); manifest(r)
    cases.append(('checker_failure_propagated', failed_checker, 'Mathematical checker failed', True))
    count = 0
    with tempfile.TemporaryDirectory(prefix='sidorenko-release-controls-') as temporary:
        for name, mutate, reason, entered_math in cases:
            cloned = Path(temporary) / name
            shutil.copytree(root, cloned)
            mutate(cloned)
            result = check(cloned)
            require(result.returncode != 0 and reason in result.stderr,
                    name + ' did not fail as expected: ' + result.stdout + result.stderr)
            require(('BEGIN mathematical checks' in result.stdout) == entered_math,
                    name + ' mathematical-phase boundary differs')
            print('PASS control rejected: ' + name)
            count += 1
    for flag in ('-O', '-OO'):
        result = check(root, flags=(flag,))
        require(result.returncode != 0 and 'Optimized execution is not permitted' in result.stderr
                and 'BEGIN mathematical checks' not in result.stdout, 'Optimization control failed')
        print('PASS control rejected: optimized_' + flag.lstrip('-'))
        count += 1
    print('PASS ' + str(count) + ' release controls; omission/corruption is distinct from mathematical mutation')

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print('FAIL release controls: ' + str(exc), file=sys.stderr)
        sys.exit(1)
