# Sidorenko sharp relaxed coercivity

An **Erebos Labs** AI-assisted mathematics project with three sharp bounds on
the original necessary real relaxation of the pinned OpenAI source:

| Quadratic denominator | Sharp coefficient | Proof |
|---|---:|---|
| N = P^2 + T^2 + delta^2 | 1/40 | [Original theorem](package/THEOREM.md) |
| V = sum over i<j of ((p_i+t_i)-(p_j+t_j))^2 | 1/48 | [Variance theorem](variance/THEOREM.md) |

These have different denominators. The original 1/40 result and its
[v1.1.0 release](https://github.com/erebos-labs/sidorenko-sharp-coercivity/releases/tag/v1.1.0)
remain unchanged.

The [full-slack theorem](full-slack/THEOREM.md), using the unchanged full
linear loss and exactly the same relaxed real domain, gives

\[
S\ge V/48-(3c+P+T)/12-17/16.
\]

The additive constant 17/16 is sharp at coefficient 1/12, and no finite
constant permits a smaller linear coefficient. Equality is precisely
c=d=delta=v=5/2, all p_i=0, all t_i=1/2, with V=0. The supplied positive-V
family approaches the same infimum.

The [new conditional application](full-slack/DOWNSTREAM.md) keeps the same
35-vertex template and gives M<=50, integer mode removal at even D>=600,
and sufficient **even D>=1198** with the retained residual 1196.
600 is the mode-removal threshold; 1198 clears the retained analytic bound.
All gain domains, integer premises and geometric/probability/transverse
interfaces remain explicit. This is not a complete smaller counterexample.

The [defect-one residual estimate](defect-one/PROOF.md) now gives
`N_1<=2^118 q^(-D+241)` and `N_{>=2}<=2^63 q^(-2D+1196)` on the fixed
template. It counts the complete weighted ordered-basis partition before
dividing by full multiplicity. All geometric support and coefficient
budgets are explicit; enlarged locally isotropic families are not asserted
to be realizable residual profiles.

The [conditional rank-layer consequence](defect-one/DOWNSTREAM.md) admits
**every even D>=600**, with odd prime q>=16D and the unchanged envelope
`C_D=2^(32D+2048)(D+1)^256`. M<=50 and integer mode removal are inherited.
The robust unsplit bound with residual 1196 and even-D>=1198 fallback remain valid. These residual
constants are sufficient bounds, not sharpness or optimal-dimension claims.
That v1.4.0 rank-layer release by itself did not re-specialize the recovered
concrete host construction at D=7296.

The [host-parameter transfer](host-parameters/PROOF.md), published in
[v1.5.0](https://github.com/erebos-labs/sidorenko-sharp-coercivity/releases/tag/v1.5.0),
now completes that specialization at **D=600, r=300 under the retained analytic
inputs**. It establishes existence of a simple host of the sufficient order

~~~text
N = 2^53281187287257529723615577
p(G)^66 - t(H,G) >= 1024/N
~~~

The complete condition is odd prime `q>9600+J^6`, with
`J=66*601^256*2^53303404092777429`; `q>=9600` alone is insufficient.
Both orientations, every type map (including collapsed maps), kernel diagonals,
exact rational cloning and all-map sampling losses are accounted for. The old
D=7296 construction remains valid. This is a smaller certified sufficient host
order under the inherited analytic premises, with a finite deterministic
selection specification. **No enormous graph, prime, field or kernel was
instantiated.** See the [43-entry dependency ledger](host-parameters/DEPENDENCIES.md)
and [independent audit summary](docs/HOST_PUBLICATION_AUDIT.md).

For V>0, equality in Q>=V/48 is exactly, up to permutation,
c=delta=v=0, p=t=(a,0,0), a>0, d>=2a. The stronger auxiliary bound is
Q>=sum_i(p_i+t_i)^2/24+delta^2/8. Full slack S may be negative.

The [conditional application](variance/DOWNSTREAM.md) to the unchanged
35-vertex template gives M<=256 and sufficient **even D>=3072**, retaining
the recovered analytic residual constant 1196. The residue step requires
integer profiles and the inherited geometric/probability/transverse inputs.
This is an analytic sufficient-dimension certificate, not a reconstructed
smaller complete counterexample or an optimal dimension claim.

## Reproduce all five packages

Python 3.9 or newer; standard library only:

~~~sh
python3 -I -B tools/verify_repository.py
~~~

The command first checks the unchanged original package and controls, then
verifies the variance manifest and all 23 immutable source bindings, performs
full mathematical/mutation/independent replay, and requires byte-identical
certificate regeneration. CI runs this on Python 3.9 and 3.14.
It then replays the full-slack package: 46 local and 10 downstream identities,
21 examples, the matrix certificate, 12 mathematical mutation controls and
18 packaging rejection controls. The isolated full-slack replay is also
self-contained offline:

~~~sh
python3 -I -B full-slack/verify_package.py
~~~

It also checks the defect-one package's 25 identities, six source bindings,
geometric and complete weighted-partition controls, 14 mutation rejections
and 18 packaging rejection controls. Its standalone replay is offline:

~~~sh
python3 -I -B defect-one/verify_package.py
~~~

It also replays the corrected host-parameter package's four mathematical
programs byte for byte, with 20 identities, 26 new rejection controls,
14 inherited mutations and 18 packaging rejection controls. Independent
repository controls reconstruct the pinning arrays, test 4,238 type maps
(3,928 collapsed), 32,768 exact activation covariance entries, cloning,
all-map counts, prime-lemma controls and small signed-matrix normalizers.
These bounded tests support separate conventional arguments and do not
replace the inherited analytic premises. Standalone host replay is offline:

~~~sh
python3 -I -B host-parameters/verify_package.py
python3 -I -B tools/test_host_transfer.py
~~~

The unchanged original verifier is replayed on its preceding package scope;
a separate whole-public-tree privacy scan admits only the exact reviewed
historical Pro sandbox receipt and rejects new private paths or credentials.
Downloaded host assets also undergo six corruption/tree-mismatch controls.

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

Repository [v1.3.0](https://github.com/erebos-labs/sidorenko-sharp-coercivity/releases/tag/v1.3.0)
publishes full-slack package **1.0.1** and its checksum/receipt. Repository
and standalone package versions are distinct. The tracked full-slack/ tree
matches that ZIP member for member; v1.2.0 and its variance files remain
unchanged. Use the same downloaded-asset verification with v1.3.0.

Repository [v1.4.0](https://github.com/erebos-labs/sidorenko-sharp-coercivity/releases/tag/v1.4.0)
publishes defect-one standalone package **1.0.1**, its checksum and receipt.
The tracked defect-one/ tree matches its ZIP member for member. All prior
release files and results are preserved; use the same asset-verification
command with a downloaded v1.4.0 release.

Repository [v1.5.0](https://github.com/erebos-labs/sidorenko-sharp-coercivity/releases/tag/v1.5.0)
publishes the **exact approved host package 1.0.1-rc1**, SHA256
`dac74d1f440b520caa6e0f8eb961b92f6006cfe31688df07026896c5022c3083`,
its checksum and portable release receipt. The package retains its reviewed
candidate filename/version; repository v1.5.0 is a separate version.
The tracked host-parameters/ tree matches all 64 ZIP files byte for byte.
Two stale inherited notices were restored to the pinned published bytes;
all mathematics is unchanged. The original historical Pro status files
remain intact; the separate independent evidence records the completed
80,925-byte retained-manuscript hash check. No unclear-license cache is released.

~~~sh
gh release download v1.5.0 --repo erebos-labs/sidorenko-sharp-coercivity --dir release-assets
python3 -I -B tools/verify_repository.py --release-dir release-assets
~~~

~~~sh
gh release download v1.2.0 --repo erebos-labs/sidorenko-sharp-coercivity --dir release-assets
python3 -I -B tools/verify_repository.py --release-dir release-assets
~~~

The verifier also accepts the unchanged v1.1.0 assets, and the original
package remains independently reproducible with
python3 -I -B package/validate_release.py. The frozen original repository
verifier is run by the wrapper on its preceding package scope, with the
separate current-tree privacy check described above. Published-release CI downloads the
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

Novelty/global priority, geometric realization of relaxed extremizers,
optimal M/D or host order, an instantiated enormous counterexample,
independent human acceptance and Lean formalization are not claimed.
The host existence and sufficient-order transfer are conditional on the
retained analytic inputs; the geometric theorems are not newly fully proved
by this parameter audit. This is an independent Erebos Labs project, not
an official OpenAI publication.
