# Pass 12682: orbit minima identified (a second Q(cos 2π/9) level); the orbit-A symmetry is a diagonal SL(2,8) with Ree-unital orbits; a symmetry-reduced degree-8 SOS on 16-dimensional code spaces

Claude track. Follows Pass 12681. **Not a theory of everything.**

## 1. Minima of the 17 orbit code spaces, at 32 digits (`w33_f8_orbit_levels_identify.py`)

For the 13 orbits whose code spaces do not attain c₈, each minimum was polished by 40-digit mpmath Newton in the effective four-qubit model (gradients ≤ 10⁻³⁹).

| orbit (type) | minimum | identification |
|---|---|---|
| 2, 12 (control) | 2.74108998535534750026 | root of 13c³ − 265c² + 1447c − 2243 (Pass 12672) ✓ |
| **15** ({1: 135}, \|Stab\| 504) | **2.76998179276121463447** | **(87 − 16γ − 16γ²)/9, γ = 2cos(2π/9)**: root of 243c³ − 4455c² + 24921c − 40013 |
| 8, 13 | 3 | stabiliser value |
| 16 | 7 | rational |
| 1, 6, 5 = 10, 3, 0, 7 | 2.7318227568, 2.8094922052, 2.8123447618, 2.8481957611, 2.8634243626, 2.9454579104 | not identified (degree ≤ 8, coefficients ≤ 10⁶) |

The second orbit whose stabiliser has order 504 (orbit 15) has its minimum in the same cubic field Q(cos 2π/9) as c₈, with denominator 9.

## 2. The orbit-A symmetry is a diagonal SL(2,8) (`w33_f8_orbitA_symmetry.py`)

- The stabiliser of S_A in H has **order 504**, with element orders {1: 1, 2: 63, 3: 56, 7: 216, 9: 168}, exactly the profile of SL(2,8) ≅ PSL(2,8).
- Both projections to the SL(2,8) factors are injective, so it is a graph subgroup {(g, φ(g))}. No Frobenius is involved.
- **Its orbits on the effective phase space S_A^⊥/S_A = F₂⁸** are 1 + 28 + 28 + 36 + 36 + 63 + 63. All 63 weight-1 points form one orbit and all 36 weight-2 points another; one nonzero point is fixed.
- The two 28-point orbits match the classical 2-transitive action of PSL(2,8) ≅ ²G₂(3)′ on the 28 points of the Ree unital.

## 3. A symmetry-reduced degree-8 SOS (`w33_f8_symmetric_sos8.py`)

The construction:
1. **Pauli-character blocks.** Degree-4 monomials (charges 4, 2, 0) split into Pauli-character blocks labelled w ∈ F₂^{2n}. The code space's symmetry group G acts on the labels by w ↦ S_h w for blocks with an even number of conjugate copies. For charge 2 (one conjugate copy) the action is **affine**, w ↦ S_h(w + t_h): complex conjugation of the Hermitian Pauli images adds the sign (−1)^{q(Sp) + q(p)}, which is linear in p. Only this placement of the twist is a group action, checked by orbit counts.
2. **Representatives and commutants.** One block per label orbit. On it the Gram matrix ranges over the commutant of the stabiliser H_w, whose action is fitted from samples. The residual is ≤ 10⁻¹⁴, certifying that each block is invariant.
3. **Isotypic splitting.** The commutant is split into blocks (unitarise with the invariant form K = ⟨RᴴR⟩, then use eigenspaces of a generic group-algebra element and equivalence via the commutant), giving the M_m ⊗ I_d structure.
4. **Sampled identity.** The invariant SOS is s(ψ) = |G|⁻¹ Σ_g Σ_w b_w(U_gψ)ᴴ Y_w b_w(U_gψ). The identity s + c = c_eff on the sphere is imposed at random points until the rank saturates, then checked at fresh points.

**Validation on the T code space** (8-dimensional, D₉ symmetry; known Pauli-only degree-8 value 2.4985086841, Pass 12674):

| version | variables | cones (max) | bound | identity error |
|---|---|---|---|---|
| first (charge-2 twist missing) | 3,253 | 24 (72) | 2.4985086504 | 1.7×10⁻⁸ (block residual 0.77; still a valid but possibly lossy family) |
| twist fixed, full commutant | 3,253 | 24 (72) | 2.4985085945 | 5.5×10⁻⁸ |
| twist fixed, isotypic split | 2,419 | 69 (24) | **2.4985086252** | 2.3×10⁻⁸ |

All agree with c₈ to within the identity error.

**Orbit A (16-dimensional, symmetry 504).**
- The label orbits are consistent: 256 = 1 + 36 + 63 + 28 + 63 + 28 + 36 + 1 for even charges, and 4·36 + 4·28 for charge 2.
- There are 24 representative blocks (the largest of size 136), commutant dimension 4,573, and the invariant identities have rank 151.
- After the isotypic split the SDP has 290 cones (largest 32) and 5.7×10⁶ nonzeros, against about 2×10⁶ pair variables for the Pauli-only formulation.
- The SCS solve is running at the time of this commit; the result is reported in an addendum.

## Parallel work (other track, 2026-11-16)

- `8f8467de2` / `a9ae33bd4`: a rank-five isotropic subgroup with all 31 non-identity elements uncovered gives **mixed** states with every covered Pauli expectation zero for every purity 1/64 ≤ p ≤ 1/2, so the global mixed-state minimum is 0 on that range. They use it for measurement-restricted data hiding.
- This complements, and does not overlap, the pure-state results here. Like this pass, they state that the global pure-state c₈ bound is still open.
