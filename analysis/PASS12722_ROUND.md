# Pass 12722: the light-5 + 5̄ hybrid clashes with DESI's neutrino-mass bound (the seesaw operator couples the TeV triplets to matter; proton stability then forces Σm_ν ≥ 0.08 eV) and its y′ moves onto B′'s; the light d-type quark is allowed at 1.74 TeV; thawing quintessence recovers a third of DESI's preference; the ternary–fp32 gap shrinks slightly with width

Claude track. **Not a theory of everything.**
- Scripts: `explore_pass12722_round.py` and `explore_pass12722_charlm64.py` (≈45 min).
- Certificates: `data/explore_pass12722_round.json` and `data/explore_pass12722_charlm64.json`.
- Tests: `tests/test_toe_pass12722.py`, 5 tests passing.

## (1) The TeV triplets cannot be decoupled from matter
- **Where the couplings come from:** the seesaw operator (y/M)·16·16·H̄·H̄ gives M_R = y⟨H̄⟩²/M. With one H̄ fluctuation along the pseudo-Goldstone triplet, the same operator gives a triplet–matter coupling g ≈ √2·M_R/⟨H̄⟩, in both the QQ and QL channels (the 126 contraction).
- **No symmetry can forbid it without also forbidding neutrino masses.**
- **Consequence:** proton stability (|g_QQ·g_QL| ≤ 1.7×10⁻²⁵ at M_T = 1.74 TeV, Pass 12721) caps the first-generation entries of M_R. With the minimal SO(10) Dirac relation m_D = m_u:

| ⟨H̄⟩ | m_u(GUT) | max M_R1 (GeV) | min m₁ (eV) | min Σm_ν, normal ordering (eV) |
|---|---|---|---|---|
| 10¹⁶ | 0.4 / 0.7 MeV | 2.9×10³ | 0.055 / 0.17 | 0.19 / 0.51 |
| 4×10¹⁶ | 0.4 / 0.7 MeV | 1.2×10⁴ | 0.014 / 0.042 | **0.082** / 0.15 |

- **Every case exceeds DESI DR2 + CMB's Σm_ν < 0.064 eV** (and < 0.070 with Pantheon+). Inverted ordering is worse.
- **The light-5 + 5̄ version of the hybrid (Pass 12721) is therefore disfavoured by cosmology** in minimal SO(10) flavour structure.
- **Escapes:** 126-type contributions to the Dirac masses, or a small (M_R)₁₁ with large mixing.

## (4) The light 5 + 5̄ moves the hybrid's y′ onto B′'s
Added: the Dirac fermions (3,1)_{1/3} and (1,2)_{1/2} at 1.74 TeV, with Δb_Y = 10/9 and Δb₂ = Δb₃ = 2/3 above 1.74 TeV; λ(M_SS = 8.45×10⁹) = 0.

| M_t | hybrid y′, Q + U | with the light 5 + 5̄ |
|---|---|---|
| 172.57 | 0.472 | **0.507** |
| 172.80 | 0.460 | **0.497** |

- **The extra light states raise y′ by about 0.036, onto B′'s 0.496.** If the hybrid carries a light 5 + 5̄, the B′-vs-hybrid discrimination by y′ (Passes 12715–12716) is lost. Belle II (B → ψ + baryon, B′ only) and proton decay/Σm_ν (hybrid) remain.
- **Together with (1):** the light-5 + 5̄ variant is disfavoured by DESI's Σm_ν and degenerate with B′ in y′. The Q + U-only hybrid (with doublet–triplet splitting still unsolved) stays distinct.

## (2) The light d-type triplet at the LHC
- **Current limits:** vectorlike-B pair limits are 1.45–1.52 TeV (CMS 2024; ATLAS/CMS recast 2412.01761).
- **Combined rate:** with the doublet's B, two B-like states double the rate, shifting the effective limit by about 130 GeV to 1.58–1.65 TeV.
- **A 1.74 TeV triplet is allowed,** and HL-LHC reaches it. It decays via mixing (tW, bZ, bh). Leptoquark/diquark decays go through squarks at M_SS and are negligible.

## (5) Thawing quintessence vs DESI DR2 + CMB + Pantheon+
- **Inputs:** w₀ = −0.857 ± 0.057, w_a = −0.55 ± 0.235, with correlation −0.9 assumed.
- **Thawing relation:** w_a ≈ −1.58(1 + w₀).
- **Result:** best fit w₀ = −0.946, w_a = −0.086, with χ² = 4.16 against 0 (CPL best fit) and 6.33 (ΛCDM).
- **An uncoupled thawing field recovers about a third of DESI's preference** (Δχ² = 2.2 over ΛCDM) and has no G variation. It is the natural dark-energy option for a static-radius B′. DESI's steep w_a < 0 (phantom crossing) remains unexplained.

## (3) A wider ternary character language model (d = 64, 4000 steps, same corpus + this round's text)

| width | fp32 | ternary (curriculum, 46% zeros) | gap |
|---|---|---|---|
| d = 48 (Pass 12721) | 2.97 | 3.42 | 0.46 bits/char |
| d = 64 | **2.79** | **3.21** | **0.43** bits/char |

The gap narrows slightly with width, in the direction of BitNet's scale-dependent parity, but a 7% change over 1.3× width is far from closing it at toy scale.

## Status
- **Hybrid:**
  - The light-5 + 5̄ variant is disfavoured by DESI Σm_ν (minimal flavour) and degenerate with B′ in y′.
  - The Q + U-only variant stays distinct but needs doublet–triplet splitting. That is still the central open problem.
- **B′:** a static dimension plus thawing quintessence is viable (it captures part of DESI's preference).
- **Ternary:** the language-model gap to fp32 is about 0.43 bits/char at d = 64 and shrinks slowly with width.
