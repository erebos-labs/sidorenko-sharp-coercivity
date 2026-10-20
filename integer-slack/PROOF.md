# Sharp integer full-slack bound

Alexander Richard Towell, with substantial OpenAI Codex assistance.

This refines Erebos Labs' real full-slack theorem at commit
`64f9ebf631c568c86adfdd3e1b6d8249cca00d8d`. Its algebraic domain and polynomial
are unchanged; only integrality is added. The local theorem below is an
algebraic inequality, independent of the claimed Sidorenko counterexample.
The downstream application retains that project's analytic assumptions.
This is a written proof with exact-arithmetic checks, not a formal proof or
human peer review.

## Statement

Let \(c,d,\delta,v,p_1,p_2,p_3,t_1,t_2,t_3\) be integers. Write
\[
P=\sum_i p_i,\quad T=\sum_i t_i,\quad s_i=p_i+t_i,\quad
w=(d-3\delta)/2-P+v,\quad
V=\sum_{i<j}(s_i-s_j)^2 .
\]
Assume precisely
\[
c\ge|\delta|,\quad d\ge P+T,\quad
p_i,t_i,v\ge0,\quad t_i\le p_i+\delta,\quad
v\le p_i+\delta\ (i=1,2,3),\quad w\ge0.                 \tag{F}
\]
No parity, upper dimension bound, or geometric realization is assumed.
Define the unchanged source polynomials
\[
Q=\frac{c(d+\delta)-\delta d+2\delta^2}{4}
 +\sum_i\left[\frac{(2p_i-t_i)^2}{6}
             +\delta p_i-\frac c6(p_i+t_i)\right]
 +v\left(\frac{d-3\delta}{2}-P\right)+\frac{v^2}{2},
\]
\[
S=Q-\frac c4-\frac\delta2-\frac{2P-T}{6}-\frac v2,\qquad
L=\frac\delta2+\frac{P-T}{4}+\frac v2,\qquad R=Q-V/48-L.
\]
Then the sharp integer inequality is
\[
\boxed{S\ge V/48-(3c+P+T)/12-1.}                       \tag{1}
\]
Equivalently \(R\ge-1\). The additive constant \(1\) is optimal, and the
linear coefficient \(1/12\) cannot be decreased while retaining a finite
additive constant.

## The dispersion term retained from the real proof

The published real proof establishes \(R\ge-17/16\). For \(\delta=0\)
it proves the stronger \(R\ge-1/2\), and for \(\delta<0\) it proves
\(R\ge-9/16\). These sign cases therefore already imply (1).

For \(\delta>0\), put \(q_i=p_i-t_i\) and \(\bar q=(q_1+q_2+q_3)/3\).
Sections 3–5 of the source proof in fact give
\[
R\ \ge\ -17/16+\frac5{48}\sum_i(q_i-\bar q)^2.         \tag{2}
\]
Here is why the extra term survives. First lower \(c\) to \(\delta\);
the loss is nonnegative because its coefficient in \(Q\) is
\((d+\delta)/4-(P+T)/6\ge0\).
At fixed \(q_i,\delta,v,e=d-P-T\), lower each \(p_i\) to
\(\max(0,v-\delta,q_i)\). Equation (14) of the source expresses the loss
in \(24(Q-V/48)\) as a sum of nonnegative terms. These reductions leave
\(L\) fixed. The exact symmetrization identity, source equation (16),
then writes its loss as
\[
\frac52\sum_i(q_i-\bar q)^2+\text{nonnegative terms}.
\]
The other terms are nonnegative by the 1-Lipschitz property of
\(x\mapsto b+|x-b|\), with \(b=(v-\delta)_+\), and convexity of
\((x-b)_+\) and its square. Symmetrization also leaves \(L\) fixed.
The remaining reduction lowers \(e\) to
\((3\bar q+3\delta-2v)_+\), at nonnegative loss \(v(e-e_0)/2\).
Finally source equations (18)–(24) bound the reduced remainder by
\(-17/16\). Dividing the retained symmetrization term by \(24\) proves
(2). None of these reductions is required to preserve integrality;
they are real-variable lower bounds applied to the original integer tuple.

