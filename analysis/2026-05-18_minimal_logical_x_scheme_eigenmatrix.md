# Minimal Logical X-Scheme Eigenmatrix Theorem

## Executive result

The projective minimal X-rays form a 4-class commutative association scheme under visible-Z overlap.  The relations are

\[
R_0,
R_1,
R_3,
R_9,
R_{27},
\]

where \(R_k\) means two minimal X-rays share exactly \(k\) visible minimal Z-rays.

The new spectral result is that the primitive multiplicities are

\[
\boxed{1,\\ 24,\\ 30,\\ 24,\\ 81.}
\]

The protected \(H_1=81\) sector is not merely the rank of the signed phase frame.  It is a primitive eigenspace of the association scheme itself.

## First eigenmatrix

Columns are

\[
R_0,R_1,R_3,R_9,R_{27}.
\]

The primitive eigenspaces have rows:

| Multiplicity | Eigenvalue row |
|---:|---|
| 1 | \((1,81,54,18,6)\) |
| 24 | \((1,-9,6+3\sqrt6,-2\sqrt6,2-\sqrt6)\) |
| 30 | \((1,9,-6,-6,2)\) |
| 24 | \((1,-9,6-3\sqrt6,2\sqrt6,2+\sqrt6)\) |
| 81 | \((1,1,-2,2,-2)\) |

So the \(81\)-sector has the clean integral character row

\[
\boxed{(1,1,-2,2,-2).}
\]

## Relation spectra

The individual relation spectra are:

\[
R_1:
81^1,\ 9^{30},\ 1^{81},\ (-9)^{48}.
\]

\[
R_3:
54^1,\ (6+3\sqrt6)^{24},\ (-6)^{30},\ (6-3\sqrt6)^{24},\ (-2)^{81}.
\]

\[
R_9:
18^1,\ (2\sqrt6)^{24},\ (-6)^{30},\ (-2\sqrt6)^{24},\ 2^{81}.
\]

\[
R_{27}:
6^1,\ (2+\sqrt6)^{24},\ 2^{30},\ (2-\sqrt6)^{24},\ (-2)^{81}.
\]

## Unsigned Gram spectrum recovered

Because

\[
UU^T=81R_0+R_1+3R_3+9R_9+27R_{27},
\]

the unsigned Gram spectrum becomes

\[
648^1,
\]

\[
(144+36\sqrt6)^{24},
\]

\[
72^{30},
\]

\[
(144-36\sqrt6)^{24},
\]

\[
40^{81}.
\]

This matches the previous 3-adic overlap spectrum, now explained by the primitive eigenspaces.

## Interpretation

The multiplicity pattern

\[
1,24,30,24,81
\]

is extremely suggestive:

- \(1\): trivial/vacuum sector;
- \(24\): W33 positive spectral multiplicity / first conjugate sector;
- \(30\): middle integral sector;
- \(24\): second conjugate sector;
- \(81\): protected \(H_1\) sector.

The two \(24\)-dimensional sectors are conjugate over

\[
\mathbb Q(\sqrt6).
\]

The protected \(81\)-sector is integral and primitive.

## The theorem

**Minimal Logical X-Scheme Eigenmatrix Theorem.** The 4-class association scheme on the 160 projective minimal X-rays has primitive multiplicities

\[
\boxed{1,24,30,24,81.}
\]

The protected \(H_1=81\) sector is a primitive eigenspace with integral eigenvalue row

\[
\boxed{(1,1,-2,2,-2)}
\]

across the relations

\[
R_0,R_1,R_3,R_9,R_{27}.
\]

The two \(24\)-dimensional sectors form a conjugate pair over \(\mathbb Q(\sqrt6)\).

## Why this is a breakthrough

The previous results showed:

\[
\text{minimal logical noncommutation}\Rightarrow |W(E_6)|,
\]

\[
\text{signed phase frame}\Rightarrow H_1=81,
\]

\[
\text{projective overlaps}\Rightarrow 3\text{-adic association scheme}.
\]

Now we have:

\[
\boxed{H_1=81\text{ is a primitive eigenspace of that association scheme}.}
\]

So the protected sector is not imposed from homology after the fact. It emerges inside the Bose-Mesner algebra of the minimal logical visibility geometry.

## Honesty boundary

This is an exact finite spectral invariant of the association scheme. It does not by itself assign continuum dynamics, physical probabilities, or empirical observables. It gives the qutrit/TQC bridge a finite representation-theoretic skeleton.
