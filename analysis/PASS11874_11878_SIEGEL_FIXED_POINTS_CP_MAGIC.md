# Passes 11874–11878: fixed points, Weil 5+4, the hierarchy law, magic, and genus-2 CP of the level-3 modulus

Producer: `analysis/w33_pass11874_11878_siegel_fixed_points_cp_magic.py`
Certificate: `data/w33_pass11874_11878_siegel_fixed_points_cp_magic.json` (16/16 checks)
Regression: `tests/test_w33_pass11874_11878.py`
Track: Claude.

This pass follows up Passes 11869–11873. Those passes showed that W(3,3) is the level-3 structure of a genus-2 modulus Ω.
Their dictionary is:
* two qutrits = the level-3 theta functions;
* Clifford group = the Siegel modular group;
* W(E₆) = Γ₂,₃ extended by CP.

ψ(Ω)_c = θ[c/3,0](0,3Ω) is the theta-null state. The five next steps of that note are executed here.

## 11874: the six isolated fixed points: residual symmetry, CP, Yukawa rank

**How they were found.** I searched the companion matrices of Φ₅, Φ₈ and Φ₁₂ (and the products Φ₃Φ₆ and Φ₃Φ₄) over their
invariant unimodular symplectic forms, solved γΩ = Ω, and Siegel-reduced. This recovers Gottschling's six points; the
x⁶−1 point was then identified by its stabiliser.

**How the stabilisers were computed.** Exactly, as automorphism groups of the polarised lattice: integer M with
MᵀSM = S that commute with the complex structure.

| point | Ω | stabiliser | orbits on the 40 points of W(3,3) | Yukawa ψ as 3×3 (σ₂/σ₁, σ₃/σ₁) | magic M₂ |
|---|---|---|---|---|---|
| y² = x⁵ − 1 | Z₅ point | 10 | 5⁸ | 0.235, 0.160 | 1.162 |
| y² = x⁶ − 1 | (i/√3)(2 1; 1 2) | 24 | 2,2 (isotropic pairs), 6⁴, 12 | 0.185, 0.132 | 1.005 |
| E_i × E_ρ | diag(i, ρ) | 24 | **1** (a fixed point of W(3,3)), 2, 2, 3, 4, 4, 12, 12 | **rank 1** | 1.040 |
| E_i × E_i | iI | 32 | 4, 4, 8, 8, 16 | **rank 1** | 0.940 |
| Bolza y² = x⁵ − x | ((1+2√2i)/3, (−1+√2i)/3; …) | 48 | **two isotropic lines** (two contexts), 8, 12, 12 | 0.293, 0.138 | 1.223 |
| E_ρ × E_ρ | ρI | 72 | 2,2 (isotropic pairs), 6, 12, 18 | **rank 1** | 1.141 |

**Embedding.** Every stabiliser injects into Sp(4,3) (Γ(3) is torsion-free). So the residual flavour groups are
subgroups of Aut W(3,3), and the orbit column says what each fixes in W(3,3).

**CP.** **Every fixed point is CP-conserving.** For each one there are exact lattice isomorphisms Ω → −Ω̄, as many as
the stabiliser order. This agrees with the literature statement (Carducci et al. 2026) that the zero-dimensional fixed
points are CP-conserving.

**Physics.** The symmetric vacua are of two kinds:
* **Products** (E_i², E_ρ², E_i×E_ρ): the theta-null is a product state, so the 3×3 texture has **rank 1**, one heavy
  generation.
* **Jacobians** of smooth curves: rank 3 with O(0.1–0.3) ratios, i.e. **no hierarchy**.

So hierarchies need the vacuum *near a product point*: the "modular proximity" mechanism with ε = Ω₁₂ (11876). CP
violation needs it off the CP locus (11878).

## 11875: Rac = theta-nulls (weight ½), Di = odd gradients (det^{½} ⊗ std)

**Spans.** The theta-nulls span exactly the even Weil 5. The z-gradients of the odd theta functions span exactly the
odd 4. Both are irreducible: commutant dimension 1 under the Clifford generators.

**Transformation law.** S acts on the gradients as

  G(−Ω⁻¹) = √det(−iΩ) (F⊗F) G(Ω) (−Ω),

to 2·10⁻¹⁵, with the right factor exactly −Ω.

**Reading.** The finite-AdS₄ singletons of Passes 11834–11837 are modular forms:
* Rac is scalar, of weight ½;
* Di carries an extra holomorphic index: the cotangent space of T⁴, i.e. a Weyl spinor of the internal SO(4) under its
  U(2) holonomy. This matches Di being the spinorial singleton.

## 11876: the hierarchy law, and one modulus for all sectors is excluded

**The law.** Near a factorised torus the Schmidt values are (1, ε, ε²) with ε ∝ Ω₁₂. The leading shape invariant is
exact:

  σ₁σ₃/σ₂² = r(τ₁) r(τ₂) / 2,   r(τ) = |g₀ ∧ g₂| / |g₁|²,  g_k(c) = Σ_n (n+c/3)^k e^{3πiτ(n+c/3)²},

* **Agreement:** relative error ≤ 1.2·10⁻⁸ at Ω₁₂ = 10⁻⁴.
* **Symmetry:** r is invariant under S and T² (the theta group), but not under T, which changes the spin structure.
* **Range:** r runs over (0, ∞). It goes to 0 at the cusp τ → 1 and to ∞ at i∞.
* **Exact values:** r(1+i) = √2 and r(1+i/2) = 3 − 2√2.

A corrected algebra slip: an earlier draft dropped a factor σ₁.

**The universality test.** With one modulus and one characteristic for all fermion sectors, both R = σ₁σ₃/σ₂² and
σ₂/σ₁ would be sector-universal. At M_Z (Xing–Zhang–Zhou masses):

