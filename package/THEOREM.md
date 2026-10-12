# Sharp coercivity for the relaxed Sidorenko tail quadratic

**Status:** conventional exact proof, with finite symbolic arithmetic checks supplied separately. The largest constant for the denominator specified below is **1/40**. This is a statement about the source's necessary real relaxation, not about realizability of its extremizers.

**Source pin:** `openai/math` commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, family 161, *A counterexample to Sidorenko's conjecture*. The two authoritative files are [tail.tex](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/tail.tex) and [planted.tex](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/planted.tex). Their exact bytes, Git blob identifiers, and SHA-256 hashes accompany this package.

## 1. The exact optimization problem

All variables in this note are real. For i=1,2,3, define

\[
P=\sum_i p_i,\qquad T=\sum_i t_i,\qquad
w=\frac{d-3\delta}{2}-P+v.
\]

The feasible domain is precisely `eq:tail-feasible` interpreted over the reals:

\[
c\ge |\delta|,\qquad P+T\le d,\qquad
p_i,t_i,v\ge0,\qquad t_i\le p_i+\delta,\qquad
v\le p_i+\delta\quad(i=1,2,3),\qquad w\ge0.
\tag{1}
\]

There are no added integrality, parity, individual-subspace-dimension, or realizability conditions. In particular d is not fixed. The ambient parameter D, if desired for notation only, is c+d. The source's actual geometric tuples lie in this relaxation, but the source explicitly does not assert sufficiency of these necessary conditions.

Use exactly the homogeneous quadratic part in `eq:tail-quadratic`:

\[
\begin{aligned}
Q={}&\frac{c(d+\delta)-\delta d+2\delta^2}{4}\\
&+\sum_{i=1}^3\left[
\frac{(2p_i-t_i)^2}{6}+\delta p_i-\frac{c(p_i+t_i)}6
\right]
+v\left(\frac{d-3\delta}{2}-P\right)+\frac{v^2}{2}.
\end{aligned}
\tag{2}
\]

The denominator is

\[
N=P^2+T^2+\delta^2.
\tag{3}
\]

The source's `lem:coercivity` proves Q>=N/342. Its full slack is a different expression:

\[
S=Q-\left(\frac c4+\frac\delta2+\frac{2P-T}{6}+\frac v2\right).
\tag{4}
\]

Every bound below concerns Q, not S.

### Theorem

Every tuple satisfying (1) satisfies

\[
\boxed{Q\ge\frac{P^2+T^2+\delta^2}{40}.}
\tag{5}
\]

The constant 1/40 is the largest possible. With N>0, equality holds **if and only if** there is a real y>0 such that

\[
\boxed{
\delta=-y,\quad d=3y,\quad
p_1=p_2=p_3=y,\quad
t_1=t_2=t_3=v=0,\quad c\ge y.
}
\tag{6}
\]

With N=0, feasibility is equivalent to p_i=t_i=v=delta=0 and c,d>=0. Then Q=cd/4. The inequality is an equality exactly when cd=0. The quotient Q/N is undefined throughout this zero-denominator set.

## 2. Related work and non-equivalence

