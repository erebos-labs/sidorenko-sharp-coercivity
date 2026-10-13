#!/usr/bin/env python3
"""Regenerate only the fixed original-template 33-coordinate certificate.

There is no template search or finite-host operation. All arithmetic is exact.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import reduce
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path


def lcm(a, b):
    return a // gcd(a, b) * b


def inverse_integer_matrix(A):
    n = len(A)
    rows = [[F(x) for x in row] + [F(i == j) for j in range(n)]
            for i, row in enumerate(A)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if rows[i][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        rows[col] = [x / divisor for x in rows[col]]
        for i in range(n):
            if i != col and rows[i][col]:
                factor = rows[i][col]
                rows[i] = [a - factor*b for a, b in zip(rows[i], rows[col])]
    inverse = [row[n:] for row in rows]
    tau = reduce(lcm, (x.denominator for row in inverse for x in row), 1)
    N = [[int(tau * x) for x in row] for row in inverse]
    common = reduce(gcd, (x for row in N for x in row), tau)
    return [[x // common for x in row] for row in N], tau // common


def main():
    base = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("variance_downstream_checker", base / "check_downstream.py")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    source = json.loads((base / "sources/global/experiment/template_data.json").read_text())
    original = source["original"]
    edges, de, L, orders = checker.build_template(original)
    A = [[L[i][j] + (4 * de[i] if i == j else 0) for j in range(33)]
         for i in range(33)]
    N, tau = inverse_integer_matrix(A)
    b = [12 - x for x in de]
    u = [sum(N[i][j]*b[j] for j in range(33)) for i in range(33)]
    Hnum = sum(bi * ui for bi, ui in zip(b, u))

    def strict_bound(B):
        for i in range(33):
            margin = B*tau - 2*u[i]
            if margin <= 0 or margin**2 <= 4*Hnum*N[i][i]:
                return False
        return True

    # Find the least strict integer coordinate threshold for this fixed ellipsoid.
    lo, hi = 0, 1
    while not strict_bound(hi):
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if strict_bound(mid):
            hi = mid
        else:
            lo = mid
    B = hi
    M, D = B - 1, 12 * (B - 1)
    source_paths = [
        "sources/openai/tail.tex",
        "sources/openai/planted.tex",
        "sources/global/global-residual-dimension.md",
        "sources/global/experiment/template_data.json",
        "sources/global/experiment/certificates.json",
        "sources/effective-host/PROOF.md",
    ]
    certificate = {
        "format": "sidorenko-original-variance-energy-v1",
        "kappa": "1/48",
        "template": original,
        "source_pins": {
            "openai_math": "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb",
            "global_energy": "9922b05bf2c3418e1a46378d4ebac60e8a34ce51",
            "recovered_effective_proof": "06acd4cf46bfe9086f9abc7d85b5c9f171480143",
        },
        "source_sha256": {p: sha256((base / p).read_bytes()).hexdigest() for p in source_paths},
        "edge_order": list(map(list, edges)),
        "three_rho": de,
        "exposure_orders": orders,
        "matrix_scale": 48,
        "A": A,
        "inverse_numerator": N,
        "inverse_denominator": tau,
        "u": u,
        "Hnum": Hnum,
        "strict_bound_B": B,
        "M_bound": M,
        "sufficient_even_D": D,
        "coordinate_linear_margins": [24*B*tau - 48*ui for ui in u],
        "coordinate_squared_margins": [
            (24*B*tau - 48*u[i])**2 - 48**2*Hnum*N[i][i] for i in range(33)
        ],
        "retained_nondirect_remainder": 1196,
        "old_M_bound": 608,
        "old_even_D": 7296,
    }
    report = checker.verify_certificate(certificate, base)
    destination = base / "original_certificate.json"
    destination.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
