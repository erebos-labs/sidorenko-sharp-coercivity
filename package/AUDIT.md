# Independent audit of the sharp constant theorem

**Outcome:** the conventional proof in `THEOREM.md` is valid for precisely the stated real relaxation. No substantive mathematical gap was found. The largest coefficient for `P^2+T^2+delta^2` is `1/40`, and the positive-denominator and zero-denominator equality descriptions are complete.

**Date:** 2026-10-12. This is the **second and final focused proof pass** on the same bounded claim. It did not search for an alternative problem, extend the construction, or authorize publication or communication.

## Material reviewed

The audit compared `THEOREM.md` against the archived source text at the specified `openai/math` commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`:

* `sources/openai/tail.tex`: `eq:tail-feasible`, `eq:tail-quadratic`, `eq:tail-linear-loss`, `eq:tail-scalar-quadratic`, and the full proof of `lem:coercivity`.
* `sources/openai/planted.tex`: the definitions of the reduced and subspace parameters and the necessary-feasibility discussion in `prop:planted-gain`.
* `sources/related/global-residual-dimension.md`, at commit `9922b05bf2c3418e1a46378d4ebac60e8a34ce51`: its local scalar theorem in Section 2, including its sharpness family and scalar endpoint proof.
* `RELATED_WORK_REVIEW.md`: the stated bounded duplicate screen and its limitations.

The full global dimension theorem in the related work was not audited. This audit also does not independently re-run its repository inventory or establish mathematical priority. The exact checker and its mutation runner are separate artifacts; their recorded execution results, rather than this audit, establish whether their checks completed.

## Source fidelity

The feasible inequalities in the new theorem are exactly `eq:tail-feasible` over real variables. In particular, they retain `w=(d-3delta)/2-P+v>=0` and each individual inequality `t_i,v<=p_i+delta`. They do not insert integrality, parity, geometric-realizability conditions, or the additional subspace inequalities discussed in `planted.tex`.

The definitions of `P`, `T`, and `Q` match the source. The distinction between `Q` and the full slack `S` is explicit and correct: the linear loss is `c/4+delta/2+(2P-T)/6+v/2`. The proof never substitutes `S` for `Q`.

The denominator is retained as `N=P^2+T^2+delta^2` before every scalar optimization. No step tries to infer the minimum of the ratio from the minimum of the scalar numerator alone.

## Reduction audit

### 1. Scalar envelope and its equality

From the actual feasible inequalities, `0<=T<=P+3delta`. Consequently both arguments of

`b=min(P/3+delta,(P-T+3delta)/2)`

are nonnegative. With `z=(d-3delta)/2-P` and `a=(-z)_+`, the proof correctly derives `a<=v` from `w>=0`, `a<=P/3+delta` from averaging the individual bounds on `v`, and `a<=(P-T+3delta)/2` from `d>=P+T` and the nonnegativity of that last bound. Thus `0<=a<=b` uses no extra premise.

For `n_i=2p_i-t_i`, the exact variance identity has coefficient `1/18`:

`sum(n_i^2)/6-(sum n_i)^2/18=sum_{i<j}(n_i-n_j)^2/18`.

Also `z=z_+-a` and `a*z_+=0`. Expanding the completed square gives the stated identity

`Q-Phi = sum_{i<j}(n_i-n_j)^2/18 + (v-a)^2/2 + z_+*v + (b-a)*(b+a)/2`.

Every term is nonnegative. Its equality characterization is exact: `n_1=n_2=n_3` and `v=a=b`; these conditions automatically make `z_+*v=0`. The proof does not silently require that `v` attain the averaged individual upper bound.

### 2. Eliminating c without losing its equality direction

The exact coefficient of `c` is

`A=(d+delta)/4-(P+T)/6=(d+3delta)/12+(d-P-T)/6`.

Both terms on the right are nonnegative, since `d+3delta>=P+T+3delta>=2T`. Hence replacing `c` by `|delta|` is legitimate. The exact equality condition is `(c-|delta|)*A=0`, not merely `c=|delta|`.

The reported characterization of `A=0` is correct: the two displayed nonnegative terms must both vanish; then `d=P+T=-3delta` and `T<=P+3delta=-T`, so `T=0`, `P=d=-3delta`, and `delta<=0`. The converse is immediate. This zero-coefficient direction is essential to retaining every allowed `c>=y` in the sharpness family.

### 3. Nonnegative-delta branch

After `c=delta`, the coefficient of `d` cancels exactly. The source expression `F(T)` is unchanged. The branch breakpoint is `B=P/3+delta`; the upper endpoint is `U=P+3delta=3B`. The first minimum argument applies on `[0,B]`, and the second applies on `[B,U]`.

After subtracting the full `N/40`, the coefficient of `T^2` is `11/360` on the first interval and `-17/180` on the second. The derivative at the breakpoint on the first branch is

`-109P/540-19delta/180`.

The two endpoint values are exactly

* `(115P^2+393P*delta+144delta^2)/1620` at `B`;
* `(P^2+33P*delta+90delta^2)/180` at `U`.

These verify both the translated-square identity and the concave interpolation identity in the theorem. They are strictly positive whenever `P` and `delta` are not both zero. If both vanish, feasibility forces `T=0`, and the interval is degenerate with `N=0`. Thus this sign branch contains no positive-denominator equality case. Endpoints and the degenerate interval are all covered.

### 4. Negative-delta branch

With `delta=-y<0` and `x=P-3y`, feasibility gives `x>=0` and `0<=T<=x`. The reduction after `c=y` is exactly

`Phi(y,d;P,T,-y)=G(T)+(y/2)*(d-P-T)`.

Its discarded term is nonnegative and vanishes exactly at `d=P+T`, because `y>0`. After subtracting `((x+3y)^2+T^2+y^2)/40`, the `y^2` term cancels; this cancellation is part of the sharp coefficient, not an omitted loss.

The branch breakpoint is `B=x/3`, and the upper endpoint is `U=x`. The respective `T^2` coefficients remain `11/360` and `-17/180`, and the first-branch derivative at the breakpoint is `-109x/540-y/3`.

The endpoint values are exactly

* `(115x^2+657x*y)/1620` at `B`;
* `(x^2+33x*y)/180` at `U`.

They are strictly positive when `x>0`. When `x=0`, feasibility forces `T=0`, both endpoints coincide, and the scalar remainder is exactly zero. Thus the scalar equality condition `x=T=0` is necessary and sufficient in this sign branch. No division by the length of a zero interval occurs.

## Complete equality and sharpness audit

For `N>0`, equality forces the negative branch, `x=T=0`, and then `P=3y`. The original individual feasibility bounds give `p_i>=y`; their sum forces each `p_i=y`. Nonnegative `t_i` with sum zero vanish, and `v<=p_i-y=0` forces `v=0`. The positive coefficient `y/2` in the `d` reduction forces `d=3y`.

At these values, `A=0` permits every `c>=y`. The scalar-envelope equality also holds: the three `n_i` are `2y`, and `z=a=b=v=0`. Thus no equality condition from an earlier reduction was omitted.

Conversely, the entire family

`y>0, delta=-y, d=3y, p_1=p_2=p_3=y, t_1=t_2=t_3=v=0, c>=y`

satisfies the original constraints, including `w=0`. Direct substitution gives `Q=y^2/4` and `N=10y^2`; hence its ratio is exactly `1/40`. The supplementary identity

`Q=y^2/4+(c+y)*(d-3y)/4`

on the slice with `delta=-y`, `p_i=y`, and `t_i=v=0` independently confirms that no additional `d` direction yields equality.

For `N=0`, the constraints force `p_i=t_i=v=delta=0` and allow exactly `c,d>=0`. Then `Q=cd/4`, so equality of the inequality holds exactly when `cd=0`. The quotient is undefined and is never assigned a value on this set.

## Related bound and scope

The right-side comparison with the requested related theorem is exact:

`N/40-(P+T)^2/72=[4(P-T)^2-2P*T+9delta^2]/360`.

At the new sharpness family it is positive; at `c=delta=v=0`, `p_i=t_i=a>0`, `d>=6a`, it is negative. Both examples satisfy the same relaxed domain, and the related family has exactly `Q=a^2/2`. Consequently the two numerical lower bounds do not dominate one another by their right-hand sides under feasibility. The related theorem does not already state the same sharp-denominator result.

The wording about prior work is appropriately limited to material inspected. The theorem does not claim geometric realizability, a smaller Sidorenko counterexample, or an improved full construction dimension. No such consequence follows from the local sharp ratio alone.

## Corrections and remaining conditions

One case-sensitive documentation filename was flagged during this audit: `related_work_review.md` needed to be `RELATED_WORK_REVIEW.md`. The author corrected it. No mathematical correction was requested.

There is **no unresolved mathematical step in the conventional sharp-constant proof** identified by this audit. The independently implemented checker, its actual baseline and mutation runs, and the final checksum manifest are separate verification artifacts. Their outcomes must be read from their actual recorded results and are not implied by the mathematical verdict here.
