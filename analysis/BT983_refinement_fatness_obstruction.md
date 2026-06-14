# BT983 — The R3 refinement-fatness obstruction, and the fat-tower fix

**Status: genuine advance on R3 (continuum lift). Not a closure — a correction
of the route plus a reduction of the curvature half to a known theorem.**
Script `analysis/bt983_refinement_fatness_obstruction.py`, data
`data/bt983_refinement_fatness_obstruction.json`.

## The setup

R3 (the sole remaining open) asks: prove the refinement tower's spectral
action / Regge curvature converges to the continuum Einstein–Hilbert action.
The corpus names the tools — Cheeger–Müller–Schrader (CMS) curvature
convergence and Dodziuk–Patodi (Whitney-form) spectral convergence — and uses
a **barycentric** refinement tower.

## The obstruction (internet-checked + numerically verified)

Both CMS and Dodziuk–Patodi carry a **fatness / shape-regularity** hypothesis:
the mesh sequence must keep its simplex quality (minimal angle / fatness)
bounded away from zero as the mesh width → 0. The literature is explicit that
**barycentric subdivision fails this** — "with barycentric subdivision,
dihedral angles decrease by half at each iteration, so fatness cannot be kept
fixed." We confirm it numerically on a 2-simplex (equilateral seed):

| level | barycentric min-angle | edgewise min-angle |
| --- | --- | --- |
| 0 | 60.0° | 60.0° |
| 1 | 30.0° | 60.0° |
| 2 | 13.9° | 60.0° |
| 3 | 6.3° | 60.0° |
| 4 | 2.9° | 60.0° |
| 5 | 1.3° | 60.0° |

So **the barycentric refinement tower does not satisfy the hypotheses of the
very theorems R3 relies on** — CMS and Dodziuk–Patodi do not apply to it.

## The fix: a shape-regular (fat) tower

The **edgewise (Freudenthal–Kuhn)** subdivision is provably shape-regular:
"the fatness of simplices in the subdivision is independent of k", and "the
shape regularity constant remains bounded away from zero as more refinements
are performed." Numerically its minimal angle is **constant** (above). On the
edgewise tower the fatness + (mesh → 0) hypotheses hold, so **both CMS and
Dodziuk–Patodi apply**.

## The reframe: EH = a₂ = ∫R = Regge, converges by CMS

The Einstein–Hilbert term of the spectral action is the $a_2$ Seeley–DeWitt
coefficient $\propto \int R\sqrt g$. Its piecewise-flat incarnation is exactly
the **Regge deficit-angle action** — the $n=2$ Lipschitz–Killing curvature,
the original Regge case of CMS. Cheeger–Müller–Schrader proved these
combinatorial curvatures converge (in the sense of measures) to the smooth
curvature integrals on a fat tower. Therefore, on the edgewise tower, **the
gravitational (Einstein–Hilbert) convergence is the CMS theorem, not an open
problem.**

## What this changes, honestly

- **Corrects the route:** R3 must use the **edgewise/Freudenthal–Kuhn** tower,
  not the barycentric one; the latter provably fails the convergence
  hypotheses.
- **Reduces the curvature half to a theorem:** on the fat tower, the EH (and
  lower Lipschitz–Killing) curvature integrals converge by CMS — the geometric
  (Regge) route to the gravitational action is essentially settled.
- **Narrows the residual to one analytic step:** the *spectral-action* (heat-
  trace) realization of $a_2$ requires interchanging the short-time
  heat-kernel limit (which produces $a_2$) with the refinement limit
  (level → ∞). The geometric/Regge route *bypasses* this interchange; the
  spectral-action route still needs it. This limit-interchange is now the
  precise, isolated analytic residual of R3.
- **Even the spectral route is within reach on the fat tower:**
  finite-element exterior calculus (Arnold–Falk–Winther) + Dodziuk–Patodi give
  convergence of the combinatorial Hodge–Laplacian eigenvalues to the de Rham
  spectrum **under shape regularity** — so on the edgewise tower, taking
  $n\to\infty$ before $t\to0$ reproduces the continuum heat trace and its $a_2$.
  **Structural upshot:** the obstruction to R3 was the *choice of refinement*
  (a non-shape-regular tower), not the almost-commutative framework. On a
  shape-regular tower, both the geometric (CMS) and spectral (FEEC/
  Dodziuk–Patodi) routes are governed by established convergence theorems, and
  R3 reduces to applied verification on the CP²₉/K3₁₆ seeds.

## Open (sharpened)

1. Re-run the corpus's CP²₉/K3₁₆ refinement program on the **edgewise** tower
   (so CMS/Dodziuk–Patodi apply) instead of barycentric.
2. The spectral-action limit-interchange (short-time ↔ refinement), or adopt
   the geometric/Regge definition of the gravitational action, on which CMS
   closes the convergence.

Sources: Cheeger–Müller–Schrader, *On the curvature of piecewise flat spaces*,
Commun. Math. Phys. 92 (1984) 405; Edgewise subdivision (Freudenthal 1942;
Edelsbrunner–Grayson, *Edgewise subdivision of a simplex*, Discrete Comput.
Geom. 2000); Dodziuk–Patodi (Whitney-form Laplacian convergence).
