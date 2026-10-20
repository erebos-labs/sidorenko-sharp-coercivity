# Immediate conditional consequence: even D >= 600

Version 1.0.0. Only the defect split and its immediate analytic interface are new.

## 1. Retained prerequisites

Keep the original 35-vertex incidence template, all activity and sign cases,
the original independent point Lagrangians, the complete necessary integer gain
domain (or the original actual union), and the odd-prime condition q>=16D.
The full-slack release pinned in SOURCES.json supplies M<=50 and integer mode
removal once D>=12M. Consequently every nonsaving profile has zero face-common
dimensions, pair dimensions zero or two, zero excess, and total gain 2m for
a selected subset of the 28 zero-excess pairs, at every even D>=600.

Integrality is essential at this inherited step. We do not apply it to arbitrary
real profiles. Lower-activity face gains and equality conditions remain exactly
as published, including each of the eight local activity masks. Empty gain
domains contribute zero. Our residual estimates bound all possible geometric
families for each mask uniformly, so require no new choice of local gain or
simultaneous realization of independently chosen local maximizing tuples.

The existing fixed-template cost estimate and 1/6 strict-saving lattice give

    T_saving <= 2^87 (D+1)^55 q^(-1/6).

The unchanged direct residual count is

    T_direct <= 2^56 q^(-1).

The original robust fallback remains

    T_nondirect <= 2^63 q^(-D+1196).

It still independently certifies the old final threshold even D>=1198. It is
not an assumed proof of the new defect-one estimate. The older 189 estimate
is not imported.

## 2. New defect split with every coefficient paid

PROOF.md gives

    T_defect_one <= 2^118 q^(-D+241),
    T_defect_ge2 <= 2^63 q^(-2D+1196).

Hence the weighted singular tail obeys

    T_D <= 2^87(D+1)^55 q^(-1/6)
           +2^56 q^(-1)
           +2^118 q^(-D+241)
           +2^63 q^(-2D+1196).                            (1)

The gain q^(2m) is already included in each residual term. The local geometric
gain prefactor A_D^22 is NOT included yet; it is applied in Section 3 below.
There is no extra profile count in the residual terms: h_e in {0,2} and c_j=0
make their dimensional profile determined by the chosen support, whose count
has already been included.

At every D>=600,

    D-241 >=359,
    2D-1196 >=4.

The relatively large defect-one prefactor fits without changing the retained
tail envelope. For q>=2 and D>=600,

    [2^118 q^(-D+241)]/[2^56 q^(-1)]
      =2^62 q^(-D+242)
      <=2^(304-D) <=1.                                   (2)

Thus (1) gives

    T_D <= 2^87(D+1)^55 q^(-1/6)+2^57 q^(-1)+2^63 q^(-4)
         <=2^88(D+1)^55 q^(-1/6),                         (3)

because 2^57+2^63<2^64<2^87(D+1)^55. All powers of q in the other terms save
at least 1/6. The stronger retained q>=16D certainly satisfies the q>=2 used
in this elementary absorption. No q-dependent constant has been hidden in C.

## 3. Unchanged rank-layer envelope

Retain source (3.10) and (6.14) at the immutable residual-proof pin:

    A_D=2^(D+47)(D+1)^5,
    |R_D-P| <=2^170 D q^(-1/2)+2^299 A_D^22 T_D.             (4)

The source states this weighted interface for every even D>=12, odd prime
q>=16D, and every activity/sign pattern, before assuming residue classification.
Substituting (3) gives precisely the same coefficient formulas as before:

    |R_D-P| <=2^170 D q^(-1/2)
              +2^(22D+1421)(D+1)^165 q^(-1/6).             (5)

Indeed 299+22*47+88=1421 and 22*5+55=165. Each coefficient is at most half of

    C_D=2^(32D+2048)(D+1)^256.                             (6)

For the second coefficient the quotient by it of C_D/2 is exactly
2^(10D+626)(D+1)^91>=1. For the first coefficient, use (D+1)^256>=D and
32D+1877>=0. Also q^(-1/2)<=q^(-1/6). Thus (5) implies

    |R_D-P| <= C_D q^(-1/6)

for every even D>=600 and odd prime q>=16D. The envelope formula has not been
improved or reoptimized. It is newly admitted at D=600 by the completed residual
count. At that dimension C_D=2^21248 * 601^256; this is symbolic arithmetic,
not an instantiated field or kernel.

## 4. Revised threshold ledger

| Interface | Requirement | At D=600 |
|---|---|---|
| Inherited real full-slack estimate | Published complete relaxed domain | Preserved |
| Inherited global M bound | Original template, nonsaving integer profiles | M<=50 |
| Inherited integer mode removal | D even, D>=12M | Passes at 600 |
| Retained transverse estimate | D even, D>=12; point degree<=6 | Passes |
| Field condition | q odd prime, q>=16D | q>=9600 |
| Saving profiles | 1/6 lattice saving | Unchanged |
| Direct residuals | 2^56 q^-1 | Unchanged |
| New defect-one residuals | 2^118 q^(-D+241) | 2^118 q^-359 |
| Actual-defect robust count, a>=2 | 2^63 q^(-2D+1196) | 2^63 q^-4 |
| Full weighted tail envelope | 2^88(D+1)^55 q^-1/6 | Preserved |
| Full rank-layer envelope | C_D q^-1/6 with (6) | Preserved |
| Old unsplit fallback | even D>=1198 | Remains valid separately |

**New immediate conditional conclusion: every even D>=600 suffices for the
retained original-template rank-layer argument, with the same odd-prime and
analytic inputs.** This is smaller than the previous final 1198 threshold.
The local full-slack theorem and M bound have not changed.

The statement is not an optimal-dimension theorem. We do not recompute the
recovered proof's finite-host parameters, its prime threshold beyond q>=16D,
activation/pinning margins, or any complete smaller counterexample. The task
ends with this defect-one estimate and its rank-layer consequence.
