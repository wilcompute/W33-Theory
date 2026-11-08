# An affine-congruence Hadamard obstruction for the Forty Points null-history tower
**Date:** November 8, 2026.  
**Producer:** [analysis/w33_20261108_full_affine_covariance_no_go.py](w33_20261108_full_affine_covariance_no_go.py)  
**Independent tests:** [tests/test_w33_20261108_full_affine_covariance_no_go.py](../tests/test_w33_20261108_full_affine_covariance_no_go.py)  
**CI:** [.github/workflows/w33_20261108_full_affine_no_go.yml](../.github/workflows/w33_20261108_full_affine_no_go.yml).

**Mathematical scope.** A representation-theoretic obstruction to a flat quantum walk on one finite affine space, given precise global symmetry assumptions. No new physical interaction, vacuum, measured constant, or emerging spacetime is established.

## Theorem — independent of locality, reality, time, or a chosen Hamiltonian

Let q be an odd prime power, V=Sym_2(F_q), |V|=q^3, and let the affine group V ⋊ GL(2,q) act on V with translations and matrix congruences S↦GSG^T. Suppose U is unitary on ℓ²(V) and commutes with every element of this affine group. For d corresponding to the symmetric matrix

    d = [[0,1],[1,0]] = (a=0,b=1,c=0),

we claim

\[
\boxed{|U_{0,d}|\leq 2/q^2.}
\]

Perfect instantaneous mixing would require every |U_{x,y}|=q^{-3/2}. For all odd prime powers q>=5, 2/q² < q^{-3/2}. **Therefore no affine-congruence-invariant unitary on this q³-dimensional permutation representation is complex Hadamard for q>=5.** In particular, no self-adjoint Hamiltonian that commutes with the entire group can produce exact uniform mixing at any time, regardless of hopping range, complex chiral amplitudes, higher-order couplings, or the chosen evolution time.

The q=3 exceptional walk is *not ruled out*; it is independently known to mix uniformly.

This theorem is **stronger** than the previously established no-go for the **unweighted null-support graph**, and stronger than the previous real symmetric null-orbit special case. It does **not** exclude a flat walk that drops full GL2 congruence covariance, drops translation covariance, changes the Hilbert representation or changes the number of modes. The weighted Gaussian chirps from the preceding pass do exactly the first: their q>=5 phase polynomials break full congruence invariance.

## Proof with only five exact character coefficients

Because U is translation invariant, U_{x,y}=f(x−y), and the abelian Fourier characters diagonalize U. The full GL2(q) action on dual characters partitions the q³ momenta into five orbits:
1. zero;
2. nonzero rank-one symmetric dual matrices with square overall scalar;
3. rank-one matrices with nonsquare scalar;
4. nondegenerate dual matrices with square determinant;
5. nondegenerate dual matrices with nonsquare determinant.

Identify dual momentum k=(u,v,w) with the symmetric matrix K=[[u,v/2],[v/2,w]], whose determinant is Q*(k)=uw−v²/4. The dual Fourier pairing is k·d=v at the selected displacement d=(0,1,0).

For an orbit O_j, define its character sum at d as C_j = Σ_{k∈O_j} ψ(v), with any nontrivial additive character ψ:Fq→C. **Each C_j is an exact integer,** obtained by counting the number N0 of orbit momenta with v=0 and the common number N1 with v=t for each t≠0; additive-character orthogonality gives C_j=N0−N1.

The five coefficients are, in the order listed,

\[
\boxed{(C_0,C_1,C_2,C_3,C_4)
=\left(1,\frac{q-1}{2},\frac{q-1}{2},-q,0\right)}
\]

when q≡1 (mod 4), with the last two exchanged when q≡3 (mod 4).

**Direct derivation.** The zero class contributes one. For nonzero rank-one K (det K=0), at v=0 the two coordinate axes contribute 2(q−1) elements, q−1 in each square class. At any fixed v≠0, choose u≠0 in q−1 ways and set w=v²/(4u), with exactly (q−1)/2 choices in each square class. Thus each rank-one class contributes q−1−(q−1)/2=(q−1)/2.

For all q³ dual momenta, Σ_k ψ(k·d)=0 because d≠0. Therefore the sum of the two nondegenerate-class coefficients is −1−(q−1)=−q.

To split these final two, let χ be the quadratic character, extended by χ(0)=0. The *difference* of their character sums is

\[
D=\sum_{u,v,w}\chi(uw-v^2/4)\psi(v).
\]

