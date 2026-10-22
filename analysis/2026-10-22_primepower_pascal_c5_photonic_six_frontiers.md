# Six W33 research frontiers: prime-power Pascal ranks, cyclotomic Galois obstruction, photonic signed cycle, generalized bases and RH audits

**Date:** 22 October 2026. **Status:** exact finite mathematics plus narrowly scoped numerical experiments. Classical Riemann RH and any proposed physical TOE remain open.

## Repository search and corrections

The prior prime-only Pascal rank program is analysis/w33_20261022_pascal_jordan_w3p.py. Other preexisting contributions include the genus-two local Frobenius polynomial family, the positive weighted-metric Levi companion, the small finite-prime CCM matrix, completed 2x2 smooth Weil tests, and golden/supergolden Pascal-base analogues. This release extends or tests their interfaces, not all their underlying theorems.

The historical file passes/pass_1304_jordan_census_prime_power.py concerns **different binary point-line incidence maps**, and even records unresolved contradictory claims about kernel dimensions of transpose maps. It is not a proof of this report's defining-characteristic point-point noncollinearity rank. Do not conflate the two.

## Frontier 1: Exact prime-power Pascal/Jordan law

For q=p^t, the symplectic generalized quadrangle W(3,q) point graph A has v=(q+1)(q^2+1) vertices. Let B=J-I-A over Fp; B detects nonorthogonality.

  B_[x],[y] = <x,y>^(q-1).
  B^2=0 mod p.
  rank_Fp B = binomial(p+2,3)^t.

Proof: the columns are evaluations of powers of linear forms in four variables. In characteristic p the multinomial coefficients for degree q-1 survive exactly for exponent quadruples whose base-p addition into q-1 has no carries. Each of t digit positions has binomial(p+2,3) possible weak compositions of p-1. These monomials are independent as polynomial functions because all variable exponents are below q, and powers of all nonzero linear functionals span the indicated subspace. The square-zero identity follows from the strongly regular graph parameters reduced modulo p. The theorem agrees with established modular symplectic incidence representation theory; we do **not** claim a first discovery.

Independent finite-field implementations and exact row elimination verified:

| q | characteristic | vertices | rank B | size-one Jordan blocks |
|---:|---:|---:|---:|---:|
| 3 | 3 | 40 | 10 | 19 |
| 4 | 2 | 85 | 16 | 52 |
| 8 | 2 | 585 | 64 | 456 |
| 9 | 3 | 820 | 100 | 619 |

Size-two Jordan blocks at eigenvalue -1 number rank B. The nonconstant complement has v-1 dimensions. The rank fraction tends to zero as t grows at fixed p, yet B is not the zero operator and the module is not diagonalizable over an extension field merely because its rank fraction shrinks.

## Frontier 2: Symplectic order-five C5 character versus the curve's noncommuting mu5

A reproducible order-five symplectic permutation of W33 points and its 40 lines induces G on the 80-vertex Levi graph. It commutes exactly with Levi adjacency and the Bass transfer. Rational projector traces on nontrivial transfer sectors:

  quartic 96D traces at g^0,...,g^4: 96,-4,-4,-4,-4
  quadratic 60D traces: 60,0,0,0,0.

Therefore their rational C5 modules decompose into:

  96D = 16 trivial + 20 copies of four-dimensional Q(zeta_5).
  60D = 12 trivial + 12 copies of four-dimensional Q(zeta_5).

For the curve C:y^2=x^5+1, the obvious geometric automorphism sigma(x,y)=(zeta_5*x,y) satisfies F sigma F^-1=sigma^p under arithmetic Frobenius, whereas p mod5 has order four for p=3 or 7 mod20. It **does not commute with Frobenius**. Consequently the commuting graph C5 action cannot be identified with this particular curve mu5 action by a simultaneous equivariant operator intertwiner. Other geometric correspondences and twisted semidirect-product descent C5 semidirect C4 remain possible.

This is a precise no-go for one natural construction, not a theorem ruling out all Galois-compatible motives.

## Frontier 3: Exact diagonal-loss tolerance of a signed four-mode circuit

For the signed cyclic permutation U4 with U4^4=-I and arbitrary fixed complex diagonal mode matrix D,

  (D U4)^4 = -det(D) I.

For signed two-mode swap U2, (D U2)^2=-det(D)I.

