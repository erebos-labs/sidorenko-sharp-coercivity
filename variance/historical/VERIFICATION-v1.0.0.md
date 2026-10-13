# Verification record

Version 1.0.0; completed 2026-10-12 UTC.

## Result

The local sharp theorem and the conditional original-template certificate are
proved. One derivation pass was followed by one adversarial audit. No unresolved
mathematical step remains within the stated scope.

The exact local result is kappa = 1/48, with all positive-denominator equality
cases and the zero-denominator cases classified in THEOREM.md. The original
template certificate gives M <= 256 and sufficient even D = 3072 while retaining
the recovered proof's residual constant 1196.

## Executed arithmetic

| Check | Final staged result |
|---|---|
| Source identity | 23 files pass byte-length, SHA-256 and Git blob SHA-1 checks |
| Local proof algebra | 35 exact rational polynomial identities pass |
| Local examples | 10 rational feasible tuples pass; 5 have negative full slack S |
| Local mutation controls | 6 of 6 deliberately changed inputs are rejected at their intended checks |
| Downstream proof algebra | 19 exact identities pass |
| Activity coverage | All eight local subsets covered by the proof and checker |
| New original-template inverse | All 1,089 entries of A N = tau I pass |
| New original-template bounds | All 33 strict coordinate certificates pass at B = 257 |
| Old original-template baseline | All 1,089 inverse entries and 33 bounds replay at B = 609 |
| Downstream mutation controls | 2 of 2 matrix/threshold corruptions are rejected |

The local and downstream programs use the Python standard library,
fractions.Fraction, integer arithmetic, and exact sparse polynomial
coefficients. They execute no retrieved source program and make no network
request. The full rational inverse, coordinate margins, coefficients and
examples are included as data.

The independent audit also checked ten central quadratic identities using
exact rational determining nodes. For polynomials of degree at most two,
these nodes determine every coefficient; this is not random sampling.

AUDIT.md records the auditor's initial 22 mathematical/review source entries.
The final package also includes the already pinned original OpenAI LICENSE,
raising the final source count to 23. No mathematical source bytes or proof
claims were changed by that packaging addition.

## Actual execution records

The final four staged commands ran successfully from an unrelated working
directory with isolated Python mode and bytecode disabled. Their actual
stdout, stderr and exit-code receipts are under verification/.

The downstream implementation's earlier successful replay and mutation
records are retained under logs/. The audit is separately recorded in
AUDIT.md. There is no requirement to trust a stored PASS line: verify_package.py
recomputes the package hashes and reruns all four check programs.

## Mutation scope

The controls change the candidate coefficient to 1/47, a zero-delta coefficient,
a positive-delta scalar coefficient, the full-slack delta sign, pinned TeX
bytes, feasibility of a sharpness tuple, an inverse-matrix entry, and the
coordinate threshold. Each is rejected at the expected check.

These are meaningful selected failure controls, not an assertion that every
possible defect is detected. The conventional proof supplies the sign
arguments, complete real-domain case split, and equality implications.
This package is not a proof-assistant formalization.

## Fixed inputs and limitations

All four requested repository pins are listed in source-pins.json.
The current PR/branch review did not locate an exact duplicate; it does not
establish priority. The local theorem makes no realizability claim, and the
downstream integer argument does not apply to arbitrary fractional profiles.

The revised sufficient dimension concerns the original analytic argument
under its retained geometric, counting and transverse inputs. Those inputs
are neither replaced nor presented as newly proved here. In particular,
1196 is retained and the disputed 189 step is unnecessary. No finite-host
construction, new template, graph-size comparison, publication, or PR is part
of the result.

