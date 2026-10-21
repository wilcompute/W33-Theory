# 2026-10-21 — Five RH research frontiers executed

**Scope: five reproducible experiments and exact finite operator statements. Classical RH remains unproved.**

Executable: analysis/w33_20261021_rh_five_frontiers.py
Tests: tests/test_w33_20261021_rh_five_frontiers.py
Command: PYTHONPATH=. pytest -q tests/test_w33_20261021_rh_five_frontiers.py
Certificate producer: python analysis/w33_20261021_rh_five_frontiers.py
Generated certificate location: data/w33_20261021_rh_five_frontiers.json

An independent local prototype with the same five mathematical targets passed five focused tests before porting to the GitHub-connected source. This is not itself a GitHub CI result.

## Repository intake, conducted separately for each track

1. E8–Hecke: PASS7385_7400_EISENSTEIN_E8_W33_BRIDGE.md; analysis/w33_theta_E8_eisenstein_E4.py; analysis/PART_CCCCCXCIX_E8_SPECTRAL_SCOPE_AUDIT.md. Existing: actual 40 Eisenstein six-root fibers and classical Theta(E8)=E4.
2. Levi/Frobenius: analysis/w33_pass4956_point_line_24d_intertwiner.py; analysis/w33_20261021_levi_genus2_frobenius.py; analysis/2026-10-21_levi_genus2_local_frobenius_bridge.md. Existing: a point-line incidence intertwiner and a local prime-3 genus-two/elliptic factorization.
3. Weil: analysis/w33_weil_cocycle_positivity.py; docs/RH_CASEY_W33_NEXT5_SYNTHESIS.md; analysis/RH_INVARIANT_TANGENT_AUDIT.md. Existing: local positive reflection cocycle, not the full Weil functional.
4. Artin–Ihara: analysis/PASS4447_ZETA_AND_SIGNING_ARE_ONE_SUBJECT.md; analysis/w33_pass4461_line_signing_apartment_trace.py; analysis/w33_pass4409_4410_signings_and_larger_graphs.py. Existing: signed graph L-functions and the exact 1620 Levi apartments.
5. Infinite operator: docs/RH_CASEY_W33_CORRESPONDENCE_ANALYTIC_OPERATOR_SYNTHESIS.md; analysis/w33_preregistered_higher_moment_search.py; analysis/w33_rh_correspondence_analytic_operator.py. Existing: inverse-log tower no-go and Lambert-W approximate counting ladder.

## Frontier 1 — Standard Hecke law, with a rigorous boundary

For a(n)=sigma_3(n), the normalized E4 eigenform has a(pn)+p^3 a(n/p)=(1+p^3)a(n). Tested 1200 integer cases: primes 2,3,5,7,11 and integers n=1,...,240. The Hecke eigenvalues are 9,28,126,344,1332. The scalar E4 Hecke eigenspace is one-dimensional. Putting its scalar action on W33's constant eigenspace is tautological, not an arithmetic equivariant Hecke action on W33's nonconstant 24D and 15D sectors. The latter remains open.

## Frontier 2 — Constructive rational Levi/Frobenius module

Let N be W33's 40x40 point-line incidence and let L=[[0,N],[N^T,0]]. Its rational projectors onto L^2 eigenvalues 16,6,0 are P16=L^2(L^2-6I)/160, P6=L^2(16I-L^2)/60, P0=(L^2-6I)(L^2-16I)/96, of ranks 2,48,30.

The 160D Bass companion T=[[L,-3I],[I,0]] obeys (T^4+9I)diag(P6,P6)=0 on 96D and (T^2+3I)diag(P0,P0)=0 on 60D.

The verifier provides 24 explicit integer Krylov generators of length 4 and 30 of length 2, with rank 96 and 60 modulo 101. This proves the 156D nontrivial transfer representation over Q is the direct sum of 24 companion modules Q[x]/(x^4+9) and 30 Q[x]/(x^2+3). These polynomials are exactly the local F3 Frobenius characteristic polynomials of the previously constructed genus-two curve y^2=x^5+1 and elliptic curve y^2=x^3-x.

**Novel scope:** explicit rational module blocks, stronger than matching polynomial multiplicities. Actual etale cohomology is Q_l-linear, and no canonical Galois-equivariant, geometric, or Sp(4,3)-equivariant map has been obtained. Local identification is not a global classical L-function.

## Frontier 3 — Off-line Weil-type negative control

