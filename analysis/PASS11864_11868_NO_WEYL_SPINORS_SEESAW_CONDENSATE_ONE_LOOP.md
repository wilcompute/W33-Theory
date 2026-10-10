# Passes 11864–11868 — the finite Lorentz group has no Weyl spinors and its spinor has no helicity; the unique Lorentz-invariant B−L condensate breaks to exactly the Standard-Model algebra; coloured (charged-sector) momenta have only rotation little groups; one loop removes the tree positivity bounds; Lean: A₆ ↛ GL(2,ℂ)

**Files.**
* Producers:
  * `analysis/w33_pass11864_11866_weyl_chirality_bl_quark_sectors.py`
  * `analysis/w33_pass11867_one_loop_positivity.py`
* Frozen:
  * `data/w33_pass11864_11866_weyl_chirality_bl_quark_sectors.json`
  * `data/w33_pass11867_one_loop_positivity.json`
* Lean: `formal/W33/Pass11868A6NotInGL2RealFixed.lean`
* Regression: `tests/test_w33_pass11864_11868.py`

## 11864 — chirality and the finite Lorentz group

* **SL(2,9) is ambivalent.** Every element is conjugate to its inverse (checked on all 720). Equivalently:
  * #{g² = 1} = 2 and #{g² = −1} = 90, so A₆ has 45 involutions;
  * the Frobenius–Schur sums then force **every A₆ irreducible real and every faithful SL(2,9) irreducible
    quaternionic**.

  **The finite Lorentz group has no complex representations at all, hence no analogue of a Weyl spinor (1/2, 0).**
  Contrast: the massive little group SL(2,3) does have complex irreducibles (Pass 11842).
* **Di has no helicity on the light cone.** Restricted to the massless little group 3² ⋊ ℤ₄ (order 36), the Lorentz
  spinor Di contains **no** helicity character: m_n = 0 for n = 0, 1, 2, 3. All four dimensions lie in the 2-dimensional
  "continuous-spin"-type representations, because the little group's translations act on Di without fixed vectors.
* **Consequence.**
  * The helicity modules H₁ and H₃ (Pass 11840) are conjugate and inequivalent, so Wigner-type chirality exists for
    the finite Poincaré group.
  * But matter of the form R ⊗ Di contributes **no** helicity states. A Weyl (helicity) projection of Di-matter is
    empty, so no chiral fermion of helicity ±½ can be built from the two-qutrit Lorentz spinor.
  * The triality-paired orbifold (quarks in the charged sectors) cannot change this.
  * Together with 11855/11859 (no E₈ automorphism is chiral), **chirality is excluded for all Di-carried matter of the
    finite geometry.** A chiral theory would need massless fermions with nonzero helicity, i.e. matter carried by
    Lorentz data other than Di (helicity modules built on spinors, Pass 11840).

## 11865 — B−L breaking: a unique, Lorentz-invariant Majorana condensate gives exactly the Standard-Model algebra

* **Setting.** The spinorial structure is SL(2,9) × central ℤ₃, with commutant su(3) ⊕ so(5) ⊕ u(1)_{B−L}
  (Passes 11857, 11862).
* **The candidates.** The SM-singlet states of E₈ form a 25-dimensional space:
  * **17 with B−L = 0**, Lorentz scalars;
  * **4 with B−L = +3/4 and 4 with B−L = −3/4**, all in the Lorentz-spinor block (one Di each), i.e. νᶜ-type.

  So **every B−L-charged SM singlet is a Lorentz spinor**, and B−L cannot be broken by a Lorentz-invariant
  *field* vev.
* **The condensate.** On the B−L = +3/4 singlets (≅ Di) there is **exactly one Lorentz-invariant bilinear**, and it is
  **antisymmetric**: the quaternionic ε-form of Di. This is a Majorana-type fermion condensate ⟨νᶜνᶜ⟩ with B−L charge
  2 × (lepton charge).
* **Its stabiliser** inside su(3) ⊕ so(5) ⊕ u(1) has dimension 15 and rank 4: a 3-dimensional nilradical (the complex
  stabiliser of a vector) and a **Levi part of dimension 12 containing su(3), su(2) and Y**. That Levi part is **exactly
  su(3) ⊕ su(2) ⊕ u(1)_Y**. The compact stabiliser, which is the physical unbroken symmetry, is the Standard-Model
  algebra.
* **Reading.** This is the left–right seesaw pattern (SU(2)_R × U(1)_{B−L} → U(1)_Y by a ν^c-type Majorana
  condensate), here **forced**: it is the unique Lorentz-invariant B−L-breaking order parameter of this E₈ structure.
* **Bulk preference.** The bulk 15 and 20 modes are internal singlets (11862), so the bulk cannot pick a different
  direction. The condensate is the only option. Its dynamics (whether it forms) is not derived.

## 11866 — little groups of the charged (quark) sectors

