# Pass 11939: the symmetric-channel Weber law — normal ordering and m₁m₃/m₂² = m_u m_t/m_c²

Producer: `analysis/w33_pass11939_symmetric_weber_neutrinos.py`
Certificate: `data/w33_pass11939_symmetric_weber_neutrinos.json`
Regression: `tests/test_w33_pass11939.py`
Track: Claude. Builds on Pass 11938 (the Weber law) and reconsiders Pass 11933 (the inverted-ordering reading).

## Why this pass

**The prediction under test.** The only concrete neutrino prediction in the corpus is Pass 11933: inverted ordering,
with m₃ ≈ 1.3 meV.

**Its consequence.** That spectrum implies Σm_ν = 0.1006 eV (0.100–0.103).

**The data it now faces.**
* **Cosmology.** DESI DR2 BAO + CMB gives Σm_ν ≲ 0.064 eV in ΛCDM (about 0.16 eV with evolving dark energy).
  Recent ACT DR6 + DESI DR2 analyses give similar limits (arXiv:2606.17994).
* **Oscillations.** These mildly prefer normal ordering. JUNO plus the long-baseline experiments are expected to reach
  3σ within about five years (arXiv:2606.14121).
* **Double-beta decay.** The full KamLAND-Zen dataset gives m_ββ < 28–122 meV (PRL 135, 262501 (2025)).

**Status of Pass 11933.** In ΛCDM it is disfavoured. This pass asks what the new geometric mechanism of Pass 11938
predicts instead.

## Results

**1. Symmetric channels need a swap-symmetric home.**
* **Which channels.** Two couplings are flavour-symmetric: the Weinberg operator L_aL_bHH and the SU(5) up coupling
  10_a10_bH.
* **Condition.** Realised as the reshaped theta null Y_ab = Θ[(a,b)](Ω), such a coupling needs Y = Yᵀ. That requires
  Ω = [[τ, ε], [ε, τ]] (checked: Y symmetric to 10⁻¹⁵).
* **The law.** By Pass 11938,

  **m_light · m_heavy / m_mid² = |𝔣(τ)|¹⁶ / 4**

  (checked at 6 random τ, relative error ≤ 10⁻⁸).
* **CM values.** τ = i (the square torus of Pass 11937) gives 4; τ = ω gives 2^{2/3}; τ = 1+i gives 1.

**2. Ordering lemma.**
* **Inverted ordering.** With the oscillation data, an inverted spectrum always has m₃m₂/m₁² < 1 (supremum 0.9988).
* **Normal ordering.** A normal spectrum has m₁m₃/m₂² ≤ 2.952.
* **Consequence.** A geometric neutrino texture at any CM point (R ≥ 1) is **normal ordered**.
* **Square torus.** The square torus (R = 4) is excluded by the oscillation data alone.

**3. CM spectra.**

| home | ordering | masses (meV) | Σ (eV) | m_ββ (meV) | m_β (meV) |
|---|---|---|---|---|---|
| τ = 1+i (R = 1) | NO | 1.53, 8.75, 50.13 | 0.0604 | 0.49–4.76 | 8.94 |
| τ = ω (R = 2^{2/3}) | NO, hierarchical | 2.55, 8.98, 50.17 | 0.0617 | 0–5.53 | 9.17 |
| τ = ω | NO, quasi-degenerate | 37.4, 38.4, 62.5 | 0.138 (disfavoured) | 12.5–38.3 | 38.4 |
| τ = i (R = 4) | none | — | — | — | — |

**4. The shared-home relation.**
* **Assumption.** The up coupling and the Weinberg operator are theta nulls of the same swap-symmetric home.
* **Relation.** They then share |𝔣(τ)|¹⁶/4, so

  **m₁ m₃ / m₂² = m_u m_t / m_c²** = 0.54 at M_Z (0.45–0.65 from the m_u error and the running).
* **What it fixes.** The neutrino spectrum, with no free parameter:
  * **Ordering:** normal. The inverted branch has Σ = 0.135–0.171 eV, excluded in ΛCDM.
  * **Spectrum:** m₁ = 0.80 meV (0.67–0.97), m₂ = 8.65 meV, m₃ = 50.1 meV.
  * **Σ:** 0.0596 eV (0.0594–0.0598).
  * **m_ββ:** 0.95–4.25 meV (Majorana phases free).
  * **m_β:** 8.8 meV.
* **The home itself is non-CM.** |𝔣(τ)|⁸ = 1.47, at τ = 1 + 0.874i, checked by the full theta Yukawa (relative error
  < 10⁻⁵). This is consistent with Pass 11938: the up data exclude CM factors.

**5. The two readings, side by side.**

| | Pass 11933 (Eisenstein, theta-zero) | Pass 11939 (shared home, geometric) |
|---|---|---|
| ordering | inverted | normal |
| m_lightest | 1.3 meV (0.8–3.8) | 0.80 meV (0.67–0.97) |
| Σm_ν | 0.1006 eV | 0.0596 eV |
| m_ββ | 15–50 meV | 1–4 meV |
| status (2026) | disfavoured by DESI in ΛCDM; JUNO pending | inside every current bound |

**How they will be told apart.** The mass ordering (JUNO + long-baseline), Σ from cosmology (CMB-S4 / Euclid
sensitivity ~0.02 eV separates 0.06 from 0.10), and m_ββ (next-generation searches reaching ~10 meV probe the IO
band).

## Scope and assumptions

**Exact or numerical results.**
* The symmetric-channel law.
* The CM values.
* The ordering lemma (given the oscillation inputs).

**Assumed, not derived.**
* The symmetric channels are theta nulls of **one** swap-symmetric home near the reducible locus.
* Leading order in Ω₁₂.
* The light-neutrino mass matrix is the Weinberg coefficient itself (no seesaw distortion).
* The neutrino ratio is compared with M_Z-scale quark ratios. Their running to high scales moves R_up within
  0.45–0.65; m₁ moves within 0.67–0.97 meV.

**The relation is a conditional prediction (tier C), not a derivation of the neutrino sector.**
* **Sector rule.** It replaces neither Pass 11933 nor Pass 11934. Pass 11934 showed that one radiative rule does not
  fit all sectors. Here the rule is "the symmetric channels share a home". The charged-lepton and down couplings
  (10·5̄) are not symmetric, so they are not constrained.
* **Unconstrained quantities.** PMNS angles and Majorana phases are not addressed.

**Rediscovery check.**
* Searched the corpus for "m1 m3", "m_u m_t", "DESI" and "0.0596". No prior statement of the relation exists.
* DESI itself was met before: the older physics track resolved a DESI tension of its geometric-cascade neutrino texture
  with a type-I seesaw (commit 39af532c8, `w33_neutrino_seesaw_texture.py`; Continuity decision f2652072). That is a
  different mechanism. It is cited here because it is the corpus's earlier contact with the same bound.
* The old physics track's Σm_ν ≈ 0.101 eV (CCXLIX, μ_eff² = 1/4) coincides numerically with the Pass 11933 IO sum.
  It is noted, not used.
