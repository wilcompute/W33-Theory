# BT1807 — Defect Phase-Plane Transversal Design Theorem

## Result

Pass 64 made the contextuality-tax defect into an executable interrupt controller, and Pass 65 showed that a real kernel/page/telemetry workload walks the defect along cheap center-quad channels. BT1807 removes the remaining seed-specific ambiguity from that telemetry: the escape surface is an exact local design at every defect center.

For each center \(p\in W(3,3)\):

\[
\Gamma(p)=12,
\qquad
W(3,3)\setminus (\{p\}\cup\Gamma(p))=27.
\]

The closed-form vector table has exactly nine safe triads:

\[
\mathcal T_p=\{T_1,\ldots,T_9\},
\qquad
|T_i|=3,
\qquad
\bigsqcup_i T_i = W(3,3)\setminus (\{p\}\cup\Gamma(p)).
\]

Each safe triad has a four-point common-perp inside the defect star:

\[
Q_i = T_i^\perp\cap\Gamma(p),
\qquad
|Q_i|=4.
\]

The nine quads \(Q_i\) are not arbitrary. They are exactly a transversal design

\[
\boxed{TD(4,3)}
\]

on the four star-lines through \(p\). Equivalently:

\[
\Gamma(p)=L_1\sqcup L_2\sqcup L_3\sqcup L_4,
\qquad
|L_a|=3,
\]

and every \(Q_i\) contains one point from each \(L_a\). Each neighbor of \(p\) appears in exactly three quads, every pair of neighbors from different star-lines appears in exactly one quad, and no pair from the same star-line appears in a quad.

## Global cover law

Across the whole substrate, the cheap exits are a uniform cover of the actual W33 fabric:

\[
40\cdot 9\cdot 4 = 1440
=3\cdot 480
=6\cdot 240.
\]

So the cheap relocation surface is:

\[
\boxed{3\text{-fold cover of directed fabric edges}}
\]

or, forgetting direction,

\[
\boxed{6\text{-fold cover of undirected fabric edges}.}
\]

## Why this matters

Pass 65 had a real walking-defect trace, but coverage statistics were honestly labeled seed-specific. BT1807 separates what is exact from what is telemetry: the *allowed local escape geometry* is exact, design-theoretic, and independent of the run. The seeded walk is only sampling a rigid \(TD(4,3)\)-fibered edge cover already written into the interrupt vector table.

This also gives the runtime team a stronger scheduling invariant:

> Every interrupt vector exposes four cheap target centers, but globally every directed fabric edge is exposed by exactly three interrupt vectors.

That is the missing load-balancing law between the local AG\((2,3)\) phase plane and the global diameter-2 W33 fabric.

## Verified checks

The witness proves:

- \(W(3,3)=SRG(40,12,2,4)\) from the symplectic form over \(\mathbb F_3^4\).
- All 40 centers have exactly 9 all-centers-in-perp safe triads.
- The 9 triads partition the 27 safe non-neighbors.
- The 9 unlit quads are independent 4-point star transversals.
- The unlit quads form \(TD(4,3)\): neighbor replication 3, cross-star pair replication 1, same-star pair replication 0.
- The 1440 cheap directed exits cover every directed W33 edge exactly 3 times.

## Honest scope

This is an exact finite-geometric witness. It strengthens the seeded walking-defect telemetry into a local/global incidence law, but it does not claim hardware timing, ergodicity, or physical noise tolerance.
