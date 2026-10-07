# Pass 11641 — the Hesse CP order parameter of a qutrit state is the Vandermonde of its four MUB triple products

Producer: `analysis/w33_pass11641_hesse_cp_is_mub_vandermonde.py`
Certificate: `data/w33_pass11641_hesse_cp_is_mub_vandermonde.json`
Regression: `tests/test_w33_pass11641_11646.py`

## The Hesse doublet is the Clifford quotient of a qutrit state

**The map.** Let ψ be a qutrit state. Project ψ⊗ψ⊗ψ onto the Hesse pencil inside Sym³(C³). Pass 11600 spans the
pencil by two orthonormalised tensors: the diagonal tensor (norm² 3) and the all-distinct tensor (norm² 6). This gives

  u(ψ) = Bᵀψ^{⊗3} = ( (ψ₀³ + ψ₁³ + ψ₂³)/√3 ,  √6 ψ₀ψ₁ψ₂ ).

**Equivariance.** For every one-qutrit Clifford g, g^{⊗3}B = B R(g), so u(gψ) = R(g)u(ψ). Since B is real,
u(ψ̄) = ū(ψ). The exact checks in the certificate are:

| object | value |
|---|---|
| R(Fourier) | **= Pass 11600's `normalized_F`** (symbolic identity) |
| R(phase gate diag(1,1,ω)) | **= Pass 11600's `normalized_P` = diag(1, ω)** |
| R(X), R(Z) | identity (the Heisenberg kernel of G216 → A4) |
| Bloch actions in Pass 11600's tetrahedral axes | match `Bloch_F`, `Bloch_P` (10/10) |

So the Hesse doublet field of Passes 11600–11614 is exactly the pencil map P² ⇢ P¹ of a family qutrit, and its
"coefficient CP" is complex conjugation of the state.
* The pencil map is classical: Artebani–Dolgachev; Hughston 2007 (cited in Pass 11269).
* Codex's Pass 11627 already has a degree-2 Clifford intertwiner and the MUB ↔ tetrahedron pairing.
* The objectwise identification with the 11600 matrices is new here.

**Convention found here.** Pass 11600's stored `Bloch_axes` are *columns*: n = Tᵀr. With rows, no action matches.

## The theorem (exact, symbolic in ψ)

Let Π_b = ∏_{s∈b} |⟨s|ψ⟩|² be the **triple product** of MUB b, for b = Z, X, XZ, XZ². The images of the four MUBs
are the cube vertices (1,1,1)/√3, (1,−1,−1)/√3, (−1,1,−1)/√3 and (−1,−1,1)/√3, written m_b, in Pass 11600's own axes.
Every state of one MUB maps to the same vertex. Then:

> ρ = |u|² = 3 Σ_b Π_b ,   r = −9 Σ_b Π_b m_b .

* **Proof idea.** For the Z basis, |u₁|² = 6|ψ₀ψ₁ψ₂|² = 6Π_Z, so m_Z·r = ρ − 12Π_Z. Clifford covariance transports
  this to each vertex, and the four tetrahedral projections determine r.
* **Verification.** The producer verifies both identities symbolically, by polynomial expansion in the six real
  coordinates of ψ (no normalisation assumed).
* **Reading.** The Hesse doublet's Bloch data **are** the four MUB triple products, linearly.

### Consequences (all exact)

1. **A cone identity for every pure qutrit state:** (Σ_b Π_b)² = 3 Σ_b Π_b². This is |r| = ρ.
2. **The doublet norm is a stabiliser moment:** ρ = M₃ − M₁³, where M_k = Σ_s |⟨s|ψ⟩|^{2k} is Pass 11534's moment over
   the 12 stabiliser states.
