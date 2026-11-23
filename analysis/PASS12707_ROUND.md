# Pass 12707: a new preprint removes B's dark-graviton window, so B moves to y′ = 0.488–0.505 with MeV reheating; the one-loop threshold at M_VL adds +0.006 to +0.009 to y′; the top-mass scheme ambiguity widens μ₀ to 1×10¹⁰–4×10¹¹ GeV; single-T searches do not beat B's 1.74 TeV floor; a shared input card

Claude track. Follows Pass 12705; Pass 12706 is reserved by another session for the E₆ mass matrix and is not touched here. **Not a theory of everything.**
- Script: `toe_pass12707_round.py` (≈1 min). It reuses the two-loop running of Passes 12703–12704.
- Inputs: `toe_inputs_card.json`, which is new.
- Certificate: `data/toe_pass12707_round.json`.
- Tests: `tests/test_toe_pass12707.py`, 5 tests passing.

## (1) Shared input card and drift
- **New file:** `analysis/toe_inputs_card.json` holds M_t, α_s, M_h, M_VL, M_SS, the FCC-era errors and the dark-dimension bounds. Each value carries its source, checked 2026-11-23.
- **Drift scan:** 13 scripts from Passes 12684–12706 were scanned. They hard-code M_VL as both 1650 and 1740 GeV. Pass 12704's B band used 1650; its forecast used 1740. The effect is about 0.0008 in y′, which is small, but later passes should load the card.

## (2) Fresh inputs and the top-mass scheme

| inputs | μ₀ (GeV) |
|---|---|
| PDG M_t = 172.57, α_s = 0.1180 (repo) | 5.4×10¹⁰ |
| ATLAS+CMS 172.52 | 6.5×10¹⁰ |
| CMS 172.44 / ATLAS 172.69 | 8.8×10¹⁰ / 3.6×10¹⁰ |
| PDG M_t, FLAG α_s = 0.1183 | 8.1×10¹⁰ |
| M_t ∓ 0.5 GeV (MC-vs-pole scheme) | 4.4×10¹¹ / 1.1×10¹⁰ |

**Uncertainty in μ₀ and y′.**
- **Experimental errors today:** σ(log₁₀ μ₀) = 0.68 and σ(y′_B) = 0.019.
- **With the scheme ambiguity added:** σ(log₁₀ μ₀) = 1.04 and σ(y′_B) = 0.028. The ambiguity is 0.5 GeV: the pole-mass renormalon is about 0.25 GeV (Hoang–Lepenik–Preisser) and MC calibration about 0.5–1 GeV.
- **FCC era:** σ(log₁₀ μ₀) = 0.13 and σ(y′_B) = 0.004.

**Effect on earlier passes.**
- Passes 12684–12706 carried only the experimental M_t error, and some quoted ranges carried none. Two examples are B's "0.522–0.530" and the "5.4×10¹⁰ ceiling".
- The E₆-SUSY ceiling on M_SS (Pass 12700) tracks μ₀. It is therefore uncertain by about one decade today.

**Other inputs checked.**
- **Toponium:** CMS and ATLAS have seen the near-threshold tt̄ excess, about 9 pb, which is interpreted as quasi-bound toponium. It concerns cross-section shapes. It does not shift the direct-reconstruction M_t that is used here.

## (3) One-loop threshold at M_VL (new, computed)

Integrating out the vectorlike Q + T with y′ H Q̄ T, at degenerate Dirac mass M, in MS-bar at μ = M:
- **Coleman–Weinberg part:** the exact series of Σ m⁴(ln m²/M² − 3/2) is −3M⁴ − 2M²a² + (5/6)a⁴, with a = y′h/√2. This gives λ_SM = λ_VL − (5/6) N_c y′⁴/16π².
- **Field renormalisation:** for a chiral vertex the bubble has trace 2k·(k+p). This gives Z_kin = 1 + N_c y′²/16π² [ln(μ²/M²) − 1/3], hence λ_SM = λ_VL(1 + 2N_c y′²/48π²) − (5/6) N_c y′⁴/16π².

| target | y′ (no threshold) | + CW h⁴ | + Z | shift |
|---|---|---|---|---|
| B at R = 0.088 μm | 0.4929 | 0.5034 | **0.5003** | +0.0074 |
| B at R = 10 μm (old window) | 0.5217 | 0.5334 | 0.5303 | +0.0086 |
| hybrid at 10¹⁰ GeV | 0.4637 | 0.4730 | **0.4699** | +0.0062 |

- The threshold is **3–4 times the two-loop vectorlike correction** of Pass 12703 (+0.002). Passes 12685–12706 did not include it.
- It moves B and the hybrid almost together, so the gap changes by only about 0.002.
- The Z term was computed by hand here. A cross-check with Matchmakereft is open.

## (4) B after the dark-graviton result

