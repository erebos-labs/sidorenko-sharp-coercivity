"""Exact supporting checks for PROOF.md; Python 3.9+, standard library only.

Written by Alexander Richard Towell with substantial OpenAI Codex assistance.
No upstream checker is imported or executed. Polynomial identities of degree
at most two are checked on an exact unisolvent set, not random samples.
"""
from dataclasses import dataclass, replace
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json


ROOT = Path(__file__).resolve().parent
PAIRS = tuple(combinations(range(3), 2))


class VerificationError(ValueError):
    """A claimed exact obligation failed."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


@dataclass(frozen=True)
class Profile:
    c: F
    d: F
    delta: F
    v: F
    p: tuple
    t: tuple

    def __post_init__(self):
        require(len(self.p) == len(self.t) == 3, "three coordinates required")
        for value in (self.c, self.d, self.delta, self.v, *self.p, *self.t):
            require(type(value) in (int, F), "exact integer or Fraction required")
        for key in ("c", "d", "delta", "v"):
            object.__setattr__(self, key, F(getattr(self, key)))
        object.__setattr__(self, "p", tuple(map(F, self.p)))
        object.__setattr__(self, "t", tuple(map(F, self.t)))

    def integral(self):
        return all(x.denominator == 1 for x in
                   (self.c, self.d, self.delta, self.v, *self.p, *self.t))

    def feasible(self):
        z, p, t = self.delta, self.p, self.t
        return (self.c >= abs(z) and self.d >= sum(p) + sum(t)
                and min((*p, *t, self.v)) >= 0
                and all(t[i] <= p[i] + z and self.v <= p[i] + z for i in range(3))
                and (self.d - 3*z)/2 - sum(p) + self.v >= 0)

    def Q(self):
        c, d, z, v = self.c, self.d, self.delta, self.v
        return ((c*(d+z) - z*d + 2*z*z)/4
                + sum((2*p-t)**2/6 + z*p - c*(p+t)/6
                      for p, t in zip(self.p, self.t))
                + v*((d-3*z)/2 - sum(self.p)) + v*v/2)

    def V(self):
        s = [p+t for p, t in zip(self.p, self.t)]
        return sum((s[i]-s[j])**2 for i, j in PAIRS)

    def L(self):
        return self.delta/2 + (sum(self.p)-sum(self.t))/4 + self.v/2

    def W(self):
        return self.Q() - self.V()/48

    def R(self):
        return self.W() - self.L()

    def S(self):
        return (self.Q() - self.c/4 - self.delta/2
                - (2*sum(self.p)-sum(self.t))/6 - self.v/2)


def quadratic_identity(n, residual):
    """Prove zero for a known quadratic via 0, ±e_i, e_i+e_j.

