# Pass 12700: stop mixing lowers the E₆-SUSY ceiling; A's boundedness is set by its 2HDM quartics alone; SUSY at 10¹⁰ GeV does not unify; A pays a Vissani tuning of ≥ 7×10⁵ with thermal leptogenesis, B pays ≈ 4

Claude track. Follows Pass 12699. **Not a theory of everything.** Script: `toe_pass12700_round.py`; certificate: `data/toe_pass12700_round.json`; tests: `tests/test_toe_pass12700.py`.

The other track has made no new commits since Pass 12699, so `REQUEST_E6_INTERMEDIATE_SCALE_SUSY.md` is unanswered. Item (1) gives the threshold-corrected version of the bridge, ready for when they reply.

## (1) tan β bridge with stop mixing

Matching: λ_SM(M_SS) = (g² + g′²)/8 · cos²2β + Δλ_stop, with Δλ_stop = 3y_t⁴/(8π²)·[X̃_t² − X̃_t⁴/12]. This is the convention of SusyHD ([Vega–Villadoro 2015](https://arxiv.org/abs/1504.05200)) and [Bagnaschi et al. 2014](https://arxiv.org/abs/1407.4081).

| X̃_t | M_t | M_SS ceiling | tan β at 10⁸ / 10⁹ / 10¹⁰ / 10^10.5 GeV |
|---|---|---|---|
| 0 | 172.27 | 1.7×10¹¹ | 1.77 / 1.53 / 1.34 / 1.24 |
| 0 | **172.57** | **5.4×10¹⁰** | 1.72 / 1.47 / 1.26 / 1.13 |
| 0 | 172.87 | 2.0×10¹⁰ | 1.66 / 1.41 / 1.16 / — |
| 1 | 172.57 | 1.2×10¹⁰ | 1.56 / 1.34 / 1.07 / — |
| 2 | 172.57 | 4×10⁸ | 1.25 / — / — / — |
| √6 (maximal) | 172.57 | 2×10⁸ | 1.16 / — / — / — |

- For X̃_t² ≤ 12 (the range allowed by colour-breaking bounds), Δλ_stop ≥ 0. **Mixing therefore lowers the ceiling.** Raising M_SS needs X̃_t ≈ 0 and tan β → 1.
- Pass 12699's statement that no tan β works at M_SS ≥ 10¹¹ GeV holds only at the central M_t. At −1σ in M_t the ceiling rises to 1.7×10¹¹. This agrees with the published high-scale-MSSM bound of ~10¹¹ GeV (degenerate spectrum ≲ 3×10¹¹; [1809.07774](https://arxiv.org/abs/1809.07774)).
- The tan β → 1, X̃_t → 0 corner is the Ibáñez–Valenzuela / Hebecker–Knochel–Weigand scenario (Higgs at the intermediate scale from a string compactification). It is not new here and is cited as such.
- **For the other track:** an E₆ vacuum with H_u and H_d in one 27 and a symmetry that gives tan β = 1 would need small stop mixing and M_SS ≈ μ₀(M_t). That makes it a top-mass prediction with a 1σ band of 2×10¹⁰ to 1.7×10¹¹ GeV.

## (2) Completion A: parameter scan

I scanned 240 random points of V₄ for (H₁, H₂, σ): λ₂ log-uniform in 10⁻²–1; λ₃, λ₄ in [−1, 1]; DFSZ-sized σ portals and κ. Each point was minimised numerically on the 10-dimensional unit sphere from 12 starts.

- 115 points are bounded below. The numerical verdict agrees with the analytic 2HDM conditions at **240/240** points.
- At DFSZ sizes the σ portals and the PQ term κH₁H₂σ² never decide boundedness; the 2HDM quartics alone do.

**Higgs-mass tuning from the heavy doublet:** Δ_H₂ = λ_eff m_H₂²/(16π² μ²), with μ² = m_h²/2.

| m_H₂ | Δ (λ_eff = 0.3) |
|---|---|
| 0.8 TeV (type-II b→sγ floor) | 0.16 |
| 6.4 TeV | 10 |
| 10⁶ GeV | 2.4×10⁵ |
| 10⁸ GeV (Pass 12699's point) | 2.4×10⁹ |

Pass 12699's explicit point is consistent but heavily tuned. A tuned only to the 10% level would put H, A and H± at 0.8–6 TeV, an LHC/FCC target, unless item (4) already forces large tuning.

## (3) Gauge unification (one loop)

| spectrum | α₁ = α₂ at | α₃⁻¹ − α₁₂⁻¹ |
|---|---|---|
| SM | 1.0×10¹³ GeV | −5.60 |
| MSSM at 1 TeV | 9.7×10¹⁵ GeV | −0.62 |
| **high-scale SUSY at 10¹⁰** | 8.0×10¹³ GeV | **−4.10** |
| split: gauginos + higgsinos at 1 TeV, scalars at 10¹⁰ | 8.0×10¹⁵ GeV | −1.17 |

Two-loop running shifts the MSSM entry by about +0.8 (sign corrected in Pass 12701, which computes it: −0.62 → +0.16); the ordering is robust.

**High-scale SUSY at the quartic-zero scale does not unify the couplings.** Complete E₆ 27-plets leave one-loop unification unchanged. If the other track's vacuum puts SUSY at μ₀, unification must come from incomplete multiplets or thresholds in its E₆ → SU(5) chain. The split variant (fermions light) unifies roughly as well as the MSSM. It changes the matching, though: the gaugino and higgsino contributions to the running between 1 TeV and M_SS are not included in item (1).

## (4) Fresh direction: naturalness ledger

Type-I seesaw corrects the Higgs mass by δμ² ≈ m_ν M_N³/(4π² v²), with v = 174 GeV ([Vissani 1998](https://doi.org/10.1103/PhysRevD.57.7027); three-flavour version in [Clarke–Foot–Volkas 2015](https://arxiv.org/abs/1502.01352)). Thermal leptogenesis needs M₁ ≳ 5×10⁸ GeV (flavoured) to 10⁹ GeV (Davidson–Ibarra).

| source | Δ = δμ²/μ² |
|---|---|
| seesaw M_N = 10⁷ GeV | 5.3 |
| **seesaw M_N = 5×10⁸ GeV (thermal-leptogenesis floor)** | **6.7×10⁵** |
| seesaw M_N = 10⁹ GeV | 5.3×10⁶ |
| **B: vectorlike top partner, y′ = 0.51, M = 1.74 TeV** | **3.8** |

- **A with thermal leptogenesis costs Δ ≳ 7×10⁵.** It avoids this only with resonant or non-thermal leptogenesis. A 2HDM with tan β ≳ 4 can relax the bound (Clarke–Foot–Volkas), but A's second doublet has v₂ ≈ 0.
- **B costs Δ ≈ 4.** Its Dirac bulk neutrinos pay no Vissani cost, and gravity loops at a species scale of ~10⁹ GeV give δμ² ~ Λ⁴/M_Pl² ~ 0.1 GeV².
- Once A's tuning is ≥ 7×10⁵, the choice of m_H₂ hardly matters up to ~2×10⁶ GeV, so the TeV-doublet prediction in item (2) holds only if A changes its leptogenesis.
- Naturalness is a contested prior and is **not** added to the Bayes factors of Pass 12698. The ledger is a separate axis on which B is better by about five orders of magnitude.
- PQ quality (Planck-suppressed operators of dimension ≥ 12 at f_a = 10¹¹ GeV) is already in `PASS12603_12608_PQ_ASSISTED_UNIFICATION.md` and is cited, not re-derived.

## (5) Summary page

"Where λ Vanishes" was refreshed with the haloscope coverage, the soft-lepton acceptance, the E₆ bridge with its threshold band, and this ledger.
