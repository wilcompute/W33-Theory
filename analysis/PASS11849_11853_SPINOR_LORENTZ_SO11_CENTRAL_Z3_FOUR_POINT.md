# Passes 11849–11853 — Lorentz plus the central translation commutes with exactly the Standard-Model algebra; an independent two-qutrit (Weil) realisation of the parallel track's so(11) result for the spinorial Lorentz group; the hidden bulk 20 is seen at four points

**Files**
* Producers:
  * `analysis/w33_pass11849_11851_spinor_lorentz_central_z3_generations.py`
  * `analysis/w33_pass11852_bulk_four_point.py`
* Frozen:
  * `data/w33_pass11849_11851_spinor_lorentz_central_z3_generations.json`
  * `data/w33_pass11852_bulk_four_point.json`
* Lean: `formal/W33/Pass11853HyperchargeSpectrum.lean`
* Regression: `tests/test_w33_pass11849_11853.py`

**Setting (Passes 11843–11847).**
* E₈ ⊃ SU(6) × SU(3) × SU(2), with SU(6) the A₅ orthogonal to a Kramers root α of E₆.
* The faithful finite Lorentz group A₆ (adjacent Tits words) commutes with su(5)_GUT.
* The order-2 torus elements break su(5)_GUT to su(3) ⊕ su(2) along exactly the Georgi–Glashow hypercharge.
* The translations exist only as ℤ₃ · M: the A₅ lattice mod 3, with a central radical line.

## 11850 — the Standard-Model algebra from Lorentz and the central translation

**Relation to the parallel Round 33 §3b** (`782bfe0e1`). That corollary combines the faithful A₆, the **full** ℤ₃ · M
translation group and the order-7 hypercharge rotation, and gets su(3) ⊕ su(2): hypercharge is lost once all
translations are imposed. Round 33 §3 also reproduces the no-4-dim-submodule obstruction of 11844. The statement below
is complementary. It uses **only the central element** of the translations, and hypercharge survives.


* **The element.** The radical line of the A₅ lattice mod 3 is spanned by c = (0,0,0,0,0,0,1,2) in E₈ simple-root
  coordinates. Its torus element t_c (order 3) fixes every root vector of A₅, A₂ and A₁, i.e. it is central in
  SU(6) × SU(3) × SU(2), and it commutes with the A₆ lift.
* **The commutant** of ⟨A₆, t_c⟩ in E₈ is **dimension 12, derived algebra 11, centre 1, rank 4**, containing su(3)_A₂
  and su(2)_α. Its centre is the unique hypercharge direction of 11845, so the commutant is **exactly
  su(3) ⊕ su(2) ⊕ u(1)_Y**.
* **Intrinsic.** This replaces 11845's hand-chosen order-7 hypercharge rotation by something already in the geometry:
  **finite Lorentz × the centre of the finite Poincaré translations commutes with exactly the Standard-Model gauge
  algebra.** The non-central translations break further, to su(3) ⊕ su(2) (11844).
* **Erratum to 11845.** The order-7 rotation there was implemented as the real part cos(2π·6 ad Y/7). That has the same
  fixed space as the true rotation exp(2πi·6 ad Y/7), because both fix exactly ker ad Y when |6Y| ≤ 6. So the result
  stands; the construction here supersedes it.

## 11849 — the spinorial finite Lorentz group: E₈ ⊃ Spin(11) × Spin(5) (independent reproduction)

**Ownership.** The result c_E₈(SL(2,9)) = so(11), with E₈ = (55,1) + (1,10) + (11,5) + (32,4) and the vector-like
16 + 1̄6̄ content, **belongs to the parallel track**:
* Round 34 (`f46a1b576`, the Clifford spinorial SL(2,9) ⊂ Spin(6));
* Round 35 (`a24c8c186`, `analysis/2026-10-10_toe35_spinorial_so11_dimensionality_alpha_audit.md`).

Both were committed before this pass. What follows reproduces the result independently with a different realisation and
adds four things:
1. the Lorentz spinor is the **two-qutrit Weil half Di** of Pass 11834, placed inside the SU(5)_L that commutes with the
   Georgi–Glashow su(5) of Pass 11845;
2. a Casimir-ratio certification of so(11);
3. the exact split of the spinor sign over the blocks;
4. the identification of the vector 5 as *not* Rac.


* **Building su(5)_L.** su(5)_L is the commutant of su(5)_GUT (dim 24, rank 4). It is given an explicit sl₅ → E₈
  homomorphism (error 6·10⁻¹¹) from its own Chevalley basis.
* **Embedding SL(2,9).** The spinorial Lorentz group SL(2,9) = 2·A₆ acts through Di, the odd Weil half of Pass 11834,
  as diag(Di, 1) ∈ SU(5)_L.
  * Di is **quaternionic** on SL(2,9) (Frobenius–Schur indicator −1), so SL(2,9) ⊂ Sp(4) ≅ Spin(5).
  * The two chosen elements generate all 720 elements, and −1 acts nontrivially on E₈.
  * The generator lifts satisfy their orders to 10⁻⁸.
* **Commutant: so(11).** It is **dimension 55, rank 5, semisimple, containing su(5)_GUT**. Its Casimir splits E₈ into
  blocks of dimension 10, 55, 128, 55, with ratios to the adjoint of **5/9 and 55/72**. These are exactly so(11)'s
  vector (10/18) and spinor (13.75/18) values. So the commutant is **so(11)**, and

  **E₈ = (55, 1) + (11, 5) + (32, Di) + (1, 10)** under so(11) × finite Lorentz.

  This is E₈ ⊃ Spin(11) × Spin(5), with the finite Lorentz group inside Spin(5) = Sp(4). The complexified Sp(4) is the
  AdS₄ group of Passes 11831–11833.
