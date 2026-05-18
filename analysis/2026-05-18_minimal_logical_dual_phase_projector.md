# Minimal Logical Dual Phase-Projector Theorem

## Executive result

Let \(A\) be the signed projective phase matrix of minimal logical rays in the canonical W(3,3) edge CSS code:

\[
A\in\{-1,0,+1\}^{160\times1620},
\]

with rows indexed by minimal X-rays and columns indexed by minimal Z-rays.

The row-side result was

\[
\boxed{AA^T/160\text{ is an exact rank-}81\text{ projector}.}
\]

The dual column-side result is now:

\[
\boxed{A^TA/160\text{ is also an exact rank-}81\text{ projector}.}
\]

Because \(A\) has rank \(81\), both projectors have the same nonzero spectrum:

\[
\boxed{160^{81}.}
\]

So

\[
\operatorname{spec}(AA^T)=160^{81}\oplus0^{79},
\]

while

\[
\operatorname{spec}(A^TA)=160^{81}\oplus0^{1539}.
\]

## Constant diagonals

The two projectors have constant diagonal values:

\[
\operatorname{diag}(AA^T)=81,
\]

so

\[
\operatorname{diag}(AA^T/160)=\frac{81}{160}.
\]

On the Z side,

\[
\operatorname{diag}(A^TA)=8,
\]

so

\[
\boxed{\operatorname{diag}(A^TA/160)=\frac{1}{20}.}
\]

The trace check is exact:

\[
160\cdot\frac{81}{160}=81,
\]

and

\[
1620\cdot\frac{1}{20}=81.
\]

Thus the same protected \(H_1=81\) dimension is seen from both sides.

## Interpretation

The signed phase matrix \(A\) is a rectangular partial-isometry-like bridge between:

\[
160\text{ minimal X-rays}
\]

and

\[
1620\text{ minimal Z-rays}.
\]

It projects both sides onto the same protected \(81\)-dimensional phase sector.

The row side says:

\[
\boxed{X\text{-ray phase visibility collapses onto }H_1.}
\]

The column side says:

\[
\boxed{Z\text{-ray phase visibility also collapses onto }H_1.}
\]

The difference is in how the projection is distributed:

\[
X\text{-side diagonal weight}=81/160,
\]

\[
Z\text{-side diagonal weight}=1/20.
\]

This is a very clean asymmetric-dual signature: the X side is small and high-weight; the Z side is large and low-weight; both carry total trace \(81\).

## Relation to unsigned visibility

The unsigned projective matrix \(U=|A|\) gives the visibility geometry:

\[
X\text{-side overlaps}=1,3,9,27,
\]

and

\[
Z\text{-side overlaps}=0,1,2,3,4.
\]

The signed phase matrix \(A\) is the collapse map:

\[
\boxed{\text{unsigned visibility geometry }\longrightarrow\text{ signed }H_1\text{ projector}.}
}
\]

In other words, the unsigned layer sees the combinatorial spread of minimal logical visibility, while the signed layer extracts the protected homological phase sector.

## Theorem statement

**Dual Phase-Projector Theorem.** For the signed projective minimal logical pairing matrix \(A\) of the W(3,3) edge CSS code,

\[
A\in\{-1,0,+1\}^{160\times1620},
\]

both normalized Gram matrices

\[
AA^T/160
\]

and

\[
A^TA/160
\]

are exact rank-81 projectors onto the same nonzero singular spectrum.  The row projector has constant diagonal \(81/160\), while the column projector has constant diagonal \(1/20\).  Both traces are exactly \(81\), the protected \(H_1\) dimension.

## Honesty boundary

This is an exact finite phase-projector invariant.  It does not by itself assign physical amplitudes, probabilities, continuum dynamics, or empirical observables.  It provides a canonical finite linear-algebra object for later TQC and Standard Model bridges.
