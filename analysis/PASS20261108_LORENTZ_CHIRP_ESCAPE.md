# Finite Lorentz isometry, exact Hadamard mixing, and the minimal q=5 symmetry escape

**Date:** November 8, 2026. **Code:** analysis/w33_20261108_lorentz_chirp_escape.py. **Tests:** tests/test_w33_20261108_lorentz_chirp_escape.py. **CI:** .github/workflows/w33_20261108_lorentz_chirp_escape.yml.

**Tier:** exact finite-field theorem and independently tested Fourier examples, *not* a demonstration of physical Lorentz spacetime, gravitation, light, particle couplings, a vacuum or TOE.

## The new structural connection

The Forty Points affine history space is V=Sym2(Fq), with the nondegenerate quadratic form

\[
Q(S)=\det S=ac-b^2,\qquad S=\begin{pmatrix}a&b\\b&c\end{pmatrix}.
\]

This form has the algebraic structure of a 2+1 Lorentzian quadratic metric. Over real numbers the determinant-preserving SL2(R) congruence maps give the standard spin double cover of the connected proper Lorentz isometry group SO+(2,1). Over finite odd fields, SL2(Fq) similarly preserves the quadratic form. **This is an algebraic analogy: finite-field topology has neither physical causal propagation nor a calibrated speed of light.**

Under any invertible G, determinant transforms as Q(GSG^T)=(det G)^2 Q(S). So the full GL2 congruence action is a group of quadratic *similitudes*, not exclusively isometries. Define the index-(q−1)/2 subgroup

\[
H_q=\{G\in GL_2(F_q):(\det G)^2=1\}.
\]

It includes SL2(Fq) and also the det=−1 coset. Its order is \(2|GL_2(F_q)|/(q-1)\). At q=3 all nonzero determinants square to one, so H3=GL2(F3); at q>=5 the proper isometry subgroup is strictly smaller.

**At q=5 this is an index-two subgroup, the smallest possible nontrivial subgroup index.** The full GL2-congruence obstruction of PASS20261108_AFFINE_COVARIANCE_NO_GO proves that exact flat mixing cannot occur with full affine symmetry. The construction below attains it after breaking only this index-two factor (no narrower finite-index reduction is possible in the group-index sense).

## The exact Gauss-flat isometric unitary

For any finite field Fq of odd order, fix a nontrivial additive character psi and define

\[
\boxed{U_{S,T}=q^{-3/2}\,\psi\bigl(\det(S-T)\bigr).}
\]

This is a unitary complex Hadamard matrix on q³ modes. Indeed, for S≠T the phase difference

\[
\det(S-Z)-\det(T-Z)
\]

is a *nonzero linear functional in Z plus a constant*, because det is a nondegenerate quadratic form in odd characteristic. Summing that character over all Z gives zero, so all distinct rows are orthogonal. Each entry has modulus q^-3/2. A global phase may be included without changing the result.

The unitary is translation invariant by construction. For any G in Hq, det(G(S−T)G^T)=det(S−T), so U commutes with the induced congruence action. At q>=5, a GL2 element with det(G)^2 !=1 changes the phase for a suitable S−T, so full congruence covariance is lost. **Thus it evades, rather than contradicts, the full-affine no-go.**

The code checks p=3,5,7,11,13,17. The finite Fourier spectrum of the convolution kernel has modulus one (the unitary criterion) with maximum residual below 1e-12. The subgroup indices are 1,2,3,5,6,8. All nonzero matrix elements have probability 1/p³ as required.

For odd prime-power q the same proof works with the field trace in psi, although the code's NumPy modular array implementation tests prime fields only.

## What the construction does not solve: locality and the physical clock

The unitary itself is a perfect mixer. But the Hermitian generator H obtained through the principal spectral logarithm U=exp(-iH) is **not generally supported only on null-cone edges**. The code computes its translation-invariant convolution and counts off-null couplings. This provides an explicit nonlocal generator witness, not a theorem that no other local logarithm could generate the same U.

