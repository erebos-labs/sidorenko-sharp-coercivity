> Packaging note for 1.0.1: mathematical/historical text below is unchanged from 1.0.0. Source paths under global, effective-host, and review are external references, not bundled snapshots. See README.md and distribution.json. Historical replay commands require the temporary source overlay; use verify_package.py --source-cache DIR for this release. The historical API review inventory is omitted.

# Sharp variance coercivity on the relaxed family-161 domain

Version 1.0.0. Derivation date: 2026-10-12 UTC.

## Result and scope

On exactly the relaxed real domain of OpenAI's `eq:tail-feasible`,
the largest constant in
\[
 Q\ge\kappa V,\qquad
 V=\sum_{1\le i<j\le3}[(p_i+t_i)-(p_j+t_j)]^2
\]
is **\(\kappa=1/48\)**.

For \(V>0\), equality holds precisely, up to permutation of the three indices, at
\[
 c=\delta=v=0,\quad p=t=(a,0,0),\quad a>0,\quad d\ge2a.
\]
When \(V=0\), the ratio is undefined. The inequality still holds, and its equality cases are precisely
\[
 p=t=0,\quad \delta=v=0,\quad c,d\ge0,\quad cd=0.
\]

This is a statement about real tuples satisfying the displayed inequalities. No geometric realizability, integrality, or parity condition is added to the local theorem. The downstream dimension argument in DOWNSTREAM.md explicitly reintroduces the existing integer-profile assumptions only where its source requires them.

## 1. Pinned definitions

