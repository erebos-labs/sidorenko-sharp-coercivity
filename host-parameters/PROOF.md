# Audit of the concrete host parameters at D = 600

Version 1.0.0. MIT License, copyright (c) 2026 Erebos Labs.

## 1. Outcome, scope and precise premises

**Outcome: valid specialization with explicit conditions.** The recovered
construction at D=7296 can be specialized to D=600, r=300, using the uniform
rank-layer interface of the pinned v1.4.0 release. The prime threshold must
also change; q>=9600 alone is not a complete-host condition.

The audit is pinned to `erebos-labs/sidorenko-sharp-coercivity` commit
`4844aba6a45ef725e2e15b25f9709640837b32c1` [R]. The retained concrete proof [H] is
`artuskg/sidorenko-template-refinements` commit
`06acd4cf46bfe9086f9abc7d85b5c9f171480143`,
`experiments/original-effective-host/recovered/PROOF.md`.
Its expected SHA256 is
`20c917f8fbab9cc51a92d0a4c853ca2080541a9a15c116bd3343150993aaf031`,
its length is 80,925 bytes, and its Git blob is
`e5f1aaef9c3020054f0221a5b5dedc8260d5d5e4`.
The source-access report distinguishes connector reading and metadata checks
from a whole-file local digest computation, which was not run.

The original graph H is the bipartite incidence graph on 13 point vertices
and 22 distinct face vertices, with the following faces:

```
(0,1,3) (0,1,9) (0,2,3) (0,2,9)
(1,3,10) (1,7,10) (1,7,12) (1,9,12)
(2,3,4) (2,4,9) (3,4,11) (3,10,11)
(4,8,9) (4,8,11) (5,6,7) (5,6,11)
(5,7,10) (5,10,11) (6,7,12) (6,8,11)
(6,8,12) (8,9,12)
```

Their bits are `000 010 001 110 001 000 100 110 101 100 111 101 101 011
000 110 010 111 001 010 011 111`, in the same order. There are 35 vertices,
66 source incidences and 33 auxiliary point pairs. The two vertex parts
are disjoint even when numeric labels coincide. For a simple host G on n
vertices, p(G)=2|E(G)|/n^2 and t(H,G)=hom(H,G)/n^35, counting **all** maps.

The inherited sharp 1/40 coercivity theorem, sharp variance theorem,
sharp full-slack theorem, M<=50, integer mode removal at even D>=600, and
the old unsplit residual-1196 fallback are preserved. The old D=7296
construction remains valid. No optimization of those results is new here.

The analytic premise used below is the following exact published interface:
for this H, every even D>=600, every odd prime q>=16D, every incidence
activity subset B and every sign assignment xi,

    |R_D(B,xi;q)-P(B,xi)| <= C_D q^(-1/6),
    C_D = 2^(32D+2048)(D+1)^256,                         (RL)
    P(B,xi) = product_{e: U_e subset B}(1+product_{kappa in U_e}xi_kappa),
    0 <= P(B,xi) <= 2^33.

Here U_e is the four source incidences at the two endpoints and two faces
of the point pair e. R_D uses the actual normalized signed rank-r kernels
of independent symmetric D-by-D matrices, r=D/2. The premise includes
both difference orientations. The release derives it from the retained
geometric/probability/transverse inputs of [H] §§1-7 and its new defect split.
This audit checks that interface and the specialization conditions; it does
not present the inherited geometric theorems as newly proved or formally
verified. Given (RL) and the fixed, checked template, §§3-8 below are a
conventional complete transfer to the host statement.

**Specialized conclusion.** Define

    Z = 3807386006623258,
    A0 = 53303404092753965,
    Lambda = 53303404092753966,
    J = 66 * 601^256 * 2^53303404092777429,
    Q0 = 9600 + J^6.

For every odd prime q>Q0, the same rational construction gives a symmetric
kernel U with 0<=U<=1 and

    mean(U) = q^(-2524200),
    mean(U)^66 - t(H,U) >= Delta_q,
    Delta_q = 2^(-Lambda) q^(-166597200).                 (T1)

