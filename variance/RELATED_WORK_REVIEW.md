> Packaging note for 1.0.1: mathematical/historical text below is unchanged from 1.0.0. Source paths under global, effective-host, and review are external references, not bundled snapshots. See README.md and distribution.json. Historical replay commands require the temporary source overlay; use verify_package.py --source-cache DIR for this release. The historical API review inventory is omitted.

# Bounded related-work review

## Decision

The exact target is the largest real-domain coefficient in

`Q >= kappa V`, where `V = sum_{i<j} ((p_i+t_i)-(p_j+t_j))^2`,

with precisely `eq:tail-feasible` and `eq:tail-quadratic` from the pinned OpenAI source.

No theorem establishing that exact optimum, and no argument asserting the candidate coefficient `1/48` on the full domain, was located in the inspected current material. The duplicate stop condition was therefore not met. This is a bounded non-duplication finding, not a mathematical-priority claim.

The preliminary screen was completed before proceeding with the new derivation. It did not run a proof search, template search, or finite-host reconstruction.

## Live branch and PR inventory

The direct GitHub REST collection endpoints were used rather than relying on keyword-search completeness. Every collection returned fewer than the requested 100 entries, so no further collection page was indicated.

| Repository | Current observed branch heads | Current PR inventory |
|---|---|---|
| `openai/math` | `main=1581d4cbdd69a0faf34b2089614fe2a814316a6a` | Two closed PRs; #1 manuscript synchronization and #2 automatic PR-conversation locking |
| `erebos-labs/sidorenko-sharp-coercivity` | `main=0339f50a039001dc06bd12ffc664ab05a50253fb` | No PRs |
| `rohanarun/sidorenko-template-refinements` | `main=d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d`; `refine/active-support-bound=e68124868f55bba9ed791ff4379c7a42ab48955b`; `refine/defect-overlaps=9aecdfbd987ecda60b7c5e0b382849d67c6bbc2f`; `refine/sequential-basis-count=b513fb4576b30443d0f41df556d378b676723e06` | PRs #1–#7; #1 and #2 merged, #3–#7 open |
| `artuskg/sidorenko-template-refinements` | `main=d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d`; `codex/global-residual-dimension-20261011=9922b05bf2c3418e1a46378d4ebac60e8a34ce51`; `codex/original-effective-host-20261012=06acd4cf46bfe9086f9abc7d85b5c9f171480143`; `codex/support33-correction-20261011=c3088e0bf0d5e694d84e00ff6c9b9e852e32ae97`; `codex/t7-orbit-conditional-20261011=cfc4ecfaffbdfb3f2bb08edcef1a6fe7cbfa40e3` | No PRs into the fork itself |

The only change from the OpenAI pinned commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` to its observed main head is an added workflow for locking PR conversations. The current `tail.tex` has Git blob `dc11e07a592e70d3a13e3a005c72378c88edc351`, identical to the requested pin.

All seven refinement PR titles and bodies were read. Their issue-comment collections were empty. Relevant analytic files were selected from complete recursive Git trees; each retrieved tree reported `truncated=false`.

## Closest results

### PR #4: the existing variance lower bound is 1/144

[PR #4](https://github.com/rohanarun/sidorenko-template-refinements/pull/4) remains at head `9922b05bf2c3418e1a46378d4ebac60e8a34ce51`.

Its [global-residual-dimension.md](https://github.com/artuskg/sidorenko-template-refinements/blob/9922b05bf2c3418e1a46378d4ebac60e8a34ce51/global-residual-dimension.md), §§2–3, proves the sharp scalar-sum estimate `Q >= (P+T)^2/72`, then uses nonnegative `s_i=p_i+t_i` and the exact identity

`2(P+T)^2 - V = 6 sum_{i<j} s_i s_j >= 0`.

These imply `Q >= V/144`. The same section retains the full linear loss `L=c/4+delta/2+(2P-T)/6+v/2`, and derives a local slack estimate rather than assuming every local slack is nonnegative.

Its energy matrix is explicitly `K=L_triangle/144+diag(rho)/4`. The supplied checker and literal templates are in `experiments/global-residual-energy/`. No assertion of an optimal coefficient for `V` or of `Q >= V/48` appears in the inspected theorem or checker.

The PR's current title and body concern sufficient rank-layer dimensions 7296 and 7644 for the original and a separate candidate template. This task considers only the original.

### PR #7: the same 1/144 energy coefficient is retained

[PR #7](https://github.com/rohanarun/sidorenko-template-refinements/pull/7) remains at head `06acd4cf46bfe9086f9abc7d85b5c9f171480143`.

Its [recovered PROOF.md](https://github.com/artuskg/sidorenko-template-refinements/blob/06acd4cf46bfe9086f9abc7d85b5c9f171480143/experiments/original-effective-host/recovered/PROOF.md), §§4.1–4.3, repeats the scalar estimate, the reduction to `V/144`, and the same energy matrix. It gives `M<=608` and `D=7296` for the original template.

The recovered proof is material to this task's downstream scope, but no finite-host reconstruction is required or performed here. Its §5 expressly distinguishes integer dimension tuples from real relaxed tuples. Its §7.5 identifies a per-pattern basis-multiplicity obstruction in the sharper sequential residual draft; its own theorem retains a sufficient residual constant 1196. A downstream specialization should preserve the chosen argument's actual inputs and should not silently import the disputed 189 premise.

### The completed coercivity theorem has a different denominator

The [pinned erebos theorem](https://github.com/erebos-labs/sidorenko-sharp-coercivity/blob/0339f50a039001dc06bd12ffc664ab05a50253fb/package/THEOREM.md) establishes the largest coefficient `1/40` for `N=P^2+T^2+delta^2`, retaining equality through the scalar reductions. It does not state the optimum for the present variance denominator.

The equality examples for that theorem have equal `p_i+t_i`, hence `V=0`. They do not themselves furnish sharpness witnesses for the present positive-variance ratio.

### Other inspected current branches

The main refinement proof, support refinement, sequential refinement, defect-overlap draft, and its support-uniform correction concern residual counting. Their main results do not establish an optimum for this local variance quadratic.

The T7 branch's [L3 analytic proof](https://github.com/artuskg/sidorenko-template-refinements/blob/cfc4ecfaffbdfb3f2bb08edcef1a6fe7cbfa40e3/experiments/t7-orbit/dependencies/l3-template-transfer-proof.md), §7.1, still states and proves `Q_0 >= (P^2+T^2+delta^2)/342`. The branch's top-level theorem and inspected formal remainder-bound file concern stable maps, weighted coefficients, and a different template. They do not provide the requested variance result.

## Review record and limits

`sources/review/current-review.json` records the retrieval timestamp, collection URLs, compact PR snapshots, all observed branch heads, recursive tree inventories, selected analytic documents with Git blob IDs, and the relevant line excerpts. Supplementary inspected analytic source texts are saved in the same directory. The primary requested source files are separately pinned by the main package.

This review did not exhaust every public fork, every unpublished manuscript, all inline review threads, or every unrelated implementation file. It did not infer novelty from an empty keyword search. Current-source correctness, a new proof's relaxed-domain sharpness, and mathematical priority remain separate questions.

