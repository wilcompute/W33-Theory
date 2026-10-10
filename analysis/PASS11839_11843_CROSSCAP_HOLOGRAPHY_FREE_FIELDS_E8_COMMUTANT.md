# Passes 11839–11843 — crosscap holography in the finite AdS₄, finite spinor-helicity, the singleton couplings, no three-doublet spin, and an E₈ commutant su(3) ⊕ su(2) for the finite Lorentz group

Producers:
* `analysis/w33_pass11839_11842_crosscap_fields_couplings_spin.py`
* `analysis/w33_pass11843_e8_tits_lorentz_commutant.py`

Frozen:
* `data/w33_pass11839_11842_crosscap_fields_couplings_spin.json`
* `data/w33_pass11843_e8_tits_lorentz_commutant.json`

Regression: `tests/test_w33_pass11839_11843.py`

These passes follow Passes 11831–11838:
* 11831–11833: the finite AdS₄ of two qutrits. Bulk = 36 Kramers reversals, boundary = 40 contexts; finite Lorentz group
  SL(2,9) with tangent Minkowski space.
* 11834: the exact linear Weil representation C⁹ = Rac (5) ⊕ Di (4).
* 11835: the bulk C[36] = 1 + 15 + 20, where the boundary sees only the 15.
* 11837: the Weil-embedded E₈ commutes with Lorentz only through u(1)_P.

## 11839 — an explicit holographic map: bulk points are crosscaps

Each Kramers reversal p gives an anti-symplectic J_p with J_p² = −1. With K the complex conjugation (which acts as
J_K = (x, z) ↦ (x, −z)), its antiunitary is T_p = U_{J_p J_K} K, built from the exact linear Weil representation U.

* **T_p² = P exactly** for all 36, at the operator level. Pass 11210 owns this statement as a θ² classification.
* **The crosscap form B_p(ψ, φ) = ⟨T_p ψ, φ⟩** is:
  * symmetric on Rac;
  * antisymmetric on Di;
  * zero between them.
* **On Rac the crosscaps are exactly Sp(4,3)-equivariant**: U_hᵀ B_{hp} U_h = B_p, with error 8·10⁻¹⁵. The reason is
  that T_{hJh⁻¹} = U_h T_J U_h⁻¹ holds exactly in the linear representation, and the sign ambiguity J ↔ −J acts as P,
  which is trivial on Rac.
* **The holographic map Φ : Sym² Rac → C[36], v ↦ (p ↦ B_p(v)), is injective with image exactly the 15-dimensional bulk
  mode.** The 36 crosscaps span all of Sym² Rac (rank 15), and Φ's image lies in the eigenvalue-3 eigenspace of the bulk
  orthogonality graph (residual 2·10⁻¹⁴). This turns Pass 11835's module isomorphism into an explicit map. The Di
  crosscaps span all of Λ² Di (rank 6).
* **Bulk two-point function.** ⟨C_p, C_q⟩ is 5 for coincident points, **+1 for orthogonal pairs** (anticommuting, the
  Fourier relation of 11833) and **−1 for null-separated pairs** (unipotent-tick relation). So G = 6I + 2A − J: it vanishes
  on the constant and on the 20, and equals 12 on the 15.
* **A flat control.** For every context the crosscap weights of its 9 stabiliser states sum to Σ_s |B_p(s₊, s₊)|² = 1,
  for every reversal p. Single stabiliser states therefore do not carry the incidence; the context-level relation of
  11835 does.

**Literature.** In AdS/CFT, local bulk states are crosscap (Ishibashi-type) states of an involution of the boundary
theory: H. Verlinde, arXiv:1505.05069, and Y. Nakayama and H. Ooguri, arXiv:1605.00334. Here the involution is the
Kramers time reversal. In this finite form, bulk point = time reversal is exact.

## 11840 — finite free fields

* **Shell propagators.** G_s(x) = (1/81) Σ_{k ∈ s} ω^{β(k,x)}, exact rationals by the class of x:

  | shell | x = 0 | null x | split-type x | Kramers-type x |
  |---|---:|---:|---:|---:|
  | massless (20) | 20/81 | **−7/81** | 2/81 | 2/81 |
  | split-type (30) | 30/81 | 3/81 | 3/81 | −6/81 |
  | Kramers-type (30) | 30/81 | 3/81 | −6/81 | 3/81 |

  **The massless propagator takes its one distinct value exactly on the light cone**, the finite counterpart of the
  light-cone singularity. The association scheme is self-dual: the propagator table is the eigenvalue table divided by 81.