This follows because a cyclic orbit visits every diagonal weight once per cycle and accumulates the single negative wrap sign. If det D is nonzero, **postselected normalized states** return exactly under fixed unequal attenuation and phase shifts. Survival probability and photon flux are not restored. A 3% off-diagonal crosstalk perturbation produces a nonzero four-step residual near 0.05257 in the numerical test. Time-varying loss and mode-mixing errors fall outside the exact robustness theorem. The raw Levi Bass companion is nonunitary in the ordinary Euclidean optical norm; only its weighted-metric signed-permutation surrogate is passive unitary.

## Frontier 4: Golden versus supergolden base companion phase falsifier

The standard golden companion for x^2-x-1 and the cubic Pisot supergolden companion for x^3-x^2-1 have modular matrix orders:

| modulus p | golden | supergolden |
|---:|---:|---:|
| 2 | 3 | 7 |
| 3 | 8 | 8 |
| 5 | 20 | 31 |
| 7 | 16 | 57 |
| 11 | 10 | 60 |
| 13 | 28 | 168 |

At p=3, x^3-x^2-1 factors (x+1)(x^2+x-1), producing an F9 quadratic constituent; the shared order eight is thus not a unique intrinsic phinary quantum clock. Distinct moduli immediately falsify a universal identification. This work retains the established exact prime-power curve basechange controls from the preceding research pass.

## Frontier 5: Actual finite-prime CCM and smooth compact-support Weil controls

The small N=4, cutoff-13 finite-prime Connes–Consani–Moscovici matrix and smooth compact-support two-function Weil test are rerun. The next parameter sensitivity experiment scans N=4 and 5 and cutoff 13 and 14 to expose the ill-conditioning of near-zero Weil eigenvalues under float64 arithmetic. A successful small-N eigenvalue approximation is **not** the paper's corrected-metric high-precision N=120 spectral triple. The Weil test has numerical gamma integrals, not interval-certified universal positivity.

The GitHub-verified cutoff scan found these absolute first-zero errors: N=4 at cutoff 13: 7.43345108e-5; N=5 at cutoff 13: 1.19522088e-6; N=4 at cutoff 14: 1.00138615e-3. The corresponding smallest computed Weil eigenvalues are 9.60717e-15, 1.19371e-17, and 5.81626e-15, respectively. The N=5 eigenvalue spread is around 6.4e16, meaning float64 eigenvector stability is inadequate for large-N claims. Increasing prime cutoff at fixed small N need not monotonically improve individual zeros. These are finite numerical diagnostics only.

The rank-two W33 bright-channel coupling still fails to determine a canonical prime-dependent trace and leaves 37 dark modes, so unmodified Hilbert-Polya Xi determinant equality is unavailable.

## Code, CI and reproducibility

Producer files: analysis/w33_20261022_six_algebra_optics_frontiers.py and analysis/w33_20261022_beta_ccm_sensitivity.py.

Regression: tests/test_w33_20261022_six_algebra_optics_frontiers.py. Workflow: .github/workflows/w33-primepower-pascal-c5-optics.yml.

The workflow generates data/w33_20261022_six_algebra_optics_frontiers.json and data/w33_20261022_beta_ccm_sensitivity.json, publishes them as GitHub Actions artifacts, and checks the strict classical_RH_proved=false firewall.

External sources: Chandler, Sin, Xiang on finite symplectic incidence p-ranks (https://arxiv.org/abs/math/0603100); Connes, Consani, Moscovici (2026), Zeta Spectral Triples (https://ems.press/books/elm/323/6477); independent multiprecision replication (https://github.com/giuseppesorge/zeta-spectral-triples-replication).

## Five top independent next steps

1. Derive and test all composition factors of the Sp(4,p^t) modular point-point module, not just its square-zero Jordan ranks; compare separately against the proper point-line p-rank formulas.
2. Investigate twisted C5 semidirect C4 descent in genus-two Jacobian cohomology and compute explicit character obstructions to any full symplectic-equivariant graph morphism.
3. Establish interval-certified completed Weil positivity for smooth compact test families using independent Arb/ball bounds, nontrivial negative controls and explicit prime/gamma/pole error budgets.
4. Reconstruct high-precision corrected-metric Connes–Consani–Moscovici matrices for N=40/80/120 and several prime cutoffs, with no fitted zeta zeros, and test Xi determinant convergence.
5. Design a complete passive two-/four-mode optics error budget for U2/U4 with static and drifting diagonal attenuation, off-diagonal crosstalk, survival probability, heralding requirements and physical metric encoding.

**Scientific boundary:** none of these exact finite-field or circuit identities proves classical Riemann RH, quantum gravity or an experimental photon computer.
