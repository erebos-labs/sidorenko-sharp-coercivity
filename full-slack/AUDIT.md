# Same-session adversarial audit

## Review boundary

This was one bounded derivation followed by an adversarial audit of that
claim and its one conditional application. The audit was conducted in this
session. It is not independent human review or independent-model consensus.
The new `audit_exact.py` is a separate arithmetic implementation and imports
none of the primary checker.

## Mathematical pressure points examined

1. The c coefficient is nonnegative under the original feasible inequalities,
   not an extra constraint. Its zero cases were retained until equality was
   forced. At the unique new equality tuple the coefficient is 1, so c=delta.
2. The flat sharp-variance ray has zero quadratic remainder and zero residual
   linear functional L. It therefore does not destroy finiteness at coefficient
   1/12, but it does destroy it at every smaller coefficient.
3. Nonpositive delta is handled directly, with strict margins relative to C=17/16.
   The negative-delta shift preserves every original inequality, including w.
4. Positive delta is reduced at fixed L only after subtracting V/48. Reducing
   Q alone would not justify this operation. The p-reduction loss includes
   every new cross product and is nonnegative with strictly positive leading
   coefficients.
5. Symmetrization includes the cross products of s_i. Its exact identity pays
   the possible decrease using the 1-Lipschitz absolute-value representation
   of s(q), leaving a positive (5/2) sum of squared deviations. All signs and
   hinge boundary cases are justified without a numerical optimization.
6. The homogeneous certificates cover all maxima and both signs of 3u-2v.
   Ties cause no missing region. No sign of k=4L is assumed in completing
   the final square. Equality is traced through all reductions.
7. The affine minimizer has V=0; the proof never divides by V. The exact
   positive-V perturbation approaches the same infimum. The original negative
   local-slack examples remain negative and feasible.
8. Every lower-activity subset admits the new coefficient 1/12 with no additive
   constant, by the exact comparison (3) in DOWNSTREAM.md. The final all-active
   constant is at most 22*(17/16); it is not multiplied by 33 energy coordinates.
9. K is unchanged, but ell and the radius are not. The calculation retains both
   the excess's linear term and Gamma=187/8. The certificate uses
   Psi=Hnum+12*Gamma*tau, not Hnum alone.
10. Integer mode removal at D>=12M is inherited with all its integer premises.
    It is not asserted on the real domain. The real counterprofile Delta=-7/4
    remains an explicit regression control.
11. D=600 clears mode removal, but fails the retained nondirect count. D=1198
    is the stated sufficient even value because D-1196=2. The older 189 bound
    is not used. No finite-host parameter has been recalculated.

## Separate arithmetic audit

`audit_exact.py` evaluates the full n_i(n_i-1) slack formula independently
of Q minus linear loss. It checks all 21 stored rational examples and 24
fixed mixed hinge/max triples. These finite examples are regression checks,
not evidence extrapolated to the entire domain.

It constructs K directly with Fraction(1,48) face entries and rho/4 anchors,
computes its inverse by exact Gaussian elimination, and checks all 1,089
entries against 48N/tau. It then forms ell=1/6-rho/4 and the direct rational
ellipsoid expression, separately from the integer-scaled primary formula.
All 33 strict B=51 inequalities pass. The exact direct squared-margin minimum
is 5562400696417/33819776988.

## Mutation controls

`test_mutations.py` lowers C to 1; changes the linear coefficient to 1/13;
changes the homogeneous multiplier 17 to 16; violates an individual v bound;
changes the expected full-slack value; corrupts a pinned source byte; drops
the global constant; restores the old linear vector; corrupts an inverse
entry; lowers B to 50; uses D=600 as the final dimension; and replaces 1196
by 189. Each is rejected at its intended named check. The B=50 failure occurs
at coordinate 4. These controls establish detection only for those mutations.

## Implementation correction and execution evidence

The first complete primary arithmetic run reached JSON output but failed to
serialize an exactly integral Fraction margin. Converting that output margin
to an integer fixed this presentation error; no mathematical identity or
certificate value was changed for that correction. The final implementation
also uses explicit Fraction coefficients in generic numerical formula helpers.
The actual final stdout, stderr, commands, input hashes and return codes are
recorded in logs/. No failed run is represented as a successful receipt.

The portable checker is standard-library only. Exploratory coefficient
expansion during derivation used SymPy, but there was no floating-point
optimization or numerical search used to establish the theorem.
