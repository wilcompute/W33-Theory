# Pass 12709: B′ survives through Dark_CP mesogenesis (A_CP·BR ≳ 0.5–1.4×10⁻⁷, inside Belle II reach); the W33 tetrahedral complex is uniformly negatively curved (−2 per point) but is not a Regge manifold; FCC-ee decides vacuum stability at 18σ; the updated evidence still prefers nothing over the SM

Claude track. Follows Pass 12708. **Not a theory of everything.**
- Script: `toe_pass12709_round.py` (≈1 min).
- Certificate: `data/toe_pass12709_round.json`.
- Tests: `tests/test_toe_pass12709.py`, 4 tests passing.

**Correction to Pass 12708.** That pass gave the B-mesogenesis requirement as BR ≳ 10⁻⁴, taken from a summary of 2101.02706. The corrected requirements are:
- **[2211.10553](https://arxiv.org/abs/2211.10553):** ≳ 10⁻⁵ (neutral), ≳ 10⁻⁶ (charged) and ≳ 10⁻⁷ (most general).
- **Dark_CP [2509.18246](https://arxiv.org/abs/2509.18246):** down to about 10⁻⁸.

## (1) B′ against B-mesogenesis
- **Dark_CP mechanism:** the relation is Y_B/Y_B^obs = (BR/1.3×10⁻⁸)|A_CP|(T_R/60 MeV)(2m_M/m_Φ), valid for T_R = 5–60 MeV.
- **Overlap:** B′'s dark-dimension reheating window (Pass 12707) lies **entirely inside** that range for every surviving R.

| R (μm) | T_RH window (MeV) | A_CP·BR needed (m_Φ = 11 GeV) | (m_Φ = 100 GeV) |
|---|---|---|---|
| 0.009 | 6.0–16.9 | 4.8×10⁻⁸ – 1.4×10⁻⁷ | 4.4×10⁻⁷ – 1.2×10⁻⁶ |
| 0.026 | 6.0–11.7 | 6.9×10⁻⁸ – 1.4×10⁻⁷ | 6.3×10⁻⁷ – 1.2×10⁻⁶ |
| 0.088 | 6.0–7.8 | 1.0 – 1.4×10⁻⁷ | 0.9 – 1.2×10⁻⁶ |
| 0.200 | 6.0 | 1.4×10⁻⁷ | 1.2×10⁻⁶ |

- **Existing limits:** Belle and BaBar limit B_d → Λψ to 10⁻⁵–10⁻⁴, which disfavours some channels of the original neutral mechanism but not B′.
- **Prediction:** at O(1) dark CP violation, B′ needs BR ≳ 5×10⁻⁸–10⁻⁶ (larger at small R and heavy Φ).
- **Test:** Belle II's projected reach (~10⁻⁷) cuts into this. **B′ is falsifiable at Belle II**, together with an FCC y′ of 0.488–0.505.

## (2) Curvature of the W33 tetrahedral complex
This is the continuation of the triangle idea from the Pass 12708 note.
- **Gluing:** every triangle and every edge lies in **exactly one** of the 40 tetrahedra. The tetrahedra share only vertices, so the complex is **not a pseudomanifold**. Regge calculus, whose curvature sits on shared hinges, does not apply to it as it stands.
- **Links:** the link of each point is **4 disjoint triangles**.
- **Curvature:** Banchoff combinatorial curvature κ(v) = 1 − f₀/2 + f₁/3 − f₂/4 = **−2 at every point**. It sums to χ = −80, a discrete Gauss–Bonnet.
- **Interpretation:** W33 is a uniformly negatively curved, tree-like gluing of tetrahedra with 81 independent loops (the loop count is owned by BT545–551).
- **Equilateral metric:** edge deficit 2π − arccos(1/3) = 5.05 rad; vertex solid-angle deficit 10.36 sr.
- **Consequence:** a Regge or CDT-type model on W33 needs a different gluing, for example identifying faces along the 160 triangles or using the 4-simplex structure of a larger building.

## (3) Warped dark dimensions
- **Lee–Randall–Riojas ([2609.36234](https://arxiv.org/pdf/2609.36234)):** a universal q⁵ near-threshold rate, covering both RS-like and flat geometries, which they use to rule out existing dark-dimension dark-matter models.
- **Langhoff:** the d-wave suppression holds for any static warping. Its kinematics was reproduced in Pass 12708.
- **Warping does not revive graviton dark matter.**
- **Open:** the R ≲ 0.2 μm bound itself assumes a flat spectrum, m_n = n·m_KK, so strongly warped spectra need their own freeze-in calculation.

## (4) Vacuum stability: today vs FCC-ee
The critical pole mass for absolute stability (minimum λ ≥ 0 up to M_Pl) is 170.63, 170.98, 171.10 and 171.33 GeV at α_s = 0.1171, 0.1180, 0.1183 and 0.1189. This agrees with Buttazzo et al. (171.0–171.4).

| input | σ_eff (incl. α_s) | distance from stability | P(absolutely stable) |
|---|---|---|---|
| PDG, experimental only | 0.46 | 3.5σ | 2.5×10⁻⁴ |
| PDG + 0.5 GeV scheme | 0.68 | 2.3σ | 0.9% |
| ATLAS+CMS + scheme | 0.69 | 2.2σ | 1.3% |
| FCC-ee (PDG central) | 0.09 | **18σ** | 10⁻⁷³ |

- **Today:** stability is disfavoured at 2.2–3.5σ, but the scheme error keeps it at about 1% (the MS-bar route of Pass 12708 is consistent with this).
- **FCC-ee:** with the current central value, it would establish that the quartic crosses zero at 18σ. That is a precondition for A, B′ and the hybrid alike.

## (5) Updated Bayesian evidence (Pass 12698 rerun)
The rerun reproduces Pass 12698 at σ(m_t) = 0.43: boundary 13.5, A 2.6. What changed:
- σ(m_t) now includes the 0.5 GeV scheme error.
- B is replaced by B′: dark matter comes from mesogenesis, so there is no T_i³ tuning.
- B′ carries two prior penalties:
  - the surviving λ ∈ [10⁻⁴, 2.3×10⁻³], a fraction 0.34 of a log prior on [10⁻⁴, 1];
  - the overlap of its reheating window with Dark_CP's 5–60 MeV (mean fraction 0.25).
- dy′/dm_t = 0.0357 from Pass 12707.

| SM m_t prior width | boundary (/8 trials) | A (/8 trials) | B′ |
|---|---|---|---|
| 15 GeV | 8.97 (1.12) | 1.82 (0.23) | 0.044 |
| 5 GeV | 2.99 (0.37) | 0.61 (0.08) | 0.015 |
| 2 GeV | 1.20 (0.15) | 0.24 (0.03) | 0.006 |

- **The conclusion of Pass 12698 stands and strengthens:** with honest priors and trials, no model is preferred over the SM.
- **Per model:** the scheme error lowers the boundary and A by about 1/3. B′ is penalised for its narrow surviving parameter range, not for tuning.
- **Where evidence can come from:** the scenarios gain only through new measurements, namely FCC y′, a Belle II B → ψ + baryon signal, or short-range gravity at 10–200 nm.

## Status
- **A:** evidence 0.03–0.23 after trials. Unchanged physics.
- **B′:** falsifiable at Belle II (A_CP·BR ~ 10⁻⁷) and FCC (y′ = 0.488–0.505). It is disfavoured a priori only by its narrow range.
- **Hybrid:** y′ = 0.470. Not in the evidence table; to be added.
- **Common precondition:** the quartic must cross zero. That is about 99% likely today, and FCC-ee would settle it at 18σ.
