#!/usr/bin/env python3
"""Verify the exact historical-receipt exception cannot admit new private data."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    if not __debug__:
        raise RuntimeError("Use unoptimized Python")
    spec = importlib.util.spec_from_file_location("public_privacy", ROOT/"tools/verify_repository.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    receipt_name = "host-parameters/logs/execution_receipt.json"
    original = (ROOT/receipt_name).read_bytes()
    controls = []
    with tempfile.TemporaryDirectory(prefix="public-privacy-controls-") as td:
        root = Path(td)
        receipt = root/receipt_name
        receipt.parent.mkdir(parents=True)
        receipt.write_bytes(original)
        with contextlib.redirect_stdout(io.StringIO()):
            verifier.verify_public_privacy(root)
        private_path = str(Path("/").joinpath("home", "private-owner", "file"))
        cases = [
            ("changed historical receipt", receipt, original + private_path.encode(), "private filesystem path"),
            ("new private-path file", root/"private-path.txt", private_path.encode(), "private filesystem path"),
            ("credential with reviewed receipt present", receipt, original + ("gh" + "p_" + "x"*30).encode(), "credential marker"),
        ]
        for name, path, data, expected in cases:
            # Put the credential test outside the path-bearing receipt so the
            # unchanged path detector cannot preempt the credential detector.
            if expected == "credential marker":
                path = root/"credential.txt"
                data = ("gh" + "p_" + "x"*30).encode()
            path.write_bytes(data)
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    verifier.verify_public_privacy(root)
            except RuntimeError as err:
                if expected not in str(err):
                    raise RuntimeError("Unexpected rejection: " + str(err))
                controls.append({"name": name, "status": "REJECTED_AS_EXPECTED"})
            else:
                raise RuntimeError("Accepted invalid privacy control: " + name)
            finally:
                if path == receipt:
                    path.write_bytes(original)
                else:
                    path.unlink()
    print(json.dumps({"status": "PASS", "positive_controls": 1,
                      "rejection_controls": len(controls), "controls": controls}, indent=2))


if __name__ == "__main__":
    main()
