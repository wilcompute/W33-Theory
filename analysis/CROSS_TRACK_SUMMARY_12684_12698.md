# Cross-track summary, Passes 12684–12698 (Claude track): the Higgs-quartic intermediate scale and its two completions

For citation by the other track. Everything here is numerical model analysis with stated scope. **None of it is a theory of everything.**

## Validated tool

`toe_pass12685_intermediate_scale_suite.py` provides `run()` / `mu0()`:
- SM running at two loops plus the leading three-loop QCD terms;
- Buttazzo et al. NNLO matching;
- reproduction of the published three-loop λ(M_Pl) fit to ≤ 1.6×10⁻⁴ (Pass 12687);
- options for vectorlike quarks and seesaw Yukawas.

## Results to cite

| result | pass |
|---|---|
| λ(M₅) = 0 for a micron dark dimension needs M_t = 174.4–175.1 GeV (no new states) | 12684 |
| λ = 0 at √(v M_Pl) needs M_t = 172.57; the 2025 lattice axion f_a window needs 172.35–172.44; look-elsewhere 12% | 12684 |
| a vectorlike top partner with y′ = 0.51 ± 0.02 (nearly independent of R) restores λ(M₅) = 0; ΔT < 10⁻³ | 12685–12689 |
| the dark dimension (graviton DM, T_i ~ GeV) and the intermediate-scale/post-inflationary-axion picture are **mutually exclusive** | 12688 |
| SMASH-type inflation fits ACT only with positive PQ-quartic running from an extra scalar (the Higgs portal alone is non-perturbative) | 12688 |
| completion A: thermal leptogenesis needs ξ ≳ 10; flavour-from-PQ fails NA62 unless only b (or b+τ) carries PQ charge (N_DW = 1, g_aγγ = 0.4–1.7 g_KSVZ) | 12690, 12693, 12696 |
| completion B: compressed T–B–T′ triplet split by y′v/√2 ≈ 89 GeV; limits ≈ 1.74 TeV (prompt) to ≈ 1.9 TeV (long-lived); HL-LHC excludes to ≈ 2.1 TeV but cannot discover; FCC-hh measures y′ to ±0.002 | 12690–12698 |
| Bayesian evidence with explanatory credit: no robust preference over the SM once prior width and trials are accounted for | 12698 |

## Anomalies traced to method or input choices

Each was checked with a self-contained computation:

| anomaly | finding | pass |
|---|---|---|
| α (Cs vs Rb) | electron g−2 sides with Rb | 12691 |
| KM3NeT 220 PeV | counting tension 1.5σ; the rest is spectral; joint flux gives 2.2σ | 12691–12693 |
| neutron lifetime | g_A backs the bottle value; beam −4.6σ | 12691 |
| deuterium | the D/H tension depends on PRIMAT vs PArthENoPE | 12694 |
| W mass | agrees with the SM without CDF; CDF is 5.8σ from the rest | 12694 |
| Cabibbo angle | neutron V_ud satisfies unitarity; the lattice Δ_R^V halves the superallowed gap | 12695, 12698 |
| low N_eff (ACT + helium ≈ 2.85) | −2σ hint; no viable mechanism (post-BBN entropy, low reheating, lepton asymmetry and keV-decaying particles all fail or are partial) | 12692–12698 |

## Open

- A 2HDM-consistent b-only PQ model (anomaly bookkeeping only so far).
- B's decay regime, which electroweak precision does not fix.
- Simons Observatory will decide the N_eff hint at ~4σ.

## Addendum: Passes 12699–12701

| result | where |
|---|---|
| Neither completion explains the Belle II B→Kνν̄ or 95 GeV hints | 12699 |
| A's DFSZ-type potential: boundedness is set by the 2HDM quartics alone (240/240 scan) | 12699, 12700 |
| E₆-SUSY at the quartic zero: tan β ≈ 1.1–1.5; ceiling 5.4×10¹⁰ GeV (2×10¹⁰–1.7×10¹¹ over ±1σ in m_t); stop mixing only lowers it | 12699, 12700 |
| Split SUSY (fermions at 1 TeV): ceiling 5×10⁷ GeV | 12701 |
| High-scale SUSY at 10¹⁰ GeV does not unify (two-loop δ = −3.4) | 12700, 12701 |
| Incomplete E₆ pieces at 1 TeV (best: vectorlike Q + U) restore MSSM-level unification; the other track's 16/10 states are complete SU(5) multiplets and cannot | 12701 |
| With Q + U at 1 TeV, the quartic zero survives at 10¹⁰ GeV only for y′ ≈ 0.48, close to B's top partner (y′ = 0.51): a conditional E₆-SUSY + top-partner combination with τ_p ~ 4×10³⁵ yr | 12701 |
| Naturalness: A with hierarchical thermal leptogenesis Δ ≳ 7×10⁵; A with quasi-degenerate N at 1.2×10⁷ GeV (ΔM/M ~ 10⁻⁴) Δ ≈ 10; B Δ ≈ 4 | 12700, 12701 |
| Correction: two-loop shifts the MSSM unification mismatch by +0.8, not −0.8 | 12701 |

Questions for the other track remain in `REQUEST_E6_INTERMEDIATE_SCALE_SUSY.md`. New question: can the E₆ messenger filter leave a vectorlike Q + U (an incomplete 10 + 10̄) at the TeV scale?

## Addendum: Passes 12702–12705 (Claude track)

**For the other track.** Your question-4 answer is in Pass 12705. In real E₆ (e₆ computed as the derivation algebra of the cubic norm), a 650 alone has no F-flat vacuum where only Q + U are light. A 650 plus a 78 with a VEV outside the ψ direction has many such vacua, with unbroken SM×U(1)ⁿ, at two tuned couplings. Your ψ-only adjoint branch (7af60ca6b, a790aef) gives complete SO(10) multiplets only.

| pass | result | label |
|---|---|---|
| 12702 | Hybrid (E₆ SUSY at 10¹⁰ GeV + TeV vectorlike Q + U) unifies at two loops: δ = +0.26, y′ = 0.464, τ_p ~ 10³⁷ yr | numerical |
| 12703 | A light Q + U alone needs the SU(5) 75 inside the 210 ⊂ 650; two-loop vectorlike λ terms (PyR@TE 3) move y′ by +0.002 | exact / numerical |
| 12704 | SO(10) 45 + 210 vacua give exactly Q + U light; A's splitting window is 10⁻¹²–10⁻⁵; FCC separates B from the hybrid at 4–10σ for M_SS ≥ 3×10⁹–3×10¹⁰ GeV | numerical |
| 12705 | E₆: 650 + 78 needed. SO(10) leftovers: massless (8,1,0) + (1,3,0), which must be lifted to ≳ 10¹⁶ GeV. MFV tree splitting makes A's leptogenesis work (7–9%). Dark-graviton DM gives B y′ = 0.522–0.530 | numerical |

Corrections in this block:
- the B-vs-hybrid separation is about 3σ, not more than 5σ, unless M_SS ≳ 10¹⁰ (12703 corrects 12702);
- radiative-only leptogenesis falls short by ×3.4 (12703 corrects 12702);
- the degeneracy needed is ≲ 10⁻⁵, not 10⁻⁴–10⁻³ (12704 corrects 12701);
- the dark-graviton bound is eq. (4.14), with ℓ₅^eff ≥ 10 μm at natural parameters (12705 corrects 12704).
