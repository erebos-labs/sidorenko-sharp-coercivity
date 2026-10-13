# Conditional application to the unchanged original template

Handoff 1.0.0. New conclusion: M <= 50; mode removal at even D >= 600;
retaining the recovered 1196 residual bound, sufficient even D >= 1198.

## 1. Exactly what is inherited

The authoritative baseline is `variance/DOWNSTREAM.md` and
`variance/original_certificate.json` at published repository commit
`1b6abc821b7fb95cc0ca71ba804e0c4ae19df4e4`. Their statements M<=256 and
sufficient even D>=3072 remain valid and unchanged. Their source definitions,
actual or necessary-integer-domain gain choice, geometric cost argument,
integer mode-removal theorem, and recovered analytic inputs are retained.
No result about a different template or finite host is imported.

For clarity the required premises are explicit here.

* The original incidence template has 13 point vertices and 22 face vertices,
  hence 35 vertices and 66 incidence edges. Its 33 point pairs are the energy
  coordinates, not the 66 incidence edges. Each point pair belongs to two
  faces. The literal faces, bits, six exposure orders, and pair ordering are
  in both the inherited and new certificates, with no changes.
* D is an even integer; r=D/2. Pair dimensions h_e and common dimensions c_j
  are nonnegative integers, with h_e>=c_j on a face. Three-active tuples
  have integers u,p_i,t_i,v, d=D-c, r'=r-u, delta=2u-c, s_i=h_i-c=p_i+t_i,
  0<=u<=min(c,r), 0<=r'<=d, and every inequality (F) of THEOREM.md.
  The gain is the same maximum over the actual tuple union or the same
  enlarged necessary integer domain specified by the published source.
  No extra realizability restriction is imposed in taking this maximum.
* A face with empty gain domain has zero face factor and its profile is
  omitted. Maximizing tuples may be selected independently, sharing the
  prescribed h_e. Simultaneous geometric realizability is not needed for
  the algebraic bounds. Probability estimates are still applied only to
  actual configurations, as in the inherited argument.
