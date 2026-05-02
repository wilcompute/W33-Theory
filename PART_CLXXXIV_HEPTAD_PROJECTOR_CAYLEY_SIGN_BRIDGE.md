# Part CLXXXIV — Heptad Projector / Cayley Sign Bridge

**Date:** 2026-05-02  
**Status:** structural sign-capacity theorem; projector Gram/sign extraction artifact needs regeneration

---

## 1. Starting point

CLXXXI ranked the third bridge as:

\[
\text{projector heptad}\to\text{Cayley signs}.
\]

The source file `exploration/w33_toroidal_heptad_projector_bridge.py` states that the seven toroidal realizations give rank-3 shell projectors, span a 7-dimensional heptad, leave an exact 6-dimensional centered shell after mean subtraction, refine as \(4+1+1=6\), refine fully as \(4+3=7\), match the six bivectors in four dimensions, and have toroidal genus numerator 12 as the orientation double cover of the 6D shell.  fileciteturn329file0

The generated summary file `data/w33_toroidal_heptad_projector_bridge_summary.json` is not currently committed on master, so CLXXXIV does not claim explicit projector Gram eigenvalues beyond the source-file structural theorem.

---

## 2. Projector heptad

The seven toroidal realizations split as

\[
5+2=7.
\]

The five Császár realizations give

\[
5=J,
\]

and the two Szilassi realizations give

\[
2=q-1.
\]

Together:

\[
5+2=7=\Phi_6.
\]

These seven rank-3 projectors supply the seven Fano/Cayley imaginary units.

---

## 3. Mean line and scalar origin

The projector heptad has a mean line:

\[
1.
\]

Subtracting it leaves

\[
7-1=6.
\]

This matches the scalar-plus-imaginary decomposition of the Cayley carrier:

\[
1+7=8.
\]

And

\[
8=J^{-1}.
\]

So the projector mean line plays the same role as the scalar/origin completion in the octonion algebra.

---

## 4. Centered shell and bivectors

The centered projector shell has dimension

\[
6=2q.
\]

It also matches

\[
\binom42=6,
\]

the dimension of bivectors in four dimensions.

The refinement is

\[
4+1+1=6.
\]

Here:

- \(4\) is the centered Császár family shell,
- \(1\) is the centered Szilassi mode,
- \(1\) is the primal-dual family separation mode.

The full heptad refines as

\[
4+3=7.
\]

---

## 5. Orientation double cover

The centered shell has orientation double cover

\[
2\cdot6=12.
\]

But

\[
12=k.
\]

This is exactly the mod-12 sign/phase wheel needed for oriented Fano/Cayley multiplication.

So the projector geometry has the correct sign capacity:

\[
6\text{ bivector directions}
\quad\to\quad
12\text{ oriented sign/phase directions}.
\]

---

## 6. Fano multiplication capacity

The seven heptad residues are

\[
\{1,5,12,8,3,6,9\}.
\]

The Fano line system contains seven triples:

\[
(1,5,3),
\]

\[
(12,8,3),
\]

\[
(1,12,6),
\]

\[
(5,8,6),
\]

\[
(1,8,9),
\]

\[
(5,12,9),
\]

\[
(3,6,9).
\]

These seven lines cover all unordered pairs:

\[
\binom72=21
\]

exactly once.

That is the combinatorial skeleton required for octonion multiplication: each pair of imaginary units multiplies to the third unit on its unique Fano line, with sign determined by orientation.

---

## 7. What is proved now vs what remains measured

### Proved structurally

The projector data has the exact sign capacity needed for the Cayley algebra:

\[
7\text{ projectors}=7\text{ imaginary units},
\]

\[
1\text{ mean line}=1\text{ scalar origin},
\]

\[
6\text{ centered dimensions}=\binom42\text{ bivectors},
\]

\[
12=2\cdot6\text{ oriented sign/phase cover}.
\]

### Still needs regeneration

We still need to determine whether the realization projectors uniquely select the same Fano sign convention used in CLXXIV.

That requires regenerating:

```bash
python exploration/w33_toroidal_heptad_projector_bridge.py
```

and committing:

```text
data/w33_toroidal_heptad_projector_bridge_summary.json
```

Then measure:

1. projector overlap matrix,
2. centered Gram eigenvectors/eigenvalues,
3. family separation orientation,
4. whether Gram parity determines Fano line signs,
5. residual between projector-induced signs and Cayley signs.

---

## 8. Theorem statement

**Structurally, the toroidal projector heptad has exactly the sign capacity required by the Fano-Cayley algebra.**  The seven projectors supply the seven imaginary units; the mean supplies the scalar origin; the centered 6D shell matches the \(\binom42\) bivector space; and its orientation double cover

\[
12=2\cdot6
\]

supplies the sign/phase wheel.  The Fano line system covers all

\[
21=\binom72
\]

unordered pairs exactly once, giving the required octonion multiplication skeleton.

Numerical projector-Gram extraction is still needed to decide whether the realizations determine the signs uniquely.

---

## 9. Why this matters

This is the careful bridge from geometry to algebra.

Compatibility is already exact.  Derivation is the next measurement.

The projector heptad is not just seven pictures or seven counts.  It has precisely the right operator dimensions to become the Fano/Cayley carrier:

\[
\text{toroidal projectors}
\to
\text{Fano signs}
\to
\mathbb O
\to
J_3(\mathbb O).
\]

---

## 10. Regression status

Local validation of the CLXXXIV test file:

```text
7 passed in 0.04s
```

The tests verify:

1. projector heptad family split,
2. centered and full refinements,
3. bivector/orientation/Cayley completion,
4. Fano pair coverage,
5. tool/artifact registry,
6. threshold/carrier inverse,
7. audit-level consistency.

---

## 11. Next move

The next target is the fourth-ranked bridge from CLXXXI:

\[
45\text{ quotient points as cubic triads.}
\]

The goal is to connect the quotient/packet transport family to the E6 cubic split:

\[
45=36+9
\]

and the Albert generation:

\[
27=J_3(\mathbb O).
\]
