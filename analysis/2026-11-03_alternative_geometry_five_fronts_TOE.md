# November 3, 2026 — Five-front TOE research with independent non-W33 causal and dynamical-growth falsifiers

**Scope and epistemic status:** Eight executable research packets, mostly finite exact identities and numerical controls, built after inspecting the current W33 master and relevant prior scripts. This is **not** a Theory of Everything or a demonstration of emergent 3+1D spacetime. Previous local work was left untouched.

## Repository and literature intake

Initial local/remote `master` was `58faf400658f54bb0f81efee31bdb8dd795d56d0`; 57 preexisting dirty entries were preserved. Existing relevant owners found through GitHub search and direct reading:

- **E8 hexagon reversal**: `analysis/bt1774_e8_inversion_witness.py` already provided an explicit Weyl word that conjugates the Coxeter element to its inverse, while `analysis/2026-11-03_e8_fiberwise_phase_reversal_no_go.md` established no **base-fixing** fiberwise inversion. We reconstruct the existing word and report its actual action on the 40 fibers, not claim to discover the inversion itself.
- **Spectral decimation**: `analysis/2026_11_03_pascal_two_scalar_resolvent_rg.py` already established the boundary resolvent recursion for the level-3 Pascal support graph. The new component carries the **entire characteristic determinant and Dirichlet determinant**.
- **Gauge/gravity spin two**: `analysis/w33_pass11968_native_spin2_constraint_completion.py` and `analysis/PASS11620_11624_COVARIANT_PAIR_VACUUM.md` already owned continuum Fierz-Pauli and nonlocal finite graph constraint results. The new positive control deliberately discards W33 and tests geometry/TT ranks on an externally supplied 4D lattice.
- **Process memory**: `analysis/PASS11042_INSTRUMENT_DEPENDENT_PROCESS_MEMORY.md` already owns one-slot qutrit comb checks. The quantum-switch calculation is a distinct controlled-order control, **not** a new result about process tensors in general.

Literature first-principles controls: Benincasa-Dowker-Glaser causal-set action and persistent dynamics problem, Phys. Rev. Research **8**, 023188 (May 2026), https://doi.org/10.1103/qdst-yrh6 ; indefinite causal order vs causal inequalities, Phys. Rev. Research **8**, 013127 (February 2026), https://doi.org/10.1103/9jss-yf1c ; de la Hamette et al., PRL **135**, 141402 (October 2025), https://doi.org/10.1103/bnkn-4p3f ; Weinberg's soft-graviton universality theorem, Phys. Rev. **135**, B1049 (1964), https://doi.org/10.1103/PhysRev.135.B1049 ; current analogue-gravity discussion of scope of Weinberg–Witten, https://link.springer.com/article/10.1007/s41114-026-00064-9 .

## 1. Exact global E8 inversion: the base permutation is the escape hatch

Reconstruct BT1774's two length-seven reflection words with the actual integer E8 simple roots. Verify `h c h^-1 = c^-1` on **all 240 roots**, all root positive-inner-product adjacency edges, the W33 collinearity graph, and all 40 entire six-root Coxeter fibers. The induced permutation of the 40 fibers has cycle census **8 fixed fibers and 16 transpositions**. Each fiber's phase is taken to `k -> alpha_f-k` in its **image fiber**. This resolves the earlier restricted obstruction because `alpha_f-k` with **f fixed** is impossible, but `(f,k)->(sigma(f),alpha_f-k)` with sigma nonidentity exists. No physical CP or weak interaction follows.

Producer: `analysis/2026_11_03_e8_base_permuting_inversion.py`.

## 2. Complete recursive characteristic-determinant bookkeeping

For `L_n` the unweighted level-n Pascal mod-three graph Laplacian with outer boundary B of three corners, define `Q_n(z)=det((L_n-zI)_{int,int})`, `P_n(z)=det(L_n-zI)`, and the 3-port Schur boundary matrix `D_n(z)`. Six copies of `D_n`, joined by the nine unit interblock edges, form an explicit 18×18 matrix `M_n(z)`. Block determinant identities provide:

```text
P_(n+1)(z)=Q_n(z)^6 det(M_n(z))
Q_(n+1)(z)=Q_n(z)^6 det((M_n(z))_{internal 15×15})
D_(n+1)(z)=Schur_{3×3}(M_n(z)).
```

These are **exact rational-function identities** away from removable poles, and characteristic polynomials result after cancellation. Independent dense determinants (6, 36, and 216 vertices) agree for `z=-1,-0.1,0.05`, yielding six parent/child tests each checking full determinant, interior determinant and Schur map. This is stronger than the previous boundary-visible recursion, but is not a factored all-level eigenvalue genealogy or full continuum spectral theorem.

Producer: `analysis/2026_11_03_pascal_full_determinant_rg.py`.

## 3. Actual interaction-generated gap versus pure combinatorial scaling

