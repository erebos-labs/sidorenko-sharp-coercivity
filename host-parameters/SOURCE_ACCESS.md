# Exact input access and provenance

## Authoritative release

The audit uses v1.4.0, commit
`4844aba6a45ef725e2e15b25f9709640837b32c1` of
`erebos-labs/sidorenko-sharp-coercivity`. All requested essential mathematical
text was accessible. No definition was reconstructed from an inaccessible file.

| Requested input | Actual access in this audit |
|---|---|
| `defect-one/PROOF.md` | Read-only pinned connector response and complete local licensed handoff copy, bound to the published manifest/blob |
| `defect-one/DOWNSTREAM.md` | Complete pinned connector text and locally bound copy |
| `defect-one/STATUS.md` | Complete pinned connector text and locally bound copy |
| `defect-one/SOURCES.json` | Complete pinned connector ledger and locally bound copy |
| `defect-one/certificates/controls.json` | Directory metadata at the pin, complete local JSON, published hash/blob binding, inherited checker replay |
| `defect-one/certificates/proof_coefficients.json` | Same complete JSON and binding/replay |
| `defect-one/certificates/template_and_budget.json` | Same complete JSON and binding/replay; literal template independently rebuilt |
| `full-slack/THEOREM.md` | Pinned connector identity/statement and complete locally bound proof; inherited, not reoptimized |
| `full-slack/DOWNSTREAM.md` | Pinned connector identity/premises and complete locally bound proof |
| `full-slack/certificates/original.json` | Pinned connector blob and complete locally bound JSON; all inverse entries and M<=50 margins independently recalculated |
| `variance/DOWNSTREAM.md` | Pinned connector identity/premises and complete locally bound text |
| `variance/source-pins.json` | Pinned connector ledger; relevant immutable dependency paths followed, not bundled |

Additional release inputs accessed were `defect-one/SHA256SUMS`, the exact
current `defect-one/verify_package.py`, `defect-one/test_packaging.py`, published
MIT license and third-party notices, and the locally bound immutable source
snapshots named in these ledgers. The arithmetic checkers and mutation programs
copied under `inherited/defect-one/` match the current pinned manifest and were
reviewed and rerun. Their outputs match the pinned expectations byte-for-byte.

The exact strict `verify_manifest` function is reused unchanged. The root
`test_packaging.py` is the exact pinned file, SHA256
`2d93696689efc21052eca850a0d017e4cf2bf31c93c6c99284d0d4a5ab488808`.
The complete original verifier is preserved under `sources/pinned-packaging/`;
its SHA256 is
`17268d34b6ad6caad382b8cc9c0969962a8a3582b1eeb880963af4a8dadcccd4`.
Only the root verifier's orchestration paths and scope text are modified.

## Retained concrete manuscript

Accessed through the read-only GitHub connector:

```
artuskg/sidorenko-template-refinements
commit 06acd4cf46bfe9086f9abc7d85b5c9f171480143
experiments/original-effective-host/recovered/PROOF.md
```

The complete relevant text was retrieved in overlapping ranges covering
Sections 1-13 and the source ledger. Sections 8-13 were audited for transfer;
the needed definitions, conditional counts, gain choices and error interfaces
in Sections 1-7 were read and checked for dimensional restrictions.
The accompanying `recovered/source-pins.json` was also read. The directory
metadata reports 80,925 bytes and Git blob
`e5f1aaef9c3020054f0221a5b5dedc8260d5d5e4`, matching the user and published ledger.

The expected whole-file SHA256 is
`20c917f8fbab9cc51a92d0a4c853ca2080541a9a15c116bd3343150993aaf031`.
**An independent local recomputation of that whole-file SHA256 was NOT_RUN.**
The connector supplied readable text and metadata, but an exact raw whole-file
copy was not obtained in the container. The digest is identified as an expected
published binding, not as a newly measured one. This is a byte-provenance
limitation, not missing mathematical text or an inferred missing lemma.

The manuscript is not redistributed because its redistribution permission was
not established. `check_external_source.py /path/to/PROOF.md` optionally checks
length, SHA256 and Git blob on an independently supplied file. Its wrong-length
and equal-length corruption controls were run. Its positive whole-file check
was not run. No external source program was executed.

## Primary OpenAI dependencies

All at `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, under
`preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/`:

| File | Git blob | Access |
|---|---|---|
| `complex.tex` | `178b0e9da21867a727ea847dae8e537b9d719a70` | Exact licensed local bytes; source table parsed and checked |
| `tail.tex` | `dc11e07a592e70d3a13e3a005c72378c88edc351` | Exact licensed local bytes; relevant feasibility/slack/gain interfaces retained |
| `planted.tex` | `e1a4636e66361dae0f5918e1245950060535a83c` | Exact licensed local bytes; necessary domain, quotient/difference law and chosen gains reviewed |
| `kernel.tex` | `bbe11be8fffe968012060ec43e6aff597e922831` | Full pinned connector response; expansion, repeated maps, pinning, thinning and crossed-product interfaces reviewed |
| `transverse.tex` | `d4991976e630f117c8d85a7e22deb60643a2450d` | Full pinned connector response; signs, normalizers and restriction/interface conditions reviewed |
| `orbits.tex` | `7da7ee247b4be60c3baf545a2e0f78309a667ee0` | Full pinned connector response; containment, chart and individual-orbit interfaces reviewed |

The last three were not materialized as exact local raw files, and no new local
SHA256 computation is claimed for them. The copied OpenAI files retain their
Apache-2.0 license. The full mathematical source lists, expected bindings and
actual access descriptions are in `SOURCE_ACCESS.json`.

## Deliberate exclusions

Comparator Lean challenge stubs, the full Lean solution closure, unrelated
campaign branches, older residual-189 code, template search programs, and the
recovered enormous generator were not needed as transfer premises and were not
run. The underlying recovered geometric statements are retained analytic inputs,
not certified by the finite arithmetic checker. The new proof explicitly proves
the host transfer from the admitted uniform rank-layer interface.

No complete upstream repository verifier or CI job is reported as rerun. The
`inherited/` directory is a documented, licensed subset for this audit and its
specified arithmetic replay, not an exact full repository export. Every member
of the handoff, including this subset and nested source files, is covered by the
root strict manifest; no cache or nested manifest is exempted from inventory.
