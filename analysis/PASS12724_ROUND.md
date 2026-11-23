# Pass 12724: corrections and rigour. The y′ floor with uncertainties is 0.40 (95%: 0.35–0.47), so the robust falsifier is y′ < 0.35; DM-coupled quintessence *raises* σ8 by 1–8% (correcting Pass 12723's S8 claim); orbifold KK thresholds allow only M_sR ≈ 10–15; ψ carries ≤ 80% of B′'s dark matter; the fixed-corpus ternary gap falls as width^−0.59

Claude track. **Not a theory of everything.**
- Scripts: `explore_pass12724_round.py` and `explore_pass12724_charlm{32,48}_fixed.py`.
- Certificates: `data/explore_pass12724_*.json`.
- Tests: `tests/test_toe_pass12724.py`, 5 tests passing.

## (4) Linear growth with DM-coupled quintessence (corrects Pass 12723)
**Equations:**
- δ_c″ + (2 + H′/H − βφ′)δ_c′ = 1.5[Ω_c(1 + 2β²)δ_c + Ω_b δ_b];
- the baryons obey the uncoupled equation;
- same early amplitude and Ω_m(today) = 0.31 as ΛCDM.

| model | σ8 / σ8(ΛCDM) | fσ8(z = 0.5) ratio |
|---|---|---|
| thawing, λ = 1, β = 0 | **0.977** | 0.951 |
| **coupled, λ = 1, β = 0.1 (DESI best fit)** | **1.013** | 0.999 |
| coupled, λ = 0.7, β = 0.1 | 1.021 | 1.019 |
| coupled, λ = 1.4, β = 0.2 | 1.082 | 1.066 |

- **Correction:** the stronger effective DM–DM gravity (1 + 2β²) and the reduced friction outweigh the lower DM density. **The DESI-fitting coupled B′ slightly raises σ8 (+1.3%), worsening the S8 tension.** Pass 12723's "S8 eased" came from a density proxy and had the wrong sign.
- **Thawing without coupling lowers σ8 by 2.3%,** but fits DESI worse (Pass 12722).
- **The trade-off is now explicit:** DESI-like phantom mimicry via coupling comes with more structure growth.

## (2) The y′ floor with uncertainties
**Monte Carlo:** 40 samples of M_t (172.80 ± 0.26 ⊕ 0.5 GeV scheme), α_s (0.1180 ± 0.0009) and the threshold Z-term (±50%). The floor is the minimum needed y′ over μ_match = 10¹⁰–10¹³ GeV.
- **Results:** median **0.400**, 95% range **0.351–0.469**.
- **The robust falsifier:** a measured **y′ < 0.35** excludes every quartic-zero completion with one TeV vectorlike family at about 97.5% confidence. The 0.41 of Pass 12723 was the central value at fixed inputs.

## (3) Orbifold KK thresholds (Hall–Nomura-type SU(5) estimate)
**Setup:** massive levels at 2n/R carry the SM adjoint plus the Higgs doublets; levels at (2n+1)/R carry X,Y plus the triplets. The shift of the predicted α₃⁻¹ is δ₃ − δ₁ + (12/7)(δ₁ − δ₂).

| M_sR | shift in predicted α₃⁻¹ | hybrid mismatch (+0.26 before) |
|---|---|---|
| 10 | −0.12 | ≈ +0.14 (better) |
| 30 | −1.23 | ≈ −1.0 |
| 100 | −5.53 | fails |

- **With protection requiring M_sR ≥ 9.8 (Pass 12723), the orbifold hybrid lives in a narrow window, M_sR ≈ 10–15.**
- **Caveats:** this uses SU(5) rather than SO(10)/E₆ content, my own b-assignments, and no brane-localised kinetic terms (which add O(1/2π) per unit of ln). It is an estimate.

## (1) B′'s two-component dark matter
- **Bound on the dark baryon:** the kinematic bound m_ψ(early) < 4.34 GeV and the drift of 0.931 give m_ψ(today) ≤ 4.04 GeV.
- **Consequence:** with one ψ per baryon, ψ carries **≤ 80%** of the dark matter. **At least 20% must be a second component** (mesogenesis's dark scalar, or an axion).

## (5) Fixed-corpus ternary scaling (130,676 characters, 4000 steps)

| width | fp32 | ternary (curriculum) | gap (bits/char) | zero weights |
|---|---|---|---|---|
| 32 | 2.850 | 3.436 | 0.586 | 47% |
| 48 | 2.695 | 3.236 | 0.541 | 45% |
| 96 (Pass 12723) | 2.608 | 2.914 | 0.306 | 45% |

- **Overall gap ∝ width^−0.59, steepening at larger width** (0.20 from 32 to 48, 0.82 from 48 to 96).
- **On a fixed corpus the gap still closes with width,** consistent with BitNet's parity at scale.

## Status (corrections in bold)
- **Falsifier:** **y′ < 0.35** kills the quartic-zero + vectorlike-quark class at 97.5%.
- **B′:**
  - DM-coupled quintessence fits DESI but **raises σ8 slightly**;
  - ψ carries ≤ 80% of the dark matter.
- **Hybrid:** the orbifold doublet–triplet splitting works only in **M_sR ≈ 10–15**.
- **Ternary:** the gap closes as width^−0.59 on a fixed corpus.