| sector | orbit | little group in A₆ | spin lift | type |
|---|---:|---|---:|---|
| k = 0 (neutral, Minkowski) | 1 | A₆ | 720 | rest |
| | 20 | 3² : 2 | 36 | massless (translations) |
| | 30, 30 | A₄ | 24 | massive (finite SU(2) = SL(2,3)) |
| k = 1, 2 (charged, conjugate) | 6 | **A₅** | 120 (binary icosahedral) | rotation |
| | 15 | **S₄** | 48 (binary octahedral) | rotation |
| | 60 | **S₃** | 12 | rotation |

* Only the neutral sector has a little group with a 3² "translation" part, i.e. a light-cone. **The charged sectors'
  little groups are all finite rotation groups**: icosahedral, octahedral and dihedral, all inside SO(3), with
  binary-polyhedral spin lifts inside SU(2).
* **Reading (conditional on the triality pairing of 11862).** Coloured states (triality ±1) would carry only
  rotation-type, massive-like little groups. Only colour singlets could sit on a light-cone momentum. This echoes "no
  massless coloured asymptotic states"; it is a kinematic observation, not a derivation of confinement.

## 11867 — one loop: positivity is restored, so the tree bounds mark loss of perturbative control

* **Conventions.** As in 11861. The one-loop 1PI four-point diagrams are:
  * the φ⁴ bubble (s + t + u, weight 1/2);
  * the φ⁴–φ³–φ³ triangle (all six pairings);
  * the φ³ box (three cyclic orders).

  All are fully crossing-symmetric and scalar on each channel, with **integer** channel eigenvalues:

  | channel | D | C | E₁₅ | Bubble | Triangle | Box |
  |---|---:|---:|---:|---:|---:|---:|
  | 60 | 2 | 0 | −96 | 144 | 3840 | 15360 |
  | 24 | 2 | 0 | 96 | 144 | 768 | 3072 |
  | 20 | 2 | 24 | 288 | 1008 | 18432 | 46080 |
  | 15 | 2 | 24 | 384 | 1008 | 16896 | 39936 |
  | 1 | 17 | 60 | 576 | 3384 | 62208 | 179712 |

* **The bubble and box are positive in every channel.**
  * The 60-channel at one loop, 2 − 96g₃² + 15360g₃⁴, has negative discriminant, so it is **positive for all g₃**.
  * The 15-channel at g₃ = 0, 2 − 24g₄ + 1008g₄², is likewise positive for all g₄.
  * On the scanned grid the allowed region grows from **33% (tree) to 90% (one loop)**.
* **Conclusion.** The tree "bounds" g₃² ≤ 1/48 and g₄ ≤ 1/12 of 11861 mark where truncated perturbation theory fails:
  the one-loop terms equal the tree terms at g₃² ≈ 96/15360 = 1/160 and g₄ ≈ 24/1008 = 1/42. They are not true
  exclusions. **Positivity does not fix the couplings.** The O(1) combinatorial weights are a stated convention; the
  sign structure (positive bubble and box) does not depend on it.

## 11868 — Lean: A₆ has no faithful image in GL(2, ℂ); the real-structure lemma

`W33.Pass11868A6NotInGL2RealFixed` (self-contained, clean) proves:
* the involution lemma in SL(2,ℂ);
* **(0 1)(2 3) = ⁅(0 1)(0 2), (0 1)(0 3)⁆ and (0 1)(2 4) = ⁅(0 1)(0 2), (0 1)(0 4)⁆** (by `decide`);
* that a homomorphism to a commutative group kills commutators;
* **`no_injective_hom_GL2`**: an injective A₆ → GL(2,ℂ) would send both involutions, which have determinant 1, to −1;
* **`real_structure_fixed`**: if gJ = Jḡ, then the fixed space of g is preserved by v ↦ J v̄.

The first closes the family no-go of 11854 for U(2) **without** needing perfectness of A₆. The second is the linear-
algebra core of "no E₈ automorphism is chiral" (11859).

## Prior art and scope

* **Classical.**
  * SL(2,q) for q ≡ 1 (mod 4) has only self-conjugate characters.
  * Wigner's continuous-spin representations.
  * The left–right-symmetric seesaw (Mohapatra–Senjanović): SU(2)_R × U(1)_{B−L} → U(1)_Y by a ν^c-type triplet vev.
  * Finite subgroups of SO(3)/SU(2).
  * Perturbative unitarity versus loop restoration.
* **Corpus.**
  * Passes 11836, 11840, 11842, 11855, 11857–11863.
  * Parallel Rounds 33–35, cited earlier. No parallel commit since 11859 touches these questions (checked).
* **New here.**
  * Ambivalence of the finite Lorentz group and the absence of Weyl spinors.
  * The vanishing helicity content of Di.
  * The unique Lorentz-invariant B−L condensate and its SM Levi stabiliser.
  * The charged-sector little groups.
  * The one-loop channel table and the restoration of positivity.
  * The two Lean theorems.
* **Scope.**
  * Exact finite-group computations; Lie algebra to 10⁻⁹. "Majorana condensate", "seesaw", "colour" and
    "confinement-like" are readings of computed structures.
  * No dynamics forms the condensate.
  * The no-chirality statement concerns Di-carried matter of this structure.
