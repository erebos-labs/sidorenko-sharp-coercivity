#!/usr/bin/env python3
"""Reject corrupt host release assets and mismatched tracked trees."""
import argparse
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    if not __debug__:
        raise RuntimeError("Use unoptimized Python")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-dir", type=Path, required=True)
    folder = parser.parse_args().release_dir.resolve()
    spec = importlib.util.spec_from_file_location("host_release_validation", ROOT/"tools/verify_repository.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    with contextlib.redirect_stdout(io.StringIO()):
        verifier.verify_host_assets(folder)
    controls = []
    for name in ("corrupt ZIP", "wrong checksum", "wrong receipt", "missing receipt",
                 "changed tracked proof", "extra tracked file"):
        with tempfile.TemporaryDirectory(prefix="host-release-rejection-") as td:
            temp = Path(td)
            assets = temp/"assets"
            assets.mkdir()
            for suffix in (".zip", ".sha256", ".release.json"):
                filename = verifier.HOST_ARCHIVE.replace(".zip", suffix)
                shutil.copy2(folder/filename, assets/filename)
            expected = ""
            if name == "corrupt ZIP":
                archive = assets/verifier.HOST_ARCHIVE
                archive.write_bytes(archive.read_bytes() + b"corrupt")
                expected = "Host ZIP hash differs"
            elif name == "wrong checksum":
                (assets/verifier.HOST_ARCHIVE.replace(".zip", ".sha256")).write_text("0"*64 + "\n")
                expected = "Host asset metadata differs"
            elif name == "wrong receipt":
                (assets/verifier.HOST_ARCHIVE.replace(".zip", ".release.json")).write_text("{}\n")
                expected = "Host asset metadata differs"
            elif name == "missing receipt":
                (assets/verifier.HOST_ARCHIVE.replace(".zip", ".release.json")).unlink()
            else:
                replica = temp/"repository"
                shutil.copytree(ROOT/"host-parameters", replica/"host-parameters")
                shutil.copytree(ROOT/"artifacts", replica/"artifacts")
                verifier.ROOT = replica
                if name == "changed tracked proof":
                    proof = replica/"host-parameters/PROOF.md"
                    proof.write_bytes(proof.read_bytes() + b"\nchanged\n")
                    expected = "Host ZIP/repository bytes differ"
                else:
                    (replica/"host-parameters/unexpected.txt").write_text("extra\n")
                    expected = "Host ZIP/repository coverage differs"
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    verifier.verify_host_assets(assets)
            except (RuntimeError, FileNotFoundError) as err:
                if expected and expected not in str(err):
                    raise RuntimeError("Wrong rejection for " + name + ": " + str(err))
                if not expected and not isinstance(err, FileNotFoundError):
                    raise RuntimeError("Wrong missing-receipt rejection")
                controls.append({"name": name, "status": "REJECTED_AS_EXPECTED"})
            else:
                raise RuntimeError("Accepted invalid control: " + name)
            finally:
                verifier.ROOT = ROOT
    print(json.dumps({"status": "PASS", "positive_controls": 1,
                      "rejection_controls": len(controls), "controls": controls}, indent=2))


if __name__ == "__main__":
    main()
