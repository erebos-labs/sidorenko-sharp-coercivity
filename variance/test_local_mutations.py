#!/usr/bin/env python3
"""Require the exact local checker to reject targeted mutations.

No source code from the pinned repositories is executed. Each mutation runs
in an isolated temporary directory or certificate; the delivered package
is unchanged. Standard library only.
"""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def run(root, certificate=None):
    command = [sys.executable, "-I", "-B", str(ROOT / "check_variance.py"),
               "--root", str(root), "--json"]
    if certificate:
        command += ["--certificate", str(certificate)]
    return subprocess.run(command, cwd=root, text=True, capture_output=True)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    baseline = run(ROOT)
    require(baseline.returncode == 0, "Unmutated checker failed: " + baseline.stderr)
    data = json.loads((ROOT / "local_certificate.json").read_text(encoding="utf-8"))
    mutations = [
        ("claim_1_over_47", ("kappa",), "1/47", "auxiliary-to-variance gap"),
        ("alter_zero_delta_certificate", ("zero_delta", "q2"), "2", "zero-delta nonnegative certificate"),
        ("alter_positive_delta_scalar", ("positive_scalar", "delta_u"), "-41", "positive-delta scalar H"),
        ("reverse_full_slack_delta_loss", ("linear_loss", "delta"), "-1/2", "full slack is Q"),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="variance-mutations-") as temp:
        temp = Path(temp)
        for name, keys, replacement, expected in mutations:
            changed = copy.deepcopy(data)
            slot = changed
            for key in keys[:-1]:
                slot = slot[key]
            slot[keys[-1]] = replacement
            cert = temp / (name + ".json")
            cert.write_text(json.dumps(changed, indent=2) + "\n", encoding="utf-8")
            outcome = run(ROOT, cert)
            require(outcome.returncode != 0 and expected in outcome.stderr,
                    "Mutation was not rejected at intended check: " + name + "\n" + outcome.stdout + outcome.stderr)
            results.append({"mutation": name, "result": "REJECTED",
                            "exit_code": outcome.returncode, "intended_check": expected})

        # Copying is only for deliberate source/example corruption. The checker
        # itself remains the unmutated program at ROOT.
        source_root = temp / "source_corruption"
        shutil.copytree(ROOT, source_root, ignore=shutil.ignore_patterns("__pycache__", "*.zip"))
        tail = source_root / "sources/openai/tail.tex"
        tail.write_bytes(tail.read_bytes() + b"% deliberate mutation\n")
        outcome = run(source_root)
        expected = "Source byte length: sources/openai/tail.tex"
        require(outcome.returncode != 0 and expected in outcome.stderr,
                "Source mutation not rejected by source pin check")
        results.append({"mutation": "alter_pinned_tail_bytes", "result": "REJECTED",
                        "exit_code": outcome.returncode, "intended_check": expected})

        example_root = temp / "infeasible_example"
        shutil.copytree(ROOT, example_root, ignore=shutil.ignore_patterns("__pycache__", "*.zip"))
        example_path = example_root / "examples.json"
        examples = json.loads(example_path.read_text(encoding="utf-8"))
        examples["examples"][0]["tuple"]["v"] = "1/10"
        example_path.write_text(json.dumps(examples, indent=2) + "\n", encoding="utf-8")
        outcome = run(example_root)
        expected = "Example violates exact source domain"
        require(outcome.returncode != 0 and expected in outcome.stderr,
                "Infeasible sharpness mutation not rejected")
        results.append({"mutation": "violate_per_index_v_bound", "result": "REJECTED",
                        "exit_code": outcome.returncode, "intended_check": expected})

    print(json.dumps({"status": "PASS", "baseline": "PASS", "mutations": results,
                      "rejected": len(results), "limitations":
                      "Mutations test selected verifier failures; the conventional proof remains necessary."}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, KeyError, OSError) as err:
        print("FAIL: " + str(err), file=sys.stderr)
        raise SystemExit(1)

