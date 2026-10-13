# Pass 11943: the minimal theta-null SU(5) picture gets the PMNS matrix wrong — and a correction to Pass 11942

Producer: `analysis/w33_pass11943_pmns_no_go_and_lepton_band.py`
Certificate: `data/w33_pass11943_pmns_no_go_and_lepton_band.json`
Regression: `tests/test_w33_pass11943.py`
Track: Claude. Tests the chain of Passes 11938–11942 on lepton mixing; corrects Pass 11942.

## Setting

* **Where L sits.** The lepton doublet L sits on the 5̄ factor, at τ_d in the cusp regime.
* **Charged leptons.** Y_e = Y_dᵀ, with the hypercharge Wilson argument z_e = 6·z_d (Pass 11942).
* **Dirac neutrinos.** L·N·H_u has Wilson argument −Y_N·a = 0 under the same charge rule.
* **Neutrino basis.** With a near-product seesaw (Pass 11940), the neutrino left basis is the parity-clean
  Gram–Schmidt basis of f₀, f₁, f₂ at τ_d, ordered ν₃, ν₂, ν₁.

So PMNS = U_e†U_ν is fixed by the quark fit, with **no free parameter**.

## 1. No-go (robust)

**Best fits** (angles in degrees):

| | θ₁₂ | θ₂₃ | θ₁₃ |
|---|---|---|---|
| fit A | 45.1 | 83.0 | 1.1 |
| fit B | 88.6 | 5.7 | 45.1 |
| data | 33.4 | 49 | 8.6 |

**Posterior** (frozen record; quark-data MCMC, 2 chains of 3000 steps, 5–95%):

| | θ₁₂ | θ₂₃ | θ₁₃ |
|---|---|---|---|
| A | 44.8–45.2 | 80.3–85.2 | 0.3–1.7 |
| B | 86.8–88.6 | 2.6–5.0 | 45.1–45.2 |

**Other Wilson rules.** Changing the neutrino Wilson rule (z_ν/z_d ∈ {1, 2, 3, −3/2, −3, 6}) does not rescue either
best fit.

## 2. Why it fails

**The neutrino basis is tri-bimaximal.** Near the cusp, the parity-clean 5̄ basis is the set of tri-bimaximal vectors:
(1,1,1)/√3, (0,1,−1)/√2 and (2,−1,−1)/√6. The deviation is 2·10⁻⁴ at fit B's τ_d. This is the familiar S₃/TBM structure
already in the corpus (BT920, Pass 11225, Pass 11243).

**Problem 1: the wrong mass slot.** The theta parity puts the μ–τ-odd vector f₁ = (0,1,−1)/√2 at the **middle** mass,
since it enters at order Ω₁₂. TBM and TM₁ need it to be ν₃. With a charged-lepton basis near the qutrit basis this gives
θ₁₂ ≈ 0 and θ₁₃ ≈ 35°.

**Problem 2: the charged-lepton basis.** The hypercharge-Wilson charged-lepton basis is instead nearly democratic. It
rotates the TBM vectors into near-trivial or near-permutation mixing.

**What would be needed.** Large but non-maximal PMNS mixing needs the charged-lepton and neutrino L-bases at
*different* points of the level-3 geometry: a residual-symmetry misalignment of the kind in Passes 11225 and 11243. The
minimal picture does not provide it.

## 3. Correction to Pass 11942

**The new chain.** A fifth MCMC chain (branch B, seed 7, median χ² 4.4, so quark-acceptable) gives:
* m_μ/m_τ = 0.029–0.046;
* m_e/m_μ = 0.0071–0.017.

These bands **exclude** the data (0.0588, 0.00474).

**Withdrawn.** The 11942 statement that "both measured ratios lie near the centre of every chain's band".

**What survives.**
* **The band.** Over the quark-acceptable region, the rule z_e = 6·z_d gives m_μ/m_τ ≈ 0.029–0.081 and
  m_e/m_μ ≈ 0.002–0.017 (union of 6 chains).
* **What it does and does not include.** That band contains the data and excludes minimal SU(5) (0.0185, 0.050).
* **Reading.** The right direction and order, Georgi–Jarlskog-like, but not a sharp prediction.

**The lesson.** Local MCMC chains in a multimodal posterior must be counted as a union, and one more chain can change a
claim. This is the corpus rule "vary the sample before believing".

## Reading

**The tally.** The theta-null SU(5) chain of Passes 11938–11942 now stands as follows:

| item | status |
|---|---|
| up-texture law (Weber) | exact |
| neutrino mass relation (normal ordering, Σ = 0.0596 eV) | conditional |
| CKM | existence, not prediction |
| lepton mass ratios | band, not sharp |
| PMNS | **fails** in the minimal form |

**The next structural requirement.** The PMNS failure is the sharpest constraint so far: the neutrino and
charged-lepton doublet bases must not share one level-3 point.
