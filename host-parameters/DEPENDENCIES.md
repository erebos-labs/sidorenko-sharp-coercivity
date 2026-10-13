# Dimension and fixed-padding dependency ledger

Version 1.0.0. The formulas are not silently reoptimized. See PROOF.md for the conventional transfer and SOURCE_ACCESS.md for access limitations.

## Exact old/new parameters

| Quantity | D=7296, recovered | D=600, audited |
|---|---:|---:|
| Half rank | 3648 | 300 |
| b(D) | 26619456 | 180300 |
| b(r) | 6655776 | 45150 |
| Rank-layer prime floor, not the complete condition | 116736 | 9600 |
| Signed kernel mean exponent | 372672384 | 2524200 |
| Kernel deficit q exponent | 24596377344 | 166597200 |
| Strict q upper-bound exponent F_q | 319820424557970218 | 319820424556679978 |
| Host exponent B in N=2^B | 7866423844799423288734694969 | 53281187287257529723615577 |
| Atom q exponent | 3513768192 | 23799600 |
| Clone log2 upper bound | 1123774834967853447267918484 | 7611598180401195980621428 |
| Coin log2 upper bound | 357564720215858629205464514 | 2421872147123821977688178 |
| Layer-enumeration log2 upper bound | 8513445719422207667361408 | 57663622547569400033400 |

C_D is `2^235520 * 7297^256` versus `2^21248 * 601^256`. J is `66*7297^256*2^53303404092991701` versus `66*601^256*2^53303404092777429`. The complete conditions are odd prime `q>116736+J_old^6` and odd prime `q>9600+J_new^6`, respectively.

Both constructions retain Z=3807386006623258, A0=53303404092753965, Lambda=53303404092753966, epsilon exponent3807386006625439, H_c=66*2^2210, and the same rational score data. The old host exponent is reproduced exactly; the new one is strictly smaller.

## Full ledger

[R] means the pinned v1.4.0 release. [H] means the pinned recovered manuscript. “Reviewed” for retained geometric inputs is an interface/condition audit, not new formal verification.

