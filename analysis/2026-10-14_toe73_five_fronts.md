# TOE73 — Five independent validation fronts: exact crossing, static gauge dipole, quantum cover matchings, explicit 4D CW census, eleven-site interacting ED

**Date:** 2026-10-14. **Parent:** TOE72, with any concurrent GitHub head preserved. **Status:** finite W33 theorems + source-regenerated numerical controls. **Not:** a physical Theory of Everything, global disorder proof, rigorous infinite-gauge spectral gap, or native overlap-Dirac Standard Model.

## Prior-work intake and external checks

Read TOE71's full-160-link fixed-direction mixed-integer method and complement block proof, TOE72's full 3x3 native winding Hessian, exact seven ground-cover orbits, Gram/Gershgorin bounds, W33-squared topology and 70-state octagon interaction benchmark. Examined native 11-site / 12-link / two-Wilson-cycle Gauss solver of TOE69–72 and verified the precise role of its background charges and selected spanning-tree chords. We distinguish its *dynamic gauge fields* from the *static Z2 flux* in the new exact interacting benchmark.

External cross-checks: Lüscher, *Abelian chiral gauge theories on the lattice with exact gauge invariance*, hep-lat/9811032 (anomaly-free representation and a consistent fermion measure are additional nontrivial requirements); Lüscher, *Topology and the axial anomaly in abelian lattice gauge theories*, hep-lat/9808021; *Efficient truncations of lattice gauge theory for quantum simulation*, Phys. Rev. D, DOI 10.1103/ylqb-phv5. These references are prior mathematical / simulation work; they do not validate a W33 physical theory.

## Front 1 — An exact and unique instability crossing of the native 17-high-edge witness

TOE72's exact three-by-three Hessian coefficients show that q=(0,-1,1) is an **exact eigenvector** of the 17-high native edge amplitude pattern for *every* epsilon. The unnormalized Rayleigh eigenvalue has exact numerator

\[
P(\epsilon)=72(1+\epsilon)^2(1-\epsilon)^6
+46(1+\epsilon)^3(1-\epsilon)^5
+34(1+\epsilon)^4(1-\epsilon)^4
-12(1+\epsilon)^8.
\]

Write u=1+epsilon, v=1-epsilon, r=u/v. The strict-positive factor u²v⁶ separates the polynomial

\[
P=u^2v^6[72+46r+34r^2-12r^6].
\]

The bracket has coefficient signs (descending powers) minus, plus, plus, plus, exactly **one** sign variation. Descartes' rule of signs, the positive value Q(1)=140, and Q(r)→−∞ prove there is **exactly one positive real root**, in fact r*>1. Since r(epsilon) rises strictly for 0≤epsilon<1, the destabilizing eigenvalue changes sign **exactly once** along the entire physical interval, not merely between sample points. Exact Python integers verify

\[
\boxed{24461518/10^8<\epsilon_*<24461519/10^8}.
\]

The numerical root is roughly 0.2446151803711919. This is a rigorous *fixed-17-edge and fixed-antisymmetric-Hessian-eigenvector* theorem. TOE71's finite-precision all-160-link MILP reported global minima near this threshold, but **no independently checkable exact branch-and-bound certificate** yet validates that global conclusion, and other Hessian directions might fail earlier. The universal small-disorder guarantee and actual threshold are not asserted equal to this witness root.

**Producer:** analysis/w33_20261014_toe73_exact_fronts.py.

## Front 2 — Actual Gauss-source response rather than mistaking gauge covariance for screening

Use the **same native 11-site, 12-edge W33 patch**, with three supported Wilson octagons, two independent electric coordinates and all C(11,5)=462 mobile five-fermion states. Compare two *different Gauss-background sectors*: (a) native alternating background (five point charges), and (b) transfer one unit of external background across an **actual native point–line edge** while keeping total background charge exactly five. Set the on-site staggered mass to zero, so no external mass term is changed between backgrounds.

For each sector reproduce a sparse gauge-dressed, electric-and-magnetic Hamiltonian with parameters g=0.8, hopping kappa=0.7 and magnetic beta=0.4 at L=1 (4158 states) and L=2 (11550 states). Record ground-energy shift of the imposed source, the flux covariance and probability on the outer electric shell. The producer also enumerates **every allowed local transition** in the complementary infinite-flux Q sector and derives an exact Gershgorin lower bound in units 1/2000, checking all 462 occupations and all omitted -9≤m_i≤9; chord electric field ensures the analytic tail |m_i|≥10 has lower bound 47200/2000=23.6 independently of the finite scan.

