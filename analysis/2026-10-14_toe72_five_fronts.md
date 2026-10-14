# TOE72 — Five independent W33 physics fronts: multidirectional hopping, stronger unbounded-gauge bound, seven quantum-cover orbits, W33-squared chirality obstruction, exact interacting benchmark

**14 October 2026. Parent:** TOE71 \`fbbad366d4b3c03103436eed9a248921a14131b5\` plus current parallel head. **Scientific scope:** finite native W33 combinatorics, exact arithmetic with explicitly scoped hypotheses, numerical mixed-integer and many-body diagonalization, and topology. No physical TOE or Standard Model has been derived.

## Intake and cross-comparisons

Reviewed the TOE67 all-positive-temperature continuous *uniform-free* determinant theorem, TOE66 native 17-edge disorder witness, TOE71 full 160-bit fixed-ray numerical MILP, TOE71 22,638-dimensional Gauss patch complement bound, TOE69–71 20-octagon cover construction and full \(PGSp(4,3)\) 51,840 orbit, TOE71 genus-81 boundary-manifold proposal, and full 80-site unrestricted Hartree–Fock producer. Cross-checked external spinless fermion exact-diagonalization comparisons, including Capponi–Läuchli, [arXiv:1505.01676](https://arxiv.org/abs/1505.01676), and [Phys. Rev. B 106, 205133 (2022)](https://doi.org/10.1103/PhysRevB.106.205133). Standard lattice gauge, graph and topological methods are prior art; the claims below concern the particular native W33 model.

## 1. All 160 links: six Hessian direction probes and an exact eigen-axis of the disorder witness

For the established 17-high-link / 143-low-link native edge pattern, reconstruct the **entire three-by-three phase Hessian** as an integer multivariate polynomial indexed by the number \(k\) of high links in each of the 238 winding octagons:

\[
H(\epsilon)=d^{-8}\sum_{k=0}^8 C_k(d+n)^k(d-n)^{8-k},\qquad\epsilon=n/d,\ C_k\in M_3(\mathbb Z).
\]

Exact coefficient identities hold at every \(k\): \((C_k)_{22}=(C_k)_{33}\) and \((C_k)_{12}=(C_k)_{13}\), with zero-based 2/3-coordinate labels corresponding to the final two deck directions. Therefore the antisymmetric vector \(q=(0,-1,1)\) is an **exact** eigenvector of the entire Hessian for **every** epsilon, not merely the direction selected from a numerical local search. Its unnormalized Rayleigh polynomial has coefficients \([0,0,72,46,34,0,0,0,-12]\) by high-edge count. The corresponding normalized eigenvalue first vanishes numerically at epsilon≈0.244615180371192 on the fixed witness; rational sign tests and integer matrices are exact. The other two eigenvalues remain positive near this root.

Independently build **six distinct full 160-edge MILP** optimization problems at exact epsilon=1223/5000=0.2446, with integer ray directions

\[
(0,-1,1),\ (1,0,0),\ (1,-1,0),\
(1,1,1),\ (1,1,-1),\ (0,1,1).
\]

All have positive reported minimum: approximately 0.010968, 7.97700, 15.45511, 23.85604, 10.34038, and 15.97875, respectively. Their reported HiGHS primal/dual objectives agree; every winning corner is independently checked with unbounded **exact rational integer** arithmetic. As with TOE71, MILP optimality remains **numerical** because the finite-precision branch-and-bound tree lacks a formal exact-rational certificate. Six tested directions **do not cover** the full continuous direction sphere, so no theorem about the global smallest eigenvalue is claimed. The exact eigen-axis is a theorem **for the specified 17-edge witness**, not an assertion that it is globally worst over all link patterns.

**Producer:** \`analysis/w33_20261014_toe72_hessian_multiray.py\`.

## 2. Rigorous stronger operator inequalities on the unbounded native two-loop gauge sector

TOE71 bounded the omitted \(Q\)-sector for the native 11-site, 12-link, five-fermion, three-supported-octagon magnetic Hamiltonian at electric cutoff \(L=3\), with 22,638 included and 14,784 first-shell states. This pass improves both rigorous constants without changing the physical Hamiltonian.

**Exact complement Gershgorin.** Instead of subtracting the absolute maximum 12 hopping and six magnetic terms from the *smallest diagonal regardless of its row*, reconstruct each actual omitted-state transition (respecting the exact Gauss-law fermion occupation and the \(P/Q\) boundary). Using common integer denominator **2000**, the smallest \(Q\) diagonal-minus-actual-allowed-row-sum is **28,330/2,000=14.165**, at electric flux \((-4,2)\). Exhaustive occupation census runs over all 462 allowed five-particle configurations and omitted \(|m_1|,|m_2|\le9\). A separate exact tail bound proves all states with either \(|m_i|\ge10\) have diagonal-minus-row-sum at least **44,200/2,000=22.1**, so the finite enumeration certifies the entire infinite complement. Thus

\[
QHQ\succeq 14.165\,I
\]

is a **rigorous** operator bound for this finite-patch, infinite-electric-rotor sector.

**Exact integer interface Gram.** Multiply every nonzero coefficient of \(K=PHQ\) by **80**: signed fermion hopping becomes integer \(\pm56\), magnetic shifts integer \(-25\). There are 28,476 nonzero entries. The Gram matrix \(K_{\rm int}K_{\rm int}^\top\) has **exact** maximum absolute row sum **12,822**, hence

\[
\|K\|_2^2
=\frac{\|K_{\rm int}\|_2^2}{80^2}
\le\frac{12822}{6400}
=\boxed{2.0034375},
\]

improving TOE71's 3.51125.

With the TOE70/71 *numerical* \(P\)-sector gap \(1.064312487261\), the Schur/inertia min-max formula yields the **conditional** full-rotor gap lower estimate

\[
\Delta_\infty\ge
\Delta_P-\frac{2.0034375}{14.165}
\approx\boxed{0.92287673}.
\]

The new 14.165 and 2.0034375 inequalities are exact/rigorous. The final decimal full-rotor gap is **NOT YET a theorem** until the two finite \(22{,}638\times22{,}638\) ordered low-energy eigenvalues are enclosed by a rigorous interval/inertia method. A small residual from ordinary sparse eigensolvers does not prove eigenvalue ordering. This front has made the remaining proof dependency much narrower and quantitatively sharper.

**Producer:** \`analysis/w33_20261014_toe72_gauge_gram_bound.py\`.

## 3. The six second-order quantum-cover neighbors ESCAPE the 51,840-state orbit

TOE71 found six two-vertex local pairing flips mapping its 20-octagon cover to other exact 20-loop vacua. One might hope to diagonalize quantum tunneling **within its known 51,840-cover \(PGSp(4,3)\) orbit**. Exact permutation enumeration disproves that simplification.

Reconstruct all 1,620 native length-eight cycles and the site-local three pairing choices, verify the full 12,640 two-vertex-alternative loop-count census \(12628\) yielding 18 loops, \(6\) yielding 19 loops, \(6\) retaining 20 loops. Convert each of the six retained configurations into its **actual unordered set of 20 octagons**. Transport that ordered six-neighbor tuple through the native point-line-flag action of six symplectic generators. The primary \(PSp(4,3)\) orbit has 25,920 states; adding the outer similitude doubles it to 51,840. **None of the six neighbor states belongs to this 51,840 orbit**, and the same remains true after transporting them through every group element.

Now enumerate the *full* \(PGSp(4,3)\) orbit of **each** of the six neighboring covers separately. Every orbit has 51,840 elements, and none of the six seed neighbors appears in the orbit of any other seed neighbor. Thus the program explicitly exhibits **SEVEN DISJOINT full-group exact-cover ground-state orbits**, each of size 51,840:

\[
N_{\text{classical exact-cover vacua}}\ge
7\cdot 51{,}840=\boxed{362{,}880}.
\]

These are distinct combinatorial configurations but **only seven proved symmetry-inequivalent orbits**, not 362,880 symmetry-inequivalent vacua. The six seed moves are second-order \(t^2\) tunneling links **between** the original orbit and six other orbits, with amplitude \(-2t^2/J\) for each pair of distinct local flips through 19-loop virtual intermediate states. Inside the original orbit there are **no** such second-order links. No assertion is made that all 20-loop cover orbits have been found, nor that the 7-orbit induced network is closed against more local moves or all orders.

This is a concrete, structurally important correction to the proposed effective quantum geometry calculation. It does **not** derive gravity, Lorentz invariance, or a physical spacetime vacuum.

**Producer:** \`analysis/w33_20261014_toe72_cover_orbit_escape.py\`.

## 4. W33-only 4D closed spin topology and a graph-inherited chirality obstruction

TOE71's closed four-manifold \(\Sigma_{81}\times T^2\) preserved all 81 graph characters but inserted an **external torus**. We can remove that particular extra factor: take the product of **two copies** of the closed genus-81 boundary of a three-dimensional handlebody thickening of the native W33 Levi graph. The result \(M=\Sigma_{81}\times\Sigma_{81}\) is a genuine closed oriented **spin** four-manifold with no unrelated torus input, integral torsion-free Betti numbers

\[
(b_0,b_1,b_2,b_3,b_4)
=(1,324,26246,324,1),
\]

Euler characteristic \(25{,}600\), signature zero and \(13{,}123\) hyperbolic intersection planes. It still depends on a **noncanonical graph thickening/embedding** and a choice to take two copies, so it is not a unique space selected by \(PGSp(4,3)\).

**New topological obstruction:** Graph-cohomology characters map into \(H^1(\Sigma_{81})\) as a rank-81 **Lagrangian isotropic** subspace (they extend over the handlebody). All pairwise surface cup intersections of graph-inherited 1-classes therefore vanish. Hence the rank-\(81^2=6561\) subspace of mixed degree-two classes constructed using *only* inherited graph 1-classes from both factors has identically zero 4D intersection form. Any integer line bundle whose first Chern class is made entirely from these inherited mixed classes obeys

\[
c_1(L)^2=0,\qquad
\mathrm{ind}\,D_L^+=\frac12\int_M c_1(L)^2=0
\]

(the untwisted \(\hat A\) term vanishes by signature zero). This is true even for arbitrary **sums of mixed graph classes**, not only for a single decomposable form. A small exact integral cup-product matrix \(-J\otimes J\) verifies the algebra and demonstrates that adding meridian-dual classes permits \(c_1^2=2\) and index \(1\).

**Conclusion:** Closed 4D topology and the flat three-deck characters can come from W33 alone in this existence construction, but graph-inherited flux classes **cannot by themselves furnish a nonzero twisted chiral index**. A dual boundary class or separately selected curvature is essential. No local W33 four-dimensional overlap-Dirac operator or anomaly-free chiral Standard Model spectrum was constructed.

**Producer:** \`analysis/w33_20261014_toe72_w33_squared_index.py\`.

## 5. Exact interacting native octagon exposes the limits of 80-site Hartree–Fock gaps

Select native simple octagon **111**, using edge IDs \((1,56,59,37,38,131,128,3)\), which carries winding \((1,0,0)\). The native \(\pi\) link gives exact edge-sign product \(-1\). Use all eight sites and four spinless fermions at half filling; the canonical Fock dimension is \(\binom84=70\). Diagonalize the **exact fixed-N many-body** Hamiltonian

\[
H=-\sum_{\{i,j\}\in\mathrm{octagon}}
s_{ij}(c_i^\dagger c_j+c_j^\dagger c_i)
+V\sum_{\{i,j\}\in\mathrm{octagon}}
(n_i-\tfrac12)(n_j-\tfrac12)
\]

for V=.2,.5,1,2,4,8, retaining exact fermionic signs. Independently solve the **unrestricted site-dependent exchange-inclusive** 8×8 Hartree–Fock fixed point for the *same* graph, signs, N and V.

| repulsion V | exact canonical first excitation E1−E0 | HF occupied–unoccupied one-body gap |
|---:|---:|---:|
| .2 | 1.510838 | 1.630734 |
| .5 | 1.462854 | 1.780734 |
| 1 | 1.345562 | 2.030734 |
| 2 | 1.045349 | 2.963109 |
| 4 | 0.517527 | 7.014215 |
| 8 | 0.122589 | 15.361533 |

**These are different gap definitions** (a true same-N many-body excitation vs an approximate HF particle-hole eigenvalue gap), so they must not be equated mathematically. They are appropriate diagnostics of the danger of inferring exact low-energy behavior from an HF one-body gap. The HF energy is always a variational upper bound on the exact many-body ground energy. The exact finite ground state has \(\langle M_{\rm stagger}\rangle\approx0\) at every tested coupling, while \(\langle M_{\rm stagger}^2\rangle\) increases from about 4.225 to 14.334 across this scan. At strong V, HF selects a broken-symmetry branch and its single-particle gap grows while the exact finite first excitation gap **decreases** sharply.

This is a genuine **controlled exact-diagonalization countercheck** of the previous optimistic mean-field interpretation. The finite octagon does not prove the absence or presence of spontaneous order in the full 80-site graph or its thermodynamic completion.

**Producer:** \`analysis/w33_20261014_toe72_exact_interacting_octagon.py\`.

## Reproducibility and status separation

Five source-regenerating producers, five pytest gates, frozen JSON certificates available as CI artifacts, and an explicit GitHub Actions workflow are provided. The two exact new mathematical structures—the seven full cover orbits, and the inherited-flux index obstruction—are independent of any floating point solver. The gauge Gram/Gershgorin improvements use exact integer arithmetic. Fixed-direction MILP reports and HF/ED eigenvalues remain labeled numerical. All broader TOE, spacetime, dynamical gauge and Standard Model claims remain open.

## Five best independent successors

1. **Exact global disorder verification:** export a rational cutting-plane/branching certificate for all 160 amplitudes and then solve the *full* direction-dependent 3×3 Hessian minimax, not a finite six-ray sampling.
2. **Finish rigorous interacting gap:** compute verified finite two-loop *ordered* eigenvalue enclosures, feed them into the new exact 14.165/2.0034375 constants, and check charged sectors with an independent code.
3. **Multi-orbit quantum geometry:** build the sparse second-order tunneling graph across the seven 51,840-state orbits (and search for further cover orbits); classify connected components and ground-state representations rather than restricting to one orbit.
4. **Geometry-to-lattice index:** construct a concrete local spin discretization of \(\Sigma_{81}\times\Sigma_{81}\), add dual meridian flux when justified, calculate admissible overlap indices and anomalies, and keep inherited-class index-zero controls.
5. **Exact many-body mass dynamics:** grow the exact interacting benchmark from 8 to 11 or more native sites, compare spectral gaps and symmetry-symmetric correlators with unrestricted HF and dynamical Gauss-constrained matter, and seek a parameter-independent falsifiable prediction.

**The physical Theory of Everything remains unproved.**
