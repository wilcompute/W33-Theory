# Seven research controls around Császár–Szilassi duality, the Jungerman–Ringel bound, and five TOE physics fronts

**Date:** 2026-11-15. **Code:** `analysis/toe_20261115_genus_duality_sevenfront_falsifiers.py`; **data:** `data/toe_20261115_sixfront_genus_duality_native_tests.json`; **tests:** `tests/test_toe_20261115_genus_duality_sevenfront.py`. Existing source data is read without modification through AST literals.

## Executive result and epistemic boundary

The Császár `(V,E,F)=(7,21,14)` and Szilassi `(14,21,7)` have the *same abstract genus-one toroidal map* with vertices and faces dualized. Their next neighborly genus-six rung `(12,66,44)` exists as an abstract simplicial orientable 2-manifold, and its dual has `(44,66,12)` with 12 11-sided faces.

**Important:** Schewe (2008 preprint, 2010 publication) proved all 59 orientable 12-vertex genus-six neighborly triangulations **lack a flat triangular polyhedral embedding in R³**. That theorem does not automatically rule out a *geometric realization of a combinatorially dual 12-face map* with planar hendecagons, which is a different realization problem. It certainly does not prohibit the abstract map, a CW complex, a high-dimensional embedding, a thickened surface after subdivision, or a topological genus-six surface in ordinary space.

These are mathematical structures; none uniquely selects a quantum clock or derives physical Standard Model dynamics.

## 1. Equation origin, assumptions and the correct genus-three-way distinction

Jungerman–Ringel, *Minimal triangulations on orientable surfaces* (1980), derived `V >= ceil[(7+sqrt(1+48g))/2]` from `E<=C(V,2)`, `3F=2E` and Euler `V-E+F=2-2g`. When equality in the edge inequality holds, the triangulation is **neighborly** (1-skeleton `K_V`) and

`g=(V-3)(V-4)/12,\quad E=C(V,2),\quad F=V(V-1)/3`.

These are **exact** under the assumption of a closed simplicial *orientable triangular* embedding with a complete vertex graph. The arithmetic integrality condition requires `V mod 12 in {0,3,4,7}`, not a guarantee of a *straight-faced 3D polyhedron*. The next rungs are `(n,g)=(4,0),(7,1),(12,6),(15,11),(16,13),(19,20),(24,35)`.

The **graph genus** of `K_n`, for arbitrary n, is `ceil((n-3)(n-4)/12)`, by Ringel–Youngs; an integer after ceiling need not correspond to a triangular embedding. For example, `K8` has genus 2 but there is no neighborly 8-vertex triangulation with genus 2.

The Jungerman–Ringel **minimum-vertex / minimum-face triangulation** formula holds for genus g except the genus-two exception: `V_min(2)=10`, `F_min(2)=24`; the naïve Heawood lower bound would allow nine vertices, but the bound is not attained at g=2.

For a **face-complete simple cubic dual**, start with n faces, one common edge for every face pair, and exactly three faces at each vertex. Then `E=C(n,2),V=2E/3`, and the *same* polynomial `g=(n-3)(n-4)/12` results. The primal and dual are **not two independent genus equations**; they are one Euler identity under combinatorial duality.

The 1996 Altshuler–Bokowski–Schuchert list has 59 abstract orientable K12 triangulations. Schewe's paper proves the 3D geometric impossibility, using SAT constraints on admissible acyclic, uniform oriented matroids. An earlier 2000 paper of Bokowski–Guedes de Oliveira excluded only one of these triangulations.

**External foundational sources:**
- Jungerman and Ringel, *Minimal Triangulations on Orientable Surfaces*: https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6282-11511_2006_Article_BF02414187.pdf
- Altshuler, Bokowski and Schuchert (1996): https://www.sciencedirect.com/science/article/pii/S0097316596900692
- Lars Schewe (arXiv:0801.2582 / *Discrete & Computational Geometry* 43, 2010): https://arxiv.org/abs/0801.2582 ; https://doi.org/10.1007/s00454-009-9222-y
- Grünbaum and Szilassi (2009), *Geometric Realizations of Special Toroidal Complexes*: https://faculty.washington.edu/moishe/branko/BG277%20Toroidal%20complexes.pdf
- Conder regular-map database, dual Heawood map: https://weddslist.com/rmdb/map.php?a=C1.t1-3
- Wikipedia: https://en.wikipedia.org/wiki/Cs%C3%A1sz%C3%A1r_polyhedron and https://en.wikipedia.org/wiki/Szilassi_polyhedron
- Explicit specialized realizations: https://dmccooey.com/polyhedra/Csaszar1.html and https://dmccooey.com/polyhedra/Szilassi1.html

