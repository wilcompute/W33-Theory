# Pass 12697: A's PQ doublet decouples; EW precision cannot fix B's decay regime; the keV particle has no clean candidate; the Cabibbo gap is 14× the new ab initio δ_NS error; BIC Bayes factors

Claude track. Follows Pass 12696. **Not a theory of everything.** Script: `toe_pass12697_round.py`; certificate: `data/toe_pass12697_round.json`.

## (1) Completion A's PQ-charged doublet decouples

A portal λ₁₂ σ² H₁H₂ gives the second doublet m_H₂ ~ √λ₁₂ f_a: 10⁵, 10⁷, 10⁹ GeV for λ₁₂ = 10⁻¹², 10⁻⁸, 10⁻⁴.
- Every 2HDM flavour and B-physics constraint (b → sγ, B_s mixing, tree-level FCNCs) is therefore decoupled.
- The axion's E/N and N_DW are set by the charges alone, so the b-only assignment of Pass 12696 survives (E/N = 2/3, N_DW = 1, g = 0.65 g_KSVZ).
- The cost is the generic DFSZ hierarchy tuning (125 GeV/m_H₂)² ~ 10⁻⁶–10⁻¹⁴. Every axion model with charged doublets pays this; it is not specific to A.

## (2) Completion B: electroweak precision allows any decay regime

- Singlet-like top mixing: ΔT ≈ T_SM θ²(2 ln r − 2) with r = M²/m_t², giving **θ_t ≲ 0.18** at 1.74 TeV.
- Doublet-like bottom mixing: Z → bb̄ (|δg_L^b| ≲ 2×10⁻³) gives **θ_b ≲ 0.06**.

The prompt-versus-cascade boundary (θ ≈ 1.1×10⁻⁴, Pass 12692) lies 3 orders of magnitude inside the allowed range. Electroweak data do not decide whether B's triplet decays directly or through soft cascades; only collider searches can.

## (3) Candidates for the keV-window particle (Pass 12695–12696)

The target is decays at T ≈ 5–30 keV (τ ≈ 10³–5×10⁴ s) with ζ ~ 10⁻⁶ GeV and almost no hadronic or neutrino branching.

| candidate | parameters for τ = 1.3×10⁴ s | problem |
|---|---|---|
| photophilic ALP, m = 1–4 MeV (photons below the D threshold) | g_aγγ = 3×10⁻⁹ – 4×10⁻¹⁰ GeV⁻¹ | sits in the region constrained by SN1987A and BBN (the "cosmological triangle") |
| modulus, Γ = m³/(4πM_Pl²) | m ≈ 1.6 TeV | generic gluon couplings, so hadronic BBN bounds at ζ ~ 10⁻⁶ GeV exclude it |
| gravitino | m ≈ 3.1 TeV | hadronic branching ~10⁻³, excluded |

> No clean candidate. The low-N_eff hint (Pass 12692–12694) remains without a viable mechanism, even for its CMB half.

## (4) The Cabibbo gap vs ab initio nuclear structure

- With the 2024 superallowed value V_ud = 0.97361(30) (Seng et al.), the neutron value 0.97456(44) is 1.8σ higher.
- Reconciling them needs Ft to drop by **0.195% (6.0 s)**.
- The new ab initio δ_NS(¹⁰C) = −0.422(14)% (Gennari et al., PRL 2025) has an uncertainty **14× smaller** than the needed shift.

A δ_NS error is therefore an unlikely closure for light emitters. The remaining suspects are the inner radiative correction Δ_R^V, the Zα² structure-dependent terms that Cao–Hill–Plestid–Vander Griend (2025) argue must be revisited, medium-mass δ_NS (not yet ab initio), or the neutron inputs (g_A, τ_n).

## (5) Combined ranking (BIC over n = 7 observables)

| model | χ² | free params | ΔBIC | Bayes factor vs SM |
|---|---|---|---|---|
| SM + ΛCDM | 2.00 | 0 | 0 | 1 |
| λ(√(v M_Pl)) = 0 boundary | 2.00 | 0 | 0 | 1.0 |
| **Completion B** (dark dimension + VL, GeV reheating) | 2.00 | 1 | +1.95 | **0.38** |
| **Completion A** (b-only PQ, extra scalar, ξ ≳ 10) | 2.04 | 2 | +3.93 | **0.14** |
| λ(M_Pl) = 0 (AS / MPP) | 7.74 | 0 | +5.74 | 0.06 |
| original SMASH | 9.01 | 0 | +7.01 | 0.03 |

Neither completion is favoured over the SM by these observables. The Bayes factors count only their parameters, not what they explain (dark matter, strong CP, baryogenesis, the dark-energy/neutrino coincidence). The ranking among the high-scale options is stable: the intermediate-scale boundary costs nothing, and the Planck boundary and original SMASH are disfavoured by factors 17–33.

## Parallel work

No new commits from the other track since Pass 12696 (c4be9ca26).
