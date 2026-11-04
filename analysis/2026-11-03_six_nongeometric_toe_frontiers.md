# 2026-11-03 — Six independent TOE falsifiers: algebraic locality, curved holonomy, causal growth, Pachner topology, universal spin-2 matter, operational metric

**Scope:** User requested all five independent fronts after the preceding six-track local-gravity/causal-growth study, plus creative extensions. These six programs are *reproducible mathematical and numerical controls*. **They do not establish a complete Theory of Everything, derive the Standard Model, or generate emergent 3+1-dimensional Lorentzian gravity.**

## Prior repo checks and independent literature

Initial local and GitHub `master` at `d6948329503b7ccec863d0c41b54b5c119a70187`, with 57 existing dirty/untracked files owned by parallel work. Searches of the indexed repository and inspection of recent commit history found relevant existing owners:

- `analysis/2026_11_03_local_spin2_hamiltonian_closure.py`: commuting flat spatial derivatives lead to a **linear** first-class constraint algebra, while an x-varying local derivative breaks the naive brackets. The new curved packet directly builds a covariant gauge connection and quantifies its discrete curvature, **not** a curved gravity Hamiltonian.
- `analysis/2026_11_03_csg_action_heldout.py`: one transitive-percolation null vs 4D Minkowski sprinklings. The new competition independently fits two qualitatively different random history families using training density and withholds three other causal diagnostics.
- `analysis/2026_11_03_incidence_dimension_phase_competition.py`: dimensions were labels of candidate hypercubic states and changed via global D moves. The new code implements **actual local Pachner 1-3, 3-1, 2-2 moves**, and exposes the invariant manifold dimension.
- `analysis/2026_11_03_two_species_stress_gravity_ward.py` is new; the preceding `analysis/2026_11_03_spin2_soft_ward_universality.py` contained a purely massless two-species soft Ward example. Here separate real scalar fields have **different supplied masses**, exact conserved stress tensors, an offshell negative control, and elastic mixed-mass rational kinematics.
- The repo contains operator-algebra and quantum-error-correction experiments, but the new independent `[[5,1,3]]` code packet certifies all 2-erasure errors, all 3-of-5 reconstructions, and an explicit *same encoded unitary, distinct physical supports* counterexample.
- The new operational-metric packet extracts shortest-path distance from the first nonvanishing quantum-transfer Taylor coefficient, comparing nonisomorphic same-degree graphs. This is a theorem for **supplied graph Hamiltonians**, not a dynamical spacetime derivation.

