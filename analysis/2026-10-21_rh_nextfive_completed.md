# 2026-10-21 — Five deeper RH research frontiers: exact algebra, genuine explicit formula, and falsifiers

**Classical Riemann Hypothesis: OPEN.** All five are scoped algebraic/numerical research outcomes, not a proof. Producer: analysis/w33_20261021_rh_nextfive.py; focused tests: tests/test_w33_20261021_rh_nextfive.py; CI: .github/workflows/w33-rh-nextfive.yml. GitHub Actions regenerates data/w33_20261021_rh_nextfive_certificate.json.

## Search-before-work: what the repository already contained

1. Nonconstant Hecke: PASS7385_7400_EISENSTEIN_E8_W33_BRIDGE.md (Eisenstein E8 gives a concrete 40-orbit W33 geometry); analysis/PART_CCCCCXCIX_E8_SPECTRAL_SCOPE_AUDIT.md (noncanonical numerical analogies rejected); analysis/w33_theta_E8_eisenstein_E4.py (classical theta E8 = E4); analysis/w33_pass4956_point_line_24d_intertwiner.py (an actual incidence intertwiner). This pass seeks an obstruction to mapping E4's **trivial** eigenspace to W33's nontrivial packets, not another 240-root counting identity.
2. Levi conjugator: analysis/w33_20261021_levi_genus2_frobenius.py; analysis/w33_20261021_rh_five_frontiers.py; analysis/2026-10-21_levi_genus2_local_frobenius_bridge.md. The preceding pass proved 24 quartic and 30 quadratic rational companion summands by a modular rank certificate. This pass constructs their full 160×156 **integer** embedding and transports a concrete nontrivial GQ symplectic automorphism.
3. Completed Weil Galerkin: analysis/w33_weil_cocycle_positivity.py and docs/RH_CASEY_W33_NEXT5_SYNTHESIS.md already contain positive orbit-level kernels and finite scans, **not** a genuine complete prime/gamma/pole numerical comparison. This pass evaluates the entire Guinand–Weil formula on an explicit Gaussian test family; it does **not** assert interval-verified positivity or universal positivity.
4. Apartment holonomy: analysis/w33_pass4461_line_signing_apartment_trace.py gives 1620 octagons and fourth-moment identities; analysis/PASS4447_ZETA_AND_SIGNING_ARE_ONE_SUBJECT.md identifies signed graph Artin–Ihara L-factors. This pass computes the **binary span** of all octagonal cycle incidence vectors, a distinct structural invariant.
5. Infinite operator: analysis/w33_preregistered_higher_moment_search.py and docs/RH_CASEY_W33_CORRESPONDENCE_ANALYTIC_OPERATOR_SYNTHESIS.md already establish failed prime towers and an approximate Lambert-W scaffold. This pass uses the analytic Xi Taylor coefficients and normalized Xi values to **falsify exact spectral matching** for a W33-modulated scaffold.

## Frontier 1 — Rigorous obstruction for the naive scalar Hecke intertwiner

The W33 point action is transitive. Hence its 40D permutation representation has a one-dimensional invariant subspace spanned by the all-ones vector. The two nontrivial Bose–Mesner projectors
P2=(2/3)I+(1/6)A-(1/15)J and Pminus4=(1/3)I-(1/6)A+(1/24)J annihilate that invariant vector. Since the normalized E4 Eisenstein Hecke eigenline is one-dimensional with trivial geometric W33 group action, every W33-equivariant linear map from this source into either the 24D or 15D constituent is zero:
Hom_G(1,V24)=Hom_G(1,V15)=0.
The verifier explicitly reconstructs a nontrivial symplectic transvection, the permutation action, and the spectral projectors.

**Consequence:** the **scalar** Hecke eigensystem 1+p^3 cannot be attached to the nonconstant W33 sectors through an equivariant map from a trivial source. A new, richer source representation or a weaker/different equivariance notion would be required. This does not rule out every Hecke construction.

## Frontier 2 — Explicit 160×156 Levi/Frobenius companion conjugator and equivariant transport

Let N be the 40×40 point-line incidence matrix, L=[[0,N],[N^T,0]] and T=[[L,-3I],[I,0]]. Define Q6=L²(16I-L²) and Q0=(L²-6I)(L²-16I), integer multiples of the exact squared-eigenspace projectors.

The producer materializes the complete integer 160×156 Krylov column matrix S: 24 seeds times four T iterates from Q6, and 30 seeds times two iterates from Q0. It forms the block companion operator C consisting of 24 copies of the companion for x^4+9 and 30 copies for x²+3. It verifies the exact integer equality

TS=SC.

The full rational rank of S is certified by a rank-156 minor invertible modulo 101; the algorithm publishes pivot rows, seed indices, and a SHA256 digest of the integer column data. This explicitly constructs an injective Q[x]-module intertwiner with the direct sum of local genus-two/elliptic Frobenius blocks. No 156×156 dense inverse needs to be misrepresented as integral.

A concrete order-three projective symplectic transvection on W33 points and lines induces an 80×80 permutation G with GL=LG. Lift it to H=diag(G,G). The rational action on S(Q^156) is transported to a 156×156 matrix M over F101 by solving S M=H S; the verifier checks MC=CM, M³=I, a nontrivial M, and no mixing between quartic and quadratic summands.

**Boundary:** Transporting an automorphism to an abstract companion module is formal once S exists. There is still NO canonical action on the actual etale cohomology of C/F3 and E/F3, no morphism of motives, and no all-prime identity.

