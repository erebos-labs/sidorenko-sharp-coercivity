> Packaging note for 1.0.1: mathematical/historical text below is unchanged from 1.0.0. Source paths under global, effective-host, and review are external references, not bundled snapshots. See README.md and distribution.json. Historical replay commands require the temporary source overlay; use verify_package.py --source-cache DIR for this release. The historical API review inventory is omitted.

# One adversarial audit

Package version: 1.0.0. Audit completed 2026-10-12 23:14 UTC.

## Decision and provenance

**PASS: no material mathematical or certificate gap was found in the delivered local theorem or the original-template application.** The sharp relaxed-domain coefficient is `1/48`; the conditional downstream calculation certifies `M <= 256` and the sufficient even dimension `D = 3072`.

This is the single adversarial audit requested for this task, performed by a separate agent within the same task. It reviewed the completed derivation rather than conducting another proof search. No template search, finite-host reconstruction, publication, external communication, or new mathematical direction was undertaken.

The audit read `THEOREM.md`, `DOWNSTREAM.md`, both exact checkers, both mutation scripts, the local and matrix certificates, the example file, and the source manifest. The governing source passages were checked against the pinned copies of OpenAI's `tail.tex` and `planted.tex`, the original literal template in `complex.tex`, the PR4 global-energy theorem and certificate, and Sections 4–7 of the recovered proof. The source commits are:

| Source | Commit |
|---|---|
| `openai/math` | `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` |
| Completed sharp `1/40` package | `0339f50a039001dc06bd12ffc664ab05a50253fb` |
| PR4 global-energy package | `9922b05bf2c3418e1a46378d4ebac60e8a34ce51` |
| Recovered original-template proof | `06acd4cf46bfe9086f9abc7d85b5c9f171480143` |

The six principal source bindings are hard-pinned in the local checker. Every one of the 22 manifest entries passes its byte-length, SHA-256, and Git-blob SHA-1 checks. Retrieved source programs are retained as data and are not executed by the new checkers.

## Local proof audit

The displayed real domain is precisely `eq:tail-feasible`. In particular, the bound on `v` is imposed at every index, and `w >= 0` is retained. No dimension parity, integrality, `r'` restriction, or geometric realizability condition has been inserted into the local theorem. The displayed `Q` is exactly `eq:tail-quadratic`; `S` retains every term of `eq:tail-linear-loss`.

The proof establishes the stronger intermediate inequality

`Q >= sum_i (p_i+t_i)^2 / 24 + delta^2 / 8`.

The variable-level sum of squares is subtracted before the positive-delta scalar reduction, retaining the information needed for the final variance comparison. The proof does not confuse a minimizer of `Q` with a minimizer of a ratio.

| Reduction | Audited issue and outcome |
|---|---|
| Common variable `c` | Its coefficient is nonnegative by `T <= P+3delta` and `d >= P+T`. The exact loss is `(c-|delta|)A`; equality correctly permits `A=0`. |
| `delta=0` | Every term of the exact nonnegative identity has the stated sign. Equality forces `p=t`, `v=0`, and `cA=0`. |
| `delta<0` | The shift `p_i=y+a_i`, `d'=d-3y` preserves the feasible zero-delta domain and `w`. The additional auxiliary gap is nonnegative because `T<=X`. Its equality family is correctly retained. |
| `delta>0`: lower bounds | `q_i>=-delta` makes every coefficient `12q_i+16delta` strictly positive. The lower bound on `e` follows directly from `w>=0`. |
| Positive-delta convexity | The positive-part representation of `f` is exact. Its `3x^2` term gives strict convexity, so Jensen equality requires all `q_i` equal. Both displayed positive-part Jensen gaps are nonnegative. |
| Positive-delta cases | The alternatives `m=u`, `m=delta`, and `m=v` cover the whole maximum, including ties. Every positive-part subcase is covered, and all stated factor signs hold on their stated regions. |
| Equality after the cases | Equality at the auxiliary lower bound for positive delta forces `u=2delta/3`, `v=delta`, then `p_i=0`, `t_i=delta/3`, and `c=d=v=delta`. These tuples have positive `Q` and zero `V`. |

In addition to reading the sparse-polynomial checker, the auditor independently verified ten central identities by exact rational quadratic interpolation: the negative shift, the positive-delta expansion, its scalar `H`, and all the maximum/positive-part identities. For a polynomial known to have total degree at most two, its values at `0`, `+e_i`, `-e_i`, and `e_i+e_j` determine every coefficient. All these identities agreed at the determining nodes. This is a coefficient check, not random or numerical sampling.

The final comparison is

`Q - V/48 >= sum_{i<j} (p_i+t_i)(p_j+t_j)/24 + delta^2/8`.

With `V>0`, equality forces `delta=0`, at most one nonzero pair sum, `p=t`, and `v=0`. The positive pair sum makes `A>0`, hence `c=0`. Thus the complete equality family is, up to index permutation,