Grünbaum–Szilassi (2009) separately proves **all even numbers >=14 of triangular faces occur for geometric torus triangulations** by gluing tetrahedra, and supplies detailed seven-face Szilassi hexangulation coordinates and geometric construction. This does **not** extend the complete adjacency property to every higher-face hexangulation. The requested detailed "Polywiki" page was not independently located reliably in web indexing; the supplied construction notes are compared instead with the first-author paper, Conder's regular-map database, and McCooey's coordinate models.

## 2. Actual repo triangulations, dualization, homology and the Fano divide

Sources used as **immutable input**:
- `analysis/w33_csaszar_concrete_rotation_flag_orientation.py: FACES_UNORIENTED` (seven vertices, 14 triangles);
- `analysis/w33_genus_six_execution.py: TORUS_ONE` (alternate 7-vertex torus);
- `analysis/w33_genus_six_execution.py: FACETS_ONE` (Frank Lutz catalogue of a 12-vertex genus-six neighborly triangulation).

For each face list, the verifier independently checks: distinct vertices, `K_n` skeleton, precisely two triangles per edge, consistent global orientability, connected `(n-1)`-cycle at every vertex, `3F=2E`, Euler genus, and the ranks of the two cellular boundary maps over `F_2`. This yields:

| Surface | Primal V/E/F | Genus | mod-2 Betti | Dual V/E/F | Dual face-size | Dual skeleton |
|---|---|---|---|---|---|---|
| Császár | 7/21/14 | 1 | (1,2,1) | 14/21/7 | 6 | Heawood, bipartite, girth 6 |
| Lutz N12 | 12/66/44 | 6 | (1,12,1) | 44/66/12 | 11 | cubic, connected, nonbipartite |

Each primal edge is in two triangular faces, so the faces form a `2-(n,3,2)` twofold triple system (pair multiplicity **two**). The Császár face list has exactly **two complementary ordered partitions** into two `STS(7)` Fano-plane systems (equivalently one unordered partition). Each Fano plane has seven triples covering every pair of seven points exactly once. Therefore the Heawood/Szilassi dual graph is **bipartite**: its two vertex classes are the two seven-triangle Fano systems.

If a neighborly triangulation on n vertices had a bipartite dual, color its triangles by the two dual-graph colors. Every primal edge then occurs once in each color, so **each color class would itself be an STS(n)**. In any STS(n), each point belongs to `(n-1)/2` triples; n=12 would give 5.5, impossible. Hence **all 59** genus-six 12-vertex neighborly triangulations have **nonbipartite** dual graphs. This statement is a general combinatorial theorem independent of the chosen Lutz representative. The allowed n congruence classes with *possible* STS split require n ≡1 or 3 mod 6, i.e. n ≡7 or 3 mod 12 in the neighborly ladder; necessary but not sufficient.

The abstract dual face adjacency graph remains the complete `K_{12}`, requiring 12 colors on the genus-six surface and attaining the Heawood map-color bound for genus six. It does not give a 12-colorable *spatial polyhedron*: the geometric realization is a separate unresolved requirement.

**Symmetry caution:** 84 flags is `4E` for both genus-one duals; the genus-six dual pair has `4*66=264` flags. The combinatorial map automorphism order is 42 in the repo's concrete face list, whereas some 3D Császár/Szilassi coordinate realizations have only cyclic order-2 symmetry, leading to 42 geometric flag orbits (if their twofold symmetry fixes no flag). A generic realization may have only identity symmetry. Do not conflate the geometric symmetry order with the abstract map group, nor call the map fully flag-transitive just because its valences are uniform. Conder's regular-map database reports the 42-element combinatorial group.

### Repo errata and falsification guards

- `analysis/W33_Part_DXXXII_Csaszar_Szilassi_Genus_Unification.md` inaccurately says both dual polyhedra have no diagonals and both "require exactly 7 vertices". Only Császár has the complete 7-vertex skeleton; Szilassi has 14 vertices and seven mutually adjacent **faces**.
- The same report equates W33's 12-point *neighbor set* with `K12`. The actual W33 point graph is SRG(40,12,2,4), whose induced 12-neighbor subgraph is **four disjoint K3 components**, **not K12**. Modeling a complete 12-body coupling requires an additional non-native interaction rule.
- `analysis/w33_pass2017_2021_the_genus_ladder_was_already_ours.md` calls the h6 12-vertex object a "polyhedron." It must be qualified as an **abstract genus-six simplicial map**, not a realized 3D straight triangular polyhedron.
- Counts `66=C(12,2)` shared by the F12 photonic mesh, the abstract genus-six skeleton, and the W33 route scheduler do **not** establish an object-level intertwiner or physical identity. The repo itself already flags the scheduler coincidence in Pass 2020.

These are new scoped verification notes, not blanket changes to unrelated historical files.

## 3. W33 native 1620-frame selector: exact incidence Gram and a 40-dimensional order parameter

