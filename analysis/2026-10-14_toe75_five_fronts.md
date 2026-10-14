# TOE75 — Five-front research and reproducibility report

Date: 2026-10-14. This pass follows TOE74 and keeps exact finite-model mathematics distinct from numerical finite-size observations and unresolved physical hypotheses.

## 1. Realizable global disorder bracket

Reconstruct the native 160-edge graph and 159 octagons active in the antisymmetric holonomy Hessian direction q=(0,-1,1). Verify using arbitrary-precision integer arithmetic that the 17-high-edge witness has strictly positive Rayleigh numerator at epsilon=24461518/100000000 and strictly negative numerator at 24461519/100000000.

Independently check the TOE64 exact signed-square sufficient condition for *every independent hopping assignment on all 160 links* at epsilon=1/7. Writing r=((1+epsilon)/(1-epsilon))^8=(4/3)^8, the symmetric Sylvester terms are 79-2r and (79-2r)(77-r)-2r^2, and the antisymmetric term 77-7r; all are strictly positive. The full TOE64 theorem gives the stronger sufficient bound epsilon <= (11^(1/8)-1)/(11^(1/8)+1) ≈ 0.1487564016. Thus the true universal disorder-tolerance boundary for the *leading high-temperature free-fermion holonomy potential* is bounded below by the TOE64 algebraic number and above by the native 17-edge negative Hessian witness just above 0.24461518. This is not an exact global 160-dimensional minimax determination.

## 2. Genuine ordered spectral progress without trusting Ritz eigenvalue ordering

On the native 11-site, 12-link, five-fermion, two-electric-coordinate patch, enumerate every one of the 22,638 finite electric-cutoff basis states and compute exact rational diagonal matrix elements. Select two low-diagonal basis states with zero *exact* direct hopping/Wilson matrix element. The Courant-Fischer min-max theorem then gives a rigorous upper bound on the ordered second eigenvalue of the full unbounded-electric-flux Hamiltonian: E1 <= max(Hii,Hjj). Retain TOE74's rigorous coarse E0 bracket. A lower E1 enclosure and hence a positive E1-E0 gap remain open; the prior 0.9229 conditional estimate is not promoted to a theorem.

## 3. Full symmetry membership audit for 20 previously unclassified cover neighbors

The seven known 20-octagon exact-cover orbit seeds have 20 further locally reachable ground-cover identifiers that TOE74 correctly left unclassified. Enumerate the *full* 51,840-state PGSp(4,3) orbit of each of the seven seeds using native point-line symplectic transvections and the outer similitude, and determine exactly which of those 20 neighbor identifiers belong to the existing orbits. If some do not, explicitly enumerate the orbit of one new candidate. This counts true symmetry orbit membership, not naive inequality between seven seed representatives. It does not classify the full 3^80 quantum state space.

## 4. Exact local cochain and Dirac index control

Construct the actual sparse cellular complex on the Cartesian product of two native W33 Levi graphs, with 6,400 vertices, 25,600 directed product edges and 25,600 squares. Build the integer cochain differentials d0=[B tensor Iv; Iv tensor B] and d1=[-Ie tensor B, B tensor Ie], directly assert d1*d0=0, and derive integer Betti numbers (1,162,6561), Euler/Kahler-Dirac index 6400, and cochain differential ranks (6399,19039). This is explicitly a 2D square complex, **not** the closed 4D product of genus-81 handlebody-boundary surfaces. The latter has Euler/de Rham index 25600 and *untwisted spin-Dirac index 0*. The distinction prevents a spurious claim of physical chirality. No 4D overlap spinor stencil or gauge-anomaly proof is derived.

## 5. Finite interacting continuous holonomy, temperature, and degeneracy controls

The exact native 11-site theta graph has 462 canonical five-particle Fock states. Its three nonzero Z2 flux sectors are exactly isospectral by S3 arm permutations, correcting TOE73's apparent flux-corner switching. Optimize the interacting U1^2 phase numerically along the full pi-boundary segment and from four local starts in the continuous 2D phase chart at V=0,.2,1,4, independently evaluate eigenvector residuals, and compare with exact Z2 controls. Compute all 462 eigenvalues at the optimized boundary phase and a Z2 phase, yielding full canonical finite-temperature free-energy differences at inverse beta 0.5,1,2,8. Sampled-grid and multistart minima are not rigorous global continuous minima, a thermodynamic phase, or physical CP violation.

## External prior art and verification

Checked the verified interval eigenvalue/inertia approach from Liu and Yanagisawa's veigs software, the Kähler-Dirac versus spin/chiral fermion literature, and the existing native W33 research. Verified spectral methods require controlled ordered eigenvalue enclosures (such as interval LDL / inertia), rather than treating ordinary Ritz residuals as an eigenvalue-ordering proof. Related work: Adams, arXiv:0912.2850 and Physical Review D 104, 014503 (2021).

The separate GitHub Actions workflow executes the independent source-generating tests and writes certificates to a downloadable Actions artifact. As always, the workflow's actual completion status must be verified before claiming all results reproduced.

## Five independent successors

1. Exact global 160-link/full-Hessian minimax certification, using interval branch-and-bound or rational polynomial SOS and native symmetries.
2. Ordered E1 lower bound from verified sparse LDL inertia, completing or falsifying the unbounded rotor positive-gap argument.
3. Full PGSp-quotient quantum cover adjacency and low-energy symmetry-sector spectra, including any newly classified orbits.
4. A genuinely local 4D spin/overlap-Dirac construction on the W33-derived surface-product manifold, with admissible gauge fields and index/anomaly checks.
5. Interval-certified full-continuous interacting-flux minima with current susceptibilities and dynamical Gauss law, compared with independent graph controls.

This is finite mathematical/physics modeling progress; the physical Theory of Everything remains unresolved.
