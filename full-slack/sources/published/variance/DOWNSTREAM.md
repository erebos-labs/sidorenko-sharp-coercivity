> Packaging note for 1.0.1: mathematical/historical text below is unchanged from 1.0.0. Source paths under global, effective-host, and review are external references, not bundled snapshots. See README.md and distribution.json. Historical replay commands require the temporary source overlay; use verify_package.py --source-cache DIR for this release. The historical API review inventory is omitted.

# Original 35-vertex template: variance energy and D = 3072

## Result and boundary

Apply the proved local real-domain theorem `Q >= V/48`, with precisely the
source's quadratic `Q` and `V = sum_{i<j}[(p_i+t_i)-(p_j+t_j)]^2`.
For the **original** 13-point, 22-face template, the unchanged global-energy
argument then gives

\[
\boxed{M\le256\quad\text{on every nonsaving integer profile}.}
\]

Consequently the original residue classification holds for every even

\[
\boxed{D\ge3072=12\cdot256.}
\]

This includes every activity pattern and every nonempty necessary integer
gain domain used in the pinned recovered proof. No simultaneous geometric
realizability of maximizing tuples is imposed. The local quadratic theorem
is on a real relaxation; the later mode-removal step **uses integrality**.
That distinction is indispensable.

| Quantity | Pinned global-energy baseline | This application |
|---|---:|---:|
| Local variance coefficient | 1/144 | 1/48 |
| Strict coordinate threshold B | 609 | 257 |
| Integer bound M <= B-1 | 608 | 256 |
| Sufficient even D = 12(B-1) | 7296 | 3072 |

The finite certificate and its conventional justification are complete.
Neither the integer M bound nor the sufficient D is claimed optimal.
No field, kernel, host, new template, or changed analytic counting input is
constructed here. Novelty is not certified by these correctness checks.

## 1. Pinned interfaces and the unchanged original template

The exact source pins are:

