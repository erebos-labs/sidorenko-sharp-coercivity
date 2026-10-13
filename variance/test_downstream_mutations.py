#!/usr/bin/env python3
"""Run two deliberate downstream certificate corruptions in temporary files."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


def main():
    base = Path(__file__).resolve().parent
    checker = base / "check_downstream.py"
    original = json.loads((base / "original_certificate.json").read_text())
    cases = []
    inverse = deepcopy(original)
    inverse["inverse_numerator"][0][0] += 1
    cases.append(("one_inverse_diagonal_plus_one", inverse, "inverse matrix product"))
    bound = deepcopy(original)
    bound["strict_bound_B"] = 1
    cases.append(("strict_bound_replaced_by_one", bound, "strict coordinate inequalities"))
    results = []
    with TemporaryDirectory(prefix="sidorenko-downstream-mutations-") as tmp:
        work = Path(tmp)
        for name, corrupted, expected in cases:
            payload = (json.dumps(corrupted, indent=2, sort_keys=True) + "\n").encode()
            path = work / (name + ".json")
            path.write_bytes(payload)
            command = [sys.executable, "-I", "-B", str(checker), "--certificate", str(path)]
            replay = subprocess.run(command, cwd=work, capture_output=True, text=True,
                                    timeout=60, check=False)
            if replay.returncode == 0 or expected not in replay.stderr:
                raise RuntimeError("Mutation was not rejected as expected: " + name
                                   + "\n" + replay.stdout + replay.stderr)
            results.append({
                "mutation": name,
                "mutated_certificate_sha256": sha256(payload).hexdigest(),
                "returncode": replay.returncode,
                "stderr": replay.stderr.strip(),
                "expected_failure": expected,
                "rejected_at_expected_check": True,
            })
    print(json.dumps({"status": "PASS", "mutation_tests": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
