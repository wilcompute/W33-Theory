# Causal incidence → torus topology → gauge-covariant overlap fermions: exact bridge and noise/chirality obstructions

**2026-11-19. Status: five grid-size demonstrations, four spin sectors, exact orientation/regulator controls and 600 seeded noise trials. This is NOT a Theory of Everything, 3+1 Lorentzian gravity, a derived gauge field, or a Standard Model prediction.**

This pass advances the previously committed *one-dimensional* causal-incidence Wilson-circle construction (commit 7518edfe) to a **two-dimensional spatial torus** recovered from a synthetic two-layer 2+1 causal relation. It then builds a genuine two-component overlap operator on the *inferred* graph, with externally supplied flux. The key scientific improvements are falsifiers: a reflection symmetry that prevents a preferred orientation, Wilson regulator branch ambiguity, spin-structure-dependent zero modes, and severe topological fragility under single-relation deletion. Engineered redundancy improves topology faster than it improves graph accuracy.

The overlap index itself is established Neuberger lattice fermion physics, and Dowker homology is established topology. The new-to-repository result is the executable conditional link between the two with independently checked topology and several failure controls.

Relevant literature:
- C.H. Dowker, *Homology groups of relations* (1952), and 2026 higher-order Dowker survey: https://doi.org/10.1007/s41468-026-00239-x .
- Neuberger, *A Practical Implementation of the Overlap Dirac Operator*, Phys Rev Lett 81, 4060 (1998): https://doi.org/10.1103/PhysRevLett.81.4060 .
- Families index theory for overlap lattice Dirac operator, https://www.sciencedirect.com/science/article/abs/pii/S055032130100623X .
- 2026 *No-go theorems for pointwise-defined spinorial quantum fields*, https://doi.org/10.1016/j.nuclphysb.2026.117605 . This is a reminder that a real continuum fermionic quantum field should be distribution/smeared-operator valued, not assumed to be a pointwise continuous operator; no new no-go is proved here.

**Parallel-commit collision audit (performed before publication).** While this session ran, GitHub master advanced to `8f9ffe846a690a6515ec4f8616fee7aadcacbbb5`, which **independently already implemented a causal torus to overlap flux bridge** using **3-by-3** witness shadows on n=5..8 lattices. We read its full diff. We are **not** claiming the existence of a causal-torus/overlap bridge as a uniquely new discovery. This packet is separately useful because it uses the **minimal 2-by-2** cover on n=5..9, independently recovers **both simplicial and square-cell boundary homology**, reconstructs elementary faces and tests local U1 gauge covariance, tests **four spin structures and their zero-mode spectra**, measures the exact **100/100 single-relation fragility**, and performs **600 replicated-shadow dropout trials** separating Betti recovery from four-neighbor accuracy. The parallel commit also independently calculated SU2 center/matter loops, optical SSR activation, Burnside causet orbit measures and flavor connections; those results are not re-announced here. Another concurrent commit, `d1a3119152e7a286cb80820621c3d59193565ae8`, developed separate E8 Higgs and BDG4 causet scalar tests. The present investigation remains conditional and does not resolve any TOE problem in full.

## I. Exact, topology-first construction from a two-layer causal relation

Start with a **given** periodic square n-by-n spatial layout at one time and another set of n-by-n future witness events. Generate a binary relation R(a,w)=1 iff the future witness lies in the 2-by-2 forward square shadow of the antichain event. The construction explicitly assumes a toroidal generating layout, equal layer sizes n² and a particular witness scale. These are inputs.

**All subsequent topology and graph recovery uses only R**:
1. Enumerate the Dowker nerve: a set of future witnesses is a simplex precisely when they have a common causal-past antichain event. Compute exact boundary matrix ranks over GF(2) for dimensions one through three; tetrahedra are required because a 2-skeleton alone can give a spurious b2.
2. Compute C=R^T R, the common-past witness overlap. Non-diagonal entries of maximal overlap define a four-regular spatial graph. Enumerate its induced chordless 4-cycles and check that each graph edge lies on two square faces.
3. Reconstruct *one of the possible coordinate frames* from the undirected graph, using opposite neighbor relationships and face-completion transport, **without** receiving an edge list or coordinate positions from the generator. Check every inferred x/y neighbor against the original graph.
4. Build the independent cellular chain complex on recovered vertices, edges and square faces, compute both GF2 boundary ranks and V-E+F. Require **simultaneous** homology agreement between the Dowker nerve and recovered cell complex.

| Grid n | Recovered V, E, F | Euler characteristic | Dowker nerve (b0,b1,b2) | Independent square-cell (b0,b1,b2) |
|---|---|---:|---|---|
| 5 | 25,50,25 | 0 | 1,2,1 | 1,2,1 |
| 6 | 36,72,36 | 0 | 1,2,1 | 1,2,1 |
| 7 | 49,98,49 | 0 | 1,2,1 | 1,2,1 |
| 8 | 64,128,64 | 0 | 1,2,1 | 1,2,1 |
| 9 | 81,162,81 | 0 | 1,2,1 | 1,2,1 |

