"""Independent bounded exact audit; standard library, no package imports or I/O."""
from itertools import product
from fractions import Fraction as F
from datetime import datetime, timezone


def q12(c, d, z, p, t, v):
    P, T = sum(p), sum(t)
    return (3*(c*(d+z)-z*d+2*z*z)
            + 2*sum((2*a-b)**2 for a, b in zip(p, t))
            + 12*z*P-2*c*(P+T)+6*v*(d-3*z-2*P)+6*v*v)


def classify_aux(c, d, z, p, t, v):
    if z == 0:
        A = F(d, 4)-F(sum(p)+sum(t), 6)
        return p == t and v == 0 and c*A == 0
    if z < 0:
        y = -z
        return p == (y,)*3 and t == (0,)*3 and v == 0 and d == 3*y
    return c == d == v == z and p == (0,)*3 and t == (F(z, 3),)*3


def classify_var(c, d, z, p, t, v, V):
    if V == 0:
        return p == t == (0,)*3 and z == v == 0 and c*d == 0
    return (c == z == v == 0 and p == t
            and sum(a > 0 for a in p) == 1 and d >= 2*sum(p))


print('UTC', datetime.now(timezone.utc).isoformat())
count = auxeq = vareq = positivevareq = 0
signs = {-1: 0, 0: 0, 1: 0}
for z in range(-3, 4):
    pairs = [(a, b) for a in range(5) for b in range(5) if b <= a+z]
    for xyz in product(pairs, repeat=3):
        p, t = tuple(x[0] for x in xyz), tuple(x[1] for x in xyz)
        P, T = sum(p), sum(t)
        for v in range(5):
            if any(v > a+z for a in p):
                continue
            dmin = max(P+T, 3*z+2*P-2*v)
            for d in (dmin, dmin+1, dmin+4):
                for c in (abs(z), abs(z)+1, abs(z)+4):
                    N = q12(c, d, z, p, t, v)
                    s = tuple(a+b for a, b in zip(p, t))
                    V = sum((s[i]-s[j])**2 for i in range(3) for j in range(i+1, 3))
                    ga = 2*N-sum(a*a for a in s)-3*z*z
                    gv = 4*N-V
                    assert ga >= 0, (c, d, z, p, t, v, ga)
                    assert gv >= 0, (c, d, z, p, t, v, gv)
                    assert (ga == 0) == classify_aux(c, d, z, p, t, v), (c, d, z, p, t, v, ga, 'aux classification')
                    assert (gv == 0) == classify_var(c, d, z, p, t, v, V), (c, d, z, p, t, v, gv, 'variance classification')
                    count += 1
                    auxeq += ga == 0
                    vareq += gv == 0
                    positivevareq += gv == 0 and V > 0
                    signs[(z > 0)-(z < 0)] += 1
print('GRID PASS', dict(feasible=count, by_delta_sign=signs,
                       aux_equalities=auxeq, variance_equalities=vareq,
                       positive_variance_equalities=positivevareq))

scalar_count = scalar_eq = 0
regions = {k: 0 for k in ['m=u', 'm=delta', 'm=v,u>=2v/3',
                          'm=v,u<=2v/3,u<=2delta/3',
                          'm=v,u<=2v/3,u>=2delta/3']}
for u, v in product((F(i, 6) for i in range(25)), repeat=2):
    z = F(1)
    m = max(z, u, v)
    H = (9*u*u+36*(m-v)*u-42*z*u+12*z*m+3*z*z
         + 12*v*v+12*v*max(3*u-2*v, 0))
    assert H >= 3*z*z
    assert (H == 3*z*z) == (u == F(2, 3) and v == z)
    scalar_count += 1
    scalar_eq += H == 3*z*z
    if m == u:
        form = 6*z*z+(u-z)*(33*u+3*z)+12*(u*u-v*v)
        assert H == form
        regions['m=u'] += 1
    if m == z:
        if u <= F(2, 3)*z:
            minimum = 3*z*z+6*(z+u)*(2*z-3*u)
            loss = (12*((F(3, 2)*u)**2-v*v) if v <= F(3, 2)*u
                    else 12*(v-F(3, 2)*u)**2)
        else:
            minimum = 3*z*z+3*u*(3*u-2*z)
            loss = 12*(z*z-v*v)
        assert H == minimum+loss and loss >= 0
        regions['m=delta'] += 1
    if m == v and u >= F(2, 3)*v:
        form = (3*z*z+16*v*(v-z)+(u-F(2, 3)*v)*(48*v-42*z)
                + 9*(u-F(2, 3)*v)**2)
        assert H == form
        regions['m=v,u>=2v/3'] += 1
    if m == v and u <= F(2, 3)*v and u <= F(2, 3)*z:
        form = (3*z*z+(F(2, 3)*z-u)*(36*z-9*u)
                + 36*z*(v-z)+12*(v-z)**2)
        assert H == form
        regions['m=v,u<=2v/3,u<=2delta/3'] += 1
    if m == v and u <= F(2, 3)*v and u >= F(2, 3)*z:
        form = (3*z*z+12*u*(3*u-2*z)+(12*z+36*u)*(v-F(3, 2)*u)
                + 12*(v-F(3, 2)*u)**2)
        assert H == form
        regions['m=v,u<=2v/3,u>=2delta/3'] += 1
print('SCALAR BOUNDARY PASS', dict(tuples=scalar_count, equalities=scalar_eq,
                                  regions=regions))


def evaluate(c, d, z, p, t, v):
    P, T = sum(p), sum(t)
    assert (c >= abs(z) and P+T <= d and v >= 0
            and all(a >= 0 and b >= 0 and b <= a+z and v <= a+z
                    for a, b in zip(p, t))
            and (d-3*z)/2-P+v >= 0)
    Q = ((c*(d+z)-z*d+2*z*z)/4
         + sum((2*a-b)**2/6+z*a-c*(a+b)/6 for a, b in zip(p, t))
         + v*((d-3*z)/2-P)+v*v/2)
    s = [a+b for a, b in zip(p, t)]
    V = sum((s[i]-s[j])**2 for i in range(3) for j in range(i+1, 3))
    return Q, V, Q-sum(a*a for a in s)/24-z*z/8


for a in (F(1, 1000003), F(1, 2), F(10**12)):
    for d in (2*a, 3*a, 1000000*a):
        Q, V, gap = evaluate(F(0), d, F(0), (a, F(0), F(0)),
                             (a, F(0), F(0)), F(0))
        assert Q == V/48 and gap == 0
for z in (F(1, 1000003), F(3, 2), F(10**12)):
    Q, V, gap = evaluate(z, z, z, (F(0),)*3, (z/3,)*3, z)
    assert Q == 5*z*z/36 and V == gap == 0
    y = z
    for c in (y, 2*y, 1000000*y):
        Q, V, gap = evaluate(c, 3*y, -y, (y,)*3, (F(0),)*3, F(0))
        assert Q == y*y/4 and V == gap == 0
for c, d in ((F(0), F(0)), (F(0), F(3, 2)), (F(3, 2), F(0))):
    Q, V, gap = evaluate(c, d, F(0), (F(0),)*3, (F(0),)*3, F(0))
    assert Q == V == gap == 0
print('RATIONAL EQUALITY/BOUNDARY PASS: 9 positive-variance extremizers, '
      '3 positive-delta auxiliary extremizers, 9 negative-delta auxiliary '
      'extremizers, 3 zero-profile boundaries')
