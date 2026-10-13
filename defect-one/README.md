# Sidorenko defect-one package 1.0.1

Package 1.0.1, distributed in repository release v1.4.0. The mathematical and historical handoff
documents, certificates, original checker programs and copied sources remain
byte-identical to handoff 1.0.0. See `PACKAGING.md` for the distribution fixes.
New original contributions use the package-root MIT `LICENSE`; third-party
MIT and Apache-2.0 licenses and notices remain unchanged.

A bounded follow-up to `erebos-labs/sidorenko-sharp-coercivity` v1.3.0 at
`8b350971095fda13884ea568d1914c1edd7fc966`.

## Completed result

For the unchanged original template, with the exact geometric residual weights,

    defect a=1:    N_1 <= 2^118 q^(-D+241),
    defect a>=2:   N_2 <= 2^63  q^(-2D+1196).

The first estimate uses a complete weighted partition into ordered-basis type
sequences, with division by |GL_2(q)|^m only after the full partition sum. The
second retains the actual defect in the robust span count. All support sizes
and actual geometric residual families are covered by a larger locally
isotropic family count. Numerical rank tuples are not declared realizable.

At every even D>=600, the two exponent savings are at least 359 and 4. The
larger defect-one prefactor is explicitly absorbed into the unchanged tail
and rank-layer envelopes. Therefore the retained original-template argument
now admits every even D>=600, for odd primes q>=16D.

The sharp 1/40 and 1/48 results, full-slack theorem, M<=50 certificate and
integer mode-removal implication are inherited without modification. The
unsplit robust 1196 estimate and old even D>=1198 fallback remain valid. The
older 189 estimate is not used. No optimal dimension or finite-host consequence
is claimed.

## Replay

Python 3.9 or newer, standard library only, no installation or network needed:

```sh
python3 -I -B verify_package.py
```

Individual checks:

```sh
python3 -I -B check_exact.py
python3 -I -B test_mutations.py
python3 -I -B test_packaging.py
```

The verifier checks the package manifest, runs both programs from an unrelated
working directory, and requires byte-identical output against the actual saved
logs. It creates only temporary local files. Optimized Python is rejected.
It also runs one clean inventory control and eighteen packaging rejection
controls. Unlisted files under `__pycache__` and nested `SHA256SUMS` are
included in the actual inventory and rejected. Only the one root manifest
excludes itself. Duplicate entries, unsafe paths and symbolic links reject.

## Contents and evidence

`PROOF.md` gives the complete new weighted count, all coefficients, and actual
geometric control. `DOWNSTREAM.md` supplies the retained premises and the full
rank-layer coefficient/threshold ledger. `certificates/` contains the fixed
source template, scalar proof data and negative controls. `AUDIT.md` separates
human-readable mathematical review from finite arithmetic. `logs/` records the
historical handoff checks actually executed. `release-prep/` records the fresh
mathematical replay for the audited packaging candidate; final release replay
is recorded in the release receipt. `STATUS.md` and `SOURCES.json`
state the precise inherited mathematical scope.

The finite checks include 25 polynomial identities, all six fixed exposure
orders, the 468 degree budget, arithmetic for all 27 relevant support sizes
(without enumerating supports), two small exact geometric adjacent-plane controls,
a complete 2304-list weighted basis partition, and 14 rejected mutations.
They support the conventional proof, not a proof-assistant formalization.

Six licensed source files are bundled with exact source hashes. The external
residual manuscript is pinned but is not redistributed because its redistribution
license was not established. Its relevant content was read through the GitHub
connector; our new count and all its premises are self-contained in PROOF.md.
The new offline replay does not run an upstream historical verifier.

For optional independent retrieval of the external manuscript into a separate
local file, run `fetch_external_source.py --destination /outside/path/PROOF.md`.
This makes an explicit public read and verifies its pinned Git-blob and SHA-256
hashes. It is optional and is not part of the executed offline replay.

No template search, large field or host construction, publication, external
write or communication, novelty determination, optimality proof, independent
human acceptance, or Lean verification is part of this handoff.
