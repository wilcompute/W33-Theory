# Minimal Logical Phase-Frame Theorem

## Executive result

The previous census showed that the unsigned noncommutation graph between minimal logical X and Z vectors has exactly

\[
51840=|W(E_6)|
\]

nonzero pairings.

The next invariant is stronger: keep the \(\mathbb F_3\) phase.

Define the projective signed phase matrix \(A\) by taking one representative from each minimal logical ray and setting

\[
A_{xz}=\begin{cases}
0,& \langle x,z\rangle=0,\\
+1,& \langle x,z\rangle=1,\\
-1,& \langle x,z\rangle=2=-1.
\end{cases}
\]

Here

\[
A\in\{-1,0,+1\}^{160\times1620}.
\]

Then

\[
\boxed{\operatorname{spec}(AA^T)=160^{81}\oplus0^{79}.}
\]

So the projective minimal logical phase matrix has

\[
\boxed{\operatorname{rank}(A)=81.}
\]

That rank is exactly the protected homology dimension:

\[
\boxed{81=\dim H_1(W(3,3);\mathbb F_3).}
\]

## Vector-level expansion

If scalar multiples are retained instead of passing to projective rays, the signed vector-level matrix \(M\) has shape

\[
M\in\{-1,0,+1\}^{320\times3240}.
\]

Then

\[
\boxed{\operatorname{spec}(MM^T)=640^{81}\oplus0^{239}.}
\]

So scalar expansion multiplies the frame constant by \(4\), but preserves the same protected rank \(81\).

## Why this matters

There are now two layers:

1. **Unsigned layer:** the number of nonzero minimal logical X/Z pairings is

\[
51840=|W(E_6)|.
\]

2. **Signed phase layer:** the phase-weighted pairing matrix has rank exactly

\[
81=H_1.
\]

This means the minimal logical error surface does two things at once:

- forgetting phase gives the exceptional \(E_6\) commutation-count shadow;
- remembering phase projects the system onto the protected \(81\)-dimensional homology sector.

## Theorem statement

**Minimal Logical Phase-Frame Theorem.** Let \(A\) be the projective signed phase matrix of minimal X and Z logical rays in the canonical W(3,3) edge CSS code, with entries \(0,+1,-1\) according to the \(\mathbb F_3\) symplectic pairing. Then \(A\) has rank \(81\), and

\[
AA^T
\]

has spectrum

\[
\boxed{160^{81}\oplus0^{79}.}
\]

Keeping scalar multiples gives a vector-level signed matrix \(M\) with

\[
\boxed{\operatorname{spec}(MM^T)=640^{81}\oplus0^{239}.}
\]

Thus the phase-weighted minimal logical pairing system is a tight frame whose rank is exactly the protected \(H_1\) dimension.

## Interpretation

This is a major sharpening of the E6 bridge.  The unsigned count produces \(|W(E_6)|\).  The signed phase geometry produces \(H_1=81\).  That means the same minimal logical surface simultaneously carries:

\[
\boxed{E_6\text{ as noncommutation count},\qquad H_1\text{ as phase-frame rank}.}
\]

In TOE language: the exceptional symmetry appears when phase is forgotten; the protected qutrit memory appears when phase is retained.

## Honesty boundary

This is an exact finite phase-frame invariant.  It does not by itself identify a continuum Hilbert-space dynamics or physical braid representation.  It provides the finite algebraic object those later bridges must act on.