The caller must establish degree <= 2 from its explicit formula. These
evaluations determine constant, linear, diagonal, and mixed coefficients.
"""
    zero = (F(0),) * n
    nodes = [zero]
    for i in range(n):
        for sign in (-1, 1):
            x = list(zero)
            x[i] = F(sign)
            nodes.append(tuple(x))
    for i, j in combinations(range(n), 2):
        x = list(zero)
        x[i] = x[j] = F(1)
        nodes.append(tuple(x))
    for x in nodes:
        require(residual(x) == 0, f"quadratic identity failed at {x}")
    return len(nodes)


def from_pq(p, q, z, v, e):
    t = tuple(a-b for a, b in zip(p, q))
    return Profile(z, sum(p)+sum(t)+e, z, v, tuple(p), t)


def reduced_J(z, u, v, m, e):
    return (9*u*u + 36*(m-v)*u - 42*z*u + 12*z*m + 3*z*z
            + 12*v*v + 12*v*e + 3*(2*m-z-u)**2)


def remainder48(c, d, z, v, p, t):
    """Direct integer numerator, separately checked against Profile.R."""
    P, T = sum(p), sum(t)
    s = [a+b for a,b in zip(p,t)]
    return (12*(c*(d+z)-z*d+2*z*z)
            + sum(8*(2*a-b)**2+48*z*a-8*c*(a+b) for a,b in zip(p,t))
            + 24*v*(d-3*z-2*P)+24*v*v
            - sum((s[i]-s[j])**2 for i,j in PAIRS)
            - 24*z-12*(P-T)-24*v)


def check_identities():
    counts = {}

    def verify(name, n, f):
        counts[name] = quadratic_identity(n, f)

    def full(x):
        return Profile(*x[:4], x[4:7], x[7:10])

    verify("slack_remainder", 10,
           lambda x: full(x).S()-full(x).V()/48
           + (3*x[0]+sum(x[4:]))/12-full(x).R())
    verify("integer_numerator", 10,
           lambda x: remainder48(*x[:4],x[4:7],x[7:10])-48*full(x).R())
    for sign in (-1, 1):
        verify(f"c_reduction_{sign}", 10,
               lambda x, sign=sign: full(x).Q()-replace(full(x), c=sign*x[2]).Q()
               -(x[0]-sign*x[2])*((x[1]+x[2])/4-sum(x[4:])/6))

    def zero_parts(x):
        p, q, v, e = x[:3], x[3:6], x[6], x[7]
        profile = from_pq(p, q, F(0), v, e)
        s = [2*a-b for a, b in zip(p, q)]
        B = (sum((p[i]-v)*q[i] for i in range(3))/2 + v*e/2
             + sum(s[i]*s[j] for i, j in PAIRS)/24)
        return profile, q, v, B

    def zero_identity(x):
        profile, q, v, B = zero_parts(x)
        return profile.R()+F(1, 2)-sum((a-1)**2 for a in q)/8-(v-F(1, 2))**2/2-B
    verify("delta_zero_square", 8, zero_identity)

    def negative_identity(x):
        y, v, e = x[:3]
        a, t = x[3:6], x[6:9]
        base = Profile(0, sum(a)+sum(t)+e, 0, v, a, t)
        shifted = replace(base, c=y, delta=-y, d=base.d+3*y,
                          p=tuple(y+b for b in a))
        return (shifted.R()-base.R()-(y-F(1, 2))**2/4+F(1, 16)
                -y*(2*sum(a)-sum(t))/3-y*e/2)
    verify("negative_translation", 9, negative_identity)

    def positive_expansion(x):
        p, q, z, v, e = x[:3], x[3:6], x[6], x[7], x[8]
        profile = from_pq(p, q, z, v, e)
        s = [2*a-b for a, b in zip(p, q)]
        rhs = (sum((12*q[i]+16*z)*p[i]+3*q[i]**2+(4*z-12*v)*q[i]
                   for i in range(3))
               + sum(s[i]*s[j] for i, j in PAIRS)
               + 12*v*v + 12*v*e + 18*z*z-36*z*v)
        return 24*profile.W()-rhs
    verify("positive_expansion", 9, positive_expansion)

    def p_reduction(x):
        r, q, a = x[:3], x[3:6], x[6:9]
        z, v, e = x[9:]
        s = [2*r[i]-q[i] for i in range(3)]
        p = tuple(r[i]+a[i] for i in range(3))
        gap = (sum((12*q[i]+16*z)*a[i] for i in range(3))
               + 2*sum(s[i]*a[j]+s[j]*a[i] for i, j in PAIRS)
               + 4*sum(a[i]*a[j] for i, j in PAIRS))
        return 24*(from_pq(p, q, z, v, e).W()-from_pq(r, q, z, v, e).W())-gap
    verify("p_reduction", 12, p_reduction)

    # Explicit choices of each positive-part branch make every expression
    # a genuine quadratic, so interpolation checks full identities.
    for branch in product((0, 1), repeat=4):
        def symmetry(x, branch=branch):
            q, b, z, v = x[:3], x[3], x[4], x[5]
            mean = sum(q)/3
            hi = [branch[i]*(q[i]-b) for i in range(3)]
            h = branch[3]*(mean-b)
            s = [2*b-q[i]+2*hi[i] for i in range(3)]
            s0 = 2*b-mean+2*h
            def f(qi, hh):
                return (3*qi*qi+(12*b+4*z-12*v)*qi+16*z*b
                        +12*hh*hh+(12*b+16*z)*hh)
            gap = (sum(f(q[i], hi[i]) for i in range(3))
                   +sum(s[i]*s[j] for i, j in PAIRS)-3*f(mean, h)-3*s0*s0)
            rhs = (F(5, 2)*sum((qi-mean)**2 for qi in q)
                   +sum((q[i]-q[j])**2-(s[i]-s[j])**2 for i, j in PAIRS)/6
                   +12*(sum(a*a for a in hi)-3*h*h)
                   +(12*b+16*z)*(sum(hi)-3*h)
                   +(sum(s)-3*s0)*(sum(s)+3*s0)/3)
            return gap-rhs
        verify("symmetry_"+''.join(map(str, branch)), 6, symmetry)

    for active in (0, 1):
        def f_identity(x, active=active):
            q, b, z, v = x
            h = active*(q-b)
            r = b+h
            return ((12*q+16*z)*r+3*q*q+(4*z-12*v)*q
                    -(3*q*q+(12*b+4*z-12*v)*q+16*z*b
                      +12*h*h+(12*b+16*z)*h))
        verify(f"hinge_expansion_{active}", 4, f_identity)

    def reduced(x):
        z, u, v, m, e = x
        p, t = (m-z,)*3, (m-u,)*3
        return 24*Profile(z, sum(p)+sum(t)+e, z, v, p, t).W()-reduced_J(z,u,v,m,e)
    verify("reduced_J", 5, reduced)
    verify("excess_reduction", 10,
           lambda x: full(x).W()-replace(full(x), d=x[1]+1).W()
           +(x[0]-x[2])/4+x[3]/2)

    def B(z, u, v, m, e):
        return 17*reduced_J(z,u,v,m,e)-6*(3*u-z+2*v)**2

    verify("maximum_u", 3, lambda x:
           B(*x, x[1], 3*x[1]-2*x[2])
           -(6*x[1]**2+(x[1]-x[0])*(456*x[1]-96*x[0])
             +(x[1]-x[2])*(300*x[1]+228*x[2]-24*x[0])))
    for active in (0, 1):
        verify(f"maximum_delta_reduction_{active}", 4, lambda x, active=active:
               B(x[0],x[1],x[2],x[0],active*(3*x[1]-2*x[2]))
               -B(x[3],x[1],x[2],x[3],active*(3*x[1]-2*x[2]))
               -(x[0]-x[3])*(300*(x[0]+x[3])-168*x[1]+24*x[2]))
    verify("maximum_v_high", 3, lambda x:
           B(*x, x[2], 3*x[1]-2*x[2])
           -(6*(5*x[1]-4*x[2])**2+(x[2]-x[0])*(576*x[1]-96*x[0]-120*x[2])))
    verify("maximum_v_low", 3, lambda x:
           B(x[0],F(2,3)*x[1]-x[2],x[1],x[1],F(0))
           -(F(8,3)*x[1]**2+168*x[1]*(x[1]-x[0])+96*(x[1]-x[0])**2
             +150*x[2]**2+76*x[1]*x[2]+576*x[0]*x[2]))
    verify("last_square", 1, lambda x:
           x[0]**2/68-x[0]/4+F(17,16)-(x[0]-F(17,2))**2/68)
    verify("integer_dispersion", 3, lambda x:
           sum((q-sum(x)/3)**2 for q in x)
           -sum((x[i]-x[j])**2 for i,j in PAIRS)/3)
    verify("equal_q_variance", 4, lambda x:
           sum(((2*x[i]-x[3])-(2*x[j]-x[3]))**2 for i,j in PAIRS)
           -4*sum((x[i]-x[j])**2 for i,j in PAIRS))
    verify("integer_sharp_ray", 1, lambda x:
           Profile(0,2*x[0],0,0,(x[0],0,0),(x[0],0,0)).S()
           -x[0]**2/6+x[0]/6)
    return {"identities": len(counts), "exact_evaluations": sum(counts.values()),
            "labels": list(counts)}


def downstream_from_data(data, face_constant=F(1), strict_bound=50):
    faces = [tuple(f) for f in data["template"]["faces"]]
    bits = data["template"]["bits"]
    require(len(faces) == len(set(faces)) == len(bits) == 22, "22 faces")
    require(all(len(set(f)) == 3 for f in faces), "face triples")
    pairs = sorted({e for f in faces for e in combinations(sorted(f), 2)})
    require(len(pairs) == 33, "33 pair coordinates")
    require(pairs == [tuple(e) for e in data["edge_order"]], "pair order")
    incident = [[j for j, f in enumerate(faces) if set(e) <= set(f)] for e in pairs]
    require(all(len(js) == 2 for js in incident), "each pair used twice")
    require(all(len(b) == 3 and set(b) <= {"0", "1"} for b in bits), "bit labels")
    anchors = [sum(bits[j][k] != bits[l][k] for k in range(3))-1
               for j, l in incident]
    require(anchors == data["three_rho"] and min(anchors) >= 0 and sum(anchors) == 6,
            "nonnegative anchors")
    n = len(pairs)
    # Reconstruct as a sum of rank-one edge energies, rather than reading A.
    A = [[0]*n for _ in range(n)]
    adjacency = [set() for _ in pairs]
    for f in faces:
        indices = [i for i, e in enumerate(pairs) if set(e) <= set(f)]
        for i, j in combinations(indices, 2):
            row = [int(k == i)-int(k == j) for k in range(n)]
            for a, b in product(range(n), repeat=2):
                A[a][b] += row[a]*row[b]
            adjacency[i].add(j)
            adjacency[j].add(i)
    seen, todo = {0}, [0]
    while todo:
        for v in adjacency[todo.pop()]-seen:
            seen.add(v)
            todo.append(v)
    require(len(seen) == n, "connected energy graph")
    for i, a in enumerate(anchors):
        A[i][i] += 4*a
    require(A == data["A"], "reconstructed matrix")
    N, tau = data["inverse_numerator"], data["inverse_denominator"]
    require(type(tau) is int and tau > 0, "positive denominator")
    require(len(N) == n and all(len(r) == n and all(type(v) is int for v in r)
                               for r in N), "integer inverse")
    require(all(N[i][j] == N[j][i] for i,j in product(range(n), repeat=2)),
            "symmetric inverse")
    require(all(sum(A[i][k]*N[k][j] for k in range(n)) == tau*int(i == j)
                for i,j in product(range(n), repeat=2)), "exact inverse")
    b = [2-a for a in anchors]
    u = [sum(x*y for x,y in zip(row,b)) for row in N]
    H = sum(x*y for x,y in zip(b,u))
    require(u == data["u"] and H == data["Hnum"], "linear certificate")
    gamma = len(faces)*face_constant
    psi = H+12*gamma*tau
    linear = [strict_bound*tau-2*x for x in u]
    squared = [linear[i]**2-4*psi*N[i][i] for i in range(n)]
    require(min(linear) > 0 and min(squared) > 0, "strict coordinate bound")
    failed49 = [i for i in range(n)
                if 49*tau-2*u[i] <= 0 or (49*tau-2*u[i])**2 <= 4*psi*N[i][i]]
    mode = 12*(strict_bound-1)
    # Source defect-one/DOWNSTREAM.md: even D, mode removal, transverse
    # D>=12, two residual savings >=1/6, and absorption at D>=304.
    requirement = max(F(mode), F(12), (1196+F(1,6))/2, 241+F(1,6), F(304))
    complete_D = 2*((requirement.numerator+2*requirement.denominator-1)
                    // (2*requirement.denominator))
    return {"coordinates": n, "inverse_entries_checked": n*n,
            "Gamma": str(gamma), "Psi": str(psi), "strict_bound": strict_bound,
            "integer_M_bound": strict_bound-1, "mode_removal_even_D": mode,
            "retained_complete_even_D": complete_D,
            "minimum_linear_margin": min(linear),
            "minimum_squared_margin": int(min(squared)),
            "failed_B49_coordinates": len(failed49),
            "failed_B49_pairs": [pairs[i] for i in failed49]}


def check_downstream(path):
    return downstream_from_data(json.loads(path.read_text()))


def check_sources(root=ROOT):
    pin = json.loads((root/"source-pins.json").read_text())
    for entry in pin["files"]:
        data = (root/entry["local_path"]).read_bytes()
        require(len(data) == entry["bytes"], "source length: "+entry["local_path"])
        require(hashlib.sha256(data).hexdigest() == entry["sha256"],
                "source SHA256: "+entry["local_path"])
        blob = b"blob "+str(len(data)).encode()+b"\0"+data
        require(hashlib.sha1(blob).hexdigest() == entry["git_blob_sha1"],
                "source Git blob: "+entry["local_path"])
    return len(pin["files"])


def check_grid():
    """Finite boundary grid only; the all-domain theorem is PROOF.md."""
    count, minimum, equality = 0, None, []
    for p in product(range(4), repeat=3):
        for t in product(range(4), repeat=3):
            P, T = sum(p), sum(t)
            q = [a-b for a,b in zip(p,t)]
            dispersion3 = sum((q[i]-q[j])**2 for i,j in PAIRS)
            for z in range(-3, 6):
                if any(t[i] > p[i]+z for i in range(3)):
                    continue
                for v in range(min(p)+z+1):
                    d0 = max(P+T, 3*z+2*P-2*v)
                    for dc, dd in product(range(2), repeat=2):
                        c, d = abs(z)+dc, d0+dd
                        numerator = remainder48(c,d,z,v,p,t)
                        require(numerator >= -48, "integer grid inequality")
                        if z > 0:
                            require(3*numerator >= -153+5*dispersion3,
                                    "retained dispersion inequality")
                        if not dispersion3:
                            require(numerator % 4 == 0, "equal-q integer lattice")
                        minimum = numerator if minimum is None else min(minimum,numerator)
                        if numerator == -48:
                            equality.append({"c":c,"d":d,"delta":z,"v":v,
                                             "p":list(p),"t":list(t)})
                        count += 1
    return {"domain": {"p_i_and_t_i":[0,3], "delta":[-3,5],
                       "v":"all integers 0..min_i(p_i+delta)",
                       "c":"abs(delta)+{0,1}",
                       "d":"max(P+T,3delta+2P-2v)+{0,1}",
                       "filter":"t_i<=p_i+delta for every i"},
            "seed": None, "stopping_rule":"exhaust this deterministic finite domain",
            "profiles":count, "minimum_R":str(F(minimum,48)),
            "boundary_equality_profiles":len(equality), "equality_examples":equality}


def check_controls():
    controls = []

    def rejects(name, action):
        try:
            action()
        except VerificationError:
            controls.append(name)
        else:
            raise VerificationError("negative control accepted: "+name)

    for name, f in [("constant term",lambda x:F(1)), ("linear term",lambda x:x[0]),
                    ("square term",lambda x:x[1]**2), ("mixed term",lambda x:x[0]*x[2])]:
        rejects(name, lambda f=f: quadratic_identity(3,f))
    sharp = Profile(2,2,2,2,(0,0,0),(0,0,0))
    rejects("constant 47/48",lambda: require(sharp.R() >= -F(47,48),"false constant"))
    real = Profile(*(F(5,2),)*4,(0,0,0),(F(1,2),)*3)
    require(real.feasible(), "real control feasible")
    rejects("integer bound on real domain",lambda: require(real.R() >= -1,"missing integrality"))
    rejects("individual v constraint",lambda: require(
        Profile(1,20,1,2,(0,0,5),(0,0,0)).feasible(),"individual v constraint"))
    data = json.loads((ROOT/"source/original.json").read_text())
    changed = deepcopy(data)
    changed["inverse_numerator"][0][0] += 1
    rejects("corrupted inverse",lambda: downstream_from_data(changed))
    rejects("unsupported B49",lambda: downstream_from_data(data,strict_bound=49))
    rejects("old constant at B50",lambda: downstream_from_data(data,face_constant=F(17,16)))
    return {"rejected_controls":len(controls),"labels":controls}


def main():
    result = {"evidence": "exact arithmetic supporting a written proof",
              "source_files_checked":check_sources(),
              "identities": check_identities(),
              "downstream": check_downstream(ROOT/"source/original.json"),
              "finite_boundary_grid":check_grid(), "negative_controls":check_controls()}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
