# BT622 — \(E_1/E_3\) Conjugate Root Channel Note

## Claim

The only cross-idempotent leakage channel in the folded cubic Hashimoto operator

\[
F_3=TB^3T^T
\]

is the conjugate \(24+24\) channel

\[
E_1 \leftrightarrow E_3.
\]

This is not an arbitrary failure of diagonalization.  It is exactly the real form of the conjugate pair of nonrational primitive idempotents in the W33 Levi flag association scheme.

## Evidence from BT617

BT617 computes the full primitive block support of \(F_3\):

\[
(0,0),\quad (1,1),\quad (1,3),\quad (2,2),\quad (3,1),\quad (3,3),\quad (4,4).
\]

So:

\[
E_iF_3E_4=E_4F_3E_i=0\qquad (i\neq4),
\]

and

\[
E_4F_3E_4=E_4.
\]

The protected Hodge sector is therefore isolated.

The \(E_1,E_3\) diagonal blocks are conjugate:

\[
E_1F_3E_1=(-68-31\sqrt6)E_1,
\]

\[
E_3F_3E_3=(-68+31\sqrt6)E_3.
\]

The off-diagonal blocks satisfy

\[
M_{13}M_{31}=-6455E_1,
\]

\[
M_{31}M_{13}=-6455E_3.
\]

Thus the \(E_1/E_3\) channel is a paired conjugate channel, not a leakage into the Hodge sector.

## Association-scheme interpretation

The W33 Levi flag graph has primitive adjacency eigenvalues

\[
6,\quad 2+\sqrt6,\quad 2,\quad 2-\sqrt6,\quad -2.
\]

The two \(24\)-dimensional sectors are exactly the conjugate irrational pair

\[
2+\sqrt6,\qquad 2-\sqrt6.
\]

Therefore a real integer operator such as \(F_3\) may mix these two sectors while preserving the rational decomposition.  This is the same phenomenon as a real operator on a quadratic field pair: the individual irrational sectors are conjugate, while their direct sum is the rational \(48\)-dimensional carrier.

So the robust invariant is not separately

\[
E_1,\qquad E_3,
\]

but the rational conjugate packet

\[
\boxed{E_1+E_3.}
\]

## \(G_2\)-style reading

The \(E_1/E_3\) packet has dimension

\[
24+24=48=4\cdot12.
\]

Here \(12=|W(G_2)|\), and \(4=\chi\) is the W33 Euler/curvature unit already used throughout the cubic leakage normalization.

So a conservative reading is:

\[
\boxed{E_1+E_3\text{ is a }48=4\cdot |W(G_2)|\text{ conjugate-root channel.}}
\]

This is intentionally weaker than claiming a literal \(G_2\) representation.  What is verified is the exact \(48\)-dimensional conjugate quadratic packet and the exact \(E_1\leftrightarrow E_3\) mixing.  The \(G_2\) reading is a substrate interpretation of the factor \(48=4\cdot12\), not yet a full representation theorem.

## Boundary

The result proves:

\[
\boxed{\text{protected sector }E_4\text{ is isolated and physical,}}
\]

while

\[
\boxed{E_1+E_3\text{ is the conjugate lower-shell transport channel.}}
\]

It does **not** yet prove that the \(E_1+E_3\) channel carries an explicit \(G_2\)-module action.  That would require constructing a concrete \(W(G_2)\) or root-system action on the \(48\)-dimensional packet.

## Next test

A natural next verifier is:

\[
\text{BT623: construct a }W(G_2)\text{ action or obstruction on }E_1+E_3.
\]

The test should determine whether the \(48=4\cdot12\) factorization is only numerological substrate arithmetic or an actual equivariant \(G_2\) Weyl packet.
