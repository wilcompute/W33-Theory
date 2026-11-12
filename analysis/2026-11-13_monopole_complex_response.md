# The complex W33 monopole response suppresses its phase curvature

The finite-radius W33 monopole adjusts primarily through its matter profiles when the adjoint superpotential phase is varied. On the 160-element mesh the frozen-core curvature of its energy is 0.654510 in the repo normalization. Solving the odd scalar response reduces it to 0.101176. The adjustment accounts for about 84.5 percent of the frozen curvature. This is the curvature of the monopole rest energy along the supplied coupling, evaluated locally at the real reference point. [Phase force and real-core matching](2026-11-13_monopole_adjoint_shooting.md)

## Stationary response and gauge check

Write the scalar fields as `X(φ)=X₀+iφ η+O(φ²)` at fixed radial gauge and fixed vacuum at r=5. Let K denote the finite-element half Hessian in the conjugation-odd sector, and let f be the assembled derivative of the imaginary scalar force with respect to φ. The static energy divided by 4π has the quadratic terms

```text
1/2 E_frozen'' φ² + φ fᵀ ξ + ξᵀ K ξ,
```

where ξ is the imaginary scalar displacement. Thus the response solves Kη=−f/2. The odd magnetic amplitude has no force and vanishes in this response. The scalar force uses the full native mixed and trace F covectors, integrated with the same quadratic elements and five-point quadrature as the stationary background. The energy check evaluates the holomorphic F terms at complex fields and computes the D moments with Hermitian conjugates. [Conjugation-odd half Hessian](2026-11-11_monopole_phase_hessian.md)

The ten compact imaginary generators have an eight-dimensional vacuum orbit. The two generators fixing the boundary vacuum also fix the computed radial background, with kinetic Gram eigenvalues below 4×10⁻³⁰. Consequently they supply no active global displacement constraint in the recorded runs. The local force annihilates all ten gauge tangents at the quadrature points. If T is one of the real generators obtained after stripping i from the compact action, the linearized radial current in radial gauge is

```text
r² [ <T X₀, η'> − <T η, X₀'> ].
```

Gauge invariance and the stationary equations make this current constant in the continuum, and regularity sets the constant to zero. The finite-element current gives an independent numerical check of the radial connection equation. It decreases from 3.12×10⁻⁶ at 60 elements to 3.62×10⁻⁷ at 160. The finest scaled linear residual is 2.74×10⁻⁹ or less.

## Curvature check

The relaxed curvature equals `E_frozen''+fᵀη` in the divided-by-4π normalization. The full frozen curvature follows from differentiating the trace–mixed interference with the fields held fixed. The table restores 4π throughout.

| Elements | Frozen curvature | Response correction | Relaxed curvature |
| ---: | ---: | ---: | ---: |
| 60 | 0.654419 | −0.553269 | 0.101150 |
| 100 | 0.654507 | −0.553332 | 0.101175 |
| 160 | 0.654510 | −0.553334 | 0.101176 |

Direct centered differences of the complex-field energy along `X₀+iφ η` agree with the linear-response curvature. At φ=0.001 the finest mesh gives 0.10117582. The maximum nodal matter response norm per radian is 0.272089, while the adjoint norm peaks at 0.002814 in the corresponding kinetic coordinates. The imaginary part of the gauge-invariant trace of the family meson made from the second dual and the second fundamental has a peak slope of 0.423710 per radian. This identifies a physical matter response directly through an invariant.

## Change in the adjoint light reflection

The fixed-profile phase law has slope one in arg R. To measure the correction, the shooting calculation differentiates the holomorphic mass with A(φ) and the gauge mass with A(φ)†. It then matches the complex radial system at positive and negative φ using the first-order profile and the exact explicit phase. On the finest mesh, the resulting slopes are 0.999050804 for the color block and 1.000376045 for the weak block. The color partner has the same slope by the residual color symmetry. Each value agrees between phase increments of 0.01 and 0.003 to better than 3×10⁻¹⁰ in the replay. The 60-element results differ from the fine values by about 2.4×10⁻⁶ and 1.1×10⁻⁶ respectively. This resolves a local physical correction to the fixed-profile phase law. A winding calculation around the full circle still requires the finite-phase branch and its scattering conditions. [Radial matching](2026-11-13_monopole_adjoint_shooting.md) · [Reflection slope fixture](../data/toe_20261113_monopole_adjoint_reflection_response.json)

These are finite-radius static results with the same vacuum boundary and real reference profiles used for adjoint shooting. A stationary solution at finite φ requires nonlinear complex continuation. The infinite-domain core and slow exterior tail need separate control. [Neutral exterior modes](2026-11-11_monopole_neutral_tail.md)

Run `python analysis/toe_20261113_monopole_complex_response.py` for the core response and `python analysis/toe_20261113_monopole_adjoint_shooting.py --linear-response` for the reflection derivative. The expanded radial mesh preserves all previously frozen magnetic and adjoint entries and includes the 30 matter coordinates required to evaluate the phase force. [Complete reference mesh](../data/toe_20261113_monopole_adjoint_shooting_mesh.json) · [Nodal response and energy checks](../data/toe_20261113_monopole_complex_response.json)