* **Finite spinor-helicity theorem.** Let H_n be the space of functions on the 80 spinors ψ ∈ F₃⁴ = F₉² with
  f(J₀ψ) = iⁿ f(ψ). Let translations act by ω^{β(k(ψ), x)}, with k(ψ) = ψ ∧ J₀ψ the null momentum of 11833, and Lorentz
  act by g⁻¹ on ψ. Then H₀, H₁, H₂ and H₃ are **four irreducible, pairwise inequivalent 20-dimensional representations**
  of the finite Poincaré group: character norm 1, cross terms 0, summed over all 720 × 81 elements. These are the massless
  representations of helicity n/2 mod 2: massless fields of given helicity are homogeneous functions on spinors, as in
  the spinor-helicity and Penrose pictures.

## 11841 — Sp(4,3)-invariant cubic couplings

These are character sums over the ten irreducible modules: Rac, Rac*, Di, Di*, S15 = Sym² Rac (bulk ∩ boundary),
b20 (bulk ∩ splits), X24, D15, A10 = Λ² Rac and c20 = Rac ⊗ Di*. Selected results (full table in the certificate):
* **Rac·Rac·S15 = 1**, the crosscap vertex of 11839, and **Rac·Rac*·X24 = 1**.
* **The hidden bulk mode b20 has no Rac·Rac vertex.** It couples to c20·c20, i.e. to (Rac⊗Di*)², a mixed
  boson–fermion four-singleton composite. It also couples to A10·A10, D15·D15 and X24·X24. **The bulk mode that the
  boundary bilinears cannot see is reached through boson–fermion pairs.**
* **Di·Di·A10 = 1**: Sym² Di ≅ (Λ² Rac)*.
* **The bulk interacts with itself.** S15³ = 1, S15²·b20 = 1, S15·b20² = 1, b20³ = 2. The symmetric cubic self-couplings
  are S15: 1, b20: 2, X24: 2, D15: 1.

## 11842 — massive spin content: no three-doublet structure

The singletons are restricted to the massive little group SL(2,3) (Pass 11836), with the Z₃ labels of its abelianisation;
the character table was verified orthonormal.

| momentum | Rac (5) | Di (4) |
|---|---|---|
| Kramers-type ("timelike") | 1₁ + 1₂ + 3 | **2·2₀** (two identical neutral doublets) |
| split-type ("spacelike") | 2·1₀ + 3 | **2₁ + 2₂** (a conjugate charged pair) |

* **The three Z₃-labelled spin-½ copies of SL(2,3) never appear together.** The "three generations from the massive
  little group" reading raised as an open question in 11836 is **refuted**.
* The Z₃ generator is neither a diagonal phase gate nor a transvection, so the label is not the level (Pauli Z) flavour
  grading of Pass 11830.
* Bosons and fermions trade the Z₃ charge between the two massive shells.

## 11843 — the finite Lorentz group commutes with su(3) ⊕ su(2) in E₈ through the W(E₆) embedding

Pass 11837's no-go used the Weil embedding Sp(4,3) → SU(9) → Aut(E₈), and its commutant was u(1)_P. The same abstract
group also acts through PSp(4,3) ≅ W(E₆)′ on E₈ ⊃ E₆ × A₂, by Tits lifts of Weyl elements.
* A Kramers reversal is an E₆ root pair ±α (Pass 11210).
* Its finite Lorentz group (image A₆, Pass 11832) is W(A₅)′, the derived Weyl group of the A₅ of roots orthogonal to α.

**Construction.**
* E₈ is built in a Chevalley basis with the Frenkel–Kac sign cocycle (Jacobi error 3·10⁻¹³).
* The Tits automorphisms are n_β = exp(ad E) exp(−ad F) exp(ad E) (automorphism error 3·10⁻¹⁴).
* The subsystems check out: E₆ (72 roots) ⟂ A₂ (6), A₅ (30) ⟂ α, and A₁ = ±α.