| sector | R | σ₂/σ₁ |
|---|---|---|
| up | 0.569 | 0.0036 |
| down | 2.77 | 0.019 |
| charged lepton | 0.081 | 0.059 |

The spreads are factors of 34 and 16. **One (modulus, characteristic) for all sectors is excluded.** Each sector can be
accommodated separately, but that predicts nothing. What remains open is sector-dependent levels or characteristics,
which is exactly what magnetized fluxes supply.

## 11877: magic is a modular function with no interior maximum

The stabiliser 2-Rényi magic M₂(ψ(Ω)) behaves as follows:
* it is invariant under S, the shear and CP to 10⁻¹⁵;
* it is ≈ 0 at the cusp i∞, where ψ → |00⟩.

**Where the supremum sits.** In one qutrit, as τ → 1 (the other cusp of the theta group), ψ(τ) tends to the
maximal-magic qutrit state (2e^{−iπ/3}, 1, 1)/√6:
* M₂ → log 2 to 10⁻¹⁵;
* a grid scan finds no larger value;
* the two-qutrit supremum is log 4, at doubly degenerate factorised cusps.

The first optimisation runs appeared to find an interior maximum at log 4. That was a ridge into a cusp: the Hessian had
positive directions and the points reduced to diagonal Ω. It is recorded here as a corrected reading.

**Consequence.** "Maximal magic" does not stabilise the modulus. It runs to a degeneration, like a string-moduli runaway.
Interior values at the fixed points are 0.94–1.22.

## 11878: the genus-2 CP order parameter (the two-qutrit arrow)

Three ratios of Burkhardt-group invariants of the Coble point k(Ω) were built, of degrees 12, 16, 20 and 24, Reynolds
over the order-103680 group with real linear forms. They:
* are invariant under the **full** Sp(4,ℤ) (S, the shear, Ω₁₁+2, swap, and also T₁ and S₁ outside the theta group;
  ≤ 1.5·10⁻¹³), so they are **level-1 Siegel modular functions**, intrinsic to the abelian surface (Igusa-type);
* go to their complex conjugates under Ω ↦ −Ω̄;
* are real on the CP-conserving moduli (pure imaginary Ω, or integer real part: ≤ 10⁻¹³);
* are complex generically (|Im J|/|J| = 0.86).

This is the genus-2 lift of 11870's sign W = sign Im j(τ).

**Composition of arrows.** Take diag(τ, −τ̄) plus a CP-even off-diagonal: two tori with opposite one-qutrit arrows. The
result is CP-conserving (10⁻¹²). With equal arrows, or one CP-violating factor, it is not (0.057, 0.12).

**Degeneracies.** At special points the invariants vanish and the ratios are 0/0:
* at the Z₅ point several invariants vanish, like j = 0 at ρ;
* the product points sit at Burkhardt nodes.

There the exact lattice-isomorphism test of 11874 replaces the ratio test. An early run read rounding noise at the Z₅
point as CP violation; it is recorded as corrected.

## What this changes

The level-3 Siegel reading now has its whole symmetric skeleton computed:
* six CP-conserving fixed points with residual subgroups of Aut W(3,3);
* products give one heavy generation;
* Jacobians give no hierarchy.

It also has two exact tools:
* the hierarchy law R = r₁r₂/2;
* a modular CP order parameter.

It has two firm negatives:
* one modulus with one characteristic cannot serve all fermion sectors;
* magic does not stabilise the modulus.

**The next concrete step** is a sector-dependent-level model: magnetized fluxes M_u, M_d, M_e, i.e. level-M theta
functions, on one Ω. There R_sector = r_M(τ₁) r_M(τ₂)/2 becomes three predictions from one modulus.

## Prior art

* Gottschling (1961), the isolated fixed points of Sp(4,ℤ).
* Bolza's curve and its period matrix.
* Carducci–Meloni–Parriciatu–Penedo (arXiv:2604.21979): CP at fixed points, modular proximity hierarchies.
* Novichkov–Penedo–Petcov (hierarchies near fixed points).
* Leone–Oliviero–Hamma (stabiliser Rényi entropy).
* Freitag–Salvati Manni (Burkhardt invariants, Satake A₂(3)).
* Corpus: Passes 11869–11873, 11645, 11657/11659, 11834–11837 (Di/Rac), 11651 (Hesse space).
* Masses: Xing–Zhang–Zhou, PRD 77 (2008) 113016.

## Cross-track (TOE Round 38, commit a50a847, read after this pass was pushed)

* **Who owns the determinant law.** Round 38 Track B independently derived the leading determinant law
  det Θ(ε) = (6πi)³ε³/2 · det[u₀,u₁,u₂] · det[v₀,v₁,v₂]. Its commit is earlier, so it owns that piece.
  * The shape law σ₁σ₃/σ₂² = r(τ₁)r(τ₂)/2 here combines it with the 2×2-compound term σ₁σ₂ ≈ |ε'|·|g₀∧g₁|·|h₀∧h₁|.
  * Because g₁ is odd and g₀, g₂ are even, the τ-dependence reduces to r = |g₀∧g₂|/|g₁|².
* **A framing caveat that applies here.** Round 38 also proves that Schmidt data are frame-dependent: the CZ shear maps a
  product point to a rank-3 one.
  * So 11874's "rank one at product points" and 11876's universality test are statements about a *marked* tensor
    splitting. In a magnetized T²×T² realisation, that is the physical left/right zero-mode assignment.
  * They are not modular invariants.
* **What is frame-free.** The magic (11877) and the CP order parameters (11878) are modular invariants. 11878 is a
  frame-free, CP-odd, level-one modular observable of the genus-2 modulus, which is the object Round 38's
  hypothesis 2 asks for.
