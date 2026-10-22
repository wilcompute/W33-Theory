# 2026-10-22 — Exact phinary, supergolden and W(3,q) dual-number clocks: arithmetic vs optics

**Release status:** finite-field theorems and executable no-go checks. These are not classical RH proofs or optical implementations. Prior work: \`analysis/w33_20261022_pascal_phinary_frobenius.py\`, \`analysis/w33_20261022_pascal_jordan_w3p.py\`, \`analysis/w33_20261022_six_algebra_optics_frontiers.py\`, \`analysis/w33_20261022_beta_ccm_sensitivity.py\`, the prior local p=3 Levi Frobenius bridge and the q=9 GF9 Bruhat–Tits work. Existing Chandler–Sin–Xiang incidence-rank literature gives complementary modular representation context.

## 1. Genuine linear conjugacy between golden and supergolden companions in characteristic 3

Let F=[[0,1],[1,1]] and S=[[0,0,1],[1,0,0],[0,1,1]]. Then modulo 3,

    x^3-x^2-1=(x+1)(x^2+x-1)
    charpoly(-F)=x^2+x-1.

Indeed, with

    Q=[[1,1,0],[2,1,2],[2,0,2]], det(Q)=2 mod3,

the exact equality S Q = Q [(-1) direct_sum (-F)] holds over F3. Hence the degree-3 supergolden module is one sign eigendirection plus one irreducible negative-golden degree-2 module. Since F^4=-I and F has order8 mod3, S also has order8. This *explains* the common order-eight observation of the previous script, instead of treating it as an independent coincidence.

Over F2, F has order3 and S has order7; over F7 they have orders16 and57. **This equivalence is special to characteristic 3** and says nothing about equality of the real Pisot numbers phi and psi.

## 2. Golden and Gaussian coordinates describe the same GF9

Use golden coordinates GF9=F3[phi]/(phi^2-phi-1), where phi^2=phi+1, phi^4=-1, phi^8=1; i=phi^2 gives a square root of -1. The Gaussian presentation F3[i]/(i^2+1) is explicitly isomorphic by

    a+b*i  -> (a+b)+b*phi  (coefficients modulo3).

The executable verifies the complete 9x9 addition and multiplication tables (162 equality checks), in addition to phi's exact multiplicative order8.

This is a genuine coefficient-ring isomorphism, not merely alternative decimal numeral notation.

## 3. W33 over F3: golden unit times a square-zero graph shear has exact order24

For the 40x40 W33 noncollinearity B=J-I-A reduced mod3, B^2=0 and rank B=10. Consequently, as a module over R=F9[epsilon]/epsilon^2, extending the W33 module from F3 to F9 gives

    F9^40 = R^10 direct_sum (F9)^20

(noncanonical decomposition; epsilon acts as B).

Let F be the 2D F3 golden companion. Its tensor with the unipotent graph factor yields an 80x80 F3 matrix X=F tensor (I+B). The golden factor has order8 and the unipotent factor has order3, so X has exact order24 (coprime 8 and3). Tests check X^24=I and X^12 != I and X^8 != I, with modular reduction after every multiplication to avoid integer overflow.

## 4. Native W(3,9) is the natural home of that arithmetic clock

W(3,9) has 820 projective vertices and its B has rank100, B²=0 in characteristic3. Since F9 already contains phi, this requires no external coefficient-field adjunction:

    U = phi*(I_820+B) in GL_820(F9), order exactly24.

B contributes a unipotent order-three element. The module splits (noncanonically) as R^100 + F9^620 over R=F9[epsilon]/epsilon². This native q9 algebra is the most direct physical-algebraic *analogy* uncovered.

An independent comparison reconstructs W(3,9) twice, once with golden irreducible polynomial x²-x-1 and once with Gaussian x²+1. The explicit coefficient change maps all 820 vertices and proves equality of the noncollinearity matrices up to their coordinate permutation. Their rank 100 is unchanged.

**Non-transfer to optics:** The literal integer/complex lift X_R=F tensor (I+B_real) has eigenvalue 28*phi≈45.30495, since B_real is a 27-regular graph adjacency. Therefore it is not unitary or finite order over C. Complex Hilbert-space representation of abstract C24 is possible, but would *not* be this graph operator.

## 5. Exceptional golden prime p=5 raises nilpotent Jordan depth to THREE

The golden polynomial ramifies mod5:

    x²-x-1=(x-3)².

Write F=3(I+N) mod5 with N²=0, rank N=1. On W(3,5), graph B²=0 and rank B=35 in 156 dimensions. Define the scaled 312D tensor product

    V = (I+N) tensor (I+B) = I+M.

Then

    M²=2(N tensor B) != 0,    M³=0.

Exact modular row elimination yields rank(M)=156 and rank(M²)=35. Thus the Jordan types of M are precisely:

    J3^35 direct_sum J2^86 direct_sum J1^35,

because #J3=rank M², #J2=rank M-2 rank M² and #J1=312-3#J3-2#J2. The unscaled tensor U=F tensor (I+B) has exact order20: scalar 3 has order4 and the nontrivial unipotent has order5. This is **not** a degree-two finite field obtained by adjoining golden phi: the golden algebra here is a nonreduced dual-number ring.

This ramified behavior distinguishes p=5 from the inert p=3 case, where phi is an order-eight element of a field and the graph supplies only one nilpotent layer.

## 6. A general number-base conditioned phase-order law (not physical time)

For any prime p != 5, the golden companion F modp is separable, its finite order h_p is coprime to p. In W(3,p^t), the nonzero square-zero graph operator B gives I+B order p. Therefore

    ord[F tensor (I+B)] = p*h_p   for p != 5.

Examples from certified companion-order census: p=2 ->6, p=3 ->24, p=7 ->112, p=11 ->110, p=13 ->364. At p=5 the golden factor itself contains a unipotent, and the coprimality argument fails; the explicit calculation gives order20 and Jordan length3.

This sharp characteristic dependence is an **obstruction** to interpreting the finite-field periods as a universal physical processor clock. Exact base changes preserve algebraic relations inside the same field, but reduction from characteristic zero to p changes the algebra and may introduce nilpotents.

## Connections, limits and falsification policy

- The Pascal no-carry formula rank_Fp(B)=binomial(p+2,3)^t already admits an independent exact q=3,4,8,9 certificate. Our new work adds a concrete hybrid coefficient-ring construction and ramified-prime Jordan analysis.
- The p=3 local supersingular Levi Bass transfer has an 8-step normalized period over a *characteristic-zero* weighted Hilbert space. Our native q9 golden–nilpotent operator has period24 in **characteristic 3**; there is no proven operator intertwiner between them.
- The earlier finite-prime CCM N=4 reproduction, smooth compact Weil 2x2 form, and rank-two trace coupling remain numerical / formally scoped. The 37 dark modes obstruct an unmodified full-Xi determinant. None of the golden-period coincidences repairs the missing global arithmetic trace formula.
- No physical photonic device or noise threshold has been built. A signed-mode permutation is an available abstract passive unitary surrogate but is not a unitary representation of the literal reduced W33 matrix.

## Reproduction

    OPENBLAS_NUM_THREADS=1 PYTHONPATH=. python -m pytest -q tests/test_w33_20261022_golden_dualnumber_clock.py
    OPENBLAS_NUM_THREADS=1 PYTHONPATH=. python analysis/w33_20261022_golden_dualnumber_clock.py
    OPENBLAS_NUM_THREADS=1 PYTHONPATH=. python analysis/w33_20261022_gold_prime5_ramification.py

The combined CI job \`.github/workflows/w33-primepower-pascal-c5-optics.yml\` checks these together with six existing prime-power Pascal, C5/Frobenius, beta and optical-control tests. JSON artifacts: \`data/w33_20261022_golden_dualnumber_clock.json\` and \`data/w33_20261022_gold_prime5_ramification.json\`.


## 7. Supergolden ramification at p=31 and the 930-step modular tensor (algebraic prediction)

The quadratic golden field has discriminant +5, but the cubic supergolden polynomial x³-x²-1 has discriminant **-31**. Its only ramified rational prime is 31. Indeed,

    x³-x²-1 = (x-10)(x-11)²   over F31.

The residues 10 and 11 have multiplicative orders 15 and 30 respectively. The 3D supergolden companion S is similar to an eigenline (10) and a size-two Jordan block (11). The exact script \`analysis/w33_20261022_supergolden_prime31.py\` checks the factorization and nilpotency over F31, and verifies directly that a faithful 6D block S tensor J2(1) has **order 930 = 30*31**. No floating-point logarithms or asymptotics enter this result.

For W(3,31), the previously proved generalized-Pascal p-rank theorem gives n=(31+1)(31²+1)=30784 and rank B=binomial(33,3)=5456. The nontrivial square-zero B module has 5456 J2 blocks and 19872 J1 blocks. Tensor with the two-dimensional repeated-root 11 sector produces:

    eigenvalue 11 : J3^5456 + J2^19872 + J1^5456  (dimension 61568)
    eigenvalue 10 : J2^5456 + J1^19872             (dimension 30784)

Total dimension: 92352. This census is **derived algebraically** from the q-family rank theorem and cubic factorization; no 92352-square matrix was constructed or numerically diagonalized. The corresponding scalar/eigenvalue and unipotent orders imply order 930 for the full abstract tensor action. The six-dimensional faithful block is an independently executed witness.

Thus the prime 5 is exceptional for the *golden* base, while prime 31 is exceptional for the *supergolden* base. Both create Jordan chains longer than those at their semisimple primes. Discriminant ramification, rather than a raw coincidence of decimal constants, is the structural feature to generalize.

The formula \`-31\` is an elementary polynomial discriminant computation, consistent with published number-field tables; the tensor-Jordan analysis is a newly implemented cross-track repo calculation, not a claim that the base itself causes new physics.

## Five independent top next steps

1. **General modular beta-clock classification:** For beta-polynomials x^m-x^(m-1)-1 and W(3,p^t), classify separable versus ramified primes via discriminants/resultants, tensor nilpotency depth, and exact modular Jordan types.
2. **Actual q9 symplectic group equivariance:** Determine how Sp(4,9) acts on the R^100 and F9^620 module constituents and whether the golden multiplication operator is central versus geometrically informative; compute commutants and identify nontrivial intertwiners.
3. **Arithmetic semidirect C5 correspondence:** Test a Frobenius-twisted representation for the genus-two curve's mu5 automorphism against the graph's fifth-order automorphism, using local Weil-group characters to prove or refute compatible geometry.
4. **Completed Weil/CCM convergence at certified precision:** Increase actual prime-driven truncations while enforcing corrected quotient metrics, interval enclosures and all prime/gamma/endpoint terms, comparing full Xi moments and determinants—not just first ordinates.
5. **Optical implementation falsifier:** Construct a loss-/crosstalk-aware multi-mode circuit for signed U4/U2 and, separately, a complex permutation representation of C24; test experimentally observable distinctions from the *nonunitary, characteristic-three* phinary graph operator.

**Boundaries:** Exact finite algebra != arithmetic L-function identity != physical dynamics != the classical Riemann hypothesis.
