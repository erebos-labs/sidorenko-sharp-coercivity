#!/usr/bin/env python3
"""Packaging/retrieval regression controls. Mutations are confined to temp dirs."""
import argparse
from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location("test_" + name, ROOT / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def manifest(root):
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.name != "SHA256SUMS")
    (root / "SHA256SUMS").write_text("".join(
        hashlib.sha256(p.read_bytes()).hexdigest() + "  " + str(p.relative_to(root)) + "\n"
        for p in files))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-cache", type=Path, required=True)
    args = parser.parse_args()
    verifier, fetcher = load("verify_package"), load("fetch_sources")
    cache = verifier.validate_cache_location(args.source_cache)
    _, retained, external = verifier.verify_inventory()
    for e in external:
        verifier.verify_source(verifier.regular_file(cache, e["path"]).read_bytes(), e)
    results = []

    def reject(name, action, expected):
        try:
            action()
        except (ValueError, OSError) as err:
            if expected not in str(err):
                raise AssertionError(name + ": wrong failure: " + str(err))
            results.append({"control": name, "outcome": "REJECTED", "expected": expected})
        else:
            raise AssertionError(name + ": corrupt input was accepted")

    baseline = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "verify_package.py"),
                               "--inventory-only"], text=True, capture_output=True)
    assert baseline.returncode == 0
    parsed = json.loads(baseline.stdout)
    assert parsed["status"] == "INVENTORY_ONLY_PASS" and parsed["full_replay"] == "NOT_RUN"
    results.append({"control": "inventory_does_not_claim_full_replay", "outcome": "PASS"})
    absent = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "verify_package.py")],
                            text=True, capture_output=True)
    assert absent.returncode == 1 and "Full replay requires 18 external source files" in absent.stderr
    results.append({"control": "cache_required_no_false_full_pass", "outcome": "REJECTED"})

    with TemporaryDirectory(prefix="variance-release-controls-") as tmp:
        tmp = Path(tmp)
        copied = tmp / "public"
        shutil.copytree(ROOT, copied)
        (copied / "THEOREM.md").write_bytes((copied / "THEOREM.md").read_bytes() + b"\n")
        reject("changed_public_proof_bytes", lambda: verifier.verify_inventory(copied), "Checksum mismatch")
        shutil.rmtree(copied); shutil.copytree(ROOT, copied)
        (copied / "extra.txt").write_text("not part of the release")
        reject("unexpected_public_file", lambda: verifier.verify_inventory(copied), "exact package")
        shutil.rmtree(copied); shutil.copytree(ROOT, copied)
        e = external[0]
        target = copied / e["path"]; target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((cache / e["path"]).read_bytes())
        manifest(copied)
        reject("excluded_snapshot_even_with_rebuilt_manifest", lambda: verifier.verify_inventory(copied),
               "Excluded source redistributed")
        shutil.rmtree(copied); shutil.copytree(ROOT, copied)
        (copied / "LICENSE").write_text("replacement license\n")
        (copied / "sources/prior/LICENSE").write_text("replacement license\n")
        manifest(copied)
        reject("changed_MIT_notices_even_with_rebuilt_manifest", lambda: verifier.verify_inventory(copied),
               "Prior MIT notice")
        shutil.rmtree(copied); shutil.copytree(ROOT, copied)
        (copied / "source-pins.json").write_bytes((copied / "source-pins.json").read_bytes() + b"\n")
        manifest(copied)
        reject("changed_original_source_bindings", lambda: verifier.verify_inventory(copied),
               "Original source bindings changed")
        reject("cache_inside_package", lambda: verifier.validate_cache_location(ROOT / "cache"), "separate cache")
        reject("cache_is_package_ancestor", lambda: verifier.validate_cache_location(ROOT.parent), "separate cache")
        empty = tmp / "empty"; empty.mkdir()
        reject("missing_external_source", lambda: verifier.stage_overlay(ROOT, empty, external, tmp / "overlay"),
               "Missing or unsafe source")
        corrupt = tmp / "corrupt"; shutil.copytree(cache, corrupt)
        file = corrupt / external[0]["path"]; raw = file.read_bytes()
        file.write_bytes(bytes([raw[0] ^ 1]) + raw[1:])
        reject("same_length_cache_corruption", lambda: verifier.stage_overlay(ROOT, corrupt, external, tmp / "overlay"),
               "Source SHA-256")
        file.unlink(); file.symlink_to(cache / external[0]["path"])
        reject("symlink_cache_source", lambda: verifier.stage_overlay(ROOT, corrupt, external, tmp / "overlay"),
               "Symlink source path")
        bad = deepcopy(external[0]); bad["commit"] = "main"
        reject("floating_download_ref", lambda: fetcher.raw_url(bad), "Immutable commit")
        bad = deepcopy(external[0]); bad["upstream_path"] = "../escape"
        reject("download_path_traversal", lambda: fetcher.raw_url(bad), "Unsafe relative path")
        bad = deepcopy(external[0]); bad["repository"] = "unexpected/repository"
        reject("unapproved_download_repository", lambda: fetcher.raw_url(bad), "Unapproved external repository")
        reject("download_redirect", lambda: fetcher.NoRedirect().redirect_request(
            None, None, 302, "", {}, "https://unexpected.example/file"), "Unexpected source redirect")

        # Exercise the downloader's real response-validation and write path with
        # a deterministic transport. Actual public retrieval is audited separately.
        by_url = {fetcher.raw_url(e): e for e in external}
        requested = []

        class Response:
            def __init__(self, data):
                self.data = data
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self, limit):
                return self.data[:limit]

        class Transport:
            def __init__(self, corrupt=False):
                self.corrupt = corrupt
            def open(self, request, timeout):
                entry = by_url[request.full_url]
                assert request.get_method() == "GET" and timeout == 30
                assert request.get_header("Authorization") is None
                requested.append(entry["path"])
                data = (cache / entry["path"]).read_bytes()
                if self.corrupt:
                    data = bytes([data[0] ^ 1]) + data[1:]
                return Response(data)

        old_argv = sys.argv
        try:
            fetcher.build_opener = lambda *handlers: Transport()
            sys.argv = ["fetch_sources.py", "--cache", str(tmp / "downloaded")]
            buf = io.StringIO()
            with redirect_stdout(buf):
                assert fetcher.main() == 0
            output = json.loads(buf.getvalue())
            assert output["files"] == len(external) == len(requested) == 18
            assert all(x["status"] == "RETRIEVED_AND_VERIFIED" for x in output["results"])
            results.append({"control": "download_response_checks_and_writes", "outcome": "PASS", "files": 18})
            fetcher.build_opener = lambda *handlers: Transport(corrupt=True)
            sys.argv = ["fetch_sources.py", "--cache", str(tmp / "bad-download")]
            reject("corrupt_download_rejected_before_write", fetcher.main, "Source SHA-256")
            assert not (tmp / "bad-download" / external[0]["path"]).exists()
        finally:
            sys.argv = old_argv
    print(json.dumps({"status": "PASS", "controls": results,
                      "live_HTTPS_transport": "Separate public retrieval record; this transport test is simulated"},
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