**Falsifier:** a graph alone does not determine the filled faces or homology; unlike simple graph coincidences, both the complex's higher-dimensional boundary maps and cellular edge/face incidences must agree. The method is not a stochastic Lorentzian manifold emergence result.

## II. The operator bridge: actual overlapping gauge/fermion transport on recovered edges

Now **supply** a U(1) compact lattice link connection with integer flux Q, using the recovered coordinate frame. Landau-gauge phases on +x/+y links are

    Ux(x,y) = exp(-2*pi*i*Q*y/n²),
    Uy(x,y) = exp(+2*pi*i*Q*x/n)  if y=n-1, else 1.

These give a uniform plaquette angle +2*pi*Q/n². The program verifies the phase around **every** recovered square and total plaquette winding Q. A U(1) gauge connection has NOT been derived from order, and the phase convention depends on a chosen orientation.

Insert the standard 2D Euclidean Pauli matrices gamma_x=sigma_x, gamma_y=sigma_y, gamma5=sigma_z, Wilson regulator mass m=1, and build the Hermitian Wilson matrix

    H = gamma5 [ (2-m)I
          -(1/2) sum_mu (T_mu tensor (I-gamma_mu)
                        +T_mu^dagger tensor (I+gamma_mu)) ].

Obtain the overlap index via -Tr sign(H)/2, the full overlap matrix

    D_ov = I + gamma5 sign(H),

and verify the Ginsparg–Wilson identity gamma5 D + D gamma5 = D gamma5 D.

| Grid | Flux Q=-1 | Q=0 | Q=+1 |
|---|---:|---:|---:|
| 5x5 | index +1 | index 0 | index -1 |
| 6x6 | +1 | 0 | -1 |
| 7x7 | +1 | 0 | -1 |
| 8x8 | +1 | 0 | -1 |
| 9x9 | +1 | 0 | -1 |

All Hermitian Wilson kernels remain gapped in these tested sectors. On the nonzero-index n=5 case, the full Ginsparg–Wilson Frobenius residual was **2.15e-14**. The actual full operator has the required overlap zero mode(s). Independent random antichain and witness relabelings recover the same topological and chiral-index *relative to an arbitrarily chosen reconstructed orientation*. Independent random sitewise U(1) gauge-frame transformations preserve the kernel gap, index and Ginsparg–Wilson identity. A separate implementation already in the repo (analysis/toe_20261105_overlap_flux_chirality_index.py) agrees on flux/index for n=5.

**Boundary:** This proves no more than a finite EUCLIDEAN TWO-DIMENSIONAL overlap construction on a given synthetically produced spatial torus with an inserted U1 connection. A physical 3+1 Lorentzian causal fermion operator, chiral SU2xU1 gauge theory, Standard Model anomaly freedom and gauge dynamics remain missing.

## III. Three independent nonuniqueness/fragility controls

### A. Orientation-reversing automorphism prevents intrinsic chiral sign

For the square-shadow relation, swap coordinates x<->y for all antichain and witness event labels. This permutation preserves R EXACTLY, while it reverses the orientation of the recovered torus (det=-1 on H2). Hence an automorphism-equivariant deterministic method cannot extract a preferred nonzero oriented fundamental class or an oriented Chern sign from R alone. It must choose orientation, break the symmetry or supply other physical structure. This does NOT forbid chirality in an asymmetric microscopic model; it identifies a precise missing input in this maximally symmetric benchmark.

### B. Same recovered geometry, five possible indices plus a Wilson branch sign flip

We hold the very same recovered toroidal graph fixed. At mass m=1 the external fluxes Q=-2,-1,0,+1,+2 yield overlap index +2,+1,0,-1,-2. If the Wilson mass branch is instead m=2.5, the same fluxes yield -2,-1,0,+1,+2. Therefore neither the gauge field's Chern number nor the regulator branch follows uniquely from the recovered causal incidence. The Wilson regulator branch check reproduces prior standard lattice-fermion results, now on a graph inferred from order.

### C. A single missing causal relation destroys the minimal cover's b2

We deleted each of the 100 relation entries, one at a time, from the n=5 matrix. **100/100 cases** changed the Dowker nerve's (b0,b1,b2) from (1,2,1) to (1,2,0). This is a precise failure of robust T2 recovery under noisy incidence in this *minimally redundant* 2-by-2 cover. It is not a theorem about stochastic causal-set topology reconstruction more generally.

## IV. Four Spin structures: the index does not select the fermion vacuum

Since T² has H¹(T²;Z2)=Z2², there are four possible spin structures. The program supplies independent periodic/antiperiodic twists along the two recovered fundamental cycles via flat Z2 boundary links and recomputes the *full* overlap matrix:

| Supplied flux | Spin structure | Index | Exact zero modes |
|---|---|---:|---:|
| Q=0 | periodic x, periodic y | 0 | 2 |
| Q=0 | all other 3 choices | 0 | 0 |
| Q=+1 | each of all 4 choices | -1 | 1 |

The Ginsparg–Wilson relation passes for every tested sector. **A net chiral index is insufficient to specify spin structure or vacuum state:** the full spectral determinant can be different even when the index is identical. This operationally links the causal topology effort to the earlier fermionic path-integral and sector-weight calculations, but no physical selection is inferred without matter content, physical mass and functional integration.

