# Sidorenko full-slack package 1.0.1

Package 1.0.1, distributed in repository release v1.3.0. This packaging correction preserves
the mathematical/historical documents and source snapshots of handoff 1.0.0
byte for byte. See `PACKAGING.md` for the exact distribution changes.
New original contributions use the package-root MIT `LICENSE`; third-party
licenses and notices remain in `THIRD_PARTY_NOTICES.md` and `sources/`.

A bounded, unpublished follow-up to Erebos Labs' published v1.2.0, pinned to
`1b6abc821b7fb95cc0ca71ba804e0c4ae19df4e4`.

## Results

On exactly the published relaxed real domain, the optimal additive constant is

    S >= V/48 - (3c+P+T)/12 - 17/16.

The coefficient 1/12 cannot be made smaller with any finite additive
constant. Equality in the displayed bound occurs exactly at

    c=d=delta=v=5/2, p_i=0, t_i=1/2 for i=1,2,3.

It has V=0. A supplied positive-V family approaches the same infimum.

On the unchanged original template, retaining all source analytic inputs:

    M <= 50;
    integer mode removal at even D >= 600;
    sufficient even D >= 1198 with the recovered residual constant 1196.

600 is not a sufficient final dimension under those retained inputs.
The previous 1/40 theorem, sharp Q>=V/48 result, M<=256 and D>=3072 are
preserved as inherited statements, not claimed as new here.

## Read and replay

Read `THEOREM.md` for the self-contained all-real proof and full equality
analysis; `DOWNSTREAM.md` for the complete conditional premises and exact
original-template calculation. `AUDIT.md`, `RELATED_WORK.md` and `STATUS.md`
separate correctness, finite checking, inheritance, and limitations.

Run from any working directory with Python 3.9 or newer:

```sh
python3 -I -B /path/to/sidorenko_full_slack_v1.0.1/verify_package.py
```

This verifies the manifest, the new proof identities and examples, both
published source bindings and matrix data, twelve targeted corruptions,
and a separate exact Gaussian-elimination/slack-formula audit. It performs
no network requests, installations, template search, or finite-field/host
construction. Successful JSON outputs are compared with the included logs.
The verifier also runs eighteen packaging rejection controls and a clean
inventory positive control. Duplicate manifest entries and any unlisted
regular files are rejected, including files named nested `SHA256SUMS` or
located under `__pycache__`. Only the one root manifest excludes itself.

The individual commands are:

```sh
python3 -I -B checker.py
python3 -I -B test_mutations.py
python3 -I -B audit_exact.py
python3 -I -B test_packaging.py
```

The new handoff's replay is offline and self-contained. This is **not** a
claim that the upstream v1.2.0 repository's entire historical verifier has
been replayed here. That separate upstream workflow needs external files.
Those unclear-license refinement snapshots are not bundled. Their retained
analytic interface is listed explicitly in `DOWNSTREAM.md` and `SOURCES.json`.

## Contents and provenance

`certificates/local.json` records the new sharp constant and witness.
`certificates/original.json` contains the complete unchanged inverse and
new linear vector, constant, coordinate margins, and dimension gates.
`examples.json` contains exact rational boundary/equality/regression tuples.
`logs/` contains historical handoff 1.0.0 stdout/stderr and execution receipts.
`release-prep/` contains actual replay outputs and receipts for the audited packaging candidate;
the final package replay is recorded in the release receipt.
The internal `SHA256SUMS` lists every package file except itself.

The three required published variance files are exact Git-blob-matched
copies. Source text was read using the connected GitHub reader. Their local
bytes were recovered from the prior conversation archive, with the exact
published packaging note restored for the two Markdown files, and then
checked against the live pinned Git blob IDs. No mathematical definition was
reconstructed from memory. OpenAI source copies match their immutable blobs.
The source-binding receipt explains this path rather than claiming that a
raw HTTPS download succeeded.

No publication or external communication was performed. The local proof is
conventional mathematics supported by exact arithmetic, not a Lean proof.
The audit is same-session AI work with a separate arithmetic implementation,
not independent human acceptance. Local relaxed sharpness does not imply
geometric realization or optimal dimension. No complete smaller counterexample
or recalculated finite host is claimed.
