# Pass 11644 — the "if" half of the union law: a per-solution theorem, k = 0 off the isotropic locus, and a 3-adic splitting criterion

Producer: `analysis/w33_pass11644_union_law_splitting.py` (stages `n2`, `n3`)
Certificate: `data/w33_pass11644_union_law_splitting.json`
Regression: `tests/test_w33_pass11641_11646.py`

**Setting.** This follows Passes 11350 and 11537.
* The tick is U = W(a)V_M T₁.
* A solution (Q, k) of (S) gives the anti-symplectic map A = QJ, with AMA⁻¹ = s^k M⁻¹ and Az₁ = −z₁.
* K = ker(M − I), K₀ = K ∩ z₁^⊥, and N_Q = (I − A⁻¹)K₀.
* Pass 11537 proved that reversible frames ⊆ ∪_Q N_Q^⊥ (necessity) and observed equality.

## Three theorems (every n)

**Theorem 1 (the frames of one solution).** r_Q = 0, and

  frames(Q, k) = N_Q^⊥ ∩ { a : ω(v_Q, a) = c_Q },  v_Q = (I − A⁻¹)x_Q.

There are two cases.

| case | condition | choose | x_Q |
|---|---|---|---|
| 1 | z₁ ∉ Im(M − I) | w₁ ∈ K with c₁ = ω(w₁, z₁) ≠ 0 | w₁ − kc₁z₁ |
| 2 | z₁ ∈ Im(M − I) | w₀ with (I − M)w₀ = z₁, and c₀ = ω(w₀, z₁) | w₀ + (1 − kc₀)z₁ |

*Proof.*
* (F) is solvable iff its right-hand side pairs to zero with K′ = {w : (I − M)w ∈ span z₁}.
* Since K^⊥ = Im(M − I), K′ is K₀ + span(w₁) in case 1 and K₀ + span(w₀) in case 2.
* The K₀ part gives N_Q^⊥ (Pass 11537).
* The extra vector gives one affine condition, using three facts: s^k w = w + kω(w, z₁)z₁, A⁻¹z₁ = −z₁, and
  Mw₀ = w₀ − z₁.
* **Checked against the decider on all 132 192 (Q, k) pairs at n = 2.**

**Theorem 2 (k = 0 off the isotropic locus).** If the M-cyclic span of z₁ is not totally isotropic, every solution has
k = 0.

*Proof.*
* A conjugates M to s^k M⁻¹ = (I + k z₁e_{x₁}ᵀ)M⁻¹, which must therefore have the characteristic polynomial of M⁻¹.
* By the matrix determinant lemma, the two characteristic polynomials differ by k·Σ_{j≥1} ω(M⁻ʲz₁, z₁) t⁻ʲ, times the
  characteristic polynomial.
* So k ≠ 0 forces ω(M^j z₁, z₁) = 0 for all j. ∎

**Theorem 3 (splitting).** Take k = 0.
* **Setup.** Then c_Q = 0. A preserves K₀ and K̃ = K₀ + span(x_Q), and acts trivially on K̃/K₀.
* **The criterion.** frames(Q, 0) = N_Q^⊥ ⇔ (A − I)x_Q ∈ (A − I)K₀ ⇔ A fixes a vector of K̃ outside K₀.
* **When it holds.** It **holds whenever 3 ∤ ord(A|K̃)**, in particular for every involutive reverser.
  *Proof.* Σ_{j<m} A^j x_Q is fixed and is congruent to m·x_Q modulo K₀.

**Corollary (union law, class by class).**
* If every solution of (S) for M has k = 0 and 3 ∤ ord(A_Q|K̃), then the reversible frames are exactly
  ∪_Q N_Q^⊥. Pass 11537's law is then **proved** for that class by linear algebra on its solutions, with no frame
  enumeration.
* Solutions with k ≠ 0, case 2 and c₀ = 0 have v_Q ∈ N_Q and c_Q = k ≠ 0, so they reverse no frame at all.

## Certificates

**n = 2 (all 51 840 classes; 6 have solution spaces beyond 3⁸).**

| | count |
|---|---|
| Theorem 1 formula = decider, per (Q, k) | **132 192 / 132 192** |
| k ≠ 0 solutions: isotropic cyclic span (Theorem 2) / reversing no frame | 7 776 / 7 776 of 7 776 |
| k = 0 solutions with 3 ∤ order: exact (Theorem 3) | 123 120 / 123 120 |
| k = 0 solutions with 3 \| order: **not** exact | 1 296 / 1 296 (so at n = 2 the criterion is an iff) |
| involutive reversers among k = 0 | 115 992 / 124 416 |

| cell | union law **proved** | no solution | criterion silent |
|---|---|---|---|
| non-collinear | **34 992 (all)** | 0 | 0 |
| collinear, different lines | **11 664 (all)** | 0 | 0 |
| same line (three cells) | **2 592 (all with a solution)** | 1 296 | 0 |
| Mz₁ = z₁ | 405 | 0 | 240 |
| Mz₁ = −z₁ | 477 | 0 | 168 |

* **Every class outside the two eigenvector cells is proved.**
  * For the 1 296 classes with no solution, the law holds trivially by necessity: there is no reversible frame.
  * The remaining classes are proved by the criterion.
* The 408 silent classes lie in the eigenvector cells. There some solutions do not split, and the union of other
  solutions covers their frames. That is verified frame by frame in Pass 11537, not proved here.

**n = 3 (Pass 11373's orbits, exact weights; |Sp(6,3)| = 9 170 703 360; the counts below are in units of 324, so the total is 28 304 640 units).** *(Unit convention corrected in Pass 11650; the fractions are unchanged.)*

| | mass |
|---|---|
| union law **proved** by the criterion | **96.098%** (27 200 133) |
| no solution of (S) (law holds by necessity) | 3.571% (1 010 880) |
| criterion silent | 0.301% (85 120) |
| solution space beyond 3⁹ | 0.030% (8 507) |

* **An exact observation.** The classes with no solution of (S) are exactly **1/40** of Sp(4,3) (1 296/51 840) and
  exactly **1/28** of Sp(6,3) (1 010 880/28 304 640). No explanation is claimed.
* **Theorem 2** holds on all 12 708 k ≠ 0 solutions.
* **Splitting.** 75 360 of the 83 406 k = 0 solutions split by averaging.
* **Silent orbits.** Unlike n = 2, 50 non-collinear orbits are silent: some reversers there have order divisible by 3.
  Pass 11537 verified the law on them frame by frame.
* **What was not recomputed at n = 3.** The n = 3 stage did not compute frames or r_Q. It relies on Theorem 1, which was
  checked at n = 2, and on Pass 11537's r_Q = 0.

## Reading

**Where the gap went.** The open half of the union law has become one concrete structure.
* **Generically**, the k-dependent extra condition of Pass 11537 disappears because k = 0 (Theorem 2).
* **What remains** is whether the reverser A_Q splits the extension of the trivial line by K₀ inside K̃. That holds
  automatically when A_Q has order prime to 3.

**Status by size.**
* **n = 2:** the "if" half is a theorem plus a finite certificate on every non-eigenvector class.
* **n = 3:** the same holds on 99.67% of Sp(6,3) by mass.

**Open.**
* A proof that non-splitting reversers are always covered by splitting ones, which would close the eigenvector cells and
  the silent n = 3 orbits.
* Whether 3 | ord(A|K̃) ⇒ not exact in general. It holds at n = 2.
