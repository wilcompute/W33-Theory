# Pass 11893: the chiral spectrum of the heterotic W(3,3) sector at the radiative trinification point has no Standard Model

Producer: `analysis/w33_pass11893_trinification_chiral_spectrum.py`
Certificate: `data/w33_pass11893_trinification_chiral_spectrum.json` (9/9 checks)
Regression: `tests/test_w33_pass11893.py`
Track: Claude.

## Setting

The chiral heterotic realisation of the E₈ twisted sector is T⁶/ℤ₃ with the W(3,3) (A₈) shift. Its visible SU(9) matter
was established by orbifolder in Pass 11714:
* untwisted: 3 × 84, one per complex plane;
* twisted: 27 × 9̄.

Pass 11714 also owns the coupling: the untwisted cubic is the E₈ bracket, so W = g ε^{ijk}⟨Xᵢ, [Xⱼ, X_k]⟩.

**F-flatness.** It reads [Xⱼ, X_k] = 0, i.e. the three 84s pairwise commute in E₈. The grade-1 × grade-1 bracket is
exactly ∗(x∧y) and lands only in grade 2 (exact). So the supersymmetric moduli are three points of one common Cartan 𝔥,
which are also D-flat (11881). The radiative vacuum (11884) is X₁ = v on a Witting ray, X₂ = X₃ = 0.

## Spectrum at that vacuum (exact linear algebra)

* **X₂, X₃.** The mass matrix M_ab = ⟨v, ∗(a∧b)⟩ is antisymmetric with rank 56, so 28 of each stay massless.
* **X₁.** The su(9) orbit of v is 56-dimensional and is eaten by the 56 broken generators. X₁ keeps 28, whose singlet
  is the modulus v itself.
* **Unbroken group:** SU(3)³ (24 generators).
* **Each massless 28 = 27 + 1.** The 27 is *irreducible* under SU(3)³ (commutant dimension 2), i.e. a (3,3,3)-type
  representation in which every state is coloured. It is the grade-1 coset of the vacuum's E₆ (11887).
* **Each twisted 9̄** = three inequivalent anti-triplets (commutant dimension 3).

**Visible chiral spectrum:** 3·[(3,3,3) + 1] + 27·[(3̄,1,1) + (1,3̄,1) + (1,1,3̄)]. It is anomaly-free: 27 triplets
against 27 antitriplets in each factor. "Three families = three planes" (Holotrade 3caf15e, Pass 11714) shows up here as
three copies of (3,3,3).

## Standard-Model test

**Setup.** Colour must be one SU(3) factor; a diagonal colour produces sextets. The weak SU(2) commuting with it embeds
into each of the other two factors as trivial, 2+1, or principal (spin 1). The 27 anti-triplets carry no SU(2) charge,
so the net number of quark doublets is 3 × (the number of doublets in 3⊗3).

| embedding | spins in 3⊗3 | net quark doublets |
|---|---|---|
| trivial × trivial | 0⁹ | 0 |
| trivial × (2+1) | ½³ 0³ | **9** |
| trivial × principal | 1³ | 0 |
| (2+1) × (2+1) | 1, 0, ½, ½, 0 | **6** (+ coloured triplets) |
| (2+1) × principal | 3/2, ½, 1 | **3**, but with chiral coloured quartets (3,4) and triplets (3,3) |
| principal × principal | 2, 1, 0 | 0 |

**Conclusion: no SU(2) embedding gives three families with coloured states only in singlets and doublets.**
* A first draft of this pass claimed "never 3". That was wrong: principal × (2+1) gives 3.
* The corrected, and true, statement includes the exotic quartets.

**There is no three-family Standard Model at the radiative trinification point of this sector.**

## Reading

**Where the trinification-family states go.** The states that would make Standard-Model families here are the
bifundamentals (3̄,3,1) + … of trinification. At this vacuum they are exactly:
* the 54 eaten components of X₁;
* the components of X₂ and X₃ that get superpotential masses from v.

What stays light is the E₆ coset (3,3,3), the wrong 27.

**Consistency with the corpus.** This matches the corpus's independent finding that the order-3 heterotic route gives
no complete family (Forty Points §9, "order three fails"). It now has a vacuum-level reason. Within this programme, the
Standard Model must come from the even-order constructions (the ℤ₆ flagship, or the SO(16)×SO(16) models), or from a
higher-dimensional completion in which the (3,3,3) are gauge fields and the bifundamentals are matter.

## Scope

* Visible sector only.
* Tree-level superpotential masses only.
* The trinification point of 11884 (bosonic loops) only. Other regimes of the phase diagram (11890–11892) have finite
  or other unbroken groups and are not tested here.