Results and guards reside in the frozen CI certificate. They are finite-static-dipole response energies, **not** continuum screening lengths or a rigorous infinite-spectrum level ordering. The earlier TOE72 uncharged rotor gap bound (14.165 and 2.0034375) does not automatically apply when the imposed Gauss background changes. The source respects that distinction.

**Producer:** analysis/w33_20261014_toe73_gauge_static_dipole.py.

## Front 3 — An exact matching theorem and soluble compression of the seven quantum-cover orbits

TOE72 proved **seven pairwise disjoint \(PGSp(4,3)\) symmetry orbits** of exactly 51,840 twenty-octagon ground configurations each, and six distinct double-local-pairing-flip neighbors of the original cover, one in each different orbit. Every orbit stabilizer is trivial.

A basic but consequential group-theoretic theorem now upgrades this to a **complete, explicit inter-orbit edge count**: transporting each of the six chosen seed transitions by full group action gives a well-defined map between two free transitive \(PGSp(4,3)\)-sets. Such a map is automatically a **bijection**. Hence the six relations each form a perfect matching containing 51,840 edges, producing

\[
\boxed{6\times 51{,}840=311{,}040}
\]

distinct center-to-neighbor *second-order* tunneling edges among the seven orbits.

If we **deliberately retain only these six perfect matchings**, the compressed transition graph decomposes into 51,840 disjoint seven-node stars \(K_{1,6}\), with adjacency eigenvalues \(-\sqrt6,0,+\sqrt6\), each with multiplicities 51,840, 259,200, 51,840. Multiplying by the second-order transition amplitude −2t²/J gives exact outer energy shifts ±2sqrt(6)t²/J and five zero shifts per star.

**Important:** this is the exact spectrum of an explicitly **restricted/compressed star model, not the full induced seven-orbit graph**. It discards unknown target-to-target links, links into further orbits, and all higher-order transitions. It therefore cannot establish symmetry breaking, a unique full quantum vacuum, or emergent spacetime. It exposes precisely the next adjacency data needed.

**Producer:** analysis/w33_20261014_toe73_exact_fronts.py.

## Front 4 — Finite four-dimensional CW product and a quantitative obstruction to "native" chirality

Start with TWO copies of a chosen genus-81 boundary surface of a regular W33 Levi graph handlebody, without importing an unrelated torus. A closed genus-g surface has a minimal CW decomposition with **one 0-cell, 2g oriented 1-cells and one 2-cell** attached along the product of g fundamental commutators. Its cellular differential is zero because each commutator abelianizes to zero, **not** because the attaching maps or cup products are trivial.

Taking the product of the two chosen genus-81 CW decompositions produces a concrete closed smoothable oriented spin four-dimensional CW model with **integer cell counts**

\[
\boxed{(c_0,c_1,c_2,c_3,c_4)=(1,324,26246,324,1)}.
\]

All minimal cellular boundary matrices are zero. The resulting free homology equals these Betti numbers; Euler characteristic is 25,600. There are \(2^{324}\) spin-structure choices on the product, showing that the graph input does not specify a unique spin structure.

The inherited graph 1-classes on each surface form an isotropic 81-dimensional Lagrangian; the 6561-dimensional cross-product subspace of \(H^2(M)\) generated exclusively from these classes has identically zero intersection form. Thus every U(1) line bundle confined to this graph-inherited *mixed* flux subspace has c1²=0 and vanishing twisted spin Dirac index. Dual meridian classes can instead give c1²=2 and index +1, but choosing them is additional geometric data.

This is now an **explicit finite CW chain census**, upgrading TOE72's Betti computation; it is **not** an admissible local discretization of the Dirac operator. No metric, facewise spin parallel transport, Ginsparg–Wilson spectrum, chiral lattice measure, or anomaly-free Standard Model multiplet emerges from the cell counts.

**Producer:** analysis/w33_20261014_toe73_exact_fronts.py.

## Front 5 — Grow exact interacting W33 fermions from 70 to 462 Fock states

TOE72's eight-site native W33 octagon ED used \(\binom84=70\) spinless, fixed-N many-body states. The new experiment uses the native **11-site / 12-link** overlap of two different native eight-cycles with five fermions and

\[
\boxed{\dim\mathcal H_{N=5}=\binom{11}5=462}.
\]

