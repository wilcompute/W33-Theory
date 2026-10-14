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


## Independently verified GitHub Actions results — 14 October 2026

**Successful run:** https://github.com/wilcompute/W33-Theory/actions/runs/38637198595. **Seven tests passed in 77.06 seconds**, then all five source-regenerating producers and the audited evidence summary completed, with a downloadable JSON certificate ZIP. Verified sources were in commit 3fb7a3c4ea21fdc87bbc020f8691769e65540867.

### New exact quantum combinatorial result — 27 regular symmetry orbits

The former TOE72 baseline contained seven disjoint full PGSp(4,3) orbits of 20-octagon edge covers, each with 51,840 elements. TOE74 discovered 20 additional two-local-pairing-flip neighbors of the seven *representative covers*, explicitly declining to label them 20 new orbits. TOE75 first verified that **every one of the 20 neighbors lies outside the whole seven previous orbits**, rather than merely differing from the original seven representatives.

The new independent exhaustive group audit enumerates the entire full PGSp orbit of *each* of those 20 neighbors. **Each new orbit is a different regular 51,840-member orbit, with trivial stabilizer.** Consequently:

\[
\boxed{\text{at least 27 pairwise distinct PGSp(4,3) orbits}},
\qquad
\boxed{\text{at least }27\cdot51840=1{,}399{,}680\text{ distinct exact covers}}.
\]

The exhaustive group search checks membership and orbit size, not an arbitrary canonical-label heuristic. All 20 candidate neighbor identifiers are classified; **it does not follow** that all possible ground covers or all further-distance orbit classes are now known. The prior nine-matching friendship graph F3 remains a *deliberately restricted* transition model, not the complete physical quantum-cover adjacency. The full 20-seed orbit data are now frozen in data/w33_20261014_toe75_full_orbit_census.json, in addition to the regenerated CI certificate.

### New exact native-theta free-fermion theorem — global 120-degree phases

The native overlapping-octagon subgraph is a three-arm, equal-length Theta(4,4,4) graph. Its 11-site bipartition has 5 and 6 vertices, with 5 fermions at the canonical particle number. Choose path-phase differences \(\phi_1,\phi_2\), and define
\[
s=|1+e^{i\phi_1}+e^{i\phi_2}|\in[0,3].
\]
An exact 5-by-5 Gram factorization of its uniform free hopping matrix yields
\[
\det(\lambda I-TT^\dagger)=
(\lambda-2)\big[(\lambda^2-5\lambda+3)^2-s^2\big].
\]
The *exact* five-fermion ground energy is
\[
E_0(s)=-\sqrt2-\sqrt{5+2\sqrt{3+s}}-
                   \sqrt{5+2\sqrt{3-s}}.
\]
Since \(g(t)=\sqrt{5+2\sqrt t}\) is strictly concave, \(g(3+s)+g(3-s)\) is maximized **uniquely** at \(s=0\). The latter forces the three arm phasors to be the cube roots of unity. Thus, modulo \(2\pi\), the **only global free-fermion flux minimizing pairs** are
\[
\boxed{(\phi_1,\phi_2)=(2\pi/3,4\pi/3)
\ \ \text{or}\ \ (4\pi/3,2\pi/3)}.
\]
They are symmetry and time-reversal partners on the equal-arm graph. The exact free ground energy is
\[
E_0=-7.232839384725914,
\]
and it lies **0.020693170421004936** below the three exactly degenerate nonzero Z2 corners (which previously appeared to be favored because the old phase grid did not cover both sides of \(\pi\)). The derivation is analytically complete for this **11-site free theta subgraph**, and CI independently checked the analytical eigenvalue polynomial and 462-state many-body energies at eight phase points.

This is an instance of quantum interference on a highly symmetric three-arm graph and is **not** known to be uniquely W33-specific. It neither disproves Lieb's 1994 flux-phase theorem (its hypotheses differ), nor overrides TOE67's full 80-site free W33 analysis. Prior-art context: Elliott Lieb, Phys. Rev. Lett. 73, 2158 (1994), DOI 10.1103/PhysRevLett.73.2158; Goller and Porta, J. Stat. Phys. 193, 60 (2026), DOI 10.1007/s10955-026-03617-y; interacting frustrated fermion networks, arXiv:1110.2224.

### Numerical interacting and finite-temperature follow-up

Using the *full 462-dimensional canonical N=5 many-body matrix* at all continuous flux choices, four-start two-dimensional numerical local minimization selects points close to the exact free 120-degree pattern for V=.2,1,4. Separate complete 462-level finite-temperature traces show positive free-energy differences relative to nontrivial Z2 flux, at selected beta values. The following are **numerical finite-model comparisons**, not a global continuous interacting theorem.

| repulsion V | 2D locally optimized ground energy below best nontrivial Z2 | Z2 minus optimized-background canonical free energy at beta=2 |
|---:|---:|---:|
| 0 | 0.02069317042 | 0.00530269256 |
| 0.2 | 0.02133223583 | 0.00576525930 |
| 1 | 0.02129397173 | 0.00695968060 |
| 4 | 0.00174210959 | 0.00148148402 |

For all four V, the sampled pointwise Z2-minus-optimized free-energy differences were also positive at beta=0.5, 1 and 8 (though some at small beta are only order 10^-5). **Pointwise positive differences do not prove a globally preferred finite-temperature flux**. The new fully numerically evaluated phase points cluster around (2pi/3,4pi/3) and its phase-swapped partner. Any conclusion about spontaneous time-reversal/CP breaking or dynamical-gauge vacuum remains unwarranted.

### Rigorous gauge spectral and geometry controls

The exact rational 22,638-dimensional P-block basis calculation gives an **unconditional ordered second-eigenvalue upper bound** for the full unbounded two-loop rotor of
\[
\boxed{E_1\le387/200=1.935}.
\]
The earlier coarse rigorous \(E_0\in[-9.983,-0.001]\) remains valid. **No nonzero full spectral-gap lower bound** is established by these two inequalities.

The actual local 2D cellular square complex on two native Levi graphs has (6400,25600,25600) cell counts, verifies \(d_1d_0=0\) exactly, and has Kunneth Betti (1,162,6561) and Euler–Kahler-Dirac index 6400. It is *not* a four-dimensional spin lattice. The distinct closed W33-squared surface product has Euler index 25600 and untwisted **spin-Dirac index zero**. This remains an unsolved 4D chiral-fermion construction, and no false chirality is inferred.

## What the expanded pass did not solve

An exact all-edge disorder minimax threshold; a rigorous positive full unbounded-rotor gap; a complete quantum pairing Hamiltonian ground state or proof these 27 cover orbits exhaust the full cover set; a native admissible 4D spin/overlap Dirac construction; or a dynamically interacting, experimentally confirmed 80-site W33 quantum field theory. The newly demonstrated 120-degree phase theorem is *specific to the 11-site native subgraph*, not a general Theory of Everything.