The specifically requested related work is [PR #4](https://github.com/rohanarun/sidorenko-template-refinements/pull/4), whose inspected head is `9922b05bf2c3418e1a46378d4ebac60e8a34ce51`. Section 2 of its [pinned theorem](https://github.com/artuskg/sidorenko-template-refinements/blob/9922b05bf2c3418e1a46378d4ebac60e8a34ce51/global-residual-dimension.md) proves the different sharp inequality

\[
Q\ge\frac{(P+T)^2}{72}.
\tag{7}
\]

At inspection on 2026-10-12, that PR was open and draft, with no discussion comments in the retrieved snapshot. Its local inequality is a mathematical argument inspected directly; its PR state is not a claim of merged or formally verified status. The broader bounded inspection is recorded in `RELATED_WORK_REVIEW.md`, including current branches, relevant newer work, query limitations, and exact pins.

Neither displayed bound dominates the other on (1). Exactly,

\[
\frac N{40}-\frac{(P+T)^2}{72}
=\frac{4(P-T)^2-2PT+9\delta^2}{360}.
\tag{8}
\]

Two feasible directions give opposite signs:

| Feasible family | N/40 | (P+T)^2/72 | Q |
|---|---:|---:|---:|
| (6), y>0 | y^2/4 | y^2/8 | y^2/4 |
| c=delta=v=0, p_i=t_i=a>0, d>=6a | 9a^2/20 | a^2/2 | a^2/2 |

Thus one numerical lower bound cannot be converted into the other simply by comparing right-hand sides under the feasible constraints. The statements are not equivalent. They share the source scalar reduction, but their different denominators require different endpoint inequalities. In particular, replacing (7) by (5) in an argument needing the full coefficient 1/72 would not be justified by dominance.

The target theorem was not located in the inspected material. This is a bounded non-duplication finding, not a claim of global novelty or mathematical priority.

## 3. Verification of the proposed upper-bound family

Take the parameters in (6). They have P=3y, T=0, and

\[
p_i+\delta=0,\qquad P+T=d,\qquad
w=\frac{3y+3y}{2}-3y=0.
\]

All conditions in (1) hold for every c>=y. Substitution into (2) gives

\[
\begin{aligned}
Q
&=\frac{2cy+5y^2}{4}
 +3\left(\frac{4y^2}{6}-y^2-\frac{cy}{6}\right)\\
&=\frac{y^2}{4},
\qquad N=9y^2+y^2=10y^2.
\end{aligned}
\tag{9}
\]

Consequently Q/N=1/40, so no larger universal constant is possible. The rest of the proof establishes the universal lower bound and excludes all other positive-denominator equality cases.

## 4. Scalar reduction, with its exact equality conditions

Define

\[
n_i=2p_i-t_i,\quad
z=\frac{d-3\delta}{2}-P,\quad
a=(-z)_+,\quad z_+=\max(z,0),\quad
b=\min\left(\frac P3+\delta,\frac{P-T+3\delta}{2}\right).
\tag{10}
\]

Here b is the scalar called v_0 in the source's coercivity proof; it is not the source's unrelated function b(n)=n(n+1)/2.

From t_i<=p_i+delta and nonnegativity,

\[
0\le T\le P+3\delta,\qquad P+3\delta\ge0.
\tag{11}
\]

Both arguments defining b are therefore nonnegative. As w=z+v>=0 and v>=0, a<=v. Averaging v<=p_i+delta gives v<=P/3+delta. Also

\[
-z=P-\frac{d-3\delta}{2}
\le\frac{P-T+3\delta}{2};
\]

because the right side is nonnegative, this gives a<=(P-T+3delta)/2. Hence

\[
0\le a\le b.
\tag{12}
\]

Let the scalar expression in `eq:tail-scalar-quadratic` be

\[
\Phi(c,d;P,T,\delta)=
\frac{c(d+\delta)-\delta d+2\delta^2}{4}
+\frac{(2P-T)^2}{18}+\delta P
-\frac{c(P+T)}6-\frac{b^2}{2}.
\tag{13}
\]

There is an exact identity

\[
\begin{aligned}
Q-\Phi
={}&\frac1{18}\sum_{i<j}(n_i-n_j)^2
+\frac{(v-a)^2}{2}+z_+v
+\frac{(b-a)(b+a)}2.
\end{aligned}
\tag{14}
\]

Every summand is nonnegative. This records both the variance inequality and the two scalar-square reductions, rather than losing their equality conditions. Equality Q=Phi holds exactly when

\[
n_1=n_2=n_3,\qquad v=a=b.
\tag{15}
\]

Indeed v=a makes z_+v=0 automatically, since a=(-z)_+; and b^2=a^2 with a,b>=0 is equivalent to b=a.

The coefficient of c in Phi is

\[
A=\frac{d+\delta}{4}-\frac{P+T}{6}
=\frac{d+3\delta}{12}+\frac{d-P-T}{6}\ge0.
\tag{16}
\]

For its sign, use d+3delta>=P+T+3delta>=2T>=0. Thus

\[
\Phi(c,d;P,T,\delta)
=\Phi(|\delta|,d;P,T,\delta)+(c-|\delta|)A.
\tag{17}
\]

This reduction is an equality if and only if c=|delta| or A=0. On the feasible domain,

\[
A=0\quad\Longleftrightarrow\quad
\delta\le0,\quad T=0,\quad P=d=-3\delta.
\tag{18}
\]

To see this, the two nonnegative terms in (16) must both vanish. Then d=-3delta=P+T and (11) gives T<=-T, so T=0. The converse follows by substitution. In particular, equality does not generally force c=|delta|.

## 5. Proving the lower bound with the denominator retained

We now subtract N/40 before bounding the scalar expression. Minimizing Phi or Q alone would not determine Q/N, since N changes with T.

### 5.1. Nonnegative delta

Suppose delta>=0. After c is replaced by delta, all d terms cancel. Equation (13) becomes

\[
F(T)=\frac{3\delta^2}{4}+
\frac{(2P-T)^2}{18}+\frac{(5P-T)\delta}{6}
-\frac12\min\left(\frac P3+\delta,\frac{P-T+3\delta}{2}\right)^2,
\quad 0\le T\le P+3\delta.
\tag{19}
\]

Set

\[
H_+(T)=F(T)-\frac{P^2+T^2+\delta^2}{40},\quad
B_+=P/3+\delta,\quad U_+=P+3\delta.
\tag{20}
\]

On [0,B_+] the first argument of the minimum is used. On [B_+,U_+] the second is used. Direct expansion gives the following endpoint values and first-interval coefficient:

\[
\begin{aligned}
E_{+,B}&=H_+(B_+)
=\frac{115P^2+393P\delta+144\delta^2}{1620},\\
E_{+,U}&=H_+(U_+)
=\frac{P^2+33P\delta+90\delta^2}{180},\\
C_+&=\frac{109P}{540}+\frac{19\delta}{180}.
\end{aligned}
\tag{21}
\]

All these expressions have nonnegative coefficients in P,delta>=0. On the first interval write s=B_+-T>=0. Then exactly

\[
H_+(T)=E_{+,B}+sC_++\frac{11s^2}{360}\ge0.
\tag{22}
\]

If B_+<U_+, write T=B_++lambda(U_+-B_+) with 0<=lambda<=1. The second interval has the exact interpolation identity

\[
H_+(T)=(1-\lambda)E_{+,B}+\lambda E_{+,U}
+\frac{17}{180}\lambda(1-\lambda)(U_+-B_+)^2\ge0.
\tag{23}
\]

The degenerate interval B_+=U_+ is possible only for P=delta=0; then T=0 and N=0. If N>0, at least one of P,delta is positive, and both endpoint values in (21) are strictly positive. Equations (22)-(23) therefore give H_+(T)>0 throughout the allowed interval. In this sign case the target bound is strict whenever its denominator is positive.

### 5.2. Negative delta

Now let delta=-y<0 and put x=P-3y. From (11), x>=0 and 0<=T<=x. At c=y, equation (13) has the exact form

\[
\Phi(y,d;P,T,-y)
=G(T)+\frac y2(d-P-T),
\tag{24}
\]

where

\[
G(T)=\frac{y^2}{4}+\frac{(2x-T)y}{3}
+\frac{(2x-T)^2}{18}
-\frac12\min\left(\frac x3,\frac{x-T}{2}\right)^2.
\tag{25}
\]

The discarded term in (24) is nonnegative, and because y>0 it vanishes exactly when d=P+T.

Set

\[
H_-(T)=G(T)-\frac{(x+3y)^2+T^2+y^2}{40},\quad
B_-=x/3,\quad U_-=x.
\tag{26}
\]

The endpoint values and first-interval coefficient are

\[
\begin{aligned}
E_{-,B}&=H_-(B_-)
=\frac{115x^2+657xy}{1620},\\
E_{-,U}&=H_-(U_-)
=\frac{x^2+33xy}{180},\\
C_-&=\frac{109x}{540}+\frac y3.
\end{aligned}
\tag{27}
\]

On 0<=T<=B_-, with s=B_--T, exactly

\[
H_-(T)=E_{-,B}+sC_-+\frac{11s^2}{360}\ge0.
\tag{28}
\]

For x>0 and B_-<=T<=U_-, put T=B_-+lambda(U_--B_-). Then

\[
H_-(T)=(1-\lambda)E_{-,B}+\lambda E_{-,U}
+\frac{17}{180}\lambda(1-\lambda)(U_--B_-)^2\ge0.
\tag{29}
\]

If x>0, both endpoints in (27) are strictly positive, so H_-(T)>0. If x=0, feasibility forces T=0; both endpoints are zero and H_-(0)=0. Thus H_-=0 if and only if x=T=0 in this sign case.

Equations (14), (17), and (24), followed by (28)-(29), prove Q>=N/40. Together with the positive-sign case, this establishes the universal assertion (5).

## 6. Complete equality analysis

Suppose N>0 and Q=N/40. The positive-sign analysis excludes delta>=0, so delta=-y<0.

The nonnegative decomposition is, exactly,

\[
Q-\frac N{40}
=(Q-\Phi)+(c-y)A+\frac y2(d-P-T)+H_-(T).
\tag{30}
\]

Every summand must vanish. By (27)-(29), H_-=0 forces x=0 and T=0, hence P=3y. Since every p_i+delta=p_i-y is nonnegative and sum p_i=3y, necessarily p_i=y individually. Nonnegative t_i summing to T=0 give t_i=0. The constraints v<=p_i-y=0 give v=0. The strictly positive coefficient y/2 in (30) forces d=P+T=3y.

For these parameters, A=0. Therefore (c-y)A=0 for every c>=y. Also n_i=2y, z=a=b=v=0, so the full equality conditions (15) hold, not just the scalar endpoints. The candidate-family calculation (9) verifies the converse.

An additional direct identity on the entire forced slice is useful as a check:

\[
Q=\frac{y^2}{4}+\frac{(c+y)(d-3y)}4
\quad\text{when}\quad
\delta=-y,\ p_i=y,\ t_i=v=0.
\tag{31}
\]

Feasibility gives c>=y and d>=3y, and c+y>0. Consequently equality on this slice is precisely d=3y, with c unrestricted above y. This agrees with (30) and excludes an accidental extra d direction.

For N=0, all three nonnegative squares P^2,T^2,delta^2 vanish. Nonnegative p_i and t_i then vanish individually, and v<=p_i+delta=0 gives v=0. Conversely any c,d>=0 with these zero coordinates satisfies (1). Substitution in (2) gives Q=cd/4. Equality of the inequality holds exactly when c=0 or d=0; Q/N is never assigned a value here.

## 7. Exact checks, scope, and stopping point

The checker reconstructs Q and S using exact rational arithmetic, verifies the symbolic reduction and branch identities coefficient by coefficient, validates pinned source hashes, and evaluates exact feasible examples. Its certificate mutations deliberately alter an endpoint coefficient and the proposed sharp constant, and the mutation runner requires rejection. No floating-point minimization, numerical tolerance, bounded scan, or solver result is used to justify the universal theorem.

The finite checker supports the conventional proof; it is not a proof assistant and does not certify the source's geometric construction. The human-readable sign and equality arguments are part of this proof, with their specific algebraic identities checked separately. Source-file hash checks bind the archived source bytes; they do not automatically translate LaTeX semantics into executable mathematics.

The completed result improves the coefficient of the source's particular coercive denominator from 1/342 to its relaxed-domain optimum 1/40, a factor 171/20. It does not assert that (6) is geometrically realizable, that a smaller Sidorenko counterexample exists, or that the full construction dimension has improved. The separate sharp inequality (7) remains useful in its own direction. No global construction, dimension optimization, publication, pull request, or external communication is part of this work.

The work stops at this proved sharp theorem and its equality classification. At most two focused proof passes are used: derivation and an independent audit of the same bounded claim.
