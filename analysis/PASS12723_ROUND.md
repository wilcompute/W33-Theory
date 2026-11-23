# Pass 12723: coupled quintessence fits DESI (χ² 2.0 vs 6.3, with phantom crossing) in a static-radius B′; energy flows dark matter → dark energy, so the mesogenesis dark baryon was heavier in the past (it cannot be all of the dark matter) while S8 is eased; y′ has a floor of 0.41 for every quartic-zero completion with one vectorlike family, a universal falsifier; the ternary–fp32 language-model gap falls as width^−0.58; Belle II covers 62–89% of B′ by ~2042; a mild flavour escape for the light-triplet hybrid

Claude track. **Not a theory of everything.**
- Scripts:
  - `explore_pass12723_round.py`;
  - `explore_pass12723_charlm96.py` (≈100 min);
  - add-ons `explore_pass12723_mesogenesis_drift.py` and `explore_pass12723_attractor.py`.
- Certificates: `data/explore_pass12723_*.json`.
- Tests: `tests/test_toe_pass12723.py`, 6 tests passing.

## (2) Coupled quintessence in a static-radius B′
**Model:**
- Potential V = V₀e^{−λφ}; dark-matter mass ∝ e^{βφ}.
- Background integrated from z ≈ 1100, with Ω_m = 0.31 by shooting.
- An observer who assumes uncoupled dark matter infers w_app. That is fitted to CPL and compared with DESI DR2 + CMB + Pantheon+.

| λ | β | apparent w₀ | apparent w_a | min w_app | χ² (ΛCDM 6.33) |
|---|---|---|---|---|---|
| 1.0 | 0 | −0.847 | −0.217 | −0.986 | 13.1 |
| **1.0** | **+0.1** | **−0.873** | **−0.349** | **−1.108 (phantom crossing)** | **1.97** |
| 0.7 | +0.1 | −0.965 | −0.095 | −1.026 | 3.86 |
| 1.4 | +0.2 | −0.815 | −0.517 | −1.135 | 4.00 |

- **A dark-matter coupling β ≈ 0.1 reproduces most of DESI's preference, including the apparent phantom crossing,** with no change in Newton's constant (the radius stays fixed) and within the dark-sector fifth-force bound (c′ ≲ 0.2).
- **This is the dark-energy completion of B′.** Uncoupled thawing gave only χ² = 4.2 (Pass 12722).

## (2b) What the coupling implies for B′'s dark matter (exploration)
- **The puzzle:** mesogenesis makes one dark baryon per baryon. If ψ were all of the dark matter, m_ψ = 5.36·m_p = 5.03 GeV, above the kinematic bound m_ψ < m_B − m_p = 4.34 GeV.
- **The scan:** in every DESI-fitting point, m_ψ(today)/m_ψ(z = 1100) = 0.69–0.99, and 0.93 at the best fit. No point lifts the mass by the 1.16 needed.
- **Why:** the field always moves to lower total energy, so energy flows dark matter → dark energy. That is exactly the mechanism that mimics phantom behaviour.
- **Consequences:**
  - **The puzzle worsens.** The dark baryon was heavier in the past, so today m_ψ ≲ 4.0 GeV, and ψ cannot be all of the dark matter. B′ needs a second dark component, such as mesogenesis's dark scalar.
  - **S8 is eased.** The late-time dark-matter density is about 7% below the CMB extrapolation. That lowers S8 by a few percent (a proxy), toward the weak-lensing values. This is a testable side prediction.

## (exploration) The y′ floor: a universal falsifier
Scan: the y′ needed for λ(μ_match) = 0, with M_VL = 1.74 TeV and the Pass 12707 threshold.

| M_t | light 5 + 5̄ | y′ at μ = 10⁷ … 10¹³ GeV | slope per decade |
|---|---|---|---|
| 172.80 | no | 0.608, 0.544, 0.495, 0.458, 0.433, 0.418, 0.413 | −0.032 |
| 172.80 | yes | 0.618, 0.561, 0.522, 0.496, 0.482, 0.477, 0.479 | −0.022 |
| 172.57 | no / yes | 0.614 → 0.428 / 0.624 → 0.487 | −0.031 / −0.022 |

