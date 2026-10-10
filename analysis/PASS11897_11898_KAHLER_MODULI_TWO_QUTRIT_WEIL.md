# Passes 11897–11898: the Kähler moduli of two ℤ₃ tori carry the W(3,3) structure — an SM-neutral home for the Siegel modulus

Producer: `analysis/w33_pass11897_11898_kahler_moduli_two_qutrit_weil.py`
Certificate: `data/w33_pass11897_11898_kahler_moduli_two_qutrit_weil.json`
Regression: `tests/test_w33_pass11897_11898.py`
Track: Claude.

## Why

Pass 11896 found that every Kempf–Ness flat direction in the visible untwisted sector of the flagship is
Standard-Model-charged. In that sector, the Siegel-type modulus and the Standard Model exclude each other. The question
this pass answers: is there a field that carries the same two-qutrit/Siegel structure and is gauge-neutral by
construction?

## Setting

T⁴/ℤ₃ = (ℂ/ℤ[ω])²/ℤ₃.
* The complex structure is frozen at ω.
* The untwisted moduli form the Hermitian Kähler-plus-B matrix Z, with 4 complex entries, the off-diagonal ones
  included. The ℤ₃ orbifold keeps all T_{i j̄}; T⁶/ℤ₃ has the classic nine.
* Z is a point of the Hermitian half-space over O = ℤ[ω], whose duality group is U(2,2;O).
* The nine fixed points are (O/√−3)² = F₃², the basis of two qutrits.
* The twisted instanton sums are built from

  θ_μ(Z) = Σ_{x ∈ O² + μ/√−3} e(x* Z x),  μ ∈ F₃².

## 11897: the finite modular flavour group is the two-qutrit Weil representation of Sp(4,3)

Numerical transformation laws (relative error ≤ 10⁻¹²):

| duality | action on the nine fixed-point functions |
|---|---|
| Z → −Z⁻¹ | θ(−Z⁻¹) = det(Z/i) · F θ(Z), with F = (1/3) ω^{μ·ν}: weight 1, Fourier on both qutrits |
| Z → Z + diag(1,0) | phase gate ω^{c₁²} |
| Z → Z + B, B₁₂ = 1 or ω | **entangling gate ω^{2c₁c₂}** |
| Z → Z + B, B₁₂ ∈ √−3·O | trivial |
| Z → A*ZA, A ∈ GL(2,O) | μ → Aμ mod √−3 |

* **Order.** The group these generate has projective order **51840**. Its conjugation action on the Pauli group is an
  isomorphism onto **Sp(4,3) = Aut W(3,3)**: the image has order 51840 and preserves the symplectic form. The linear
  group has order 103680.
* **Diagonal moduli alone** (one SL(2,ℤ) per torus) give only **576 = |T′ × T′|**. The entangling W(3,3) structure is
  carried exactly by the off-diagonal Kähler moduli.
* **Odd part.** θ_μ = θ_{−μ}, so the moduli-dependent couplings span the even Weil **5**, and the odd **4** vanishes
  identically. This is the same 5 + 4 split as 11874–11878.
* **The full eclectic group.** Two Wilson-line-free tori also carry the space-group Heisenberg group 3^{1+4}
  (Pass 11105: Δ(54) per torus). Together with the modular group above, this gives the full two-qutrit Clifford group.
  The 40 projective classes of the traditional flavour group, under commutation, form SRG(40,12,2,4) = W(3,3).
  * One-torus prior art: Δ(54) and T′ = SL(2,3), which combine to the order-648 eclectic group (Nilles, Ramos-Sánchez,
    Vaudrevange et al.). The order-648 group is the one-qutrit Clifford group.
  * Two-torus Siegel prior art: Baur–Kade–Nilles–Ramos-Sánchez–Vaudrevange (Sp(4,ℤ) with a Wilson-line modulus).
  * The Hermitian Eisenstein two-torus case was not found in the literature searched.

## 11898: geometry, and the three-torus case

* **Dominance.** The five even weight-1 thetas map the Kähler moduli **dominantly onto ℙ⁴**: the real Jacobian has rank 8.
* **Invariants.** The PSp(4,3)-invariant quartic is unique (the Burkhardt quartic). Invariant dimensions in degrees
  4, 6, …, 18 are 1, 1, 1, 2, 3, 2, 4, 5.
