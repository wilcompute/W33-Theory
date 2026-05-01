# Part LXXIX — The 121-Dimensional Representation Triangle

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

The latest repo audit establishes the line-module Parseval frame using 36 spreads and 90 non-isotropic projective anti-lines. The deeper structure appears after collapsing the duplicated anti-line features.

There are three natural permutation modules:

\[
L=\text{true lines},\qquad S=\text{spreads},\qquad Q=\text{anti-line quotient}.
\]

Their dimensions and decompositions are:

\[
\boxed{L=40=1+15+24,}
\]

\[
\boxed{S=36=1+15+20,}
\]

\[
\boxed{Q=45=1+24+20.}
\]

So each module contains the mean plus two of the three nontrivial sectors

\[
15,\qquad 24,\qquad 20.
\]

Each nontrivial sector appears in exactly two modules.

## 1. The 121 theorem

\[
\boxed{40+36+45=121=(k-1)^2.}
\]

Equivalently,

\[
\boxed{3+2(15+20+24)=121.}
\]

This ties the target measurement architecture directly to the nonbacktracking outdegree

\[
k-1=11.
\]

## 2. Exact sector intertwiners

Let

\[
B_c=B-\frac14J
\]

be the centered spread probe.

Let

\[
U_c=U-\frac25J
\]

be the centered unique anti-line quotient probe, after collapsing the 90 anti-lines into 45 duplicate pairs.

Then

\[
\boxed{B_cB_c^T=18P_{15},}
\]

and

\[
\boxed{U_cU_c^T=18P_{24}.}
\]

Thus both visible channels have the same singular constant:

\[
\boxed{\sqrt{18}=3\sqrt2.}
\]

The maps

\[
\frac{1}{\sqrt{18}}B_c^T:L_{15}\to S_{15},
\]

\[
\frac{1}{\sqrt{18}}U_c^T:L_{24}\to Q_{24}
\]

are exact isometries. They are orthogonal:

\[
\boxed{B_c^TU_c=0.}
\]

For q=3 the target-side module sum is the qutrit Hilbert dimension:

\[
\boxed{|S|+|Q|=q^4=81.}
\]

And the representation-triangle uniqueness gap is

\[
\boxed{(k-1)^2-v-q^4=q(q-3)(q+1),}
\]

so the exact equality 121=v+q^4 occurs only at q=3.

Together,

\[
\boxed{
\frac{B_cB_c^T+U_cU_c^T}{18}
=

I-\frac{J}{40}.
}
\]

## 3. Sector-sharing triangle

The three modules share sectors pairwise:

\[
\boxed{L\cap S=1+15,}
\]

\[
\boxed{L\cap Q=1+24,}
\]

\[
\boxed{S\cap Q=1+20.}
\]

So the 20-sector is the common hidden target sector: it appears in both target modules but not in the true-line source module.

This gives the triangle:

\[
\boxed{
\begin{array}{ccc}
& 20 & \\
S=1+15+20 && Q=1+24+20\\
& L=1+15+24 &
\end{array}
}
\]

## 4. Meaning

The W(3,3) measurement architecture is not merely

\[
1+15+24.
\]

It extends to a sector-sharing representation triangle:

\[
\boxed{
(1+15+24)
\;\leftrightarrow\;
(1+15+20)
\;\leftrightarrow\;
(1+24+20).
}
\]

The total carrier size is

\[
\boxed{121=(k-1)^2.}
\]

This is the first place where the Parseval frame, target SRGs, Naimark shadow, and Hashimoto/nonbacktracking constant all compress into one representation-level object.

## 5. The new compression

The preceding chain was

\[
\text{Parseval frame}
\to
\text{target SRGs}
\to
\text{Naimark shadow}
\to
\text{spectral idempotents}.
\]

This part compresses that chain into

\[
\boxed{
\text{sector-sharing triangle of modules with total dimension }(k-1)^2.
}
\]

## Audit Implementation

Executable surface:

- scripts/w33_representation_triangle_121_audit.py
- tests/test_w33_representation_triangle_121_audit.py