For a toy quartet of ordinate values z=+/-14 +/-0.2i and f(z)=sum_j c_j exp(i*x_j*z), the finite spectral-side form Q(f)=sum_z f(z)f(-z) has real symmetric Gram matrix K_ij=4cos((x_i-x_j)*14)cosh((x_i-x_j)*0.2). Choosing x=(0,2*pi/14) gives eigenvalues -0.01612446146895 and 8.01612446146895; the on-line version has eigenvalues 0 and 8.

Tensoring K with the nonzero positive W33 projectors P2 and Pminus4 preserves the negative eigenvalue with multiplicity 24 and 15 respectively. Finite projector positivity cannot force universal Weil positivity by itself.

**Boundary:** This is a finite quartet countermodel, NOT the full arithmetic Weil form. No classical RH claim.

## Frontier 4 — One-edge Levi Artin–Ihara twist

The Levi graph has 1620 simple octagons, 160 edges, and 81 octagons through each incidence edge. Negating one signed edge changes the length-eight closed-walk trace by 32*81=2592, verified by integer matrix powers: trace(L^8)=193280 and trace(L_signed^8)=190688. Gauge-conjugate vertex signings preserve trace.

For this one-edge twist the spectral radius is about 3.97311724355, exceeding the 4-regular tempered bound 2sqrt(3)=3.46410161514. Thus its twisted Artin–Ihara factor does not satisfy graph RH on the radius 3^(-1/2). A flat graph sign character is not automatically a pure weight-one Frobenius sheaf.

This respects the work of Stark–Terras on graph-cover Artin L-functions. The unrestricted Bilu–Linial conjecture has a September 2026 counterexample (Xu arXiv:2609.15591); the Ramanujan-base restriction is a separate open question.

## Frontier 5 — Compact-resolvent infinite diagonal scaffold

Use t_n=2*pi*(n-7/8)/LambertW((n-7/8)/e) and phases theta2=acos(1/sqrt(11)), theta_minus4=acos(-2/sqrt(11)). Define an infinite diagonal operator on l2(N) with eigenvalues t_n+0.05*(24cos(n theta2)+15cos(n theta_minus4))/39.

The modulation is bounded by 0.05 and t_n tends to infinity, so the diagonal realization is self-adjoint with compact resolvent and retains the leading Riemann-von Mangoldt counting class TlogT without multiplying the coefficient by 39. The first-20-zero mean relative error changes from 4.8830% baseline to 4.8780% with this untuned phase modulation. This is a negligible numerical improvement, not evidence of spectral equality. Eventual monotonicity of the diagonal entries is not asserted. No determinant equality to completed Xi or zeta-zero matching is proved.

## Why these five do not solve classical RH

The exact finite graph Hecke/Frobenius operators and finite Weil-toy quadratic form are not the same object as the global Riemann explicit formula. A real RH proof still requires either (i) a universally positive *completed arithmetic* Weil form for all admissible tests, or (ii) an exact self-adjoint operator determinant equal to completed Xi, including multiplicities and analytic regularization. Local characteristic polynomial equality, finite rank positivity, and a correct leading zero-density law are insufficient.

## External literature considered

- Eisenstein Hecke eigenforms: https://www.lolathompson.com/uploads/1/1/0/6/110629329/sarajevo2.pdf
- Ihara-Bass, ICM 2026: https://epubs.siam.org/doi/10.1137/25M1805862
- Graph-cover Artin L-functions: https://www.sciencedirect.com/science/article/pii/S0001870800919170
- Bombieri-Lagarias Li/Weil criterion: https://www.sciencedirect.com/science/article/pii/S0022314X99923922
- Connes–Consani–Moscovici, Zeta Spectral Triples (2026): https://alainconnes.org/2026/07/zeta-spectral-triples/
- Xu Bilu–Linial counterexample (2026): https://arxiv.org/abs/2609.15591

## Five independent follow-up targets

1. Prove or refute a nonconstant Hecke-equivariant map from E8 modular coefficients into W33 sectors.
2. Construct the 156x156 rational conjugator explicitly and test geometric and Galois symmetry compatibility.
3. Compute the **completed** arithmetic Weil Galerkin form with prime, gamma, and pole terms and independently certified interval bounds.
4. Classify all Levi apartment-holonomy signing classes and which twisted Ihara L-factors are tempered.
5. Benchmark the arithmetic spectral triple against W33 scalar perturbations, testing individual ordinates, all inverse moments, and normalized Fredholm/regularized determinants.
