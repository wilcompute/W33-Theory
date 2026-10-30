# Passes 331–332: the Weil–integral chirality bridge

## Status

Two GAP certificates close the concrete module-map question left open by
Pass 170 and correct Pass 330's q=3 dichotomy:

- <code>analysis/w33_pass331_weil_chirality_lift_obstruction.g</code> — PASS 24/24.
- <code>analysis/w33_pass332_integral_halfspin_lift.g</code> — PASS 39/39.

The result is deliberately narrower than a physics derivation. It builds an
explicit characteristic-zero lift of the incidence module and the associated
complex half-spin representations. It does not choose a chirality, identify a
half-spinor with a physical generation, construct an integral spinor lattice,
or extend the lift from PSp(4,3) to PGSp(4,3).

## 1. Ownership

Pass 170 used the 2-modular decomposition matrix of
U₄(2) ≅ PSp(4,3) to show that the ordinary conjugate pair 5a+5b has the
same composition-factor multiset as

    H₁₀ = C⊥/C, with structure 1|8|1.

That pass explicitly stopped at composition factors: it did not determine the
extension class and did not construct a module isomorphism. BT866 later found
the same conjugate 5a+5b pair in the oriented H₂ carrier and its degree-10
fusion under U₄(2).2, but again supplied no integral reduction map to H₁₀.

The following ingredients are standard, not claimed here as new:

- the ATLAS 5a representation over Z[ω], including its uniserial 4a.1 reduction;
- the exterior-power identities for 5a;
- the realization of the two D₅ half-spinors on the even and odd exterior
  algebras of a maximal isotropic 5-space.

The repo-new object is the explicit stable-lattice switch and the simultaneous
generator intertwiners to the actual incidence H₁₀. A targeted primary-source
search did not locate that exact construction; this is not a global priority
claim.

## 2. Pass 331: the scalar obstruction is real

Let H₈ = ker(A₂)/im(A₂) be the central binary shadow. GAP computes

    End_PSp(H₈) ≅ F₄.

Over F₄, H₈ splits as two nonisomorphic, absolutely irreducible,
Frobenius-conjugate and mutually dual modules:

    H₈ tensor_F₂ F₄ = 4a ⊕ 4b, with 4b ≅ 4a*.

Their transvection values are the q=3 Weil pair

    (-1 ± 3 sqrt(-3))/2.

Thus Pass 330's inference “End = F4 implies achiral” is false. Two arithmetic
clocks must be kept separate:

- q mod 8 controls separate F₂ descent versus one F₂ Galois fusion;
- q mod 4 controls self-duality versus a mutually dual pair on the tested Weil
  anchors.

The outer controller from Pass 211 acts on H₈ by the exact Frobenius rule

    t⁻¹ ω t = ω² = ω+1,

and therefore End_PGSp(H₈) = F₂.

The complete logical module behaves differently. GAP computes

    End_PSp(H₁₀) = End_PGSp(H₁₀) ≅ F₂[ε]/(ε²),

where ε has rank one, im(ε) is the unique socle, and ker(ε) is the unique
9-dimensional radical. Its unit orders are 1 and 2, so no commuting root of
x²+x+1 exists. The central F₄ scalar cannot extend inside any individual H₁₀.

Independent Brauer-table restriction selects the actual U₄(2) < O₁₀⁺(2)
fusion:

    10 restricted to U₄(2) = 2·1 + 4a + 4b,
    16± restricted to U₄(2) = 2·1 + 4a + 4b + 6.

The ATLAS 32 for O₁₀⁺(2).2 restricts to two nonisomorphic irreducible 16s,
certifying that the D₅ graph automorphism exchanges the half-spin pair. This
does not yet identify that graph automorphism with the concrete Pass 211
controller on a common lifted module.

## 3. Pass 332: the obstruction is a polarization obstruction

Take the standardized ATLAS 5a over K=Q(ω), restrict scalars to Q, and let L be
the GAP-computed invariant integral lattice. Its reduction M=L/2L has submodule
dimensions

    0, 8, 9, 9, 9, 10

and composition profile 8+1+1. Hence M has a unique invariant 8-space H₈ and
exactly three invariant 9-spaces U₁,U₂,U₃, all containing it. They are precisely
the three lines of the 2-dimensional trivial head:

    0 → H₈ → M → F₂² → 0,
    {Uᵢ/H₈} = P¹(F₂).

