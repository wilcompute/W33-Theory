# Passes 11869–11873: W(3,3) is the level-3 structure of a genus-2 modulus

Producer: `analysis/w33_pass11869_11873_siegel_level3_two_qutrits.py`
Certificate: `data/w33_pass11869_11873_siegel_level3_two_qutrits.json` (10/10 checks)
Regression: `tests/test_w33_pass11869_11873.py`
Track: Claude.

## How this pass came about

The brief was to stop running exhaustive tests and to read both papers in full: `w33_paper.pdf` (790 pp.) and the
Forty Points paper. Pass 11873, below, is the reading ledger.

The reading turned up one structural thread that runs through all three of these, and that no pass had followed:
* the Burkhardt supplement of the PDF (Supp. ω/ℵ, pp. 659–666);
* the CZ₃ Wilson-line result (§79.81, p. 395);
* the S₃ = ⟨z, s⟩ ↔ Konopka bridge (§79.79–80, pp. 393–394).

All three point at the same classical object: the **moduli space of abelian surfaces with level-3 structure**.

The literature check came first:
* Γ₂,₃ = Sp(4,ℤ)/Γ₂(3) ≅ Sp(4,F₃) is known in modular-flavour physics.
* Carducci–Meloni–Parriciatu–Penedo 2026 quote |Γ₂,₃| = 51840, then work at level 2 because level 3 is "too large".
* Kikuchi–Kobayashi et al. use Sp(4,ℤ) on magnetized T⁴.
* None of them connects Γ₂,₃ to W(3,3), to the qutrit Pauli/Clifford structure, or to this corpus's arrow and chirality
  results.

The corpus grep (`Siegel`, `eclectic`, `modular flavour`, `Γ₂,₃`) found only "Siegel parabolic" in the group-theory sense.

## The dictionary

Take a principally polarised abelian surface A = ℂ²/(ℤ² + Ωℤ²), with Ω in the Siegel half-space H₂. Its nine level-3
theta functions are

  f_c(z) = θ[c/3, 0](3z, 3Ω),   c ∈ F₃².

Mumford's theta group acts on them, and so does the Siegel modular group. Write ψ(Ω)_c = f_c(0) for the theta-null
vector.

| two-qutrit / W(3,3) object | genus-2 geometry |
|---|---|
| Hilbert space ℂ⁹ | level-3 theta functions of A |
| Pauli group 3^{1+4} | translations by A[3] (Weil pairing = commutator) |
| W(3,3) | the symplectic space A[3] = F₃⁴ |
| Clifford group mod Paulis = Sp(4,3) | finite Siegel modular group Γ₂,₃ = Sp(4,ℤ)/Γ₂(3) |
| qutrit Hadamards F⊗F | S: Ω ↦ −Ω⁻¹ (weight ½, factor √det(−iΩ)) |
| CZ₃ | shear Ω₁₂ ↦ Ω₁₂ + 1 |
| local phase gate | Ω₁₁ ↦ Ω₁₁ + 2 |
| SWAP | exchange of the two tori |
| outer coset of W(E₆) = PGSp(4,3) (antiunitary, time-reversing, chirality-swapping; Cor. 9.7 of Forty Points) | generalised CP: Ω ↦ −Ω̄, the multiplier −1 element diag(I, −I) of GSp(4,ℤ) |
| a tensor factorisation (45 of them) | a splitting A = E₁ × E₂ (Ω diagonal in a level-3 frame) |
| product state | factorised torus |
| Hesse P⁴ (Pass 11651), Burkhardt quartic (Pass 11657) | moduli of Coble cubics; Burkhardt ≈ Satake compactification of A₂(3) (Freitag–Salvati Manni) |
| 40 points / 40 lines of W(3,3) | the 1-dim / 0-dim cusps of A₂(3)* (isotropic lines / planes of F₃⁴; standard Satake theory, not computed here) |

## Results

### 11869: the Siegel generators act exactly as the Clifford group

All of the following hold to 3·10⁻¹⁵ on 12 random moduli Ω:
* **S** acts as F⊗F with factor √det(−iΩ).
* **The off-diagonal shear** acts as CZ₃.
* **The diagonal shift by 2** acts as the qutrit phase gate.
* **Exchanging the tori** acts as SWAP.
* **Ω ↦ −Ω̄** acts as complex conjugation.

**Group orders.**
* The four generators reduce mod 3 to a group of order **51840 = |Sp(4,3)|**.
* On the 40 points of W(3,3) they act as **PSp(4,3)** (order 25920).
* Adding diag(I, −I), the CP element of multiplier −1, gives **PGSp(4,3) = W(E₆)** (order 51840).
* That element preserves W(3,3) collinearity.

So **Aut W(3,3) is the level-3 Siegel modular group extended by generalised CP.**