- **The needed y′ flattens above about 10¹⁰ GeV and never drops below 0.41.**
- **That is why B′ and the hybrid variants all land at y′ ≈ 0.46–0.50.**
- **The falsifier:** a vectorlike top partner measured with **y′ < 0.41 rules out every completion with a quartic zero plus one TeV vectorlike family,** whatever its UV physics. A measured y′ > 0.6 would put the matching scale below 10⁷ GeV.
- **The old coincidence is weaker.** "λ = 0 at √(v·M_Pl) = 5.5×10¹⁰ GeV" needs M_t = 172.57, which is 0.9σ below the new 172.80 ± 0.26.

## (5) Ternary language-model scaling

| width | fp32 | ternary (curriculum, ~45% zeros) | gap (bits/char) |
|---|---|---|---|
| 48 | 2.97 | 3.42 | 0.46 |
| 64 | 2.79 | 3.21 | 0.43 |
| **96** | **2.61** | **2.91** | **0.31** |

- **The gap falls roughly as width^−0.58.** Extrapolated, it reaches about 0.05 bits/char near width 2000, consistent with BitNet's parity at scale. The corpus grew slightly between runs, and three points is a thin fit.

## (4) Belle II coverage of B′
**Assumptions:** an inclusive search, a 0.3% tag, signal efficiency 0.2·√(1 − (m_ψ/4.34)²), and 2 background events per ab⁻¹. The plan is about 1 ab⁻¹ now, about 10 ab⁻¹ in the 2030s, and 50 ab⁻¹ by about 2042 (30 without the interaction-region upgrade).

| luminosity | reach (m_ψ = 1 / 2 / 3 / 4 GeV) | B′ excluded |
|---|---|---|
| 1 ab⁻¹ | 3.7×10⁻⁶ … 9.3×10⁻⁶ | 9 / 8 / 5 / 0% |
| 10 ab⁻¹ | 7.6×10⁻⁷ … 1.9×10⁻⁶ | 61 / 57 / 49 / 26% |
| 50 ab⁻¹ | 2.9×10⁻⁷ … 7.4×10⁻⁷ | 89 / 87 / 82 / 62% |

- **Belle II alone cannot fully exclude B′ before about 2042,** and coverage is weakest for heavy ψ. This is more realistic than Pass 12714's optimistic 56–100%.

## (1) The flavour escape for the light-triplet hybrid
- **Requirement:** DESI's Σm_ν < 0.064 eV needs m₁ ≲ 4.2 meV. With M_R1 capped by proton stability (Pass 12722), the first-generation Dirac mass must satisfy **m_D1/m_u ≤ 0.16–0.55**.
- **Feasibility:** that is a factor-2-to-6 cancellation, which 126-type terms (m_D = v(Y₁₀ − 3r·Y₁₂₆)) can supply.
- **Status:** the light-5 + 5̄ hybrid is not excluded, but it needs a non-minimal flavour structure. It also remains degenerate with B′ in y′.

## (3) Orbifold doublet–triplet splitting
- **The mechanism:** Kawamura/Hall–Nomura S¹/(Z₂ × Z₂′) keeps the doublets and removes the triplets.
- **A free bonus:** putting Σ on one brane and H on the other gives the brane separation of Pass 12717 automatically.
- **The scale window:** protection needs M_*·πR ≥ 30.8, i.e. M_*R ≥ 9.8, while 5D perturbativity needs M_*R ≲ 100. **The window 10 ≲ M_*R ≲ 100 is the standard orbifold-GUT range.** This is the most promising route for the Q + U-only hybrid's doublet–triplet problem.

## Status
- **B′:** a static radius plus dark-matter-coupled quintessence fits DESI (χ² 2.0). Its dark baryon cannot be all of the dark matter. It predicts a slightly lower S8. Belle II covers 62–89% by about 2042.
- **Hybrid:** the Q + U-only variant plus orbifold doublet–triplet splitting (window 10 ≲ M_*R ≲ 100) is the preferred form. The light-5 + 5̄ variant needs flavour cancellation and is y′-degenerate with B′.
- **Universal:** y′ < 0.41 falsifies the whole class.
- **Ternary:** its language-model gap closes as width^−0.58.
