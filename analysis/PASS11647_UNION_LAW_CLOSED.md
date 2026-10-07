# Pass 11647 — the union law is a theorem: one-gate reversibility is the union over semisimple reversers

Producer: `analysis/w33_pass11647_union_law_closed.py` (stages `2`, `3`)
Certificate: `data/w33_pass11647_union_law_closed.json`
Regression: `tests/test_w33_pass11647_11654.py`

**Setting.** This follows Passes 11537 and 11644.
* The tick is U = W(a)V_M T₁.
* A solution (Q, k) of (S) gives the anti-symplectic A = QJ, with AMA⁻¹ = s^k M⁻¹ and Az₁ = −z₁.
* K₀ = ker(M − I) ∩ z₁^⊥, and N_A = (I − A⁻¹)K₀.
* Pass 11644 showed that A preserves K₀, and that a k = 0 solution of order prime to 3 reverses exactly N_A^⊥.

## Two lemmas (every n)

**Lemma A (semisimple part).** Let A be a k = 0 solution of order 3^a·m, with 3 ∤ m.
* **The power.** Its semisimple part is A_s = A^N for an odd N with N ≡ 0 (mod 3^a) and N ≡ 1 (mod m).
* **It is a solution.** Since N is odd, A_s M A_s⁻¹ = M⁻¹ and A_s z₁ = −z₁. So A_s is again a k = 0 solution, and
  Q_s = A_sJ is symplectic and fixes z₁.
* **It splits.** Its order is prime to 3, so frames(A_s) = N_{A_s}^⊥ (Pass 11644, Theorem 3).
* **It dominates.** I − A^{−N} = (I − A⁻¹)(I + A⁻¹ + … + A^{−(N−1)}), and K₀ is A-invariant, so N_{A_s} ⊆ N_A.
* **Hence N_A^⊥ ⊆ frames(A_s): every k = 0 solution is covered.** ∎

**Lemma B (k ≠ 0 in the eigenvector cells).**
* **For every solution, AsA⁻¹ = s⁻¹.** A is anti-symplectic with Az₁ = −z₁, and s is the transvection with centre z₁.
* **In the eigenvector cells, s commutes with M.** If Mz₁ = ±z₁, then M s M⁻¹ = t_{Mz₁} = s.
* **A³ has k = 0.** Conjugating three times gives A³MA⁻³ = s^{3k}M⁻¹ = M⁻¹. So A³ is a k = 0 solution with
  N_{A³} ⊆ N_A, and Lemma A applies to it. ∎

**Theorem (the union law).** Consider any n and any class M whose k ≠ 0 solutions either lie in the eigenvector cells or
are dominated by a split k = 0 solution. For it,

> **reversible frames = ∪ over the semisimple reversers A (AMA⁻¹ = M⁻¹, Az₁ = −z₁, order prime to 3) of ((I − A⁻¹)K₀)^⊥.**

* "Only if" is Pass 11537.
* "If" follows from Lemmas A and B together with Pass 11644's Theorems 1 and 3.
* By Pass 11644's Theorem 2, a k ≠ 0 solution needs an isotropic M-cyclic span of z₁. Outside the eigenvector cells that
  happens only in some "same line" cells, which the certificate checks class by class.

## Certificate

| | n = 2 (every class) | n = 3 (Pass 11373 orbits) |
|---|---|---|
| k = 0 split solutions (Pass 11644) | 123 120 | 75 360 |
| k = 0 non-split: Lemma A holds (A^N a split solution, dominating) | **1 296 / 1 296** | **8 046 / 8 046** |
| k ≠ 0 in eigenvector cells: Lemma B holds | **7 776 / 7 776** | **12 600 / 12 600** |
| k ≠ 0 elsewhere: dominated by an explicit split solution | — | **108 / 108** (6 orbits, same-line cells) |
| **union law proved (theorem + certificate)** | **8639/8640 of Sp(4,3)** | **99.970% of Sp(6,3)** |
| solution spaces beyond the cap | 1/8640 (6 classes) | 0.030% |

## Reading

* **What is now proved.** Pass 11537 observed the union law, and Pass 11644 proved its "if" half off the eigenvector
  cells. It is now proved for every class within reach at n = 2 and n = 3. Only 108 same-line k ≠ 0 solutions need a
  computed dominator, and the lemmas cover everything else for every n.
* **The structural statement.** A one-gate tick reverses frame a iff a is ω-orthogonal to (I − A⁻¹)K₀ for some
  *semisimple* anti-symplectic reverser of M that negates the magic axis.
  * The Jordan-unipotent parts of reversers, the 3-adic part, never help. They only shrink the reversible set.
  * The shear exponent k never helps either: k ≠ 0 solutions reverse no frame of their own (Pass 11644), and their
    N-spaces are dominated.
* **Open.**
  * A uniform proof for k ≠ 0 solutions in the non-eigenvector "same line" cells. At n = 3 there are 108 of them in 6
    orbits; A³ does not work there because s and M do not commute.
  * The classes beyond the enumeration caps.
