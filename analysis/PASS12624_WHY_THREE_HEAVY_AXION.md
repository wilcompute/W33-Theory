# Pass 12624: unification does not select three copies; heavy brane-instanton axion; an inflation prior turns into a c′ band

Claude track. Continues `PASS12621_OUTSIDE_LINKS.md`. Producer: `analysis/w33_pass12624_why_three_heavy_axion.py` (reads `analysis/toe_uv/items_234.json`, `items_more.json`, `class_fit_dovekie.json`). Test: `tests/test_w33_pass12624.py`. Scripts: `analysis/toe_uv/items_234.py`, `items_more.py`.

**Not a theory of everything.** Four bookkeeping tests of the axion-unification candidates.

## 1. Why three vectorlike copies? Unification does not say

Two-loop running (`pq_twoloop.solve2`, three starting points) with n vectorlike copies of each trinification piece:

| piece | SM content (Dirac) | n = 1 | n = 2 | n = 3 | n = 4 | n = 5 |
|---|---|---|---|---|---|---|
| (3,3̄,1) | (3,2,1/6)+(3,1,−1/3) | none | M_X 8.2×10⁸ | 2.8×10¹¹ | 5.3×10¹² | 3.0×10¹³ |
| (3̄,1,3) | (3,1,2/3)+2(3,1,−1/3) | none | none | none | none | none |
| (1,3,3̄) | 2(1,2,1/2)+(1,1,1) | M_U ≈ 5×10¹² for every n: proton dead | | | | |
| full 27+27̄ (control) | all three | none | none | none | none | none |

For the (3,3̄,1) piece, M_U stays at 3.4–3.6×10¹⁶ GeV and α_U⁻¹ ≈ 34.6 for every n from 2 to 5. τ_p ≳ 2×10³⁸ yr throughout. **The control behaves as it must:** a complete E6 multiplet shifts all three b_i equally at one loop, and no solution is found.

So three copies are **not** selected by unification. Two to five all work, and only M_X moves. Three is the number of generations, but nothing here ties the two. The trinification candidate also has a splitting problem: it needs only the (3,3̄,1) piece of each 27 light, which is a doublet-triplet-type split. This pass does not solve that. What fixes n is the σ-stability axion ceiling of Pass 12612 together with the PQ scale: larger n means larger M_X and lighter axions.

"none" means no solution with M_Z < M_X < M_U was found from three starts. It is not a proof.

## 2. Heavy axion from brane SU(3) instantons (orbifold variant)

On the SM brane, small instantons add K e^(−2π α_b⁻¹) R⁻⁴ cos(a/f − θ_b). I take K ≈ ∏ y_q/(4π) ≈ 2×10⁻²⁷ (rough high-scale Yukawas, from memory; uncertain by several orders), with 1/R = 5×10¹⁵ and f = 10¹¹ GeV.

| α_b⁻¹ | brane / χ_QCD | m_a | τ(a→gg) |
|---:|---:|---:|---:|
| 1 | 7×10³⁷ | 465 TeV | 6×10⁻¹⁵ s |
| 3 | 2×10³² | 870 GeV | 10⁻⁶ s |
| 5 | 8×10²⁶ | 1.6 GeV | 150 s |
| 10 | 2×10¹³ | 244 eV | n/a (not computed) |
| 15 | 0.4 | 68 μeV | QCD-like |
| ≥ 20 | < 10⁻¹⁴ | 57 μeV | QCD axion |

- The brane term dominates the QCD mass for α_b⁻¹ < 15, and is harmless even when misaligned only above α_b⁻¹ ≈ 18.5. A factor 10¹⁰ in K moves both thresholds by about 3.7.
- Apparent unification in the orbifold usually assumes small brane kinetic terms; Pass 12617 found that brane terms move M_X by orders of magnitude. Here that means small α_b⁻¹. Identifying the instanton action with the brane coupling alone is my simplification. In that regime the axion solves strong CP only if θ_b = θ_QCD (aligned), and it is then heavy.
- **BBN:** with Γ = α_s² m³/(32π³f²), only α_b⁻¹ ≲ 3 (m_a ≳ TeV) decays before 0.1 s. α_b⁻¹ ≈ 5 to 14 lands in the window of cosmological trouble for an abundant relic. The decay is computed only for m_a ≥ 1 GeV.
- **Consequence for Model A on the orbifold:** if brane terms are small, the axion is a TeV-scale heavy axion, not the dark matter, and something else must be the dark matter. This is the heavy aligned-axion escape from the E/N = 8/3 line of arXiv:2511.21830, named as an option in the earlier write-ups; now it carries a price.

## 3. Joint target: inflation prior → band on c′

Along the fading-coupling profile (Dovekie fits), n_s and c′ are strongly degenerate: n_s = 0.971, 0.970, 0.966, 0.961, 0.951 at c′ = 0.02, 0.03, 0.05, 0.07, 0.10. A Higgs-portal or SMASH-type inflation prior n_s ∈ [0.965, 0.968] then becomes

**c′ ∈ [0.040, 0.055],** which contains the free fit c′ = 0.053.

ΛCDM's n_s = 0.970 lies outside that band. CPL gives n_s = 0.967 with w₀ = −0.81, wₐ = −0.69. SMASH predicts a lower bound r ≳ 0.004 and running α ≳ −8×10⁻⁴ (Tamarit, arXiv:1705.06951, as summarised by the search tool; Ballesteros et al., arXiv:1608.05414). This corrects my earlier memory-based statement of r ≈ 0.004 as a value.

So Model A + Higgs-portal inflation + an evolving dark energy that crosses −1 is a consistent joint target: (n_s ≈ 0.966, r ≳ 0.004, w₀ ≈ −0.8, wₐ ≈ −0.7 or c′ ≈ 0.05). CMB-S4 (r) and DESI DR3 / Euclid (w) can test it. These are point fits. The n_s Fisher widths are in Pass 12623.

## 4. Cross-check of Chat's 6e0f24d33

For X = 3(B − 3L_e) with T(−9), S(−18) and a vectorlike (3,2,1/6) of X = ±1, an independent count with exact fractions gives B_YY = 127/18, B_YX = 52/3 and B_XX = 383. These match Chat's certificate. I did not check its anomaly list or the S†T² minimality argument beyond the charge (+18 − 18 = 0, which holds).

## Limits

- One- and two-loop running only, no threshold spread (Pass 12610 showed it matters).
- K and the instanton prefactor are order-of-magnitude.
- The c′ band uses profile points, not posteriors.
- The SMASH r bound is from search summaries, not from reading the papers.
- No novelty is claimed for the heavy-axion mechanism. Aligned small-instanton heavy axions are an existing literature that I have not searched here.
