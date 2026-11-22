# Pass 12694: third-generation PQ charges rescue A's flavour; B's triplet has a soft-lepton tag; the deuterium tension is a nuclear-rate choice; the PKS 0605-085 coincidence is 27% chance; robust helium keeps N_eff ≈ 2.85; the W mass agrees with the SM without CDF

Claude track. Follows Pass 12693. **Not a theory of everything.** Script: `toe_pass12694_round.py`; certificate: `data/toe_pass12694_round.json`.

## (1) Completion A: PQ charges on the third generation only

With family-universal-free PQ charges confined to the third generation, the flavour-violating axion couplings carry CKM factors:

| coupling | value | BR at f_a = 10¹¹ GeV | current limit |
|---|---|---|---|
| C_sd ~ V_td* V_ts | 3.6×10⁻⁴ | BR(K⁺ → π⁺a) = 4.5×10⁻¹⁶ | ~(3–6)×10⁻¹¹ (NA62) |
| C_bs ~ V_tb* V_ts | 0.041 | BR(B → K a) = 1.3×10⁻¹³ | ~10⁻⁵ (B → K + invisible, Belle II) |

> **Result.** Pass 12693 showed that standard Froggatt–Nielsen charges fail NA62. Third-generation-only PQ charges are safe by 5–8 orders of magnitude, so completion A can tie the PQ field to the heavy generation (a "top-philic" or third-family axion) without kaon or B constraints. Light-family flavour then needs its own mechanism.

## (2) Completion B: a soft-lepton tag for the triplet

- TT, BB and T′T′ pairs are produced at nearly equal rates. B → T W* gives two soft W* per BB pair; T′ → B W* → T W* W* gives four per T′T′ pair.
- With P(W* → e/μ ν) ≈ 0.22, **34% of triplet pairs carry ≥ 1 soft lepton** (p_T ~ 5–25 GeV). That is ≈ 4,400 tagged pairs at the HL-LHC near threshold.
- A soft-lepton requirement on top of a standard Wb/Zt/ht pair selection is a natural discriminator from single-state vectorlike quarks.

## (3) The deuterium "tension" is a nuclear-rate choice

| BBN code (rates) | D/H (Planck η) | vs Cooke+2018 2.527(30) |
|---|---|---|
| PRIMAT (Pitrou et al.) | 2.439(37)×10⁻⁵ | +1.85σ |
| PArthENoPE (Pisanti et al.) | 2.51(11)×10⁻⁵ | +0.15σ |

The +1.8σ quoted in Pass 12693 is the PRIMAT figure; PArthENoPE removes it. The difference is the d(d,n)³He and d(d,p)³H rates, theory-based vs data-driven. This does not change Pass 12693's exclusion of post-BBN entropy injection (+5.8σ with PRIMAT; ≈ +2.5σ with PArthENoPE's larger error, so it is still disfavoured).

## (4) KM3-230213A and PKS 0605-085

Assumptions: 4FGL-DR4 has ~7,195 sources (0.17 deg⁻²), and a flaring duty fraction of 0.1.

| radius | expected flaring blazars | P(≥ 1 by chance) |
|---|---|---|
| 2.4° (PKS 0605-085 offset) | 0.32 | **0.27** |
| 1.5° (claimed systematic) | 0.12 | 0.12 |
| 0.5° | 0.014 | 0.01 |

The proposed association ([Dzhatdoev 2025](https://arxiv.org/html/2502.11434v1)) is **not significant**: a flaring Fermi blazar within 2.4° occurs by chance ~27% of the time. Only a sub-degree direction with a confirmed systematic would make it informative.

## (5) Helium with an outlier mixture model

Each Y_p is either "good" N(μ, σ_i) or an outlier with σ inflated by τ = 0.010:

| P_out | Y_p | N_eff (bottle τ_n) | P(outlier) EMPRESS / others |
|---|---|---|---|
| 0.1 | 0.2441 ± 0.0018 | 2.84 ± 0.14 | 0.26 / 0.04–0.07 |
| 0.2 | 0.2442 ± 0.0021 | 2.85 ± 0.16 | 0.42 / 0.09–0.14 |

A robust treatment does **not** remove the helium half of the low-N_eff hint. EMPRESS is flagged as an outlier but not decisively (26–42%), and helium alone sits ≈ 1.2–1.4σ low. Combined with ACT (2.86 ± 0.13) the hint stays at about −2σ, still without a viable mechanism (Pass 12693).

## (6) Extra: the W mass without CDF

| combination | m_W (MeV) | χ²/dof | vs SM (80356 ± 6) |
|---|---|---|---|
| all six | 80390.6 ± 5.8 | 34.5/5 (p = 2×10⁻⁶) | +4.1σ (inconsistent set) |
| without CDF 2022 | 80363.6 ± 7.5 | 0.6/4 | **+0.8σ** |

Inputs: CMS 2024, ATLAS 2024, LHCb 2022, D0, LEP and CDF 2022, entered from the experiments' publications; the SM value is a representative electroweak-fit number.

**CDF is a 5.8σ outlier from the rest.** Without it, the W mass agrees with the Standard Model, and there is no W-mass anomaly for any TOE candidate to explain.

## Net

- **Completion A** acquires a flavour-safe variant (third-generation PQ charges).
- **Completion B** acquires a soft-lepton collider tag.
- Of the "anomalies" examined, deuterium, KM3NeT's blazar and the W mass are resolved by data or method choices. The low-N_eff hint survives a robust helium treatment at about −2σ, with no mechanism.
