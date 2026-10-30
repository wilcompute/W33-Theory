# Five W33 RH followups — exact experiments and arithmetic boundaries (21 October 2026)

**Status:** Five executed tests; no proof of the classical Riemann hypothesis.

## Search-before-work registry

- Rational companion: analysis/w33_20261021_rh_five_frontiers.py, analysis/w33_20261021_levi_genus2_frobenius.py, analysis/w33_pass4956_point_line_24d_intertwiner.py.
- Weil: analysis/w33_weil_cocycle_positivity.py, analysis/w33_renormalized_boundary_formula.py, analysis/RH_INVARIANT_TANGENT_AUDIT.md.
- Hecke: analysis/PASS7385_7400_EISENSTEIN_E8_W33_BRIDGE.md, analysis/w33_theta_E8_eisenstein_E4.py, analysis/w33_pass1240_hecke_multiplication_tables.py.
- Graph holonomy: analysis/PASS4447_ZETA_AND_SIGNING_ARE_ONE_SUBJECT.md, analysis/w33_pass4461_line_signing_apartment_trace.py.
- Infinite spectrum: analysis/w33_preregistered_higher_moment_search.py, analysis/w33_rh_correspondence_analytic_operator.py.

## 1. Explicit integer Levi intertwiner

Let N be the 40x40 point-line incidence matrix, L=[[0,N],[N^T,0]], and T=[[L,-3I],[I,0]]. The vertex space splits according to L² eigenvalues 16,6,0 of respective dimensions 2,48,30. For the nontrivial 156D transfer space, build 24 degree-four and 30 degree-two Krylov blocks from frozen integer generators and the polynomials Q6=L²(16I-L²), Q0=(L²-6I)(L²-16I). This gives a 160x156 integer matrix B and 156x156 companion block matrix C satisfying **T B = B C exactly**. A 156-row submatrix has full rank mod 101 and hence over Q. Thus B is an explicit reconstructible full-rank rational conjugator to 24 copies of x^4+9 and 30 copies of x²+3.

This establishes a rational module equivalence with the two abstract local Frobenius factors at p=3 found in the previous genus-two/elliptic curve work. It does NOT construct a canonical etale-cohomology or Galois-equivariant map.

## 2. Completed arithmetic Weil test

Use h_d(t)=exp(-t²/(2 sigma²))cos(dt), sigma=11, and translations (0,.15,.35,.65). The exact classical explicit formula has an arithmetic side containing **pole plus digamma gamma minus von Mangoldt prime-power terms**. Numerical quadrature over |t|<=200 and prime powers n<500 gives a symmetric four-by-four matrix with smallest eigenvalue approximately **0.279998266008083**.

Its entries independently agree with the first 60 positive known zeta ordinates, paired with negatives, to within **8.104628079763643e-15**. The rapidly-decaying omitted tails are numerically negligible for this test, but the implementation does not claim interval certification. This is NOT universal Weil positivity or a proof of RH.

## 3. Hecke nonuniqueness

The Eisenstein eigenvalues (1+p³) and the abstract local recursion T_{p²}=T_p²-p³I permit inequivalent commuting W33 Bose–Mesner actions. Examples: T_p=(1+p³)I and T_p=(1+p³)P12+pPminus4, both commuting with W33 adjacency. Their traces at p=3 are 1120 versus 73. Tests cover p=2,3,5,7,11. So formal Hecke identities alone do not determine the nonconstant 24D/15D W33 arithmetic action. Actual Hecke correspondences need geometry and arithmetic compatibility beyond these formal recursions.

## 4. Complete Levi octagon holonomy

The Levi graph has 80 vertices and 160 undirected incidence edges. Its 1620 simple octagons, obtained from the W33 collinearity four-cycles, are encoded as binary edge vectors. Each edge belongs to exactly 81 octagons. Exact GF2 elimination gives **rank 81**, equal to full cycle-space dimension 160-80+1=81. Consequently octagon parity data distinguish ALL binary edge signings modulo vertex gauge: exactly 2^81 distinct gauge classes. An explicit basis of 81 octagons is frozen in the generated JSON.

This is a complete Z2 graph-connection diagnostic, not a theorem that all such Artin–Ihara L-factors are tempered.

## 5. Infinite spectrum falsifier

The Lambert-W approximate zero ladder and either sign of a bounded 0.05 W33 phase modulation produce self-adjoint compact-resolvent diagonal operators, each retaining the leading Riemann–von Mangoldt TlogT count. But the two signs give different individual ordinates and inverse power moments. Thus compact resolvent, finite W33 symmetry and correct leading density do not determine the classical Xi spectral determinant.

The Connes–Consani–Moscovici 2026 arithmetic finite-prime spectral-triple program is a substantially stronger external benchmark. This file does not claim to have replicated its specialized rank-one perturbation.

## Reproduction and proof boundaries

- Executable: analysis/w33_20261021_rh_followup_five.py
- Tests: tests/test_w33_20261021_rh_followup_five.py
- CI: .github/workflows/w33-rh-followup-five.yml
- Generated certificate: data/w33_20261021_rh_five_followups.json
- Assertion: classical_RH_proved is false.

The missing classical RH theorem remains global positivity of the *complete* Weil quadratic form on all admissible test functions, or an exact self-adjoint spectral determinant identification with completed Xi including zero multiplicities and regularization.

## External context

- Explicit formula: https://en.wikipedia.org/wiki/Explicit_formulae_for_L-functions
- Stark–Terras graph Artin L-functions: https://www.sciencedirect.com/science/article/pii/S0001870800919170
- Connes–Consani–Moscovici, Zeta Spectral Triples (2026): https://alainconnes.org/2026/07/zeta-spectral-triples/
- Independent spectral-triple replication: https://github.com/giuseppesorge/zeta-spectral-triples-replication

## Top five independent next steps

1. Compute integral index and test automorphism, symplectic, and Galois compatibility of the Levi rational conjugator.
2. Enlarge the completed Weil Galerkin test space; certify all arithmetic truncation and quadrature errors with interval arithmetic.
3. Construct or rule out an actual nonconstant W33 Hecke correspondence from geometry, not abstract recurrence relations.
4. Use the complete 81D octagon gauge coordinates to classify tempered Z2 Levi Artin–Ihara characters within provably exhaustible structural subfamilies.
5. Apply a W33 internal modulation to an actual arithmetic finite-prime spectral-triple matrix and test determinant and inverse-moment identities, not just density.
