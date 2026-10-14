# TOE70 — Five-front exact and numerical follow-through

**Date:** October 14, 2026. **Baseline:** TOE69, with subsequent parallel commits preserved.

**Research scope:** native W33 finite combinatorics, exact rational hopping disorder, native finite gauge–matter numerics, an explicit 4D topological obstruction, and restricted charge-density-wave Hartree theory. **No physical Theory of Everything has been derived.**

## 1. Native hopping disorder — three-bit and full 17-bit subcube certificates

For the previously constructed TOE66 17-high-link hopping mask at epsilon=245/1000 and fixed phase Rayleigh direction q=(0,−1,1), reconstruct the 238 actual native winding octagons from the full 1620 simple length-eight cycles. All calculations use unbounded exact integer arithmetic with common denominator 1000^8.

The base Rayleigh numerator is **−278181245315125293750000**. The smallest increases from all possible one-edge, two-edge and three-edge flips are:

| flips | alternatives tested | smallest increase in integer numerator | responsible edges |
|---:|---:|---:|---|
| 1 | 160 | 52315612734624060937500 | preceding TOE69 result |
| 2 | 12720 | 337991711991203123437500 | 37, 56 |
| 3 | **669920** | **303334787318187810937500** | **37, 56, 57** |

The seed is therefore strictly optimal among all Hamming-distance-at-most-three changes.

A separate exhaustive Gray-code exact search examines all **131072** assignments to those 17 native edges, fixing the other 143 edges low. Exactly **one** assignment has a negative Rayleigh quotient, namely the original all-17-high mask. It is the **unique restricted-subcube global minimizer**. This does not certify optimality over all 2^160 masks, optimize the entire Hessian spectrum or improve the universal lower robustness bound. The precise full minimax threshold remains OPEN.

Producer: analysis/w33_20261014_toe70_disorder_certified_subcube.py.

## 2. Native coupled overlapping-octagon gauge theory at flux cutoff L=3

Regenerate the entire native 11-vertex, 12-link, five-fermion Hilbert space with two independent electric loop coordinates and three supported magnetic Wilson octagons. Reuse the exact Gauss reconstruction and signed hopping of TOE69, which itself builds on the earlier Pass11974 two-loop patch.

| L | states | ground energy | first gap | covariance of electric fluxes | flux boundary probability |
|---:|---:|---:|---:|---:|---:|
| 1 | 4158 | −3.160471619470 | 1.071882736351 | −0.036148250445 | 0.25807084696 |
| 2 | 11550 | −3.189618205026 | 1.064323515805 | −0.047903659245 | 0.00572909089 |
| 3 | **22638** | **−3.189847448116** | **1.064312487261** | **−0.048121932413** | **0.00001994701647** |

The sparse eigensolver residual at L=3 is approximately 3.4×10^-14. This strengthens evidence of *finite-patch* flux anticorrelation; small truncation shifts and probabilities do not prove an untruncated or thermodynamic gap. Dedicated numerical controls distinguish the new covariance observable from Pass11974's earlier energy scans.

Producer: analysis/w33_20261014_toe70_interacting_mass.py.

## 3. Full-group symmetry orbit of the exact 20-octagon cover

TOE69's exact partition of all 160 native edges into 20 octagonal loops saturates girth and minimizes the automorphism-invariant classical loop-count energy at −20J.

Using actual native point/line/flag permutations from six symplectic transvections, the orbit of this cover under PSp(4,3) contains **25920** distinct configurations, precisely the known inner group order. Thus its stabilizer is trivial. The outer symplectic similitude diag(1,2,1,2) sends this cover outside the inner orbit. Consequently its orbit under full PGSp(4,3), order **51840**, has **51840 distinct symmetry-related minimum-energy configurations**. These are **not** 51840 inequivalent physical vacua after quotienting by symmetry: they constitute one group orbit, with potentially other orbits not classified.

Attempted to pair this first octagon decomposition with another edge-disjoint 20-octagon decomposition providing the complementary local through-pairings needed for a 40-face octagonal genus-21 embedding. Of all 1620 octagons, only **73** respect the required distinct vertex pairings, and **edge 45 occurs in none of them**. This is an exact construction-specific obstruction. Group covariance transports it across the entire 51840-element orbit, but it does not exclude other cover orbits, other face lengths or unrelated surface embeddings.

Producer: analysis/w33_20261014_toe70_symmetry_topology.py.

## 4. Native 4D topology / three-holonomy compatibility gate

Let X be the connected W33 Levi graph with **one disc 2-cell attached along each of the 20 edge-partitioning octagons**. The native incidence matrix has rank 79; the 20 signed octagon boundary columns are edge-disjoint, independent and primitive over the integers, so X has torsion-free Betti numbers **(1,61,0)**. Künneth then gives

