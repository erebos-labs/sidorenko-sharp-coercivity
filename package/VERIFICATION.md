# Release verification: artifact integrity and arithmetic support

Python 3.9 or newer, standard library only. Run from any working directory
using the extracted script paths; none of the checks make network requests.

```sh
python3 -I -B validate_release.py
python3 -I -B test_release_controls.py
python3 -I -B test_mutations.py
```

## Artifact-integrity phase

`validate_release.py` first refuses optimized execution and rejects symlinks,
nonregular entries, malformed or incomplete manifests, missing required
files, digest changes, incorrect licensing/attribution metadata, source-pin
changes, and changes to the frozen mathematical payload. It binds all three
required OpenAI files including the original license. The related theorem
is an exact citation/pin, not a bundled third-party document.

Only after this phase prints `PASS artifact integrity` does the entrypoint
launch the separately manifest-checked mathematical checker. A nonzero
checker exit remains a nonzero release-validation exit. The manifest is
not a signature: compare the external ZIP hash to the trusted delivery.
Editing the entire checker/manifest together is outside this consistency gate.

`test_release_controls.py` clones disposable copies, omits or corrupts required
licenses/provenance/manifest, and requires rejection before mathematical
output. It also refreshes manifest hashes for targeted semantic corruptions
to test the independent provenance checks. Original files remain unchanged.

## Mathematical-check phase

The original exact arithmetic checks remain 41 polynomial identities, 27
nonnegative-coefficient checks, and 19 feasible rational examples, including
three positive-denominator equality and three zero-denominator cases.
Source binding now covers three indispensable OpenAI files.

`test_mutations.py` is unchanged. It requires the legitimate certificate to
pass and rejects endpoint numerator 115 -> 116 at the plus-breakpoint identity
with residual `-P^2/1620`, and kappa 1/40 -> 1/39 at the sharpness identity
with residual `-y^2/156`. These mathematical tests intentionally pass mutated
certificate paths to the direct checker; the release manifest is a separate
artifact-consistency test.

The theorem, certificates, examples and mathematical functions are preserved.
The universal sign/equality arguments are conventional mathematics; the
Python program is not a proof assistant or a proof by finite enumeration.

## Fresh final evidence

Release preparation runs the affected licensing/provenance controls, both
original mathematical mutations, and a fresh replay from the completed ZIP
in an unrelated working directory. The external release receipt records
the actual interpreter, commands, return codes, output hashes, archive hash,
and privacy scan. External evidence avoids a manifest/receipt hash cycle.
Historical v1 records are preserved in the original private archive rather
than presented as v1.1.0 execution results.
