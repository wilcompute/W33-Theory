# Pass 11900: three generations over a point of W(3,3)

Producer: `analysis/w33_pass11900_three_generations_over_a_w33_point.py`
Certificate: `data/w33_pass11900_three_generations_over_a_w33_point.json`
Regression: `tests/test_w33_pass11900.py`
Track: Claude.

## The question

Passes 11897–11899 put the W(3,3) structure in the Kähler moduli of two Wilson-line-free ℤ₃ tori. Three-generation ℤ₃
models, however, need Wilson lines on two of the three tori. This is known (Ibáñez–Kim–Nilles–Quevedo), and in the
corpus it is Pass 11105's "one qutrit, never two". The question is what survives of W(3,3) once a Wilson line is on.

## Result (family torus 1, Wilson-line torus 2)

| quantity | value |
|---|---|
| holonomy of the torus-2 Wilson line | the Pauli Z₂, i.e. a **point p of W(3,3)** |
| compatible Kähler dualities = centraliser of Z₂ | linear order 1296, **projective 648 = the W(3,3) point stabiliser** |
| families | the three Z₂ eigenspaces (fixed f₂, varying f₁): one qutrit each, p^⊥/p |
| dualities on the Wilson-line-neutral class (f₂ = 0) | **T′ only** (projective 24) |
| dualities on the charged classes (f₂ = 1, 2) | **the full one-qutrit Clifford group** (projective 216), with no space-group input |
| with the space-group Δ(54) added | Clifford (216) on every class |

**Why the charged classes get Δ(54) for free.** On the class f₂ = a, two dualities restrict to the Paulis of the family
qutrit (to 10⁻¹⁵):
* the GL(2,ℤ[ω]) transvection (f₁, f₂) → (f₁ + f₂, f₂) restricts to the shift **X₁^a**;
* the off-diagonal B-shift (the entangling gate ω^{2f₁f₂}) restricts to the clock **Z₁^{2a}**.

So the "traditional" flavour group of the families is what remains of the entangling, off-diagonal Kähler dualities.

The match of this order-648 group with the qutrit Clifford group (H₂₇ : SL(2,3)) was already in the corpus:
`analysis/2026-09-21_physical_a2_clifford648_w33_bridge.md` and Pass 11105. What is new here is how a Wilson line
selects that point, and that on charged classes the dualities generate Δ(54).

## Yukawa consequence

Take families on torus 1, with left- and right-handed fields in Wilson-line classes that differ by a. The renormalisable
twisted spectrum is then (θ₍₀,ₐ₎, θ₍₁,ₐ₎, θ₍₂,ₐ₎), times factors from the other tori.

* **a = 0.** The light pair is degenerate **exactly, for every value of the moduli**, because θ is even:
  θ₍₂,₀₎ = θ₍₁,₀₎. Measured to 10⁻¹⁴.
* **a ≠ 0.** The light pair is degenerate at diagonal moduli (10⁻¹⁶) and split by the off-diagonal Kähler modulus at
  **third order**. Splitting/s³ is constant: 86.66, 86.60, 86.59 for s = 10⁻², 5·10⁻³, 2.5·10⁻³.
  * Why third order: each torus's ℤ₃ rotation fixes its own cosets (ω ≡ 1 mod √−3), and the splitting is odd under
    f₁ → −f₁. The first term allowed by both is (x̄₁x₂)³, i.e. Z₁₂³.
  * A first draft predicted a linear splitting. The measurement (s³ scaling) corrected it before commit.

Quark mixing is still absent at this level. This is the diagonal selection rule of prime orbifolds (Casas–Gómez–Muñoz);
Abel–Muñoz obtain mixing from Fayet–Iliopoulos-induced field mixing.

## Not established

* **Wilson lines.** Only one Wilson line is analysed, on the two-torus subsystem. The third torus's Wilson line enters
  only through overall factors.
* **Which class hosts the families.** Whether the Standard-Model families sit in a neutral or a charged class, and
  hence whether their Δ(54) comes from the dualities, is model-dependent and not computed.
* **Yukawa normalisation.** The overall normalisation (the argument κZ of the instanton thetas) is not fixed. The
  degeneracy statements do not depend on it.

## Prior art

* Ibáñez–Kim–Nilles–Quevedo (1987): three generations need two Wilson lines in ℤ₃.
* Casas–Gómez–Muñoz, hep-th/9110060 and hep-th/9206083: Z_N Yukawa structure and the diagonal selection rule.
* Abel–Muñoz, hep-ph/0212258.
* Nilles–Ramos-Sánchez–Vaudrevange: the eclectic group of T²/ℤ₃, order 648.
* Corpus: 11105; 2026-09-21 Clifford-648 bridge; 11897–11899.
