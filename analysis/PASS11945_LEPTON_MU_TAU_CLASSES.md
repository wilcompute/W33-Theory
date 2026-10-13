# Pass 11945: PMNS excludes the charge-rule leptons in every branch; one Higgs Wilson line forces the μ–τ paradigm

Producer: `analysis/w33_pass11945_lepton_mu_tau_classes.py`
Certificate: `data/w33_pass11945_lepton_mu_tau_classes.json`
Regression: `tests/test_w33_pass11945.py`
Track: Claude. Uses the identities of Pass 11944. Decides its fork, and in doing so disfavours the 11939/11940 neutrino
prediction within the framework.

## 1. A branch-independent exclusion

**The identity.** With a μ–τ-clean neutrino sector, the PMNS column of the odd neutrino equals the odd contents of
(e, μ, τ) (Pass 11944).

**What the data require.** The measured |U| columns are:

| column | e | μ | τ |
|---|---|---|---|
| ν₁ | 0.82 | 0.36 | 0.43 |
| ν₂ | 0.55 | 0.60 | 0.58 |
| ν₃ | 0.15 | 0.74 | 0.66 |

Whatever neutrino is odd, **the muon must be at least 0.36 odd**.

**The verdict.** The charge-rule charged leptons of Pass 11942 have a muon odd content of 0.08 at both fits. They are
excluded in every branch.

## 2. Minimal escape: a Wilson line on H_d

**The extension.** Give the Higgs H_d its own Wilson line h_d.
* The down sector is unchanged, since z_d is fitted anyway.
* The leptons get z_e = 6·z_d − 5·h_d: one complex parameter.

**Fitting the masses alone.** Fitting only the two charged-lepton mass ratios gives many solutions: 29 and 36 distinct
ones on the two quark fits, keeping |Im z_e| ≤ 0.5.

**The common profile.** **Every** solution has the same odd-content profile:
* one charged lepton nearly μ–τ even (odd content ≤ 0.12);
* the other two near-maximal (0.61–0.79).

There are three classes, according to which lepton is even.

**A traced outlier.** The |Im z_e| bound keeps the Gaussian centre Im z/Im τ_d (about 29 at the bound) well inside the
N = 40 theta truncation. One apparent outlier at Im z_e = 0.652 had odd contents (0.27, 0.79, 0.55) at N = 40. At N = 90
it becomes (0.001, 0.55, 0.84), with masses off: a truncation artefact, which also obeys the profile once computed
correctly.

## 3. Consequences

**Branch (a) is impossible in this family.** Branch (a) is the odd-ν₂ branch, and it needs all three charged leptons
about 0.58 odd. Fits to the masses plus the ν₂ column give χ² = 87 and 45; the ν₁ column gives 52.
* So the near-product, Wilson-free neutrino relation of Passes 11939/11940 (Σm_ν = 0.0596 eV, m₁ = 0.8 meV) is
  **disfavoured within the framework**.
* It survives only if the neutrino sector itself is μ–τ-broken, in which case its Weber premise changes as well.

**The μ–τ paradigm (odd ν₃) emerges.** In the e-even class, the charged-lepton contribution is:
* θ₁₃ = 0.2–0.5°;
* sin²θ₂₃ ∈ [0.37, 0.59], against data 0.561.

**A combined fit.** Fitting the masses plus the ν₃ column (2 parameters, 4 constraints) gives χ² = 7.7 at both quark
fits:
* m_μ/m_τ = 0.0585 and m_e/m_μ = 0.00482;
* sin²θ₂₃ = 0.559;
* the one miss is θ₁₃, 0.5° against 8.6°.

**What remains for the neutrino side.** θ₁₃ and θ₁₂ must come from the neutrino side. ν₃ odd requires the odd theta
coefficient to dominate, |Ω₁₂| = O(1) or an equivalent mechanism. That is the next construction.

## Scope

* **What the searches cover.** The exclusion in §1 is branch-independent but assumes a μ–τ-clean neutrino sector.
  "Every solution" is a statement about the multistart sets on the two quark fits, within the truncation-safe range.
* **One new parameter.** The H_d Wilson line is new: it is not fixed by the charge rule.
