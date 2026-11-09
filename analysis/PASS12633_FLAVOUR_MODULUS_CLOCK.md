# Pass 12633: the dark-energy field cannot be the level-3 flavour modulus, and the fixed points do not rescue it

Claude track. Script: `analysis/toe_uv/flavour_modulus_clock.py` (writes `flavour_modulus_clock.json`). Producer: `analysis/w33_pass12633_flavour_clock.py`. Test: `tests/test_w33_pass12633.py`.

**Not a theory of everything.** This closes one door; it is not a construction.

## Question

The corpus's flavour sector is a level-3 modulus: genus-2 Siegel, which reduces to the Γ(3) ≅ A4 modular forms at genus 1 (Passes 11869–11883). The dark-energy fits need a field rolling at φ_N ≈ 0.46 M_P per e-fold today (`dd_clocks.json`). Could that field be the flavour modulus, making one object do both jobs?

## Bound

Atomic clocks bound |μ̇/μ|, giving |d ln μ/dφ| < 2.5×10⁻⁶ per M_P (Lange et al. 2021; `dd_clocks.py`, Pass 12550s). The bound is not new.

## The fixed-point loophole, and why it fails

At an elliptic fixed point, any *smooth* modular-invariant real function is stationary, because the stabiliser rotates the tangent plane and the only invariant gradient is zero. This would remove the linear coupling.

Test:
- **Observable** (a proxy): ln eigenvalue ratios of M†M, where M is Feruglio's A4 weight-2 Weinberg texture (1706.08749).
- **Forms:** the level-3 weight-2 triplet from its divisor-sum q-expansion, checked against the identity Y₂² + 2Y₁Y₃ = 0 to 10⁻¹⁶ at all three points. A first version with a wrong Y₃ normalisation failed this check and was fixed before any result was read.
- **Canonical field:** K = −h ln(2 Im τ), with h = 3 and h = 1.

| sensitivity S = max \|d ln(ratio)/dφ\| (per M_P, h = 3) at distance δ | δ = 10⁻³ | 10⁻² | 10⁻¹ | 0.3 |
|---|---:|---:|---:|---:|
| τ = ω (stabiliser Z₃) | 4.23 | 4.32 | 5.33 | 9.17 |
| τ = i (stabiliser Z₂) | 2000 | 202 | 21.7 | 8.35 |
| generic τ = 0.13 + 1.21i (control) | 7.88 | 8.19 | 13.2 | 33.4 |

**Reading.**
- The residual symmetry forces a degenerate pair at τ = ω and a zero eigenvalue at τ = i, so the ratios are **not smooth** at the fixed points and the stationarity argument does not apply.
- At ω the eigenvalues split linearly with distance, a cone: the sensitivity tends to a constant of about 4 per M_P, with **no suppression**.
- At i, the zero eigenvalue (the mechanism behind fixed-point mass hierarchies) makes the sensitivity grow as about 2/δ, **worse** than a generic point.
- Every case exceeds the clock bound by a factor of at least **1.7×10⁶** (h = 3); h = 1 is larger.

**[N, given the proxy.]** The proxy assumes an O(1) map from these ratios to μ = m_p/m_e, which depends on m_e and on the quark masses through Λ_QCD and the σ-term. A factor-of-10⁶ margin survives any reasonable map.

## Consequence for the structure of a complete theory

1. The flavour modulus must be **stabilised** with m ≫ H₀; its residual drift must be below about 10⁻⁶ of an O(1) roll. The corpus already found that the "magic" supremum sits at a cusp, with no stabilisation from the substrate (P11874–11878). This pass turns that gap into a hard requirement.
2. The dark-energy field is therefore a **separate** object. It couples to dark matter at c′ ≈ 0.05 but to μ at less than 2.5×10⁻⁶, a **dark/visible sequestering ratio below 5×10⁻⁵** that the substrate has to explain. This is a definite target. A mechanism that makes the field's coupling to the visible flavour sector vanish while leaving its coupling to dark matter would be the first positive step.

**Prior art.** The generic statement, that a rolling scalar coupled at O(1) to the Standard Model is excluded by clocks, is textbook (Carroll 1998, "Quintessence and the rest of the world"). The fixed-point hierarchy literature (Novichkov, Penedo and Petcov, 2102.07488; Feruglio et al.) already has mass ratios scaling as |τ − τ*|^k. The one-line consequence, that the hierarchy-producing fixed point maximises clock sensitivity, may be known there. I found no paper combining modular flavour, quintessence and varying constants (one web search), and claim no novelty.