## V. Outside-box connection: topology can survive noise before local Dirac adjacency does

We tested **engineered antichain redundancy** as an intentionally transparent correction to the fragility above. Each original four-link antichain shadow is repeated k times, then each relation independently deleted with probability p=.05. This is **not a real Poisson sprinkling**. It is an artificial repeated-measurement model, intended to separate robust topology from robust local connectivity.

An exact *sufficient* probability for all original maximal simplices to be retained is

    P_sufficient(n,k,p) = [1-(1-(1-p)^4)^k]^(n²).

Independent seeded Monte Carlo (200 trials per k, n=5) produced:

| Replicas k | Torus b=(1,2,1) recovered | EXACT top-four common-past neighbor graph recovered | Analytic sufficient probability |
|---:|---:|---:|---:|
| 1 | 1.5% | 1.5% | 0.592% |
| 2 | 45.0% | 14.5% | 41.672% |
| 4 | 99.5% | 89.0% | 97.082% |

This illustrates an important **cross-sector requirement**: stable topological Betti numbers do not guarantee enough graph-local transport information for a physically reliable Dirac operator. A quantum gravity / fermion reconstruction method needs BOTH homological persistence and a stable, geometrically local spin connection. Merely passing b1,b2 is not adequate.

The Monte Carlo rates carry ordinary finite-sampling uncertainty and cannot be generalized to true causal spacetime without stochastic sprinkling, manifold learning, density scaling, and physically justified graph inference.

## VI. What the pieces allow us to derive next, and what they do not

The present finite chain is now:

    synthetic (2+1) causal incidence R
        -> independently reconstructed Dowker and cellular torus T2
        -> face-compatible local coordinate/transport graph
        -> [SUPPLY U(1) curvature Q, orient 2D spin frame, choose regulator]
        -> Hermitian Wilson/overlap operator
        -> exact zero modes, chiral index and spin-twist-dependent spectrum.

The most interesting lesson is a *conditional dynamical shortcut*: if a genuine Lorentzian 3+1 causal Dirac operator and physical matter masses can be derived, fermionic functional determinants could provide relative weights for spin/gauge sectors and remove an independent postulate. But as of this pass, gauge curvature, chirality orientation, matter, dynamics and the quantum measure remain extra inputs. In this test the same R is compatible with distinct externally assigned Q, opposite Wilson regulator branches, and all four spin structures.

The 2026 paper on pointwise spinorial fields further cautions against assuming a physically meaningful continuum operator-valued fermionic field is pointwise continuous; a viable continuum limit must handle smeared fields, microlocal properties and state positivity appropriately. We have not tested that in the present finite benchmark.

## Reproduce and test

    python analysis/toe_20261119_causal_torus_overlap_flux_v9.py
    python -m pytest -q tests/test_toe_20261119_causal_torus_overlap_flux_v9.py

The environment may require single-threaded BLAS for speed. The code uses integer-to-Python-int conversion before GF2 bit shifts to avoid fixed-width numpy integer overflow beyond 64 vertices; a separate regression exercises this case explicitly.

New files:
- analysis/toe_20261119_causal_torus_overlap_flux_v9.py
- tests/test_toe_20261119_causal_torus_overlap_flux_v9.py
- data/toe_20261119_causal_torus_overlap_flux_v9.json
- analysis/2026-11-19_causal_torus_overlap_flux_spin_noise.md

**40 focused tests passed**, including independent prior-code index crosschecks, larger n=8,9 homology, gauge frame covariance, random label permutation, spin zero modes, 100 deletion cases, and redundancy checks. Run a selected historical overlap/causal regression separately before committing.

## Five orthogonal high-leverage next experiments

1. **Replace synthetic square causet input with genuine stochastic 3+1 Lorentzian sprinklings**, reconstruct thickened antichain T3/S3/S1xS2 nerves and local transport jointly, and quantify topology/Dirac connectivity robustness across density and noise.
2. **Select oriented chirality dynamically rather than assign it.** Test an intrinsic discrete tetrad/Clifford structure, parity-breaking candidate action, and chiral anomaly index against the exact reflection automorphism obstruction.
3. **Derive gauge curvature rather than add integer flux Q.** Construct a physical U1/SU2 connection from causal spin/gauge transport and a gauge-invariant field action, then see whether flux-sector weights or center line operators predict an observed gauge state.
4. **Quantize the recovered fermions with a real state/functional measure.** Compute zero-mode-saturating correlators, spectral determinants and normalized spin-structure weights; require causal propagation, state positivity and the appropriate continuum smeared-field conditions.
5. **Couple the actual 3+1 causal fermions to emergent gravitational and Standard Model dynamics.** Demonstrate a Lorentzian Einstein continuum with spin-2 excitations and an anomaly-free chiral matter spectrum, including neutrino neutrality and nontrivial predictive couplings, before claiming TOE completion.

**Scientific verdict:** a substantial computational bridge beyond the prior circle is now reproducible; a direct chain from topology to observed parity violation or quantum gravity is NOT yet derived.