* **The −1 of SL(2,9) is −1 on exactly the 128-dimensional block (32 ⊗ Di) and +1 on the other 120.** Only the Spin(11)
  spinor carries the Lorentz spinor.
* **The 5 is not Rac.** The 5 multiplying the so(11) vector is Λ²Di − 1, the Spin(5) vector. It is irreducible on
  SL(2,9) but **orthogonal to Rac** (overlap 0): A₆ has two inequivalent 5s, and this is the other one.

## 11851 — generations

Round 35 §2 (parallel track) already concluded that the spinorial sector is vector-like (16 + 1̄6̄, zero net chirality)
with no natural three-generation selection. This section agrees and adds the E₆ × A₂ statement.


* **The 27s are not generations here.** dim(e₆ ∩ su(5)_GUT) = 4, i.e. su(2)_α ⊕ u(1); A₂ ⊂ su(5)_GUT. So in this
  embedding the threefold index of E₈ ⊃ E₆ × SU(3), (27,3) + c.c., is **colour**, not family.
* **Spinorial matter is one family.** Under so(11) ⊃ so(10) ⊃ su(5), the 32 = 16 + 1̄6̄. The Lorentz spinor Di therefore
  carries **one SO(10) family 16 (10 + 5̄ + 1, including νᶜ) together with its conjugate**, which is vector-like on the
  quaternionic Di. The multiplicity space of Di in E₈ is exactly one 32.
* **Verdict:** the spinorial embedding gives **N_gen = 1**, and the bosonic A₆ embedding gives Lorentz multiplicities
  5 and 10 (11846). **No embedding examined here produces three generations.** Three would need the Lorentz spinor to
  sit in a group whose commutant carries a 3-dimensional family space. This is open; it is not claimed.

## 11852 — bulk dynamics and the boundary four-point function

* **Setup.**
  * Bulk fields: φ (the 15, crosscap propagator 12 Π₁₅) and χ (the hidden 20, propagator Π₂₀).
  * Vertices: φ⁴, φ³ and φ²χ (the S15·S15·b20 coupling of 11841).
  * Boundary operators: O_x = Σ_p N(x,p) φ_p.
* **The space of allowed boundary four-point functions.** The Sp(4,3)-invariant symmetric forms on the boundary 15 have
  dimensions **Sym² 1, Sym³ 1, Sym⁴ 3** (character sums over all 51 840 elements).
* **The bulk fills it exactly.** The tree structures contact C, 15-exchange E₁₅ (s + t + u) and 20-exchange E₂₀ are fully
  symmetric, supported on the boundary 15, and **linearly independent (rank 3)**. The three bulk diagrams span the whole
  3-dimensional space.
* **The hidden 20 is detected at four points.** E₂₀ has relative component **1/√10** outside span{C, E₁₅}. The bulk mode
  that never appears in boundary two- and three-point functions (11847) is detected by the four-point function, the
  finite analogue of seeing a bulk field only through exchange.

## 11853 — Lean: the Georgi–Glashow hypercharge spectrum

`W33.Pass11853HyperchargeSpectrum` (clean) builds 6Y on all 248 directions of E₈, starting from 6Y = (−2,−2,−2,3,3) on
the 5:
* the adjoint differences with one zero removed;
* the pair sums on the 10, ×5;
* their negatives, ×5;
* the 5̄ and the 5, ×10;
* the Lorentz-side 24, neutral.

It proves by `decide`:
* length 248;
* **counts 0³⁶ (±1)³⁰ (±2)³⁰ (±3)²⁰ (±4)¹⁵ (±5)⁶ (±6)⁵**, the spectrum measured numerically in 11845;
* tracelessness;
* the 10 = (Q, uᶜ, eᶜ) content.

## Prior art and scope

* **Classical.**
  * E₈ ⊃ Spin(11) × Spin(5), ⊃ SU(5) × SU(5), and the Georgi–Glashow / SO(10) branching.
  * Spin(5) ≅ Sp(4).
  * The quaternionic 4 of 2·A₆.
* **Corpus.**
  * Passes 11834 (Rac/Di), 11841 (couplings), 11843–11848, 11713 (family A₂ reading).
  * Parallel Rounds 30–35; Rounds 33 (§3, §3b), 34 and 35 (§1, §2) are directly related and cited above.
* **New here.**
  * Lorentz × central ℤ₃ ⇒ exactly su(3) ⊕ su(2) ⊕ u(1)_Y.
  * An independent Weil-Di realisation of the parallel track's so(11) result (Rounds 34/35 own it), with the Casimir
    certification, the exact spinor-sign blocks and the identification of the vector 5 (not Rac).
  * e₆ ∩ su(5)_GUT = su(2) ⊕ u(1) and A₂ = colour; the verdict that no examined embedding gives three generations
    (consistent with Round 35 §2).
  * The 4-point rank and detection of the hidden 20.
  * The Lean hypercharge spectrum.
* **A numerical lesson recorded.** `T.fixed_subalgebra` uses `vh.T` without conjugation. That is exact for real
  generators and for diagonal ℤ₃ torus elements, whose conjugates are inverses with the same fixed space. For general
  complex automorphisms it returns the commutant of the conjugate group. Here a conjugation-correct null space is used.
  The earlier results (11843–11850) involve only real generators or diagonal torus elements and are unaffected.
* **Scope.** Exact finite-group and Lie-algebra computations. "Family", "Standard-Model algebra" and "spinor" are fixed
  by Casimirs, hypercharge spectra and the action of −1. No vacuum, symmetry-breaking dynamics, masses or a
  three-generation mechanism is derived.
