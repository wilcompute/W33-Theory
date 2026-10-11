# Pass 11910: down quarks, leptons and the CKM — the minimal magnetized home fails two cross-sector tests

Producer: `analysis/w33_pass11910_cross_sector_invariant_and_ckm.py`
Certificate: `data/w33_pass11910_cross_sector_invariant_and_ckm.json`
Regression: `tests/test_w33_pass11910.py`
Track: Claude.

## Minimal home

Every Yukawa sector has fluxes (3, 3, 6) on the **shared** family torus τ, its own relative Wilson line, and a localised
Higgs:
* up: Q u^c H_u;
* down: Q d^c H_d;
* leptons: L e^c H_d.

## 1. A universal invariant (prediction)

I_s = m₁m₂/m₃² = e^{−(4π/3) Im τ} for every sector, independently of that sector's Wilson line. The exact texture gives
1.8628, 1.8644 and 1.8630 (×10⁻⁵) for three generic Wilson lines, against the predicted 1.8628·10⁻⁵. Near the level
crossing ν → 1/3 the Gaussian form does not apply.

## 2. Data (running masses at M_Z; Xing–Zhang–Zhou, arXiv:0712.1419)

| sector | I_s | implied Im τ |
|---|---|---|
| up | 2.67·10⁻⁸ | 4.16 |
| down | 1.91·10⁻⁵ | 2.59 |
| leptons | 1.64·10⁻⁵ | 2.63 |

**Down and leptons agree.** Their invariants match to 17 % and their Im τ to 1.4 %. This is the product form of the
Georgi–Jarlskog pattern, which implies it.

**The up sector does not.** Mass ratios within a sector are nearly scale-independent, so running cannot close a factor
of about 700 (an Im τ ratio of 1.6). **The minimal home with one family torus for all sectors is falsified by the up/down
comparison.** The up Yukawas need a larger effective area than the down and lepton ones.

## 3. The CKM

With a localised Higgs, each Yukawa matrix has one nonzero entry per row, from the selection rule i + j ≡ k (mod 3). So
YY† is diagonal in the family basis, and |V_CKM| is a permutation matrix: **V_us = 0**. TOE46 front 4 found the same for
equal backgrounds. The data need |V_us| = 0.225.

## 4. The minimal fix and its cost

A second Higgs component in another selection class, with admixture ε, mixes the light down states linearly:

| ε | mixing |
|---|---|
| 10⁻³ | 0.074 |
| 2·10⁻³ | 0.148 |
| 4·10⁻³ | 0.286 |

A Cabibbo-sized angle therefore needs only ε ≈ 3·10⁻³. But it needs a **non-localised Higgs**, which deforms item 1. The
localised-Higgs dynamics of Passes 11907 and 11909 does not supply one (TOE48: the Higgs-mode phases are flat).

## Reading

What the minimal magnetized home does:
* it carries the up hierarchy, at a cost: an O(1) coefficient (11907) and a top-sector cancellation (11909);
* it gets the down/lepton relation right.

What it gets wrong:
* the up versus down areas;
* the CKM.

Both failures point to the same missing ingredient: **sector-dependent geometry and a non-localised Higgs**, for
instance different fluxes or tori for the up Yukawas, and a Higgs spread over selection classes.

## Prior art

* Georgi–Jarlskog (1979).
* Xing–Zhang–Zhou (2008).
* TOE46, TOE48.
* Corpus: 11904–11909.
