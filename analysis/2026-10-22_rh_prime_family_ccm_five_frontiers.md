# October 22, 2026 — Five independent RH frontiers executed and tested

**Claim boundary:** the classical Riemann hypothesis is NOT proved. Exact prime-family mathematics is separated below from finite numerical reproductions and impossibility statements for particular ansatzes.

**Main producers**:
- analysis/w33_20261022_levi_prime_family.py
- analysis/w33_20261022_ccm_compact_weil_trace.py
- tests/test_w33_20261022_rh_five_prime_family_ccm.py
- .github/workflows/w33-rh-prime-family-ccm.yml
- CI-produced data/w33_20261022_levi_prime_family.json and data/w33_20261022_ccm_compact_weil_trace.json.

## Search-before-work and prior-claim collisions

The following already existed and must NOT be described as new: the prime-3 genus-two local identity (analysis/2026-10-21_levi_genus2_local_frobenius_bridge.md), the exact 156-dimensional rational companion intertwiner (analysis/2026-10-21_rh_five_followups_synthesis.md), the standard q-family Levi Ihara-Bass spectrum (analysis/2026-10-14_toe76_six_fronts_rh_ihara.md), the Levi apartment unimodular integer basis (Pass5041), the [1620,81,81] binary apartment code (Pass5051), and old numerical completed Gaussian Weil checks (analysis/2026-10-21_rh_nextfive_completed.md). The Lambert-W ladder was already falsified by inverse spectral moments and was not reused as the arithmetic model.

The new synthesis connects these through an **infinite congruence-prime family with actual local curves**, constructs **an independent small finite-prime CCM operator**, tests **genuine smooth compactly supported Weil functions**, and derives an **exact trace-coefficient constraint on any W33 rank-two coupling**.

## 1. Local \ell-adic Galois equivalence — exactly what follows, and what does not

For a fixed prime p in the family below, set f=p(p+1)^2/2 and g=p(p²+1)/2. The graph Bass companion has nontrivial characteristic polynomial (X^4+p²)^f (X²+p)^(2g), with semisimple rational action because these polynomials are separable and graph adjacency is diagonalizable.

For the smooth proper curves C/Fp: y²=x^5+1 and E/Fp: y²=x³-x, the geometric Frobenius characteristic polynomials on H^1(C,Q_l), H^1(E,Q_l) are X^4+p² and X²+p. Their \ell-adic Frobenius operators are semisimple. For \ell != p, the graph companion module after extension to Q_l and the direct-sum curve cohomology modules are therefore **abstractly isomorphic as representations of the procyclic Gal(Fbar_p/Fp)** after choosing a matching Frobenius convention.

This is already a local noncanonical Galois-compatible *linear* equivalence, not merely matching numbers. What remains absent is a natural, integral, symplectic-automorphism-equivariant geometric correspondence inducing it, and all-prime compatibility. Any argument claiming "no Galois-compatible linear map is known" without this distinction overstates the gap.

## 2. Actual finite-prime Connes–Consani–Moscovici matrix

Reconstructed (for cutoff x=lambda²=13 and N=4, dimension 9) the Weil matrix Q using equations (4.2)-(4.4) of Connes–Consani–Moscovici:

Q = point-mass - archimedean - sum_{k=p^m <=13} Lambda(k)/sqrt(k) q(U_n,U_m)(log k),

with the actual nine prime powers 2,3,4,5,7,8,9,11,13 and the explicit Fourier test kernel q. The archimedean integral is independently evaluated by scipy quadrature. The raw rank-one perturbation D = D0 - |D0 xi><delta_N|, xi being the lowest Weil eigenvector normalized against delta_N, gives first positive predicted ordinate ~14.1347995935 versus true 14.1347251417 (absolute discrepancy ~7.45e-5). The known zeta ordinate is *only* used after constructing Q.

The raw D is NOT Euclidean Hermitian; the paper's finite selfadjoint realization takes place on its corrected quotient inner product. Near-zero Weil eigenvalues become extremely ill-conditioned at larger N in float64; this small-N example is a reproduction, not a high-precision implementation of the full paper.

Connes et al.'s convergence to the entire Riemann Xi function in the joint N,lambda limit remains an open mathematical problem. Independently reproduced small-N zero agreement cannot prove classical RH.

## 3. Completed Weil form with truly C-infinity compact logarithmic support

Take L=log13 and b(t)=exp(-a²/[t(L-t)]) for 0<t<L, zero outside, a=0.33. Normalize f0=b and f1=b cos(2pi t/L) in L²(0,L). Their symmetric convolution omega_ij(y) is supported in [-L,L] and C-infinity. Directly compute

W_0,2 = 2 int_0^L omega(y) cosh(y/2) dy,
W_R = omega(0)/2 * [EulerGamma + log(4pi tanh(L/2))]
      + int_0^L [exp(y/2)omega(y)-omega(0)]/[2sinh(y)] dy,
W_p = sum_{p^m <= 13} log(p) p^{-m/2} omega(log(p^m)).

Set K_ij=W_0,2-W_R-W_p. Numerical eigenvalues are approximately 1.097e-6 and 0.03252217, both positive. **The prime cutoff is exact due to support**: no infinite omitted prime series.

