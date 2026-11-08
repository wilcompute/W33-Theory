# Forty Points — S4 symmetry selection and the finite Gaussian dual clock

**Date:** 2026-11-08. **Evidence:** exact finite character enumeration, numerical Hodge and Fourier cross-checks, six-prime Gaussian identities. This is *not* a measured physical constant, a photon identification, a Lorentzian continuum or a complete TOE.

**Source:** analysis/w33_20261108_s4_harmonic_qdual.py  
**Tests:** tests/test_w33_20261108_s4_harmonic_qdual.py  
**CI:** .github/workflows/w33_20261108_s4_harmonic_qdual.yml  
**Machine certificate:** generated JSON in GitHub workflow artifact forty-points-s4-harmonic-qdual-json.

## Ownership and mathematical setting

The prior September 24 history-compactification report already derives the 27-vertex big cell of the quadric Q(4,3), its 108 edges and 36 edge-disjoint triangles, harmonic first-cohomology rank 46, and the shared PGL(2,3) = S4 action on the four projective null directions, linking this geometry to the four Hesse/E8 A2 factors. The November 8 five-front continuation already derives the translation momentum multiplicities 8 times 2, 12 times 1 and 6 times 3, totaling 46; the subsequent deep continuation gives uniform Hodge edge leverage 23/54. We do not rebrand these prior results.

This certificate adds the complete **S4 character and ordinary irreducible decomposition of the actual 46D harmonic cochain module**, an independent symmetry-Hodge projector, a partial translation-orbit reachability audit, and the explicit finite-field Fourier-dual quadratic phase of weighted higher-prime clocks.

## 1. Exact S4 character theorem

Label the 27 vertices by 2-by-2 symmetric matrices over F3, with determinant q(a,b,c)=ac-b². Use the null-adjacency edges and oriented triangles. The exact boundary matrices satisfy B1 B2=0 and B2-transpose B2=3 I36, so the filled complex has no H2.

Enumerate GL(2,3)/{±I}, order 24, acting as S -> G S G-transpose. Edge and triangle characters must use *signed fixed cells*, not just setwise fixed counts.

The exact equivariant Euler identity is:

\[
\chi_{H^1}=\chi_{C^1}-\chi_{C^0}-\chi_{C^2}+\chi_{H^0}.
\]

| S4 cycle type | Class size | chi C0 | signed chi C1 | signed chi C2 | chi H1 |
|---|---:|---:|---:|---:|---:|
| 1+1+1+1 | 1 | 27 | 108 | 36 | 46 |
| 2+1+1 | 6 | 9 | 18 | 6 | 4 |
| 2+2 | 3 | 3 | 0 | 0 | -2 |
| 3+1 | 8 | 3 | 3 | 3 | -2 |
| 4 | 6 | 1 | 0 | 0 | 0 |

Pairing this character with the irreducible S4 character table gives the exact complex-representation identity:

