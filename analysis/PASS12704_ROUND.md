# Pass 12704: SO(10) vacua with a 45 + 210 leave exactly Q + U light, a 210 alone never does; A's leptogenesis works for an O(2)-breaking splitting 10⁻¹² ≲ ΔM/M ≲ 10⁻⁵ or tan β ≳ 1.6–3 with the τ on the PQ doublet; dark-graviton DM narrows B to y′ ≈ 0.51–0.53; FCC separates B from the hybrid at 4–10σ for M_SS ≥ 3×10⁹–3×10¹⁰ GeV

Claude track. Follows Pass 12703. **Not a theory of everything.** Script: `toe_pass12704_round.py`; certificate: `data/toe_pass12704_round.json`; tests: `tests/test_toe_pass12704.py`.

**Correction to Pass 12701.** The degeneracy A needs is ΔM/M ≲ 10⁻⁵, not 10⁻⁴–10⁻³. The earlier R = ε/ε_DI estimate was optimistic by 10–100× (item 3).

## (1) SO(10) truncation: which vacua leave only Q + U light

The setup:
- the SO(10) Clifford algebra, built explicitly with 32×32 Γ matrices;
- the 16, identified state by state through Y and B − L;
- the SM singlets of the 210 and the 45, found numerically as block-scalar operators on the 16: **3 and 2** directions;
- the invariants, computed directly.

The 210 directions are p = e₆₇₈₉, a = the color 4-form, and ω = J₆ ∧ (e₆₇ + e₈₉). The 45 directions are B − L and T3R. The invariants come out as **I₂ = 24(p² + 3a² + 6ω²)** and **I₃ = 48(a³ + 6aω² + 3pω²)**, which is the standard minimal-SO(10) form. The mixed term is 45·45·210 = 24A²a + 48ABω + 8B²p.

Mass patterns on (Q, u^c, d^c, L, e^c, ν^c):

| direction | Q | u^c | d^c | L | e^c | ν^c |
|---|---|---|---|---|---|---|
| p (210) | 1 | −1 | −1 | 1 | −1 | −1 |
| a (210) | 1 | 1 | 1 | −3 | −3 | −3 |
| ω (210) | 0 | −2 | 2 | 0 | −6 | 6 |
| B − L (45) | 1 | −1 | −1 | −3 | 3 | 3 |
| T3R (45) | 0 | −2 | 2 | 0 | 2 | −2 |

**A 210 alone (W = m·210² + λ·210³), all six F-flat vacua.** In every vacuum, Q is degenerate with Q + u^c + d^c (all quarks), with the SU(5) 10 (Q + u^c + e^c), with the flipped 10 (Q + d^c + ν^c), with everything, or with nothing. **No vacuum isolates Q + U.**

**A 45 + 210 (W = m₁·45² + m₂·210² + λ·210³ + κ·45²·210).** For three parameter sets there are real vacua where 16̄(M + η₄₅·45 + η₂₁₀·210)16 has **Q = U = 0 with d^c, L, e^c, ν^c all heavy**. An example: p = a = −1, ⟨45⟩ along T3R = ±2√3, ω = 0, which preserves SU(3)×SU(2)×U(1)_R×U(1)_{B−L}. The other states come out at 4, 4, 8, 4 in units of η₂₁₀. It needs two tunings (M and η₄₅) to the TeV/M_heavy level.

**E₆ reading (not computed in E₆).** The 650 contains both an SO(10) 45 and a 210, but they enter 27̄·27·650 through one coupling. The independent 45 coupling would then have to come from 27̄·27·78 with a **78 VEV along a non-ψ direction**, for example T3R, or from a second 650. The other track's vacuum (adjoint along ψ only) does not supply it.

## (2) A with the τ on the PQ doublet

Pass 12703 needs y_τ ≥ 1.84× SM for radiative-only leptogenesis. If the τ couples to the PQ-charged doublet, y_τ = y_τ^SM / cos β. The Y_e term in the running of the neutrino Yukawa is −3/2 = +1/2 (lepton wave function) − 2 (vertex, present only if N and τ share the doublet).

| case | y_τ needed | tan β |
|---|---|---|
| N and τ on the same doublet (−3/2) | ≥ 1.84× SM | **≥ 1.55** |
| N on the other doublet (+1/2) | ≥ 3.19× SM | **≥ 3.0** |

At 1.15× the threshold, 3–4% of points reach η_B ≥ 6.1×10⁻¹⁰.
- The cost is the axion. Charging b and τ with the same sign gives E/N = 8/3, N_DW = 1 and g_aγγ = 0.39 g_KSVZ, so haloscopes need **×44 the scan time** (Pass 12696). b alone gives ×5.6.
- At tan β ~ 2–3 and multi-TeV H₂, LHC H/A → ττ searches are not sensitive (they bite at large tan β).