This overcomes the former noncompact Gaussian-test limitation, but NOT the bigger problem: the archimedean integrals are approximate floating-point quadrature, not validated Arb/interval bounds, and two test functions do not prove positivity for every admissible compactly supported smooth test function. RH remains unproved.

## 4. Infinite congruence-prime family; local supersingularity vs global-rank obstruction

For every prime p = 3 or 7 modulo 20, gcd(5,p²-1)=1 and p=3 modulo 4. Hence the map x -> x^5 permutes both Fp and Fp²; the character sums for C vanish at extension degrees 1 and 2. Genus-two Poincare duality / functional equation then uniquely forces

P_C,p(u)=1+p²u⁴.

The elliptic curve E:y²=x³-x has trace 0 at such p (supersingular j=1728), so

P_E,p(u)=1+pu².

W(3,p) is the symplectic generalized quadrangle GQ(p,p). Write m=(p+1)(p²+1), f=p(p+1)²/2, g=p(p²+1)/2. Its point/line incidence squared spectrum is

(p+1)² [1], 2p [f], 0 [g].

Consequently the *nontrivial* Levi Ihara inverse factor is exactly

D_nt(u)=(1+p²u⁴)^f (1+pu²)^(2g)
       =P_C,p(u)^f P_E,p(u)^(2g).

There are infinitely many such primes by Dirichlet's theorem on arithmetic progressions. All normalized local phases have finite order dividing 8, and all Newton slopes are 1/2 (supersingular). The independent field-count verifier checks p=3,7,23 over Fp and Fp².

**New negative theorem for the naive global program**: this packet's local rank is 4(f+g)=2p[(p+1)²+(p²+1)] and grows strictly with p: 156,1596,50876 at p=3,7,23. A single fixed-rank global motive or fixed-degree automorphic L-function cannot have these as its unmodified good-prime local factors for infinitely many p. One might still seek varying-rank correspondences or a rigorously specified limit; simply multiplying the local graph factors into a fixed-degree zeta function is impossible.

## 5. Exact relative trace anomaly of W33 bright-channel coupling

Use the small-N CCM rank-one operator's **real eigenvalue list** as a *self-adjoint diagonal isospectral surrogate*, and couple it through eta*u*v^* to K=2I24 + (-4)I15 with u_j=1/j, v_i=1/sqrt39. This is NOT automatically a spectral triple preserving the paper's corrected inner product; the choice is explicitly a new toy rank-two coupling.

For the full block H, finite-dimensional trace expansion yields the exact formulas

Tr H² - Tr (H_ext + K)² = 2 eta² ||u||² ||v||²,
Tr H³ - Tr (H_ext + K)³ = 3 eta² [<u,H_ext u> ||v||² + ||u||² <v,Kv>].

The determinant ratio is 1-eta² g(z)h(z) by the Schur complement. Numerical eigensums and direct 48x48 determinants agree with these formulas to rounding error. Since eta is an unconstrained continuous parameter, the relative trace and determinant vary, rather than equaling any **fixed** prime-determined Xi trace formula. Further, 37 W33 dark modes remain in the full spectrum, defeating any unmodified full Xi determinant identification.

This is a concrete trace-formula obstruction for the *unconstrained coupling*, not a no-go theorem for all arithmetic spectral triples. A next construction must derive the coupling and internal reduction from an arithmetic action, not merely tune eta until zeros align.

## External references

- Connes, Consani, Moscovici, Zeta Spectral Triples (EMS 2026; arXiv 2511.22755): https://arxiv.org/abs/2511.22755
- Independently reproducing the same operator: https://github.com/giuseppesorge/zeta-spectral-triples-replication
- Explicit primary-equation code audit, including the crucial sign correction: https://github.com/skylinetrailcomputing/zeta-spectral-gpu/blob/main/knowledge/ccm-operator.md
- Everett Howe, supersingular genus-two curves over fields of characteristic three (2006): https://arxiv.org/abs/math/0604413

## Five independent next priorities

1. Classify symplectic W(3,p) automorphism representations compatible with the p-local genus-two Frobenius operator and test whether any algebraic correspondence realizes the **noncanonical** local Gal(Fbar/Fp) isomorphism.
2. Implement the full high-precision CCM corrected-metric quotient at multiple cutoffs and systematically certify eigenvector simplicity, parity and normalized Xi determinant convergence using independent high-precision libraries.
3. Build Arb/ball-arithmetic enclosures for the C-infinity compact-support Weil kernels (especially the archimedean digamma term), then systematically increase the support and Galerkin dimension with fail-closed negative eigenvalue tests.
4. Test whether local-factor reciprocity extends to composite q=p^r, and determine which underlying curves (if any) realize the q-Levi factors; avoid incorrectly base-changing the p-curve to claim the same polynomials.
5. Seek a canonical prime-determined W33 two-bright-channel coupling and a justified removal/relative determinant for the 37 dark modes; demand equality of completed Xi moments and Weil trace terms at several unrelated prime cutoffs before speculating about RH.

**Final status: classical Riemann hypothesis OPEN.** All positive claims refer to exact finite algebra or explicitly scoped finite numerical tests.