[Langhoff, arXiv:2610.01825](https://arxiv.org/abs/2610.01825) (v1, Oct 2026, a preprint) argues the following. Lee–Randall–Riojas obtained the same threshold suppression independently.
- Near-threshold KK-graviton decays are d-wave suppressed (Q^{5/2}), so the "dark cascade" never transfers the freeze-in population to light modes.
- **KK gravitons are therefore excluded as dark matter in a flat dark dimension.**
- The irreducible freeze-in population, constrained by COMPTEL and EGRET MeV photons, combined with T_RH ≥ 5.96 MeV from BBN and CMB+BAO, requires **R ≲ 0.2 μm (m_KK ≳ 1 eV)**.

**Consequences for B.**
- The window B used in Passes 12704–12705 (ℓ₅^eff = 10–30 μm, from the dark-graviton dark-matter constraints of 2307.11048) is gone.
- **Surviving range:** R = λΛ^{−1/4} with Λ^{−1/4} = 87.7 μm. Montero–Vafa–Valenzuela give λ ~ 10⁻¹–10⁻³; later work extends this to 10⁻⁴. So λ = 10⁻⁴–2.3×10⁻³, which is R = 0.009–0.2 μm. The UHECR-motivated value λ = 10⁻³ (R = 0.088 μm) is inside this range.

| λ | R (μm) | M₅ (GeV) | y′_B | gap to hybrid (0.470) | FCC separation (σ_meas = 0.005–0.002) |
|---|---|---|---|---|---|
| 1×10⁻⁴ | 0.009 | 2.8×10⁹ | 0.488 | 0.018 | 3–8σ |
| 3×10⁻⁴ | 0.026 | 1.9×10⁹ | 0.494 | 0.024 | 5–10σ |
| 1×10⁻³ | 0.088 | 1.3×10⁹ | 0.500 | 0.030 | 6–13σ |
| 2.3×10⁻³ | 0.200 | 9.8×10⁸ | 0.505 | 0.035 | 7–15σ |
| (excluded) | 10 | 2.7×10⁸ | 0.530 | 0.060 | — |

**B now predicts y′ = 0.488–0.505 (±0.019 experimental, ±0.028 with the scheme ambiguity, today).** This replaces 0.522–0.530.
- The gap to the hybrid shrinks from 0.058 to 0.018–0.035.
- The 11σ FCC separation of Pass 12705 becomes 3–15σ, depending on λ and on the FCC-hh precision.

## (5) Single-T production vs B
- **Assumed coupling map:** B's electroweak-precision mixing bound θ_t ≲ 0.18 (Pass 12697) corresponds to κ ≲ 0.25, assuming singlet-like κ ≈ √2 sin θ_L. This map has not been checked against Roy et al., PRD 101, 115027.
- **ATLAS single-T combination** ([2408.08789](https://arxiv.org/abs/2408.08789)): κ > 0.57 is excluded at all masses, κ = 0.5 is excluded below 2.1 TeV, and κ ≈ 0.25 only below about 1.5 TeV.
- **No new constraint on B.** The floor stays at M_VL ≳ 1.74 TeV (prompt) and ≳ 1.9 TeV (long-lived).
- **HL-LHC estimate:** with a 1/√L scaling, HL-LHC reaches κ ≈ 0.23 at 2.1 TeV, which is the mixing bound itself. If B's top mixing is near its electroweak-precision limit, single-T production at HL-LHC becomes a test of B.
- **No new pair-production limit:** ATLAS/CMS have no 2025–26 pair-production limit beyond about 1.5 TeV for standard decays.

## (6) Reheating window and B-mesogenesis
- **Reheating window:** with R ≤ 0.2 μm, T_RH is bounded below by 5.96 MeV. Above, Langhoff eq. (28) gives ρ ∝ T³/m_KK; at a fixed allowed fraction the ceiling is T_RH,max ≈ 6 MeV (R/0.2 μm)^{−1/3}. This is a scaling estimate: the mass dependence of the photon limits is ignored.
- **Resulting ranges:** T_RH,max ≈ 6–17 MeV over the surviving R range, so **B's universe reheats at 6–17 MeV**.
- **Implications for B:**
  - Baryogenesis must happen at MeV temperatures, with no sphalerons and no thermal leptogenesis.
  - Dark matter cannot be KK gravitons.
- **B-mesogenesis fits this window.** Elor–Escudero–Nelson and Alonso-Álvarez–Elor–Escudero supply both the baryon asymmetry and dark matter (a dark baryon) at T_R ≈ 5 MeV for B_d and 10 MeV for B_s, with up to ~140 MeV allowed in 2610.03455. It therefore fills both gaps.
- **Completion B′ = dark dimension (R ≈ 0.01–0.2 μm) + top partner (y′ ≈ 0.49–0.51) + B-mesogenesis.** It predicts:
  - BR(B → ψ + baryon) ≳ 10⁻⁴, testable at Belle II and LHCb;
  - deviations from Newton's law at R ≈ 0.01–0.2 μm (Casimir-range experiments);
  - an FCC y′.
- **Open:** whether the heavy scalar Φ of B-mesogenesis can be the dark-dimension radion/inflaton.

## Status
- **A:** unchanged (Pass 12705). The scheme ambiguity widens μ₀ but A's leptogenesis does not depend on μ₀ at better than a decade.
- **B:** moved to y′ = 0.488–0.505. KK-graviton dark matter is excluded if 2610.01825 holds. B′ (with B-mesogenesis) is the viable form.
- **Hybrid:** y′ = 0.470 with the threshold, ±0.019 / ±0.028 today. Its separation from B at FCC is now 3–15σ instead of 11σ.
- **Corrections to earlier passes:**
  - Pass 12705 item (4) is superseded.
  - The ranges in Passes 12700–12705 lacked the scheme error and the M_VL threshold.
