# Packaging correction 1.0.1

This package corrects distribution issues in handoff
1.0.0, whose original ZIP SHA256 is
`f1d1b459e09dfc5ca2902e0ccb699af971807a6a5bae5d2130429ccec70567dc`.

The root MIT License is byte-identical to the existing Erebos repository's
license at `8b350971095fda13884ea568d1914c1edd7fc966`; it explicitly covers
our new original contributions. Copied MIT/Apache-2.0 source licenses,
attribution, source bytes and immutable pins remain unchanged. No external
unclear-license manuscript or source cache is included.

verify_package.py now checks every regular package file except the single
root SHA256SUMS. It rejects duplicate entries, invalid digests and paths,
self-listing, missing/mismatched files, symbolic links and unexpected files.
There are no basename or cache exclusions: a nested SHA256SUMS or file under
__pycache__ is counted and therefore rejects when unlisted. Empty directories
are not files. The implementation adapts the checked manifest function from
the pinned full-slack package without weakening it.

test_packaging.py runs one clean positive inventory control and eighteen
rejection controls through the actual CLI on disposable copies. These
regressions are integrated into normal verify_package.py replay. The two
original mathematical/mutation programs still must reproduce their historical
stdout and stderr byte for byte; all fourteen original mutation expectations
are unchanged.

Only README.md, THIRD_PARTY_NOTICES.md, verify_package.py and SHA256SUMS are
modified original files. PROOF.md, DOWNSTREAM.md, STATUS.md, AUDIT.md,
SOURCE_ACCESS.md, SOURCES.json, all certificates, original programs, historical
logs and copied sources/licenses remain byte-identical to handoff 1.0.0.
Actual candidate mathematical replay receipts are under release-prep/;
full verification and final ZIP replay are recorded in the preparation sidecar.

The new count and its conditional threshold remain exactly those audited:
N_1<=2^118 q^(-D+241), N_{>=2}<=2^63 q^(-2D+1196), and sufficient even
D>=600 for the retained original-template rank-layer interface. The robust 1196
fallback is retained. This packaging work establishes no new mathematics,
complete smaller counterexample, optimality, novelty, geometric realization,
host parameters or Lean verification. Historical handoff statements describe the original preparation; current
publication metadata is in the release receipt.
