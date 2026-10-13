# Sharp coupling of the variance remainder and linear loss

Handoff version 1.0.0, 2026-10-13. Conventional proof with exact-arithmetic support.
This is a bounded follow-up to the published v1.2.0 of
`erebos-labs/sidorenko-sharp-coercivity`, commit
`1b6abc821b7fb95cc0ca71ba804e0c4ae19df4e4`.
The bundled `sources/published/variance/` files are authoritative inherited sources.

## 1. Inherited results and the exact new statement

The earlier theorem with denominator P^2+T^2+delta^2 and sharp coefficient
1/40, the sharp variance theorem Q >= V/48 and its equality classification,
and the published conditional M <= 256, sufficient even D >= 3072 remain
unchanged. They are inherited results, not discoveries of this handoff.

All local variables c,d,delta,v,p_i,t_i (i=1,2,3) are real. Define

\[
 P=\sum_i p_i,\quad T=\sum_i t_i,\quad s_i=p_i+t_i,\qquad
 w=(d-3\delta)/2-P+v,
 \quad V=\sum_{i<j}(s_i-s_j)^2.
\]

The complete feasible domain is precisely the published real relaxation:

\[
 c\ge|\delta|,\quad d\ge P+T,\quad p_i,t_i,v\ge0,
 \quad t_i\le p_i+\delta,\quad v\le p_i+\delta\ (i=1,2,3),
 \quad w\ge0.                                      \tag{F}
\]

There is no integrality, parity, fixed d, or geometric-realizability
assumption in this local theorem. In particular the three inequalities on
v are individual constraints, not merely their average.

Use exactly the published polynomial

\[
 Q=\frac{c(d+\delta)-\delta d+2\delta^2}{4}
 +\sum_i\left[\frac{(2p_i-t_i)^2}{6}+\delta p_i
                   -\frac c6(p_i+t_i)\right]
 +v\left(\frac{d-3\delta}{2}-P\right)+\frac{v^2}{2}. \tag{1}
\]

The full slack is retained without alteration:

\[
 S=Q-\left[\frac c4+\frac\delta2+\frac{2P-T}{6}+\frac v2\right]. \tag{2}
\]

Put

\[
 W=Q-V/48,\qquad L=\delta/2+(P-T)/4+v/2,\qquad R=W-L.
\]

**New sharp theorem.** On (F),

\[
 \boxed{S\ge\frac V{48}-\frac{3c+P+T}{12}-\frac{17}{16}.} \tag{3}
\]

The constant C = 17/16 is the smallest finite constant for this coefficient
1/12. Equality in (3) holds if and only if

\[
 \boxed{c=d=\delta=v=5/2,\qquad p_1=p_2=p_3=0,
                 \qquad t_1=t_2=t_3=1/2.}             \tag{4}
\]

Thus equality has V=0. Even on the restricted set V>0, the infimum of R is
-17/16, approached by the explicit family in Section 7, but never attained.
No division by V is used in the proof.

## 2. Equivalence and obstruction to a smaller linear coefficient

Subtracting (2) shows exactly

\[
 S-V/48+(3c+P+T)/12
  =Q-V/48-\delta/2-(P-T)/4-v/2=R.                  \tag{5}
\]

For a>0, the tuple c=delta=v=0, p=t=(a,0,0), d>=2a is feasible:
P=T=a, the two zero p coordinates force v=0, and w=d/2-a>=0.
Direct evaluation, solely to verify the obstruction, gives

\[
 Q=a^2/6,\quad V=8a^2,\quad S=a^2/6-a/6.
\]

If the coefficient of 3c+P+T were beta instead of 1/12, then on this ray

\[
 S-V/48+\beta(3c+P+T)=2a(\beta-1/12).              \tag{6}
\]

For beta<1/12 this tends to minus infinity. No finite additive C can work
with such a smaller coefficient. This is a direct feasible-ray obstruction;
it does not depend on an optimization of Q alone.

## 3. Removing c and treating nonpositive delta

Let e=d-P-T>=0. The coefficient of c in Q is

\[
 A=(d+\delta)/4-(P+T)/6
  =(d+3\delta)/12+e/6\ge0.                         \tag{7}
\]