For every integer n>=1322/Delta_q there is a nonempty simple host of order
n with deficit at least Delta_q/2. In particular, the bounded prime choice
in §8 gives a simple host of exactly N=2^B vertices, where

    B = 53281187287257529723615577,
    p(G)^66 - t(H,G) >= 1024/N > 0.                      (T2)

All large powers in this statement are symbolic. No prime satisfying Q0,
field, kernel table, host, or full enumeration is materialized. This is an
explicit sufficient order and deterministic selection specification, not a
practical construction, an optimal order, a novelty claim or a Lean theorem.

## 2. Dependency audit through the rank-layer interface

The exact gain at new D is defined by the same maximization, not by copying
old numerical maximizers. For a fully active face use integers

    d=D-c, r=D/2, 0<=u<=min(c,r), r'=r-u, 0<=r'<=d,
    delta=2u-c=d-2r', p_i,t_i>=0,
    p_i+t_i=h_i-c, P=sum p_i, T=sum t_i, P+T<=d,
    0<=t_i<=p_i+delta, 0<=v<=p_i+delta for every i,
    w=(d-3delta)/2-P+v>=0.

The selected gain is the q-independent maximum over this same necessary
integer domain of

    (r+c+1)u-2u^2 + sum b(p_i+t_i)
      -delta P-sum p_i^2-vw-sum b(t_i)+b(v),
    b(x)=x(x+1)/2.

