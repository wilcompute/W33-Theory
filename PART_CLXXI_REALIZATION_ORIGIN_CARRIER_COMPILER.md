# Part CLXXI — Realization Origin / Carrier Compiler

**Date:** 2026-05-02  
**Status:** realization-data theorem integrating geometric realizations, Fano origin, and carrier completion

---

## 1. Source hint

The fuller toroidal-triad page gives more than the raw toroidal counts.  Its realization section says:

\[
\text{Császár realizations}=5,
\]

\[
\text{Szilassi realizations}=2,
\]

and the tetrahedron sits as the genus-zero seed.  It also emphasizes the lone-1 asymmetry

\[
1+2+2+2=7.
\]

The page notes two related counting conventions:

\[
5+2=7
\]

for the toroidal realization closure, and

\[
1+5+1=7
\]

when the Szilassi mirror pair is collapsed to one combinatorial type.  The full geometric triad count, however, is

\[
1+5+2=8.
\]

---

## 2. Realization counts as W33 atoms

The Császár realization count is

\[
5=J,
\]

the stabilizer residue / threshold count.

The Szilassi realization count is

\[
2=q-1,
\]

the binary mirror/duality count.

Together they give

\[
5+2=7=\Phi_6.
\]

So the toroidal realization total is exactly the threshold field.

---

## 3. Adding the tetrahedron origin

Now include the tetrahedron seed:

\[
1+5+2=8.
\]

But

\[
8=J^{-1}\pmod{13},
\]

the carrier residue.

Thus the full geometric triad count is

\[
1+\Phi_6=8=J^{-1}.
\]

The realization layer therefore moves from threshold closure to carrier completion by adjoining the genus-zero origin.

---

## 4. Combinatorial-type convention

If the two Szilassi geometric realizations are collapsed to one combinatorial type, then

\[
1+5+1=7=\Phi_6.
\]

So the page contains both counts:

\[
\text{geometric total}=8=J^{-1},
\]

and

\[
\text{combinatorial-type total}=7=\Phi_6.
\]

The difference between them is exactly one:

\[
8-7=1,
\]

the tetrahedral/origin distinction between geometric completion and combinatorial collapse.

---

## 5. Lone-1 as Fano-origin decomposition

CLXVI built the Fano plane from

\[
\{1,5,12,8\}\cup\{3,6,9\}.
\]

Choose the affine origin

\[
1.
\]

The remaining six points split into three direction-pairs:

\[
(5,3),
\]

\[
(12,6),
\]

\[
(8,9).
\]

So the Fano plane decomposes as

\[
7=1+2+2+2.
\]

This is exactly the lone-1 asymmetry described for both the Császár vertex decomposition and the Szilassi face decomposition.

---

## 6. Theorem statement

**The realization data realizes the same threshold/carrier grammar.**  Császár's five realizations are

\[
J=5,
\]

Szilassi's two geometric realizations are

\[
q-1=2,
\]

and their toroidal total is

\[
\Phi_6=7.
\]

Adding the tetrahedron origin gives

\[
1+5+2=8=J^{-1},
\]

the carrier residue.  Collapsing the two Szilassi geometries to one combinatorial type gives

\[
1+5+1=7=\Phi_6.
\]

---

## 7. Why this matters

The realization data is not merely suggestive.  It supplies a physical/geometric version of the same algebraic transition:

\[
\text{threshold closure } \Phi_6=7
\quad\longrightarrow\quad
\text{carrier completion } J^{-1}=8.
\]

The tetrahedron seed is the origin that performs the completion.

The page's lone-1 asymmetry is also now identified with the Fano-origin decomposition:

\[
\text{origin} + 3\text{ direction-pairs}
=1+2+2+2=7.
\]

---

## 8. Regression status

Local validation of the CLXXI test file:

```text
5 passed in 0.04s
```

The tests verify:

1. realization counts generate \(\Phi_6\) and carrier residue,
2. combinatorial/geometric count distinction,
3. carrier transition identities,
4. Fano-origin decomposition,
5. audit-level consistency.

---

## 9. Next move

The next target is to make the realization layer dynamical: the pair

\[
\Phi_6=7
\quad\to\quad
J^{-1}=8
\]

is exactly the same one-step transition seen in the decimal and mod-12 wheel: 7 is the cyclic denominator/torus solution, and 8 is the carrier/inverse residue immediately after it.  This may define the geometric realization step from toroidal threshold to carrier completion.