* `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, family 161
  `tail.tex` and `planted.tex`. The used labels are `eq:tail-feasible`,
  `eq:tail-quadratic`, `eq:tail-linear-loss`, `eq:tail-total-slack`,
  `lem:tail-lower-active`, and the selected planted gains.
* `artuskg/sidorenko-template-refinements@9922b05bf2c3418e1a46378d4ebac60e8a34ce51`,
  `global-residual-dimension.md` and `experiments/global-residual-energy/`.
  Sections 3–5 give the energy and integer-mode argument and original matrix.
* The same repository at `06acd4cf46bfe9086f9abc7d85b5c9f171480143`,
  `experiments/original-effective-host/recovered/PROOF.md`, Sections 3–7.
  The retained nondirect input is its robust **1196** remainder from Section
  7.4. Its Section 7.5 identifies the per-pattern full-basis-multiplicity
  obstruction in the older sharper sequential argument. This application
  does not rely on that argument or on the older number 189.

The 22 faces, in order, are

```text
(0,1,3)  (0,1,9)   (0,2,3)   (0,2,9)
(1,3,10) (1,7,10)  (1,7,12)  (1,9,12)
(2,3,4)  (2,4,9)   (3,4,11)  (3,10,11)
(4,8,9)  (4,8,11)  (5,6,7)   (5,6,11)
(5,7,10) (5,10,11) (6,7,12)  (6,8,11)
(6,8,12) (8,9,12).
```

Their corresponding bit strings are

```text
000 010 001 110 001 000 100 110 101 100 111
101 101 011 000 110 010 111 001 010 011 111.
```

There are 33 unordered point pairs, each occurring in two faces. These are
the coordinates of the energy matrix. They are distinct from the 66 edges
of the 35-vertex incidence graph. For a point pair e on faces j,k, put

\[
a_e=\operatorname{Hamming}(\mathrm{bits}_j,\mathrm{bits}_k)/3,
\qquad \rho_e=a_e-1/3.
\]

The only positive excesses are

\[
\rho_{02}=2/3,\qquad
\rho_{48}=\rho_{56}=\rho_{5,10}=\rho_{7,12}=1/3,
\qquad\sum_e\rho_e=2.
\]

The checker reads the pinned template data as data only, compares these
literal faces and bits, and rebuilds the pair table. It verifies the two
connected graphs, every vertex link, degree at most six, all three literal
Hamiltonian cuts, and all six 11-face fresh-point exposures. These checks
preserve the geometric cost interface and the transverse degree condition.
The chosen template is never varied.

## 2. Global profile and every activity case

Put b(t)=t(t+1)/2. For a profile let h_e be the shared pair dimensions,
c_j the face common dimensions, and s_{je}=h_e-c_j >= 0. Set

\[
\begin{aligned}
C_j&=(D+1)c_j+\sum_{e\subset j}b(h_e-c_j),\\
\mathcal C&=\tfrac12\left(\sum_j C_j-\sum_e(1-a_e)b(h_e)\right),\\
\beta_j&=C_j/2-\tfrac16\sum_{e\subset j}b(h_e),\\
S_j&=\beta_j-g_j,\qquad
\mathcal E=\tfrac12\sum_e\rho_e b(h_e).
\end{aligned}
\]

The exact identity, retaining the linear part of the excess, is

\[
\Delta:=\mathcal C-\sum_jg_j=\sum_jS_j+\mathcal E. \tag{1}
\]

A nonsaving profile means Delta <= 0. For a three-active face, g_j is the
unchanged maximum on the source's actual tuple union or the recovered
proof's stated necessary integer domain. An empty gain domain gives zero
face contribution and its profile is omitted. Each local maximizing tuple
can be selected independently while sharing the specified h_e values.

There are exactly eight activity subsets on a triangular face:

| Number active | Number of subsets | Selected gain and treatment |
|---:|---:|---|
| 0 | 1 | g=0; lower-activity argument below |
| 1 | 3 | g=0; the same argument |
| 2 | 3 | g=b(floor(h'/2)), where h' is the active endpoints' pair dimension |
| 3 | 1 | Exact S=Q-linear-loss and the new variance theorem |

For three active incidences retain exactly

\[
S=Q-\mathcal L,\qquad
\mathcal L=c/4+\delta/2+(2P-T)/6+v/2.
\]

The unchanged nonnegative loss envelope is the exact identity

\[
\frac{3c+P+T}{2}-\mathcal L
=\frac c4+(c-\delta)+\frac{2T}{3}
 +\frac{P/3+\delta-v}{2}\ge0. \tag{2}
\]

The source feasibility constraints imply every displayed sign. Since
h_i=c+p_i+t_i, their pair differences equal those of p_i+t_i. Applying the
proved local result before subtracting the full loss gives

\[
\boxed{S_j\ge\frac1{48}\sum_{e<e',\ e,e'\subset j}(h_e-h_{e'})^2
                 -\frac12\sum_{e\subset j}h_e.} \tag{3}
\]

For completeness, the source's lower-activity estimate is strong enough
for this *new* coefficient. Let h=max(h_0,h_1,h_2), and write the other two
dimensions as x,y in [0,h]. The original baseline calculation yields

\[
S_j\ge0,\qquad S_j\ge h^2/24-h/12. \tag{4}
\]

Here is the full activity-dependent justification of that input. Write
h=c+s_0 with s_0 maximal. Then

\[
\beta-\left[\frac{b(h)}3+\frac{b(c)}6+
                    \frac{b(s_1)+b(s_2)}3\right]
=\frac c6(3d-3s_0-s_1-s_2)\ge0.
\]

This uses d >= s_0+s_1+s_2. The gain is zero for zero or one active
incidence. With two, its actual pair satisfies h'<=h and hence its gain
is at most b(floor(h/2)). For integer h,

\[
\frac{b(h)}3-b(\lfloor h/2\rfloor)=
\begin{cases}
k(k-1)/6,&h=2k,\\
(k+1)(k+2)/6,&h=2k+1.
\end{cases}
\]

Both are nonnegative, and b(floor(h/2)) <= h(h+2)/8. This proves (4).
Equality S_j=0 requires c=0 and either all pair dimensions zero or one
pair dimension two and the others zero. The dimension-two alternative
requires exactly two active incidences at that pair's endpoints. Zero or
one active incidence permits only the all-zero alternative.

Write V_h=(h-x)^2+(h-y)^2+(x-y)^2. There are exact nonnegative identities

\[
2h^2-V_h=2[x(h-x)+y(h-y)+xy]\ge0,
\]

\[
\left(\frac{h^2}{24}-\frac h{12}\right)
-\left[\frac{V_h}{48}-\frac{h+x+y}{2}\right]
=\frac{2h^2-V_h}{48}+\frac{x+y}{2}+\frac{5h}{12}\ge0. \tag{5}
\]

Thus (3) holds for all eight local activity cases. This checks the precise
new coefficient rather than assuming the older lower-activity comparison
automatically transfers.

No general local nonnegativity claim has been made: the feasible fully
coincident specialization c=D,d=delta=p_i=t_i=v=0 gives S=-D/4. Its exact
symbolic identity is a control in the checker.

## 3. The fixed 33-coordinate matrix and exact rational bound

Let L_triangle be the Laplacian with one triangle on the three pair
coordinates of each face. Thus

\[
h^T L_\triangle h=
\sum_j\sum_{e<e',\ e,e'\subset j}(h_e-h_{e'})^2.
\]

Summing (3), each pair is counted twice. Keeping both terms of
E=(1/4)sum rho_e(h_e^2+h_e) gives

\[
\boxed{\Delta\ge h^TKh-\ell^Th,\qquad
K=\frac{L_\triangle}{48}+\frac{\operatorname{diag}(\rho)}4,
\qquad \ell_e=1-\rho_e/4.} \tag{6}
\]

K is positive definite: a vector in its zero set is constant by the
connected Laplacian, and the positive excess anchors then make that
constant zero. This is an exact structural argument, not a floating-point
eigenvalue check.

Put z=K^{-1}ell and H=ell^T K^{-1}ell. If Delta<=0, completing the square
and using Cauchy–Schwarz in the K inner product gives

\[
(h-z/2)^TK(h-z/2)\le H/4,\qquad
h_e\le\frac{z_e+\sqrt{H(K^{-1})_{ee}}}{2}. \tag{7}
\]

This enlarges the domain to the whole real ellipsoid. Neither its
coordinate extrema nor its arbitrary vectors are assumed to be feasible
profiles or realizable dimension data.

Order point pairs lexicographically. Put d_e=3rho_e and b_e=12-d_e.
The exact integer matrix is

\[
A=48K=L_\triangle+4\operatorname{diag}(d_e).
\]

The supplied symmetric integer matrix N and positive denominator tau in
`original_certificate.json` obey

\[
\boxed{AN=\tau I,\qquad\tau=270558215904.} \tag{8}
\]

The checker reconstructs A from the pinned literal template and checks
all 1,089 entries of (8). Let u=Nb and H_num=b^TNb. Then

\[
H_{\rm num}=3716263103433120,\qquad
z=4u/\tau,\qquad H=H_{\rm num}/(3\tau),
\]

so the coordinate bound in (7) is exactly

\[
\frac{2}{\tau}\left(u_e+\sqrt{H_{\rm num}N_{ee}}\right). \tag{9}
\]

For B=257, all 33 coordinates have strict integer certificates

\[
B\tau-2u_e>0,\qquad
(B\tau-2u_e)^2-4H_{\rm num}N_{ee}>0. \tag{10}
\]

The respective minimum margins are

```text
44766905118600
1933549752433619726193600.
```

The complete matrix and every coordinate margin, not just these minima,
are supplied. The JSON uses the equivalently scaled margins 24 times the
first margin and 576 times the second. All are computed and checked with
integers or rational numbers. Equations (9)–(10) give h_e<257 for every
real vector in the enlarged ellipsoid, and therefore M=max h_e<=256 for
the integer profiles.

The checker also replays the *original-template only* inverse and all 33
coordinate inequalities from the pinned old artifact. These certify the
comparison baseline M<=608 and D=7296; its separate residual-189 assertion
is not imported.

## 4. Unchanged integer mode removal at D >= 12M

To avoid confusion with the sharp variance coefficient, write
eta=(c-delta)/2=c-u for the source's nonnegative integer common-mode
parameter. Put n_i=2p_i-t_i and

\[
S_0=3c(c-1)/4+\frac16\sum_i[n_i^2+(c-1)n_i+3cp_i].
\]

The exact full-slack identity, including every linear term, is

\[
S=S_0+\frac\eta2[d-3c-2\delta+2-4P]
       +\frac v2[d-3\delta-2P+v-1]. \tag{11}
\]

Since P<=3(M-c), delta<=c, and d=D-c, the bracketed terms are at least

\[
D-12M+6c+2,\qquad D-6M+2c+v-1. \tag{12}
\]

Their exact differences from these lower bounds are
2(c-delta)+4[3(M-c)-P] and 3(c-delta)+2[3(M-c)-P]. They are nonnegative.
At D>=12M, the first bracket is strictly positive; the second is strictly
positive when v>0, since v is an integer and then M>=1. If M=0 these
variables are all zero.

The unchanged integer equality analysis of S_0 is:

* If c>=2, the identity
  S_0=(c-1)(5c+1)/8 + sum_i[n_i+(c-1)/2]^2/6 + cP/2
  proves strict positivity.
* If c=1, S_0=sum_i(n_i^2+3p_i)/6. Equality forces every p_i=t_i=0.
* If c=0, feasibility gives delta=0 and t_i<=p_i. Thus n_i>=p_i>=0
  are integers and S_0=sum_i n_i(n_i-1)/6>=0. Equality is exactly
  (p_i,t_i)=(0,0) or (1,1), independently for each i. Indeed n_i is
  then zero or one; the constraints 0<=t_i=2p_i-n_i<=p_i give those
  two pairs and no others.

For any nonsaving profile and even D>=3072, the matrix bound gives
D>=12M. Equations (11)–(12) and the lower-activity lemma now imply that
every local slack and E are nonnegative. Their sum Delta<=0 forces all
of them to vanish. Three-active faces therefore have eta=v=0 and c=0 or
one. A c=1 equality face has h_e=1 on its three pairs. Across such a pair,
the neighboring zero-slack face must again be a three-active c=1 face:
every other equality case has pair dimensions only zero or two.
Connected face adjacency propagates this to the whole template. But
then E=(1/2)sum_e rho_e=1, contradiction.

Consequently every nonsaving profile has

\[
\boxed{c_j=0,\quad h_e\in\{0,2\},\quad
\mathcal E=0,\quad S_j=0,\quad\Delta=0,\quad
\sum_jg_j=\tfrac23\sum_e b(h_e).} \tag{13}
\]

Every positive-excess pair has h_e=0. All lower-activity equality cases
were included above. The final gain identity follows from c_j=0 and
each pair's two appearances.

**Integrality control.** On all 22 faces set c=delta=v=0,
p_i=t_i=1/2, and h_e=1 globally. For even D>=12 these are real feasible
tuples, with S_j=-1/8, E=1, and Delta=-7/4. Thus (13) would be false
on the full real domain. The checker verifies these values symbolically;
the local real theorem and the subsequent integer classification are
separate statements.

## 5. Retained analytic inputs and thresholds

The coverage denominator three and selected integer gains are unchanged.
Thus 6C is integral and strict saving still means Delta>=1/6. This lattice
is unrelated to the denominator 48 of the quadratic comparison.

The 28 zero-excess pairs have degree caps
(3,6,3,6,4,2,4,4,4,6,4,6,4), giving sum_i binom(2degree_i,2)=468.
Retain the recovered proof's direct bound 2^56 q^-1 and its robust
nondirect bound 2^63 q^(-D+1196), with the same global-span count and
strict span defect. The number 1196 arises from

\[
-k^2+2mk-2m+468
=m^2-2m+468-(k-m)^2\le1196\quad(m\le28).
\]

It is not replaced by the older 189 claim. At D=3072 the nondirect
exponent saving is 1876, which is more than 1/6. The remaining unchanged
dimension requirement is even D>=12 for the transverse estimate. The
unchanged field condition is an odd prime q>=16D. Hence every even
D>=3072 clears every dimension threshold used in Sections 2–7 of the
recovered proof.

In particular its unchanged singular-tail expression is still valid:

\[
\mathfrak T_D\le
2^{87}(D+1)^{55}q^{-1/6}+2^{56}q^{-1}
 +2^{63}q^{-D+1196}.
\]

The same retained gain prefactor, transverse error and rank-layer envelope
can be used at these admitted dimensions. Their formulas are unchanged;
no finite-host parameter or constructed graph is recalculated in this task.

## 6. Replay, controls, and what the checks establish

From the package directory, using Python 3.9 or newer:

```sh
python3 -I -B check_downstream.py
python3 -I -B test_downstream_mutations.py
```

Optional deterministic regeneration of the one fixed matrix certificate:

```sh
python3 -I -B generate_original_certificate.py
```

The generator uses exact Gaussian elimination on the 33-by-33 rational
matrix. Its integer threshold calculation concerns that fixed ellipsoid
only; it varies no template and performs no dimension sweep of tuples.

The standalone checker verifies 19 polynomial identities, all eight local
activity masks, the literal template/cuts/exposures, 1,089 new inverse
product entries, all 33 new strict coordinate inequalities, and the same
1,089/33 old original-template baseline checks. The conventional argument
above establishes the signs, domain implications and equality classification.
The finite checker is not a proof assistant and does not re-prove the
retained geometric or transverse analytic inputs.

The executed mutation controls separately add one to a diagonal entry of
N and replace B=257 by one. They are rejected at the inverse matrix product
and strict coordinate inequality, respectively. Actual stdout, stderr and
execution receipts are in `logs/downstream*`. A clean replay from an
unrelated temporary working directory passed. No claim is based on random
sampling, floating-point optimization, a realized extremizer, or a hidden
change to the full slack.
