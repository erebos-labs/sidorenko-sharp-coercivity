#!/usr/bin/env python3
"""Replay the original-template variance-energy certificate, exactly.

Standard library only. Source files are read as data, never executed.
The conventional proof in DOWNSTREAM.md supplies all domain arguments.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


class Polynomial:
    """A small sparse multivariate Q-polynomial implementation."""
    def __init__(self, terms=None):
        self.terms = {m: F(c) for m, c in (terms or {}).items() if c}

    @staticmethod
    def cast(x):
        return x if isinstance(x, Polynomial) else Polynomial({(): F(x)})

    def __add__(self, other):
        out = dict(self.terms)
        for m, c in self.cast(other).terms.items():
            out[m] = out.get(m, F(0)) + c
        return Polynomial(out)

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.cast(other))

    def __rsub__(self, other):
        return self.cast(other) + (-self)

    def __mul__(self, other):
        out = defaultdict(F)
        for ma, ca in self.terms.items():
            for mb, cb in self.cast(other).terms.items():
                mon = Counter(dict(ma))
                mon.update(dict(mb))
                out[tuple(sorted(mon.items()))] += ca * cb
        return Polynomial(out)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1 / F(scalar))

    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError("Polynomial exponent must be a nonnegative integer")
        out = self.cast(1)
        for _ in range(exponent):
            out = out * self
        return out

    def substitute(self, replacements):
        out = self.cast(0)
        for monomial, coefficient in self.terms.items():
            term = self.cast(coefficient)
            for name, exponent in monomial:
                term *= self.cast(replacements.get(name, variable(name))) ** exponent
            out += term
        return out


def variable(name):
    return Polynomial({((name, 1),): F(1)})


def require(condition, label):
    if not condition:
        raise ValueError(label)


def same(left, right, label):
    residual = Polynomial.cast(left) - right
    require(not residual.terms, "Polynomial identity: " + label)


def symbolic_checks(kappa):
    """Coefficient identities supporting all activity cases and mode removal."""
    labels = []

    def check(left, right, label):
        same(left, right, label)
        labels.append(label)

    c, d, delta, v = map(variable, ("c", "d", "delta", "v"))
    p = [variable("p" + str(i)) for i in range(3)]
    t = [variable("t" + str(i)) for i in range(3)]
    P, T = sum(p), sum(t)
    n = [2 * p[i] - t[i] for i in range(3)]
    b = lambda x: x * (x + 1) / 2
    Q = (c * (d + delta) - delta * d + 2 * delta**2) / 4
    Q += sum(n[i] ** 2 / 6 + delta * p[i] - c * (p[i] + t[i]) / 6
             for i in range(3))
    Q += v * ((d - 3 * delta) / 2 - P) + v**2 / 2
    loss = c / 4 + delta / 2 + (2 * P - T) / 6 + v / 2
    S = Q - loss
    source_S = (c * (d + delta - 1) - delta * (d + 2) + 2 * delta**2) / 4
    source_S += sum(n[i] * (n[i] - 1) / 6 + delta * p[i]
                    - c * (p[i] + t[i]) / 6 for i in range(3))
    source_S += v * ((d - 3 * delta) / 2 - P + v) - b(v)
    check(S, source_S, "full source slack Q minus linear loss")
    check((3 * c + P + T) / 2 - loss,
          c / 4 + c - delta + 2 * T / 3 + (P / 3 + delta - v) / 2,
          "three-active loss envelope")

    H, x, y = map(variable, ("H", "x", "y"))
    Vh = (H - x)**2 + (H - y)**2 + (x - y)**2
    check(2 * H**2 - Vh,
          2 * (x * (H - x) + y * (H - y) + x * y),
          "pair variance bounded by twice maximum squared")
    check((H**2 / 24 - H / 12) - (kappa * Vh - (H + x + y) / 2),
          (F(1, 48) - kappa) * Vh + (2 * H**2 - Vh) / 48
          + (x + y) / 2 + 5 * H / 12,
          "all lower-activity energy transfer")
    s0, s1, s2 = map(variable, ("s0", "s1", "s2"))
    baseline = ((d + c + 1) * c + b(s0) + b(s1) + b(s2)) / 2
    baseline -= (b(c + s0) + b(c + s1) + b(c + s2)) / 6
    check(baseline - (b(c + s0) / 3 + b(c) / 6 + (b(s1) + b(s2)) / 3),
          c * (3 * d - 3 * s0 - s1 - s2) / 6,
          "lower-activity baseline identity")
    k = variable("k")
    check(b(2 * k) / 3 - b(k), k * (k - 1) / 6,
          "even pair dimension floor gain")
    check(b(2 * k + 1) / 3 - b(k), (k + 1) * (k + 2) / 6,
          "odd pair dimension floor gain")
    check((2 * k) * (2 * k + 2) / 8 - b(k), 0,
          "even floor gain quadratic envelope")
    check((2 * k + 1) * (2 * k + 3) / 8 - b(k), (4 * k + 3) / 8,
          "odd floor gain quadratic envelope")

    S0 = 3 * c * (c - 1) / 4
    S0 += sum(n[i]**2 + (c - 1) * n[i] + 3 * c * p[i]
              for i in range(3)) / 6
    qmode = (c - delta) / 2
    bracket_c = d - 3 * c - 2 * delta + 2 - 4 * P
    bracket_v = d - 3 * delta - 2 * P + v - 1
    check(S, S0 + qmode * bracket_c / 2 + v * bracket_v / 2,
          "exact integer mode-removal identity")
    M = variable("M")
    check(bracket_c - (d + c - 12 * M + 6 * c + 2),
          2 * (c - delta) + 4 * (3 * (M - c) - P),
          "common mode bracket comparison")
    check(bracket_v - (d + c - 6 * M + 2 * c + v - 1),
          3 * (c - delta) + 2 * (3 * (M - c) - P),
          "v mode bracket comparison")
    check(S0, (c - 1) * (5 * c + 1) / 8
          + sum((ni + (c - 1) / 2)**2 for ni in n) / 6 + c * P / 2,
          "positive common dimension square completion")
    check(S0.substitute({"c": 1}), sum(ni**2 for ni in n) / 6 + P / 2,
          "common dimension one equality expression")
    check(S0.substitute({"c": 0}), sum(ni * (ni - 1) for ni in n) / 6,
          "common dimension zero integer expression")

    D = variable("D")
    zeros = {"d": 0, "delta": 0, "v": 0, "c": D}
    zeros.update({"p" + str(i): 0 for i in range(3)})
    zeros.update({"t" + str(i): 0 for i in range(3)})
    check(S.substitute(zeros), -D / 4, "negative fully coincident slack control")
    half = {"c": 0, "delta": 0, "v": 0, "d": D}
    half.update({"p" + str(i): F(1, 2) for i in range(3)})
    half.update({"t" + str(i): F(1, 2) for i in range(3)})
    check(S.substitute(half), F(-1, 8), "fractional tuple local negative slack")
    check(22 * S.substitute(half) + 1, F(-7, 4),
          "integer-mode removal cannot be applied to real tuples")

    # Exact remaining exponent identities use no new analytic input.
    m, span = map(variable, ("m", "span"))
    check((-span**2 + 2 * m * span - 2 * m + 468),
          (m**2 - 2 * m + 468) - (span - m)**2,
          "retained robust nondirect completion")
    require(28**2 - 2 * 28 + 468 == 1196, "retained nondirect constant 1196")
    return labels


def connected(adjacency, vertices=None):
    subset = set(adjacency) if vertices is None else set(vertices)
    if not subset:
        return False
    reached = {min(subset)}
    queue = deque(reached)
    while queue:
        for nxt in adjacency[queue.popleft()]:
            if nxt in subset and nxt not in reached:
                reached.add(nxt)
                queue.append(nxt)
    return reached == subset


def build_template(original):
    faces = [tuple(face) for face in original["faces"]]
    bits = original["bits"]
    require(len(faces) == 22 and len(set(faces)) == 22, "22 distinct faces")
    require(all(len(f) == 3 and tuple(sorted(set(f))) == f for f in faces),
            "ordered triangular faces")
    require(set().union(*map(set, faces)) == set(range(13)), "13 point vertices")
    require(len(bits) == 22 and all(len(s) == 3 and set(s) <= {"0", "1"}
                                   for s in bits), "22 bit strings")
    edge_faces = defaultdict(list)
    for j, face in enumerate(faces):
        for edge in combinations(face, 2):
            edge_faces[edge].append(j)
    edges = sorted(edge_faces)
    require(len(edges) == 33 and all(len(v) == 2 for v in edge_faces.values()),
            "33 point pairs, each in two faces")
    require(13 - 33 + 22 == 2 and 13 + 22 == 35 and 3 * 22 == 66,
            "sphere and incidence counts")
    point_graph = {i: set() for i in range(13)}
    dual = {i: set() for i in range(22)}
    for (a, b), (j, k) in edge_faces.items():
        point_graph[a].add(b)
        point_graph[b].add(a)
        dual[j].add(k)
        dual[k].add(j)
    require(connected(point_graph) and connected(dual), "connected original graphs")
    require(max(map(len, point_graph.values())) == 6, "point degree at most six")
    for point in range(13):
        link = {i: set() for i in point_graph[point]}
        for face in faces:
            if point in face:
                a, b = [x for x in face if x != point]
                link[a].add(b)
                link[b].add(a)
        require(connected(link) and all(len(x) == 2 for x in link.values()),
                "vertex link cycle")

    exposure_orders = []
    for bit in range(3):
        boundary = [e for e, (j, k) in edge_faces.items() if bits[j][bit] != bits[k][bit]]
        boundary_graph = {i: set() for i in range(13)}
        for a, b in boundary:
            boundary_graph[a].add(b)
            boundary_graph[b].add(a)
        require(len(boundary) == 13 and connected(boundary_graph)
                and all(len(v) == 2 for v in boundary_graph.values()),
                "literal cut is Hamiltonian")
        for value in ("0", "1"):
            subset = {j for j in range(22) if bits[j][bit] == value}
            require(len(subset) == 11 and connected(dual, subset), "eleven-face class")
            require(sum(len(dual[j] & subset) for j in subset) == 20,
                    "class dual is a tree")
            root = min(subset)
            order = []
            reached = {root}
            queue = deque([root])
            while queue:
                j = queue.popleft()
                order.append(j)
                for k in sorted(dual[j] & subset):
                    if k not in reached:
                        reached.add(k)
                        queue.append(k)
            seen = set(faces[order[0]])
            for j in order[1:]:
                require(len(set(faces[j]) - seen) == 1, "fresh point in exposure")
                seen.update(faces[j])
            require(seen == set(range(13)), "exposure uses every point")
            exposure_orders.append(order)

    excess = []
    for edge in edges:
        j, k = edge_faces[edge]
        excess.append(sum(a != b for a, b in zip(bits[j], bits[k])) - 1)
    require(all(x >= 0 for x in excess) and sum(excess) == 6,
            "nonnegative excess with sum rho two")
    expected = {(0, 2): 2, (4, 8): 1, (5, 6): 1, (5, 10): 1, (7, 12): 1}
    require({e: de for e, de in zip(edges, excess) if de} == expected,
            "five exact anchors")
    residual_graph = {i: set() for i in range(13)}
    for (a, b), de in zip(edges, excess):
        if de == 0:
            residual_graph[a].add(b)
            residual_graph[b].add(a)
    degrees = list(map(len, residual_graph.values()))
    require(degrees == [3, 6, 3, 6, 4, 2, 4, 4, 4, 6, 4, 6, 4],
            "retained residual support degree caps")
    require(sum(degrees) == 56 and sum(x * (2*x-1) for x in degrees) == 468,
            "retained robust count support data")
    index = {edge: i for i, edge in enumerate(edges)}
    L = [[0] * 33 for _ in edges]
    edge_graph = {i: set() for i in range(33)}
    for face in faces:
        ids = [index[e] for e in combinations(face, 2)]
        for a, b in combinations(ids, 2):
            L[a][a] += 1
            L[b][b] += 1
            L[a][b] -= 1
            L[b][a] -= 1
            edge_graph[a].add(b)
            edge_graph[b].add(a)
    require(connected(edge_graph), "connected triangle edge graph")
    return edges, excess, L, exposure_orders


def verify_certificate(certificate, base):
    require(certificate["format"] == "sidorenko-original-variance-energy-v1", "format")
    kappa = F(certificate["kappa"])
    require(F(1, 144) < kappa <= F(1, 48), "admitted coefficient range")
    # Source bindings pin data and proof interfaces, not just mutable filenames.
    for relative, digest in certificate["source_sha256"].items():
        data = (base / relative).read_bytes()
        require(sha256(data).hexdigest() == digest, "source SHA256: " + relative)
    source = json.loads((base / "sources/global/experiment/template_data.json").read_text())
    require(certificate["template"] == source["original"], "exact pinned original literals")
    edges, excess, L, exposure_orders = build_template(certificate["template"])
    require(certificate["edge_order"] == list(map(list, edges)), "lexicographic edge order")
    require(certificate["three_rho"] == excess, "literal excess vector")
    require(certificate["exposure_orders"] == exposure_orders, "six exposure orders")
    labels = symbolic_checks(kappa)

    # Verify only the original-template baseline matrix from the pinned artifact.
    # Its old residual-189 assertion is not used: the retained remainder is 1196.
    prior = json.loads((base / "sources/global/experiment/certificates.json").read_text())
    old = prior["templates"]["original"]
    old_N, old_tau = old["adjugate"], old["denominator"]
    require(old["edge_order"] == list(map(list, edges)), "baseline pair order")
    old_A = [[L[i][j] + (12 * excess[i] if i == j else 0)
              for j in range(33)] for i in range(33)]
    for i in range(33):
        for j in range(33):
            require(sum(old_A[i][k] * old_N[k][j] for k in range(33))
                    == (old_tau if i == j else 0), "baseline inverse matrix product")
    old_b = [12 - x for x in excess]
    old_u = [sum(old_N[i][j] * old_b[j] for j in range(33)) for i in range(33)]
    old_Hnum = sum(old_b[i] * old_u[i] for i in range(33))
    for i in range(33):
        margin = 609 * old_tau - 6 * old_u[i]
        require(margin > 0 and margin**2 > 36 * old_Hnum * old_N[i][i],
                "baseline strict coordinate inequalities")
    require((old["strict_bound_B"], old["M"], old["D"]) == (609, 608, 7296),
            "baseline original M and D")

    scale = certificate["matrix_scale"]
    require(isinstance(scale, int) and scale > 0, "positive matrix scale")
    A = [[scale * kappa * L[i][j] + (F(scale * excess[i], 12) if i == j else 0)
          for j in range(33)] for i in range(33)]
    require(all(x.denominator == 1 for row in A for x in row), "integral scaled energy")
    A = [[int(x) for x in row] for row in A]
    require(A == certificate["A"], "reconstructed exact energy matrix")
    N, tau = certificate["inverse_numerator"], certificate["inverse_denominator"]
    require(isinstance(tau, int) and tau > 0, "inverse denominator positive")
    require(len(N) == 33 and all(len(row) == 33 for row in N)
            and all(isinstance(x, int) for row in N for x in row), "integer inverse shape")
    require(all(N[i][j] == N[j][i] for i in range(33) for j in range(33)),
            "symmetric inverse numerator")
    for i in range(33):
        for j in range(33):
            require(sum(A[i][k] * N[k][j] for k in range(33)) == (tau if i == j else 0),
                    "inverse matrix product")
    bvec = [12 - x for x in excess]
    u = [sum(N[i][j] * bvec[j] for j in range(33)) for i in range(33)]
    Hnum = sum(bvec[i] * u[i] for i in range(33))
    require(Hnum > 0 and all(N[i][i] > 0 for i in range(33)), "positive inverse diagonal")
    require(u == certificate["u"] and Hnum == certificate["Hnum"], "inverse right-hand side")
    B = certificate["strict_bound_B"]
    require(isinstance(B, int) and B > 0, "integer strict bound")
    linear = [24 * B * tau - scale * u[i] for i in range(33)]
    squared = [linear[i]**2 - scale**2 * Hnum * N[i][i] for i in range(33)]
    require(all(x > 0 for x in linear) and all(x > 0 for x in squared),
            "strict coordinate inequalities")
    require(linear == certificate["coordinate_linear_margins"]
            and squared == certificate["coordinate_squared_margins"], "all coordinate margins")
    M, D = certificate["M_bound"], certificate["sufficient_even_D"]
    require(M == B - 1 and D == 12 * M and D % 2 == 0, "integer M and D metadata")
    require(D >= 12 and D - 1196 >= F(1, 6), "retained transverse and residual thresholds")
    require(certificate["retained_nondirect_remainder"] == 1196,
            "retain robust nondirect remainder")
    require(certificate["old_M_bound"] == 608 and certificate["old_even_D"] == 7296,
            "comparison baseline")
    require(M < 608 and D < 7296, "claimed numerical improvement")
    # Positive common dimension one would give h=1 everywhere and excess=1.
    require(sum(F(x, 3) for x in excess) / 2 == 1, "common-one mode exclusion anchor")
    # Three local activity subsets of size two, three of size one, one of each other size.
    masks = [tuple((mask >> i) & 1 for i in range(3)) for mask in range(8)]
    require(Counter(map(sum, masks)) == {0: 1, 1: 3, 2: 3, 3: 1}, "all local activity cases")
    return {
        "status": "PASS",
        "kappa": str(kappa),
        "polynomial_identities": len(labels),
        "local_activity_masks": len(masks),
        "original_point_vertices": 13,
        "original_faces": 22,
        "original_point_pairs": 33,
        "literal_cuts": 3,
        "fresh_point_exposures": 6,
        "inverse_product_entries": 1089,
        "strict_coordinate_bounds": 33,
        "baseline_inverse_product_entries": 1089,
        "baseline_strict_coordinate_bounds": 33,
        "inverse_denominator": tau,
        "Hnum": Hnum,
        "strict_bound_B": B,
        "M_bound": M,
        "sufficient_even_D": D,
        "minimum_linear_margin": min(linear),
        "minimum_squared_margin": min(squared),
        "retained_nondirect_remainder": 1196,
        "nondirect_exponent_saving": D - 1196,
        "local_slack_nonnegativity_assumed": False,
        "integer_mode_removal_applied_to_real_domain": False,
        "symbolic_identity_labels": labels,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    path = args.certificate or base / "original_certificate.json"
    certificate = json.loads(path.read_text())
    report = verify_certificate(certificate, base)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