### 11870 (genus one): the qutrit arrow is the modular CP sign

**The identity.** For ψ(τ) = (θ[c/3,0](0, 3τ))_c, the Hesse cubic through ψ is the elliptic curve E_τ itself:
* j(E_ψ(τ)) = j(τ), to a relative error of 3·10⁻¹⁵ over 30 moduli.

**What it implies.**
* Pass 11645 proved sign W(ψ) = sign Im j(E_ψ), where W is the corpus's time-arrow invariant of a qutrit state.
* Combined with the identity above, **the arrow of a theta-null state is sign Im j(τ)**.
* Generalised CP is τ ↦ −τ̄, i.e. ψ ↦ ψ̄.

**Check against modular-flavour CP.** In modular-flavour models CP is conserved exactly on the locus where j(τ) is real
(Novichkov–Penedo–Petcov–Titov 2019).
* We checked Im j = 0 to 10⁻¹⁵ on Re τ = 0, Re τ = ±½ and |τ| = 1.
* Off that locus, |Im j|/|j| ≥ 0.24.

Hence **the corpus's intrinsic one-qutrit arrow of time is the CP-violating order parameter of the elliptic modulus.**

### 11871 (genus two): theta-null states are Coble singular points on the Burkhardt quartic

Write the five Heisenberg-invariant cubics of Pass 11651 as Σ k_i T_i(x,x,x).

**Theta-null states.** For every theta-null state, the 9×5 gradient matrix at x = ψ(Ω) has a kernel:
* smallest relative singular value ≤ 1.2·10⁻¹⁶;
* so ψ(Ω) is a singular point of a unique Heisenberg-invariant cubic, **the Coble cubic** of A.

**Control.** No random even two-qutrit state has such a cubic: smallest relative singular value ≥ 0.027.

**On the Burkhardt quartic.** The Coble coefficient vector k(Ω) lies on the Burkhardt quartic I₄ of Pass 11657:
* |I₄(k)| ≤ 4·10⁻¹⁵ for theta-null states;
* |I₄| ≥ 0.72 for random points;
* I₄ is the Reynolds quartic over the order-103680 group of Pass 11657.

This is the genus-2 lift of 11870. The two-qutrit Hesse space of Passes 11651–11659 is the space of Coble cubics. Its
Burkhardt hypersurface is the image of the moduli space.

The mathematics is classical (Coble 1917; Gruson–Sam–Weyman 2013; Hunt). The reading in qutrit terms is new.

### 11872: product ⟺ factorised torus; Schmidt spectrum (1, ε, ε²)

**Product states.** Reshape ψ(Ω) as a 3×3 matrix M_{c₁c₂}.
* It has rank 1 exactly when Ω₁₂ = 0 (σ₂/σ₁ ≤ 4·10⁻¹⁷).
* So **the qutrit tensor factorisation is the factorisation of the torus.**

**The spectrum near a factorised torus.** The singular values scale as (1, ε, ε²), with ε ∝ |Ω₁₂|:
* log-slopes 1.0000 and 2.0000 in three random base points;
* σ₁σ₃/σ₂² = 4.4, 4.3 and 5.4 there, so this ratio depends on (τ₁, τ₂).

