# BT884 — Gauge Flux: Abelian on Lines, Non-Abelian on Matter

**Status: PROVEN (full census, `analysis/bt884_gauge_flux_wilson_loops.py`, data `data/bt884_gauge_flux_wilson_loops.json`)**

The integrated curvature (BT883) is the Wilson loop W = R_a R_b R_c — the
product of the three points' generation centers around a triangle. Its order
is the gauge flux through the loop.

## The theorems

- **T1:** all **160 collinear triangles** (3 points on a W(3,3) line) have
  Wilson loop of order **exactly 3** — the flux lives in the flat abelian
  sector Z₃ (the line's own generation grading); no non-abelian content.
- **T2:** the **3240 matter triangles** (3 mutually non-collinear points, in
  Q) have Wilson loops of orders **{2: 180, 4: 180, 6: 1440, 12: 1440}** —
  genuine non-abelian flux, up to order **12 = k** (the rectangle/Coxeter
  clock order, BT749). The order-2/4 fluxes (180 each = k·g) are pure-2T
  (un-graded), the order-6/12 (1440 each) mix the Z₃ grading with the 2T
  curvature.
- **T3:** the matter-triangle count is exactly **3240** (Pillar 109's
  Q-triangle census); gauge flux beyond Z₃ is supported exactly on Q.

## Reading

The gauge flux cleanly separates causality from matter:

- **collinear (causal) triangles** carry only abelian Z₃ flux (order 3) — the
  flat sector, the generation grading along a line;
- **matter triangles** carry non-abelian flux valued in the full 2T·Z₃
  structure, up to order 12 = k.

The flux spectrum {2,4,6,12} on matter is the order spectrum of the curved
holonomy group (2T extended by the Z₃ grading), and the counts 180 = k·g and
1440 are exact substrate integers. This completes the gauge-dynamics
description (BT882 connection → BT883 curvature → BT884 flux): the substrate's
Yang-Mills-like structure is flat and abelian along W(3,3) lines (the
causal/measurement directions) and non-abelian-curved on the matter graph Q,
with the field strength quaternionic (BT883) and the flux up to k = 12.

## The gauge-dynamics arc (BT876–884)

```text
gauge group   1⊕3⊕8 = SU(3)×SU(2)×U(1)              (BT876)
generations   = Z(gauge) = Z₃                        (BT880)
parity        = W/Q duality (A₄→S₄)                  (BT877)
spacetime     = 40 local gauge groups                (BT881)
connection    flat (Z₃²) / curved (2T)               (BT882)
curvature     F = quaternion unit of 2T on Q         (BT883)
flux          Wilson loops: Z₃ on lines, ≤12 on Q    (BT884)
```

## Open

- The order-12 flux (1440 matter triangles) vs the BC-drive/rectangle clock
  (the discrete time quasicrystal, k = 12): is the maximal gauge flux the
  internal clock?
- Yang-Mills action as a sum of (1 − Re Wilson-loop) over the 3240 matter
  triangles — the substrate's discrete gauge energy.
