# Independent correction 1.0.1-rc1

This unpublished candidate derives from the preserved host-audit 1.0.0 ZIP,
SHA256 `cb9e0321ce9bbd722553c2c5e08c74a81c07212ca49c6c8f421a6b1e3db93e42`.
No mathematical claim, premise, proof, certificate, checker or rejection
expectation was changed.

Independent comparison with published commit
`4844aba6a45ef725e2e15b25f9709640837b32c1` found that two inherited notice
files contained pre-packaging text, despite being labelled as exact copies
of that commit. Their internal lengths/hashes were self-consistent, so the
original replay passed. Both exact published files are now restored:

- inherited/defect-one/THIRD_PARTY_NOTICES.md;
- inherited/full-slack/THIRD_PARTY_NOTICES.md.

Their length, SHA256 and Git-blob bindings in SOURCE_ACCESS.json were corrected
to the actual pinned objects, with explicit provenance. Root README.md marks
this corrected candidate and distinguishes historical Pro access/status logs
from this independent check. Root SHA256SUMS is regenerated. Source licenses
and notices remain MIT/Apache-2.0 with no reassigned ownership.

INDEPENDENT_SOURCE_CHECK.json records freshly fetched raw source bindings,
including the full 80925-byte retained manuscript's positive SHA256/Git-blob
check. The original status documents and checker output's NOT_RUN describe
the original Pro run; they were not rewritten or made to claim a check they
did not execute. The separate independent auditor did execute the optional
positive byte check. No unclear-license manuscript or source cache is bundled.

The strict manifest function and all 18 packaging rejection controls remain
unchanged from the published implementation. The four mathematical/mutation
programs must still reproduce their original stdout/stderr byte for byte.
The author proof remains conditional on the stated retained analytic inputs.
No large prime, field, kernel or host was materialized and no publication,
commit or push was performed by this correction.
