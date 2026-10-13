# Release verification: 1.0.1

Staged replay completed 2026-10-13T00:50:52.578172+00:00. This record was finalized 2026-10-13T00:53:33.190834+00:00.
The corrected release requires a separate 18-file source cache for full replay.
Inventory-only explicitly reports arithmetic NOT_RUN. A cold cache needs public
network access; an already verified cache can be replayed offline. The archive
alone is not a self-contained offline full replay.

## Observed checks

| Check | Actual result |
|---|---|
| Licensed bundled sources | 5 exact length/SHA256/Git-blob checks pass |
| External pinned sources | All 18 freshly retrieved public files match exact length/SHA256/Git blob |
| Full original source coverage | All 23 original checks retained and pass |
| Original local program | 35 identities, 10 rational examples, 5 negative full-slack examples pass |
| Original mutations | All 6 local and 2 downstream corruptions rejected at intended checks |
| Original downstream program | 19 identities, both 1089-entry inverse products, both 33-coordinate strict bounds pass |
| Independent local exact grid | 1,251,801 feasible tuples, 625 scalar boundary points, 24 rational probes pass |
| Independent original-template reconstruction/activity | Both rational matrices match; all 8 masks, 14,757 bounded tests pass |
| Generator in disposable overlay | Passes; original_certificate.json output is byte-identical |
| New packaging/retrieval controls | All 18 controls pass, including expected omission/corruption/path/symlink/ref failures |
| Original arithmetic/data/pin files | All 9 core files are byte-identical to 1.0.0 |
| Original theorem/downstream/review bodies | Preserved byte-for-byte after the explicit packaging notice |
| Python 3.9 grammar | All public scripts pass; actual replay ran on Python 3.14.7 |

The four original program outputs match the independently audited 1.0.0 replay
exactly. Independent programs do not import submitted arithmetic implementations.
No fetched source program is executed. The optional generator and all mutation
controls operate only in disposable temporary directories.

## Execution records and transport limits

verification/staged-full-replay.json preserves the actual staged wrapper result,
including its inventory count at execution. verification/execution-receipts.json
records actual times/exit codes and output hashes. verification/release-controls.json
and cache-hit-fetch.json record the failure controls and reuse of the verified
cache. Public-retrieval.json records the immutable public URLs and byte/hash
verification. Raw source bodies and the source cache are not included here.
The final clean archive is additionally checked in the accompanying release
metadata and local release audit; staged logs are not a claim about a later
uninspected archive.

Actual fresh source retrieval used the permitted read-only public GitHub
connector. A direct fresh-cache stdlib HTTPS attempt in the restricted audit
sandbox failed DNS resolution. Its live CLI download transport is therefore
not claimed to have passed here. The downloader response-validation/write path
was exercised with deterministic transport for all 18 actual pinned payloads,
including rejection of corrupted bytes before writing. Its existing-cache CLI
path passed. Readers need working public HTTPS access for cold-cache retrieval.

An initial packaging control exposed a macOS filesystem-alias
comparison in the new regular-file helper. Normalizing its base resolved that
bug; the same SHA256/symlink controls then passed without weakened assertions.
The failed run is retained in the private release audit. No mathematical check
failed or was waived.

## Evidence boundary

The conventional proofs supply sign and equality reasoning; bounded tests do
not prove claims over all reals. The original historical records are retained
under historical/ and in AUDIT.md. This packaging audit adds no new proof search
or priority claim. Inherited geometry/probability/transverse assumptions remain
conditional, integer mode removal remains integer-only, and 1196 is retained.
No smaller complete counterexample, optimal dimension, geometric realization,
finite host recalculation or Lean formalization is certified. Python 3.9 runtime
was not executed here; grammar and standard-library compatibility were inspected.

## Publication finalization

Package 1.0.1 finalizes only version/status wording from reviewed candidate 1.0.1-rc1 for repository release v1.2.0. All nine original mathematical/program/data/pin files remain unchanged. The real standard-library HTTPS downloader has now retrieved all 18 external files from a fresh cache, with byte-length, SHA256 and Git-blob checks, exit 0 and empty stderr. See verification/publication-live-retrieval.json. The earlier sandbox DNS failure above is a historical staging limitation, not the outcome of this publication retrieval. No downloaded code was executed and no cache is redistributed. Final repository/asset checks are recorded in the accompanying publication metadata and CI.