For u≠0, the sum over w vanishes by quadratic-character balance. For u=0, it becomes q χ(−1) Σ_{v≠0} ψ(v)=−qχ(−1). Since C3+C4=−q and C3−C4=−qχ(−1), the two coefficients are exactly −q and 0 in the advertised order. **This is a proof over every finite field of odd order**, not merely a numerical polynomial fit.

Under the affine symmetry, the Fourier eigenphase z_j of U is constant on each of the five dual classes. Unitarity gives |z_j|=1. Consequently

\[
U_{0,d}=q^{-3}\sum_{j=0}^4 C_j z_j,\qquad
|U_{0,d}|\leq q^{-3}\sum_j |C_j|=\frac{2}{q^2}.
\]

No assumption about generator support, spectral integrality, one-loop physics, Euclidean metric or a time choice appears in this final inequality.

## Critical correction to earlier reports

The faithful congruence action on Sym_2(Fq) is GL(2,q)/{±I}, *not* PGL(2,q) in general. A scalar G=λI acts by S↦λ²S and is nontrivial unless λ²=1. Therefore:

- q=3: GL(2,3)/{±I} and PGL(2,3) both have 24 elements; S4 labels are correct.
- q=5: the faithful congruence group has 240 elements, while PGL(2,5) has 120.
- q=7: the respective sizes are 1008 and 336.

Earlier documents using "PGL2-invariant" for q>=5 as if it were this same congruence action must be read as **GL2-congruence-invariant**. The earlier numerical orbit data remain valid because their generators were actual GL2 congruences. This erratum matters: covariance under a *different* projectively normalized action is a different problem.

## Exact independent integer certificate and tested cases

The Python regression does **not** approximate the C_j with floating-point FFTs. It enumerates all five dual orbit classes, constructs an exact integer histogram of each middle-coordinate value v, verifies all nonzero values occur equally often, and checks C_j=N0−N1. Six primes tested:

| q | Exact five character coefficients | Max transition amplitude | Required uniform amplitude | Excluded? |
|---|---|---:|---:|---|
| 3 | 1,1,1,0,−3 | 2/9 | 1/√27 | No |
| 5 | 1,2,2,−5,0 | 2/25 | 1/√125 | Yes |
| 7 | 1,3,3,0,−7 | 2/49 | 1/√343 | Yes |
| 11 | 1,5,5,0,−11 | 2/121 | 1/√1331 | Yes |
| 13 | 1,6,6,−13,0 | 2/169 | 1/√2197 | Yes |
| 17 | 1,8,8,−17,0 | 2/289 | 1/√4913 | Yes |

Prime-power q extensions are covered by the exact finite-field proof, although the supplied code checks **prime** fields and uses NumPy integer residues rather than a general F_(p^n) implementation. This separation between proof and test scope is deliberate.

## What actually remains open

A complex Hermitian two-orbit Hamiltonian on the q>=5 null cone that commutes with full GL2 congruence is now ruled out from exact flat mixing, as is the independent-real-weight q=1 (mod4) case. **The relevant escape is to break the full affine congruence symmetry.** One can retain selected subgroups, a momentum-dependent gauge twist, a magnetic projective translation action or an augmented internal Hilbert space. The pre-existing nonlocal Gaussian chirps explicitly break congruence covariance for q>=5 and do achieve flat mixing, but do not supply locality.

This is a **quantum-walk symmetry theorem**, not a privileged numerical proof of nature's number of qutrit levels. Compare the existing quantum-walk literature: Godsil, Mullin and Roy, *Uniform Mixing and Association Schemes* (Electronic Journal of Combinatorics 24(3), 2017; doi:10.37236/4745), and Coutinho and Guo, *Selected open problems in continuous-time quantum walks* (2024; doi:10.1515/spma-2024-0025). An independent priority review is required before claiming a new published theorem.

## Five independent next targets

1. **Minimal symmetry breaking:** classify index-two and index-(q−1)/2 subgroups of the congruence action that admit a flat unitary at q=5 while retaining as much locality as possible.
2. **Gauged/magnetic translations:** test a U(1) or qutrit-center magnetic translation cocycle; then measure whether it evades the literal commutant while maintaining a meaningful local action.
3. **Gauge H1 matter dynamics:** calculate the translation-averaged 18D frame of S4-invariant harmonic sources and test whether a physical kinetic operator can separate it from the 28D complement.
4. **E6 chiral sector:** derive a genuine broken-subgroup 3-family mass matrix, rather than selecting a skew 3×3 coordinate fiber.
5. **Photonic realization:** optimize an actual 27-port waveguide ordering and include tritter routing, loss, interference-phase calibration, and full 729-channel preregistration.
