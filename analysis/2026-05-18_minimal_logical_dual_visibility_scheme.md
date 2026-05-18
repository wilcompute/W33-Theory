# Minimal Logical Dual Visibility Scheme

## Executive result

The previous theorem gave the X-side projective overlap scheme for the unsigned minimal logical incidence matrix

\[
U\in\{0,1\}^{160\times1620},
\qquad
U_{xz}=1\Longleftrightarrow \langle x,z\rangle\neq0.
\]

This file gives the dual Z-side scheme.

The degrees are:

\[
\boxed{\deg_X=81,\qquad \deg_Z=8.}
\]

So each minimal X-ray sees 81 minimal Z-rays, while each minimal Z-ray sees 8 minimal X-rays.

## X-side recap

For the X-side Gram matrix

\[
UU^T,
\]

pairwise X-ray overlaps are exactly

\[
\boxed{1,3,9,27.}
\]

Per X-ray, the multiplicities are

\[
\boxed{81,54,18,6.}
\]

So the X-side is purely 3-adic by overlap value:

\[
1,3,9,27=3^0,3^1,3^2,3^3.
\]

## Z-side result

For the Z-side Gram matrix

\[
U^TU,
\]

every minimal Z-ray has diagonal degree

\[
8.
\]

For each fixed minimal Z-ray, the overlap distribution with all other minimal Z-rays is:

| Shared visible X-rays | Number of other Z-rays |
|---:|---:|
| 0 | 1187 |
| 1 | 288 |
| 2 | 96 |
| 3 | 32 |
| 4 | 16 |

Therefore every minimal Z-ray overlaps nontrivially with exactly

\[
288+96+32+16=432
\]

other minimal Z-rays.

And

\[
\boxed{432=16\cdot27=2^4\cdot3^3.}
\]

This is the dual visibility law.

## Global Z-side pair counts

The off-diagonal pair counts are:

| Shared visible X-rays | Number of unordered Z-ray pairs |
|---:|---:|
| 0 | 961470 |
| 1 | 233280 |
| 2 | 77760 |
| 3 | 25920 |
| 4 | 12960 |

The nonzero part is

\[
233280+77760+25920+12960=349920.
\]

Equivalently,

\[
1620\cdot432/2=349920.
\]

## Dual interpretation

The two sides behave differently but compatibly:

\[
\boxed{X\text{-side: overlap values are }1,3,9,27.}
\]

\[
\boxed{Z\text{-side: overlap multiplicities cascade }288\to96\to32\text{ by }3:1,\text{ with }16\text{ as the overlap-4 core}.}
\]

So:

- the X-side is q-adic in overlap values;
- the Z-side is bounded by the distance root \(d_Z=4\) and q-adic in multiplicity cascade;
- the nonzero Z-neighborhood size is \(16\cdot27\), combining \(2^4\) with \(q^q\).

## Signed phase projector remains the collapse map

The signed phase matrix \(A\) still satisfies

\[
(AA^T)^2=160AA^T.
\]

So

\[
\boxed{AA^T/160}
\]

is the exact rank-81 protected projector.

The unsigned dual schemes describe visibility geometry; the signed phase refinement collapses that visibility geometry onto the protected homology sector.

## The theorem

**Dual Visibility Scheme Theorem.** For the projective minimal logical incidence matrix \(U\) of the W(3,3) edge CSS code, the X-side overlaps are the 3-adic values \(1,3,9,27\) with per-row counts \(81,54,18,6\). Dually, every minimal Z-ray has column degree \(8\), is disjoint from \(1187\) other Z-rays, and has pairwise visibility overlaps \(1,2,3,4\) with \(288,96,32,16\) other Z-rays. In particular, every Z-ray overlaps nontrivially with exactly

\[
\boxed{432=16\cdot27}
\]

other Z-rays.

## Honesty boundary

This is an exact finite dual visibility scheme. It does not by itself assign physical probabilities, continuum dynamics, or empirical observables. It supplies another finite invariant for the qutrit/TQC bridge.