The supporting checker verifies the polynomial identities in these
reductions and all branches of the final homogeneous certificate by exact
quadratic interpolation. The sign and branch-coverage arguments are written
mathematics, not consequences of sampling.

## Integer gap argument

If the integers \(q_i\) are not all equal, then
\[
\sum_i(q_i-\bar q)^2
=\frac13\sum_{i<j}(q_i-q_j)^2\ge\frac23.
\]
At least two pair differences are nonzero integers. Equation (2) gives
\[
R\ge-17/16+5/72=-143/144>-1.                         \tag{3}
\]

If all \(q_i=q\), then \(s_i=2p_i-q\), hence
\[
V=4\sum_{i<j}(p_i-p_j)^2,\qquad V/4\in\mathbb Z.
\]
Directly from the displayed definition, \(12Q\) and \(12L\) are integers.
Consequently \(12R=12Q-V/4-12L\) is an integer. The real bound implies
\(12R\ge-51/4=-12.75\), so \(12R\ge-12\), or \(R\ge-1\).
This completes the proof on the entire unbounded integer domain (F).

Integrality is essential. The source tuple
\(c=d=\delta=v=5/2,\ p_i=0,\ t_i=1/2\) satisfies (F) and has
\(R=-17/16<-1\).

## Sharpness and the linear coefficient

Both integer tuples
\[
(c,d,\delta,v)=(2,2,2,2),\quad p=(0,0,0),\quad t=(0,0,0)
\]
and
\[
(c,d,\delta,v)=(3,3,3,3),\quad p=(0,0,0),\quad t=(1,1,1)
\]
are feasible and have \(R=-1\). Thus the additive constant cannot be
smaller. No exhaustive equality classification is claimed.

For every positive integer \(a\), the source ray
\[
c=\delta=v=0,\quad p=t=(a,0,0),\quad d=2a
\]
is feasible. It has \(Q=a^2/6,\ V=8a^2,\ S=a^2/6-a/6\).
Replacing \(1/12\) by \(\beta\) in (1) would require a finite lower bound on
\(S-V/48+\beta(3c+P+T)=2a(\beta-1/12)\).
For \(\beta<1/12\) this tends to minus infinity along integers, proving
the stated obstruction. This ray and its argument are credited to the
source real theorem.

## Conditional coordinate consequence

For the source's integer profiles, a three-active face now pays constant
\(1\) instead of \(17/16\). The lower-activity bounds are unchanged.
Summing at most 22 three-active faces changes only
\(\Gamma=22(17/16)\) to \(\Gamma=22\) in the source's full-slack
downstream argument:
\[
\Delta\ge h^TKh-\ell^Th-22.
\]
The template, matrix \(K\), linear vector \(\ell\), integer-profile
premises, and all analytic inputs remain unchanged.

Using the pinned matrix certificate \(A=48K,\ AN=\tau I\), let
\[
\tau=270558215904,\quad b=12\ell,\quad u=Nb,\quad
H_{\rm num}=b^TNb=96183743778420,\quad
\Psi=H_{\rm num}+264\tau .
\]
For \(\Delta\le0\) the same completed-square argument gives
\[
h_e\le\frac2{\tau}\bigl(u_e+\sqrt{\Psi N_{ee}}\bigr).
\]
The exact checker reconstructs \(A\) from the source faces and bits,
checks its inverse, and verifies for every coordinate
\[
50\tau-2u_e>0,\qquad
(50\tau-2u_e)^2-4\Psi N_{ee}>0.
\]
Thus \(h_e<50\); integrality yields **\(M=\max_e h_e\le49\)**.
The source mode-removal premise \(D\ge12M\) is therefore sufficient at
even \(D\ge588\).

This does **not** improve the published complete dimension threshold 600:
the later [defect-one application](source/defect-one-DOWNSTREAM.md) has a
retained higher-defect estimate with exponent \(-2D+1196\), which
still requires even \(D\ge600\) for a strictly negative exponent.
No smaller host, new unconditional counterexample, or optimal global
dimension is claimed. Even the sharper outer ellipsoid does not certify
\(h_e<49\) for every coordinate; the checker records the failed margins,
which are not counterexamples to stronger bounds on actual profiles.
