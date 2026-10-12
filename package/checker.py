#!/usr/bin/env python3
"""Exact finite symbolic certificate checker for the relaxed-domain Q bound.

Run: python3 -I -B checker.py

Python standard library only. No network, source-program imports, floating point,
computer algebra dependency, sampling, or proof-assistant claim. The checker
compares sparse rational polynomial coefficients and rational examples. The
conventional argument that the displayed terms are nonnegative, and its full
equality classification, remain in the accompanying proof. Source formulae are
explicit transcriptions of the hash-bound TeX, not a general TeX parser.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


class CheckFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def rational(value):
    require(isinstance(value, (str, int)) and not isinstance(value, bool),
            "Rational literals must be strings or integers, never floating point")
    return Fraction(value)


class Poly:
    """Sparse polynomial over Q; monomials are sorted (variable, power) pairs."""

    def __init__(self, terms=None):
        self.terms = {m: Fraction(c) for m, c in (terms or {}).items() if c}

    @staticmethod
    def coerce(value):
        if isinstance(value, Poly):
            return value
        return Poly({(): Fraction(value)})

    def __add__(self, other):
        result = dict(self.terms)
        for monomial, coefficient in Poly.coerce(other).terms.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly.coerce(other))

    def __rsub__(self, other):
        return Poly.coerce(other) + (-self)

    def __mul__(self, other):
        result = {}
        for ma, ca in self.terms.items():
            for mb, cb in Poly.coerce(other).terms.items():
                powers = dict(ma)
                for variable, power in mb:
                    powers[variable] = powers.get(variable, 0) + power
                monomial = tuple(sorted(powers.items()))
                result[monomial] = result.get(monomial, Fraction(0)) + ca * cb
        return Poly(result)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        require(not isinstance(scalar, Poly), "Only rational scalar division is allowed")
        return self * (Fraction(1) / Fraction(scalar))

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "Nonnegative integer power required")
        result = Poly.coerce(1)
        for _ in range(exponent):
            result = result * self
        return result

    def sub(self, replacements):
        result = Poly()
        for monomial, coefficient in self.terms.items():
            term = Poly.coerce(coefficient)
            for variable, power in monomial:
                term = term * Poly.coerce(replacements.get(variable, V(variable))) ** power
            result = result + term
        return result

    def evaluate(self, values):
        result = self.sub(values)
        require(all(m == () for m in result.terms), "Evaluation left unassigned variables")
        return result.terms.get((), Fraction(0))

    def homogeneous(self, degree):
        return Poly({m: c for m, c in self.terms.items()
                     if sum(e for _, e in m) == degree})

    def __repr__(self):
        return repr(sorted(self.terms.items()))


def V(name):
    return Poly({((name, 1),): Fraction(1)})


def load_polynomial(data):
    variables = data["variables"]
    require(len(set(variables)) == len(variables), "Repeated polynomial variable")
    result = Poly()
    seen = set()
    for coefficient, exponents in data["terms"]:
        require(len(exponents) == len(variables), "Wrong exponent count")
        require(all(isinstance(e, int) and e >= 0 for e in exponents), "Invalid exponent")
        monomial = tuple(sorted((v, e) for v, e in zip(variables, exponents) if e))
        require(monomial not in seen, "Duplicate literal monomial")
        seen.add(monomial)
        result = result + Poly({monomial: rational(coefficient)})
    return result


class Checks:
    def __init__(self):
        self.identities = 0
        self.positive_checks = 0

    def identity(self, name, left, right):
        difference = Poly.coerce(left) - right
        require(not difference.terms,
                "IDENTITY FAILED: " + name + "; residual=" + repr(difference))
        self.identities += 1

    def nonnegative_coefficients(self, name, expression, positive_variables):
        expression = Poly.coerce(expression)
        allowed = set(positive_variables)
        require(all(c >= 0 for c in expression.terms.values()),
                "NEGATIVE COEFFICIENT: " + name)
        require(all(v in allowed for m in expression.terms for v, _ in m),
                "NONNEGATIVITY DOMAIN ERROR: " + name)
        self.positive_checks += 1


def bfun(z):
    return z * (z + 1) / 2


def source_expressions():
    """Transcribe source eqs tail-quadratic, slack, and planted-gain independently."""
    c, d, delta, v = (V(name) for name in ("c", "d", "delta", "v"))
    p = [V("p" + str(i)) for i in range(1, 4)]
    t = [V("t" + str(i)) for i in range(1, 4)]
    P, T = sum(p), sum(t)
    n = [2 * pi - ti for pi, ti in zip(p, t)]
    z = (d - 3 * delta) / 2 - P
    w = z + v
    Q = (c * (d + delta) - delta * d + 2 * delta**2) / 4
    Q = Q + sum(ni**2 / 6 + delta * pi - c * (pi + ti) / 6
                for ni, pi, ti in zip(n, p, t)) + v * z + v**2 / 2
    N = P**2 + T**2 + delta**2
    L = c / 4 + delta / 2 + (2 * P - T) / 6 + v / 2
    S = (c * (d + delta - 1) - delta * (d + 2) + 2 * delta**2) / 4
    S = S + sum(ni * (ni - 1) / 6 + delta * pi - c * (pi + ti) / 6
                for ni, pi, ti in zip(n, p, t)) + v * w - bfun(v)
    D = c + d
    r = D / 2
    u = (c + delta) / 2
    gC_unsimplified = 3 * (bfun(r) - bfun(r - u)) - u * d - bfun(u)
    gC = (r + c + 1) * u - 2 * u**2
    pair_s = [pi + ti for pi, ti in zip(p, t)]
    C = (D + 1) * c + sum(bfun(si) for si in pair_s)
    beta = C / 2 - sum(bfun(c + si) for si in pair_s) / 6
    # g below is one planted maximand, not a maximization over a real domain.
    g = (gC + sum(bfun(si) for si in pair_s) - delta * P
         - sum(pi**2 for pi in p) - v * w - sum(bfun(ti) for ti in t) + bfun(v))
    return locals()


def check_sources(root, pins_path):
    pins = json.loads(pins_path.read_text(encoding="utf-8"))
    require(pins["schema_version"] == 1, "Unsupported source-pins schema")
    entries = pins["files"]
    require(len({e["path"] for e in entries}) == len(entries), "Duplicate source path")
    paths = {e["path"]: e for e in entries}
    mandatory = {
        "sources/openai/tail.tex": ("openai/math", "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb",
                                     "dc11e07a592e70d3a13e3a005c72378c88edc351"),
        "sources/openai/planted.tex": ("openai/math", "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb",
                                        "e1a4636e66361dae0f5918e1245950060535a83c"),
        "sources/openai/LICENSE": ("openai/math", "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb",
                                    "261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64")
    }
    require(set(paths) == set(mandatory), "Unexpected source-pins file inventory")
    for path, expected in mandatory.items():
        require(path in paths, "Missing mandatory pinned source: " + path)
        entry = paths[path]
        require((entry["repository"], entry["commit"], entry["git_blob_sha1"]) == expected,
                "Immutable source pin differs: " + path)
    for entry in entries:
        path = (root / entry["path"]).resolve()
        require(path.is_relative_to(root), "Source path escapes artifact directory")
        data = path.read_bytes()
        sha256 = hashlib.sha256(data).hexdigest()
        git_blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
        require(sha256 == entry["sha256"], "Source SHA256 mismatch: " + entry["path"])
        require(git_blob == entry["git_blob_sha1"], "Source git blob mismatch: " + entry["path"])
    tail = (root / "sources/openai/tail.tex").read_text(encoding="utf-8")
    for label in ("eq:tail-feasible", "eq:tail-quadratic", "eq:tail-scalar-quadratic", "lem:coercivity"):
        require("\\label{" + label + "}" in tail, "Missing required source label: " + label)
    print("PASS source binding: " + str(len(entries)) + " SHA256 and git-blob checks; immutable source pins match")


def check_symbolic(cert, checks):
    require(cert["schema_version"] == 1, "Unsupported certificate schema")
    require(cert["denominator"] == "P^2+T^2+delta^2", "Unexpected denominator")
    kappa = rational(cert["kappa"])
    require(kappa > 0, "Kappa must be positive")
    polys = {name: load_polynomial(data) for name, data in cert["polynomials"].items()}
    src = source_expressions()
    c, d, delta, v = (src[name] for name in ("c", "d", "delta", "v"))
    p, t, n, P, T, z, w, Q, N = (src[name] for name in ("p", "t", "n", "P", "T", "z", "w", "Q", "N"))
    checks.identity("planted common gain, expanded counting formula", src["gC_unsimplified"], src["gC"])
    checks.identity("beta minus planted maximand equals exact slack", src["beta"] - src["g"], src["S"])
    checks.identity("source full slack equals Q minus linear loss", src["S"], Q - src["L"])
    checks.identity("homogeneous degree-two part of exact slack is Q", src["S"].homogeneous(2), Q)
    checks.identity("full slack has no degree outside one and two", src["S"], src["S"].homogeneous(2) + src["S"].homogeneous(1))

    # Sharpness is checked before the endpoint certificate. A kappa mutation is
    # thus rejected here against the independently transcribed source Q.
    y, excess_c, excess_d = V("y"), V("excess_c"), V("excess_d")
    equality_sub = {"c": y + excess_c, "d": 3 * y, "delta": -y, "v": 0}
    equality_sub.update({"p" + str(i): y for i in range(1, 4)})
    equality_sub.update({"t" + str(i): 0 for i in range(1, 4)})
    Qeq, Neq = Q.sub(equality_sub), N.sub(equality_sub)
    checks.identity("sharpness family Q", Qeq, rational(cert["sharpness_Q_coefficient"]) * y**2)
    checks.identity("sharpness family denominator", Neq, rational(cert["sharpness_N_coefficient"]) * y**2)
    checks.identity("sharpness: Q = kappa N", Qeq, kappa * Neq)
    family_residuals = [c - y, d - P - T, v, w] + p + t
    family_residuals += [pi + delta - ti for pi, ti in zip(p, t)]
    family_residuals += [pi + delta - v for pi in p]
    for i, residual in enumerate(family_residuals):
        checks.nonnegative_coefficients("sharp family constraint " + str(i), residual.sub(equality_sub), {"y", "excess_c"})
    unrestricted_eq = dict(equality_sub)
    unrestricted_eq.pop("c")
    unrestricted_eq.pop("d")
    checks.identity("remaining equality gap with c,d retained",
                    (Q - kappa * N).sub(unrestricted_eq), (c + y) * (d - 3 * y) / 4)
    remaining_gap = ((c + y) * (d - 3 * y) / 4).sub({"c": y + excess_c, "d": 3 * y + excess_d})
    checks.nonnegative_coefficients("remaining equality gap on c>=y,d>=3y", remaining_gap,
                                   {"y", "excess_c", "excess_d"})

    b = V("b")
    common = (c * (d + delta) - delta * d + 2 * delta**2) / 4
    Phi = common + (2 * P - T)**2 / 18 + delta * P - c * (P + T) / 6 - b**2 / 2
    variance = sum((n[i] - n[j])**2 for i in range(3) for j in range(i + 1, 3)) / 18
    checks.identity("three-pair variance gap", sum(ni**2 for ni in n) / 6 - (2 * P - T)**2 / 18, variance)
    checks.identity("Q minus Phi, z>=0 (a=0)", Q - Phi, variance + v**2 / 2 + z * v + b**2 / 2)
    checks.identity("Q minus Phi, z<=0 (a=-z)", Q - Phi, variance + (v + z)**2 / 2 + (b**2 - z**2) / 2)
    checks.identity("constraint sum giving T<=P+3delta", P + 3 * delta - T, sum(pi + delta - ti for pi, ti in zip(p, t)))
    checks.identity("constraint average giving v<=P/3+delta", P / 3 + delta - v, sum(pi + delta - v for pi in p) / 3)
    checks.identity("nonnegative decomposition of d+3delta", d + 3 * delta, (d - P - T) + (P + 3 * delta - T) + 2 * T)
    checks.identity("a<=first b argument when z<=0", P / 3 + delta + z, sum(pi + delta - v for pi in p) / 3 + w)
    checks.identity("a<=second b argument when z<=0", (P - T + 3 * delta) / 2 + z, (d - P - T) / 2)
    A = (d + delta) / 4 - (P + T) / 6
    checks.identity("c coefficient nonnegative decomposition", A, (d + 3 * delta) / 12 + (d - P - T) / 6)
    checks.identity("c reduction for delta>=0", Phi - Phi.sub({"c": delta}), (c - delta) * A)
    checks.identity("c reduction for delta=-y", Phi.sub({"delta": -y}) - Phi.sub({"delta": -y, "c": y}), (c - y) * A.sub({"delta": -y}))

    # Now use independent aggregate variables, and subtract the actual target
    # denominator before either interval minimization.
    P, T, delta, x, y, s, lam = (V(name) for name in ("P", "T", "delta", "x", "y", "s", "lam"))
    c, d = V("c"), V("d")
    Phi_aggregate = ((c * (d + delta) - delta * d + 2 * delta**2) / 4
                     + (2 * P - T)**2 / 18 + delta * P - c * (P + T) / 6 - b**2 / 2)
    F = 3 * delta**2 / 4 + (2 * P - T)**2 / 18 + (5 * P - T) * delta / 6 - b**2 / 2
    G = y**2 / 4 + (2 * x - T) * y / 3 + (2 * x - T)**2 / 18 - b**2 / 2
    checks.identity("positive delta scalar reduction", Phi_aggregate.sub({"c": delta}), F)
    checks.identity("negative delta scalar reduction and exact d loss",
                    Phi_aggregate.sub({"c": y, "delta": -y, "P": x + 3 * y}),
                    G + y * (d - (x + 3 * y) - T) / 2)
    first_square = rational(cert["first_interval_square_coefficient"])
    chord_coefficient = rational(cert["second_interval_chord_coefficient"])
    require(first_square > 0 and chord_coefficient > 0, "Interval certificate coefficients must be positive")
    for sign, base, norm, B, U, second_b, variables in (
        ("plus", F, P**2 + T**2 + delta**2, P / 3 + delta, P + 3 * delta,
         (P - T + 3 * delta) / 2, {"P", "delta"}),
        ("minus", G, (x + 3 * y)**2 + T**2 + y**2, x / 3, x,
         (x - T) / 2, {"x", "y"})
    ):
        H_first = base.sub({"b": B}) - kappa * norm
        H_second = base.sub({"b": second_b}) - kappa * norm
        E_B = polys["E_" + sign + "_B"]
        E_U = polys["E_" + sign + "_U"]
        C_first = polys["C_" + sign]
        checks.identity(sign + " min branch comparison", second_b - B, (B - T) / 2)
        checks.identity(sign + " breakpoint from first interval", H_first.sub({"T": B}), E_B)
        checks.identity(sign + " breakpoint from second interval", H_second.sub({"T": B}), E_B)
        checks.identity(sign + " final endpoint", H_second.sub({"T": U}), E_U)
        checks.identity(sign + " first interval nonnegative certificate",
                        H_first.sub({"T": B - s}), E_B + s * C_first + first_square * s**2)
        checks.identity(sign + " second interval chord certificate",
                        H_second.sub({"T": B + lam * (U - B)}),
                        (1 - lam) * E_B + lam * E_U
                        + chord_coefficient * lam * (1 - lam) * (U - B)**2)
        for label, expression in (("breakpoint", E_B), ("endpoint", E_U), ("first slope", C_first),
                                  ("breakpoint nonnegative", B), ("interval length", U - B)):
            checks.nonnegative_coefficients(sign + " " + label, expression, variables)

    # The endpoint strictness facts used by the conventional equality proof are
    # checked from their literal supports. Plus endpoints vanish only at P=delta=0;
    # minus endpoints have a positive x^2 coefficient and vanish when x=0.
    for label in ("E_plus_B", "E_plus_U"):
        expression = polys[label]
        require(expression.terms.get((("P", 2),), 0) > 0 and
                expression.terms.get((("delta", 2),), 0) > 0,
                "Plus endpoint does not control both squares: " + label)
    for label in ("E_minus_B", "E_minus_U"):
        expression = polys[label]
        require(expression.terms.get((("x", 2),), 0) > 0,
                "Minus endpoint lacks positive x^2 term: " + label)
        checks.identity(label + " vanishes at x=0", expression.sub({"x": 0}), 0)

    zero_sub = {"delta": 0, "v": 0}
    zero_sub.update({"p" + str(i): 0 for i in range(1, 4)})
    zero_sub.update({"t" + str(i): 0 for i in range(1, 4)})
    checks.identity("zero denominator specialization", N.sub(zero_sub), 0)
    checks.identity("zero denominator Q specialization", Q.sub(zero_sub),
                    rational(cert["zero_denominator_Q_coefficient"]) * c * d)

    # The preceding different sharp bound has different directional strength.
    old_rhs = (src["P"] + src["T"])**2 / 72
    checks.identity("comparison on new sharpness family", (kappa * N - old_rhs).sub(equality_sub), y**2 / 8)
    a = V("old_a")
    old_family = {"c": 0, "delta": 0, "v": 0}
    old_family.update({"p" + str(i): a for i in range(1, 4)})
    old_family.update({"t" + str(i): a for i in range(1, 4)})
    checks.identity("prior sharpness family Q", Q.sub(old_family), old_rhs.sub(old_family))
    checks.identity("comparison on prior sharpness family", (old_rhs - kappa * N).sub(old_family), a**2 / 20)
    print("PASS symbolic certificate: " + str(checks.identities) + " exact polynomial identities")
    print("PASS nonnegative coefficient checks: " + str(checks.positive_checks) + "; endpoint strictness supports match")
    return kappa, src


def check_examples(path, kappa, src):
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data["schema_version"] == 1, "Unsupported examples schema")
    require(len({e["name"] for e in data["examples"]}) == len(data["examples"]), "Duplicate example name")
    count, equal_count, zero_count = 0, 0, 0
    for e in data["examples"]:
        name = e["name"]
        c, d, delta, v = (rational(e[k]) for k in ("c", "d", "delta", "v"))
        p, t = [rational(z) for z in e["p"]], [rational(z) for z in e["t"]]
        require(len(p) == 3 and len(t) == 3, "Example must have three pairs: " + name)
        P, T = sum(p), sum(t)
        z = (d - 3 * delta) / 2 - P
        w = z + v
        feasible = (c >= abs(delta) and P + T <= d and min(p + t + [v]) >= 0
                    and all(ti <= pi + delta and v <= pi + delta for pi, ti in zip(p, t)) and w >= 0)
        require(feasible, "INFEASIBLE EXAMPLE: " + name)
        # Direct rational evaluation, separately from the sparse-polynomial path.
        Q = (c * (d + delta) - delta * d + 2 * delta**2) / 4
        Q += sum((2 * pi - ti)**2 / 6 + delta * pi - c * (pi + ti) / 6 for pi, ti in zip(p, t))
        Q += v * z + v**2 / 2
        N = P**2 + T**2 + delta**2
        values = {"c": c, "d": d, "delta": delta, "v": v}
        values.update({"p" + str(i + 1): pi for i, pi in enumerate(p)})
        values.update({"t" + str(i + 1): ti for i, ti in enumerate(t)})
        require(Q == src["Q"].evaluate(values), "Example Q evaluation routes disagree: " + name)
        require(N == src["N"].evaluate(values), "Example N evaluation routes disagree: " + name)
        require(Q == rational(e["Q"]) and N == rational(e["N"]), "Example recorded Q or N mismatch: " + name)
        require(Q >= kappa * N, "Example violates claimed bound: " + name)
        equality = Q == kappa * N
        require(equality == e["equality"], "Example equality status mismatch: " + name)
        a = max(-z, Fraction(0))
        b = min(P / 3 + delta, (P - T + 3 * delta) / 2)
        require(0 <= a <= b and a <= v, "Scalar feasibility consequence failed: " + name)
        variance = sum(((2 * p[i] - t[i]) - (2 * p[j] - t[j]))**2
                       for i in range(3) for j in range(i + 1, 3)) / 18
        Phi = ((c * (d + delta) - delta * d + 2 * delta**2) / 4
               + (2 * P - T)**2 / 18 + delta * P - c * (P + T) / 6 - b**2 / 2)
        gap_parts = [variance, (v - a)**2 / 2, max(z, Fraction(0)) * v, (b**2 - a**2) / 2]
        require(min(gap_parts) >= 0 and Q - Phi == sum(gap_parts), "Scalar gap check failed: " + name)
        scalar_equal = all(2 * pi - ti == 2 * p[0] - t[0] for pi, ti in zip(p, t)) and v == a == b
        require((Q == Phi) == scalar_equal, "Scalar equality conditions failed: " + name)
        if N == 0:
            zero_count += 1
            require(e["ratio"] is None, "Zero denominator must have undefined ratio: " + name)
            require(delta == v == P == T == 0 and Q == c * d / 4, "Zero denominator example mismatch: " + name)
            require(equality == (c * d == 0), "Zero denominator equality mismatch: " + name)
        else:
            require(Q / N == rational(e["ratio"]), "Example ratio mismatch: " + name)
            classified = (delta < 0 and all(pi == -delta for pi in p) and T == 0 and
                          v == 0 and d == -3 * delta and c >= -delta)
            require(equality == classified, "Positive denominator classification mismatch: " + name)
            equal_count += int(equality)
        count += 1
    require(count > 0 and equal_count > 0 and zero_count > 0, "Missing essential examples")
    print("PASS exact examples: " + str(count) + "; positive-denominator equality=" + str(equal_count)
          + "; zero-denominator=" + str(zero_count))


def main():
    require(sys.version_info >= (3, 9), "Python 3.9 or newer required")
    require(sys.flags.optimize == 0, "Refusing optimized Python; replay with -I -B and without -O/-OO")
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=root / "certificate.json")
    parser.add_argument("--examples", type=Path, default=root / "examples.json")
    parser.add_argument("--source-pins", type=Path, default=root / "source-pins.json")
    args = parser.parse_args()
    check_sources(root, args.source_pins)
    certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
    kappa, source = check_symbolic(certificate, Checks())
    check_examples(args.examples, kappa, source)
    print("PASS all finite symbolic and rational certificate checks; kappa=" + str(kappa))
    print("Scope: conventional all-real-domain proof and equality reasoning are in the proof document.")
    print("This is not formal proof-assistant verification, realizability certification, or a finite-search proof.")


if __name__ == "__main__":
    try:
        main()
    except (CheckFailure, ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