\[
\boxed{H^1=2\mathbf 1\oplus4\mathbf 2\oplus7\mathbf 3\oplus5\mathbf 3'.}
\]

The dimensions add to 2+8+21+15=46. There is **no sign representation**, and **two S4-invariant directions**. Independent numerical verification uses the 108-dimensional Hodge projector and the signed 24-group average: the resulting orthogonal projector has rank 2, trace 2 and residual below 1e-10.

The same procedure averaged over all 27 affine translations gives *zero* translation-invariant harmonic vectors. Hence there is no nonzero invariant vector for the full affine 3³:S4 symmetry, although there are two for the reduced S4.

**Physical boundary:** These two finite cochains cannot be identified with physical photon polarizations just because the number is two. Photon plane waves need not be fixed by translations; a physical identification requires a Lorentzian action, gauge charges and a kinetic normalization.

## 2. Which parts of the 46D harmonic space can the two S4 seeds reach?

Apply all 27 translations to an orthonormal basis of the two S4-invariant harmonic cochains. The resulting 54 vectors have **numerical rank 18**, not 46. This separates 18 reached modes from 28 unspanned harmonic dimensions.

The finite Fourier character projector is

\[
\Pi_k=\frac1{27}\sum_{t\in F_3^3}\omega^{-k\cdot t}R_t.
\]

Let n0(k) count projective null directions perpendicular to momentum k. The **directly computed** spectral weight of the two S4 seed currents is:

| n0 | Number of characters | Total harmonic dimension | Seed trace per character | Translation-reached dimension |
|---|---:|---:|---:|---:|
| 4 | 1 | 0 | 0 | 0 |
| 1 | 8 | 16 | 0 | 0 |
| 2 | 12 | 12 | 1/12 | 12 |
| 0 | 6 | 18 | 1/6 | 6 |
| Total | 27 | 46 | weights sum to 2 | 18 |

The other 28 modes consist of the 16 modes in the eight two-dimensional character fibers and another 12 directions inside the six three-dimensional fibers. The character theorem is exact integer representation theory. The orbit rank, its nonzero singular-value gap and the rational-looking Fourier weights were independently verified **numerically**, not by a separate exact symbolic minimal-polynomial proof.

This supplies a strong falsifier for oversimplified proposals that assume an S4 selector automatically generates all 46 possible harmonic gauge degrees of freedom.

## 3. Prime-field Gaussian clock: the unique fixed-chart q=3 coincidence

For an odd prime p use q(k)=k0*k2-k1² mod p, and the translation-invariant weighted Hamiltonian with real Fourier eigenvalues the integer representatives of q(k). At special time 2π/p, its finite Fourier kernel is

\[
U(d)=p^{-3}\sum_k\exp[2\pi i(k\cdot d-q(k))/p].
\]

The quadratic Gauss sum and completion of the square yield

\[
U(d)=U(0)\exp[2\pi i q^*(d)/p],\quad
q^*(d)=d_0d_2-4^{-1}d_1^2,\quad |U(0)|=p^{-3/2}.
\]

Thus **all p^6 transition probabilities equal p^-3 exactly** for every odd prime. Six independent FFT regressions p=3,5,7,11,13,17 confirm this phase law and flatness near floating precision.

In the *fixed original symmetric-matrix coordinates*, q*(d)=q(d) if and only if 4^-1=1 mod p, so **only p=3** among odd primes has identical primal and Fourier-dual coordinate polynomials. This is **basis-sensitive**: it does not mean equivalent forms over other fields cannot be related by a change of coordinates, and does not establish an exclusive physical role for three.

The six numerically checked off-diagonal weighted Hamiltonian support counts are p=3:26, p=5:100, p=7:342, p=11:1330, p=13:2028, p=17:4624. The counts use a 1e-9 coefficient threshold and are not asserted as an all-prime theorem. Most weighted couplings violate null-cone locality. Therefore the exact uniform-chirp extension does **not** supply a controlled local continuum or contradict the earlier all-time no-go for the unweighted null-only adjacency family.

## 4. Implications for the ongoing five fronts

**Gauge:** Two S4-fixed seeds exist, but full translation symmetry fixes none. Translation of those two seeds reaches only 18/46 harmonic directions. Test a normalized, dynamically chosen matter coupling before identifying photon or helicity sectors.

**Flavor:** The previously checked native 1,620-record E6 signed tensor yields skew 3-by-3 coordinate-fiber mass blocks. The actual symmetry-breaking projector and loop-stable Nelson–Barr embedding remain open; this pass does not alter those results.

**Higher-q locality:** The new dual-phase identity explains the especially simple native coordinate form of q=3. Weighted higher-prime uniform mixing is an exact mathematical construction but remains nonlocal.

**Provenance:** Existing September and November owners are named and do not become independent support merely because a new script rechecks them.

**Optics:** The full 27-port Clifford/compiler benchmark can now use the Gaussian dual polynomial as a phase reference; a genuine phase-interference experiment remains to be built.

## Top five orthogonal next investigations

1. Construct and falsify a *matter-normalized dynamical selector* on the two S4 seeds and the 28 complementary harmonic modes.
2. Search *bounded-range, null-local weighted* higher-field Hamiltonians that admit rigorous continuum-limit dispersion rather than the dense Fourier chirp.
3. Identify a *physical E6 broken-subgroup projection* with three chiral masses and gauge-invariant Nelson–Barr loop protection.
4. Produce a *fabrication-specific 27-port interferometer* measuring gauge-invariant phase plaquettes, port intensities and calibrated noise.
5. Complete a *rename-aware conceptual provenance ledger* with conditional/withdrawn claims, RG scheme details and untouched observational holdouts.
