# Pass 12049: the coloured threshold inventory for the strong-CP divisor

* **Producer:** `analysis/w33_pass12049_coloured_divisor_inventory.py` (6/6 checks)
* **Certificate:** `data/w33_pass12049_coloured_divisor_inventory.json`
* **Regression:** `tests/test_w33_pass12049.py`
* **Track:** Claude. Reservation `4e6501a1d`.

## The target (Codex 11950)

Near the separating divisor ε = Ω₁₂ = 0, det Y_u = C ε³ + O(ε⁵) (TOE38/39). So θ̄ = arg[e^(−8π²f₃) det Y_u det Y_d]
winds unless e^(−8π²f₃) ∝ ε⁻³, that is, 8π²f₃ = (3/2) log χ₁₀ + regular. 11950 called the 3/2 "a falsifiable target
for an actual colored threshold inventory". This pass supplies the inventory.

* **Winding check.** At the fitted up home, the winding of det Y_u around a small ε circle is exactly 3.
* **χ₁₀ near the divisor.** χ₁₀ ∝ π² ε² ΔΔ (Pass 12048).

## Inventory (exact group theory)

**How states enter f₃.** Integrating out states of holomorphic mass m with SU(3) β coefficient b gives
e^(−8π²f₃) ∝ ∏ m^b. Suppose a continuous Wilson line V along a generator H restores a group G at V = 0. Then:
* **Broken vector multiplets:** masses ∝ q_H V, contributing **b_vec = −3T + T = −2T**, where T is the SU(3) index
  of the broken generators (the same for N = 2).
* **Vectorlike coloured pairs:** each 3 + 3̄ with mass ∝ V contributes **+1**.

**Selection rule.** Regularity against a total winding W (3 per determinant that winds in V) requires

  **b_vec + n = −W, i.e. n = −W − b_vec.**

**Method.** Each T is computed from explicit real Lie-algebra matrices: the broken subspace is the image of ad_H, and
T = −tr ad_X² on it. Control: T(3 + 3̄) = 1.

| restoring pattern | broken real dim | T | b_vec | n (W = 3) | n (W = 6) |
|---|---|---|---|---|---|
| **SU(5) → SU(3)×SU(2)×U(1)_Y** | 12 | 2 | −4 | **1** | impossible |
| SO(10) → SU(5)×U(1)_X | 20 | 3 | −6 | 3 | 0 |
| SO(10) → U(3)×SO(4) | 30 | 5 | −10 | 7 | 4 |

Two further patterns use standard branchings and are not computed here: E6 → SO(10)×U(1) has T = 4; E6 → SU(3)³ has
T = 9.

**Minimal solution.** A hypercharge-direction Wilson line restoring SU(5), plus exactly **one** vectorlike 5 + 5̄
light with it, gives −4 + 1 = −3. That is precisely the coefficient 3/2 on log χ₁₀.

## Coherence with earlier passes (suggestive, not proof)

* **One pair.** n = 1 is the single vectorlike row that 12004/12005 found necessary and sufficient for CP-real theta
  quarks.
* **The lepton Clebsch.** If that pair's mass comes from the same hypercharge Wilson line, then
  μ_L/μ_D = |Y(L_H)|/|Y(D)| = 3/2. So b_e = (2/3) b, the adjoint-mass Clebsch, the only rule that fitted both lepton
  ratios in 12047.
* **The row size.** With μ ∝ εM, the large Barr row |b| = |B|/μ ~ 1/ε_u ≈ 181 for B ~ M. The 12045 branches have
  |b| = 117–284.

So one assumption — that the divisor Ω₁₂ = 0 is where a hypercharge Wilson line restores SU(5) — links four
previously separate facts:
* the up hierarchy parameter;
* the strong-CP regularity coefficient;
* the single Nelson–Barr row;
* the lepton Clebsch.

## Tensions

1. **Interpretation.** In the magnetized reading of 11942, Ω₁₂ is a complex-structure modulus and the hypercharge
   Wilson line is z. The identification here needs a heterotic (T, U, V)-type reading, where Wilson-line moduli are
   period-matrix entries. That construction is not done here.
2. **The down divisor.** det Y_d also winds 3 in its own ε_d. With one SU(5) line, ε_d must not wind in V. If up and
   down shared V (W = 6), SU(5) is impossible, and SO(10) → SU(5)×U(1)_X with n = 0 is the solution.
3. **Light X and Y bosons.** M_X ~ ε_u M_c forces a very high compactification scale for a standard M_X, or else fast
   proton decay. This is not computed here.

## What is not new

* Thresholds of massive vector and vectorlike multiplets (textbook).
* Wilson-line GUT breaking (Hosotani; Witten 1985; Ibáñez–Nilles–Quevedo 1987).
* Igusa forms in heterotic thresholds (Kawai hep-th/9512046; Mayr–Stieberger).
* Modular strong CP (Feruglio–Marrone–Strumia–Titov, arXiv:2505.20395; arXiv:2608.13796). At abstract level, neither
  uses GUT-restoring thresholds.
* The divisor target (Codex 11950).

## What is new

* The inventory and the selection rule n = −W − b_vec.
* The coherence with 12004/12005/12047.
