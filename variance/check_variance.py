#!/usr/bin/env python3
"""Exact arithmetic checker for the sharp relaxed variance theorem.

Python standard library only; no network, numerical optimization, external CAS,
or execution of retrieved source programs. Run python3 -I -B check_variance.py.
The conventional proof supplies the domain and equality reasoning; coefficient
identities and rational examples are checked exactly here.
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



# The sparse rational engine and source-expression transcription above are
# adapted from this session's completed sharp-1/40 verification package.
# This checker is standalone: it does not import that package or execute sources.

PINNED = {
    "sources/openai/tail.tex":
        ("openai/math", "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb", "dc11e07a592e70d3a13e3a005c72378c88edc351"),
    "sources/openai/planted.tex":
        ("openai/math", "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb", "e1a4636e66361dae0f5918e1245950060535a83c"),
    "sources/openai/complex.tex":
        ("openai/math", "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb", "178b0e9da21867a727ea847dae8e537b9d719a70"),
    "sources/prior/THEOREM.md":
        ("erebos-labs/sidorenko-sharp-coercivity", "0339f50a039001dc06bd12ffc664ab05a50253fb", "9682cbdf2ee58a819a45116e89c480f1b2f61edb"),
    "sources/global/global-residual-dimension.md":
        ("artuskg/sidorenko-template-refinements", "9922b05bf2c3418e1a46378d4ebac60e8a34ce51", "dcc39f4f593460cbad663ab168e1e68bf9c0146d"),
    "sources/effective-host/PROOF.md":
        ("artuskg/sidorenko-template-refinements", "06acd4cf46bfe9086f9abc7d85b5c9f171480143", "e5f1aaef9c3020054f0221a5b5dedc8260d5d5e4"),
}


def check_sources(root):
    pins = json.loads((root / "source-pins.json").read_text(encoding="utf-8"))
    require(pins["schema_version"] == 1, "Unsupported source manifest")
    by_path = {e["path"]: e for e in pins["files"]}
    require(len(by_path) == len(pins["files"]), "Duplicate source path")
    for path, binding in PINNED.items():
        require(path in by_path, "Missing primary source: " + path)
        ent = by_path[path]
        require(tuple(ent[k] for k in ("repository", "commit", "git_blob")) == binding,
                "Changed primary source binding: " + path)
    for path, ent in by_path.items():
        data = (root / path).read_bytes()
        require(len(data) == ent["bytes"], "Source byte length: " + path)
        require(hashlib.sha256(data).hexdigest() == ent["sha256"], "Source SHA-256: " + path)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == ent["git_blob"], "Git blob SHA-1: " + path)
    return len(by_path)


def check_symbolic(cert):
    checks = Checks()
    a = source_expressions()
    Q, S, L = a["Q"], a["S"], a["L"]
    p, t, P, T, c, d, delta, v = (a[k] for k in ("p", "t", "P", "T", "c", "d", "delta", "v"))
    s = [pi + ti for pi, ti in zip(p, t)]
    variance = sum((s[i] - s[j])**2 for i in range(3) for j in range(i + 1, 3))
    pair = sum(s[i] * s[j] for i in range(3) for j in range(i + 1, 3))
    norm = sum(si**2 for si in s)
    e, y = V("e"), V("y")
    A = (d + delta) / 4 - (P + T) / 6
    q = [pi - ti for pi, ti in zip(p, t)]
    R = 24 * Q - norm
    cr = {k: rational(x) for k, x in cert["zero_delta"].items()}
    cn = {k: rational(x) for k, x in cert["negative_shift"].items()}
    cp = {k: rational(x) for k, x in cert["positive_expansion"].items()}
    ch = {k: rational(x) for k, x in cert["positive_scalar"].items()}
    cl = {k: rational(x) for k, x in cert["linear_loss"].items()}
    kappa = rational(cert["kappa"])
    aux_s = rational(cert["auxiliary"]["sum_square"])
    aux_d = rational(cert["auxiliary"]["delta_square"])
    checks.identity("full slack is Q minus the specified linear loss", S,
                    Q - (cl["c"] * c + cl["delta"] * delta
                         + cl["P"] * P + cl["T"] * T + cl["v"] * v))
    checks.identity("source homogeneous quadratic part", S.homogeneous(2), Q)
    checks.identity("source planted common-space gain", a["gC_unsimplified"], a["gC"])
    checks.identity("source full slack from beta minus planted maximand", a["beta"] - a["g"], S)
    checks.identity("variance expansion", variance, 2 * norm - 2 * pair)
    checks.identity("PR4 denominator conversion", 2 * (P + T)**2 - variance, 6 * pair)
    checks.identity("auxiliary-to-variance gap with requested coefficient",
                    aux_s * norm + aux_d * delta**2 - kappa * variance,
                    pair / 24 + delta**2 / 8)
    checks.identity("coefficient of c", A, (d + 3 * delta) / 12 + (d - P - T) / 6)
    ca = V("ca")
    checks.identity("exact common-space reduction gap", Q - Q.sub({"c": ca}), (c - ca) * A)

    Qzero = Q.sub({"c": 0, "delta": 0, "d": P + T + e})
    Rzero = 24 * Qzero - norm
    rhszero = (cr["pq"] * sum((pi - v) * qi for pi, qi in zip(p, q))
               + cr["q2"] * sum(qi**2 for qi in q)
               + cr["v2"] * v**2 + cr["ve"] * v * e)
    checks.identity("zero-delta nonnegative certificate", Rzero, rhszero)
    checks.identity("restoring c at delta zero",
                    R.sub({"delta": 0, "d": P + T + e}), rhszero + cr["cA"] * c * A.sub({"delta": 0, "d": P + T + e}))

    aa = [V("a" + str(i)) for i in range(3)]
    X, dd = sum(aa), V("dd")
    rename = {"p" + str(i + 1): aa[i] for i in range(3)}
    Q0 = Q.sub({"c": 0, "delta": 0, "d": dd, **rename})
    negmap = {"c": y, "delta": -y, "d": dd + 3 * y,
              **{"p" + str(i + 1): aa[i] + y for i in range(3)}}
    Qnegative = Q.sub(negmap)
    nshift = cn["y2"] * y**2 + cn["mixed"] * y * (2 * X - T) + cn["ye"] * y * (dd - X - T)
    checks.identity("negative-delta exact quadratic shift", Qnegative, Q0 + nshift)
    checks.identity("negative-delta w preserved", a["w"].sub(negmap),
                    a["w"].sub({"delta": 0, "d": dd, **rename}))
    norm0 = sum((aa[i] + t[i])**2 for i in range(3))
    checks.identity("negative-delta auxiliary gap",
                    Qnegative - norm.sub(negmap) / 24 - y**2 / 8,
                    Q0 - norm0 / 24 + y * (7 * X - 5 * T) / 12 + y * (dd - X - T) / 2)

    Rpositive = R.sub({"c": delta, "d": P + T + e})
    expansion = sum((cp["p_q"] * qi + cp["p_delta"] * delta) * pi
                    + cp["q2"] * qi**2 + (cp["q_delta"] * delta + cp["q_v"] * v) * qi
                    for pi, qi in zip(p, q))
    expansion += cp["v2"] * v**2 + cp["ve"] * v * e + cp["delta2"] * delta**2 + cp["delta_v"] * delta * v
    checks.identity("positive-delta variable-level R", Rpositive, expansion)
    qbar = sum(q) / 3
    checks.identity("w imposes the e lower bound", 2 * a["w"].sub({"d": P + T + e}),
                    e - 3 * (qbar + delta) + 2 * v)
    x, b, h = map(V, ("x", "b", "h"))
    flow = (12 * x + 16 * delta) * b + 3 * x**2 + (4 * delta - 12 * v) * x
    fhigh = (12 * x + 16 * delta) * x + 3 * x**2 + (4 * delta - 12 * v) * x
    fconvex = (3 * x**2 + (12 * b + 4 * delta - 12 * v) * x + 16 * delta * b
               + 12 * h**2 + (12 * b + 16 * delta) * h)
    checks.identity("convex f lower branch", fconvex.sub({"h": 0}), flow)
    checks.identity("convex f upper branch", fconvex.sub({"h": x - b}), fhigh)
    hh, hb = [V("h" + str(i)) for i in range(3)], V("hb")
    jleft = sum(fconvex.sub({"x": q[i], "h": hh[i]}) for i in range(3)) - 3 * fconvex.sub({"x": qbar, "h": hb})
    jright = (3 * sum((qi - qbar)**2 for qi in q)
              + 12 * (sum(hi**2 for hi in hh) - 3 * hb**2)
              + (12 * b + 16 * delta) * (sum(hh) - 3 * hb))
    checks.identity("exact Jensen gap", jleft, jright)
    checks.identity("squared positive-part Jensen gap",
                    sum(hi**2 for hi in hh) - 3 * hb**2,
                    sum((hh[i] - hh[j])**2 for i in range(3) for j in range(i + 1, 3)) / 3
                    + (sum(hh) - 3 * hb) * (sum(hh) + 3 * hb) / 3)

    u, mm, em = map(V, ("u", "m", "em"))
    H = (ch["u2"] * u**2 + ch["mu"] * (mm - v) * u + ch["delta_u"] * delta * u
         + ch["delta_m"] * delta * mm + ch["delta2"] * delta**2
         + ch["v2"] * v**2 + ch["ve"] * v * em)
    uniform = {"c": delta, "d": 3 * (mm - delta) + 3 * (mm - u) + em,
               **{"p" + str(i + 1): mm - delta for i in range(3)},
               **{"t" + str(i + 1): mm - u for i in range(3)}}
    checks.identity("positive-delta scalar H after reductions", R.sub(uniform), H)
    Hu = H.sub({"m": u, "em": 3 * u - 2 * v})
    checks.identity("maximum u case", Hu,
                    6 * delta**2 + (u - delta) * (33 * u + 3 * delta) + 12 * (u**2 - v**2))

    Hd0 = H.sub({"m": delta, "em": 0})
    Hd1 = H.sub({"m": delta, "em": 3 * u - 2 * v})
    low = 3 * delta**2 + 6 * (delta + u) * (2 * delta - 3 * u)
    high = 3 * delta**2 + 3 * u * (3 * u - 2 * delta)
    checks.identity("maximum delta, low u, v above 3u/2", Hd0, low + 12 * (v - 3 * u / 2)**2)
    checks.identity("maximum delta, low u, v below 3u/2", Hd1, low + 12 * ((3 * u / 2)**2 - v**2))
    checks.identity("maximum delta, high u", Hd1, high + 12 * (delta**2 - v**2))

    Hv0 = H.sub({"m": v, "em": 0})
    Hv1 = H.sub({"m": v, "em": 3 * u - 2 * v})
    checks.identity("maximum v, active positive part", Hv1,
                    3 * delta**2 + 16 * v * (v - delta)
                    + (u - 2 * v / 3) * (48 * v - 42 * delta) + 9 * (u - 2 * v / 3)**2)
    checks.identity("maximum v, zero positive part, low u", Hv0,
                    3 * delta**2 + (2 * delta / 3 - u) * (36 * delta - 9 * u)
                    + 36 * delta * (v - delta) + 12 * (v - delta)**2)
    checks.identity("maximum v, zero positive part, high u", Hv0,
                    3 * delta**2 + 12 * u * (3 * u - 2 * delta)
                    + (12 * delta + 36 * u) * (v - 3 * u / 2) + 12 * (v - 3 * u / 2)**2)

    # Parameterized sharpness and auxiliary equality identities: these are
    # symbolic families, not inferences from a finite sample.
    aa1 = V("aa1")
    sharp = {"c": 0, "delta": 0, "v": 0, "p1": aa1, "t1": aa1,
             "p2": 0, "p3": 0, "t2": 0, "t3": 0}
    checks.identity("sharp family Q", Q.sub(sharp), aa1**2 / 6)
    checks.identity("sharp family V", variance.sub(sharp), 8 * aa1**2)
    checks.identity("sharp family denominator constant", Q.sub(sharp), kappa * variance.sub(sharp))
    checks.identity("sharp family w", a["w"].sub(sharp), d / 2 - aa1)
    eqpos = {"c": delta, "d": delta, "v": delta,
             **{"p" + str(i): 0 for i in range(1, 4)},
             **{"t" + str(i): delta / 3 for i in range(1, 4)}}
    checks.identity("positive-delta auxiliary equality Q", Q.sub(eqpos), 5 * delta**2 / 36)
    checks.identity("positive-delta auxiliary equality V", variance.sub(eqpos), 0)
    eqzero = {"delta": 0, "v": 0,
              **{"p" + str(i): 0 for i in range(1, 4)},
              **{"t" + str(i): 0 for i in range(1, 4)}}
    checks.identity("zero numerator residual cd/4", Q.sub(eqzero), c * d / 4)

    return checks.identities, a, variance


def feasible(vals):
    c, d, delta, v = (vals[k] for k in ("c", "d", "delta", "v"))
    p = [vals["p" + str(i)] for i in range(1, 4)]
    t = [vals["t" + str(i)] for i in range(1, 4)]
    P, T = sum(p), sum(t)
    return (c >= abs(delta) and P + T <= d and min(p + t + [v]) >= 0
            and all(ti <= pi + delta and v <= pi + delta for pi, ti in zip(p, t))
            and (d - 3 * delta) / 2 - P + v >= 0)


def variance_equality(vals):
    p = [vals["p" + str(i)] for i in range(1, 4)]
    t = [vals["t" + str(i)] for i in range(1, 4)]
    ss = [pi + ti for pi, ti in zip(p, t)]
    vv = sum((ss[i] - ss[j])**2 for i in range(3) for j in range(i + 1, 3))
    if vv > 0:
        return (vals["c"] == vals["delta"] == vals["v"] == 0
                and p == t and sum(pi > 0 for pi in p) == 1)
    return (not any(p + t) and vals["delta"] == vals["v"] == 0
            and vals["c"] * vals["d"] == 0)


def check_examples(root, kappa, a, variance):
    examples = json.loads((root / "examples.json").read_text(encoding="utf-8"))
    names, count, negatives, seen_positive, seen_zero = set(), 0, 0, False, False
    for ent in examples["examples"]:
        require(ent["name"] not in names, "Duplicate example name")
        names.add(ent["name"])
        vals = {k: rational(x) for k, x in ent["tuple"].items()}
        require(feasible(vals), "Example violates exact source domain: " + ent["name"])
        Qv, Vv, Sv = a["Q"].evaluate(vals), variance.evaluate(vals), a["S"].evaluate(vals)
        for key, actual in (("Q", Qv), ("V", Vv), ("S", Sv)):
            require(actual == rational(ent[key]), "Wrong exact " + key + ": " + ent["name"])
        require(Qv >= kappa * Vv, "Candidate constant fails: " + ent["name"])
        actual_eq = Qv == kappa * Vv
        require(actual_eq == ent["equality"], "Wrong equality flag: " + ent["name"])
        require(actual_eq == variance_equality(vals), "Equality classification: " + ent["name"])
        seen_positive |= Vv > 0 and actual_eq
        seen_zero |= Vv == 0 and actual_eq
        negatives += Sv < 0
        count += 1
    require(seen_positive and seen_zero and negatives, "Missing required example class")
    return count, negatives


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    cert_path = args.certificate or root / "local_certificate.json"
    try:
        cert = json.loads(cert_path.read_text(encoding="utf-8"))
        require(cert["schema_version"] == 1, "Unsupported local certificate")
        source_count = check_sources(root)
        identities, src, variance = check_symbolic(cert)
        count, negatives = check_examples(root, rational(cert["kappa"]), src, variance)
        result = {"status": "PASS", "arithmetic": "fractions.Fraction; exact sparse polynomial coefficients",
                  "kappa": cert["kappa"], "source_files": source_count,
                  "polynomial_identities": identities, "rational_examples": count,
                  "negative_local_slack_examples": negatives,
                  "scope": "Arithmetic certificate; the complete real-domain proof and equality reasoning are in THEOREM.md"}
        print(json.dumps(result, indent=2) if args.json else
              "PASS: %s source files; %s exact identities; %s rational examples; kappa=%s"
              % (source_count, identities, count, cert["kappa"]))
        return 0
    except (CheckFailure, KeyError, ValueError, OSError, TypeError) as err:
        print("FAIL: " + str(err), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