The primary source is `openai/math` at
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`,
`preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/tail.tex`,
equations `eq:tail-feasible`, `eq:tail-quadratic`, and `eq:tail-linear-loss`.
The accompanying `planted.tex` defines the quantities from which the slack is obtained.

All of \(c,d,\delta,p_i,t_i,v\) are real. Put
\[
 P=\sum_i p_i,\quad T=\sum_i t_i,\quad s_i=p_i+t_i,\quad
 w=\frac{d-3\delta}{2}-P+v.
\]
The entire local feasible domain is
\[
 c\ge|\delta|,\qquad P+T\le d,\qquad
 p_i,t_i,v\ge0,\qquad t_i\le p_i+\delta,\quad v\le p_i+\delta,\qquad w\ge0.
 \tag{F}
\]
There are three indices. In particular, the bound on \(v\) holds for every index.

The quadratic under study is exactly
\[
 Q=\frac{c(d+\delta)-\delta d+2\delta^2}{4}
 +\sum_i\left[\frac{(2p_i-t_i)^2}{6}+\delta p_i-\frac c6(p_i+t_i)\right]
 +v\left(\frac{d-3\delta}{2}-P\right)+\frac{v^2}{2}. \tag{1}
\]
The full slack remains
\[
 S=Q-\left[\frac c4+\frac\delta2+\frac{2P-T}{6}+\frac v2\right]. \tag{2}
\]
No assertion below replaces \(Q\) by \(S\), or assumes each local \(S\) is nonnegative.

The source's scalar averaging in `eq:tail-scalar-quadratic` and its \(1/342\) coercivity lemma are not sufficient to identify this variance optimum. Here the variable-level sum \(\sum_i s_i^2\) is retained.

## 2. An intermediate inequality

We will prove
\[
 \boxed{\quad Q\ge\frac1{24}\sum_i s_i^2+\frac{\delta^2}{8}.\quad} \tag{3}
\]
This auxiliary bound is used to prove the requested theorem; the denominator is never replaced during an optimization of a ratio.

Let \(e=d-P-T\ge0\). The coefficient of \(c\) in \(Q\) is
\[
 A=\frac{d+\delta}{4}-\frac{P+T}{6}
  =\frac{d+3\delta}{12}+\frac e6\ge0. \tag{4}
\]
Indeed \(T\le P+3\delta\), hence \(d+3\delta\ge2T\ge0\).
Reducing \(c\) to \(|\delta|\) loses exactly \((c-|\delta|)A\).
Equality in this reduction means that product is zero; it does not generally force \(c=|\delta|\).

### 2.1. The case \(\delta=0\)

Here \(q_i=p_i-t_i\ge0\), and \(p_i-v\ge0\). At \(c=0\), direct expansion gives
\[
 24Q-\sum_i s_i^2
 =12\sum_i(p_i-v)q_i+3\sum_iq_i^2+12v^2+12ve. \tag{5}
\]
Every term is nonnegative, proving (3) in this case. For arbitrary \(c\ge0\), add \(24cA\) to the right.

Equality in (5) holds if and only if \(q_1=q_2=q_3=v=0\).
Thus equality in (3) at \(\delta=0\) means \(p=t,\ v=0,\ cA=0\).
This leaves \(d\) free subject to (F).

### 2.2. The case \(\delta=-y<0\)

The constraints imply \(p_i=y+a_i\), where \(a_i\ge0\), \(t_i\le a_i\), and \(v\le a_i\). Put
\[
 X=\sum_i a_i=P-3y,\qquad \widetilde d=d-3y.
\]
The tuple with \(c=\delta=0\), \(p_i=a_i\), the same \(t_i,v\), and \(d=\widetilde d\) satisfies (F):
\(\widetilde d\ge X+T\), and its \(w\) equals the original \(w\).
Call its quadratic \(Q_0\). At \(c=y\), the exact identity is
\[
 Q=Q_0+\frac{y^2}{4}+\frac{y(2X-T)}3+\frac{ye}{2}. \tag{6}
\]
Since \(s_i=y+a_i+t_i\), applying (5) to \(Q_0\) yields
\[
 Q-\frac1{24}\sum_i s_i^2-\frac{y^2}{8}
 \ge \frac{y(7X-5T)}{12}+\frac{ye}{2}\ge0, \tag{7}
\]
because \(0\le T\le X\). Restoring \(c\) adds \((c-y)A\).

For completeness, equality in (3) for \(y>0\) forces \(X=T=e=0\); then \(a_i=t_i=v=0\), \(d=3y\), and \(A=0\). Consequently every \(c\ge y\) is allowed. These tuples have \(V=0\) and \(Q=y^2/4>0\). In particular, the earlier sharp \(1/40\) equality family does not give equality for the present positive-denominator ratio.

### 2.3. The case \(\delta>0\)

After reducing \(c\) to \(\delta\), define
\[
 R=24Q-\sum_i s_i^2,\qquad q_i=p_i-t_i,\qquad q=\frac13\sum_iq_i.
\]
Here \(q_i\ge-\delta\). The constraints also give
\[
 p_i\ge\max(0,q_i,v-\delta),\qquad
 e\ge\max(0,3q+3\delta-2v). \tag{8}
\]
The last inequality is precisely the consequence \(w\ge0\) that is needed below; it is not discarded.

An exact expansion, before any averaging, is
\[
 R=\sum_i\left[(12q_i+16\delta)p_i+3q_i^2+(4\delta-12v)q_i\right]
   +12v^2+12ve+18\delta^2-36\delta v. \tag{9}
\]
Since \(12q_i+16\delta\ge4\delta>0\), replacing \(p_i\) by the lower bound in (8) decreases \(R\). The precise loss is
\[
 \sum_i(12q_i+16\delta)
       \bigl[p_i-\max(0,q_i,v-\delta)\bigr]\ge0. \tag{10}
\]

Let \(b=(v-\delta)_+\) and define, for \(x\ge-\delta\),
\[
 f(x)=(12x+16\delta)\max(b,x)+3x^2+(4\delta-12v)x.
\]
Writing \(h=(x-b)_+\), this is
\[
 f(x)=3x^2+(12b+4\delta-12v)x+16\delta b
      +12h^2+(12b+16\delta)h. \tag{11}
\]
It is strictly convex: its \(3x^2\) term is strictly convex and all the other nonlinear terms are convex with nonnegative coefficients. Thus
\(\sum_i f(q_i)\ge3f(q)\), with equality only when all \(q_i=q\).
More explicitly, the Jensen gap is
\[
 3\sum_i(q_i-q)^2+
 12\left[\sum_i(q_i-b)_+^2-3(q-b)_+^2\right]+
 (12b+16\delta)\left[\sum_i(q_i-b)_+-3(q-b)_+\right]. \tag{12}
\]
Both bracketed terms are nonnegative, by the positive-part inequality followed by the sum-of-squares inequality. This reduction is applied to \(R\), which already contains the desired variable-level quadratic subtraction, rather than to \(Q\) alone.

Set
\[
 u=q+\delta\ge0,\qquad m=\max(\delta,u,v),\qquad
 e_0=(3u-2v)_+.
\]
Then \(\max(0,q,v-\delta)=m-\delta\). Replacing \(e\) by \(e_0\) loses exactly \(12v(e-e_0)\ge0\). After these reductions,
\[
 R\ge H:=
 9u^2+36(m-v)u-42\delta u+12\delta m+3\delta^2
 +12v^2+12v(3u-2v)_+. \tag{13}
\]

We next prove \(H\ge3\delta^2\) on \(u,v\ge0,\delta>0\).
Ties in the maximum defining \(m\) can be assigned to either applicable case.

**Case \(m=u\).** Here \(u\ge\delta,v\), so \(3u-2v\ge0\), and
\[
 H=45u^2-30\delta u+3\delta^2-12v^2
 \ge 6\delta^2+(u-\delta)(33u+3\delta)\ge6\delta^2. \tag{14}
\]
The first difference is exactly \(12(u^2-v^2)\ge0\).

**Case \(m=\delta\).** Here \(0\le u,v\le\delta\).
In (13), the \(v\)-dependent part after collecting terms is
\[
 g_u(v)=
 \begin{cases}
 -12v^2,&v\le3u/2,\\
 12(v-3u/2)^2-27u^2,&v\ge3u/2.
 \end{cases}
\]
It is minimized on \([0,\delta]\) at \(v=\min(\delta,3u/2)\).
It follows that
\[
 H\ge
 \begin{cases}
 3\delta^2+6(\delta+u)(2\delta-3u),&u\le2\delta/3,\\
 3\delta^2+3u(3u-2\delta),&u\ge2\delta/3.
 \end{cases} \tag{15}
\]
Both displayed remainders are nonnegative. Equality at \(3\delta^2\) requires \(u=2\delta/3\) and \(v=\delta\).
For the first line the exact minimization remainders are
\(12[(3u/2)^2-v^2]\) when \(v\le3u/2\), and \(12(v-3u/2)^2\) when \(v\ge3u/2\).
For the second line the remainder is \(12(\delta^2-v^2)\).

**Case \(m=v\).** Here \(v\ge\delta,u\).
If \(u\ge2v/3\), direct expansion gives
\[
 H=3\delta^2+16v(v-\delta)
 +(u-2v/3)(48v-42\delta)+9(u-2v/3)^2\ge3\delta^2. \tag{16}
\]
Indeed \(48v-42\delta\ge6\delta>0\).
If \(u\le2v/3\), the positive part vanishes. There are two useful exact forms:
\[
 \begin{split}
 H={}&3\delta^2+(2\delta/3-u)(36\delta-9u)
       +36\delta(v-\delta)+12(v-\delta)^2,
       &&u\le2\delta/3; \tag{17}\\
 H={}&3\delta^2+12u(3u-2\delta)
       +(12\delta+36u)(v-3u/2)+12(v-3u/2)^2,
       &&u\ge2\delta/3. \tag{18}
 \end{split}
\]
Their terms are nonnegative under their indicated cases.
Equality in any of (16)–(18) at \(3\delta^2\) again requires
\(u=2\delta/3,\ v=\delta\).

Thus \(R\ge3\delta^2\), proving (3) for \(\delta>0\).
The equality losses have all been displayed. Combining them shows that equality in (3) for this sign occurs precisely at
\[
 c=d=v=\delta>0,\qquad p_i=0,\qquad t_i=\delta/3.
 \tag{19}
\]
In particular, \(e=e_0=0\), all the \(q_i\) agree, the bounds on \(p_i\) are attained, and \(A>0\) forces \(c=\delta\). This family also has \(V=0\), with \(Q=5\delta^2/36>0\).

## 3. The sharp variance constant and all equality cases

Because \(s_i\ge0\),
\[
 V=2\sum_i s_i^2-2\sum_{i<j}s_is_j.
\]
Consequently (3) gives the explicit gap bound
\[
 Q-\frac V{48}
 \ge \frac1{24}\sum_{i<j}s_is_j+\frac{\delta^2}{8}\ge0. \tag{20}
\]
This proves the universal coefficient \(1/48\).

If \(V>0\) and equality holds, (20) forces \(\delta=0\) and every \(s_is_j=0\).
At most one \(s_i\) is positive. Equality in (5), including the restored \(c\) term, forces \(p=t,\ v=0,\ cA=0\).
The positive coordinate is therefore \(s_i=2a\) with \(a>0\).
Since \(d\ge2a\),
\[
 A=d/4-a/3\ge a/6>0,
\]
so \(c=0\). The remaining constraints are exactly \(d\ge2a\).
This proves necessity of the stated equality classification, without inferring equality solely from a minimizer of \(Q\).

Conversely, for the stated family,
\[
 P=T=a,\quad w=d/2-a\ge0,\quad
 Q=\frac{a^2}{6},\quad V=(2a)^2+(2a)^2=8a^2.
\]
Every constraint in (F) is satisfied. Thus the ratio is \(1/48\), proving maximality of the constant.

If \(V=0\), then \(s_1=s_2=s_3=\sigma\ge0\). Equation (3) gives
\(Q\ge\sigma^2/8+\delta^2/8\).
Equality \(Q=0\) therefore requires \(\sigma=\delta=0\).
Nonnegativity forces \(p=t=0\), the bounds on \(v\) force \(v=0\), and (F) reduces to \(c,d\ge0\).
Directly from (1), \(Q=cd/4\), giving the zero-denominator equality classification in the result statement.

## 4. The earlier \(1/144\) bound and the slack distinction

At its specified commit, PR4 proves \(Q\ge(P+T)^2/72\).
For \(s_i\ge0\),
\[
 2(P+T)^2-V=6\sum_{i<j}s_is_j\ge0,
\]
which verifies its consequence \(Q\ge V/144\). Independently, (3) recovers
\(Q\ge\sum_i s_i^2/24\ge(P+T)^2/72\).
The new variance coefficient is three times the old coefficient. The sharpness family gives \(Q=V/48>V/144\), so the old bound alone does not establish the sharp constant.

The full slack (2) can be negative even on a positive-\(V\) tuple.
For \(a=1/2,\ d=1,\ c=\delta=v=0,\ p=t=(1/2,0,0)\),
\[
 Q=1/24,\quad V=2,\quad S=-1/24.
\]
All constraints hold, and the quadratic bound is an equality.
This example prevents a substitution of \(S\) for \(Q\).

## 5. What is certified, and what is not

The standard-library checker compares exact rational polynomial coefficients for the source identities, each reduction above, the case identities, and rational equality examples. Mutation tests change the proposed constant, a reduction coefficient, a sign, a full-slack coefficient, and source bytes, and require rejection. Numerical sampling is not used as proof.

The accompanying downstream certificate concerns the original 35-vertex template and the existing analytic argument only. It does not realize local sharp tuples geometrically. Neither local sharpness nor that certificate establishes a smaller counterexample graph, reconstructs a finite host, or proves that the resulting sufficient dimension is optimal.

RELATED_WORK_REVIEW.md records the bounded inspection of the requested current PRs and branches. No duplicate was found in that inspected material. Mathematical novelty is unverified; absence from this review is not a priority claim.

