# Bounded upstream review, 2026-10-13

The exact target screened was a finite additive remainder for

    S >= V/48 - (3c+P+T)/12 - C,

or equivalently Q-V/48-delta/2-(P-T)/4-v/2 bounded below. This is not the
already established sharp Q>=V/48 theorem or the separate 1/40 theorem.

## Current repository state inspected

The connected GitHub reader returned one branch for
`erebos-labs/sidorenko-sharp-coercivity`: main at
`1b6abc821b7fb95cc0ca71ba804e0c4ae19df4e4`, exactly the requested pin.
Its all-state PR collection was empty. The pinned root README advertises
only the two sharp quadratic bounds and conditional M<=256, D>=3072.
The three required variance files were read and their exact Git blobs bound.
The README blob is `043c33b54178ffc35047bbd9bec70c446fcab8ee`.

The current branch collection for `artuskg/sidorenko-template-refinements`
returned:

| Branch | Head |
|---|---|
| codex/global-residual-dimension-20261011 | 9922b05bf2c3418e1a46378d4ebac60e8a34ce51 |
| codex/original-effective-host-20261012 | 06acd4cf46bfe9086f9abc7d85b5c9f171480143 |
| codex/support33-correction-20261011 | c3088e0bf0d5e694d84e00ff6c9b9e852e32ae97 |
| codex/t7-orbit-conditional-20261011 | cfc4ecfaffbdfb3f2bb08edcef1a6fe7cbfa40e3 |
| main | d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d |

For `rohanarun/sidorenko-template-refinements` it returned:

| Branch | Head |
|---|---|
| main | d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d |
| refine/active-support-bound | e68124868f55bba9ed791ff4379c7a42ab48955b |
| refine/defect-overlaps | 9aecdfbd987ecda60b7c5e0b382849d67c6bbc2f |
| refine/sequential-basis-count | b513fb4576b30443d0f41df556d378b676723e06 |

The joint all-state PR search reported seven items and
`incomplete_results=false`. The relevant current PR4 metadata was separately
read: open/draft, head 9922b05..., giving old global energy at D=7296/7644.
The current PR7 body concerned its separate effective-host theorem at
D=7296 and explicitly retained 1196. PR5 concerned overlap corrections;
PR6 concerned its separate 17-vertex template. No exact additive full-slack
bound was identified in the inspected relevant source text or PR descriptions.
This review did not redo unrelated template searches or audit every branch
file and comment. No claim of exhaustive repository-wide semantic equivalence
or global priority follows from branch names or PR descriptions alone.

## Retrieval record and limitations

Read-only endpoints used included:

- https://api.github.com/repos/erebos-labs/sidorenko-sharp-coercivity/branches?per_page=100
- https://api.github.com/repos/erebos-labs/sidorenko-sharp-coercivity/pulls?state=all&per_page=100
- https://api.github.com/repos/artuskg/sidorenko-template-refinements/branches?per_page=100
- https://api.github.com/repos/rohanarun/sidorenko-template-refinements/branches?per_page=100
- https://api.github.com/search/issues?q=repo%3Arohanarun%2Fsidorenko-template-refinements+repo%3Aartuskg%2Fsidorenko-template-refinements+is%3Apr&per_page=100

GitHub provided the pinned definitions even though direct raw-HTTPS/web
retrieval failed. The runtime copies were recovered and checked against the
published blobs, as documented in README.md and SOURCES.json. A general web
search returned irrelevant Slack-software material; that is not evidence of
mathematical novelty and was not used as such.

Conclusion: no duplicate was identified in this bounded current review.
Correctness and relaxed sharpness are proved separately in THEOREM.md.
Mathematical novelty remains unverified. Nothing was posted or communicated
externally beyond these read-only retrieval requests.
