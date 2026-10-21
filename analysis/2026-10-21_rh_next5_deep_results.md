# 21 October 2026: Five independent W33/RH follow-up investigations

**Scope:** exact finite graph mathematics, a completed Weil-form numerical audit, a representation-theoretic obstruction, and an analytic spectral-model falsifier. **Classical Riemann RH remains open.**

Producer: analysis/w33_20261021_rh_next5_deep.py
Tests: tests/test_w33_20261021_rh_next5_deep.py
Dedicated workflow: .github/workflows/w33-rh-next5-deep.yml
Generated certificate: data/w33_20261021_rh_next5_deep.json

## 1. Rational Levi companion conjugator

Prior corpus checked: analysis/w33_pass4956_point_line_24d_intertwiner.py; analysis/w33_20261021_levi_genus2_frobenius.py; analysis/w33_20261021_rh_five_frontiers.py.

The producer computes an integer 160x156 Krylov embedding S from 24 four-step generators and 30 two-step generators. It verifies T*S=S*C exactly over Z, where T is the 160-dimensional Levi Bass companion and C consists of 24 companion blocks for x^4+9 and 30 blocks for x^2+3. Rank modulo 101 is 156; these columns are a rational basis of the nontrivial transfer space.

A genuine W33 symplectic transvection on 40 points and 40 lines acts as G on the full Bass carrier and satisfies GT=TG over integers. The induced 156x156 action H obeys SH=GS and HC=CH modulo 101. This tests automorphism compatibility nontrivially, but is not a canonical geometric or Galois-equivariant curve-cohomology correspondence.

## 2. Completed Weil explicit-formula Galerkin matrix

Prior corpus checked: analysis/w33_weil_cocycle_positivity.py; docs/RH_CASEY_W33_NEXT5_SYNTHESIS.md; analysis/RH_INVARIANT_TANGENT_AUDIT.md.

Use three even Schwartz test functions with Fourier profiles F_w(t)=exp(-a(t-w)^2)+exp(-a(t+w)^2), a=0.07, w=0,7,14. For h_ij=F_i F_j the inverse Fourier transform is an exact finite Gaussian sum, so the right-hand side of the completed Riemann–Weil explicit formula is computable: the pole terms h(i/2)+h(-i/2), the prime-power terms -2 sum Lambda(n)/sqrt(n) g(log n), and the archimedean digamma integral (1/2pi) integral h(t)(Re psi(1/4+it/2)-log pi) dt.

Using all prime powers n<=1000, numerical quadrature and the first 64 computed positive critical-line zeros on the independent zero side, the 3x3 matrices agree to approximately 2.4e-17 absolute error. The approximate eigenvalues are -2.4e-17 (numerical rounding), 1.61e-6, 1.99854. This numerical finite family is consistent with RH but is not an interval-certified universally positive Weil form and proves no new RH statement.

## 3. E8 Hecke scalar-line obstruction

Prior corpus checked: PASS7385_7400_EISENSTEIN_E8_W33_BRIDGE.md; analysis/w33_theta_E8_eisenstein_E4.py; analysis/PART_CCCCCXCIX_E8_SPECTRAL_SCOPE_AUDIT.md.

The normalized Eisenstein E4 Hecke eigenspace is one-dimensional with T_p eigenvalue 1+p^3. W33's point permutation representation splits as 1+24+15. The only invariant vectors for the full transitive symplectic W33 automorphism action are constants, so the 24- and 15-dimensional summands contain no invariant vectors. Therefore Hom_G(1,V24+V15)=0. An equivariant map from the scalar E4 eigenline into nonconstant W33 sectors is necessarily zero. This does not rule out a nontrivial higher-dimensional arithmetic Hecke module or symmetry reduction.

## 4. All Levi octagons span the binary cycle space

Prior corpus checked: analysis/w33_pass4461_line_signing_apartment_trace.py; analysis/PASS4447_ZETA_AND_SIGNING_ARE_ONE_SUBJECT.md; analysis/w33_20261014_toe76_levi_ihara_hierarchy.py.

Construct 1620 distinct length-eight Levi apartments as binary incidence vectors of length 160. Their exact rank over F2 is 81 = |E|-|V|+1 = 160-80+1. Thus octagon holonomies distinguish ALL Z2 characters of the Levi graph modulo vertex-gauge transformations. There are 1539 linear dependencies among the 1620 octagon vectors. Every incidence edge belongs to 81 octagons.

All 12720 choices of two flipped incidence edges were exhaustively classified, with frustrated-octagon counts:
108 -> 480 edge pairs;
144 -> 1440 edge pairs;
156 -> 4320 edge pairs;
160 -> 6480 edge pairs.

This is a complete TWO-EDGE census, not a classification of all 2^81 characters and not a purity result for arithmetic Frobenius sheaves.

## 5. Rigorous fourth-inverse-moment obstruction for Lambert-W/W33 diagonal model

Prior corpus checked: analysis/w33_preregistered_higher_moment_search.py; analysis/w33_rh_correspondence_analytic_operator.py; analysis/w33_20261021_rh_five_frontiers.py.

With t_n=2pi(n-7/8)/LambertW((n-7/8)/e) and delta_n=.05*(24cos(n theta2)+15cos(n thetaMinus4))/39, the diagonal operator with eigenvalues t_n+delta_n is self-adjoint with compact resolvent and the correct leading T log T density.

The inverse-fourth moment of levels 1..1200 is approximately 1.8833e-5, but just the first 60 established positive classical zeta-zero ordinates contribute approximately 3.71295e-5. Crucially the entire uncomputed tail is provably too small to repair the difference.

For n>=1201, t_n > pi*n/log n and |delta_n|<=.05, hence (t_n+delta_n)^(-4)<1.001*(log n/(pi*n))^4. Since that comparison function decreases for n>=1200, first-term-plus-integral bounds the entire tail by less than 7e-9. Therefore the model's entire infinite inverse-fourth spectral moment is strictly smaller than the 60-zero contribution. An exact spectral identification with the classical zero ordinates is ruled out for this specific operator, independently of additional finite levels.

Normalized finite determinant ratios Xi(1/2+iz)/Xi(1/2) were also compared for z=2,5,10,12. Their logarithms and inverse moments disagree substantially with finite model products, confirming the negative control. These tests DO NOT refute Hilbert–Pólya generally.

## External context

Connes–Consani–Moscovici, Zeta Spectral Triples (2026):
https://alainconnes.org/2026/07/zeta-spectral-triples/

Connes–Consani, Weil explicit formula positivity under support restrictions:
https://www.sciencedirect.com/science/article/abs/pii/S0764444200016876

Stark–Terras graph-cover Artin L-function theory:
https://www.sciencedirect.com/science/article/pii/S0001870800919170

Xu September 2026 Bilu–Linial unrestricted-signing counterexample:
https://arxiv.org/abs/2609.15591

## Five independent next experiments

1. Compute all full-group generator actions on the 156-dimensional rational Levi companion basis and test arithmetic motive equivariance.
2. Introduce certified interval arithmetic for larger completed Weil Galerkin matrices, including adversarial off-line quartet detection.
3. Seek nontrivial Hecke representations with multiplicities 24 and 15, rather than repackaging the scalar E4 eigenline.
4. Bound minimum nonzero octagon frustration among all binary H1 characters, using code bounds or symmetry rather than enumerating 2^81 cases.
5. Develop an all-prime self-adjoint arithmetic operator that satisfies the inverse-moment and normalized-determinant constraints which ruled out this Lambert-W scaffold.