For the sign, sum t_i<=p_i+delta to get T<=P+3delta, and observe

d+3delta-2T=e+(P-T+3delta)>=0.

Reducing c to |delta| changes neither V nor L, preserves (F), and loses
exactly (c-|delta|)A>=0. This loss vanishes precisely when that product
vanishes; c=|delta| is not silently assumed in equality cases.

### 3.1. delta=0

At c=0 put q_i=p_i-t_i>=0. Then p_i-v>=0 and

\[
 \begin{split}
 W={}&\frac18\sum_iq_i^2+\frac{v^2}{2}+B_0,\\
 B_0={}&\frac12\sum_i(p_i-v)q_i+\frac{ve}{2}
                         +\frac1{24}\sum_{i<j}s_i s_j\ge0. \tag{8}
 \end{split}
\]

This is an exact expansion of the specified Q and V. As L=sum q_i/4+v/2,

\[
 R+\frac12
 =\frac18\sum_i(q_i-1)^2+\frac12(v-1/2)^2+B_0\ge0. \tag{9}
\]

Restoring c adds cA. Therefore R>=-1/2>-17/16 in this entire sign case,
including all zero-variance and degenerate tuples.

### 3.2. delta=-y<0

Write p_i=y+a_i. Feasibility gives a_i>=0, t_i,v<=a_i. Set
X=sum a_i and d_0=d-3y. The tuple with c=delta=0, p_i=a_i, the same t_i,v,
and d=d_0 is feasible. Its w equals the original w, and its excess
length is still e=d_0-X-T>=0. Denote its quantities by Q_0,W_0,L_0,R_0.
Translation by y of all s_i leaves V invariant, and exact identities give

\[
 Q=Q_0+y^2/4+y(2X-T)/3+ye/2,\qquad L=L_0+y/4     \tag{10}
\]

at c=y. Hence

\[
 R=R_0+(y-1/2)^2/4-1/16+y(2X-T)/3+ye/2.          \tag{11}
\]

Because 0<=T<=X, the last two terms are nonnegative. Section 3.1 yields
R>=-9/16>-17/16. Restoring c adds (c-y)A>=0. This handles y>0, X=0,
zero p_i-y, zero v, and V=0 without excluding any boundary.

## 4. Positive delta: minimize the full quadratic remainder at fixed L

Now delta>0 and first c=delta. Define

\[
 q_i=p_i-t_i,\quad q=\tfrac13\sum_iq_i,\quad
 b=(v-\delta)_+,
\]

so q_i>=-delta and

\[
 p_i\ge r_i:=\max(b,q_i),\qquad
 e\ge e_0:=(3q+3\delta-2v)_+.                    \tag{12}
\]

The last bound uses w>=0; it is not omitted. The linear functional
L=delta/2+3q/4+v/2 depends only on delta,q,v, not on the distribution of
individual p_i at fixed q_i. We therefore reduce **W=Q-V/48**, not Q.

The exact expansion is

\[
 \begin{split}
 24W={}&\sum_i\{(12q_i+16\delta)p_i
                +3q_i^2+(4\delta-12v)q_i\}
          +\sum_{i<j}s_i s_j\\
       &+12v^2+12ve+18\delta^2-36\delta v.          \tag{13}
 \end{split}
\]

Let a_i=p_i-r_i>=0 and s_i^*=2r_i-q_i>=0. Replacing p_i by r_i at fixed
q_i,delta,v,e loses exactly

\[
 \sum_i(12q_i+16\delta)a_i
 +2\sum_{i<j}(s_i^*a_j+s_j^*a_i)
 +4\sum_{i<j}a_i a_j\ge0.                         \tag{14}
\]

The first coefficients are >=4delta>0, so equality requires every a_i=0.
The reduced tuple remains feasible: t_i=r_i-q_i>=0, t_i<=r_i+delta follows
from q_i>=-delta, r_i+delta>=v, and d is adjusted to P+T+e. Its w is
unchanged. This is a justified lower-bound reduction, not extra premises.

### 4.1. Exact symmetrization with the variance term retained

Define

