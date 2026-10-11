# Pass 11920: the diagonal-pair texture — slopes quantised in π/3, robust m_d = m_e = 0, and what the A₂ model can reach

Producer: `analysis/w33_pass11920_diagonal_pair_texture.py`
Certificates:
* `data/w33_pass11920_diagonal_pair_texture.json`
* `data/w33_pass11920_a2_scan_frozen.json`

Regression: `tests/test_w33_pass11920.py`
Track: Claude. Route 3 of the plan after Pass 11917: does the two-coset Schmidt ratio δ give m_s/m_b?

## 1. Quantised slopes

**Setup.** Take a scalar modulus Ω = it·1 and symmetric (zero) Wilson lines.

**Result.** Every single-Higgs log singular-value ratio is linear in t, with slope an **integer multiple of π/3**.
Slope × 3/π is within 5·10⁻³ of an integer.

| sector | ratio | slope / π |
|---|---|---|
| A₂ down, δ = s₂/s₁ | s₂/s₁ | −4/3, −2/3 (or 0) |
| A₂ up | s₂/s₁ | −4/3 |
| A₂ up | s₃/s₂ | −2/3 |
| (1,1,4) down | s₂/s₁ | −5/3, −1, −1/3 |

**Origin.** The quantum is the (3/m)Ω Gaussian of Pass 11917, evaluated on coset representatives.

## 2. No parameter-free prediction

**The plan.** Fit the A₂ moduli (t, β), with Ω = it(1 + βJ), to the up ratios m_c/m_t and m_u/m_c, and then *predict*
m_s/m_b = δ from each down Higgs mode.

**Why it fails.** At symmetric Wilson lines the A₂ up spectrum is always (1, x, x) or (1, 1, x). This is Pass 11918's
lemma; the maximum gap is 10⁻¹⁵. The fit therefore has no solution.

**What it needs.** The hypercharge Wilson line. That adds continuous intercepts, so there is no parameter-free prediction.

## 3. m_d = m_e = 0 is robust

**Why.** With the hypercharge Wilson line, the A₂ down **and** lepton Yukawas are still dual-pair Yukawas. So by Pass
11917, m_d = m_e = 0 exactly for every modulus, Wilson line and Higgs mode.

**The scan maxima are a numerical artefact.** In the 210-moduli scan the maxima were m_d/m_s, m_e/m_μ ≈ 10⁻⁷.
* These do **not** change with the grid (G = 12 → 16).
* They **are** theta-truncation residuals: |n_i| ≤ 4 gives 1.2·10⁻⁷, while |n_i| ≤ 7 and ≤ 9 both give 3·10⁻¹⁵.

## 4. The A₂ scan (40 320 rows, frozen)

| question | result |
|---|---|
| masses only: m_s/m_b, m_u/m_c, m_c/m_t, m_μ/m_τ | best rms log-deviation 0.64 (about a factor 1.9) |
| down vs lepton | median (m_μ/m_τ)/(m_s/m_b) = 1.00: no Georgi–Jarlskog factor (Pass 11918) |
| CKM shape | 81% near-permutation; of the aligned rows, 83% have V_cb = 0 exactly |
| realistic quark masses and CKM together | **0 of 63** rows with realistic quark masses have a hierarchical CKM with all angles nonzero |

## Reading

**The model fails on three counts.**
1. It needs a source for m_d and m_e. Tree level gives zero, and Pass 11919 shows that for A₂ no modulus can change this.
2. It needs a Georgi–Jarlskog splitting, which the hypercharge Wilson line does not supply.
3. It needs a non-monomial up sector for the CKM.

**What survives.** The quantised slopes (multiples of π/3) are a clean structural fact. In the single-Higgs model,
log m_s/m_b and log m_c/m_t are asymptotically commensurate. But that is not a prediction once Wilson lines are on.

## Prior art

Corpus: Passes 11915–11919.