3. **A magic bound:** 0 ≤ ρ ≤ 1/3.
   * **ρ = 1/3 holds exactly on the 12 stabiliser states.** On the cone, max_b Π_b ≥ ΣΠ/3, and each Π_b ≤ 1/27 by
     AM–GM. So ΣΠ ≤ 1/9, with equality only for Π = (0, 1/27, 1/27, 1/27). The purity sum rule Σ_b P2_b = 2 then
     forces a basis state.
   * **ρ = 0 holds exactly on the nine Hesse SIC ("strange") states,** the base points of the pencil.
   * The T-magic state T|+⟩ = (1, ζ₉, ζ₉⁻¹)/√3 has ρ = 2/9. It sits exactly at **−m_Z**, the antipode of the Z vertex,
     with Π = (3,1,1,1)/81. Its fibre is the Fermat cubic x³ + y³ + z³ = 0, the equianharmonic member.
4. **Pass 11600's CP-odd discriminant is a Vandermonde:**

   > W = (x² − y²)(y² − z²)(z² − x²) = **−108³ ∏_{a<b} (Π_a − Π_b)** = −1 259 712 V(Π).

   The constant is computed in Pass 11600's own axes, with the MUBs ordered Z, X, XZ, XZ². The CP-even pieces are the
   symmetric functions of the Π_b:
   * xyz = −81√3 ∏ over the three pairings of (Π_a + Π_b − Π_c − Π_d), the resolvent cubic;
   * Pass 11614's W² is the discriminant of the quartic ∏(t − Π_b).
5. **CP sign = parity of the MUB ordering.** Unitary Cliffords permute the MUBs by A4: Fourier acts as (Z X)(XZ XZ²),
   and the phase gate as (X XZ XZ²). Complex conjugation swaps XZ ↔ XZ², an odd permutation. It flips sign W on
   2000/2000 random states. Hence:
   * **Pass 11614's 24 Weyl chambers are the 24 strict orderings of the four MUBs by their triple products.**
   * Its walls are the ties Π_a = Π_b.
   * The CP sign is the sign of the ordering permutation.
6. **Pass 11600's vacua are on the stabiliser side.**
   * The MUB vertices all have xyz > 0, and Pass 11600's vacuum potential pins xyz > 0.
   * The canonical vacuum ray (1,2,3)/√14 has Π/ρ = (0.0062, 0.1348, 0.1091, 1/12) for (Z, X, XZ, XZ²). So its MUB
     order is **X > XZ > XZ² > Z**.
   * It is realised by explicit qutrit states ψ = (1, 1, t), with t a root of u₁t³ − 3√2u₀t + 2u₁ = 0. For example,
     t = −1.1626 − 4.4681i gives ρ = 0.2721.

## Reading

**Composite reading.** If the flavour CP field of Passes 11600–11614 is the pencil shadow of a family-qutrit state
(Φ = Bu(ψ)), then the following become statements about four measured numbers, the MUB triple-coincidence
probabilities:
* the Weyl-selecting sign (Pass 11607);
* the E8 shell bit (Pass 11609);
* the CP-witness sign (Pass 11611).

**Physical content of the sign.** The sign records which of the four complementary measurements is most balanced,
which next, and so on. Time reversal reverses that order's parity, because it swaps two bases.

**Scope.**
* This is an exact algebraic identity on the qutrit state space.
* It does not derive that the flavour field *is* a composite of a family qutrit.
* It does not fix Pass 11600's potential or its target ratios (1,4,9)/14, which remain model data.

## Addendum (Pass 11651): prior art and the group

1. **Consequence 2 is a known structure.** The identity ρ = M₃ − M₁³ is the one-qutrit case of the
   Gross–Nezami–Walter description of the third tensor power of the Clifford group (arXiv:1712.08628). At two qutrits,
   |u|² = (M₃ − 2)/6 exactly (Pass 11651). Cite it as such.
2. **The doublet's group is Shephard–Todd G₆.** The linear group generated by R(Fourier) and R(phase) has order 48,
   with 6 reflections of order 2 and 8 of order 3. Its invariants have degrees 4 and 12, and j is their ratio.
3. **The linear triple-product law is special to n = 1.** It fails at n = 2 (Pass 11651).