\[
 \begin{split}
 f(x)&=(12x+16\delta)\max(b,x)+3x^2+(4\delta-12v)x,\\
 s(x)&=2\max(b,x)-x=b+|x-b|.
 \end{split}
\]

Writing h(x)=(x-b)_+, an exact form is

\[
 f(x)=3x^2+(12b+4\delta-12v)x+16\delta b
                       +12h(x)^2+(12b+16\delta)h(x). \tag{15}
\]

Set h_i=h(q_i), h=h(q), s_i^*=s(q_i), s_0=s(q), and S_*=sum s_i^*.
The following identity provides the complete symmetrization loss:

\[
 \begin{split}
 &\sum_i f(q_i)+\sum_{i<j}s_i^*s_j^*-3f(q)-3s_0^2\\
 ={}&\frac52\sum_i(q_i-q)^2
 +\frac16\sum_{i<j}[(q_i-q_j)^2-(s_i^*-s_j^*)^2]\\
 &+12[\sum_i h_i^2-3h^2]
 +(12b+16\delta)[\sum_i h_i-3h]\\
 &+\frac{(S_*-3s_0)(S_*+3s_0)}3\ \ge0.             \tag{16}
 \end{split}
\]

Every sign is justified as follows. The function s(x)=b+|x-b| is
1-Lipschitz, by the triangle inequality, so every pairwise difference of
squared differences is nonnegative. Also sum h_i>=3h: if q<=b the right
side is zero, while if q>b, summing (q_i-b)_+>=q_i-b proves it. If
hbar=sum h_i/3, then

\[
 \sum_i h_i^2-3h^2
   =\sum_i(h_i-\bar h)^2+3(\bar h-h)(\bar h+h)\ge0.
\]

Finally S_*-3s_0=2(sum h_i-3h)>=0 and both S_*,s_0 are nonnegative.
The positive first coefficient in (16) implies equality only if all
q_i=q, which also suffices for this gap to vanish.

This argument controls the possible decrease of the cross products under
symmetrization; simply applying Jensen to Q and forgetting those products
would not suffice.

### 4.2. The remaining three-scalar expression

Put

\[
 u=q+\delta\ge0,\qquad m=\max(\delta,u,v),\qquad
 e_0=(3u-2v)_+,\qquad k=3u-\delta+2v=4L.
\]

At equal q_i, the reduced variables are p_i=m-delta,
t_i=m-u, s_i=2m-delta-u. Lowering e to e_0 loses
12v(e-e_0)>=0. Direct substitution after these reductions gives

\[
 24W\ge J:=H+3(2m-\delta-u)^2,                     \tag{17}
\]

where

\[
 H=9u^2+36(m-v)u-42\delta u+12\delta m+3\delta^2
                 +12v^2+12v(3u-2v)_+.
\]

We prove the homogeneous inequality

\[
 \boxed{17J-6k^2\ge0.}                            \tag{18}
\]

No sign of k is required.

## 5. Complete nonnegative certificates for (18)

Write B=17J-6k^2 in this section only; this local B is unrelated to the
global coordinate threshold in DOWNSTREAM.md.

**When m=u**, u>=delta,v, and

\[
 B=6u^2+(u-\delta)(456u-96\delta)
                   +(u-v)(300u+228v-24\delta)\ge0. \tag{19}
\]

The two brackets are respectively 360u+96(u-delta) and
276u+228v+24(u-delta), both nonnegative. If u>0, B>0.

**When m=delta**, set delta_0=max(u,v). For either branch of the positive
part (which depends only on u,v), the exact difference is

\[
 B(\delta,u,v)-B(\delta_0,u,v)
 =(\delta-\delta_0)[300(\delta+\delta_0)-168u+24v]\ge0. \tag{20}
\]

The bracket equals
300(delta-delta_0)+600(delta_0-u)+432u+24v.
At delta=delta_0, either m=u and (19) applies, or m=v and one of the next
two identities applies. If delta>delta_0 and delta>0 this loss is strict.

**When m=v and u>=2v/3**, v>=delta,u, and

\[
 B=6(5u-4v)^2+(v-\delta)(576u-96\delta-120v)\ge0.  \tag{21}
\]