Literature checked: [Pachner moves preserve PL-type](https://link.springer.com/article/10.1007/s00454-026-00818-w), [a quantum-error-correcting five-qubit code](https://doi.org/10.1103/PhysRevLett.77.198), [operator-algebraic reconstruction](https://arxiv.org/abs/1607.03901), [lattice-gauge Wilson curvature](https://pmc.ncbi.nlm.nih.gov/articles/PMC12026112/), [quantum information propagation bounds](https://doi.org/10.1103/PhysRevA.81.062107), [causal-set sequential growth](https://doi.org/10.1103/PhysRevD.61.024002), and [soft graviton universality](https://doi.org/10.1103/PhysRev.135.B1049).

## Front 1 — Curved covariant connection versus flat spin-two assumptions

Define a `U(1)` link connection on a **supplied** periodic `L×L` square lattice with lattice spacing `a=1/L` and integer flux `m`:

```text
U_x(x,y)=exp[-2πi m y/L²],
U_y(x,y)=1 except U_y(x,L−1)=exp[2πi m x/L].
```

With parallel-transport shifts `T_x,T_y`, the plaquette product is exactly `W=exp[2πi m/L²]` at every site (including torus boundaries), and

```text
T_x T_y = exp[2πi m/L²] T_y T_x,
||[T_x,T_y]|| = 2|sin(πm/L²)|.
```

An independently random local site-phase gauge change conjugates both shift operators and preserves all plaquette phases. Both identities are checked across `L=4,6,8` and `m=0,1,2`. The Wilson action `Σ_p(1−Re W_p)/a²` converges to `(2πm)²/2` on the unit-area square when `L→∞`. This is a controlled local *gauge* curvature model, **not** a curved Levi-Civita spin connection or Einstein curvature. It confirms that a flat spin-two constraint construction based on commuting ordinary derivatives cannot be transferred unchanged to curved covariant shifts; the correct curvature-dependent gravitational constraints remain unconstructed.

Producer `analysis/2026_11_03_curved_covariant_holonomy.py`; certificate `data/2026_11_03_curved_covariant_holonomy_obstruction.json`.

## Front 2 — Two blinded causal-history null models

Construct three ensembles with `N=72`: background four-dimensional Minkowski-diamond sprinklings (**dimension is input**), transitive-percolation CSG, and independent-chain stochastic growth. Fit exactly one statistic (comparable-pair fraction) on separate 15-sample target training data; select `p` over a fixed CSG grid and chain-count `k` over a fixed integer grid, using 22 samples per candidate. Freeze `p=0.04` and `k=10` before looking at the 36 withheld target sprinklings or 100 independent samples from each null.

| Held-out feature | 4D target | CSG `p=0.04` | Independent chains `k=10` |
|---|---:|---:|---:|
| Comparable fraction | 0.098733 | 0.106420 | 0.099002 |
| Longest chain | 4.3611 | 7.0700 | 11.5500 |
| Comparability components | 9.25 | 5.01 | 10.00 |
| First-four-interval L1 discrepancy to target | 0 | 0.72114 | 0.79961 |

Both stochastic growth models approach the fitted causal density but fail chain and interval structure. This is a finite-sample rejection *of these exact declared models under this benchmark*, not an exclusion of classical sequential growth generally. It is also not a proof that a random-sprinkled Minkowski diamond is a complete dynamical model of spacetime.

Producer `analysis/2026_11_03_blind_two_growth_causal_competition.py`; certificate `data/2026_11_03_blind_two_growth_causal_competition.json`.

## Front 3 — Actual Pachner dynamics and exact discrete Gauss–Bonnet

Start with the eight triangular faces of an octahedral two-sphere. Implement true local `1→3` face subdivisions, their admissible `3→1` inverses at valence-three vertices, and admissible `2→2` edge flips. After each accepted move independently certify: every undirected edge belongs to exactly two triangles; each vertex link is one connected cycle; the graph is connected and planar; Euler characteristic `χ=V−E+F=2`; and the equilateral-triangle curvature identity

```text
Σ_v (6−deg(v))=12,
Σ_v (2π−πdeg(v)/3)=4π.
```

There were **325 accepted moves** (175 flips, 74 1→3, 76 3→1), retaining all invariants. This is an actual local simplicial dynamics, not the previous global dimension-label sampler. However, a Pachner move preserves PL manifold type and its dimension by construction. A model initialized as a 2D sphere **cannot select 4D by such moves alone**. To seek genuine dimensional selection, the microscopic action must permit different-dimensional complexes or a more fundamental notion of causal adjacency—not secretly label a fixed dimension and then refine it.

Producer `analysis/2026_11_03_local_pachner_gauss_bonnet.py`; certificate `data/2026_11_03_pachner_sphere_dimension_obstruction.json`.

## Front 4 — Conservation of two separate matter stress tensors is not gravity universality

For a flat metric `diag(+1,−1,−1,−1)`, independently specify two real, on-shell scalar waves:

```text
φ_A=cos(t−x),       m_A=0,
φ_B=cos(5t−4x),    m_B=3.
T_{μν}=∂_μφ ∂_νφ−(1/2)η_{μν}[(∂φ)²−m²φ²].
```

Symbolic differentiation proves `∂^μ T^A_{μν}=∂^μ T^B_{μν}=0`, while a mass-mismatched offshell negative control has nonzero divergence. Consequently `h_{μν}(κ_A T_A^{μν}+κ_B T_B^{μν})` obeys the **linear** source-conservation requirement for arbitrary `κ_A,κ_B`. This alone does not imply the equivalence principle.

The stronger soft-graviton polarization Ward test uses exact elastic scattering of these masses:

```text
p1_A=(1,0,0,1), p2_B=(3,0,0,0),
p3_A=(3/4,3/4,0,0), p4_B=(13/4,−3/4,0,1).
```

Energy–momentum conservation holds and all legs satisfy mass shells `[0,9,0,9]`. With null soft momentum `q=(5,3,4,0)`, the exact polarization-gauge variation is

```text
δS = −73/330 × (κ_A−κ_B).
```

Therefore universal coupling is necessary in this nontrivial scattering even though *both separately conserved matter currents* pass the weaker linear test. This is a concrete two-species refinement of the existing project Ward audit, not a derived matter–graviton interaction or a proof of interacting quantum gravity.

Producer `analysis/2026_11_03_two_species_stress_gravity_ward.py`; certificate `data/2026_11_03_two_species_stress_spin2_ward.json`.

## Front 5 — A nongeometric quantum algebraic substrate and its missing physical metric

Build the [[5,1,3]] five-qubit perfect stabilizer code using

```text
XZZXI, IXZZX, XIXZZ, ZXIXZ;
logical X=XXXXX, logical Z=ZZZZZ.
```

An explicit 32×32 matrix code projector has rank two; all four generators stabilize it. The Knill–Laflamme compression identities are verified for **all 106 Pauli words of weight at most 2**, proving any two *known-location* qubit erasures are correctable. On each of the **10** possible three-qubit regions, explicit stabilizer-dressed Pauli words implement the complete logical X/Z algebra on the code.

The deeper **operational nonuniqueness** check constructs two distinct physical three-body Hermitian Pauli Hamiltonians, supported on different triples, which induce *exactly the same continuous unitary logical evolution* `exp(−iθ X_L)` on all encoded states, at three tested angles. Their full physical operator difference has nonzero norm, but their code-restricted dynamics agree up to floating-point tolerance. Thus even a protected logical observable with a known evolution law **need not identify the unique physical region or microscopic geometry**.

This is an independent proof-of-concept for quantum operator-algebraic encoding. To obtain geometry from it, one must add a physical Hamiltonian, an observable net, modular structure or operational propagation constraints. The code **does not derive AdS/CFT, RT entropy, Einstein gravity, or a bulk causal metric**.

Producer `analysis/2026_11_03_five_qubit_algebraic_locality.py`; certificate `data/2026_11_03_five_qubit_algebraic_locality.json`.

## Bonus — a metric *can* be inferred from supplied quantum dynamics

Given an explicitly supplied finite simple graph with adjacency matrix A and one-excitation Hamiltonian `H=J A`,

```text
U_{ji}(t)=Σ_{k≥0} (−iJt)^k (A^k)_{ji}/k!.
```

By the nonnegative walk-count interpretation of `A^k`, `(A^k)_{ji}=0` whenever `k<dist(i,j)`, whereas `(A^dist)_{ji}>0`. Therefore:

```text
dist(i,j)=minimum Taylor order of <j|exp(−itA)|i> that is nonzero.
```

Exhaustive 8×8 operator tests certify all pairs on two connected nonisomorphic **3-regular** eight-vertex graphs. On the cube `Q3`, the unordered distance census is `12,12,4` at distances 1,2,3. On the Möbius ladder `M8`, it is `12,16` at distances 1,2. Thus the dynamical transfer amplitudes distinguish two networks that have identical numbers of sites and local degrees, and recover their intrinsic interaction distance exactly.

The critical qualification: the interaction adjacency A is an **INPUT**. The result explains how operational geometry can be *read from dynamics* but not how a nongeometric algebra selects those interactions. The freedom `J→λJ,t→t/λ` also leaves the evolution unchanged, so absolute propagation speed and physical scale remain undetermined without independent calibration.

Producer `analysis/2026_11_03_operational_metric_from_dynamics.py`; certificate `data/2026_11_03_operational_metric_from_dynamics.json`.

## The new synthesis: coding and dynamics are jointly necessary but not yet sufficient

The code alone has **many equivalent physical reconstructions** and cannot choose a metric. The adjacency Hamiltonian alone has a **uniquely reconstructible operational shortest-path distance**, but supplies its microscopic interactions by hand. These together suggest a sharper research program than seeking integer coincidences:

1. Define a microscopic observable algebra, state/encoding, and a **locality-selecting action** without imposing a spacetime dimension.
2. Let its dynamics select a stable interaction algebra or adjacency relation; operationally reconstruct distances from commutator growth/transfer Taylor coefficients.
3. Require this operational distance to support scale-stable manifoldlikeness and an emergent Lorentz cone, using blinded non-geometric causal competitors.
4. Derive local first-class gravitational constraints, not just TT projections or flat-space descendants; test soft-graviton universal coupling to independently constructed species.
5. Show that the same action fixes the relevant relative hierarchy and has a separately calibrated, independently predictive dimensional scale.

This is a **conditional strategy, not a completed derivation**. No current test satisfies all five criteria.

## Reproduce

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -m pytest -q -s -o addopts='' tests/test_20261103_six_geometry_free_toe_tests.py --maxfail=1
```

The focused module independently reruns all six producers and verifies saved certificates. Full repository suite not invoked. The original 57 parallel dirty worktree entries must remain untouched. Outputs are in distinct `data/2026_11_03_*.json` files.

## Source-specific references

- Pachner equivalence / PL-homeomorphism: https://link.springer.com/article/10.1007/s00454-026-00818-w .
- 2D local Pachner flip and subdivision definitions: https://link.springer.com/article/10.1007/s11005-024-01874-0 .
- Five-qubit code: https://doi.org/10.1103/PhysRevLett.77.198 .
- Algebraic code reconstruction and complementary regions: https://arxiv.org/abs/1607.03901 .
- Introductory Wilson lattice curvature: https://pmc.ncbi.nlm.nih.gov/articles/PMC12026112/ .
- Local interaction propagation/Lieb–Robinson scale: https://doi.org/10.1103/PhysRevA.81.062107 .
- Causal set sequential growth: https://doi.org/10.1103/PhysRevD.61.024002 .
- Soft graviton universality: https://doi.org/10.1103/PhysRev.135.B1049 .
