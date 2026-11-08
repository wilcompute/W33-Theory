# Null-cone chirality: a stronger symmetry-preserving no-go for real higher-prime clocks

**Date:** 2026-11-08. **Code:** analysis/w33_20261108_null_orbit_chirality.py. **Tests:** tests/test_w33_20261108_null_orbit_chirality.py. **CI:** .github/workflows/w33_20261108_null_orbit_chirality.yml.

This report establishes an exact **conditional** statement about real, symmetric, strictly null-local, translation- and PGL(2,p)-covariant finite Hamiltonians. It does **not** establish a general quantum computational or Lorentzian locality no-go. In particular, Hermitian complex chiral hopping is an explicit logical escape.

## Prior owners

The September 24 history-compactification report already notes that the eight rank-one directions in Sym2(F3) split into two four-element square-class orbits under the projective linear action, and connects their chirality to the common S4 carrier. The November 8 five-front continuation proves that the **unweighted affine null-graph Laplacian** on Sym2(Fq), q an odd prime power at least five, cannot exhibit instantaneous uniform mixing at any time: for a suitable non-null displacement d, |U_t(0,d)| <= 2/q² < 1/q^(3/2). The later deep-fivefront pass finds a weighted (but strongly nonlocal) quadratic-Gaussian escape.

This note adds a **classification of all real PGL2-covariant null-local hopping weights** for odd primes by the quadratic character of -1. It is not a discovery of the quadratic character or finite Gaussian arithmetic itself.

## Exact orbit-reversal theorem

For a nonzero rank-one symmetric 2-by-2 matrix over Fp, write S=s vv-transpose, where v is nonzero. Rescaling v by a nonzero factor rescales s by a square. Hence the Legendre symbol eta(s) is intrinsically defined and splits the p²-1 nonzero rank-one matrices into two equal orbits:

\[
N_+=\{S: \eta(s)=+1\},\qquad
N_-=\{S: \eta(s)=-1\},\qquad
|N_+|=|N_-|=(p^2-1)/2.
\]

For any invertible G, the congruence action G S G-transpose=s(Gv)(Gv)-transpose leaves eta(s) unchanged. These are precisely the two PGL(2,p)-orbits of nonzero null displacements.

Reversing an oriented displacement maps S to -S and multiplies eta(s) by eta(-1). Since

\[
\eta(-1)=(-1)^{(p-1)/2},
\]

the inversion swaps N+ and N- exactly when p is congruent to 3 modulo 4.

A translation-invariant **real** null-local Hamiltonian that also commutes with PGL(2,p) must have constant real weight w+ on N+ and w- on N-. Hermiticity of a real Hamiltonian requires H(S)=H(-S). Thus when p=3 modulo 4, the orbit-swap condition forces

\[
\boxed{w_+=w_-}.
\]

The only such hopping Hamiltonians are scalar multiples of the **unweighted null adjacency**, plus an arbitrary diagonal identity term. Multiplying the Hamiltonian by a scalar merely rescales time, and the diagonal term only contributes a global phase.

**Corollary:** For any odd prime p>=7 with p=3 modulo 4, the previous spectral bound excludes perfect instantaneous uniform mixing at **every** time throughout this entire real symmetric, PGL2- and translation-covariant, strictly null-supported class. It is no longer merely a test of a particular choice of unweighted edges.

The p=3 clock is the small-field exception: the inequality used to exclude uniform mixing fails there, and the original 27-event clock mixes uniformly at its distinguished tick.

## Why this is not an all-Hamiltonian no-go

When p=1 modulo 4, -1 is a square, each orbit is individually inversion stable, and **two independent real null-local weights** survive the same symmetries. The previous single-parameter all-time proof does not cover that family.

For p=3 modulo 4, complex hopping allows an explicitly Hermitian but time-reversal-sensitive alternative: choose w- to be the complex conjugate of w+. This breaks the real-matrix hypothesis without breaking Hermiticity. The earlier no-go does not cover this complex family either.

Thus the physics question becomes one of **actual symmetry and time-reversal assumptions**, not bare dimensional numerology. The W33 geometry supplies a natural discrete chirality, but it does not determine whether the fundamental Hamiltonian is real or which couplings are physically allowed.

## Computational certificate

The script constructs all p³ affine symmetric matrices and both Legendre-defined null sets; checks their equal populations; applies elementary GL2(p) generator matrices to every null displacement to verify square-class preservation; checks inversion exactly; and tests the p=3,5,7,11,13 cases.

| p | Each orbit size | Inversion swaps? | Independent real orbit weights | Previous all-time no-go extends? |
|---|---:|---|---:|---|
| 3 | 4 | yes | 1 | no: distinguished exact 27-clock |
| 5 | 12 | no | 2 | not proven |
| 7 | 24 | yes | 1 | yes |
| 11 | 60 | yes | 1 | yes |
| 13 | 84 | no | 2 | not proven |

The numerical p=5 control scans 1089 fixed angle pairs on [-2pi,2pi]². It finds nonzero deviation from flat probabilities on that grid, but **this is only a bounded, coarse heuristic**: no global minimizer, absent narrow resonance or all-time impossibility follows from it.

A distinct test builds complex conjugate orbit coefficients at p=7 and verifies they are Hermitian under edge reversal while not real symmetric; it also verifies that independently chosen real p=5 weights remain symmetric. These are adversarial controls to prevent overclaiming.

## Five independent next directions

1. Derive a **provable two-parameter flat-mixing obstruction or explicit counterexample** for the real p=1 modulo 4 square-class family, rather than trusting coarse scans.
2. Analyze **complex Hermitian chiral null hoppings** for p=3 modulo 4, testing whether physical time-reversal violation can yield new exact clocks without long-range links.
3. Reconstruct an **effective kinetic operator on the two S4-invariant H1 modes**, and check its mixing with the 28 modes not generated by translations of the symmetric seeds.
4. Derive **actual E6 symmetry-breaking mass projectors and radiative CP constraints**, not more toy determinants.
5. Carry the **27-port optical phase-plaquette and loss model** into a physical process design with independently calibrated phase fidelity.
