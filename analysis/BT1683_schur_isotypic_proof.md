# BT1683 — Formal Schur/Isotypic Proof Certificate

## Statement

Let \(G=PSp(4,3)\) act on the W33 Levi edge space, and let \(P_{H_1}\) be the
Levi cycle-space Hodge projector.  Let \(P_B\) be the orthogonal projector onto a
fixed oriented bridge subspace

\[
B\subset H_1,
\qquad
\dim B=8.
\]

If the Levi \(H_1\) representation is irreducible under \(G\), then

\[
\boxed{
\frac1{|G|}\sum_{g\in G}\rho(g)P_B\rho(g)^{-1}
=rac{8}{81}P_{H_1}.
}
\]

## Proof

Define

\[
A=\frac1{|G|}\sum_{g\in G}\rho(g)P_B\rho(g)^{-1}.
\]

For every \(h\in G\),

\[
\rho(h)A\rho(h)^{-1}=A.
\]

Thus \(A\) lies in the commutant of the \(G\)-representation on \(H_1\).  If the
\(H_1\) representation is irreducible, Schur's lemma gives

\[
A=\alpha P_{H_1}.
\]

Taking traces,

\[
\operatorname{tr}A=\operatorname{tr}P_B=8,
\]

and

\[
\operatorname{tr}P_{H_1}=81.
\]

Therefore

\[
\alpha=\frac8{81}.
\]

So

\[
A=\frac8{81}P_{H_1}.
\]

## BT1681 numerical certificate

BT1681 computed the actual automorphism average and found:

\[
\operatorname{tr}A=7.999999999999972,
\]

\[
\|A-(8/81)P_{H_1}\|_F=1.0598553943057821\times10^{-14},
\]

and relative Frobenius error

\[
1.1923373185940048\times10^{-14}.
\]

The nonzero eigenvalue is

\[
8/81=0.09876543209876543,
\]

with multiplicity

\[
81.
\]

## Distinction from support twirl

BT1675 averaged an all-positive support vector and got zero \(H_1\).  BT1681 and
BT1683 average an oriented \(H_1\) subspace projector and get isotropic \(H_1\)
density.  These are different operations.

## Boundary

This is a formal proof conditional on the irreducibility of the Levi \(H_1\)
module.  A fully formal paper proof should either derive that irreducibility or
include a commutant-dimension certificate.

## Files

- `analysis/bt1683_schur_isotypic_proof.py`
- `data/PART_BT1683_SCHUR_ISOTYPIC_PROOF_results.json`