For each Uᵢ, define the index-two stable preimage sublattice

    Lᵢ = {x in L : x mod 2L lies in Uᵢ}.

GAP builds the two standardized generator matrices on Lᵢ/2Lᵢ and the complete
simultaneous Hom space to the independently reconstructed incidence H₁₀. For
every i=1,2,3,

    dim Hom_U₄(2)(Lᵢ/2Lᵢ,H₁₀) = 2,
    possible Hom ranks = {0,1,10}.

An invertible Xᵢ therefore exists and satisfies Aᵢⱼ Xᵢ = Xᵢ Hⱼ for both
standard generators. Consequently

    Lᵢ/2Lᵢ ≅ H₁₀ for i=1,2,3.

The tilted uniserial structure is explained by

    0 → H₈ → Uᵢ → 1 → 0,
    0 → 2L/2Lᵢ ≅ 1 → Lᵢ/2Lᵢ → Uᵢ → 0,

which assemble to 1|8|1.

## 4. The lifts form an Eisenstein C₃ torsor

Multiplication by ω is integral on L, centralizes U₄(2), and has order three.
It fixes no chosen Lᵢ. GAP obtains the exact action

    (U₁,U₂,U₃) → (U₃,U₁,U₂),

the Singer 3-cycle on P¹(F₂). The apparent clash between Passes 331 and 332
therefore disappears:

- characteristic zero retains the Eisenstein scalar across the three-leaf
  stable-lattice star;
- choosing one leaf produces H₁₀ and breaks that scalar symmetry;
- one H₁₀ has only the dual-number commutant, while the family of its three
  integral lifts carries the C₃ action.

Chirality here is a torsor of integral polarizations, not an endomorphism of the
chosen binary logical module.

An outer lift satisfying t⁻¹ωt=ω⁻¹ would reflect this three-cycle and generate
C₃ semidirect C₂ ≅ S₃, not C₆. Raw coefficient conjugation does invert ω, but
GAP proves that it does not normalize the standardized 5a image. The S₃ outer
lift is therefore a precise open map, not a result of this packet.

## 5. Characteristic-zero half-spins

Over K, GAP constructs the split orthogonal vector module

    V = 5a ⊕ 5a*.

The standard exterior construction gives two 16-dimensional actions:

    S+ = exterior-even(5a) = 1 + 10a + 5b,
    S- = exterior-odd(5a)  = 5a + 10b + 1.

The witness checks the full exterior-power degree chain 1,5,10,10,5,1,
image order 25920 for each half-spin action, nonisomorphism, complex conjugacy,
and a nondegenerate invariant wedge pairing between S+ and S-.

This closes Pass 170's module-lift/extension-class obstruction and realizes the
associated characteristic-zero D₅ half-spin pair. Pass 331's scalar obstruction
remains true on every individual binary H₁₀.

## 6. Form-level boundary

The module lift is not yet a quadratic-isometric lattice lift. The transported
H₁₀ polar form is alternating and plus type, with 528 isotropic vectors. The
primitive invariant rational form on L has determinant 62208; after the
index-two switch and halving, each integral form has determinant

    243 = 3⁵

and is odd modulo two. GAP checks this mismatch explicitly. No integral
Clifford or half-spin lattice is asserted.

## 7. Reproduction

    gap -q analysis/w33_pass331_weil_chirality_lift_obstruction.g
    gap -q analysis/w33_pass332_integral_halfspin_lift.g
    python3 -m pytest -q tests/test_pass331_gap_weil_chirality_lift_obstruction.py tests/test_pass332_gap_integral_halfspin_lift.py

Generated certificates:

- <code>data/w33_pass331_weil_chirality_lift_obstruction.json</code>
- <code>data/w33_pass332_integral_halfspin_lift.json</code>

## Primary anchors

- [ATLAS U₄(2) representation page](https://brauer.maths.qmul.ac.uk/Atlas/v3/clas/U42/)
- [ATLAS 5a over Z[ω]](https://brauer.maths.qmul.ac.uk/Atlas/v3/matrep/U42G1-Ar5aB0)
- [Szechtman, modular Weil representations](https://arxiv.org/abs/math/0212378)
- [Nebe, finite unitary group representations](https://www.math.rwth-aachen.de/~Gabriele.Nebe/papers/Unitary.pdf)
- [Baez–Huerta, exterior-algebra spinors](https://arxiv.org/abs/0904.1556)
