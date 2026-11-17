# Pass 12685: the intermediate-scale suite — SMASH threshold window, a vectorlike-quark rescue of the dark dimension, seesaw, FCC-ee forecast, axion ≠ EDE

Claude track. Follows Pass 12684. **Not a theory of everything.** Script: `toe_pass12685_intermediate_scale_suite.py`; certificate: `data/toe_pass12685_intermediate_scale_suite.json`.

**Running.** Two-loop SM running as in Pass 12684 (Buttazzo et al. NNLO matching, three-loop offset folded into an effective M_t). Extra fields enter at one loop. Control: λ = 0 at √(v M_Pl) needs M_t = 172.566 (Pass 12684: 172.57). ✓

## (1) SMASH-type threshold: the window is open but closes fast with M_t

The Peccei–Quinn (PQ) radial mode has mass m_ρ = √(2λ_σ) f_a and shifts the Higgs quartic by δ = λ_Hσ²/λ_σ above m_ρ. Stability requires two things:
- m_ρ ≤ μ₀, so the SM quartic is still positive below the threshold;
- δ ≥ −min λ_SM above it.

f_a is taken from the 2025 lattice window, (0.88–1.27)×10¹¹ GeV.

| M_t | μ₀ (GeV) | min λ_SM | λ_σ upper bound | λ_Hσ lower bound |
|---|---|---|---|---|
| 172.14 | 3.1×10¹¹ | −0.0075 | 3.0–6.3 | 0.086 √λ_σ |
| **172.57** | **5.4×10¹⁰** | **−0.0103** | **0.09–0.19** | **0.10 √λ_σ** |
| 173.00 | 1.3×10¹⁰ | −0.0131 | 0.006–0.012 | 0.11 √λ_σ |
| 173.43 | 4.2×10⁹ | −0.0159 | 0.0006–0.0012 | 0.13 √λ_σ |

At the measured top mass, an axion-DM PQ field with λ_σ ≲ 0.1 and portal λ_Hσ ≳ 0.1√λ_σ stabilises the Higgs. At M_t ≈ 173.4 the PQ self-coupling must be below 10⁻³. That is not forbidden (SMASH inflation wants λ_σ ~ 10⁻¹⁰), but it shows how directly the top mass constrains the PQ sector.

## (2) Rescuing the dark dimension: a TeV vectorlike top partner with y′ ≈ 0.5

Pass 12684 excluded λ(M₅) = 0 at the measured M_t. Add one vectorlike family: a doublet Q and singlet T with Dirac mass M_VL and Yukawa y′ H Q T^c. It enters the running like a second top, with Δb₁ = Δb₂ = Δb₃ = 2. Then λ(M₅) = 0 at M_t = 172.57 needs:

| M_VL | R = 1 μm (M₅ = 5.7×10⁸) | R = 30 μm (M₅ = 1.8×10⁸) |
|---|---|---|
| 1.5 TeV | y′ = 0.509 | y′ = 0.530 |
| 3 TeV | 0.498 | 0.522 |
| 10 TeV | 0.484 | 0.514 |

y′ decreases with scale (QCD), so it stays perturbative up to M₅. With a single Yukawa the fermion mass matrix [[M_Q, y′v/√2], [0, M_T]] has v-independent determinant. So the Higgs–gluon coupling is unshifted at leading order (low-energy theorem). The EW T parameter and the mixing with the SM needed for the partners to decay were **not computed**.

> **Result.** "The Higgs quartic vanishes at the dark dimension's species scale" is not dead. It predicts a TeV-scale vectorlike top partner with an O(0.5) Higgs Yukawa, a concrete LHC/FCC-hh target. Without new coloured fermions it is excluded (Pass 12684).

## (3) Seesaw at the intermediate scale: harmless to stability

m_ν₃ = 0.05 eV needs y_ν = 0.0041 / 0.0128 / 0.041 for M_N = 10¹⁰ / 10¹¹ / 10¹² GeV. The resulting shift in λ(M_Pl) is −5×10⁻⁷ / −4×10⁻⁶ / −3×10⁻⁵, far below the theory error. A seesaw at the axion/quartic-zero scale is compatible, and leptogenesis-compatible (M_N ≳ 10⁹ GeV).

## (4) Precision forecast

- **Sensitivities:** d log₁₀μ₀/dM_t = −1.56 GeV⁻¹; d/dα_s = 563; d/dM_h = 0.87 GeV⁻¹.
- **σ(log₁₀ μ₀) today:** 1.06 decades. This includes 0.5 GeV of pole/MC-mass ambiguity, α_s ± 0.0009, M_h ± 0.11 and the matching errors.
- **σ(log₁₀ μ₀) in the FCC era:** 0.27 decades, with M_t ± 0.05, α_s ± 0.0003 and M_h ± 0.02. Without theory matching errors it would be 0.19. The NNLO matching uncertainty is the floor.
- The √(v M_Pl) variants span 0.43 decades, so FCC precision **marginally separates them**. Better λ and y_t matching (three-loop) is needed for a clean separation.
- **Planck boundary λ(M_Pl) = 0** (asymptotic safety / multiple-point criticality): 3.7σ today, **9.4σ** in the FCC era if the central value holds.

## (5) The intermediate-scale QCD axion cannot be early dark energy

- Early dark energy needs a field with f ~ 0.2 M_Pl and m ~ 10⁻²⁷ eV, so m²f² ~ 0.2 eV⁴.
- The QCD axion has m_a²f_a² = χ_top ≈ 3×10³¹ eV⁴, i.e. 10³² times larger.
- Its mass is 10²³ times too large to stay frozen until z ~ 3500.
- If early dark energy resolves the Hubble tension, it needs a separate ultralight field (e.g. a string axiverse member). It is not the axion in this picture.

## Status of the intermediate-scale picture after 12684–12685

**Consistent (numerical):**
- the quartic zero at μ₀ ≈ 5×10¹⁰ GeV for the measured top mass;
- post-inflationary axion DM at f_a ≈ 10¹¹ GeV (2025 lattice);
- PQ-threshold stabilisation with λ_σ ≲ 0.1;
- a seesaw/leptogenesis scale of 10¹⁰–10¹² GeV;
- √(v M_Pl).

**Excluded:**
- λ(M_Pl) = 0 (3.7σ);
- λ(M_GUT²/M_Pl) = 0 (2.7σ);
- λ(M₅) = 0 for a micron dark dimension without new coloured states (≥ 4σ).

**Rescue:** the dark dimension needs a TeV vectorlike quark with y′ ≈ 0.5.

**Tests:** MADMAX/ALPHA at 45–65 μeV; FCC-ee M_t; LHC/FCC-hh vectorlike-quark searches; sub-millimetre gravity at 1–30 μm.

The single-coincidence look-elsewhere probability (12%, Pass 12684) still applies to the √(v M_Pl) match.
