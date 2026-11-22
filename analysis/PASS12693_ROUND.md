# Pass 12693: no simple mechanism explains the low-N_eff hint; the triplet limit rises to M_VL > 1.74 TeV; flavour-from-PQ fails NA62 for every simple FN assignment; the KM3NeT-only flux cannot be cosmogenic; EMPRESS is a 2.25σ outlier

Claude track. Follows Pass 12692. **Not a theory of everything.** Script: `toe_pass12693_round.py`; certificate: `data/toe_pass12693_round.json`.

## (1) The low-N_eff hint has no simple mechanism

The hint: helium plus ACT give N_eff ≈ 2.85 ± 0.10 (part 5).

| mechanism | effect | verdict |
|---|---|---|
| photon-entropy injection after neutrino decoupling and after BBN | N_eff = 3.044 F^(−4/3), so F = 1.048 for N_eff = 2.86. Then η_BBN = Fη_CMB, so D/H = 2.26×10⁻⁵ | **excluded**: +5.8σ against Cooke+2018 2.527(30)×10⁻⁵. The standard prediction (PRIMAT 2.439) is itself already +1.8σ |
| low reheating temperature (MeV scale) | lowers N_eff but **raises** Y_p; T_RH > 5.96 MeV and N_eff > 2.98 ([2501.01369](https://arxiv.org/html/2501.01369v2)) | **excluded** as a joint explanation |
| electron-neutrino asymmetry ξ_e | ξ_e ≈ 0.014 brings Y_p down to the helium mean (dY_p/dξ_e ≈ −0.2, approximate), with ΔN_eff ≈ 10⁻⁴ | explains helium only; the CMB N_eff = 2.86 stays −1.4σ |

> Reading: the two halves of the hint (CMB damping tail, helium) prefer N_eff ≈ 2.85 for different reasons, and no single standard mechanism lowers both. The most economical reading is two independent ~1.4–1.8σ fluctuations, or a helium systematic (part 5). It is **not** evidence for new physics at present.

## (2) Completion B: the triplet raises the effective limit

The B and T′ pairs cascade (soft W*) to the lightest T, so standard pair searches see ≈ 3× the single-T rate. With the computed σ(M) slope (factor 1.72 per 100 GeV at 13.6 TeV, Pass 12692):
- the 1.49 TeV single-T limit moves up by ≈ 200 GeV, so the **lightest T must exceed ≈ 1.69 TeV**, i.e. **M_VL ≳ 1.74 TeV**;
- the lightest T is long-lived (cτ > 1 mm) only for SM mixing below 1.1×10⁻⁸; between 10⁻⁸ and 10⁻⁴ it decays promptly, while the heavier members cascade softly.

B's y′ = 0.51 ± 0.02 is unaffected; it was computed at 1.65 TeV and moves by < 0.005 per 100 GeV (Pass 12689).

## (3) Completion A: flavour-from-PQ fails NA62 for every simple Froggatt–Nielsen assignment

With ε = 0.22: C_sd ~ ½|ΔX_Q ε^ΔX_Q + ΔX_d ε^ΔX_d|, V_us ~ ε^ΔX_Q, m_d/m_s ~ ε^(ΔX_Q + ΔX_d). This assumes N_DW = 1 normalisation and O(1) coefficients.

| (ΔX_Q, ΔX_d) | C_sd | V_us | m_d/m_s | flavour (within ×3) | NA62 (C < 0.09) |
|---|---|---|---|---|---|
| (1, 1) | 0.22 | 0.22 | 0.048 | ✓ | ✗ |
| (0, 2) | 0.048 | 1 | 0.048 | ✗ (V_us) | ✓ |
| (2, 0) | 0.048 | 0.048 | 0.048 | ✗ (V_us) | ✓ |
| (1, 0) / (0, 1) | 0.11 | 0.22 / 1 | 0.22 | ✗ | ✗ |

The only assignment reproducing V_us and m_d/m_s is (1, 1), and it has C_sd ≈ 0.22, which NA62 excludes at f_a ≈ 10¹¹ GeV (Pass 12692). Assignments that pass NA62 lose the Cabibbo angle.

> **Result (order of magnitude).** In completion A the PQ field cannot also be the Froggatt–Nielsen flavon (axiflavon or flaxion) with standard charges. Flavour must come from a separate sector, consistent with Pass 12690 (4). Alternatively N_DW > 1 or non-FN textures, both of which the lattice window constrains further.

## (4) KM3-230213A as a cosmogenic event

E²Φ(200 PeV, per flavour) ~ f_p × [10⁻⁹ (no source evolution) … 10⁻⁸ (strong evolution)]; these are literature ranges.

| flux | proton fraction needed |
|---|---|
| joint fit 7.5×10⁻¹⁰ | **0.075** (strong) – 0.75 (none) |
| KM3NeT-only 5.8×10⁻⁸ | 5.8 – 58, impossible |

The KM3NeT-only flux estimate cannot be cosmogenic. At the joint-fit flux the event is consistent with a ~10% proton component plus strong source evolution, which Auger's composition still allows. This agrees with [2502.08508](https://arxiv.org/pdf/2502.08508).

## (5) EMPRESS and the helium combination

- The four Y_p values give χ² = 5.39/3 (p = 0.15) and a Birge ratio of 1.34.
- **EMPRESS sits −2.25σ from the mean of the other three.**
- With Birge-inflated errors, helium gives N_eff = 2.83 ± 0.16 (at the bottle τ_n).
- Combined with ACT this is **2.85 ± 0.10, −2.0σ** from 3.044 (down from 2.3σ before inflation).

The helium half of the hint is driven by one 2.25σ-discrepant survey. Without EMPRESS, helium sits at 2.96 ± 0.13 (Pass 12692).

## Net effect on the picture

- **Completion A** loses the option of flavour from its PQ field; it still needs ξ ≳ 10 for thermal leptogenesis, an extra scalar for ACT's n_s, and |C_sd| < 0.09.
- **Completion B's** collider target moves to M_VL ≳ 1.74 TeV, with y′ = 0.51 ± 0.02 unchanged.
- The low-N_eff hint has no mechanism that survives the light elements, so it remains a −2σ curiosity.
- KM3NeT stays a ~2σ fluctuation unless the proton fraction is ~10% with strong evolution.
