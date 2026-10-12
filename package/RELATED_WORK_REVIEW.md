# Bounded related-work review

Reviewed on **2026-10-12, through 12:56:38 UTC**. This is a duplicate screen for the exact estimate

\[
Q\ge (P^2+T^2+\delta^2)/40
\]

on the real relaxation `eq:tail-feasible`. It is not a claim to have searched all prior work. The original private archive retained the observed branch pins, PR inventories, selected source-document blob identities, excerpts, search results and limitations. This release excludes those snapshots; `related-references.json` retains exact citation and document pins. No external write, publication, PR or message was made.

## Result of the screen

**No duplicate or equivalent sharp `1/40` theorem was located in the bounded material inspected.** The specifically requested [PR #4](https://github.com/rohanarun/sidorenko-template-refinements/pull/4) does prove the different sharp estimate

\[
Q\ge (P+T)^2/72.
\]

Its complete scalar proof is Section 2, equations (6)–(11), of [global-residual-dimension.md](https://github.com/artuskg/sidorenko-template-refinements/blob/9922b05bf2c3418e1a46378d4ebac60e8a34ce51/global-residual-dimension.md), Git blob `dcc39f4f593460cbad663ab168e1e68bf9c0146d`. It explicitly says that it is a directional bound and does not claim domination of every component of the old coercivity estimate. The checker subtracts exactly `(P+T)**2/72` in its two scalar branches. The present review did not execute that third-party checker or independently validate its later global dimension conclusions.

The absence of the proposed theorem from this material is sufficient to continue the user's bounded investigation; it does **not** establish worldwide mathematical priority or unpublished-work novelty.

## Current repository and PR status

Direct GitHub REST reads through the connector observed:

| Repository/ref | Exact observed commit |
|---|---|
| `openai/math`, current `main` | `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` |
| `rohanarun/sidorenko-template-refinements`, current `main` | `d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d` |
| `artuskg/sidorenko-template-refinements`, current `main` | `d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d` |
| PR #4, `artuskg` head | `9922b05bf2c3418e1a46378d4ebac60e8a34ce51` |
| PR #5, `artuskg` head | `c3088e0bf0d5e694d84e00ff6c9b9e852e32ae97` |
| PR #6, `artuskg` head | `cfc4ecfaffbdfb3f2bb08edcef1a6fe7cbfa40e3` |

The direct all-state PR inventory (page size 100) returned six PRs in the `rohanarun` repository, zero in the `artuskg` fork, and one in `openai/math`. These are observed API snapshots, not a guarantee against future additions.

| Refinement PR | Observed status | Relation to this task |
|---|---|---|
| #1 | Merged | Earlier active-support residual-count estimate, not a scalar `Q` theorem. |
| #2 | Merged | Sequential residual counting; incorporated in the current main proof. |
| #3 | Open | Proposed residual constant 28; its proof file concerns a different counting step. |
| #4 | Open, draft | Sharp `Q >= (P+T)^2/72`; the principal related result. No PR comments were returned. |
| #5 | Open, draft | Correction of #3 across active supports; its proof file concerns that residual step. |
| #6 | Open, draft | Seven-point orbit pinning and a conditional 17-vertex theorem. Its supplied L3 analytic proof retains `1/342`. |

The current main [proof.tex](https://github.com/rohanarun/sidorenko-template-refinements/blob/d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d/proof.tex), blob `66fc5eb655e6471df0c266c986c0ab47d943fe0f`, and README were inspected. The current [PR #3 proof](https://github.com/rohanarun/sidorenko-template-refinements/blob/9aecdfbd987ecda60b7c5e0b382849d67c6bbc2f/proof.tex), blob `860974fe611dea5e00886594f08074c48e231bad`, and [PR #5 proof](https://github.com/artuskg/sidorenko-template-refinements/blob/c3088e0bf0d5e694d84e00ff6c9b9e852e32ae97/proof.tex), blob `a01c8942470b302cfacfc55026e2bf4c267f17a1`, did not present the target scalar estimate.

## Checks against the original formalization and the newer PR #6

The pinned source [Coercivity.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Combinatorics/Sidorenko/Coercivity.lean), blob `41270b3527e8801aba0d4fa803d36e293156d615`, states the source coefficient `1/342` in the real-variable theorem `coercivity`. It retains the additional nonnegative term `(c-|delta|)*(d+3*delta)/12`. At the proposed equality family the factor `d+3*delta` is zero, so that term does not itself supply `1/40`. Its positive/negative scalar lemmas use intermediate denominators 18. No sharp `1/40` theorem was located in that file. No Lean build was run by this review.

The newer [PR #6 L3 analytic proof](https://github.com/artuskg/sidorenko-template-refinements/blob/cfc4ecfaffbdfb3f2bb08edcef1a6fe7cbfa40e3/experiments/t7-orbit/dependencies/l3-template-transfer-proof.md), blob `7c4c0283ff729d91703318829eff64f1cf7fa23a`, has its coercivity argument at equations (7.4)–(7.5). It explicitly proves `Q_0 >= (P^2+T^2+delta^2)/342`, with the same Cauchy-Schwarz and scalar-envelope reductions. Its [tail review](https://github.com/artuskg/sidorenko-template-refinements/blob/cfc4ecfaffbdfb3f2bb08edcef1a6fe7cbfa40e3/experiments/t7-orbit/reviews/l3-tail-review.txt), blob `0b3704e9e92a1a2a629c5e07e123213e24726a35`, explicitly calls `1/342` conservative. The supplied Task 4 and Task 11 orbit-theorem dependencies were also inspected for an alternative scalar result; none was located. These observations do not independently establish the correctness or status of PR #6's separate counterexample claims.

## The two sharp inequalities are quantitatively incomparable

Let

\[
A=(P^2+T^2+\delta^2)/40,\qquad B=(P+T)^2/72.
\]

The exact comparison is

\[
A-B=\frac{4P^2+4T^2-10PT+9\delta^2}{360}.
\]

Its sign changes on the stated real feasible domain.

* In the user's proposed family, `p_i=y`, `t_i=v=0`, `delta=-y`, `d=3y`, `c>=y`, with `y>0`, one has `P=3y,T=0`. Then `A=y^2/4` and `B=y^2/8`. Consequently the `1/72` right side alone supplies only half the target right side there.
* In PR #4's sharpness family, `p_i=t_i=a`, `c=delta=v=0`, `d>=6a`, with `a>0`, one has `P=T=3a`. Then `A=9a^2/20`, whereas `B=a^2/2`. The `1/40` right side alone is smaller there. Feasibility is immediate from `w=d/2-3a>=0`; the exact `Q` equals `a^2/2`.

Thus neither estimate implies the other simply by comparing their denominators under feasibility. Their combination yields the stronger pointwise statement `Q >= max(A,B)` if the proposed theorem is proved. No change of denominator identifies the two sharp constants. This distinction concerns the strength of the stated numerical lower bounds; it is not the vacuous logical observation that two independently true universal statements can both be deduced from a sufficiently complete theory.

## Bounded search and interpretation limits

The connector's PR-search operation returned empty results even for the repository containing the known PR #4. Those negative search results were discarded in favor of direct REST inventories. Code searches used `coercivity`, `tail-scalar-quadratic`, and `1/40` across the three named repositories, with a cap of 30 results; two refinement-only searches used a cap of 20. Code search covers default branches. The broad `coercivity` and `1/40` queries hit their cap and were dominated by unrelated families, so they cannot certify absence. The specific theorem and newer branch sources were read directly at immutable commits instead.

The PR #6 changed-files endpoint returned a full first page of 100 entries. Its complete recursive tree was then inspected (`truncated=false`) to locate relevant analytic material; the entire separate formal corpus was not audited. PR #4's recursive tree was also inspected and its scalar checker read. This review did not search every historical branch, all public forks, outside literature, private work or unpublished work. The justified report is **not located in the inspected material**, never **proved novel**.

## Release 1.1.0 distribution note

The complete related theorem and API snapshots are omitted because a redistribution basis for their document content was not established. Exact public references and the theorem commit/blob/SHA-256 remain in `related-references.json`. The review above records the original bounded inspection; release preparation did not repeat that search or update historical PR states.