**Physical reading, as hosting.**
* On a magnetized T² × T² with flux 3, the Yukawa matrix is a product of one-torus thetas: rank 1, one heavy
  generation (cf. Pass 235's democratic rank-1 Yukawa).
* The non-factorisable modulus Ω₁₂ lifts this to a three-generation Froggatt–Nielsen texture, with the "flavon" being
  geometry.
* This is a generic Taylor-expansion fact for analytic kernels. Antoniadis–Kumar–Panda 2009 treat non-factorisable
  magnetized Yukawas in general. It is not claimed as new.

## 11873: what the two papers contain (reading ledger)

**w33_paper.pdf, pp. 401–790 (physics parts and supplements).** Classified sentence by sentence while reading.

*Numerology, no mechanism:*
* α⁻¹ = 137 and its corrections;
* sin²θ_W = 3/13 + α/11;
* the PMNS angles 4/13, 7/13, 2/91;
* the quark ratio chain;
* Koide = (q−1)/q;
* H₀ = 67 / 70, n_s = 29/30, Λ exponent −122;
* "all 19 SM parameters";
* the Monster/Leech integers;
* "q^q = q³" (it imposes v−k−1 = 27 by hand).

The Forty Points paper's "what we do not count as evidence" is the right verdict on all of these.

*Wrong or fabricated as stated:*
* the Part XXIII β-coefficients;
* "Griess algebra = Sp(4,3) centraliser";
* the amplituhedron, c = 20 CFT, [[120,20,4]]₃ and "Golay from A mod 2" claims;
* "dim M = 4 forced by KO-dim 6", since KO-dim 6 is a choice of J-signs;
* the heterotic-on-K3 dictionary: heterotic on K3 is six-dimensional.

*Real mathematics:*
* the Ihara/Hashimoto explicit formula, and the W(3,3)/Q(4,3) Sunada pair (same zeta, different critical groups);
* the binary codes [40,16,8] / [40,24,6];
* the uniserial F₂⁴⁰ module 1|14|1|8|1|14|1, with its SO(10) and E₈ shadows;
* the eigen- and trade lattices, with 480/90 minimal shells;
* the canonical E₈ lift via the plus-type form;
* the golden-selector transport (a non-split Heisenberg packet);
* the Burkhardt/Schläfli 40/27/45/36 shells (Supp. ω);
* the q-towers;
* the chirality no-go (Pass 346).

**The pages before p. 414 that matter physically (pp. 391–400):**
* the controlled-determinant compiler;
* S₃ = ⟨z, s⟩ ≅ Konopka's non-abelian heterotic S₃ orbifold, at representation level;
* the flagship order-3 Wilson line = CZ₃ class, with the SU(5) on the zero-phase cross {xy = 0} (79.81);
* the E₈ inner lift of the holonomy pair, D₄+A₃+u₁ → A₂+A₁+u₁⁵ with the A₈ selector (79.83–86).

**Forty Points** (all sections reread; sec09 in full):
* exact structure and hosting, with honest closures;
* the heterotic orbifold route is exhausted across nine families;
* masses, mixing and gravity are OPEN;
* chirality is a NO-GO from inside.

**What the reading changes.** The open items are exactly those that a modulus would supply:
* a vacuum value ⟨Ω⟩ is the "outside datum" that the chirality no-go demands, and it breaks generalised CP;
* modular forms evaluated at ⟨Ω⟩ give Yukawas;
* the distance from a symmetric point gives hierarchies.

11869–11872 show that the corpus's finite objects *are* that modulus's level-3 structure:
* the Paulis, the Clifford group and W(3,3);
* the antiunitary arrow/chirality coset;
* the 45 factorisations;
* the Hesse/Burkhardt space.

**The evolved programme.** Treat W(3,3) as a level-3 Siegel modular flavour/moduli theory, Γ₂,₃ ⋊ CP = Sp(4,3)·2, on a
T⁴ factor. The natural strings for this are magnetized or intersecting-brane compactifications, not the cyclic heterotic
orbifolds (closed, Forty Points §9). The concrete next steps:
1. Fixed points of Γ₂,₃ on H₂ and their residual symmetries.
2. Weight-k level-3 Siegel forms decomposed into the Weil 4 ⊕ 5. The weight-½ even thetas carry the 5 (Rac), the odd
   theta derivatives the 4 (Di). These are the singletons of the finite AdS₄ passes 11831–11837.
3. A three-generation model near a factorised point, with CP broken by Re Ω.
4. Moduli stabilisation on A₂(3).

## Scope

* **Not done here:** no moduli stabilisation, no fit to masses or mixing, and no string model.
* **Identified only as conjugacy classes:** the CZ₃ ↔ shear and CZ₃ ↔ flagship Wilson line identifications. No map
  from the heterotic gauge holonomy to the T⁴ modular group is claimed.
* **Standard theory, not computed:** the cusp statement in the dictionary.
* **Exact to floating-point:** 11869–11872 (10⁻¹⁵), with controls for every positive. The group orders are exact
  (integer closure and sympy).

## Prior art

* **Mathematics:**
  * Mumford (theta groups);
  * Coble (1917);
  * Hunt, *The Geometry of some special Arithmetic Quotients* (Burkhardt);
  * Freitag–Salvati Manni, Transformation Groups 9 (2004);
  * Gruson–Sam–Weyman (2013).
* **Physics:**
  * Ding–Feruglio–Liu, arXiv:2010.07952 and 2102.06716 (symplectic modular invariance, CP);
  * Novichkov–Penedo–Petcov–Titov (2019, CP in modular models);
  * Carducci–Meloni–Parriciatu–Penedo, arXiv:2604.21979;
  * Kikuchi–Kobayashi–Nasu–Takada–Uchida, arXiv:2211.07813;
  * Antoniadis–Kumar–Panda, arXiv:0904.0910;
  * Konopka (non-abelian heterotic S₃).
* **Corpus:**
  * Passes 11641/11645 (Hesse CP, sign W = sign Im j);
  * 11651/11657/11659 (Hesse space, Burkhardt, nodes = determinants);
  * 11177 (factorisations);
  * 346 and Forty Points Cor. 9.7 (one antiunitary coset);
  * w33_paper §79.79–79.81.
