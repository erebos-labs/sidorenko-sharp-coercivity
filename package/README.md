# Erebos Labs: Sidorenko family 161 sharp relaxed coercivity

Version **1.1.0**. The largest constant in `Q >= kappa*(P^2+T^2+delta^2)`
on exactly the real relaxation `eq:tail-feasible` is **kappa=1/40**.
Read `THEOREM.md` for the unchanged conventional proof and full equality
classification. The ratio is undefined when its denominator is zero.

This is AI-assisted mathematical work. `ATTRIBUTION.md` describes the known
GPT-6 Pro supplied-package and Codex review/replay roles. Original contributions
use MIT; the included unmodified OpenAI sources retain Apache-2.0.
See `LICENSE` and `THIRD_PARTY_NOTICES.md`.

## Validate this release

First compare the ZIP against its separately supplied SHA-256. Then extract
into a new directory and run with Python 3.9 or newer:

```sh
python3 -I -B validate_release.py
python3 -I -B test_release_controls.py
python3 -I -B test_mutations.py
```

The release entrypoint first verifies the complete file manifest, required
licenses, attribution and exact source provenance. It only then launches
`checker.py`. An artifact-integrity failure stops before proof checks.
The other commands exercise release omissions/corruptions and the original
two mathematical mutations respectively. They use the standard library
and make no network requests.

The mathematical checker retains 41 exact polynomial identities, 27
nonnegative-coefficient checks, and 19 rational examples. Its source binding
now requires the two essential OpenAI sections and their original license.
The related theorem is citation-only because its redistribution rights were
not established. The direct mathematical command remains available:

```sh
python3 -I -B checker.py
```

Direct checker success does not replace release validation. Manifest/hash
checks establish consistency with the supplied artifact; they do not
authenticate an adversarially replaced checker or grant publication authority.
The manifest excludes only itself and requires exact file coverage. Use
`-I -B` to avoid environment imports and bytecode files inside the release.

## Evidence and boundaries

`VERIFICATION.md` separates artifact integrity from arithmetic proof support.
`provenance.json` records unchanged mathematical payload hashes and source
pins. `related-references.json` preserves exact public related-work references.
`RELATED_WORK_REVIEW.md` records the original bounded review and its limits.
The original `AUDIT.md` is retained as a historical second proof pass.

The earlier sharp `(P+T)^2/72` bound is numerically incomparable. Neither
proof-assistant verification, geometric realizability, worldwide priority,
a smaller counterexample nor improved full construction dimension is claimed.
The universal result rests on the conventional argument, not finite sampling.
