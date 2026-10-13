# Packaging correction 1.0.1

This package is derived from the unmodified
handoff 1.0.0 ZIP with SHA256
`b6626b2b17fdf46b3bf2773232b243b7054689a77ce148545123a4a6c875fcfb`.

The package-root LICENSE is byte-identical to the MIT License at
`erebos-labs/sidorenko-sharp-coercivity@1b6abc821b7fb95cc0ca71ba804e0c4ae19df4e4`.
It covers our new original contributions. Copied source licenses and all
source bytes remain unchanged, with Apache-2.0 and MIT boundaries retained
in THIRD_PARTY_NOTICES.md. No unclear-license external cache is distributed.

The manifest verifier now rejects duplicate entries, malformed digests or
paths, self-listing, symbolic links, missing/mismatched listed files, and
every unlisted regular file. Its only inventory exclusion is the single
root SHA256SUMS; nested manifests and __pycache__ files are included in the
actual inventory and therefore rejected if unlisted. Empty directories
do not count as files.

test_packaging.py contains one clean positive control and eighteen rejection
controls through the actual CLI. These extend the existing twelve
mathematical/source/data mutation controls without changing them. The normal
verify_package.py replay executes both suites and compares unchanged exact
mathematical program outputs against the historical recorded JSON.

THEOREM.md, DOWNSTREAM.md, AUDIT.md, RELATED_WORK.md, STATUS.md, both
certificates, examples, SOURCES.json, all original checker/audit/mutation
programs, historical program outputs and source copies are byte-identical to handoff
1.0.0. README.md only adds candidate/licensing/replay context and changes
the example directory name. Its mathematical claims are unchanged.

The sharp constant, domain and equality claims remain unchanged. The only
downstream claim remains conditional M<=50, mode removal at even D>=600,
and sufficient even D>=1198 retaining 1196 and the inherited analytic
interfaces. No publication, complete smaller counterexample, geometric
realization, optimal dimension, novelty or Lean verification is claimed.

For public distribution, logs/execution_receipt.json retains historical
times, return codes and hashes, while session-specific absolute program
paths are replaced by package-relative equivalents. The unredacted
original receipt remains preserved in the original archive and audit.