* With two active incidences, the gain is b(floor(h'/2)) for the active
  endpoints' actual pair. With zero or one active incidence the gain is
  zero. Here b(x)=x(x+1)/2.
* The inherited geometric cost and gain bounds, exposure argument, strict
  span defect, direct-family count, and robust all-family nondirect count
  are retained. In particular the nondirect remainder is 1196, not 189.
  The retained transverse threshold is even D>=12 with point degree <=6;
  the retained field condition is an odd prime q>=16D. These are premises
  and interfaces, not newly re-proved analytic theorems of this handoff.

The integer conditions are not assumptions in the new local real theorem.
They are used here at exactly the source's integer mode-removal step and
lower-activity gain calculation.

## 2. Global definitions and every local activity case

Define, exactly as in the published source,

\[
 \begin{split}
 C_j&=(D+1)c_j+\sum_{e\subset j}b(h_e-c_j),\\
 \mathcal C&=\frac12[\sum_jC_j-\sum_e(1-a_e)b(h_e)],\\
 \beta_j&=C_j/2-\tfrac16\sum_{e\subset j}b(h_e),\\
 S_j&=\beta_j-g_j,\quad
 \mathcal E=\tfrac12\sum_e\rho_e b(h_e),\qquad \rho_e=a_e-1/3,\\
 \Delta&=\mathcal C-\sum_jg_j=\sum_jS_j+\mathcal E.
 \end{split}                                                    \tag{1}
\]

A nonsaving profile means Delta<=0, not that each local slack is
nonnegative. For the original bit labels, rho_(0,2)=2/3 and
rho_(4,8)=rho_(5,6)=rho_(5,10)=rho_(7,12)=1/3; all others vanish.
Their sum is two.

For a three-active face THEOREM.md gives, on its unchanged domain,

\[
 S_j\ge V_j/48-\frac1{12}\sum_{e\subset j}h_e-17/16,
 \qquad V_j=\sum_{e<e',\ e,e'\subset j}(h_e-h_{e'})^2.             \tag{2}
\]

This uses h_i=c+p_i+t_i and hence sum h_i=3c+P+T. No term of the
published full slack is dropped.

For lower activity, the inherited integer-profile lemma gives
S_j>=h^2/24-h/12 with h=max h_i. Write the other dimensions as x,y in [0,h]
and V_h=(h-x)^2+(h-y)^2+(x-y)^2. Then the exact identities

\[
 2h^2-V_h=2[x(h-x)+y(h-y)+xy]\ge0,
\]

\[
 \left(h^2/24-h/12\right)-
 \left[V_h/48-(h+x+y)/12\right]
 =(2h^2-V_h)/48+(x+y)/12\ge0                                \tag{3}
\]

show that the same bound holds with additive constant **zero**.
There is one empty activity subset, three singleton subsets, three
specified two-incidence subsets, and one full subset. Equations (2)-(3)
cover all eight, including each possible two-active endpoint pair.

The inherited lower-activity equality classification and integer mode
argument remain unchanged. Before the integer step, a three-active local
slack may be negative; the new equality tuple has S=-29/16.

## 3. The changed linear term and constant, but unchanged matrix

Let n_3 be the number of three-active faces, so 0<=n_3<=22. Summing
(2)-(3) counts each h_e twice, and **keeps the linear term of the excess**:

\[
 \mathcal E=\tfrac14\sum_e\rho_e(h_e^2+h_e).
\]

Therefore

\[
 \Delta\ge h^TKh-\ell^Th-n_3(17/16)
          \ge h^TKh-\ell^Th-\Gamma,                           \tag{4}
\]

where

\[
 K=L_\triangle/48+\operatorname{diag}(\rho)/4,
 \qquad \ell_e=1/6-\rho_e/4,\qquad
 \Gamma=22(17/16)=187/8.                                    \tag{5}
\]

The Laplacian L_triangle has one triangle on the three pair coordinates
of each face. K is identical to the published variance-energy matrix.
The old linear vector 1-rho/4 has changed to 1/6-rho/4, and an additive
constant has been paid. Ignoring that constant would give an invalid
comparison of ellipsoids.

The edge-coordinate graph is connected, and positive anchors with total
rho=2 remove its constant nullspace. Thus K is positive definite by an
exact structural argument. No floating-point eigenvalue assertion is used.

Put z=K^{-1}ell and H=ell^T K^{-1}ell. For Delta<=0, (4) implies

\[
 (h-z/2)^TK(h-z/2)\le H/4+\Gamma,
 \qquad h_e\le\frac{z_e+\sqrt{(H+4\Gamma)(K^{-1})_{ee}}}{2}.   \tag{6}
\]

This deliberately bounds the entire enlarged real ellipsoid. Its
coordinate extrema are not asserted to be feasible or realizable profiles.

## 4. Exact integer certificate

Use the published lexicographic pair order, and set

\[
 d_e=3\rho_e\in\{0,1,2\},\quad b_e=2-d_e=12\ell_e,\quad
 A=48K=L_\triangle+4\operatorname{diag}(d_e).
\]

The **unchanged published inverse numerator and denominator** are reused,
not fitted numerically. The full symmetric integer matrix N obeys

\[
 AN=\tau I,\qquad \tau=270558215904.                         \tag{7}
\]

The new exact matrix-vector calculations are

\[
 u=Nb,\quad H_{\rm num}=b^TNb=96183743778420,
 \quad z=4u/\tau,\quad H=H_{\rm num}/(3\tau),
\]

\[
 \Psi=H_{\rm num}+12\Gamma\tau=172075323339492.               \tag{8}
\]

The coordinate bound in (6) is exactly

\[
 h_e\le\frac2\tau[u_e+\sqrt{\Psi N_{ee}}].                   \tag{9}
\]

For B=51, the full certificate verifies for every coordinate

\[
 B\tau-2u_e>0,\qquad (B\tau-2u_e)^2-4\Psi N_{ee}>0.          \tag{10}
\]

The two minimum positive margins are respectively

```text
9783442206276
3009906417131501290431936
```

`certificates/original.json` contains A, N, tau, the literal template, b,
u, Hnum, Gamma, Psi, and all 33 pairs of margins. `checker.py` reconstructs
A from the pinned original faces/bits, checks all 1,089 entries of (7),
and checks (8)-(10) exactly. It also confirms N and tau are unchanged from
the published certificate and rechecks its old B=257 coordinate claims.

Equations (9)-(10) give h_e<51 for the entire real ellipsoid. Since the
profiles in this application are integer-valued,

\[
 \boxed{M:=\max_eh_e\le50.}                                \tag{11}
\]

No optimality of this M bound, constant Gamma, or the outer ellipsoid is
claimed. The local C is sharp; those global statements are different.

## 5. The integer step and the residual bottleneck

The unchanged published mode-removal theorem applies once D>=12M. Its
premises include integral c,u,p_i,t_i,v, delta=2u-c and the complete domain
above. To make the interface auditable, the retained identities are:

\[
 \begin{split}
 \eta&=(c-\delta)/2=c-u\in\mathbb Z_{\ge0},\quad n_i=2p_i-t_i,\\
 S_0&=3c(c-1)/4+\tfrac16\sum_i[n_i^2+(c-1)n_i+3cp_i],\\
 S&=S_0+\tfrac\eta2[d-3c-2\delta+2-4P]
             +\tfrac v2[d-3\delta-2P+v-1].
 \end{split}                                               \tag{12}
\]

The two brackets are bounded below by
D-12M+6c+2 and D-6M+2c+v-1, respectively. The source's integer
S_0 classification and connectedness/excess argument then give every
nonsaving profile

\[
 c_j=0,\quad h_e\in\{0,2\},\quad S_j=\mathcal E=\Delta=0,
 \qquad \sum_jg_j=\tfrac23\sum_e b(h_e).                     \tag{13}
\]

This is an inherited implication, applied at a newly certified bound on M,
not a new proof of the old mode-removal theorem. The identities are
regression checked. Now M<=50 admits this step at every even D>=600.

**600 is not the final retained analytic threshold.** The unchanged robust
nondirect bound is 2^63 q^(-D+1196). At D=600 it does not vanish. To retain
at least the old q^(-1/6) saving, require D-1196>=1/6 as well. Together with
even D>=12 and D>=600, this is satisfied by every even

\[
 \boxed{D\ge1198.}                                        \tag{14}
\]

At D=1198 the nondirect term saves q^-2. The field condition remains an
odd prime q>=16D (so q>=19168 at this dimension); no prime is instantiated.

The recovered direct and nondirect inputs remain exactly

\[
 \mathfrak T_D\le 2^{87}(D+1)^{55}q^{-1/6}
                   +2^{56}q^{-1}+2^{63}q^{-D+1196}.          \tag{15}
\]

The 28 zero-excess pair degree caps still give sum_i binom(2degree_i,2)=468,
and 28^2-2*28+468=1196. The constant is not replaced by the older 189.
Coverage denominators and selected integer gains are unchanged, so strict
profile saving still has the inherited lattice gap 1/6. The same geometric
gain prefactor, transverse estimate, and resulting rank-layer envelopes can
be used at admitted dimensions; none of their formulas is improved here.

| Certificate | M bound | Mode-removal threshold | Sufficient even D with retained analytics |
|---|---:|---:|---:|
| Published v1.2.0 | 256 | 3072 | 3072 |
| This handoff | 50 | 600 | 1198 |

The residual constant, not this mode-removal bound, is now the larger of
these two requirements. This is a strictly smaller sufficient rank-layer
parameter under the retained argument. It is not an optimal-dimension claim
or a recomputation of the recovered proof's complete finite-host theorem.

## 6. Checks and limitations

All eight local activity cases are accounted for by the two all-domain
arguments above, not by extrapolating a finite dimension sweep. The checker
also preserves the source's real-relaxation control: all h_e=1 with every
face c=delta=v=0 and p_i=t_i=1/2 has S_j=-1/8, E=1, Delta=-7/4. This
prevents applying (13) to real profiles. The earlier 1/40 theorem and sharp
variance theorem are not modified.

The conditional geometric/analytic inputs are not re-proved by matrix
multiplication or polynomial tests. There is no new template, finite field,
kernel, host, geometric realization of the local extremizer, optimal
ambient dimension, independent human review, or Lean theorem here. The
bounded task ends at (3) of THEOREM.md and the certified application (14).