* **The Siegel slice** (Z real symmetric) is the fixed locus of Z → Zᵀ, and θ(Zᵀ) = θ(Z).
  * Its image satisfies no invariant relation below degree 18, and exactly one in degree 18.
  * It lies in the **dual Burkhardt hypersurface**, whose degree is 4·27 − 2·45 = 18.
  * Robust test: for each Siegel point y, some solution of ∇I₄(b) = y (taken in the contragredient basis) lies on
    {I₄ = 0}, with defect ~10⁻¹⁶. For generic Kähler points the defect is ≥ 10⁻³.
  * This is Freitag–Salvati Manni's description of the Satake compactification of 𝒜₂(3) (the normalisation of the dual
    Burkhardt), which links Hermitian modular forms of level √−3 to the Burkhardt group. **The mathematics is theirs;
    the identification with orbifold Kähler moduli is the step taken here.**
* **T⁶/ℤ₃.**
  * Inversion on the 27 fixed points: θ(−Z⁻¹) = det(Z/i) · F^{⊗3} θ(Z), checked to 10⁻¹⁵.
  * 14 even functions, from 27 = 14 + 13.
  * The modular group reduces mod √−3 to Sp(6,3), of order 9170703360.
  * In the SU(9) sector of Pass 11714 the 27 fixed points carry the twenty-seven twisted 9̄s.

## What this changes

* **A neutral home for the Siegel modulus.** Kähler moduli are gauge singlets. The two-qutrit/Siegel structure behind
  Passes 11869–11896 therefore has a **Standard-Model-neutral** home in the geometry of two ℤ₃ tori. Moving it there
  does not cost the Standard Model, which resolves the 11896 tension at the level of *which field carries it*.
* **Where entanglement comes from.** The entangling gate (CZ-type) is an **off-diagonal B-field across the two tori**.
* **The earlier Siegel picture.** The Siegel modulus of 11869 corresponds to the real-symmetric slice of the Kähler
  moduli, which is a branch locus (θ(Zᵀ) = θ(Z)).

## Not established

* **Wilson-line-free tori.** The construction needs two Wilson-line-free tori.
  * The SU(9) sector (Pass 11714) has them.
  * The 104 three-generation spectra of Pass 11105 do not: their Wilson lines leave one torus free. Wilson lines are
    known to reduce the modular group to congruence subgroups, and that reduction is not computed here.
* **Modular stabilisation.** No moduli stabilisation (a modular-invariant potential) is computed, so which Z is the
  vacuum is open.
* **Yukawa prefactors.** The exact Yukawa prefactors (quantum part, triangle-area normalisation, as in Casas–Gómez–Muñoz
  and Burwick–Kaiser–Müller) are not rederived. Only the modular-covariant theta building blocks are used.
* **Physical meaning of the Siegel slice.** The slice is the fixed locus of Z → Zᵀ. Its identification with a
  CP-type involution is not computed.

## Prior art

* Freitag–Salvati Manni, Manuscripta Math. 119 (2006): Hermitian modular forms and the Burkhardt quartic.
* Freitag–Salvati Manni (2004): A₂(3) and the Burkhardt quartic.
* Dern–Krieg: Hermitian modular forms over ℚ(√−3).
* Nilles–Ramos-Sánchez–Vaudrevange: the eclectic flavour group of T²/ℤ₃.
* Baur–Kade–Nilles–Ramos-Sánchez–Vaudrevange: arXiv:2012.09586.
* Nilles–Ramos-Sánchez–Trautner–Vaudrevange: arXiv:2105.08078.
* "On the moduli space of the T⁶/ℤ₃ orbifold and its modular group" (hep-th/9204040): the SU(3,3) moduli of T⁶/ℤ₃.
* Corpus:
  * 11105 (Δ(54) = traditional group; two Wilson-line-free tori needed for 3^{1+4});
  * 11714 (SU(9) sector);
  * 11869–11896 (Siegel modulus chain);
  * 11874–11878 (Weil 5 + 4).
* Rediscovery-guard candidates, read and different: PASS331_332 (integral lift of the Weil incidence module), PASS214_218 (dual-ovoid Weil shadows), PASS10954 (C8 clock). None concerns orbifold Kähler moduli or the Hermitian theta action.