## Frontier 3 — Numerical *completed* Weil explicit formula, not merely a toy quartet

For a=0.025 and d in {0, 0.5, 1, 1.5}, take the even entire test

h_d(t)=exp(-a t²) cos(d t).

The completed Riemann explicit formula for such tests gives, writing \hat h(u)=integral_R h(t)e^(-iut)dt,

sum_rho h_d((rho-1/2)/i) =
2 exp(a/4) cosh(d/2)
+ (1/pi) integral_0^infty h_d(t) [Re psi(1/4+i t/2)-log pi] dt
- (1/(2 pi)) sum_{n>=2} Lambda(n)/sqrt(n) [\hat h_d(log n)+\hat h_d(-log n)].

(The hats are sums of two Gaussian translates; the factor 1/(2pi) is crucial.) The code evaluates all three ingredients: pole terms, gamma term, and actual von Mangoldt prime-power terms. It compares the arithmetic total against a spectral sum using the first 30 known positive ordinates, paired with their negative ordinates.

Finite cutoffs: prime powers n<=400, archimedean quadrature t<=50. The four numerical cross-check discrepancies are below 5e-10, with typical actual differences around 1e-14. Form the 4×4 Toeplitz Galerkin matrix on x={0,0.5,1,1.5}; its tested eigenvalues are positive.

**Critical qualification:** This is a valuable numerical verification of the FULL formula, not a rigorous certified interval enclosure. These Gaussian test transforms are not compactly supported, and all truncations need mathematically controlled tails. A finite positive matrix cannot prove the Weil criterion, which requires every admissible test function and all matrix sizes.

## Frontier 4 — The 1620 apartments span the ENTIRE Levi binary cycle space

Construct the 160 incidence edges of the 80-vertex Levi graph as coordinates of F2^160. For each of the 1620 simple point-graph C4's, collect its eight incidence flags in the corresponding Levi octagon. Gaussian elimination over F2 on all 1620 160-bit masks returns rank exactly **81**. Independent graph topology gives cycle-space dimension |E|-|V|+1=160-80+1=81, so these particular girth-eight octagons generate *every* cycle over F2.

A Z2 edge signing has holonomy +1 around all apartments if and only if the signing is a vertex-switching coboundary. The annihilator of the octagon span has dimension 160-81=79, exactly the connected-graph gauge-boundary space of dimension |V|-1. Every incidence edge appears in precisely 81 apartment octagons.

This is a complete finite Z2 holonomy detector. It does NOT classify all 2^81 gauge inequivalent classes into tempered vs nontempered Artin–Ihara factors, and doesn't transfer to a global Dirichlet L-function.

## Frontier 5 — Quantitative Xi determinant and inverse-moment falsifier

Use the previously registered self-adjoint compact-resolvent diagonal scaffold

t_n=2pi(n-7/8)/W((n-7/8)/e),
lambda_n=t_n+0.05 [24 cos(n theta_2)+15 cos(n theta_{-4})]/39,

with theta_2=acos(1/sqrt(11)), theta_{-4}=acos(-2/sqrt(11)). Evaluate the first 3000 eigenvalues.

Compare its inverse even moments sum_n lambda_n^(-2k), k=1,2,3, against exact Taylor coefficients of the completed xi function at s=1/2:
S_{2k}=(-1)^(k+1) k [z^(2k)] log(xi(1/2+z)/xi(1/2)).
Those analytic Taylor coefficients are defined independently of assuming RH. The model has nonzero, sizeable discrepancies. Next compare the finite symmetric canonical product Prod_{n<=3000}(1-x²/lambda_n²) against Xi(x)/Xi(0)=xi(1/2+ix)/xi(1/2) at x=1,5,10. At x=10 the relative mismatch exceeds **50%**. Therefore correct leading TlogT zero counting and bounded W33 modulation do not produce the correct Xi function.

**Boundary:** This is a negative numerical test of a particular toy scaffold, not a no-go theorem for all arithmetic spectral triples, and no rigorous infinite determinant equality has been established.

## External verification anchors

- Bombieri–Lagarias, Li and Weil positivity: https://websites.umich.edu/~lagarias/doc/bombieri.pdf
- Connes–Consani–Moscovici, Zeta Spectral Triples (2026): https://arxiv.org/abs/2511.22755
- Connes website and 2026 monograph: https://alainconnes.org/2026/07/zeta-spectral-triples/
- Xu, A 3-regular counterexample to the Bilu–Linial signing conjecture (September 2026): https://arxiv.org/abs/2609.15591

## Five INDEPENDENT subsequent research choices

1. Find a nontrivial W33-equivariant, Hecke-stable source module: compute representation characters, and reject possible automorphic candidates with Hom-dimension zero.
2. Test actual Galois/geometric equivariance, beyond transported linear algebra, between the 156D Levi module and the genus-two/elliptic cohomology factors. Compute the automorphism groups and Frobenius centralizers first.
3. Convert the completed Weil quadrature into *rigorously bounded* interval arithmetic, with explicit gamma/prime tails and expanding Galerkin matrices. A proof would require uniform analytic inequalities, not just numerical checks.
4. Enumerate orbits of Z2^81 signing classes under W33 automorphisms using the complete apartment parity coordinates; sample tempered strata and search exact obstructions to finite-field purity.
5. Take a true all-prime Connes–Consani–Moscovici operator (not a generic Lambert-W scaffold), compute its determinant convergence and perturb with W33 only if the all-prime trace and normalization survive.

**No classical RH proof is claimed in this or prior finite certificates.**