## (3) A tree-level O(2)-breaking splitting

The model adds δ = (M₂ − M₁)/M with a random orientation on top of the radiative running (SM y_τ, Λ = M_GUT; 600 points per value):

| δ | median ΔM/Γ | fraction with η_B ≥ obs |
|---|---|---|
| 10⁻¹⁴ | 4 | 0 |
| 10⁻¹³ | 4 | 0.2% |
| 10⁻¹² | 4 | 64% |
| 10⁻¹⁰–10⁻⁷ | 4–90 | ≥ 99.7% |
| 10⁻⁶ | 850 | 97% |
| 10⁻⁵ | 9×10³ | 81% |
| 10⁻⁴ | 9×10⁴ | 0.2% |

- **Window: 10⁻¹² ≲ δ ≲ 10⁻⁵.** Any O(2) breaking in this range works generically.
- If the breaking is a power of the charged-lepton spurion y_τ ≈ 0.01, then δ ~ y_τ^n with n ≈ 2.5–6.
- The upper edge corrects Pass 12701's 10⁻⁴–10⁻³. Off resonance, ε ≈ (Γ/M)/δ, with Γ/M ≈ 8×10⁻¹⁰.

## (4) B with dark-graviton dark matter

In the dark dimension, dark matter is KK gravitons whose mass cascades down to ~1–100 keV today ([Gonzalo–Montero–Obied–Vafa 2209.09249](https://arxiv.org/abs/2209.09249)). The astrophysical analysis of [Law-Smith–Obied–Prabhu–Vafa 2307.11048](https://arxiv.org/abs/2307.11048) puts the natural effective radius at **1–30 μm**. Its eqs. (42)–(43) need ℓ₅ ≳ 20 μm (δ/0.5)(λ/0.1)^{2/3}; this was read from a summary of the paper and should be checked against the PDF.

| R | M₅ | m_KK | y′ (two loop, M_VL = 1.65 TeV) | m_DM(today) relative to 1 μm |
|---|---|---|---|---|
| 0.1 μm | 1.2×10⁹ | 2.0 eV | 0.495 | ×1.39 |
| 1 μm | 5.7×10⁸ | 0.20 eV | 0.508 | 1 |
| 10 μm | 2.7×10⁸ | 20 meV | 0.522 | ×0.72 |
| 20 μm | 2.1×10⁸ | 10 meV | 0.527 | ×0.65 |
| 30 μm | 1.8×10⁸ | 7 meV | 0.530 | ×0.62 |

- With the dark-graviton dark matter included, **B narrows to y′ = 0.508–0.530**, or 0.527–0.530 at the paper's natural couplings.
- The dark-matter mass today varies only as m_KK^{1/7}, so it barely constrains R.

## (5) FCC forecast

The inferred scale μ₀ of the quartic zero. Derivatives at the hybrid point: dy′/dM_t = −0.049/GeV, dy′/dα_s = +18, dy′/dlog₁₀μ₀ = −0.028. The B point at 1 μm: −0.039, +14, −0.042.

| inputs | σ(y′) | σ(log₁₀ μ₀) |
|---|---|---|
| today (M_t ±0.29, α_s ±0.0009, y′ ±0.002, theory ±0.002) | 0.022 | 0.78 |
| FCC-ee + FCC-hh (M_t ±0.04, α_s ±0.0002) | 0.005 | **0.18** |

Separation of the hybrid (μ₀ = M_SS) from B (μ₀ = M₅) with FCC:

| hybrid M_SS | B with R ≥ 0.1 μm | B with R ≥ 1 μm (dark-graviton DM range) |
|---|---|---|
| 3×10⁹ | 2.2σ | 4.0σ |
| 10¹⁰ | 5.1σ | 6.9σ |
| 3×10¹⁰ | 7.7σ | 9.6σ |

Today's inputs give at most 2σ. So FCC-ee + FCC-hh decide between B and the hybrid if M_SS ≳ 10¹⁰ GeV, which is also where the hybrid unifies best (δ ≈ 0 at about 2×10¹⁰).

## Status

- **A** works with an O(2)-breaking splitting 10⁻¹²–10⁻⁵ (generic), or with tan β ≳ 1.6–3 and τ PQ charge (E/N = 8/3, harder haloscope).
- **B:** y′ = 0.51–0.53 with dark-graviton dark matter.
- **Hybrid:** needs a non-ψ 78 VEV (or a second 650) alongside the 650 at the SO(10) level, and M_SS ~ 10¹⁰ to be distinguishable.

All three remain conditional.
