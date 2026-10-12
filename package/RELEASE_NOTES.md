# Release 1.1.0

This release prepares the supplied v1 mathematical package for distribution
under the Erebos Labs project attribution. It does not change the theorem,
equality cases, rational certificate, examples, or reported mathematical
mutation definitions.

The original archive is preserved separately. Its SHA-256 is recorded in
`provenance.json`; the release is a new version and has its own external hash.

Changes:

* Add MIT licensing for original contributions, retain exact OpenAI
  Apache-2.0 copies, and document license scope.
* Disclose AI-assisted development and the known supplied-package/replay roles.
* Omit the unlicensed related document and copied API snapshots. Preserve their
  exact public citation and pins.
* Limit executable source binding to the two essential OpenAI sections and
  their required original license. No mathematical checker function changes.
* Add `validate_release.py` to verify manifest, license and provenance before
  launching the mathematical checker.
* Add `test_release_controls.py` for omission and corruption controls.
* Replace historical execution logs with new release documentation; historical
  originals remain in the original private archive. Fresh release replay
  evidence is supplied separately beside the versioned ZIP.

`THEOREM.md`, `AUDIT.md`, `certificate.json`, `examples.json`,
`test_mutations.py`, and all three OpenAI source/license files are byte-for-byte
unchanged. Their exact retained hashes appear in `provenance.json`.

The two focused mathematical proof passes described in the original are
historical. Release integrity checks and the fresh replay are artifact
verification, not additional proof search. No publication is performed by
these tools.