Retain every signed hopping operator on all 12 native edges, exact Jordan–Wigner Fock signs and local repulsive nearest-neighbor density-density terms \(V(n_a-\frac12)(n_b-\frac12)\). The native patch has **two independent spanning-tree chord phases**; independently diagonalize all **four** Z2 holonomy corners (0,0), (0,pi), (pi,0), (pi,pi) at four couplings V=0,0.2,1,4. For every solved sector, store three lowest eigenvalues, the first **same-N many-body gap**, sublattice-density first and second moments, average connected density on native edges, and residual norm. The source explicitly determines which of the four corners minimizes energy at each V, without hardcoding a conjectured outcome.

These are genuine interacting finite-sector ED checks and should be treated as **separate** from the dynamical Gauss-constrained Hamiltonian in Front 2. The two local patch chords also differ from TOE67's three global spanning-tree chords, so a local preferred phase is **not** a proof or refutation of the full W33 three-pi all-temperature *free* theorem.

**Producer:** analysis/w33_20261014_toe73_eleven_site_ed.py.

## Verification, scope and ownership

The repository contains three independently executable producers, tests for all five fronts and an on-push GitHub Actions workflow regenerating the corresponding JSON artifacts. The exact polynomial crossing and group-equivariant matching are rigorous finite combinatorial/algebraic claims. The static Gauss-source and finite interacting-fermion eigenvalues remain numerical, with residuals and finite cutoff identified. Any workflow failure must be addressed before declaring full CI success.

**Physical TOE status: OPEN.** Missing: exact rational global disordered-Hessian minimax proof; certified finite ordered two-loop gauge eigenvalue intervals; the full quantum pairing-orbit graph and its dynamics; admissible local chiral overlap lattice and measure on W33-derived geometry; large-system exact interacting mass physics and experimentally falsifiable parameter-free predictions.

## Five independent successor fronts

1. Prove or falsify the global 160-edge *full-Hessian* threshold with an independently checkable exact integer/interval MILP or sum-of-squares certificate, rather than treating solver tolerances as mathematics.
2. Certify the two lowest **ordered** finite Gauss-constrained eigenvalues with sparse inertia/interval LDL and extend exact unbounded-rotor bounds to modified static charge backgrounds.
3. Enumerate target-to-target and outward **cover-orbit transitions**, beyond the deliberate six-perfect-matching star compression, and solve connected components/representations of the full second-order graph.
4. Equip the explicit W33-squared CW construction with a bona fide **local geometric Dirac stencil**, spin connection and admissible gauge plaquettes; compare chirality with dual-meridian and zero-index graph-only controls.
5. Extend the 11-site exact fermion benchmark to finite-temperature and dynamical gauge backgrounds, compare interaction-driven flux sectors and density correlations with a matched non-W33 graph, and demand a falsifiable physical prediction.

**The Theory of Everything itself is not solved.**

## Verified GitHub Actions outcomes (post-publication)

Workflow [TOE73 #38629784735](https://github.com/wilcompute/W33-Theory/actions/runs/38629784735) completed successfully: **5/5 source-regenerating tests passed in 13.01 seconds**. All three certificate producers completed and a ZIP artifact containing their JSON output was uploaded. These are reproducibility results, not peer review or proof of full physical claims.

**Native 11-site interacting spinless five-fermion ED, four local Z2 flux corners** (ground-state energy spread is max(E0)-min(E0), hopping unit 1):

| V | lowest-energy chord corner | spread |
|---:|:---:|---:|
| 0.0 | (pi,pi) | 0.4156003044900505 |
| 0.2 | (0,pi) | 0.39937455024460267 |
| 1.0 | (pi,pi) | 0.3071216455271113 |
| 4.0 | (0,pi) | 0.014135563871016998 |

The preferred corner **changes with repulsion** in this finite interacting patch; the four-corner energy spread becomes about 29.4 times smaller by V=4 than V=0. This is not a statement about TOE67's three selected chords or about continuous flat U(1)^3 at all temperatures.

**Gauss-background unit-charge-transfer response:** at g=.8, kappa=.7, magnetic beta=.4 and zero staggered mass, the modified static charge background minus native background ground energy is **+0.18082624543649395** at electric cutoff L=1 and **+0.17376606610476086** at L=2. This is an explicitly specified *static-source* finite-patch response, not a confinement law.

**Quantum cover compression:** exact six-equivariant-matchings count **311,040** (and 51,840 deliberately truncated seven-node stars) was regenerated by CI. See the artifact for the complete source-computed JSON, including exact Gauss-complement row bounds and finite eigenvector residuals.
