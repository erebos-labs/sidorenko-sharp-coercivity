#!/usr/bin/env python3
"""Execute the real checker on two deliberately corrupted certificate files.

Run: python3 -I -B test_mutations.py
Standard library only; temporary corruptions do not modify the deliverable.
Each mutation must fail at its specified mathematical check, not merely exit.
"""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run_checker(root, certificate=None):
    command = [sys.executable, "-I", "-B", str(root / "checker.py")]
    if certificate is not None:
        command += ["--certificate", str(certificate)]
    return subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=30)


def main():
    require(sys.flags.optimize == 0, "Use Python without -O/-OO")
    root = Path(__file__).resolve().parent
    baseline = run_checker(root)
    require(baseline.returncode == 0,
            "Legitimate certificate failed:\n" + baseline.stdout + baseline.stderr)
    print("PASS legitimate certificate accepted by the actual checker")
    cert = json.loads((root / "certificate.json").read_text(encoding="utf-8"))
    endpoint = copy.deepcopy(cert)
    require(endpoint["polynomials"]["E_plus_B"]["terms"][0][0] == "115/1620",
            "Unexpected mutation starting value")
    endpoint["polynomials"]["E_plus_B"]["terms"][0][0] = "116/1620"
    kappa = copy.deepcopy(cert)
    require(kappa["kappa"] == "1/40", "Unexpected kappa starting value")
    kappa["kappa"] = "1/39"
    mutations = [
        ("endpoint_115_to_116", endpoint, "IDENTITY FAILED: plus breakpoint from first interval"),
        ("kappa_1_over_40_to_1_over_39", kappa, "IDENTITY FAILED: sharpness: Q = kappa N")
    ]
    with tempfile.TemporaryDirectory(prefix="sidorenko-certificate-mutations-") as temporary:
        for name, corrupted, expected in mutations:
            path = Path(temporary) / (name + ".json")
            path.write_text(json.dumps(corrupted, indent=2) + "\n", encoding="utf-8")
            result = run_checker(root, path)
            require(result.returncode != 0, "CORRUPTION ACCEPTED: " + name)
            require(expected in result.stderr,
                    "Corruption failed for an unexpected reason: " + name + "\n" + result.stdout + result.stderr)
            print("PASS mutation rejected: " + name)
            print("  " + result.stderr.strip())
    print("PASS both mutation controls rejected their targeted corruptions")
    print("The controls establish detection of these corruptions, not completeness of the checker.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