| lift of the finite Lorentz group | commutant in E₈ |
|---|---|
| even Tits words n_b n_c of the A₅ simple roots (W(A₅)′) | **dim 11, rank 3, centre 0, semisimple: su(3) ⊕ su(2)** |
| all Tits words (with parity, W(A₅)) | same |
| with the torus 2-elements n_b² | same |
| control: even Tits words of all of W(E₆)′ | dim 8: su(3) (the A₂ centralising E₆) |

* The commutant contains, and by dimension equals, **su(3) = the A₂ commuting with E₆** plus **su(2)_α = the SU(2) of the
  Kramers root itself**.
* **The no-go of 11837 therefore depends on the embedding.**
  * Through the Weil route the finite Lorentz group commutes with a single u(1).
  * Through the W(E₆) route it commutes with su(3) ⊕ su(2) exactly, the non-abelian part of the Standard Model gauge
    algebra.
  * Neither route gives a u(1)_Y alongside: the Tits commutant has no centre.
* Structurally, E₈ ⊃ SU(6) × SU(3) × SU(2) is the maximal-rank subgroup of the extended diagram. The finite Lorentz
  group's Tits lift sits inside SU(6) and is large enough to have the full commutant SU(3) × SU(2) of SU(6).

**Which su(3).**
* In Pass 11713's level dictionary, the A₂ centralising E₆ is the **family** SU(3) on three levels, not colour.
* Under the trinification reading of Passes 11701–11703, it would be one of the A₂ factors.

This packet does not decide between the two. It establishes the commutant, not its physical name.

**Prior art.**
* Passes 11692 and 11701–11703 found su(3) ⊕ su(2) ⊕ u(1)⁵ as the centraliser of single E₈ elements ("clocks"), which
  are rank-8 torus centralisers.
* This is a different object: the commutant of a non-abelian finite group, rank 3, with no u(1)s.
* The subgroup E₈ ⊃ A₅ × A₂ × A₁ is classical (Borel–de Siebenthal).

## Scope

* **Exact.** Crosscap equivariance, rank and image; the propagator and helicity character sums; the coupling
  multiplicities; the SL(2,3) decompositions. The E₈ commutants are exact up to floating SVD tolerance, with closure
  errors ≈10⁻¹⁵.
* **The Tits lift is one choice.** Twisting by torus 2-elements was checked and is invariant. Other non-Weyl actions of
  PSp(4,3) on E₈ are not classified.
* **Names are labels, not identifications.** "Holographic", "propagator", "helicity", "timelike" are names fixed by the
  finite structures; no dynamics, scale or continuum limit is derived.
* **The su(3) ⊕ su(2) is a commutant, not an unbroken gauge group of a vacuum.**

## Next

1. Find the embedding of the finite Poincaré group, translations included, into E₈ or E₈ × E₈, and compute its commutant.
2. Test whether combining the Weil u(1)_P with the Tits su(3) ⊕ su(2) is consistent inside one action: a candidate
   su(3) ⊕ su(2) ⊕ u(1).
3. Assemble the crosscap two-point function and the cubic vertices into a finite bulk path integral, and check boundary
   correlators.
4. Find which E₆ 27s carry the singletons under the Tits embedding: the matter content seen by su(3) ⊕ su(2).
5. Write Lean statements for the crosscap symmetry (T² = ±1 ⇒ symmetric/antisymmetric).

## Correction (Pass 11845)

The group used above for "the finite Lorentz group" (generated by **all** ordered pairs n_a n_b of A₅ Tits elements)
is not A₆ itself: it contains order-2 elements of the SU(6) torus. Its commutant su(3) ⊕ su(2) is correct **for that
group**. The faithful A₆ lift, generated by the adjacent words n_i n_{i+1} (order exactly 360) or by permutation
matrices, commutes with **su(5)**. The torus 2-elements break su(5) to su(3) ⊕ su(2), and the direction they break is
exactly the Georgi–Glashow hypercharge. See `analysis/PASS11844_11848_LORENTZ_COMMUTANT_SU5_HYPERCHARGE_BULK_PATH_INTEGRAL.md`.
