# Sidorenko host parameter audit package 1.0.1-rc1

Bounded audit of v1.4.0 at commit `4844aba6a45ef725e2e15b25f9709640837b32c1`.

**Result:** the recovered concrete host construction validly specializes from
D=7296 to D=600,r=300 under the retained analytic inputs. The complete prime
condition is q>9600+J^6 for J=66*601^256*2^53303404092777429. One certified fixed
host order is N=2^B, B=53281187287257529723615577, with all-map deficit >=1024/N.
No theorem-sized object or specific admissible prime was computed.

Start with `PROOF.md`, then `DEPENDENCIES.md`, `SOURCE_ACCESS.md`, and `STATUS.md`.
The complete small numerical data is in `certificates/`. New files use the
published MIT license; third-party notices and licensed inherited proofs remain.
Unclear-license retained sources are immutable references, not redistributed.

## Exact offline replay

Python 3.9 or newer, standard library only:

```sh
python3 -I -B verify_package.py
```

The verifier checks the exact whole-package manifest before running mathematical
subprocesses from an unrelated temporary directory. It then requires byte-identical
new audit/mutation outputs, byte-identical inherited arithmetic/mutation outputs,
and all 18reused pinned packaging controls. It rejects optimized Python and does
not ignore cache directories, extra files, nested manifests or symbolic links.
Do not edit an extracted package in place before replaying its manifest.

Individual checks, which do not replace manifest verification:

```sh
python3 -I -B check_audit.py
python3 -I -B test_rejections.py
python3 -I -B inherited/defect-one/check_exact.py
python3 -I -B inherited/defect-one/test_mutations.py
```

The optional external raw-byte check requires an independently obtained original:

```sh
python3 -I -B check_external_source.py /path/to/retained/PROOF.md
```

That positive raw-byte check was not run in this audit. All necessary mathematical
text was available through the pinned read-only connector. The external source
checker neither fetches nor redistributes the source.

`check_audit.py --emit-certificates` regenerates only the small pinning/parameter
JSON files from the fixed inputs. It does not allocate any huge powers. Its use is
for a working copy, not a way to waive a published manifest or approve a mutation.

## Evidence boundary

See `logs/execution_receipt.json` for actual commands, outputs and an interrupted
attempt followed by a successful retry. `logs/clean_replay.json` records fresh
archive verification. No full upstream repository/CI verifier or recovered host
generator was executed. Exact arithmetic supports the separate conventional
proof and inherited analytic premises, not a formal verification claim.

## Independent packaging correction

This is an unpublished corrected candidate. PACKAGING_CORRECTIONS.md records
the restoration of two exact v1.4.0 notice files and their source bindings;
no mathematical claim, proof, certificate or checker is changed. Original
source-access and execution documents describe the Pro run. The independent
audit completed the optional positive whole-manuscript byte check; its result
is recorded in INDEPENDENT_SOURCE_CHECK.json. The source cache stays external.
