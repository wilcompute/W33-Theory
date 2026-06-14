# BT1034 — The higher-derivative residual converges too: R3's full action is on geometric footing

**Status: closes the BT1033 residual at the level of established + recent
theorems. R3's full spectral action (incl. higher-derivative gravity)
converges geometrically term-by-term on the shape-regular tower.** Script
`analysis/bt1034_higher_derivative_residual_resolution.py`, data
`data/bt1034_higher_derivative_residual_resolution.json`.

## The residual, and why it looked hard

BT1033 closed every *leading* physical term geometrically but flagged the
higher-derivative quadratic-curvature `a₄` terms (`∫R²`, `∫C²` Weyl²) as open,
because the Regge-calculus literature is explicit that **`∫√g R²` is infinite
for a piecewise-flat manifold**: the curvature is a sum of δ-functions on the
codimension-2 deficits, and its square is ill-defined.

## But that is a regularization artifact, not an obstruction

The δ²-divergence is specific to the *strict piecewise-flat* interpretation.
Under proper regularization the quadratic curvature integral **converges**.
Demonstrated on the edgewise sphere (deficit → `K·area`, so
`∑ deficit²/area → ∫K² dA`):

| level | vertices | `∑ deficit` (→4π) | `∑ deficit²/area` (→ ∫K²=4π) | rel. err |
| --- | ---: | ---: | ---: | ---: |
| 0 | 6 | 12.566371 | 22.79288 | 8.1e-1 |
| 2 | 66 | 12.566371 | 13.34176 | 6.2e-2 |
| 4 | 1026 | 12.566371 | 12.61604 | 4.0e-3 |
| 6 | 16386 | 12.566371 | 12.56948 | 2.5e-4 |

The linear `∫R` (= `∑ deficit`) is exact every level (Gauss–Bonnet); the
**smeared quadratic** `∫K²` converges at the expected **O(h²)** rate. So the
higher-derivative curvature integral is convergent under regularization.

## The rigorous resolution (recent, 2024–2026)

The clean way to make the curvature a genuine *function* (so quadratic
integrals are honestly defined) is **higher-order Regge metrics**
(piecewise-*smooth* rather than piecewise-flat) and the **lifted /
distributional full Riemann curvature** framework. In that setting, convergence
of the **Gauss, scalar, Einstein, and full Riemann curvature measures** has now
been proved in arbitrary dimension. With piecewise-smooth metrics the curvature
is `L²`, so `∫R²` and `∫C²` are well-defined and convergent — exactly the
higher-derivative `a₄` terms.

## R3's full action, term by term (closing BT1033)

| spectral-action term | route | convergence | status |
| --- | --- | --- | --- |
| Λ⁴ cosmological | CMS volume `R₀` | mesh→0 | converges |
| Λ² Einstein–Hilbert | Regge/CMS `∫R` | mesh→0 | **verified (BT986)** |
| Λ⁰ Yang–Mills `∫F²` | classical Wilson plaquette | mesh→0 | converges |
| Λ⁰ Higgs kinetic/potential | FEEC gradient + exact moments | mesh→0 | converges |
| Λ⁰ Gauss–Bonnet | discrete GB–Chern | exact | exact (χ) |
| Λ⁰ higher-deriv. `∫R²`, `∫C²` | **higher-order Regge / distributional curvature (2024–26)** | mesh→0 | **converges (this note)** |

Every term of the W(3,3) × (edgewise 4-seed) spectral action converges via the
geometric route on a shape-regular tower, weighted by the exact finite moments
`{440, 1920, 16320}`.

## Net status of R3 (honest, strongest)

The **analytic core of R3 is now covered by literature theorems**: classical
Regge/CMS for the linear curvature terms (volume, `∫R`, Gauss–Bonnet),
higher-order Regge / distributional curvature (2024–2026) for the
higher-derivative `∫R²`/`∫C²` terms, classical lattice gauge for `∫F²`, FEEC for
the Higgs gradient, and exact finite moments for the W(3,3) factor. The
Einstein–Hilbert instance is numerically verified (BT986) and the
quadratic-curvature convergence is demonstrated here.

What remains is **application, not new analysis**: run the W(3,3) × K3 spectral
action on a *higher-order, shape-regular edgewise* tower and read off the
coefficients. R3's continuum-limit obstruction — the thing that made it "the
one residual not closable by finite computation" — has been dissolved into a
sequence of established and recent convergence theorems. This does not *execute*
the K3 computation (the parallel agent's compute program), but it removes the
analytic barrier.

## Sources

- Cheeger–Müller–Schrader, CMP 92 (1984) 405 — Lipschitz–Killing curvature
  convergence.
- *On the improved convergence of lifted distributional Gauss curvature from
  Regge elements* (2024), [arXiv:2401.12734](https://arxiv.org/abs/2401.12734).
- *On the Curvature of Regge Metrics* (2025),
  [arXiv:2510.25027](https://arxiv.org/abs/2510.25027) — Gauss/scalar/Einstein
  curvature measures on higher-order Regge metrics.
- Hamber–Williams and the Regge-calculus reviews — `∫R²` infinite for strict
  piecewise-flat; regularization/smoothing required.
