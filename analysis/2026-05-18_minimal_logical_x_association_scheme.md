# Minimal Logical X-Association Scheme

## Executive result

The previous overlap theorem showed that the projective minimal X-rays have pairwise visible-Z overlaps only in

\[
1,3,9,27.
\]

This result upgrades that histogram into a full algebraic closure theorem.

Let \(U\in\{0,1\}^{160\times1620}\) be the unsigned projective incidence matrix of minimal logical rays:

\[
U_{xz}=1\Longleftrightarrow \langle x,z\rangle\neq0.
\]

Let

\[
G=UU^T.
\]

Define relation matrices on the 160 minimal X-rays:

\[
R_0=I,
\]

and, for \(k\in\{1,3,9,27\}\),

\[
(R_k)_{xy}=1\Longleftrightarrow G_{xy}=k.
\]

Then

\[
\boxed{\{R_0,R_1,R_3,R_9,R_{27}\}\text{ is a 4-class commutative association scheme}.}
\]

## Valencies

The valencies are:

| Relation | Meaning | Valency |
|---:|---|---:|
| \(R_0\) | identity | 1 |
| \(R_1\) | overlap 1 | 81 |
| \(R_3\) | overlap 3 | 54 |
| \(R_9\) | overlap 9 | 18 |
| \(R_{27}\) | overlap 27 | 6 |

So the nontrivial valency profile is

\[
\boxed{81,54,18,6=3^4,2\cdot3^3,2\cdot3^2,2\cdot3.}
\]

## Why this matters

A histogram says the numbers appear.

An association scheme says the relations form a closed finite algebra.

That means the minimal X-ray visibility geometry has its own Bose-Mesner algebra: the overlap relations partition the complete relation on 160 points, are symmetric, commute, and close under matrix multiplication.

So the X-side minimal logical surface is not merely q-adic by count. It is q-adic as an algebraic scheme.

## Full intersection-number table

The verifier computes the complete intersection table.  A row labeled \(i,j\) gives the constants \(p_{ij}^k\) for \(k\in\{0,1,3,9,27\}\), meaning:

\[
R_iR_j=\sum_k p_{ij}^k R_k.
\]

### Products with \(R_1\)

\[
R_1R_1:
(81,40,42,36,54),
\]

\[
R_1R_3:
(0,28,24,36,27),
\]

\[
R_1R_9:
(0,8,12,9,0),
\]

\[
R_1R_{27}:
(0,4,3,0,0).
\]

### Products with \(R_3\)

\[
R_3R_3:
(54,16,24,9,18),
\]

\[
R_3R_9:
(0,8,3,6,9),
\]

\[
R_3R_{27}:
(0,2,2,3,0).
\]

### Products with \(R_9\)

\[
R_9R_9:
(18,2,2,0,6),
\]

\[
R_9R_{27}:
(0,0,1,2,3).
\]

### Product with \(R_{27}\)

\[
R_{27}R_{27}:
(6,0,0,1,2).
\]

All products are symmetric because the scheme is commutative.

## The theorem

**Minimal Logical X-Association Scheme Theorem.** The projective minimal X-rays of the canonical W(3,3) edge CSS code form a 4-class commutative association scheme under visible-Z overlap. The nontrivial relations are indexed by overlap values

\[
1,3,9,27,
\]

with valencies

\[
81,54,18,6.
\]

The relation matrices partition the complete relation on 160 points and close under matrix multiplication.

## Interpretation

The stack now becomes:

\[
\text{minimal CSS distances}\Rightarrow (3,4),
\]

\[
\text{unsigned noncommutation}\Rightarrow |W(E_6)|,
\]

\[
\text{signed phase}\Rightarrow H_1\text{ projector},
\]

\[
\text{X-side projective visibility}\Rightarrow 4\text{-class }3\text{-adic association scheme}.
\]

This is a much stronger finite foundation for the qutrit/TQC substrate: the minimal logical rays carry an honest association scheme whose overlap labels are powers of the field size.

## Honesty boundary

This is an exact finite association-scheme invariant. It does not by itself assign continuum dynamics, physical probabilities, or empirical observables. It supplies a finite algebraic object for later interpretation.
