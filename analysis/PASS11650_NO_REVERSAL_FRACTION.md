# Pass 11650 — ticks with no reversal at all: decided by Gaussian elimination, 1/40 → 1/28 → ≈ 0.037

Producer: `analysis/w33_pass11650_no_reversal_fraction.py` (stages `n2`, `n3`, `s4 N`, `s5 N`)
Certificate: `data/w33_pass11650_no_reversal_fraction.json`
Regression: `tests/test_w33_pass11647_11654.py`

## The question

* **(S) and its affine relaxation.** (S) of Pass 11350 asks for a symplectic Q with M s^{−k} Q (JMJ) = Q and Qz₁ = z₁.
  Without the symplectic condition this is an affine system: an intertwiner from (V, JMJ) to (V, s^k M⁻¹) that fixes z₁.
* **Why it matters.** When (S) has no solution for any k, the tick reverses no frame at all (Pass 11537's necessity). It
  is the "maximally irreversible" class.

## Results

**1. Linear algebra decides.** Exhaustively, (S) has a symplectic solution for some k iff the affine system is
solvable for some k.

| | affine solvable and symplectic solvable | neither | mismatches |
|---|---|---|---|
| n = 2 (every class within the cap) | 50 538 | 1 296 | **0** |
| n = 3 (every orbit within the cap) | 2 071 | 46 | **0** |

**2. Exact fractions of Sp(2n, 3).**

| n | no reversal | by cell |
|---|---|---|
| 2 | **1/40** | all in "same line, other" (half of that cell) |
| 3 | **1/28** | 3/182 non-collinear + 1/52 "same line, other" |

**3. Sampled with the affine test.**

| n | samples | fraction |
|---|---|---|
| 2 (control) | 30 000 | 0.0260 ± 0.0009 (exact 0.025) |
| 4 | 60 000 | 0.0373 ± 0.0008 |
| 5 | 30 000 | 0.0376 ± 0.0011 |

The fraction rises from 0.025 to 0.0357 and then **settles near 0.037**. No closed formula is claimed.

## Unit convention correction

* **The correct order.** |Sp(6,3)| = 9 170 703 360.
* **The error.** Passes 11537 and 11644 wrote fractions with denominator 28 304 640 = |Sp(6,3)|/324, and the 11644 note
  called that number the order of Sp(6,3).
* **What is affected.** The fractions themselves are correct, since they are ratios of masses with the factor 324
  cancelling. Only that wording was wrong. It is corrected in the 11644 note, and this producer sums the actual orbit
  sizes.

## Reading

**What "no reversal" means.**
* The one-gate tick has no Clifford-antiunitary time reversal for any frame exactly when M⁻¹ (twisted by the shear) is
  not reachable from JMJ by any linear intertwiner fixing the magic axis.
* That is a cyclic-module condition on the pair (M, z₁), checkable in polynomial time at every n.
* The fraction of such classes is small and appears to converge, around 3.7%.
