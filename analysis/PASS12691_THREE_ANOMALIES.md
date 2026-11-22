# Pass 12691: three anomalies from a literature sweep, each reduced to one computation — α from electron g−2 sides with Rb against Cs (4σ); the KM3NeT 220 PeV tension is mostly spectral, not counting; g_A backs the bottle neutron lifetime

Claude track. Each anomaly was chosen from current literature and checked with a self-contained computation. **Not a theory of everything.** Script: `toe_pass12691_three_anomalies.py`; certificate: `data/toe_pass12691_three_anomalies.json`.

## (A) Electron g−2 and the fine-structure-constant split

Inputs:
- QED through tenth order, a_had = 1.693(12)×10⁻¹², a_weak = 0.0303×10⁻¹².
- Measurement: Fan et al. 2023, a_e = 0.00115965218059(13) ([PRL 130, 071801](https://ar5iv.labs.arxiv.org/html/2209.13084)).
- The tenth-order coefficient is disputed: 6.737(159) (Aoyama–Kinoshita–Nio) vs 5.891(61) (Volkov).

| α input | C₅ | Δa_e = exp − SM (×10⁻¹⁴) | pull |
|---|---|---|---|
| Cs 2018: 137.035999046(27) | AKN | −107 ± 26 | **−4.1σ** |
| Rb 2020: 137.035999206(11) | AKN | +28 ± 16 | +1.75σ |
| Cs 2018 | Volkov | −101 ± 26 | −3.9σ |
| Rb 2020 | Volkov | +34 ± 16 | +2.1σ |

- α⁻¹ inferred from a_e: **137.035999166(15)** (Volkov), which reproduces the value quoted by Fan et al. exactly, or 137.035999173(16) (AKN).
- The Cs and Rb α determinations disagree by 5.5σ.

> **Reading.** The electron g−2 sides with **Rb** (1.8–2.1σ) against **Cs** (3.9–4.1σ). The C₅ dispute moves this by only ≈0.3σ. So the "electron g−2 anomaly" is currently an atomic-interferometry discrepancy, not a QED or new-physics signal. A dark-photon or axion explanation would have to explain a 4σ offset of one α measurement, not of a_e.

## (B) KM3-230213A (220 PeV) vs IceCube

For a steady isotropic flux and exposure ratio r = IceCube/KM3NeT, the probability that the single event lands in KM3NeT is p = 1/(1 + r):

| r | p | one-sided |
|---|---|---|
| 15 (Palmisano et al., IceCube's exposure at the time) | 0.0625 | **1.5σ** |
| 30 | 0.032 | 1.85σ |
| 70 | 0.014 | 2.2σ |

The quoted 2.5σ and 3.1σ tensions correspond to effective exposure ratios r ≈ 160 and ≈ 1000.

> **Reading.** Counting alone, with IceCube's 15× exposure, gives only ~1.5σ. The literature's 2.5–3.1σ comes from IceCube's non-detections across a wider energy range, which depend on the assumed spectral shape, plus Auger. So the tension is a statement about the **flux shape**: a sharply peaked or transient source relieves it (transient: 1.6σ, Palmisano et al.). Sterile-oscillation explanations (Brdar–Chattopadhyay) are not required by the counting.

## (C) Neutron lifetime: beam vs bottle

The beam average 888.1 ± 2.0 s and the bottle average 877.8 ± 0.3 s disagree by **5.1σ**. The SM relation τ_n(1 + 3g_A²) = 5172.0 ± 1.1 s gives:

| g_A source | τ_SM | vs bottle | vs beam |
|---|---|---|---|
| PERKEO III 1.27641(56) | 878.4 ± 0.7 s | +0.9σ | **−4.6σ** |
| PDG average 1.2754(13) | 879.6 ± 1.5 s | +1.2σ | −3.4σ |

The J-PARC electron-counting beam result (877.2 +4.3/−4.0 s, 2025 talk) is −2.4σ from the proton-counting beam average and consistent with the bottle.

> **Reading.** The SM, through the independently measured axial coupling, backs the **bottle** lifetime. The 1.16% dark-decay branching that the beam value would need is therefore not supported. The anomaly points to a systematic of the proton-counting beam method, as the 2025 PSI workshop also concluded.

## Common thread

All three "anomalies" reduce to a disagreement between measurement methods rather than a failure of the Standard Model:
- Cs vs Rb atom interferometry;
- KM3NeT counting vs IceCube's spectral non-detection;
- proton-counting beam vs bottle (and electron-counting beam).

In each case the SM-internal cross-check (g−2 for α; g_A for τ_n) sides with one method. None of the three is a TOE lever as it stands.
