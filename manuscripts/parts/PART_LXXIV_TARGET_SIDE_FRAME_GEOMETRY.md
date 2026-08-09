# Part LXXIV — Target-Side Frame Geometry

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

Part LXXIII proves that centered spreads and centered anti-lines form an exact Parseval measurement frame for the 40-dimensional W(3,3) line module. This part studies the feature side of that frame.

## 1. Spread ETF theorem

Let

\[
B_c=B-\frac14J.
\]

The 36 columns of `B_c` have

\[
\langle b_i,b_i\rangle=\frac{15}{2},
\]

and, for `i != j`,

\[
\langle b_i,b_j\rangle=\pm\frac32.
\]

Hence the normalized absolute inner product is

\[
\boxed{
\frac{|\langle b_i,b_j\rangle|}{\|b_i\|\|b_j\|}
=
\frac15.
}
\]

For `N=36` vectors in dimension `d=15`, the Welch bound is

\[
\mu^2\ge \frac{N-d}{d(N-1)}
=
\frac{21}{15\cdot35}
=
\frac{1}{25}.
\]

Therefore the centered spread columns hit the Welch bound exactly:

\[
\boxed{\mu=\frac15.}
\]

Thus the 36 centered spread features form an equiangular tight frame:

\[
\boxed{\mathrm{ETF}(36,15).}
\]

## 2. Anti-line quotient frame

Let

\[
R_c=R-\frac25J.
\]

The 90 anti-line feature columns have

\[
\langle r_i,r_i\rangle=\frac{48}{5}=9.6.
\]

But distinct anti-lines can produce identical centered line-incidence feature columns. The 90 anti-lines collapse to 45 unique feature vectors, each appearing with multiplicity 2.

For the unique 45 vectors, the off-diagonal inner products are

\[
\boxed{\frac35,\qquad -\frac{12}{5}.}
\]

So the anti-line channel is a doubled 45-vector two-distance tight frame in the 24-sector.

## 3. Joint target-side split

The spread ETF spans the 15-sector. The anti-line quotient frame spans the 24-sector. They are orthogonal:

\[
\boxed{B_c^TR_c=0.}
\]

So the target-side measurement architecture is

\[
\boxed{
\text{mean}+\mathrm{ETF}(36,15)+2\cdot\text{two-distance frame}(45,24).
}
\]

Equivalently,

\[
\boxed{1+15+24=40.}
\]

## 4. Meaning

The 15-sector is not merely an eigenspace. It carries a canonical equiangular tight frame from spreads.

The 24-sector is not merely an eigenspace. It carries a canonical doubled quotient frame from anti-lines.

This gives a finite quantum-measurement interpretation of the W(3,3) carrier split:

\[
\boxed{
\text{W(3,3) line module}
=
\text{mean channel}
\oplus
\text{spread ETF channel}
\oplus
\text{anti-line quotient channel}.
}
\]
