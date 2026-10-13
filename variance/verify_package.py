#!/usr/bin/env python3
"""Verify inventory, or replay unchanged mathematics with 18 external data files."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent
SOURCE_PINS_SHA256 = "47b9ced9b41e96c302446f8e8cb0377993b4bc81eb4607458e13d2fe7352f0f1"
MIT_LICENSE_SHA256 = "04690d463ba7d13b6b853229a5b1eefefd0b346e063a55967ba2f75f06038a6c"
RETAINED_REPOSITORIES = {"openai/math", "erebos-labs/sidorenko-sharp-coercivity"}
COMMANDS = [["check_variance.py", "--json"], ["test_local_mutations.py"],
            ["check_downstream.py"], ["test_downstream_mutations.py"],
            ["independent/check_local_grid.py"], ["independent/check_downstream.py"]]


def safe_relative(name):
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or ".." in path.parts
            or "\\" in name or ":" in name or str(path) != name):
        raise ValueError("Unsafe relative path: " + name)
    return path


def regular_file(base, name):
    base = Path(base).resolve()
    rel = safe_relative(name)
    path = base.joinpath(*rel.parts)
    if any(base.joinpath(*rel.parts[:n]).is_symlink()
           for n in range(1, len(rel.parts) + 1)):
        raise ValueError("Symlink source path: " + name)
    if not path.is_file() or base not in path.resolve().parents:
        raise ValueError("Missing or unsafe source: " + name)
    return path


def verify_source(data, entry):
    name = entry["path"]
    if len(data) != entry["bytes"]:
        raise ValueError("Source byte length: " + name)
    if hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise ValueError("Source SHA-256: " + name)
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != entry["git_blob"]:
        raise ValueError("Source Git blob: " + name)


def verify_inventory(root=ROOT):
    root = root.resolve()
    listed = set()
    for line in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        if name in listed:
            raise ValueError("Repeated checksum path: " + name)
        path = regular_file(root, name)
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError("Checksum mismatch: " + name)
        listed.add(name)
    paths = list(root.rglob("*"))
    if any(p.is_symlink() for p in paths):
        raise ValueError("Release contains a symlink")
    actual = {str(p.relative_to(root)) for p in paths if p.is_file()}
    if actual != listed | {"SHA256SUMS"}:
        raise ValueError("Checksum manifest does not cover the exact package")
    raw = (root / "source-pins.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_PINS_SHA256:
        raise ValueError("Original source bindings changed")
    pins = json.loads(raw)
    distribution = json.loads((root / "distribution.json").read_text())
    if pins["schema_version"] != 1 or distribution["schema_version"] != 1:
        raise ValueError("Unsupported source/distribution schema")
    entries = pins["files"]
    retained = [e for e in entries if e["repository"] in RETAINED_REPOSITORIES]
    external = [e for e in entries if e["repository"] not in RETAINED_REPOSITORIES]
    if len({e["path"] for e in entries}) != len(entries):
        raise ValueError("Duplicate source binding")
    if (distribution["retained_source_paths"] != [e["path"] for e in retained]
            or distribution["external_sources"] != external):
        raise ValueError("Distribution does not preserve the exact source partition")
    for entry in retained:
        verify_source(regular_file(root, entry["path"]).read_bytes(), entry)
    for entry in external:
        safe_relative(entry["path"])
        if (root / entry["path"]).exists():
            raise ValueError("Excluded source redistributed: " + entry["path"])
    if (root / "sources/review/current-review.json").exists():
        raise ValueError("Excluded API snapshots redistributed")
    license_bytes = regular_file(root, "sources/prior/LICENSE").read_bytes()
    if (hashlib.sha256(license_bytes).hexdigest() != MIT_LICENSE_SHA256
            or regular_file(root, "LICENSE").read_bytes() != license_bytes):
        raise ValueError("Prior MIT notice is not preserved")
    return len(listed), retained, external


def validate_cache_location(cache, root=ROOT):
    cache = Path(cache).resolve()
    root = root.resolve()
    if cache == root or root in cache.parents or cache in root.parents:
        raise ValueError("Use a separate cache outside the release, not its ancestor")
    return cache


def stage_overlay(root, cache, external, destination):
    """Copy only hash-verified data into a disposable replay workspace."""
    payloads = []
    for entry in external:
        data = regular_file(cache, entry["path"]).read_bytes()
        verify_source(data, entry)
        payloads.append((entry["path"], data))
    shutil.copytree(root, destination)
    for name, data in payloads:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory-only", action="store_true",
                        help="Check packaging only; arithmetic replay is NOT RUN")
    parser.add_argument("--source-cache", type=Path)
    parser.add_argument("--regenerate", action="store_true",
                        help="Also regenerate the certificate in the temporary overlay")
    args = parser.parse_args()
    if args.inventory_only and (args.source_cache or args.regenerate):
        parser.error("--inventory-only cannot be combined with full replay options")
    count, retained, external = verify_inventory()
    if args.inventory_only:
        print(json.dumps({"status": "INVENTORY_ONLY_PASS", "full_replay": "NOT_RUN",
                          "sha256_files": count, "retained_source_checks": len(retained),
                          "external_sources_required": len(external)}, indent=2))
        return 0
    if args.source_cache is None:
        raise ValueError("Full replay requires 18 external source files. Use "
                         "fetch_sources.py --cache DIR, then verify_package.py "
                         "--source-cache DIR. Inventory-only is not a mathematical replay.")
    cache = validate_cache_location(args.source_cache)
    checks = []
    with TemporaryDirectory(prefix="sidorenko-variance-replay-") as tmp:
        overlay = Path(tmp) / "package"
        stage_overlay(ROOT, cache, external, overlay)
        commands = COMMANDS + ([["generate_original_certificate.py"]] if args.regenerate else [])
        original_hash = hashlib.sha256((overlay / "original_certificate.json").read_bytes()).hexdigest()
        for arguments in commands:
            result = subprocess.run([sys.executable, "-I", "-B", str(overlay / arguments[0]),
                                     *arguments[1:]], cwd=overlay.parent, text=True,
                                    capture_output=True, timeout=120)
            if result.returncode:
                raise ValueError("Replay failed: " + arguments[0] + "\n" + result.stdout + result.stderr)
            if arguments[0] == "independent/check_local_grid.py":
                # The unchanged independent grid prints its exact counts as text.
                payload = {"status": "PASS", "stdout": result.stdout}
            else:
                payload = json.loads(result.stdout)
            checks.append({"program": arguments[0], "exit_code": result.returncode,
                           "result": payload})
        if hashlib.sha256((overlay / "original_certificate.json").read_bytes()).hexdigest() != original_hash:
            raise ValueError("Regenerated certificate bytes changed")
    print(json.dumps({"status": "FULL_REPLAY_PASS", "sha256_files": count,
                      "retained_source_checks": len(retained),
                      "external_source_checks": len(external),
                      "retrieved_programs_executed": False, "checks": checks}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError, subprocess.TimeoutExpired) as err:
        print("FAIL: " + str(err), file=sys.stderr)
        raise SystemExit(1)