`c=delta=v=0, p=t=(a,0,0), a>0, d>=2a`.

The source constraints give `w=d/2-a>=0`, and direct evaluation gives `Q=a^2/6`, `V=8a^2`. These tuples establish sharpness on the relaxed domain. When `V=0`, the ratio is undefined; equality in the inequality is correctly classified by `p=t=0`, `delta=v=0`, `c,d>=0`, `cd=0`.

The old `V/144` bound follows from the pinned scalar-sum theorem and the exact nonnegative identity `2(P+T)^2-V=6 sum_{i<j}s_i s_j`. The local proof also checks negative full-slack examples, so it does not accidentally prove a claim about `S` in place of `Q`.

## Original-template application audit

The literal 22 faces and their bit strings were matched to the pinned OpenAI table. No template was varied. The three cuts, six exposure classes, connectedness, degree condition, 33 point pairs, and excess anchors are reconstructed by the checker.

All eight local activity subsets are covered. For three active incidences, the new quadratic bound is combined with the unchanged full linear-loss envelope. For zero, one, or two active incidences, the source floor-gain estimate is retained. Its exact difference from the desired `V_h/48 - sum(h_i)/2` bound is a sum of nonnegative terms. Thus transfer to the new coefficient is justified for each activity case.

The summed matrix retains both terms of the excess `rho_e(h_e^2+h_e)/4`. It is

`K=L_triangle/48+diag(rho)/4`,

so with `d_e=3rho_e`, the correct integer scaling is

`A=48K=L_triangle+4diag(d_e)`.

The certificate has `tau=270558215904`, `AN=tau I`, and `H_num=3716263103433120`. All 1,089 entries of the inverse product and all 33 strict coordinate inequalities passed. With `B=257`, the reduced minimum margins are exactly

```text
44766905118600
1933549752433619726193600
```

These prove every coordinate of the enlarged real ellipsoid is less than 257. Only after this real bound is proved is integrality used to conclude `M<=256`. The old original-template matrix and its 33 strict inequalities also replay successfully, certifying the comparison with `M<=608`, `D=7296`.

The mode-removal argument keeps the exact full slack. Under `D>=12M`, its bracket signs are correct, and the three integer cases `c=0`, `c=1`, and `c>=2` have the stated equality alternatives. The `c=1` alternative propagates through connected face adjacency and contradicts `sum rho=2`. This yields the same integer nonsaving classification at every even `D>=3072`.

The real counterprofile with all pair dimensions one and local `p_i=t_i=1/2` gives `S_j=-1/8` and total `Delta=-7/4`, exactly as stated. It correctly prevents extending the integer classification to all real profiles.

The recovered proof's robust nondirect remainder `1196` is preserved. The disputed per-pattern `189` premise is not imported. At `D=3072`, the retained nondirect saving is `1876`; the other retained requirements, even `D>=12` and odd-prime `q>=16D`, are explicitly recorded. No field or host parameter has been reconstructed.

## Executed checks and mutation controls

The auditor ran all four delivered commands successfully with isolated Python mode and bytecode disabled:

| Command | Observed result |
|---|---|
| `check_variance.py` | 22 source checks, 35 polynomial identities, and 10 rational examples pass; five examples have negative local slack. |
| `test_local_mutations.py` | Baseline passes; all six local mutations are rejected at their intended checks. |
| `check_downstream.py` | 19 identities, eight activity masks, all original-template data checks, 1,089 new and 1,089 old matrix-product entries, and 33 new and 33 old coordinate inequalities pass. |
| `test_downstream_mutations.py` | Both matrix/threshold corruptions are rejected at their intended checks. |

The eight deliberate corruptions are:

1. Replacing `1/48` by `1/47`.
2. Changing the zero-delta squared coefficient from three to two.
3. Changing the positive-delta scalar coefficient from `-42` to `-41`.
4. Reversing the delta coefficient in the full linear loss.
5. Appending bytes to the pinned `tail.tex`.
6. Violating the per-index `v` constraint in a sharpness example.
7. Adding one to an inverse-matrix diagonal entry.
8. Replacing the strict coordinate threshold 257 by one.

All eight cause nonzero verifier exits at the expected mathematical or source-binding check. They are selected failure controls, not a claim that every possible corrupted artifact is detected.

## Limits

The conventional proof supplies the inequality signs and equality implications; the exact checkers certify algebra, source bindings, examples, and the finite matrix data. This is not a proof-assistant formalization. The retained geometric, counting, and transverse analytic inputs were checked for the application interface and dimension thresholds, not rederived as new results.

Correctness of the inequality, sharpness on the relaxed domain, and mathematical novelty are separate claims. The bounded current-work review found no duplicate in its inspected material; this audit does not certify priority or exhaust unpublished work. It also does not establish geometric realizability of the sharp tuples, optimality of the sufficient dimension, a smaller counterexample graph, or an improved complete finite construction.
