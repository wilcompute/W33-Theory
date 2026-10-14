# TOE66 — Five independent follow-through investigations (2026-10-14)

**Parent:** TOE65 `d183f38e20a88ed6e55ae67353cb4054fad9fa4d` plus the parallel formula-index publication.  
**Status discipline:** finite combinatorial theorem, exact integer witness, numerical experiment, continuum topology, and genuinely open physics are separated throughout. Neither W33 nor the Standard Model is derived from these constructions.

## 1. Exact native-edge disorder counterexample strengthened

Reconstructed the W33 Levi graph *independently* on a server using the same canonical sorted projective symplectic points, 40 isotropic lines, 160 ordered incidence flags, and selected spanning-tree chords (5,30,65) from the 81 chords. Exhaustive simple-eight-cycle DFS returned 1,620 undirected octagons, with 238 nonzero integer winding and Fourier winding numbers consistent with TOE59 and TOE65. The old 18-high-edge TOE65 integer polynomial reproduced exactly.

A greedy corner search suggested removing high edge 57 from TOE65's 18-high-edge binary assignment. The new 17 high indices are:

`[30,31,49,51,59,62,63,82,83,93,95,118,119,138,139,142,143]`

For the exact integer phase direction `q=(0,-1,1)`, the Hessian Rayleigh polynomial is

```
P(e) = 72(1+e)^2(1-e)^6 + 46(1+e)^3(1-e)^5
     + 34(1+e)^4(1-e)^4 - 12(1+e)^8.
```

The first zero on this *fixed witness* is numerically `0.24461518037119193`. **Exact integer arithmetic** verifies

```
10^48 * P(244616/1000000)
  = -592200479596647810296792372727074788466491392 < 0.
```

(The integer expression is actually `(10^6)^8P`; the negative sign, not the printed decimal approximation to the root, is the certificate.) The immediately preceding grid fraction `244615/1000000` has positive numerator.

Thus the universal *leading high-temperature* positive-edge-amplitude robustness threshold satisfies

```
(11^(1/8)-1)/(11^(1/8)+1) <= e_universal < 244616/1000000.
```

This is a worst-case sufficient lower bound and an explicit native product upper counterexample; NOT the minimax optimum. The exact 17-bit corner satisfies all native edge-product correlations, unlike earlier independent Fourier-coefficient relaxations. The theorem is about local Hessian instability at pi; an actual global competing minimum follows by compactness but its location is not determined.

## 2. Exact all-beta stationarity; numerical temperature-dependent curvature reversal

For any real link weights, the native 80x80 hopping Hamiltonian obeys `H(-theta) = conjugate(H(theta))`. Hence its spectral free energy is even under `theta -> -theta`. At theta=(pi,pi,pi), inversion fixes the point modulo 2pi. Therefore three-pi is stationary whenever the free energy is differentiable, at *all positive beta* and at zero temperature if differentiable. This exact symmetry statement does **not** prove minimality.

The actual 17-edge native pattern with weights 0.7 and 1.3 at 30% disorder has a negative leading beta^7 phase-Hessian direction, so the exact high-temperature series proves three-pi ceases to be a local minimum for all *sufficiently small* positive beta (no explicit beta interval certified).

The full native 80x80 eigenspectrum was diagonalized server-side for beta `0.4,0.8,1,1.5,2,2.5,4,8,infinity`. Using central difference `h=.05` along `(0,-1,1)/sqrt2`, the directional curvature is negative at beta=.8 and positive at beta=2.5. The zero of this *finite-difference diagnostic* is approximately beta=1.9781; at halved step its curvature is not exactly zero, so this is **not** an exact critical beta. This is an informative finite-system temperature-dependent local-stability reversal, not a thermodynamic phase transition, spontaneous CP order, or all-beta theorem.

Compare the planar/periodicity hypotheses in E. H. Lieb, *Flux Phase of the Half-Filled Band*, Phys. Rev. Lett. 73 (1994), 2158, DOI 10.1103/PhysRevLett.73.2158. Those hypotheses are not automatically satisfied in the W33 Levi cover.

## 3. Constructive repair of the genus-21 surface misconception

TOE65 refuted BT1643: the 40-line triangular clique two-skeleton is not a surface (each vertex link consists of four disjoint 3-cycles). This pass takes an **alternative noncanonical** but legitimate geometric construction from the actual W33 point-line Levi graph.

Give each of its 80 degree-four vertices the cyclic order of incident edges by the canonical edge number. The ribbon rotation permutation on 320 directed half-edges has four boundary orbits of lengths `[12,14,106,188]`. The orientable ribbon neighborhood has Euler characteristic `80-160=-80`, four boundary circles and genus

```
2-2h-b=-80, b=4 => h=39.
```

Double this connected orientable ribbon surface along its four boundary circles. The result **is** a genuine closed orientable surface `Sigma_81`, with

```
g=2h+b-1=81, chi=2-2g=-160.
```

This now satisfies the local manifold requirement and has a precisely defined constructive cellulation algorithm via the rotation system. It is **not** the original clique 2-skeleton and the edge rotation is an additional choice; moreover, its 81 loops derive directly from the graph cycle rank `160-80+1`. No Lorentz signature, Einstein algebra or unique spacetime selection follows.

