# Pass 11941: the CKM needs parity breaking — and the down coupling alone can supply it

Producer: `analysis/w33_pass11941_ckm_needs_parity_breaking.py`
Certificate: `data/w33_pass11941_ckm_needs_parity_breaking.json`
Regression: `tests/test_w33_pass11941.py`
Track: Claude. Builds on Pass 11938 (Weber law) and Passes 11939/11940 (neutrinos). Complements Pass 11910
(V_us = 0 from the localised-Higgs selection rule) and Pass 11905 (the one-qutrit reflection c → −c).

## 1. Parity theorem (exact, every Ω)

**Invariance.** The zero-characteristic level-3 theta null is invariant under the central inversion c → −c of both
qutrits: Θ[(−a,−b)](0,Ω) = Θ[(a,b)](0,Ω).

**Block structure.** Reshaped as a 3×3 Yukawa, this says Y = P Y P, with P: c → −c. So Y is block-diagonal: a P-even
block of dimension 2 and a P-odd block of dimension 1.

**Consequence for mixing.** Two such Yukawas share the P-odd generation, so |V| has an **isolated generation**: a row and
column with a single unit entry. Checked:
* the parity holds to 10⁻¹⁵ at 6 random Ω;
* the isolated generation holds exactly.

**Near-product homes.** There the P-odd state is the *middle* generation, f₁ = (0,x,−x) (Pass 11938). Hence **V_us = V_cb = 0
exactly**, and only V_ub = O(ε²) survives (measured: 3·10⁻¹⁴, 3·10⁻¹⁷ and 3·10⁻⁵).

**Conclusion.** CKM mixing *requires* Wilson lines with a P-odd part.

**Relation to earlier passes.** Pass 11910 got V_us = 0 from a selection rule (localised Higgs). This is a different
mechanism, from the central element of the level-3 group, and it holds for any Higgs profile encoded in Ω. It extends
the mass statement of Pass 11905 to mixing.

## 2. Existence with the up coupling parity-clean

**Setting.**
* The up coupling stays Wilson-line-free. The Weber law of 11938 and the neutrino relation of 11939/11940 are therefore
  untouched: the fitted τ has |𝔣(τ)|⁸ = 1.4676 = 2√R_u.
* Wilson lines go **only** into the down coupling.
* Both homes are near-product: |ε| ≤ 0.03.

**Result.** All eight quark observables fit exactly (max log residual 10⁻⁹):

| m_c/m_t | m_u/m_c | m_s/m_b | m_d/m_s | V_us | V_cb | V_ub | J |
|---|---|---|---|---|---|---|---|
| 3.685e-3 | 1.984e-3 | 1.853e-2 | 5.038e-2 | 0.2250 | 0.0411 | 0.00382 | 3.08e-5 |

**Counting.** There are 12 real parameters for 8 observables. **This is existence, not prediction.** J in particular is
fittable (an exact fit includes it), so no CP prediction is claimed. An earlier hint of δ ≈ 50° from fits without J
was a basin effect.

## 3. The regime (search record)

The record is frozen from 26 multi-start fits; it is not re-run by the producer.

**Where the down factor sits.** Every good fit puts the 5̄ (down) factor in its cusp regime:
* Im(−1/τ_d) = 3.69–3.75 across the 6 exact fits;
* 3.47–3.81 across all good fits, for ε caps of 0.01 and 0.03, varied cutoffs and Wilson configurations.

**Mechanism.** There the level-3 Gaussian factor e^{−π·Im/3} ≈ 0.02 ≈ m_s/m_b. The up hierarchy is **entangling**
(Ω₁₂, Pass 11938); the down hierarchy is **Gaussian** (cusp, the mechanism of Passes 11904/11912).

**Preferred, not forced.** Forcing Im τ_d ≥ 0.15 gives best cost 3.6·10⁻³ (V_us = 0.21).

**Effect of the Wilson lines.** Without them, the fitted down coupling would give R_d = 19.5 and m_s/m_b = 0.0096. The
Wilson lines move these to the data (2.72 and 0.0185): the down Weber law is strongly modified by Wilson lines, while
the up one is exact.

## Reading

**What fits.** The theta-null family can host the full quark sector, including CP, with the up sector parity-clean
(keeping the Weber and neutrino results) and the parity breaking confined to the down coupling.

**What is not predicted.** Nothing here predicts a CKM element. The structural content is:
* the parity theorem;
* the division of labour: entangling up hierarchy, Gaussian down hierarchy near a cusp, with Wilson lines only in the
  5̄ sector.

**Open.** A mechanism that puts P-odd Wilson lines in the 5̄ but not in the 10·10 coupling. A candidate is hypercharge
flux, which distinguishes d^c and L from Q, u^c and e^c, but this is not computed here.