| Quantity | Formula / bound | Dependence | Source | Audit status and qualification |
|---|---|---|---|---|
| Template | 13 point + 22 face vertices; 66 incidences; 33 point pairs; 28 zero-excess pairs | fixed | [H] §1; [R] certificates | Literal reconstruction and inherited tests rerun. No change of template, cut distribution, or activity convention. |
| Dimension and rank | D=600; r=D/2=300 | new substitution | [R] defect-one/DOWNSTREAM; [H] §2,6 | Exact conditions checked. D even, r>1, r even; no q=1 mod4 requirement. |
| Signed layer normalizer | p_xi=n_xi/q^b(D)=[D choose r]_q q^(b(r)-b(D)) Pr(non-singular r-form of sign xi) | D,r,q | [H] §2.1; OpenAI transverse | Definition, exponent and positivity audited. n_xi is recomputed at the new dimension in the mathematical construction, not copied from D=7296. No layer enumeration run. |
| Symmetric-space size | q^b(D), b(D)=D(D+1)/2 | D,q | [H] §2 | Exact exponents checked. Only b(D), not q^b(D), allocated. |
| Elementary count constants | Gaussian normalized count in[1,2], \|GL_n\|>=q^(n^2)/2; Lagrangian containment <=q^(-Dt+binom(t,2)) | fixed constants; variable exponents | [H] §2; [R] defect-one/PROOF | Inherited elementary count interfaces reviewed. No extra upper containment constant. |
| Triple profile and conditional completion | 128 q^-C; 256 q^(-C+b(h)); 128=4*32 | D in C; fixed padding | [H] §2.3 | Retained orbit interface reviewed. Conditional fresh point remains independent of the complete older sigma-field. |
| Individual orbit lower bound | 2^(-D-15) q^-C; 15=4+5+3+3 | D | [H] §2.3 | Premise/interface audited. Every actual ordered orbit, not profile-averaged probability; residual dimension0 included. |
| Planted numerator | 2^32, 32=2+1+9+17+3 | fixed padding | [H] §3.3 | Arithmetic checked. Common space, center, normalizers, subspaces and correlated-nullity factors retained. |
| Chosen gain g_j | Same maximum over complete necessary integer domain at new D,r; at most(D+1)^5 choices | D,r | [H] §3.1; [R] full-slack/DOWNSTREAM | Domain transfer audited. All per-index t_i,v bounds, integer/parity, w>=0, actual profile h, empty-domain zero, correlated b(v) cost retained. |
| Local gain prefactor A_D | 2^(D+47)(D+1)^5; 47=32+15 | D | [H] §3.3 | Exact arithmetic checked. Applied once per22 faces, not once per incidence or per type-map assignment. |
| Lower activities | 0/1 active: gain0; 2 active: b(floor(h_active_pair/2)); 3 active: selected g_j | D via pair dimension | [H] §3,4; [R] full-slack/DOWNSTREAM | Eight local cases preserved. No substitution of max pair for actual gain except as a justified upper bound in inherited proof. |
| Chart multiplier | 2^35 * 16^66=2^299 | fixed padding; q>=16D | [H] §2.2 | Arithmetic and uniform interface checked. Allows unbounded nonnegative singular integrand; no conditioned independence claim. |
| Transverse inequalities | r>1, D even>=12, max point degree6, q>=16D; n=D-1 and s<=6 | D,r,q | [H] §6; OpenAI transverse | D=600 conditions checked. 1-2D/q>=7/8;1-6D/q>=5/8; s-b(D-1-s)<=-9 at D=600. |
| Transverse padding | F3<=21,F2<=5,common bound128; L1error128Dq^-1/2; 22 face telescope<2^159Dq^-1/2; joint sign model<=2^106Dq^-1/2; total<=2^170Dq^-1/2 | D in factor; fixed powers | [H] §6 | Retained formulas reviewed. 21/5 bounded by128; joint TV2^39D; model8^22=2^66. No new constants optimized. |
| Saving profiles | 2^87(D+1)^55 q^-1/6;87=7+10*8;55=33+22 | D | [H] §7.1 | Included in budget. Saving lattice1/6 from gains and coverages, not denominator of quadratic relaxation. |
| Integer mode removal | M<=50, even D>=12M | D | [R] full-slack/DOWNSTREAM and certificate | M50 inverse/margins rechecked; implication inherited. Real-profile counterexample prevents removing integer premise. |
| Direct residual | 2^56 q^-1 | fixed | [H] §7.3 | Retained. Counts support and basis effects, gain q^(2m) included. |
| Robust residual fallback | 2^63 q^(-D+1196) | D | [H] §7.4 | Preserved, not used at D=600. m<=28, local correction<=468,1196=28^2-56+468; old final evenD>=1198 remains valid. |
| Defect-one residual | 2^118 q^(-D+241) | D | [R] defect-one/PROOF | Pinned exact checker +14mutations rerun. Complete weighted pattern partition before division; remainder241 and support/pattern constants retained. |
| Higher defect residual | 2^63 q^(-2D+1196) | D | [R] defect-one/PROOF | Inherited exact checks rerun. No missing sum over a,k_i; uniform weight bound before enlarging count. |
| Weighted tail envelope | 2^88(D+1)^55 q^-1/6 | D | [R] defect-one/DOWNSTREAM | Absorption checked. 2^118 term absorbed since2^(304-D)<=1; 2^57+2^63<2^64. |
| Full one-coordinate error | 2^170D q^-1/2+2^299 A_D^22 T_D | D | [H] (6.14) | Retained complete interface. Uniform in every activity/sign pattern and both orientations. |
| Post-tail rank coefficient | 2^(22D+1421)(D+1)^165;1421=299+22*47+88;165=22*5+55 | D | [R] defect-one/DOWNSTREAM | Exact identities checked. No extra profile, mask, or maximizing tuple factor. |
| Published C_D | 2^(32D+2048)(D+1)^256 | D | [R] defect-one/DOWNSTREAM; [H](7.10) | Recomputed; formula unchanged. Each two-term rank coefficient<=C_D/2; second ratio2^(10D+626)(D+1)^91, first spare32D+1877. |
| Activation support and signs | 66 coordinates; \|U_e\|4; \|M\|7; \|Gamma\|6;theta1/2;one negative sigma at(0,0) | fixed | [H] §8; OpenAI kernel | Exact support, law and moment checks. Both branch weights1/2; nonincidence empty product1; all probabilities nonnegative and normalized. |
| Activation branch denominator | 512=2^9 | fixed padding | [H] §8,11 | Exact laws and coin budget checked. Includes branch1/2, sign law2^-7, and theta1/2. |
| Label and identity coefficients | M_C=2^2178;2178=66*33;Cid=-4^-66=-2^-132 | fixed padding | [H] §8 | 254first moments,4374overlaps,33 support intersections,66 corner product checked. Number of nonempty labelings bounded by(2^66-1)^33. |
| Refinement scores | 4rounds;range [-666,1188];spread1854;base1856 | fixed padding | [H] §9 | Rebuilt scores; universal square argument audited. 666=13*6^2+22*3^2;1188=66*18;1856=1854+2. |
| Score base and map count | T=2^2459;13^13*22^22<2^147;2459=147+2178+132+2 | fixed padding | [H] §9 | Exact arithmetic and collapsed controls checked. All part maps, not factorial/injective count. No map-count penalty for reverse coefficient or error averages. |
| Shifted score certificate | maxa127937502468,maxb20679552,maxell25601296520,Eid115295183886,Bpin1548347298342 | fixed | [H] §9 | Entire arrays independently generated. Certificate formulas included; scores not D-dependent. |
| Priors and whole-law thinning | pi_i=T^ai/ZI;nu_j=T^bj/ZJ;lambda_ij=T^-ell_ij | fixed before q | [H] §9; OpenAI kernel | Normalization/positivity and moment formula audited. T>=1, all exponents nonnegative; one lambda per source incidence even repeated type pairs. Mix with1, not0. |
| Pinning margin | Z=280+2459Bpin;280=132+147+1;m0=2^-Z | fixed padding | [H] §9 | Checked. Competition<2^-134wid; identity=-2^-132wid; 3/4safety yields stated m0. |
| Dilution and both orientations | epsilon=2^(-Z-2181);2181=2178+3;alpha=m0epsilon^13=2^-A0;A0=14Z+28353 | fixed padding | [H] §10 | Exponent and both-orientation argument audited. 28353=13*2181; intended13active types versus reverse22; epsilon^9 M_C<=m0/8. |
| Unscaled symmetric gap | Gamma=alpha/2=2^-Lambda;Lambda=A0+1 | fixed padding | [H] §10 | Exact error identities checked. a_inf b_inf<=1-7alpha/8; each finite error<=alpha/64; retained gap alpha/2. |
| Tensor error multiplier | H_c=66*2^2210;2210=34*65 | fixed padding | [H] §10 | Checked. 66 coordinate factors each<=2^34 once eta<=1; uniform before normalized average. |
| Complete prime threshold | J=64H_c C_D/alpha;Q0=16D+J^6;q odd prime>Q0 | D | [H] §10 specialized | Recomputed. 64=2^6;floor(q^(1/6))>=J; rank-layer qfloor alone insufficient. |
| Prime existence and dyadic upper bound | Q0>=2^16; q in (Q0,2Q0);J<2^FJ;Fq=6FJ+2 | D via FJ | [H] §13 | Conventional prime lemma and exact padding checked. No specific prime tested. h_D=ceil strict log2(D+1), coefficient66<2^7; outer+2 becauseq<4J^6. |
| Kernel bounds and scaling | W<=q^(7bD);V<=q^(14bD);U=V/q^(14bD);Delta_q=2^-Lambda q^(-924bD) | D | [H] §11 | Positivity, factorization, exponent audited. 924=66*14; K_xi<=q^bD by nonempty layer; crossed product uses disjoint source components. |
| Exact atom and clone denominator | 308q^(132bD) atoms;Mclone=2^(Z+2181)ZI ZJ q^(132bD) | D | [H] §11 | Exact multiplicity identity and small nonzero-diagonal pushforward controls. 308=14*22;132=2*66; inactive samples retainunusedmatrixcoordinates. |
| Exact edge coin denominator | DW=512T^ellmax(n+n-)^7;Dcoin=DW^2q^(14bD) | D,q | [H] §11 | Coefficient/exponent audit. New n_xi required; qcoin upper power42bD=(28+14)bD; two-powerpadding18. |
| Sampling loss | 595/n+66/n=661/n;half-gap n>=1322/Delta_q | fixed padding | [H] §12 | All-map conventional proof and controls. 595=binom35,2;loopedge-densityloss66;repeatedimageedgesonecoin. No injective-only conclusion. |
| Fixed host order and acceptance | B=11+Lambda+924bD Fq;N=2^B;target1024/N; acceptance Npowers97,131 | D | [H] §12,13 specialized | Recomputed old/new checked. 2^11=2048>661+1024;E[deficit]>1387/N;97=132-35,131=132-1. |
| Source-specific selection bounds | Latom=Z+2181+9+2459(maxa+maxb)+132bD Fq;Lcoin=18+4918ellmax+42bD Fq | D | [H] §11 specialized | Exact exponents checked, powers not allocated. 9pays 13*22;4918=2*2459; optional label/coin enumeration mathematically finite only. |

## Scope of replacement

Only the residue/rank-layer admission changes from the recovered Sections 4-7 route to the pinned v1.4.0 route. The old rank-layer interface is not mechanically evaluated outside its old dimension domain; the release supplies the admitted replacement. Sections 8-13 use its complete uniform error envelope, and their D-dependent arithmetic is recomputed above. Gains and normalizers are defined at the new D,r, while template, priors, thinnings, pinning and padding constants remain fixed.

The final construction is conditional on the inherited analytic geometry in the same sense as the release. No new unproved assumption is introduced in the parameter transfer after (RL). No prime was tested, and no theorem-sized object was allocated.
