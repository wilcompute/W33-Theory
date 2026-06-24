# BT1686 — H1 Irreducibility Certificate

## Purpose

BT1683 proves the oriented bridge twirl formula

\[
\overline P_B=\frac8{81}P_{H_1}
\]

conditional on irreducibility of the Levi \(H_1\) representation under
\(PSp(4,3)\). BT1686 records the exact certificate needed to remove that
condition.

## Representation

The representation is:

\[
G=PSp(4,3),
\qquad
|G|=25920,
\]

acting on the W33 Levi cycle space

\[
H_1,
\qquad
\dim H_1=81.
\]

## Certificate target

The needed certificate is

\[
\boxed{\dim \operatorname{End}_G(H_1)=1.}
\]

Equivalently, the only linear maps on \(H_1\) commuting with all generators of
\(G\) are scalar multiples of the identity.

## Current status

BT1681 already gives strong numerical evidence:

\[
\left\|\overline P_B-\frac8{81}P_{H_1}\right\|_F
=1.0598553943057821\times10^{-14},
\]

with relative error

\[
1.1923373185940048\times10^{-14}.
\]

The averaged projector has eigenvalue

\[
8/81
\]

with multiplicity

\[
81.
\]

This is consistent with commutant dimension one, but it is not the final exact
rational commutant certificate.

## Exact algorithm

The exact certificate should:

1. construct the W33 Levi oriented incidence matrix \(D\) over \(\mathbb Q\);
2. build projective symplectic generators as signed edge permutation matrices;
3. compute a rational basis for \(\ker D\), representing \(H_1\);
4. restrict generator matrices to that basis;
5. solve
   \[
   XA_g=A_gX
   \]
   for all generators over \(\mathbb Q\);
6. certify that the solution space is
   \[
   \operatorname{span}(I_{81}).
   \]

## Boundary

Do not state irreducibility as formally proved until the rational
commutant-dimension-one artifact is emitted. BT1686 is a precise certificate
specification plus numerical support, not the final exact proof.

## Files

- `analysis/bt1686_h1_irreducibility_certificate.py`
- `data/PART_BT1686_H1_IRREDUCIBILITY_CERTIFICATE_results.json`
