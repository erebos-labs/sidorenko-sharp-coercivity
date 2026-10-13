# Defect-one residual count on the unchanged original template

Version 1.0.0, 2026-10-13. Conventional proof with exact-arithmetic support.

## 1. Result, inheritance, and complete premises

The release baseline is `erebos-labs/sidorenko-sharp-coercivity` v1.3.0,
commit `8b350971095fda13884ea568d1914c1edd7fc966`. The exact published
`full-slack/THEOREM.md`, `full-slack/DOWNSTREAM.md`, and `full-slack/SOURCES.json`
are bundled under `sources/published/`. Their statements remain unchanged:

* the earlier sharp 1/40 and 1/48 quadratic theorems;
* the sharp full-slack constant 17/16;
* the original-template bound M <= 50 and integer mode removal at even D >= 600;
* the previously certified even D >= 1198 when using the unsplit robust residual count.

None of their optimizations or proofs is new work here. The robust count with
remainder 1196 remains a valid fallback. This handoff does not use the older
189 estimate or its proof.

The retained residual source is `artuskg/sidorenko-template-refinements` at
`06acd4cf46bfe9086f9abc7d85b5c9f171480143`, file
`experiments/original-effective-host/recovered/PROOF.md`, especially §§7.2-7.5.
Its exact source identity and access/redistribution limitations are in SOURCES.json.

Fix an odd prime q >= 3 and a nondegenerate alternating form on a 2D-dimensional
space over F_q, where D is a positive integer. The final application retains
D even and q >= 16D. The original template has 13 point vertices, 22 triangular
faces, and 33 point pairs. Its zero-excess pair set E_0 has 28 pairs and degree
vector

    (3,6,3,6,4,2,4,4,4,6,4,6,4).

The template is not varied. The certificate records the literal faces, bits,
all point pairs and zero-excess pairs, and six exposure orders. Its data is
compared against the pinned OpenAI `complex.tex`.

For a support F subset E_0 of size m, assign a two-dimensional space H_e to each
selected pair. Put

    K = sum_{e in F} H_e,             k = dim K,
    K_i = sum_{e in F, i in e} H_e,  k_i = dim K_i,
    a = sum_i k_i - 2k.

The global span K need not be isotropic. Only families whose K_i are isotropic
can occur inside the source's point Lagrangians; families with a nonisotropic
K_i have containment probability zero. We prove the count on the enlarged
set of all such locally isotropic plane families, not merely those with exact
point-pair intersections and zero face-common spaces. This is a counting
enlargement, not an assertion that all relaxed rank tuples are realizable.

Define

    theta_D(t) = product_{j=D-t+1}^D (q^j+1)^(-1),
    weight(H) = q^(2m) product_i theta_D(k_i).

The two quantities bounded below are sums of this weight over all nonempty
supports F and all locally isotropic plane families with the specified defect.
Denote them by N_1 and N_{>=2}.

**Theorem.** Uniformly in D and q on this domain,

    N_1     <= 2^118 q^(-D+241),
    N_{>=2} <= 2^63  q^(-2D+1196).

At D >= 600 their respective exponent savings are at least 359 and 4. Under
the unchanged source hypotheses, these estimates cover every actual geometric
nonsaving residual family, on every activity pattern. The immediate application
admits every even D >= 600, with q an odd prime satisfying q >= 16D, and preserves
the rank-layer envelope stated in DOWNSTREAM.md.

No sharpness, optimal dimension, priority, or formal-proof claim is made for
241, 2^118, or 600. The constants are deliberately sufficient, not optimized.

## 2. Why this is the correct weighted residual quantity

The inherited integer-profile classification gives c_j=0, every h_e in {0,2},
zero excess, and total selected gain sum_j g_j = 2m. This holds for every
nonempty gain domain and every activity pattern, at even D >= 600. Empty gain
domains contribute zero. The actual nonzero intersections H_e=L_i intersect L_j
are uniquely determined by a point configuration. Hence the gain weight on its
residual support is exactly q^(2m), not one and not an additional basis weight.

For a fixed deterministic family H, the event that all its prescribed spaces
are contained in the independent point Lagrangians has probability

    product_i theta_D(k_i).

The stricter event that these spaces are the actual intersections, with the
required zero unselected intersections and face-common dimensions, is contained
in this event. We drop those exactness conditions only for an upper bound.
Independence is used for the original point samples and these deterministic
containments; it is not asserted after conditioning on a residual profile.

