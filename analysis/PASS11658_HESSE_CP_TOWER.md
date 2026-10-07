# Pass 11658 — the Hesse CP sign at two qutrits, and why the reflection tower stops at two

Producer: `analysis/w33_pass11658_hesse_cp_tower.py` (stages `tower`, `n1`, `n2 K`, `molien`)
Certificate: `data/w33_pass11658_hesse_cp_tower.json`
Regression: `tests/test_w33_pass11655_11662.py`

## The two-qutrit Hesse CP sign

**Setup.**
* B is real, so time reversal acts on the Hesse space as u ↦ ū, composed with the Clifford action.
* A **CP-odd Hesse invariant** is a G-invariant polynomial of bidegree (k, k) in (u, ū) that changes sign under u ↦ ū. In
  the qutrit state it has degree 3k.
* The dimensions are Reynolds ranks over the reflection group. They are certified against the **exact Molien total**
  (1/|G|) Σ_g |h_k(eig g)|²: even + odd must equal it.

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| n = 1 (G₆): even / odd | 1/0 | 1/0 | 2/0 | 3/0 | 3/0 | 4/**1** | 5/1 | 6/1 |
| n = 1 Molien total | 1 | 1 | 2 | 3 | 3 | 5 | 6 | 7 |
| n = 2 (G₃₃): even / odd | 1/0 | 1/0 | 2/0 | 4/0 | 6/0 | 10/**2** | 16/5 | 27/10 |
| n = 2 Molien total | 1 | 1 | 2 | 4 | 6 | 12 | 21 | 37 |

**What the table shows.**
* **n = 1 (calibration).** The first CP-odd invariant is at k = 6. It is Codex's W, i.e. −108³ times the MUB Vandermonde
  (Pass 11641), at ψ-degree 18. The even ring is R[ρ, p₃, p₄].
* **n = 2.** The first CP-odd Hesse invariants are also at **k = 6**: two of them, at ψ-degree 18.
* **What the Hesse sector misses.** The lowest two-qutrit time-odd invariant has degree 6 (Pass 11492), so it is
  **invisible to the Hesse CP sector**. This is the same pattern as Passes 11648–11649 at one qutrit: the Hesse/CP order
  parameter only sees arrows of degree ≥ 18.
* **Range of certification.** At k = 9 and 10 the Reynolds counts (even + odd = 59, 82) fall short of the Molien totals
  (63, 107), because there were too few test functions. Those rows are lower bounds only and are not used.

## The tower stops at two qutrits

* **The count.** A tensor factorisation's local parity σ_P acts on the even Weil representation of W₁ ⊗ W_{n−1}. It is
  −1 exactly on odd₁ ⊗ odd_{n−1}, of dimension (3^{n−1} − 1)/2.
* **Checked.** The −1 multiplicity is 1 at n = 2 (a reflection: G₃₃) and 4 at n = 3, where the parity of qutrit 3 and
  SWAP(1,2) both have a 4-dimensional −1 eigenspace on the 14-dimensional Hesse space.

> **Two qutrits are the unique size at which tensor factorisations act as reflections of the Hesse space.**

This is why the Burkhardt group G₃₃ appears exactly at two qutrits. Beyond that the factorisations stop being mirrors.
It also fits the fact that no primitive complex reflection group exists in dimension (3ⁿ + 1)/2 for n ≥ 3.
