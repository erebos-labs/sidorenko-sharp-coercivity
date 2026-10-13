# Same-session adversarial audit

This is a same-session review of the completed bounded argument, not an
independent human audit or a proof-assistant acceptance.

## Most consequential failure modes checked

**Missing residual gain.** Actual classified profiles have total gain 2m.
The robust count includes +2m; the basis method combines it with -4m from the
full ordered-basis divisor, leaving -2m. The exact identity checker and the
removed-gain mutation guard this interface.

**Illegitimate counting enlargement.** In the robust argument the weight is
first bounded on actual families at fixed support and k, then the family count
is enlarged. For a>=2, one uniform weight bound is used for the entire subset;
there is no unpaid sum over a or the k_i. The old 2^63 coefficient consequently
survives for that subset.

**Per-pattern basis multiplicity.** Every family has G^m bases in the total
partition; it need not have them in one pattern. The exact weighted identity
sums complete patterns before division. The adjacent-plane control has fractions
1/(q+1) and q/(q+1), whose sum is one. The 2304-list test at q=3 and the 26208-base
count at q=13 check this distinction explicitly. A tested mutation replacing
the line-first count by the full count is rejected.

**A false defect-one structural assumption.** The proof does not identify a=1
with a single global linear dependency. The type sum only excludes 011 and
allows 000. The locally isotropic triangle control has a 000 step and a=1,
but it has a forbidden common line on a source face. It checks the enlarged
counting method without being mislabeled an actual residual profile.

**A hidden pi-partition factor.** pi=dim(U_i intersect U_j) varies even when
the binary dimension increments agree. Replacing it uniformly by min(x,y)
before multiplying branching bounds eliminates any need to partition by pi.
Every prefix x,y and terminal k_i is fixed by the type sequence. The complete
pattern count n 2^n pays exactly for the remaining type information.

**Dropped geometric constraints in the wrong direction.** New global vectors
are orthogonal to both endpoint prefixes, including the first vector of their
own plane where applicable. Nondegeneracy gives the correct orthogonal-space
dimension. Dropping global-newness, exactness, independence within a plane, or
remaining orthogonality restrictions only enlarges the allowed choice sets.
The branching bound is applied at valid prefixes, not assumed for artificial
invalid continuations.

**Local versus global isotropy.** Global span isotropy is never required.
Only the endpoint spans must be isotropic for containment in Lagrangians.
All actual point-pair and zero face-common conditions are checked for the
adjacent-plane example. No tuple of integer ranks is declared realizable merely
because it meets the numeric inequalities.

**Unpaid constants at D=600.** The one-sided exceptional prefix contributes up
to 22, the total prefix budget is 468, and the full support/pattern/basis factors
give 2^118. It is not ignored: the exact ratio to 2^56 q^-1 is at most
2^(304-D), hence at most one. The higher-defect exponent is -4 at D=600. The
unchanged 2^88(D+1)^55 tail envelope and C_D=2^(32D+2048)(D+1)^256 are recovered
with their complete coefficient budgets.

**Wrong final threshold or field.** Even D>=600 is required by the inherited
integer mode-removal theorem. The odd-prime inequality q>=16D remains. A
mutation to D=598 and another to the field lower bound are rejected. The
q=13,D=4 geometric control does not meet q>=16D and is explicitly labeled;
the generic formula, not that small test, establishes nonemptiness at D=600.

## Outcome

The audited derivation is internally consistent on its stated domain. The
coefficient 241 follows from a deliberately coarse degree bound, not from the
older 189 estimate. No equality classification or optimality is inferred from
these upper counting envelopes. The actual arithmetic checks and all tested
corruptions pass their intended acceptance criteria; their logs are bundled.
The inherited geometric/transverse proof remains a retained dependency.
