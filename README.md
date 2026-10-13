# Sidorenko sharp relaxed coercivity

An **Erebos Labs** AI-assisted mathematics project with two sharp bounds on
the original necessary real relaxation of the pinned OpenAI source:

| Quadratic denominator | Sharp coefficient | Proof |
|---|---:|---|
| N = P^2 + T^2 + delta^2 | 1/40 | [Original theorem](package/THEOREM.md) |
| V = sum over i<j of ((p_i+t_i)-(p_j+t_j))^2 | 1/48 | [Variance theorem](variance/THEOREM.md) |

These have different denominators. The original 1/40 result and its
[v1.1.0 release](https://github.com/erebos-labs/sidorenko-sharp-coercivity/releases/tag/v1.1.0)
remain unchanged.

For V>0, equality in Q>=V/48 is exactly, up to permutation,
c=delta=v=0, p=t=(a,0,0), a>0, d>=2a. The stronger auxiliary bound is
Q>=sum_i(p_i+t_i)^2/24+delta^2/8. Full slack S may be negative.

The [conditional application](variance/DOWNSTREAM.md) to the unchanged
35-vertex template gives M<=256 and sufficient **even D>=3072**, retaining
the recovered analytic residual constant 1196. The residue step requires
integer profiles and the inherited geometric/probability/transverse inputs.
This is an analytic sufficient-dimension certificate, not a reconstructed
smaller complete counterexample or an optimal dimension claim.

## Reproduce both results

Python 3.9 or newer; standard library only:

~~~sh
python3 -I -B tools/verify_repository.py
~~~

The command first checks the unchanged original package and controls, then
verifies the variance manifest and all 23 immutable source bindings, performs
full mathematical/mutation/independent replay, and requires byte-identical
certificate regeneration. CI runs this on Python 3.9 and 3.14.

**Full variance replay requires 18 external files.** The repository and ZIP
are not a self-contained offline full replay. They omit refinement snapshots
without verified redistribution permission and preserve their precise pinned
references. The default repository command retrieves those public files into
a disposable cache, checks byte count/SHA256/Git blob, and treats them as data.
No fetched program is executed. A cold cache needs working public HTTPS.

For offline reuse of a separately verified cache:

~~~sh
python3 -I -B variance/fetch_sources.py --cache ../sidorenko-variance-source-cache
python3 -I -B tools/verify_repository.py --source-cache ../sidorenko-variance-source-cache
~~~

The cache must stay outside the repository; do not redistribute it.
[Distribution scope](variance/distribution.json) and
[dependencies](variance/DEPENDENCIES.md) explain the retained premises.
Inventory-only checks report arithmetic NOT_RUN:

~~~sh
python3 -I -B variance/verify_package.py --inventory-only
~~~

## Releases and downloaded assets

Repository [v1.2.0](https://github.com/erebos-labs/sidorenko-sharp-coercivity/releases/tag/v1.2.0)
publishes reviewed variance package 1.0.1, its checksum and portable receipt.
The tracked variance/ tree matches that ZIP member for member. Release ZIPs
are assets, not Git blobs.

~~~sh
gh release download v1.2.0 --repo erebos-labs/sidorenko-sharp-coercivity --dir release-assets
python3 -I -B tools/verify_repository.py --release-dir release-assets
~~~

The verifier also accepts the unchanged v1.1.0 assets, and the original
package remains independently reproducible with
python3 -I -B tools/verify_coercivity.py. Published-release CI downloads the
actual assets and verifies their hashes, metadata and complete ZIP/tree match
after full replay on the release commit.

## Credit, licenses and limits

Pro supplied the original AI-assisted proofs and certificates. Codex
independently inspected/replayed the mathematics and prepared the releases.
No named human discovery or independent human acceptance is claimed.
See [variance attribution](variance/ATTRIBUTION.md) and the unchanged
[original attribution](package/ATTRIBUTION.md).

Original contributions use [MIT](LICENSE). Exact copied OpenAI sources retain
Apache-2.0 and source credit. Related unclear-license documents are references
only; the source cache is excluded from releases. See
[third-party notices](THIRD_PARTY_NOTICES.md) and the package notices.

Novelty/global priority, geometric realization, optimal M/D, a smaller
complete counterexample, recalculated finite host and Lean formalization
are not claimed. This is an independent Erebos Labs project, not an official
OpenAI publication.