Every actual residual configuration therefore has its contribution bounded by
the corresponding weighted sum. Summing enlarged families can count the same
configuration more than once, which only increases the upper bound. No extra
factor for local maximizing tuples is needed: the selected gains have already
been maximized in the retained planted estimate. Its prefactor A_D^22 stays
outside this weighted residual expectation, as in source equation (6.14).

Here are the elementary finite-field bounds needed in the count. Counting a
line together with a containing Lagrangian yields L_D=(q^D+1)L_{D-1}, L_0=1.
Reduction by a fixed isotropic t-space gives theta_D(t)=L_{D-t}/L_D, and thus

    theta_D(t) <= q^(-Dt + binom(t,2)).                         (1)

There is no extra constant in this upper bound. All k_i <= D automatically
for locally isotropic families. The normalized Gaussian coefficient satisfies

    {n choose t}_q <= 2 q^(t(n-t))                            (2)

because its numerator product is at most one and its denominator product is
at least 1-sum_{j>=1}q^(-j) >= 1/2. Finally

    G := |GL_2(q)| = (q^2-1)(q^2-q) >= q^4/2.                (3)

For q >= 3, the normalized left side is at least (1-1/3)(1-1/9)=16/27.
The empty containment product is one. Impossible dimension strata have zero
contribution; in particular k>2D is omitted from (4).

## 3. Actual-defect robust exponent and the entire higher-defect contribution

At a fixed support, global dimension k, and actual local dimensions k_i,
choose a prospective global k-space and then m two-spaces in it. Their number
is at most

    {2D choose k}_q {k choose 2}_q^m
       <= 2^(m+1) q^[k(2D-k)+2m(k-2)].                       (4)

Exact spanning and local isotropy may be discarded in this numerical upper
bound only after the weights on the actual stratum are bounded. Multiplying
(4) by (1) and q^(2m) gives the exponent

    k(2D-k)+2m(k-2)+2m-D sum_i k_i+sum_i binom(k_i,2)
      = -Da-k^2+2mk-2m+sum_i binom(k_i,2).                   (5)

This is the requested actual-defect identity. It retains the actual a, the
full gain q^(2m), and all local containment terms.

For every selected support of degrees d_i, k_i <= 2d_i. The fixed degree caps
therefore give

    sum_i binom(k_i,2) <= sum_i binom(2d_i,2) <= 468.         (6)

For a >= 2, at fixed support and k, every actual weight is uniformly bounded by

    q^[2m-D(2k+2)+468].

We apply this one bound before enlarging the number of families using (4).
We do NOT sum separate bounds over possible a or k_i; doing that would require
additional prefactors. The resulting exponent is at most

    -2D-k^2+2mk-2m+468
      = -2D+m^2-2m+468-(k-m)^2
      <= -2D+1196.                                         (7)

The last inequality follows from m <= 28 and the exact identity

    1196-(m^2-2m+468) = (28-m)(m+26) >= 0.

A nondirect family has 2 <= k <= 2m-1 <= 55. There are at most 2^28 supports,
55 values of k, and factor at most 2^29 in (4). Thus

    2^28 * 55 * 2^29 < 2^63,
    N_{>=2} <= 2^63 q^(-2D+1196).                            (8)

At D=600, the exponent is exactly -4. The unsplit inherited argument uses
a>=1 instead, and remains valid with 2^63 q^(-D+1196). It is not erased or
claimed false by the defect split.

For coverage, the source's strict span lemma says a>=1 for every nondirect
family on a simple pair graph. Its increment proof counts local growth at
least twice global growth and uses a minimal dependent subfamily for strictness.
Thus direct families (a=0), defect one, and defect at least two cover all
actual families. With m=0 there is no singular residual, and m=1 is always
direct, with k=2 and sum k_i=4.

## 4. Defect one: complete weighted basis patterns

Fix a support F and order its edges lexicographically. For every H_e, take
all ordered bases (x_{e,1},x_{e,2}), and concatenate them edge by edge. There
are n=2m vector positions. Before each position on e={i,j}, record

    W = span of all preceding vectors,
    U_i = span of preceding vectors on pairs incident with i,
    U_j = the analogous span at j,
    x = dim U_i,  y = dim U_j,  pi = dim(U_i intersect U_j).

For the vector at this position let g,l,r in {0,1} be the increases in the
global, i-local, and j-local dimensions. Since U_i,U_j subset W, g<=l,r.
The only possible types are

    111, 000, 001, 010, 011.

