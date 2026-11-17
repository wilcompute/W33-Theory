# Pass 12688: ACT-compatible PQ inflation needs positive quartic running (not from the Higgs portal); the dark dimension and the intermediate-scale picture are cosmologically exclusive; updated ranking

Claude track. Follows Passes 12684–12687. **Not a theory of everything.** Script: `toe_pass12688_intermediate_scale_round4.py`; certificate: `data/toe_pass12688_intermediate_scale_round4.json`.

## (1) Running-quartic PQ inflation reaches ACT's n_s

The potential is U = λ(φ)φ⁴/4/(1 + ξφ²)² with λ(φ) = λ₀[1 + b ln φ], at N_* = 55.6 (instant reheating, Pass 12687).

| ξ | b | n_s | r |
|---|---|---|---|
| 1 | 0 / 0.02 / 0.04 / 0.06 | 0.9653 / 0.9703 / 0.9741 / 0.9770 | 0.004 / 0.006 / 0.007 / 0.009 |
| 10 | 0 / 0.02 / 0.04 | 0.9653 / 0.9711 / 0.9756 | 0.0035 / 0.005 / 0.007 |
| 0.1 | up to 0.10 | ≤ 0.9722 | ≤ 0.016 |

The running needed:
- **P-ACT-LB** (n_s = 0.9743): b = 0.041 (ξ = 1) or 0.034 (ξ = 10), with r = 0.006–0.007.
- **P-ACT without DESI** (0.9709): b = 0.019–0.023.

r stays below the BK18 bound. b is β_λσ/λ_σ per e-fold of the field: λ_σ ≈ 4×10⁻¹⁰ (ξ = 1) needs only β ≈ 10⁻¹¹.

**The Higgs portal cannot supply it.** With β ⊃ 2λ_Hσ²/(16π²), one would need λ_Hσ ≈ 1.2–2.4 √λ_σ. Then the tree-level threshold δ = λ_Hσ²/λ_σ ≈ 1.5–5.8, so the Higgs quartic above m_ρ would be O(1–5) and hit a Landau pole within about one e-fold. Higgs stability needs only λ_Hσ ≥ 0.10√λ_σ (Pass 12685); with that, the portal-induced b is ~10⁻⁴.

**Any other weakly coupled scalar can.** A coupling κ ~ (2–4)×10⁻⁵ to σ gives the required β. So SMASH plus one additional singlet coupled to the PQ field, or a weakly gauged U(1)_PQ, is ACT-compatible, at the cost of one parameter.

## (2) The dark dimension and the intermediate-scale picture exclude each other cosmologically

Dark-dimension graviton dark matter needs a brane initial temperature T_i ~ 1 GeV, and overproduces as Ω ∝ T_i³ ([Gonzalo–Montero–Obied–Vafa, 2209.09249](https://arxiv.org/abs/2209.09249)):

| brane temperature needed for | Ω_KK/Ω_DM |
|---|---|
| post-inflationary PQ restoration, T ≳ f_a ≈ 10¹¹ GeV | ~10³³ |
| thermal leptogenesis, T ≳ 10⁹ GeV | ~10²⁷ |
| vectorlike quarks in the plasma, 1.65 TeV | ~5×10⁹ |
| graviton dark matter | 1 |

So in the dark dimension:
- the axion cannot be post-inflationary, so the lattice m_a window does not apply;
- leptogenesis cannot be thermal;
- the vectorlike quarks never thermalise, so the g_s dilution of Pass 12687 is irrelevant;
- the KK gravitons are non-thermal, so **ΔN_eff is negligible**. This removes the +3.1σ of Pass 12687; that benchmark assumed thermalised bulk states.

The two completions of the Higgs-quartic coincidence are therefore **alternatives, not partners**:
- **A — intermediate scale (SMASH-like):** λ = 0 at f_a ~ √(v M_Pl), post-inflationary axion dark matter, thermal leptogenesis, high reheating.
- **B — dark dimension:** λ = 0 at M₅ via a TeV vectorlike top partner, KK-graviton dark matter, GeV reheating.

## (3) FCC-era separation of the √(v M_Pl) variants (running offset closed in Pass 12687)

| scenario | σ(log₁₀ μ₀) | √(v M_Pl) vs √(v M̄_Pl) |
|---|---|---|
| FCC-ee with current NNLO matching | 0.27 | 1.3σ |
| matching errors halved | 0.21 | 1.7σ |
| N3LO matching (errors / 4) with α_s ± 0.0002 and M_h ± 0.01 | 0.145 | 2.4σ |

Separating the variants at 3σ needs matching better than N3LO. The Planck boundary is excluded much more easily (Pass 12685: 9σ).

## (4) Vectorlike-quark decay patterns (literature)

- A singlet-like T has BR(Wb : Zt : ht) ≈ 2 : 1 : 1.
- A (T,B) doublet mixing through t_R gives T → Zt, ht at 50 : 50 and B → Wt.
- In this rescue the near-degenerate T, T′, B triplet (≥ 1.65 TeV) decays through small SM mixing that y′ does not fix. Pair-production limits are 1.49–1.6 TeV (2412.01761).

## (5) ACT without DESI

SMASH's n_s = 0.9653 is −2.65σ against P-ACT-LB but **−1.47σ against P-ACT** (0.9709 ± 0.0038, no DESI). The n_s pressure on SMASH is largely the DESI-driven shift.

## (6) Updated ranking

| model | χ² | k | ΔAIC |
|---|---|---|---|
| SM + ΛCDM | 2.00 | 0 | 0 |
| λ(√(v M_Pl)) = 0 | 2.00 | 0 | 0.00 |
| λ(f_a) = 0, lattice axion | 2.04 | 0 | +0.04 |
| **dark dimension + VL quark, T_i ~ 1 GeV** | 2.00 | 1 | **+2.0** |
| **SMASH + running quartic (extra scalar)** | 2.04 | 1 | **+2.0** |
| SMASH, P-ACT n_s (no DESI) | 4.21 | 0 | +2.2 |
| λ(M_Pl) = 0 (AS / multiple-point criticality) | 7.74 | 0 | +5.7 |
| SMASH, P-ACT-LB n_s | 9.01 | 0 | +7.0 |
| dark dimension, thermal bulk (Pass 12687) | 6.86 / 17.17 | 1 / 0 | +6.9 / +15.2 |

> **After four rounds (numerical, not a TOE).** The Higgs-quartic coincidence has two viable, mutually exclusive completions, both at ΔAIC ≈ +2 with one parameter each.
> - **(A) SMASH-like intermediate scale.** Needs positive running of the PQ quartic from one extra weakly coupled scalar; the Higgs portal alone is too weak or non-perturbative. Tests: haloscopes at 45–65 μeV, CMB-S4 r ≈ 0.006–0.007, n_s.
> - **(B) Dark dimension with a TeV vectorlike top partner and GeV reheating.** Tests: VLQ triplet at ≥ 1.65 TeV with y′ ≈ 0.5, sub-mm gravity at 1–30 μm, keV sterile neutrinos.
>
> The two make opposite cosmological predictions: high vs GeV reheating, post-inflation axion vs KK-graviton dark matter. A haloscope detection at 45–65 μeV would favour A; a fifth-force signal at micron range would favour B.
