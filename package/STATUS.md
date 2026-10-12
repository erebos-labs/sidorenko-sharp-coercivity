# Release 1.1.0 status

The bounded theorem remains **PROVED SHARP on the stated real relaxation**:
`Q >= (P^2+T^2+delta^2)/40`. `THEOREM.md` and its full equality classification
are byte-for-byte unchanged from the supplied v1 archive.

For positive denominator, equality is exactly `y>0, delta=-y, d=3y,
p_i=y, t_i=v=0, c>=y`. For zero denominator, `p_i=t_i=v=delta=0`,
`c,d>=0`, `Q=cd/4`, and bound equality is exactly `cd=0`; ratio undefined.

Original contributions use MIT under the Erebos Labs attribution. The copied
OpenAI sections and license retain Apache-2.0. Related source documents and
API snapshots whose redistribution basis was unclear are omitted; exact
public citations and pins remain. AI-assisted development is disclosed in
`ATTRIBUTION.md`, without invented human mathematician authorship.

Release validation verifies required licensing, provenance, unchanged
mathematical payload, and manifest before running the arithmetic checker.
Omission/corruption controls are distinct from the original mathematical
mutation controls. See `VERIFICATION.md` for the reproducible entrypoints.

The original two proof passes and archived historical execution records remain
in the preserved v1 package. A new portable replay validates the final v1.1.0
ZIP; its external receipt is delivered beside that archive.

No mathematical research extension, Lean build, global novelty result,
geometric realizability, smaller counterexample or full construction
improvement is claimed. Release preparation creates no publication,
commit, push, pull request, or external message.