Their contributions l+r-2g to a are respectively

    0, 0, 1, 1, 2.

Summing local and global dimension increases proves exactly

    a = sum_positions (l+r-2g).                             (9)

Hence an a=1 list has exactly one position of type 001 or 010, no position of
type 011, and all other positions of type 111 or 000. Call the exceptional
position tau. No assertion that a=1 implies a single global linear relation
is used; type 000 remains allowed.

A complete type sequence determines every local prefix dimension x,y and the
terminal k_i, as well as k=sum g. Thus no extra partition by intersection
dimensions or rank tuples is necessary. With mu=min(x,y), uniform upper bounds
on the number of vector choices at any admissible prefix are:

| Type | Superset of admissible choices | Upper count |
|---|---|---|
| 111 | (U_i+U_j)^perp | q^(2D-x-y+mu) |
| 000 | U_i intersect U_j | q^mu |
| 001 | U_i | q^x |
| 010 | U_j | q^y |

For the first row, actual local isotropy forces orthogonality to both prefix
spaces. Nondegeneracy gives the exact dimension 2D-x-y+pi, and pi<=mu. In the
second row, membership in both prefixes is necessary. The last two rows use
membership in the endpoint where the local dimension does not increase.
Dropping the other orthogonality, rank, global-newness, or in-plane basis
conditions only increases these counts. The bound is applied at each valid
prefix of the actual list tree; no continuation from an invalid enlarged
prefix is needed. Multiplication along a fixed type sequence is therefore a
uniform upper bound on that sequence's list count.

### 4.1. The multiplicity identity, in the valid order

For the family set at this fixed support, the exact identity is

    sum_H weight(H)
      = G^(-m) sum_all_complete_patterns sigma
          sum_basis_lists_in_sigma weight(H(list)).         (10)

Every family contributes exactly G^m lists across the complete partition,
and its weight and defect are basis-invariant. Within a fixed type sequence
the terminal k_i are fixed, so the containment bound (1) applies uniformly.
Only AFTER (10) has summed all complete patterns do we use (3).

We do not claim an individual pattern contains all bases of any family.
Dividing a single-pattern list count and interpreting it as a bound for the
number of represented families would be wrong. Equation (10) is instead an
exact identity for the total weighted family sum.

### 4.2. Telescoping the containment weights

At an endpoint whose prefix dimension is x and whose increase is l in {0,1},

    binom(x+l,2)-binom(x,2) = lx.

Consequently the terminal containment correction is exactly

    sum_i binom(k_i,2) = sum_positions (lx+ry).              (11)

For type 111 the terms x+y cancel the -x-y in its list-count exponent. For
type 000 there is no increment correction. For the unique exceptional position,
the membership exponent at the unchanged endpoint and the increment correction
at the other endpoint sum to x_tau+y_tau. The ambient powers contribute 2Dk,
which with -D sum k_i gives -D because a=1. Finally the residual gain and full
basis division contribute 2m-4m=-2m.

It follows that each complete-pattern term on the right side of (10), after
using (3), is at most

    2^m q^(-D+R_sigma),
    R_sigma = -2m + sum_{t != tau} min(x_t,y_t)
                    +x_tau+y_tau.                          (12)

This is an upper exponent, not a claim that each list count is attained.
If actual pi_t were retained instead of mu_t at each valid prefix, the same
algebra would give pi_t in (12). We use mu_t so that the branching bound is
constant on the complete type sequence, with no missing dimension partition.

### 4.3. A degree-only bound, with no 189 input

At vertex i there are exactly 2d_i vector appearances. Before its j-th appearance,
its local dimension is at most j-1. Hence, over all vector positions,

    sum_t(x_t+y_t) <= sum_i binom(2d_i,2) <= 468.             (13)

At tau each endpoint has degree at most six, so at most eleven preceding vector
appearances. Thus

    x_tau+y_tau <= 22.                                      (14)

Using min(x,y)<=(x+y)/2 in (12),

    R_sigma <= -2m + [sum_t(x_t+y_t)+x_tau+y_tau]/2
             <= 245-2m <= 241.                              (15)

The last step uses m>=2; the a=1 domain is empty for m=0 or 1. This deliberately
loose remainder was derived here from 468, 22, and the preserved gain/basis term.
No older residual bound, support monotonicity theorem, or unproved multiplicity
premise is imported.