The finite Lorentz isometry analogy is the most promising *structural* reading: q=3 is special because the full congruence group automatically preserves det, while q>=5 requires breaking the extra finite conformal scale-similitude symmetry. It is **not a physical prediction that Nature chose q=3**, nor a proof that finite-field isometry gives continuous Lorentz invariance.

A further challenge is a genuinely null-local Hamiltonian that respects at least SL2(Fq). The prior full-affine theorem cannot exclude it, but the original unweighted null-graph theorem does exclude the one-parameter unweighted family at q>=5. The present dense chirp does not solve that local-dynamics question.

## Why this matters to the Theory of Everything program

The distinction between **isometries** (preserve a quadratic norm) and **similitudes** (preserve it only up to scale) is the central lesson. Any attempt to derive relativistic propagation from the Forty Points finite history chart must specify which group is being represented, what dynamics it preserves, which symmetry is broken and what sets a dimensionful physical propagation scale.

The data cannot distinguish this mathematical structure from ordinary quantum mechanics: a built circuit implementing the same unitary has exactly the same probabilities under standard quantum theory.

## Five orthogonal next experiments

1. Search for an **SL2-covariant strictly null-local** Hermitian generator that yields exact or controlled approximate flat mixing at q=5, without expanding to dense couplings.
2. Construct an honest **finite-field → Lorentzian continuum limit** with a propagating Green function, invariant speed and error bounds, not merely the correct quadratic norm.
3. Test whether the **46D H1 harmonic frame** supplies a nontrivial equivariant bundle over the finite Lorentz momentum orbits, rather than a static 2D seed projector.
4. Derive a **physical symmetry-breaking E6 mass operator** with rank-three effect on the native kernel and protected one-loop strong CP.
5. Design a **two-scale optical comparison**: 27-mode fully affine-symmetric clock vs 125-mode isometry-only Gaussian clock, measuring phases, calibrated losses and the preselected q=5 probability bound.


## Addendum — strictly null-local Lorentz-isometric flat mixing is excluded too

The existence of an Hq-invariant Gauss-flat unitary does **not** imply a strictly null-local Hq-invariant Hamiltonian can generate it. In fact the latter is impossible at odd prime-power q>=5 if translation invariance and the natural SL2(q) congruence symmetry are required.

**Exact orbit lemma.** The group SL2(q) is transitive on the nonzero vectors of Fq²: given any nonzero target vector v, extend it to an ordered basis of determinant one. Acting on the reference symmetric matrix e1e1^T gives the rank-one orbit {vv^T:v !=0}, of size (q²−1)/2 because v and −v give the same matrix. Multiplying by a fixed nonsquare scalar gives a disjoint second orbit of the same size. These two are **exactly the two rank-one square-class orbits under the full GL2(q)**.

Thus every translation-invariant convolution Hamiltonian with *strictly null-supported off-diagonal entries* and SL2(q) covariance has at most two independent orbital hopping coefficients (plus a diagonal). Since the larger GL2(q) preserves those same two null classes, **the operator necessarily commutes with the full GL2(q) congruence action**, without having assumed it. This statement permits complex Hermitian coefficients; it is not restricted to real symmetric hopping.

The all-time affine symmetry theorem now applies directly: for q>=5, no such strictly null-local SL2(q)-covariant Hamiltonian can generate an exactly flat unitary at any time.

**This is a locality-plus-symmetry no-go, not a no-go for ordinary relativistic propagation.** A Lorentz-like wave equation need not mix every finite basis state uniformly. Non-null hops, more than one internal degree of freedom, projective/magnetic translations or further subgroup breaking remain possible.

The regenerated code certifies two SL2 rank-one orbits of size (p²−1)/2 for p=3,5,7,11,13,17 and verifies the entire null set is partitioned. A new regression asserts the additional p>=5 no-go consequence. This addendum supersedes any suggestion that keeping full SL2 symmetry but changing only the real/complex weights on rank-one null links could evade the earlier amplitude bound.