Enumerate all 40 projective rays of `F3^4` and all 1620 symplectic four-ray apartments. Let `B` be the binary `1620x40` apartment-ray incidence matrix and `A` the W33 symplectic-orthogonality point adjacency. Exact integer enumeration gives

`B^T B = 156 I + 21 A + 6 J`.

The diagonal is 162 (ray frequency per apartment), off-diagonal 27 for symplectically orthogonal point pairs and 6 for nonorthogonal pairs. As W33's point graph has adjacency spectrum `12^1, 2^24, (-4)^15`, the frame overlap kernel `K=B B^T` has **rank 40** with spectrum

`648^1, 198^24, 72^15, 0^1580`.

The overlap `|F ∩ F'|` counts across all 1620 frames for a fixed frame are EXACTLY

`overlap=0:1081, overlap=1:440, overlap=2:90, overlap=3:8, overlap=4:1`.

Thus each frame has eight nearest one-ray-change neighbors; uniform overlap is `648/1620=2/5`. This is a natural **W33-derived PSD interaction kernel**, not an arbitrary table of frame rewards.

### Additional seven-front result: 45 exact K4,4 sectors, each a product of octahedral Johnson graphs

Build the frame transition graph `T` with edges where `|F∩F'|=3` (replace exactly one projective ray). Exhaustive integer adjacency and graph isomorphism tests reveal:

- `T` is 8-regular on 1620 frames but has **45 connected components**, exactly **36 frames each**.
- Each component's 36 frames jointly involve exactly **eight** W33 rays; their induced W33 point graph is isomorphic to **`K4,4`**, independently verified for all 45 components.
- Every frame selects **two from each of the two four-ray classes** of its K4,4; this gives `C(4,2)^2=36` choices. The one-ray move graph is **`J(4,2) Cartesian J(4,2)`**, the Cartesian product of two octahedral graphs, tested by checking each pair of frames inside *every* component.
- Its exact integer adjacency spectrum is `8^1, 4^6, 2^4, 0^9, (-2)^12, (-4)^4`; a numerical eigencheck of an entire component confirms the multiplicities.
- The 45 eight-ray supports are distinct, and every one of the 40 W33 rays occurs in **nine** of them (`45*8=40*9`).

Therefore the single-ray generator can NEVER traverse all 1620 frames: its dynamics is exactly a direct sum of 45 finite octahedral-product sectors. **Any true W33 frame mixer needs transitions that change the eight-ray K4,4 support**, not just the selected pairs within it. This is a strong native-locality falsifier, not an identification of physical spacetime or an unobserved gauge field.

 A *hypothetical* attractive mean-field energy `-J/(2M) Σ_{a,b}|F_a∩F_b|` is fully PSp-invariant. The all-aligned state beats the uniform distribution in free-energy comparison for `beta J > 2ln(1620)/(4-2/5)≈4.10565635`; the uniform local Hessian loses positivity at `beta J=1620/198≈8.18181818`. The first number is a **sufficient comparison**, not a proved critical coupling; no native physical ferromagnetic interaction is derived. Finite-M Gibbs equilibrium remains symmetric.

## 4. Driven **local** H27 four-step commutator, exact

On the 27-dimensional left regular representation of Heisenberg `H27`, take order-three translations `Ux,Uy`, each supported on the local `±X,±Y` Cayley graph of degree four. Define

`H_X = (2π/(3√3)) i (U_X-U_X†)`,
`H_Y = (2π/(3√3)) i (U_Y-U_Y†)`.

Since the translations have order 3, these are local Hermitian matrices with **54 nonzero directed hopping entries** each and `exp(-iH_X)=U_X`, `exp(-iH_Y)=U_Y` exactly.

Chronological pulses `(-H_Y,-H_X,H_Y,H_X)` implement `U_X U_Y U_X^{-1} U_Y^{-1}=U_Z` (central order three). Therefore **12 unit-duration pulses** return to the identity. The independent 27x27 matrix exponential control has error `~2.5e-15`. The prior impossibility of a short-range **time-independent Hamiltonian logarithm of one isolated 12-cycle shift** is not violated: this construction uses explicit time-dependent switching and Cayley graph locality. No physical frequency, energy, autonomous schedule or energy conservation of the *control drive* has been selected.

## 5. New D9 gauge-compensated massless-vector sector, not the full KK spectrum

The prior model is the exact classical `R-F²/4` Einstein–Maxwell compactification on `AdS5 × S² × S²` with quantized magnetic flux. On each sphere with local flux `F=f sin(theta)dtheta∧dphi`, the usual rotation Killing vector fields `K_x,K_y,K_z` satisfy exact symbolic identities

`i_{K_i}F = d(mu_i)`, with `mu_i=f(sinθ cosφ, sinθ sinφ, cosθ)_i`.

