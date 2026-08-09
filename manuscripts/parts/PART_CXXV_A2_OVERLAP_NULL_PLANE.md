# Part CXXV — A2 Overlap Null Plane for Complete Two-Qutrit MUB Frames

**Status:** theorem-grade structural extension  
**Date:** April 29, 2026

Parts CXX--CXXIV identify the complete two-qutrit stabilizer MUB frames as a binary-octahedral lift of an `S4` local skeleton.  Part CXXIV gives the decisive pair law:

```text
product overlap = fixed points of the relative S4 element,
entangled overlap = total overlap - product overlap,
total overlap in {1,4} for distinct frames.
```

This part extracts a new consequence that does **not** require resolving the remaining fine split inside every 3-cycle layer.

## 1. The three frame sectors

There are 36 complete frames, arranged as

```text
E+ : 12 frames
E- : 12 frames
O  : 12 frames
```

The even local skeletons have two binary-octahedral chiral completions `E+` and `E-`; the odd skeletons have one achiral completion `O`.

Thus the frame set has a canonical coarse quotient

```text
36 = 12 x 3.
```

The quotient is the `A2` chirality quotient: the three sector labels are the three vertices of the affine `A2` triangle, while each sector has twelve `S4/A4`-controlled local skeleton states.

## 2. Four-overlap quotient matrix

Let `G4` be the graph on the 36 complete frames where two distinct frames are adjacent iff their total overlap is 4.

From Part CXXIV:

* same sector: each frame has 3 four-overlap neighbors in its own sector;
* each other sector: each frame has 6 four-overlap neighbors.

Therefore the equitable quotient of `G4` by the partition `(E+,E-,O)` is

\[
Q_4=
\begin{pmatrix}
3&6&6\\
6&3&6\\
6&6&3
\end{pmatrix}.
\]

Consequences:

\[
Q_4\mathbf 1 = 15\mathbf 1,
\qquad
Q_4|_{A_2}=-3I.
\]

So `G4` is forced to be 15-regular, and its sector quotient already contains the `A2` eigenplane with eigenvalue `-3`.

Edge count:

```text
36 * 15 / 2 = 270 four-overlap pairs.
```

The edge decomposition is

```text
within sectors: 3 * (12*3/2) = 54,
between sectors: 3 * (12*6) = 216,
total: 270.
```

## 3. Total-overlap balancing theorem

Let `M` be the total-overlap matrix of the 36 frames, with diagonal entry `10` because a complete two-qutrit stabilizer MUB frame contains 10 contexts/bases.

For a fixed source frame, the total overlap into its own sector is

\[
10 + 3\cdot 4 + 8\cdot 1 = 30.
\]

Into either other sector it is

\[
6\cdot 4 + 6\cdot 1 = 30.
\]

Hence the equitable quotient of `M` is

\[
Q_M=
\begin{pmatrix}
30&30&30\\
30&30&30\\
30&30&30
\end{pmatrix}.
\]

This is the new locked structure:

\[
Q_M\mathbf 1 = 90\mathbf 1,
\qquad
Q_M|_{A_2}=0.
\]

## 4. Theorem CXXV

**Theorem CXXV (A2 Overlap Null Plane).**  The total-overlap matrix of the 36 complete two-qutrit stabilizer MUB frames has a mandatory null plane on the coarse chirality quotient.  Explicitly, any vector constant on the sectors `(E+,E-,O)` with coefficients summing to zero is killed by the sector quotient of the overlap matrix:

\[
(a,b,c),\quad a+b+c=0
\quad\Longrightarrow\quad
Q_M(a,b,c)^T=0.
\]

Equivalently, the two independent sector-difference modes

\[
(1,-1,0),\qquad (1,1,-2)
\]

are exact zero modes of the quotient overlap form.

## 5. Meaning

The overlap law is not merely a list of pair counts.  It has a hidden finite-geometric cancellation:

```text
product skeleton asymmetry + entangled lift correction = A2-balanced total overlap.
```

The binary-octahedral lift is doing exactly what a spin/chirality correction should do: it cancels the coarse sector imbalance and leaves a rank-one total-overlap quotient.

This gives a cleaner interpretation of the `A2` chirality quotient found just before CXXIV:

```text
A2 is not decorative.
A2 is the null discriminant of the complete MUB-frame overlap form.
```

## 6. Paper insertion point

This belongs immediately after the CXXIV relative-cycle law or in the paper's qutrit/MUB section as the first global spectral consequence of the binary-octahedral frame classification.

The accompanying regression tests are in:

```text
tests/test_mub_a2_overlap_null_plane_cxxv.py
```
