# Family 161: sharp variance coercivity

**Package 1.0.1 — packaging revision of mathematical version 1.0.0, published with repository v1.2.0.**

The sharp relaxed-real-domain bound is
`Q >= (1/48) sum_{i<j} ((p_i+t_i)-(p_j+t_j))^2`.
For positive variance, equality is exactly, up to permutation,
`c=delta=v=0, p=t=(a,0,0), a>0, d>=2a`.
The stronger auxiliary bound and all zero-variance cases are proved in THEOREM.md.
The full slack S may be negative.

The conditional application to the **unchanged original 35-vertex template**
certifies `M<=256` and sufficient **even `D>=3072`**, retaining the recovered
analytic residual constant 1196. It inherits the stated integer-profile,
geometric, probability and transverse inputs; it does not reconstruct a
finite host or establish an optimal dimension.

## Distribution and replay boundary

This archive is **not a self-contained offline full replay**. Five licensed
source files are included. Eighteen refinement snapshots without verified
redistribution permission are replaced by immutable references. Their exact
commit, path, byte length, SHA-256 and Git blob bindings remain in
source-pins.json and distribution.json. No covering license is invented for
them. The historical GitHub API/PR inventory is also omitted.

Requires Python 3.9 or newer and its standard library. From this directory:

~~~sh
python3 -I -B verify_package.py --inventory-only
python3 -I -B fetch_sources.py --cache ../sidorenko-variance-source-cache
python3 -I -B verify_package.py --source-cache ../sidorenko-variance-source-cache --regenerate
python3 -I -B test_release.py --source-cache ../sidorenko-variance-source-cache
~~~

The first command checks only the public inventory, licensed sources and
omission policy. It returns INVENTORY_ONLY_PASS with arithmetic NOT_RUN.
Full replay without a cache fails explicitly. It never substitutes an
inventory check for a mathematical pass.

fetch_sources.py performs public HTTPS reads at immutable commits, with no
authentication headers or fetched-code execution. It validates bytes,
SHA-256 and Git blob SHA-1 before writing a separate cache. A valid cache
may be reused offline. Missing, corrupted or symlink source entries are
rejected. Do not include that cache in a redistributed archive; retrieval
does not grant redistribution permission.

verify_package.py makes no network request. It verifies all 23 original
source bindings, creates a disposable overlay and runs the four original
arithmetic/mutation programs unchanged, plus two independent exact checks.
--regenerate also runs the unchanged generator in that overlay and requires
byte-identical certificate output. The release directory stays unchanged.
Original direct checker/generator commands in historical documents assume
the complete source overlay; use the wrapper for this distribution.

## Contents and attribution

- THEOREM.md and DOWNSTREAM.md: unchanged mathematical argument, with a packaging notice.
- AUDIT.md and RELATED_WORK_REVIEW.md: historical 2026-10-12 records, not a new priority claim.
- VERIFICATION.md and verification/: current release checks and receipts.
- historical/: original execution records, preserved as historical evidence.
- independent/: independently written exact corroboration programs.
- distribution.json, source-pins.json and DEPENDENCIES.md: distribution scope and inherited inputs.
- LICENSE, ATTRIBUTION.md and THIRD_PARTY_NOTICES.md: contribution and third-party scope.
- SHA256SUMS: exact public file inventory.

The supplied Pro proof, original arithmetic certificates and historical audit
remain credited. Codex performed independent AI review and this packaging
revision. No independent human acceptance, official OpenAI endorsement or
proof-assistant formalization is claimed.

Novelty is unverified. This release establishes no geometrically realizable
extremizer, smaller complete counterexample, optimal M or D, or Lean proof.
No host, field or graph-size calculation is part of the revised claim.
