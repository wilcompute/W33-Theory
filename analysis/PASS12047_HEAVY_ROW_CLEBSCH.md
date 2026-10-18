# Pass 12047: the heavy-row Clebsch

* **Producer:** `analysis/w33_pass12047_heavy_row_clebsch.py` (4/4 checks)
* **Certificate:** `data/w33_pass12047_heavy_row_clebsch.json`
* **Regression:** `tests/test_w33_pass12047.py`
* **Driver:** `analysis/search_drivers_12047/kappa.py`
* **Track:** Claude. Reservation `7d3aa5ae3`.

## Idea

Passes 12045 and 12046 assumed that the heavy vectorlike 5 + 5̄ couples to leptons exactly as to the d^c quarks. That
holds only if both its mass and the CP-breaking row coupling are SU(5) singlets. Suppose instead that the heavy mass
comes from the adjoint VEV, the textbook doublet–triplet mechanism. Then

  μ_L/μ_D = Y(L_H)/Y(D) = −3/2,

and the lepton row is b_e = κ·b with |κ| = 2/3.

**Mechanism (exact).** det A_e/det A = √((1+|b|²)/(1+κ²|b|²)), which tends to 1/|κ| for |b| ≫ 1. So κ rescales m_e
and leaves m_μ/m_τ unchanged. It also breaks the row-independence of det M_e/det M_d from 12045, by exactly this
factor.

## Scan

* **Candidates (from group theory).**
  * singlet: 1;
  * adjoint in the mass: 2/3;
  * adjoint in the row: 3/2;
  * B−L in the row: 3;
  * B−L in the mass: 1/3;
  * controls: 2 and ½.
* **Grid.** All 12045 branches (A, B, C, D, G) × 7 κ × the 8 matching scales of the 12046 SM-running records, giving
  280 entries.

**Exactly one entry** is within 15% on both ratios. It is branch C at M_Z with κ = 2/3:
* m_μ/m_τ = 0.0574 (−2.5%);
* m_e/m_μ = 0.00494 (+4.2%);
* m_e m_μ/m_τ² off by 0.8%.

The next best entry is off by 38%.

## Why this is not evidence

1. **κ is one discrete knob on one number.** The physical κ values are spaced 0.405 apart in ln κ. A random target
   lands within the ±0.13 window of one of them with probability **about 0.6**.
2. **m_μ/m_τ was already near the data on C at κ = 1.** That is why C was singled out, and 12045 showed that this
   single ratio is uninformative on C.
3. **The match needs a matching scale near M_Z.** At 10⁴ GeV, m_μ/m_τ is already 32% off.

## Reading

**Scope correction.** 12046's closure holds for the two singlet rules: the shared matching and a triplet-only heavy
state. With the adjoint-mass Clebsch, branch C is *consistent* at M_Z. This is not a prediction.

## What is not new

* Doublet–triplet splitting by the adjoint and its hypercharge Clebsch (textbook SU(5)).
* Georgi–Jarlskog Clebsches. Codex 11960 uses a different mechanism: light-Yukawa 45 Clebsches with fitted
  coefficients.
