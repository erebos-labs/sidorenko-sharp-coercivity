# Sharp integer full-slack constant

On the **integer points of the unchanged feasible domain**, the sharp additive
constant in Erebos Labs' full-slack inequality is **1**, improving the real-domain
constant \(17/16\):

\[
S \ge V/48-(3c+P+T)/12-1.
\]

The [written proof](PROOF.md) retains a dispersion term from the predecessor
proof and uses the rational lattice of the remaining expression. Two feasible
integer tuples attain equality. No geometric realization is needed for this
local algebraic theorem, and no exhaustive equality classification is claimed.

For the pinned conditional graph-profile application, the improved constant
gives **\(M\le49\)** in place of \(M\le50\), and moves the mode-removal interface
from even \(D\ge600\) to even \(D\ge588\). The higher-defect residual estimate
still requires **even \(D\ge600\)** for the complete rank-layer argument. The
published host and its inherited analytic assumptions are unchanged.

## Reproduce

Python 3.9 or later, standard library only. From this directory:

```sh
python -I -B check.py
python -B -m unittest discover -s . -p 'test_*.py'
```

The first command emits the deterministic [evidence record](evidence.json):

- 9 source files checked by SHA256, byte count, and Git blob identity.
- 37 polynomial identities checked at 1,166 exact interpolation nodes.
- All 1,089 entries of the reconstructed matrix/inverse product and all
  33 coordinate inequalities verified. The new \(\Psi\) is
  `167611112777076`; the smallest squared \(B=50\) margin is
  `194226871915968682337664`, strictly positive.
- 358,488 admissible integer profiles in a declared finite boundary grid,
  with minimum remainder \(-1\).
- 10 deliberate false-claim or altered-arithmetic controls rejected.

The second command runs 11 unit/integration tests, including altered source
bytes, matrix and bit data, individual domain constraints, exact-input
enforcement, and the real equality tuple that violates the new integer bound.
Failure checks use explicit exceptions and remain active under optimized
Python. The upstream repository's older checkers may separately forbid `-O`.

Each identity tested by interpolation has total degree at most two after its
positive-part branches are made explicit. The nodes \(0,\pm e_i,e_i+e_j\)
determine every coefficient. This is exact polynomial verification, not a
probabilistic identity test. Degree, sign, and branch-coverage arguments are
explained in the written proof and its pinned predecessor; this is not a
proof-assistant formalization.

The finite grid uses \(0\le p_i,t_i\le3\), \(-3\le\delta\le5\), all admissible
integer \(v\), \(c=|\delta|+\{0,1\}\), and
\(d=\max(P+T,3\delta+2P-2v)+\{0,1\}\).
It is exhaustive only on that domain, uses no randomness, and stops when that
domain is complete. The unbounded theorem follows from the written proof.

## Scope and predecessors

The source is
[erebos-labs/sidorenko-sharp-coercivity](https://github.com/erebos-labs/sidorenko-sharp-coercivity)
at `64f9ebf631c568c86adfdd3e1b6d8249cca00d8d`. Exact file pins are in
[source-pins.json](source-pins.json). The immutable copies include:

- The real theorem and its full-slack application, which retain the older
  unsplit residual threshold \(1198\).
- The later defect-one application, which supplies the updated threshold
  \(600\).
- The original matrix certificate, reused without altering its entries.

Credit Erebos Labs' AI-assisted real proof, its dispersion identity and
certificates, the preceding refinement contributors identified in those
sources, and the OpenAI manuscript underlying the graph template. Our
contribution is the integer gap argument, its conditional coordinate
consequence, and a separate exact checker using interpolation. Global
mathematical priority has not been established.

Alexander Richard Towell is the contributor, with **substantial OpenAI Codex
assistance** in derivation, implementation, verification, and writing. One
separately tasked AI reviewer checked the mathematical claim and the core
checker and found no blocking issue; the [review record](REVIEW.md) states its
scope. This is not human peer review.

Original files in this packet use [MIT](LICENSE). Copied Erebos files retain
[their MIT license](source/LICENSE); OpenAI material retains
[Apache-2.0](source/OPENAI-LICENSE). Source attribution and notices are preserved.
No unclear-license external manuscript is included.
