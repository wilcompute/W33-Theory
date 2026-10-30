# Pass 1031 — Dual degree-120 phase carriers

**Certificate:** `analysis/w33_pass1031_dual_120_phase_carriers.py` →
`data/w33_pass1031_dual_120_phase_carriers.json` (`23/23`, deterministic,
standard-library Python).

## Question closed

Pass 1028 exposed two objects with the same coarse parameters:

\[
120=40\cdot3,
\qquad
|\operatorname{Stab}|=216.
\]

They are:

1. the 120 E8 antipodal pairs, arranged as three residual phases over each
   W33 **point**;
2. the 120 golden-selector sheets, arranged as three phases over each W33
   **line**.

Equal degree and equal stabilizer order do not identify transitive group actions.
Pass 1031 computes the stabilizers themselves.

## Exact construction

The verifier reconstructs

\[
G=PSp(4,3),\qquad |G|=25920,
\]

from the 40 projective symplectic transvections of \(W(3,3)\). At a point, the
four incident lines have three perfect matchings. At a line, its four points have
three perfect matchings. These are the canonical local three-phase carriers.

The point and line base stabilizers both have order

\[
648.
\]

Stabilizing one local phase gives order

\[
216,
\]

and therefore degree

\[
25920/216=120
\]

on both sides.

## Nonconjugacy certificate

The point-phase stabilizer has orbit profiles

\[
\text{points}: [1,12,27],
\qquad
\text{lines}: [4,36].
\]

The line-phase stabilizer has the exact dual profiles

\[
\text{points}: [4,36],
\qquad
\text{lines}: [1,12,27].
\]

Equivalently, the first subgroup fixes one point and no line, while the second
fixes one line and no point.

Conjugate subgroups have identical orbit profiles in every fixed \(G\)-action.
Therefore the two order-216 stabilizers are not conjugate, and

\[
G/H_{\rm point}
\not\cong
G/H_{\rm line}
\]

as transitive degree-120 \(PSp(4,3)\)-sets.

## Local phase groups differ too

The local point stabilizer acts on its three matchings as a regular

\[
C_3,
\]

and its derived subgroup has order \(216\). This matches the normal residual-C3
phase quotient of the E8 pair carrier.

The local line stabilizer acts on its three matchings as the full

\[
S_3,
\]

and its derived subgroup has order \(324\). This matches the selector-side local
\(S_3\) quotient already certified by Pass 341.

Thus the difference is deeper than point-versus-line naming: the local controller
is cyclic on the E8 side and dihedral/symmetric on the selector side.

## Correct crosswalk

The two 120-carriers are a **dual pair**:

- same degree;
- same fibre size;
- same stabilizer order;
- opposite point/line orbit orientation;
- different local phase images.

They are not one shared carrier. The pending Pass-1026 GAP diagnostic should
therefore return `degree120_actions_conjugate = false`.

## Boundary

This theorem identifies the natural finite group actions. It does not supply an
outer duality operator. For odd \(q=3\), no incidence-preserving point-line
duality exists inside the verified substrate.
