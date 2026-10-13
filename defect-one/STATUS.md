# Status and inherited/new ledger

Version 1.0.0. The bounded mathematical target is complete.

## Inherited, unchanged

The published release supplies the sharp 1/40 quadratic coercivity theorem,
sharp 1/48 variance theorem, sharp full-slack estimate, M<=50 on nonsaving
integer profiles, and integer mode removal at even D>=600. All selected-gain,
activity, integer/parity and geometric/probability assumptions are retained.
The robust unsplit bound 2^63 q^(-D+1196) and previous final even D>=1198 remain
valid fallback results. The source's direct estimate, 1/6 lattice saving,
transverse input and odd-prime condition q>=16D remain unchanged.

## New conventional proofs

1. Verification of the actual-defect robust exponent
   -Da-k^2+2mk-2m+sum_i binom(k_i,2), including weights and prefactors.
2. Uniform higher-defect contribution at most 2^63 q^(-2D+1196), without a
   missing sum over local rank tuples or defects.
3. A corrected complete weighted basis-pattern count proving
   N_1 <= 2^118 q^(-D+241) over every support and locally isotropic family.
4. Complete absorption of changed prefactors into the existing tail and
   rank-layer envelopes, admitting every even D>=600 for the unchanged template.

## Executed finite evidence

See logs/primary.stdout.json, logs/mutations.stdout.json and execution receipts.
Twenty-five symbolic identities, exact fixed-template checks, geometric and
basis-partition controls, and fourteen deliberate corruptions were checked.
The 2304-list test is a complete finite partition for the one specified two-plane
control, not an enumeration of all residual families. All-support validity is
proved from degree bounds, not extrapolated from tests.

## Limitations

The new remainder 241, coefficient 2^118 and sufficient D=600 are not claimed
sharp or optimal. Actual geometric residual families are a subset of the
locally isotropic plane families counted; rank data alone does not establish
geometric residual realizability. The enlarged triangle control intentionally
violates zero face-common dimension and is not an actual residual witness.

The independent point containment probabilities are used before conditioning
on a profile. The method does not assert independence of conditioned point
Lagrangians or of correlated geometric data. No individual basis pattern is
divided by full multiplicity to bound the number of its represented families.
Only the complete weighted partition identity is used.

The ultimate rank-layer conclusion is conditional on the retained source
geometric and analytic inputs. They are not newly proved by the checker. No
finite-host parameter, prime beyond the stated lower bound, kernel table,
complete smaller counterexample, global novelty, optimal dimension, independent
human acceptance or Lean certification is established. No unresolved new lemma
remains within the stated defect-one count and its immediate conditional
consequence. Work stops here.