An empty domain gives zero factor and is omitted. Maximizing tuples can
be chosen separately with shared h_e; no simultaneous geometric realization
is required. The actual probability arguments still concern actual
independent point configurations. With two active incidences the gain is
b(floor(h'/2)) at their actual pair, not at an arbitrary pair. With zero or
one it is zero. These cover all eight local masks and all global masks.
The prior real inequalities are not used to classify arbitrary real profiles:
the inherited mode-removal step requires the stated integrality and parity.

The recovered orbit lower bound is 2^(-D-15)q^(-C). Its numerator factors
have powers 2,1,9,17,3 of two, totaling 32. At most (D+1)^5 gain tuples give

    A_D=2^(D+47)(D+1)^5.

The correlated difference-form cost b(v) is retained, not replaced by
independence. The chart comparison uses 35 Lagrangian samples and at most
66 normalizers, costing 2^35*16^66=2^299. It is valid for a nonnegative,
possibly unbounded, singular integrand. The point samples are independent
before conditioning, and fresh-point exposure conditions on all earlier
samples. Six exposure classes do not require independence of those classes.
The complete dimensional profile count is (D+1)^55, and strict profile
saving has the unchanged 1/6 lattice gap.

The new defect split already includes the residual gain q^(2m), support
counts and complete basis-pattern counts. A_D^22 is applied only afterward.
Thus the weighted tail is bounded by

    2^87(D+1)^55 q^(-1/6) + 2^56 q^(-1)
      +2^118 q^(-D+241)+2^63 q^(-2D+1196).

At D>=600, the last exponent savings are at least 359 and 4. For q>=2,
2^118 q^(-D+241) <= 2^56 q^(-1) because its ratio is at most 2^(304-D).
Together with 2^57+2^63<2^64, this preserves

    T_D <=2^88(D+1)^55 q^(-1/6).

There is no new multiplicity for masks or rank strata: the estimate is
uniform for each mask, not a sum over masks. The robust unsplit estimate
2^63 q^(-D+1196) is still valid separately, but is not used at D=600.

The retained weighted interface is

    |R_D-P| <= 2^170 D q^(-1/2) + 2^299 A_D^22 T_D.

It follows that the second coefficient is exactly
2^(22D+1421)(D+1)^165, since 299+22*47+88=1421 and 22*5+55=165.
The ratio of C_D/2 to it is 2^(10D+626)(D+1)^91>=1. The first
coefficient is also at most C_D/2 using (D+1)^256>=D and
32D+1877>=0. Hence (RL) has the same envelope, not a hidden smaller error.

At D=600, r=300>1, D is even, and the point degree is at most six.
For the joint-sign estimate, n=D-1=599 and s<=6 give
s-b(n-s)<=6-b(593)<-9. The conditioning estimates q>=16D give
1-2D/q>=7/8 and 1-6D/q>=5/8. These satisfy the recovered transverse
conditions. At r=300 even, negation multiplies the rank-r determinant
character by chi((-1)^r)=1, so the signed layers are individually preserved.
The four-incidence parity products would also cancel a common sign change.
No congruence condition q=1 mod 4 is needed.

Thus D=600 is admitted for (RL) with
A_600=2^647*601^5 and C_600=2^21248*601^256. The geometric rank kernels
and gain maxima are redefined at these D,r; their old numerical values are
not reused. Everything else in the template and law remains fixed.

## 3. Activation, mean one and every type map

Let S_D be the finite additive group of symmetric D-by-D matrices. For
xi=+1,-1, let n_xi be the positive number of rank-r matrices with determinant
character xi and let p_xi=n_xi/q^b(D). A diagonal rank-r matrix realizes
each character, so these normalizers are nonzero. Define

    K_xi(Z)=1_{rank(Z)=r, sign(Z)=xi}/p_xi.

It is nonnegative and has mean one in either difference variable with
the other fixed. Normalizers and signed-layer counts are computed in
principle at the new D,r; their finite enumeration is not executed here.

Use one independent matrix coordinate for each of the 66 source corners.
At a type pair kappa=(v,j) with v in face j, let e,f be the two pairs in j
through v, and put M_kappa=U_e union U_f and Gamma_kappa=U_e symmetric-
difference U_f. The checked template gives U_e intersect U_f={kappa},
|M_kappa|=7, |Gamma_kappa|=6, and intersection_{kappa in U_g}M_kappa=U_g.
Fix theta=1/2 and just one negative sigma, at (0,0).

The unchanged activation law is: with probability 1/2 use M_kappa and
conditional sign probabilities 2^-7(1+sigma theta product_Gamma xi);
with probability 1/2 use Gamma_kappa and conditional probabilities
2^-6(1-sigma theta product_Gamma xi). A nonincidence uses the empty set.
Both sign laws are positive and normalized. At theta=1/2 their complete
branch probabilities have denominator dividing 512. Empty activity has
product one, not zero. Thus every fixed-type rectangular kernel has mean
one, regardless of the type prior.

For phi_alpha=1_{alpha subset S} product_alpha xi, the two branch Fourier
coefficients cancel every nonempty first moment. If Q=alpha union beta
and R=alpha symmetric-difference beta, the overlap moment equals

    (1/2)1_{Q subset M}(1_{R=empty}+sigma theta 1_{R=Gamma})
      +(1/2)1_{Q subset Gamma}(1_{R=empty}-sigma theta 1_{R=Gamma}).

In particular disjoint labels with nonempty union have zero moment.
The 33-coordinate adjacency graph is connected. In the product parity
expansion, a surviving labeling therefore has either every pair label empty,
contributing one, or all 33 labels nonempty. The complete all-nonempty
coefficient for a fixed type map f is bounded by

    |C(f)| <= M_C=2^2178,  2178=66*33.

For the identity type map, support intersection forces alpha_e subset U_e.
Each two adjacent nonempty labels must contain their singleton common
corner. Across the four corners this forces alpha_e=U_e. Its coefficient
is exactly (-1)*4^-66=-2^-132. These are fixed combinatorial statements,
not large-D limits.

Repeated type values do not identify matrix samples at distinct source
vertices. When a product of kernel expectations is expanded, every source
incidence draws a separate activation/sign sample even if it repeats a type
pair. Conditional on all types and activation draws, the matrix integrals
factor across the 66 coordinates and each is an instance of (RL). This
reasoning applies to every type map, including constant and collapsed maps;
it is not an injective or type-homomorphism assertion.

## 4. Rational pinning, dominance and dilution

The pinned four color-refinement rounds give within-part color counts
(3,1), (3,7), (13,7), (13,22). At round t, let h_t(v) be the histogram of
previous neighbor colors. The vertex score is -||h_t(v)||^2, and every
pair (i,j), including a nonincidence, has score
2h_t(i)(color(j))+2h_t(j)(color(i)). For a map f preserving the previous
colors, the directed-neighbor sum gives exactly

    F_t(id)-F_t(f)=sum_v ||h_t(f(v))-h_t(v)||^2.          (4.1)

No injectivity or edge-preservation is used: both sums are over source
vertices and directed source incidences. The new exact checker rebuilds
these scores and tests collapsed examples; the universal statement follows
from this completion of squares, not from those examples.

A round score for any part-preserving map lies in [-666,1188]:
666=13*6^2+22*3^2 and 1188=66*(2*6+2*3). Its spread is at most 1854.
Weight the rounds by 1856^(4-t). A nonidentity map first fails a color at
some round because the final colors are discrete within each part. The
first loss is at least one before weighting; all earlier rounds tie, and
later gains are bounded by 1854 times a geometric sum. For k=0,1,2,3,
1856^k-1854 sum_{j<k}1856^j>=1. Thus the weighted identity gap is at least
one over all 13^13*22^22 maps, with repetitions included.

Shift the weighted scores as in [H] to nonnegative integer vertex powers
a_i,b_j and pair powers ell_ij. The checker reconstructs their entire arrays:

    max a=127937502468, max b=20679552,
    max ell=25601296520, E(id)=115295183886,
    B_pin=13 max a+22 max b-E(id)=1548347298342.

Let T=2^2459, Z_I=sum_i T^a_i, Z_J=sum_j T^b_j. Use priors
pi_i=T^a_i/Z_I, nu_j=T^b_j/Z_J, and lambda_ij=T^(-ell_ij). All are
rational, normalized where appropriate, and nonnegative; 0<lambda<=1.
Thinning keeps the WHOLE base law with probability lambda and otherwise
uses the empty set. Thus the kernel mixes with the constant one kernel,
not zero, and retains its mean. Its overlap moment becomes
lambda A(alpha,beta)+(1-lambda)1_{alpha=beta=empty}.
An all-nonempty term acquires exactly one lambda per source incidence,
including every occurrence of a repeated type pair.

For every part-preserving f its weight is exactly

    w_f = T^E(f)/(Z_I^13 Z_J^22),
    E(f)=sum_{i in I}a_{f(i)}+sum_{j in J}b_{f(j)}
                           -sum_{(i,j) in C}ell_{f(i),f(j)}.

The shifts change every score by the same constant, so w_f<=w_id/T for
nonidentity maps. The all-map count is less than 2^147. Since
2459=147+2178+132+2, the competition has absolute coefficient less than
2^-134 w_id. Together with C(id)=-2^-132,

    t0 <= -(3/4)2^-132 w_id.

The bound Z_I^13 Z_J^22 <=13^13*22^22*T^(13maxa+22maxb) gives
w_id>2^[-147-2459 B_pin]. Therefore t0<=-m0 with

    Z=280+2459 B_pin=3807386006623258,
    m0=2^-Z,  280=132+147+1.

No sign assertion is made for the reverse coefficient t1. It is an average
under normalized independent priors, so |t1|<=M_C without another map count.

Add inactive type * on the I-type side, with mass 1-epsilon, and multiply
all old I priors by epsilon. All its pairs have empty activity. Keep

    epsilon=2^[-(Z+2181)],   2181=2178+3,
    alpha=m0 epsilon^13=2^-A0,
    A0=14Z+13*2181=53303404092753965,
    Gamma=alpha/2=2^-Lambda, Lambda=53303404092753966.

Every all-nonempty term needs all vertices sampled from the diluted side
to be active. There are 13 in the intended and 22 in the reverse orientation.
Consequently

    a_infty=1+epsilon^13 t0, b_infty=1+epsilon^22 t1.

These are nonnegative because they are averages of products of the
nonnegative parity model. Using epsilon^9 M_C<=epsilon M_C=m0/8 gives
0<=a_infty<=1-alpha and 0<=b_infty<=1+alpha/8. Their product is at most
1-7alpha/8. None of these constants or priors depends on D or q. All laws
are fixed before choosing the prime.

## 5. Complete field and kernel error budget

Let eta_q=C_D/floor(q^(1/6)). This is at least the rank-layer error because
floor(q^(1/6))<=q^(1/6). When eta_q<=1, the model bound 2^33 and nonnegative
rank moments give a common bound 2^34. Telescoping the product of 66
coordinate moments costs

    H_c eta_q,  H_c=66*(2^34)^65=66*2^2210.

This bound is uniform BEFORE averaging types or activity/sign samples,
so taking their probability average introduces no cardinality multiplier.
It holds in both orientations. At D=600 the even rank 300 also preserves
every signed layer under reversal, as checked in §2.

Define

    J=64 H_c C_600/alpha
      =66*601^256*2^53303404092777429,
    Q0=16*600+J^6=9600+J^6.                             (5.1)

These are positive integers given by finite expressions. For every odd
prime q>Q0, floor(q^(1/6))>=J, so H_c eta_q<=alpha/64 and eta_q<=1.
Write e=alpha/64. The finite orientation errors are each at most e. Since
a_infty<=1, b_infty<=2 and 0<=e<=1, the product perturbation is at most
3e+e^2<=4e=alpha/16. Therefore

    a_q b_q <=1-13alpha/16 <=1-3alpha/4 <=1-Gamma.       (5.2)

Every gain prefactor, coordinate multiplicity and dilution loss has been
paid. The number 9600 is only the antecedent rank-layer lower bound; it is
not sufficient for this construction's complete negative margin.

## 6. Exact symmetric kernel, rational cloning and edge coins

Let W be the resulting rectangular kernel on X times Y, with X the
14-type (including *) side and Y the 22-type side, both carrying66 independent
symmetric-matrix coordinates. Its conditional type means, hence its global
mean, are one. On Omega=X times Y put

    V((x,y),(x',y'))=W(x,y')W(x',y).

It is symmetric and nonnegative. The two argument pairs are independent
under the product measure, so E V=1. In the H-density product the variables
used by the two orientations are disjoint components of independent Omega
samples, hence t(H,V)=a_q b_q exactly. Repeated types do not change this
factorization.

At a fixed prime, both signed rank layers are nonempty, giving p_xi>=q^-b(D)
and K_xi<=q^b(D). Every activation uses at most seven coordinates, and both
thinnings are convex mixtures with one. Thus

    0<=W<=q^(7b(D)), 0<=V<=q^(14b(D)).

Define L=q^(14b(D)) and U=V/L. Then U is a rational finite symmetric kernel
in [0,1], mean(U)=q^(-14b(D)), and (5.2) yields

    mean(U)^66-t(H,U)>=Gamma q^(-924b(D)).              (6.1)

For D=600, b(D)=180300, 14b(D)=2524200, 924b(D)=166597200, proving (T1).
The diagonal values are retained: U is not yet a simple loopless graph.

There are exactly 308 q^(132b(D)) atoms if the unused matrices of the inactive
type are retained. A common denominator of their probabilities is

    M_clone=2^(Z+2181) Z_I Z_J q^(132b(D)).             (6.2)

For a fixed matrix tuple and old types(i,j), its multiplicity after multiplying
by M_clone is T^(a_i+b_j). For (*,j), it is
(2^(Z+2181)-1) Z_I T^b_j. These positive integers sum to M_clone over the
q^(132b(D)) matrix-tuple pairs. Cloning each atom by that multiplicity makes
the vertex measure uniform EXACTLY. Independent clone samples push forward
to the original product measure for every source map, including coincident
atoms. No discretization error or removal of kernel diagonals occurs here.

Let n_+,n_- be the new positive signed-layer integer counts. With ell_max
as above, common denominators are

    D_W=512 T^ell_max (n_+ n_-)^7,
    D_coin=D_W^2 q^(14b(D)).                           (6.3)

The branch denominator divides512, thinning denominators divideT^ell_max,
and each product uses at most seven signed-layer masses. Hence D_coin U
is an integer in [0,D_coin]. n_+,n_- can be computed by a bounded enumeration
of q^b(D) symmetric matrices, or by the exact Gaussian/form-count formula.
Such enumeration was not run. The counts at D=7296 are not substituted.

Equations (6.2)-(6.3) give exact integer-label and integer-coin spaces. Their
sizes may be enormous but finite. Explicit upper exponent bounds after the
prime choice are tabulated below, with every power kept factorized.

## 7. Simple sampling, every collision and deterministic selection

For a rational kernel in [0,1] with mean mu and density tau<=mu^66-Delta_q,
sample n clone labels independently. For each unordered pair of DISTINCT
host indices, draw one independent edge coin with probability U at those
labels; draw no loops. Distinct host indices can have identical labels, in
which case the actual kernel diagonal is used. Distinct host pairs still
receive separate coins. When a source map repeats an image edge, however,
its homomorphism indicator uses that ONE host edge, not another independent
coin or a squared edge probability.

Then E p(G)=(1-1/n)mu. For each injective map of 35 source vertices into host
indices, the 66 source edges use distinct host pairs, and the expected indicator
is exactlytau. The fraction of all n^35 maps identifying at least one vertex
pair is at most binom(35,2)/n=595/n. Each of their indicators lies in [0,1],
including a collision across an edge, whose value is zero. Thus

    E t(H,G)<=tau+595/n.

Jensen for x^66 and (1-1/n)^66>=1-66/n give

    E[p(G)^66-t(H,G)] >=Delta_q-661/n.                 (7.1)

The 66/n part pays missing host loops in the edge-density moment; the 595/n
part pays EVERY noninjective source map, including repeated image edges.
Cloning itself has zero error. Consequently n>=1322/Delta_q guarantees a
host with deficit at least Delta_q/2, and it is nonempty since edgeless hosts
have deficit zero. This is an expectation over a specified finite rational
label-and-coin space, not an asymptotic sampling assumption.

The exact count used for a deterministic acceptance test is

    hom(H,G)=sum_{(z_i) in V(G)^13}
                   product_{j in J} |intersection_{i in face j} N_G(z_i)|.

Point labels repeat freely. Given them, each of the 22 face vertices can be
chosen independently from its common-neighbor set, with repetitions allowed
between face vertices too. This proves the all-map formula. Source types,
clone labels and host indices are three different levels; no injectivity
constraint is introduced at any level by this formula.

For the fixed order N below, enumerate labeled simple graphs in binary
upper-triangle order and select the first satisfying

    (2|E(G)|)^66-hom(H,G) N^97 >=1024 N^131.            (7.2)

It is exactly the desired normalized deficit after multiplication by N^132.
The existence proof guarantees termination within 2^binom(N,2) tests, with at
most N^13 point assignments and 22 common-neighbor cardinalities per assignment.
This is a mathematical finite algorithm over finite binary strings. The
checker tests tiny instances and exponent identities, not that enormous
algorithm. No machine allocation or practical time claim is made.

## 8. Prime existence, fixed host order and comparison

For completeness the elementary large-input prime lemma used by [H] is valid:
for every integer n>=2^16 there is a prime strictly between n and 2n.
Let P(x) be the product of primes at most x. Strong induction proves
P(m)<=4^m: even m>=4 is composite, and for m=2k+1 the primes in(k+1,2k+1]
divide binom(2k+1,k), giving P(2k+1)<=4^(k+1)2^(2k)=4^(2k+1).
The small starting cases hold directly; realx follows by taking floor(x).
If no prime lay in(n,2n), prime-power valuations of binom(2n,n) would give

    4^n/(2n+1) <=binom(2n,n) <=(2n)^sqrt(2n)4^(2n/3).

Indeed a prime at most sqrt(2n) contributes a power at most 2n, a larger prime
contributes at most once, and primes in (2n/3,n] contribute zero. Therefore
2n/3<=log_2(2n+1)+sqrt(2n)log_2(2n). For 2^k<=n<2^(k+1), k>=16,
induction gives k+2<=2^(k/2-2) and k+3<=2^(k-3). The first induction step
uses (k+3)/(k+2)<=19/18<sqrt(2); the second is immediate. Thus the right
side is at most n/8+3n/8=n/2, using sqrt(2)<3/2, a contradiction.
The endpoint 2n is composite, so the interval is strict.

Q0 in (5.1) is an integer above 2^16. Define q mathematically as the least
prime in (Q0,2Q0). The lemma proves existence and a finite trial-division
search specification, with fewer than Q0 candidates and at most2Q0^2 candidate
divisors. It is odd and exceeds all field requirements. **No such prime was
tested or numerically named.**

Let h_D be an integer with D+1<2^h_D. With 66<2^7,

    J<2^F_J, F_J=A0+6+2210+(32D+2048)+7+256h_D.

Since16D<J^6, q<2Q0<4J^6<2^F_q where F_q=6F_J+2. Use h_600=10 and
h_7296=13. This gives

    F_J(600)=53303404092779996,
    F_q(600)=319820424556679978.

Set S_exp=924b(D) and B=11+Lambda+S_exp F_q. For D=600 this is precisely
B=53281187287257529723615577. With N=2^B, (6.1) and the strictprimeupperbound
imply Delta_q>2^(-Lambda-S_exp F_q)=2048/N. Equation (7.1) therefore gives
E[deficit]>1387/N>1024/N. This proves (T2) and termination of (7.2).

The independently recomputed old parameters agree with every corresponding
literal in[H], including its old B=7866423844799423288734694969. The newB
is strictly smaller. These are exponents of host orders, not host vertex
counts to materialize. This comparison is a smaller certified sufficient
complete-host order under the retained analytic inputs, not merely a smaller
ambient dimension and not an optimal order.

For the source-specific finite label-and-coin selection, using q<2^F_q and
n_+,n_-<=q^b(D) gives

    log2 M_clone < L_atom
      =Z+2181+9+2459(maxa+maxb)+132b(D)F_q,
    log2 D_coin < L_coin
      =18+4918ell_max+42b(D)F_q.

The 9 uses 13*22<2^9;18 is twice the branch-denominator exponent 9;
42=28+14 pays both signed normalizers and scaling. At D=600 these are
L_atom=7611598180401195980621428 and L_coin=2421872147123821977688178.
The optional source-specific enumeration has fewer than
2^[N L_atom+binom(N,2)L_coin] outcomes. A single enumeration for both signed
normalizers has fewer than 2^57663622547569400033400 matrices. None was run.

## 9. Verification boundary

DEPENDENCIES.md and certificates/parameters.json enumerate dimension-dependent
and fixed padding constants, both old and new. SOURCE_ACCESS.md lists the exact
inputs read and distinguishes local byte binding from connector metadata.
The checker independently builds activation moments, scores, parameters and
the M50 matrix regression; it does not import the recovered executable program.
It includes collapsed maps and an exact H-to-K2 all-map count, where all
homomorphisms are noninjective. Their validity for all maps follows from the
conventional arguments above, not extrapolation from finite controls.

The manifest verifier function is unchanged from the pinned defect-one package;
its 18 packaging rejection tests are copied byte-for-byte. The current-pinned
inherited arithmetic and 14 mutations are replayed, but no full upstream
repository verifier orCIrun is claimed. Exact logs identify an interrupted
initial orchestration attempt and the successful retry separately.

There is no newly required analytic lemma after (RL). The audit is conditional
on the retained geometric and analytic inputs exactly as the release states.
No claim of independent human acceptance, novelty, optimality, formal verification,
or an instantiated large host follows from this transfer or its finite checks.