Hence `Lie_{K_i}F=d i_KF=0`: rotational isometries of the metric leave the magnetic field invariant up to a U(1) gauge transformation of the potential. The two spheres contribute a **6-dimensional gauge-compensated isometry algebra** `so(3)⊕so(3)`; together with the previously established uniform abelian vector zero mode, they supply **seven symmetry-protected five-dimensional gauge directions** in the classical reduction.

These are infinitesimal symmetry arguments, **not a diagonalization of the coupled KK scalar/vector/tensor mass matrices**, and global bundle lifting and E6 ExFT embedding remain open.

## 6. Detector-level photonics: actual cost of learning the assumed 16x16 calibration

Prior witness certificate (`903c4ff152dc`) assumed that every **column** of a 16×16 conditional confusion matrix was known to total variation/ℓ1 accuracy ε=0.002, with 99% fidelity confidence. This pass exposes the cost of establishing that accuracy independently and distribution-free.

For any distribution `p` on k=16 categories, `||p_hat-p||1=2 max_{S subset[k]}|p_hat(S)-p(S)|`. Apply two-sided Bernoulli Hoeffding to all `2^16` subsets and union bound across 16 independent prepared input rails:

`Pr(any of 16 columns has ℓ1 error > ε) ≤ 16*2^17*exp(-n ε²/2)`.

At ε=.002 and joint failure probability α=.01, a **sufficient** calibration budget is

`n=9,580,631 accepted calibrations per prepared input rail; total 153,290,096`.

This is **~2816x** the earlier *nominal expected* 54,438 signal launches. It is deliberately conservative; it is NOT a minimax sample-complexity lower bound, nor an optimized/structured/noise-model calibration. With a known sparse circulant confusion model and direct weighted endpoint-contrast estimation, much less calibration may suffice. Nevertheless it prevents treating an assumed 0.002 full-matrix confidence interval as cost-free. The 99% calibration and 99% witness confidence events require careful error-budget splitting if one wants **joint** overall 99% certification.

## 7. F8 exact SOS certificate scope and remaining gap

Read and check the *existing* Pass12673 `data/w33_f8_codespace_sos6_certificate_249_100.json`: it certifies `c8 ≥ 249/100=2.49` **on one eight-dimensional code space**, with both recorded Gram blocks PSD-certified. The prior Pass12671 exact six-qubit witness gives global **upper** bound

`c8 ≤ (47-32cos(2π/9))/9≈2.498508646688078`.

The within-code-space bracket width is about **0.00850865**. This is not a global full-C64 lower bound because the SOS certificate is restricted to a selected code space. Our Pass `903c4ff152dc` full-space Hessian had 124 positive / 2 numerically flat / 0 negative tangent directions; its degree-eight straight-family identity residual was about 2.7e-15, **still not an exact algebraic family certificate**. No claim of resolving the global F8 optimum here; this pass enforces prior-art boundaries and directs algebraic reconstruction.

## Commands and next independent research targets

```powershell
py -3 analysis/toe_20261115_genus_duality_sevenfront_falsifiers.py
py -3 -m pytest tests/test_toe_20261115_genus_duality_sevenfront.py -q
```

**Highest-priority falsifiers:** (a) exact algebraic F8 tangent families and global lower bound; (b) solve mixed D9 metric-Maxwell KK blocks and distinguish lifted bundle gauge vectors; (c) engineer a physically autonomous Cayley-local H27 control program without an external four-pulse schedule; (d) determine whether the W33 frame overlap kernel admits a native bounded-locality dynamical generator and stable ordered thermodynamic limit; (e) replace full-crosstalk estimation with direct observer witness calibration; (f) formulate the genus-six abstract dual as an orientable-matroid/planar-hendecagon 3D feasibility problem **without** contradicting Schewe's proved primal no-go.


## Additional executed locality falsifier — the minimum inter-sector move changes two rays

The exact one-ray graph decomposes into 45 disconnected sectors of 36 frames, each isomorphic to J(4,2) Cartesian J(4,2) and supported on a K4,4. Independently enumerate all transitions where two four-ray frames overlap in **exactly two** rays (replace exactly two rays).

Every one of the 1620 frames has exactly **90** such two-ray neighbors: 18 remain inside its original K4,4 sector, while 72 jump to a different one. The graph consisting of **two-ray moves alone is connected** on all 1620 frames, as verified by exact adjacency construction and NetworkX connected-component enumeration. Adding the one-ray edges retains connectivity.

This identifies the **minimal number of ray replacements required for ergodic frame mixing under this notion of move: two**. One replacement is provably confined to a single of 45 36-state Johnson-product components; two suffice to connect all sectors. It does not prove that a two-ray jump is generated by a physically local Hamiltonian in spacetime, that it is a valid code operation on photonic modes, or that an energy-cost assignment is unique.
