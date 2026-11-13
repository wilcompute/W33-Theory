# Quantum state positivity in the Pauli realization of the E6 cubic

Pass 12656 identifies the cubic N(X) = Tr(X³)/48 on the 27 traceless Hermitian three-qubit Paulis commuting with J = (Y⊗I⊗I)K. Let X be their real linear combination. The full image of ordinary mixed quantum states under the charge map is the convex body of X such that I+X is positive semidefinite. Indeed, averaging a density operator with its J conjugate retains exactly these expectations, and conversely (I+X)/8 is itself an ordinary density matrix whenever it is positive. Its extreme points are the quaternionic rank-one projectors, written X = 4Π−I. [Pass 12656](PASS12656_E6_CUBIC_IS_TR_X3_QUATERNIONIC_SUM_RULE.md)

## Exact spectral test

Let μ_i be the four eigenvalues of I+X, taking each quaternionic eigenvalue once. They are real, their sum is 4, and positivity is equivalent to nonnegative e₂, e₃ and e₄ in their elementary symmetric polynomials. If these coefficients are nonnegative, the polynomial with roots −μ_i has nonnegative coefficients and positive leading coefficient. It cannot have a positive real root. The reverse direction follows from μ_i≥0.

Writing p_k = Tr(X^k)/2, the three tests are e₂ = 6−p₂/2, e₃ = 4−p₂+p₃/3, and e₄ = 1−p₂/2+p₃/3+p₂²/8−p₄/4. The producer gives two exact diagonal examples with equal p₂ = 5/2 and p₃ = 0. The first is positive with eigenvalues of X given by ±1 and ±1/2. The other has eigenvalues ±11/10 and ±1/5, so it has a negative eigenvalue of I+X. Thus the quadratic length and the cubic invariant do not determine whether a charge vector comes from a state. The quartic is needed in general.

## Reversible state symmetries

Any affine bijection of this charge body fixes its centroid. The centroid is at zero by invariance under quaternionic unitary conjugation, since the only Hermitian matrices invariant under every such conjugation are scalar. The bijection therefore extends to a real linear trace-preserving and unital automorphism of the positive cone of quaternionic Hermitian 4×4 matrices. These are its Jordan automorphisms, given by quaternionic unitary conjugation. The effective group is USp(8)/{±I}. Conjugation preserves both the cubic and the full state body. [Jordan automorphisms and symmetric cones](https://michael.orlitzky.com/documents/papers/jordan_automorphisms_and_derivatives_of_symmetric_cones.pdf)

The connected split cubic group contains transformations outside this operational symmetry group. The producer solves the 45 integer triad weight equations to obtain a split-torus generator, then evaluates it at scale 2. On the stabilizer charge triad (IIZ, IZI, IZZ), the initial expectations (1,1,1) go to (1,2,1/2). The cubic stays 1, while the output violates the Pauli expectation bound and (I+X)/8 acquires eigenvalue −3/16. This gives an explicit positive-state obstruction in the Pauli chart. It rules out representing that boost by a deterministic positive transformation on this charge body. A different physical encoding or transformation law would need its own positivity analysis.

Replay with `py -3 analysis/toe_20261113_pauli_e6_positivity.py`.