For an **externally posited** massless 1+1-dimensional lattice Dirac mean-field model, take the gap equation

```text
1/g= ∫_{-π}^{π} dk/(2π sqrt(sin² k + m²))
   = [2/(π sqrt(1+m²))] K(1/(1+m²)).
```

At weak positive coupling, it has `m~4 exp[-π/(2g)]`, a bona fide essential singularity in the *declared interacting model*. Direct numerical roots at `g=0.2,0.25,0.3,0.35,0.4,0.5,0.7` were checked by substitution. At `g=0.2`, `m/Λ_UV≈0.00155281`. Antiperiodic finite-volume controls with 64, 256, 1024, and 4096 sites show the finite-size threshold decreases, consistent with the logarithmic IR divergence.

**Contrast:** the Pascal exact `c_(n+1)=7c_n/15+O(c_n²)` is a hyperbolic linear contraction, not this marginal logarithmic instability. Yet the UV cutoff and g remain free: a physical mass in kg/eV/meters is not selected by dimensionless graph or gap information alone. These two models **cannot** be identified absent a derived interacting action.

Producer: `analysis/2026_11_03_marginal_gap_scale_comparison.py`.

## 4. 36-mode optical engineering controls

Use the actual 36-site Pascal Laplacian as tight-binding `H=J(D-A)`, including **degree-dependent onsite terms**. Compare with a connected **degree-preserving 100-double-edge-swapped 36-site graph**, holding vertex identities, all degrees and 63 edges fixed. At `Jt/ℏ=4`, root-injected coherent probability distributions differ by **total variation ≈0.4492**. Incorrectly deleting the degree-dependent onsite values changes the same output distribution by **TV ≈0.3961**, an engineering requirement often missed.

Further checks: twelve independent ±5% edge-coupling/onsite-detuning perturbations produce at most about **0.0781** TV in the tested set. Uniform 35% detection loss leaves **normalized** probabilities invariant, but reduces counts. With synthetic 300 injected, 195 detected photons, and both distributions known exactly, a multinomial likelihood-ratio classifier correctly distinguishes 250/250 seeded replicates from *each* hypothesis. This is **not** an actual experimental performance claim: no dark counts, crosstalk, coupling calibration or fabrication layout were modeled. The rewired graph need not be planar, making it a mathematical rather than immediately fabricable same-layer comparator.

Producer: `analysis/2026_11_03_pascal_36mode_photonic_spec.py`.

## 5. Independent spacetime routes: causal orders, a supplied continuum, process order, and local graph growth

### 5a. Poisson-sprinkled causal sets and a density-matched non-geometric null

For `N=192`, independently sample finite Minkowski Alexandrov diamonds with dimensions explicitly **supplied** as `d=2,3,4,5` (12 seeds each). The causal comparability fraction tends toward

```text
r(d) = Γ(d+1)Γ(d/2) / [2Γ(3d/2)].
```

Means: `0.5038,0.2261,0.0951,0.0413` vs theory `0.5,0.2286,0.1,0.0426`. Verify exact causal transitivity, invariance of the causal relation under a nontrivial Lorentz boost, and event relabeling. **No Minkowski dimension was inferred**, because dimension entered the sampling law.

Construct a sequentially grown **transitive-percolation** random DAG and tune its edge probability to match the same d4 sprinkling's comparability density. The two posets then have essentially equal comparable-pair fractions (~0.0954 and ~0.0953), while short-interval frequencies differ substantially (sum absolute discrepancy ≈0.692) and longest chains differ (**6 versus 11**). A single fitted causal-density statistic therefore cannot prove manifoldlikeness or dimension.

As an additional, bounded comparison, calculate the 4D BDG combinatorial bracket `n-N0+9N1-16N2+8N3` in the sprinkling and matched null. Do not infer continuum curvature or an action value without normalization, nonlocality scale, physical cutoff and boundary control.

Producer: `analysis/2026_11_03_causal_set_dimension_nulls.py`.

### 5b. Supplied 4D torus: continuum and helicity benchmarks, not emergence

For a periodic d-dimensional product lattice, calculate the exact factorized graph heat trace; a large **supplied** 4D torus reaches numerical spectral dimension ≈**4.0435** in the tested intermediate diffusion window. Its D=2/3 controls approach their respective dimensions instead. A **supplied** 3D spatial central-difference wave operator has dispersion `ω²=(2c/a)² sum_i sin²(k_i a/2)`, and the axis-vs-oblique anisotropy diminishes under refinement (≈0.000535 at largest L). For symmetric `h_ij` at nonzero k, externally apply `P_ij=δ_ij-k_i k_j/|k|²`, `TT(h)=P h P-P tr(P h P)/2`. The projector has rank **2 of 6**, annihilates trace and pure gradient gauges. It is **not** an automatic spin-two graph excitation or nonlinear Einstein dynamics.

