# Sidorenko sharp relaxed coercivity

An **Erebos Labs** AI-assisted mathematics project. The largest constant in

\[
Q \ge \kappa\,(P^2+T^2+\delta^2)
\]

on precisely the necessary real relaxation `eq:tail-feasible` of the pinned
OpenAI source is **κ = 1/40**. The conventional proof and full equality
classification are in [THEOREM.md](package/THEOREM.md).

For positive denominator, equality is exactly
`y>0, delta=-y, d=3y, p_1=p_2=p_3=y, t_1=t_2=t_3=v=0, c>=y`.
For zero denominator, feasibility gives `p_i=t_i=v=delta=0`, `c,d>=0`,
`Q=cd/4`; bound equality is `cd=0`, and the ratio is undefined.

This result is limited to that real relaxation. Geometric realizability,
worldwide priority, a smaller Sidorenko counterexample, improved full
construction dimension, and proof-assistant verification are not claimed.
The earlier sharp `(P+T)^2/72` estimate is numerically incomparable.

## Reproduce

Python 3.9 or newer; standard library only:

```sh
python3 -I -B tools/verify_repository.py
```

This checks the frozen package and release metadata, then runs licensing,
provenance and manifest validation **before** the mathematical checker,
the 26 release controls, and the two original mathematical mutation controls.
The mathematical checker verifies 41 exact polynomial identities,
27 nonnegative-coefficient checks, and 19 rational examples. These finite
checks support the separate conventional proof; they do not replace it.

CI runs the same command on Python 3.9 and 3.14. Published-release events
also download the three release assets and verify their hashes and contents.

## Reviewed release

[v1.1.0 release](https://github.com/erebos-labs/sidorenko-sharp-coercivity/releases/tag/v1.1.0)
contains the unchanged reviewed ZIP, checksum and portable replay receipt.

ZIP SHA-256:
`058997f1e17a6c4298c9b62fd6b3a775f06769497c52f8e47e63288baf01fb60`

The [package directory](package/) matches that ZIP member for member.
Release ZIP bytes are assets rather than Git blobs; the source files and
reproducible checker are tracked here. To verify a downloaded release:

```sh
gh release download v1.1.0 --repo erebos-labs/sidorenko-sharp-coercivity --dir release-assets
python3 -I -B tools/verify_repository.py --release-dir release-assets
```

## Credit and licensing

The original package was supplied through GPT-6 Pro. Codex inspected the
conventional proof and checker, replayed the supplied arithmetic, and prepared
the release and CI. Per-file roles inside the original session are not
separately identified. No named human mathematician authorship or independent
human acceptance is claimed. See [ATTRIBUTION.md](package/ATTRIBUTION.md).

Original contributions are offered under [MIT](LICENSE). The included exact
OpenAI source sections retain Apache-2.0 licensing and credit for the original
construction, definitions, analytic lemmas and scalar reduction. See
[third-party notices](package/THIRD_PARTY_NOTICES.md) and
[source pins](package/source-pins.json).

Related documents with unclear redistribution rights are citation-only;
their exact public references and commit/blob/hash are retained in
[related-references.json](package/related-references.json). This is not an
official OpenAI publication.