The bracket is exactly
576(u-2v/3)+168v+96(v-delta), so it is strictly positive if v>0.
For delta>0, equality in (21) is precisely delta=v and u=4v/5.

**When m=v and u<=2v/3**, let a=v-delta>=0 and r=2v/3-u>=0. Then

\[
 B=\frac83v^2+168va+96a^2+150r^2+76vr+576\delta r\ge0. \tag{22}
\]

For delta>0, v>=delta>0, so this case is strict.

These cases cover every maximum and every positive-part branch, including
ties, u=0, v=0, and 3u=2v. On delta>0, equality in (18) occurs exactly at

\[
 \delta=v>0,\qquad u=4v/5.                         \tag{23}
\]

Equations (17)-(18) give W>=k^2/68. Completing one square now yields

\[
 R+\frac{17}{16}
 \ge\frac{k^2}{68}-\frac k4+\frac{17}{16}
 =\frac{(k-17/2)^2}{68}\ge0.                       \tag{24}
\]

Together with Section 3 this proves the all-domain theorem. Notice that
every reduction kept the linear functional fixed until the explicit
three-variable homogeneous inequality (18). There was no minimization of
Q/V or Q alone.

## 6. Sharpness and every equality condition

For r>0 take c=d=delta=v=r, p_i=0, t_i=r/5. This is feasible:
P=0, T=3r/5<=d, t_i<=r, v=r=p_i+delta, and w=0. It has V=0 and

\[
 Q=17r^2/100,\qquad L=17r/20,\qquad
 R=\frac{17}{100}(r-5/2)^2-\frac{17}{16}.            \tag{25}
\]

Thus C>=17/16, with equality attained at r=5/2.

For necessity of the equality classification, Section 3 excludes delta<=0
strictly. For delta>0, every loss in Sections 4-5 and the square in (24)
must vanish. Equation (23) and k=17/2 give

delta=v=5/2 and u=2.

Equation (16) forces all q_i=q=u-delta=-1/2. The strictly positive first
coefficients of (14) force p_i=max(0,q_i,v-delta)=0, so t_i=1/2.
Since v>0, the e-reduction forces e=e_0=3u-2v=1. Therefore d=P+T+e=5/2.
At this tuple A=(d+delta)/4-(P+T)/6=1>0, so the initial c-reduction forces
c=delta=5/2. All constraints and losses are then equalities. This gives
exactly (4), not a larger set produced by forgetting intermediate losses.

At (4), Q=17/16, L=17/8, V=0, and S=-29/16. In particular local slack is
negative at the new sharp point.

## 7. V=0 and a positive-V limiting family

The proof above never divided by V and already covers all feasible tuples
with V=0. On this subset V=0 is equivalent to s_1=s_2=s_3. Equality in the
new inequality is still exactly (4); all other feasible V=0 tuples are
strict. For example p=t=delta=v=0 leaves c,d>=0 and R=cd/4>=0. The fully
coincident subcase d=0 has S=-c/4 despite R=0.

For 0<epsilon<=1/2, retain c=d=delta=v=5/2 and p_i=0, but use

\[
 (t_1,t_2,t_3)=(1/2+\epsilon,1/2-\epsilon,1/2).
\]

This family is feasible, has w=0, and satisfies exactly

\[
 V=6\epsilon^2>0,\qquad
 R=-17/16+5\epsilon^2/24.                           \tag{26}
\]

Therefore the same optimal C is necessary even on the positive-V domain,
although equality is attained only when V=0. This handles the boundary
without mistaking the variance sharp ray for the affine minimizer.

## 8. Verification boundary

`checker.py` verifies all displayed polynomial identities with rational
coefficients, exact feasible examples, and source bindings. The sign,
coverage, and equality arguments above are conventional mathematics, not
inferred from numerical samples. `test_mutations.py` deliberately corrupts
proof constants, feasibility, and downstream data and requires rejection.
The derivation's exploratory exact algebra used SymPy; the portable replay
requires only Python's standard library. No numerical minimization was
needed. The same-session audit is not independent human review or Lean
verification. Mathematical priority and geometric realization remain
unestablished. The task stops at this sharp full-slack bound and the one
conditional original-template application.