A simple fixed-N hypercubic graph-growth cost proportional only to edge count E=DN is linear in D and selects a boundary of allowed dimensions rather than uniquely `D=3` spatial/`D=4` spacetime. More interactions are needed.

Producer: `analysis/2026_11_03_alternative_torus_spin2_controls.py`.

### 5c. Coherent temporal order without interpreting it as retrocausality

Implement the ideal two-unitary quantum switch

```text
|Ψ>= (|0>VU|ψ> + |1>UV|ψ>)/sqrt(2),
p(control=-) = ||(VU-UV)|ψ>||²/4.
```

With Pauli X and Z, `p_-=1`; with X and identity, `p_-=0`. For arbitrary X/Z rotations, the 20-point angle sweep matches exactly `sin²(θ/2)sin²(φ/2)`. Dephasing of the control interpolates continuously toward a classical mixture (minus probability 1/2). A realizable quantum switch **does not by itself violate standard causal inequalities** or prove retrocausality; this is a process-order counterexample to equating information exchange time with a unique causal history.

Producer: `analysis/2026_11_03_quantum_switch_order_witness.py`.

### 5d. Coordinate-free local face refinement selects the *wrong* geometry

A deterministic Apollonian local rule inserts a vertex in every triangle, joining it to all three corners. This uses graph incidence, not a preassigned metric. After n synchronous refinements,

```text
F_n=3^n,  V_n=(3^n+5)/2,  E_n=3V_n-6,  χ_disk=V-E+F=1.
```

All tested levels 1..7 remain **planar topological disks**, reaching 1,096 sites; highest vertex degree grows `3,6,12,24,48,96,192`, not bounded-degree local manifold structure. Exact finite graph diameters remain small (1,2,3,3,4,5 for n<=6). The rule creates complexity and shortcuts but **not** an emergent 3+1D Lorentzian spacetime. It is a fully specified dynamic graph-growth falsifier rather than a statement that all alternative growth rules fail.

Producer: `analysis/2026_11_03_apollonian_growth_dimension_null.py`.

## Independent verification

All 8 producers generate distinct machine-readable certificates in `data/`; each has explicit assertions beyond mere successful execution. The focused pytest module replays all eight producers on the connected Windows machine and verifies key outputs. The entire repository suite is **not** rerun in this packet.

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -m pytest -q -s -o addopts='' tests/test_20261103_alternative_geometry_five_fronts.py
```

## Scientific decision

Two strong positive *mathematical* results: the known global E8 inversion's induced 8+16 fiber orbit structure, and the exact full/Dirichlet characteristic determinant recursion for a declared Pascal graph. One concrete dimensionless *interaction* model produces exponentially small relative masses, but no absolute scale. The most important negative result from the independent fifth front is that **density matching, quantum-order interference, spectral dimensionality, and graph growth can each be made to resemble aspects of spacetime without generating a universal gravitational theory**.

A physically credible TOE now needs a specified selection action with testable predictions that simultaneously survive:
1. manifoldlikeness and scale-stable *unfitted* d=4 causal statistics;
2. bounded local propagators and Lorentzian light cones with a continuum limit;
3. two TT helicities from first-class dynamical constraints and universal soft-graviton matter coupling;
4. controlled vacuum/cosmological dynamics and an independently generated physical reference scale; and
5. comparison against tuned non-geometric causal graphs and other causal-process nulls.

No current result meets all five demands. The next strongest move is a **blind model competition**, with action/couplings frozen before evaluating these jointly, instead of continuing a search for matching integers.

## Independent scholarly anchors

- Adamson & Wallden, *Benincasa–Dowker–Glaser causal set actions by quantum counting*, Phys. Rev. Research **8**, 023188 (2026), https://doi.org/10.1103/qdst-yrh6 .
- Steffinlongo & Dourdent, *Simulating noncausality with quantum control of causal orders*, Phys. Rev. Research **8**, 013127 (2026), https://doi.org/10.1103/9jss-yf1c .
- de la Hamette et al., *Indefinite Causal Order and Quantum Coordinates*, Phys. Rev. Lett. **135**, 141402 (2025), https://doi.org/10.1103/bnkn-4p3f .
- Weinberg, *Photons and Gravitons in S-Matrix Theory: Derivation of Charge Conservation and Equality of Gravitational and Inertial Mass*, Phys. Rev. **135**, B1049 (1964), https://doi.org/10.1103/PhysRev.135.B1049 .
- *Analogue gravity*, Living Reviews in Relativity (2026), https://link.springer.com/article/10.1007/s41114-026-00064-9 . Specific Weinberg-Witten hypotheses matter.
- *Process Tensor Approaches to Non-Markovian Quantum Dynamics*, Phys. Rev. X **16**, 020502 (2026), https://doi.org/10.1103/1ncg-11hz .
