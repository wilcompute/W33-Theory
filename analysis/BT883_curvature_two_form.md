# BT883 — The Curvature 2-Form: A Quaternionic Field Strength on the Matter Graph

**Status: PROVEN (machine-verified, `analysis/bt883_curvature_two_form.py`, data `data/bt883_curvature_two_form.json`)**

The field strength of the gauge connection (BT882). The discrete curvature
2-form is the commutator F(p,q) = [R_p, R_q] of the two points' generation
centers, and it has a clean valued structure.

## The theorems

- **T1:** F(p,q) = identity for all 12 collinear partners — the gauge
  connection is **flat (zero curvature) on collinear edges** (the generation
  symmetries commute on a line).
- **T2:** F(p,q) for the 27 non-collinear partners is an **order-4 element of
  SL(2,3) = 2T** — a quaternion unit (one of the 6 order-4 Hurwitz units
  ±i,±j,±k), with **F² = −I the central involution**. The field strength is
  valued in the **imaginary-quaternion units of the 24-cell group 2T**,
  squaring to its center.
- **T3:** holonomy around the loops — a W(3,3) **line** (4 collinear points,
  all pairs commuting) is **gauge-flat** (no curvature in causal/gauge
  directions); a **matter triangle** (3 mutually non-collinear points of Q)
  has order-4 curvature on every edge.

## Reading

The substrate's gauge field strength is an **su(2)-valued (quaternionic)
2-form supported exactly on the matter graph Q**:

- **flat on collinearity** — the causal/gauge directions (the W(3,3) lines,
  the timetable/measurement structure) carry zero curvature;
- **curved on non-collinearity = matter** — every matter pair carries an
  order-4 quaternion-unit curvature F ∈ {±i,±j,±k} ⊂ 2T, with F² = −I.

That the field strength lands in the imaginary quaternions of the 24-cell
group is striking: the imaginary quaternions are the Lie algebra su(2), so the
substrate's discrete curvature is **su(2)-valued** — the field strength of the
weak/non-abelian gauge sector — and it lives on the same matter graph Q whose
spanning-tree gravity (BT873) carries the gauge dimension. Curvature, matter,
and the 24-cell group are one object; flatness is causality.

## The closed gauge arc (BT876–883)

```text
gauge group   C(R) = 1⊕3⊕8 = SU(3)×SU(2)×U(1)        (BT876)
generations   = Z(gauge group) = Z₃                   (BT880)
parity        = W/Q duality (A₄→S₄)                   (BT877)
spacetime     = 40 local gauge groups (homogeneous)   (BT881)
connection    flat on edges (Z₃²), curved on Q (2T)   (BT882)
curvature     F = [R_p,R_q] ∈ quaternion units of 2T  (BT883)
```

## Open

- Sum the curvature over an apartment (octagon, the Tits-building loop) — the
  substrate's integrated field strength / instanton number.
- The quaternion-unit assignment p ↦ which of ±i,±j,±k: a map from the matter
  graph Q to the 6 order-4 units — is it the 3 weak-isospin/color axes?