\[
b_*(X\times T^2)=(1,63,123,61,0).
\]

The vanishing fourth homology prohibits this direct product from being a closed connected four-manifold. Hence it does not yet support a conventional closed four-dimensional overlap-Dirac index.

More importantly, three of the face boundaries carry winding vectors **(0,0,−1), (0,1,0), (1,0,0)** against TOE67's selected three tree-chord voltages. They generate an integral basis of Z^3. Attaching those faces annihilates the chosen three *flat* deck-holonomy directions: the π,π,π configuration of the original graph cannot remain *flat* over the 20-face CW complex. It could be interpreted as nonzero magnetic curvature instead, but then TOE67's static flat-holonomy theorem is not a proof for the new two-complex.

No native closed four-dimensional spin cellulation, admissible overlap gauge links, nonzero native index or anomaly-free W33 Standard Model was built. The correct outcome on this front is a **new exact incompatibility** for this specific natural geometrization route, not a solved chirality problem.

Producer: analysis/w33_20261014_toe70_symmetry_topology.py.

## 5. Interaction-generated mass in a restricted native Hartree channel

Investigated **actual nearest-neighbor repulsion** over the 160 native Levi incidences for spinless fermions,

\[
H_{\rm int}=V\sum_{\langle a,b\rangle}(n_a-\tfrac12)(n_b-\tfrac12),\quad V>0,
\]

with a *restricted*, uniform point-vs-line sublattice density-wave Hartree ansatz. Four-regularity gives a common staggered mass m=4Vs. At fixed three-π flux its one-parameter functional is

\[
{\cal E}_H(m)=-\sum_{j=1}^{40}\sqrt{\sigma_j(B_\pi)^2+m^2}
+\frac{10m^2}{V},
\quad
\frac{20}{V}=\sum_{j=1}^{40}\frac{1}{\sqrt{\sigma_j^2+m^2}}.
\]

Exactly **12** zero singular values make the stationary equation diverge like 12/m at small m. It has exactly one positive solution for every V>0 within this restricted channel, with **m/V→0.6** at weak coupling. Selected numerical roots:

| V | restricted Hartree mass m | free quasiparticle gap 2m |
|---:|---:|---:|
| 0.01 | 0.006041948647 | 0.01208389729 |
| 0.05 | 0.031078613423 | 0.06215722685 |
| 0.20 | 0.139236995380 | 0.27847399076 |
| 0.80 | 0.922219721552 | 1.84443944310 |
| 1.60 | 2.652494473227 | 5.30498894645 |

The TOE67 uniform-link free determinant theorem retains the strict three-π minimum for each common mass, so joint minimization of this *restricted* functional maintains it. However, full native eigenspace occupancies are not uniform at fixed three-deck flux. At V=.2 their point/line density standard deviations are about **0.03720/0.03655**. Thus the restricted solution is **not** an unrestricted sitewise Hartree–Fock stationary state. Missing are Fock/exchange, gauge fluctuations, exact many-body gap, and physically realistic mass generation. This remains a testable approximation, not a physical TOE theorem.

Producer: analysis/w33_20261014_toe70_interacting_mass.py.

## Reproducibility and novelty gates

All scripts use the existing project W33 symplectic core and the native TOE69 two-loop solver, not a fabricated graph. The exact Hamming-radius-three census, 17-bit Gray-code census, 25920-element orbit, outer-coset test, 20-face integral chain complex, and native mass-channel roots were also independently calculated before writing this packet. The gauge scan was performed on the same actual 22638-dimensional native patch with a measured residual <4×10^-14. A dedicated GitHub Actions pytest workflow performs release verification separately from source publication.

**All exact claims remain mathematical finite-model statements; all interacting numeric findings remain finite-cutoff results. The physical Theory of Everything is not solved.**

## Five strongest independent successors

1. **Global disorder:** optimize all 160 native edge products and all Hessian phase directions with certified integer/interval branch-and-bound, beyond the unique 17-bit subcube result.
2. **Interacting rigor:** rigorously enclose the L=3 two-loop eigenvalues, strengthen Q-block truncation bounds, compute charge screening and test additional overlapping loop arrangements.
3. **Quantum pairing:** classify *other* 20-octagon-cover orbits and construct a symmetry-covariant quantum pairing Hamiltonian with local tunneling instead of a static −J loop-count energy.
4. **Genuine 4D W33 chirality:** find a closed oriented spin four-complex that retains the desired flux degrees of freedom, respects the new face-attachment flatness obstruction, and computes a native admissible overlap index with anomaly cancellation.
5. **Beyond restricted Hartree:** implement full site-dependent Hartree–Fock plus gauge-matter coupling; prove or refute a stable interaction-generated gap and derive a parameter-independent falsifiable W33-specific observable.
