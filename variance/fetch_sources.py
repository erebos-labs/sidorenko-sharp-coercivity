#!/usr/bin/env python3
"""Retrieve 18 public immutable files as data into a separate, non-release cache."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote
from urllib.request import HTTPSHandler, build_opener, HTTPRedirectHandler, Request

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("release_verifier", ROOT / "verify_package.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Unexpected source redirect")


def raw_url(entry):
    if entry["repository"] not in {"artuskg/sidorenko-template-refinements",
                                    "rohanarun/sidorenko-template-refinements"}:
        raise ValueError("Unapproved external repository")
    if not re.fullmatch(r"[0-9a-f]{40}", entry["commit"]):
        raise ValueError("Immutable commit required")
    path = str(verifier.safe_relative(entry["upstream_path"]))
    return "https://raw.githubusercontent.com/" + entry["repository"] + "/" + entry["commit"] + "/" + quote(path, safe="/")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    args = parser.parse_args()
    _, _, external = verifier.verify_inventory()
    cache = verifier.validate_cache_location(args.cache)
    cache.mkdir(parents=True, exist_ok=True, mode=0o700)
    opener = build_opener(NoRedirect(), HTTPSHandler())
    results = []
    for entry in external:
        destination = cache / entry["path"]
        if destination.exists() or destination.is_symlink():
            data = verifier.regular_file(cache, entry["path"]).read_bytes()
            verifier.verify_source(data, entry)
            results.append({"path": entry["path"], "status": "VERIFIED_EXISTING"})
            continue
        rel = verifier.safe_relative(entry["path"])
        if any(cache.joinpath(*rel.parts[:n]).is_symlink()
               for n in range(1, len(rel.parts))):
            raise ValueError("Symlink cache directory: " + entry["path"])
        request = Request(raw_url(entry), headers={"User-Agent": "sidorenko-variance-source-replay/1.0.1"})
        with opener.open(request, timeout=30) as response:
            data = response.read(entry["bytes"] + 1)
        verifier.verify_source(data, entry)
        destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        destination.write_bytes(data)
        results.append({"path": entry["path"], "status": "RETRIEVED_AND_VERIFIED"})
    print(json.dumps({"status": "SOURCE_CACHE_VERIFIED", "files": len(results),
                      "programs_executed": False, "redistribution_permission": "NOT_GRANTED",
                      "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError) as err:
        print("FAIL: " + str(err), file=sys.stderr)
        raise SystemExit(1)