For mathematical background, any connected graph's orientable ribbon thickening can be doubled, or one can take the boundary of a 3D regular neighborhood/handlebody.

## 4. An actual nonzero *continuum* chiral topological index on a derived M4

Construct `M4=Sigma_81 x T2`, with the above genuine closed W33-derived surface and an **externally added** torus. Ordinary integral Kunneth gives

```
b0..b4 = (1,164,326,164,1).
```

The cup-product intersection form on `H^2(M4;Z)` is even unimodular, isometric to 163 hyperbolic planes, and has signature zero. An exact 326x326 integral matrix assembled from the symplectic pairings of `H^1(Sigma_81)` and `H^1(T2)` satisfies `Q^T=Q` and `Q^2=I`, with 163 positive/negative eigenvalues.

Choose a line bundle `L` with `c1(L)=u+v`, where `u` and `v` are the integral generators of `H^2(Sigma_81)` and `H^2(T2)`. Then `int c1(L)^2=2`. Orientable surfaces (and their products) admit spin structures, and `signature(M4)=0`. The Atiyah-Singer index theorem supplies the **nonzero** mathematical continuum index

```
ind(D_L^+) = int_{M4} Ahat(TM4) ch(L)
           = 1/2 int c1(L)^2 - sigma(M4)/8
           = 1.
```

This is deliberately stronger than TOE65's nonnative torus cohomology control, but weaker than the target **native lattice overlap-operator index**: the constructed M4 requires an imposed ribbon rotation, added T2, chosen line bundle and spin structure. It is not canonically selected by W33, does not construct an admissible discretized overlap Dirac operator, and does not yield an anomaly-free Standard Model Weyl spectrum. The topological index is a rigorous *mathematical existence example* only.

## 5. Interacting gauge-fermion residual control: quantitative negative result

The original TOE62/65 native 14-site, 16-link, 6-fermion, 6-contained-octagon Gauss-constrained patch was **not rediagonalized** in this pass. Instead its stored numerical eigenvectors' `Fock_boundary_weight`, `electric_flux_boundary_weight`, and eigensolver residuals were used to derive an a-posteriori upper bound on the norm of the **full-patch** Ritz residual when a truncated Ritz vector is extended by zero:

```
|| (H - E_Ritz) psi || <=
     16*kappa*sqrt(P_Fock shell)
   + 6*(beta/g^2)*sqrt(P_flux shell)
   + numerical_eigensolver_residual
 = 11.2 sqrt(P_Fock) + 3.75 sqrt(P_flux) + r_num .
```

Derivation: any single fermion hop changes reachable Fock depth by at most one, so missing transitions require depth-shell support. A simple native octagon crosses each chord at most once, so outgoing magnetic shifts require flux-shell support. Each hopping term's operator norm is at most kappa, and each magnetic plaquette term at most beta/g^2. Triangle inequalities yield this explicit upper bound.

For the neutral sector, the reported residual upper bounds are approximately:
- depth 2, flux cutoff 3: `5.0975`;
- depth 3, flux cutoff 2: `3.8974`.

By the spectral theorem, the full Hamiltonian has *some* spectral point within this radius of the Ritz energy, but nothing ensures that point is its ground energy. The bound is not small enough to certify convergence. The neutral ground-energy shifts from depth2/L2 to depth2/L3 and from depth3/L1 to depth3/L2 are approximately `-0.001216` and `-0.102868` respectively.

This prevents using apparently small flux-boundary occupation as a convergence claim when the fermion truncation remains severe. Ciavarella et al., *Truncation uncertainties for accurate quantum simulations of lattice gauge theories*, arXiv:2508.00061, develops related truncation-error methodology, but its assumptions are not imported into our patch without proof.

## Reproducibility and strict scope

- Producer: `analysis/w33_20261014_toe66_five_physics_followthrough.py`
- Frozen certificate: `data/w33_20261014_toe66_five_physics_followthrough.json`
- Regression: `tests/test_w33_20261014_toe66_five_physics_followthrough.py`
- Reconstruction independently performed on server and matched the TOE65 18-edge exact integer polynomial.
- Five tests passed in a server-side reconstruction, including all five fronts. GitHub CI results should be checked separately once published.
- All numerical labels (finite-beta local curvature and existing native Gauss-sector energies) are distinguished from exact arithmetic and topology.
- **The physical TOE remains open:** no unique spacetime dynamics, Lorentz-covariant interacting continuum, native overlap index, Weyl anomaly cancellation, gravitational constraint algebra, or measured prediction has been obtained.

## Five independent successors

1. Certified branch-and-bound or semidefinite interval methods over the 160 binary edge corners to close the 14.8756–24.4616% disorder gap.
2. All-beta *continuous uniform* flux proof via exact determinant bounds or certified counterexample, separately from disorder.
3. Test competing W33 rotation systems and dynamics that might select a canonical ribbon/handlebody geometry instead of imposing one.
4. Discretize the derived spin four-manifold, build explicit admissible U1 links and compute a native overlap-Dirac index and anomaly tests.
5. Improve interacting residual estimates using coherent boundary-channel norms and rigorous spectral isolation, then scale cutoffs independently.