### 4.4. Full coefficient budget

For n=2m positions, choose tau in n ways, its one-sided orientation in two ways,
and each remaining type in {111,000}. There are at most

    n * 2 * 2^(n-1) = n 2^n
       <= 56 * 2^56 < 2^62                                  (16)

complete patterns. Some are infeasible; including them in the number bound is
harmless. The prefactor 2^m from (3) is at most 2^28. Summing at most 2^28
supports gives

    N_1 <= 2^28 * (56*2^56) * 2^28 q^(-D+241)
         < 2^118 q^(-D+241).                                (17)

There is no additional k, k_i, pi_t, activity-mask, or basis-pattern factor.
The type sequence already fixes the rank increments. The estimate is uniform
for each activity mask; we bound a superset of its admissible residual supports
rather than summing all activity masks in a single expectation.

## 5. Nonempty actual domain and the failed individual-pattern division

For every even D>=4 and odd prime q>=13, take a symplectic basis e_t,f_t and set

    L_1 = span(e_1,...,e_D),
    L_0 = span(e_1,e_2,f_3,...,f_D),
    L_7 = span(e_1,f_2,e_3,e_t+f_t for 4<=t<=D).

For the ten other points choose ten distinct lambda outside {0,1} and set

    L(lambda) = span(e_t+lambda f_t for 1<=t<=D).

All are Lagrangian. The only positive intersections on point-graph pairs are

    H_01=span(e_1,e_2),  H_17=span(e_1,e_3).

Indeed distinct slope spaces are transverse. A slope outside {0,1} is transverse
to each of the three special spaces, by comparison in each symplectic coordinate.
The remaining intersection L_0 intersect L_7=span(e_1) occurs on the nonedge 07.
No template face is {0,1,7}; all face-common dimensions are zero. Pairs 01 and 17
have zero excess. Thus this is an actual geometric residual profile, with

    m=2, k=3, (k_0,k_1,k_7)=(2,3,2), sum k_i=7, a=1.

The displayed formulas work at D=600 and every odd prime q>=16D. No theorem-sized
field or family is materialized; exact small controls are checked at (D,q)=(4,13)
and (4,67). The first control is only geometric; q=13 does not satisfy q>=16D.
The second satisfies the field inequality but not the final D>=600 requirement.
Neither small check substitutes for the general construction just proved.

Fix the order 01,17. Let B_line=(q-1)(q^2-q) be the number of ordered bases of H_17
whose first vector lies in the common line. Since

    B_line/G=1/(q+1),

the two complete types have counts G B_line and G(G-B_line), not G^2 each. Their
sum is G^2. With the common weight w=q^4 theta_D(2)^2 theta_D(3),

    [G B_line w + G(G-B_line)w]/G^2 = w.                     (18)

Using only the first pattern would instead give w/(q+1). This is exactly the
forbidden multiplicity error, retained as a negative control. At q=13,
G=26208 and B_line=1872. At q=3 the two-plane list partition has 576 and 1728
lists, summing to 2304; all 2304 lists are checked exactly. This q=3 partition
check does not assert the existence of the full thirteen-point slope example
at q=3.

The checker also includes a locally isotropic enlarged family on face 013:
planes span(e_1,e_2), span(e_1,e_3), span(e_1,e_4) assigned to its three pairs.
It has k=4, sum k_i=9, a=1 and a type-000 step. It has a common line on that
face and therefore is NOT a source c_j=0 residual family. It is a control that
the enlarged counting method allows type 000, not a claim of geometric residual
realizability from numerical rank data.

## 6. Verification and stopping boundary

The conventional argument proves the bounds over every support and every actual
geometric residual family by bounding a larger locally isotropic family set.
It is not inferred from numerical optimization or finite samples. The checker
verifies the actual-defect and per-type exponent identities, the exact template
and degree budget, coefficient arithmetic, geometric controls, and complete
weighted pattern partition. Mutation tests corrupt gains, type costs, defect
values, prefactors, and threshold metadata and require rejection.

The inherited sharp inequalities, M certificate, integer mode-removal proof,
and geometric/transverse interfaces are not re-proved or modified. The only
new estimates are (8) and (17), and the immediate coefficient/threshold
consequence in DOWNSTREAM.md. The task ends here. No template search, finite-host
reconstruction, external communication, publication, novelty determination,
optimal-dimension claim, independent human review, or Lean verification occurs.
