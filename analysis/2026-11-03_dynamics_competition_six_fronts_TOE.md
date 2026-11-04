# 2026-11-03 — Six executable dynamical-TOE falsifiers: causal growth, quantum memory, dimensional selection, local spin-2, scale and universality

**Scope:** Five fronts requested, plus an independent soft-graviton universality check. These are *scientific filters and finite model demonstrations*, not an established theory of everything, an emergent 3+1-dimensional spacetime, or a derivation of the observed constants. Nothing below modifies old model fits, physics conclusions, or parallel uncommitted code.

## Intake and previous owners

Initial W33 repository and Windows local checkout `master`: `872465b390e613b2d81f46b267078b3856ce94ee`. Existing 57 dirty worktree entries are owned by other work and must remain untouched. Repository searches and code inspection confirmed:

- `analysis/2026_11_03_causal_set_dimension_nulls.py`: static 2D–5D Minkowski sprinklings and density-matched transitive-percolation null. The **new test adds explicit sequential-growth transition normalization, a separate train/holdout split, and finite-action ensemble tilt**.
- `analysis/PASS11042_INSTRUMENT_DEPENDENT_PROCESS_MEMORY.md`: prior one-slot qutrit process comb with instrument-dependent memory. The new test contains a **two-intervention qubit Choi process** with a causal break, not the same example.
- `analysis/2026_11_03_apollonian_growth_dimension_null.py`: prior coordinate-free 2D face-refinement negative control. The new work uses a **dimension-state action and reversible Metropolis sampler**, explicitly revealing action parameter-selection bands.
- `analysis/w33_pass11968_native_spin2_constraint_completion.py`: prior native discrete derivative failure repaired using a **nonlocal** first-class projection. `analysis/2026_11_03_alternative_torus_spin2_controls.py` had an imposed two-polarization TT projector. The new example constructs the **unprojected local quadratic linearized spin-two Hamiltonian and verifies constraint evolution**, while identifying exactly what fails for a noncommuting local derivative.
- `analysis/2026_11_03_marginal_gap_scale_comparison.py` and related prior UV papers: existing 1D interacting gap benchmark and gauge/RG research. New result tests **inverse parameter non-identifiability at fixed two masses and compensated RG invariance**.
- Weinberg's soft-graviton universality is established physics, not a novel project theorem. The new extra packet supplies an exact two-species rank-one Ward-identity witness.

## Front A — General-covariant classical sequential growth (CSG) and held-out manifoldlikeness

**Physical literature first:** Rideout and Sorkin, *Classical sequential growth dynamics for causal sets*, Phys. Rev. D **61**, 024002 (1999), https://doi.org/10.1103/PhysRevD.61.024002 ; Surya, *The causal set approach to quantum gravity*, Living Reviews **22** (2019), https://doi.org/10.1007/s41114-019-0023-1 .

The classical CSG special family `t_k=t^k`, with `p=t/(1+t)`, has elementary probability for a specified precursor/downset P of size ω with m maximal elements:

```text
P(P | C_n)=λ(ω,m)/λ(n,0)
          =p^m (1-p)^(n−ω)
λ(ω,m)=t^m(1+t)^(ω-m), λ(n,0)=(1+t)^n.
```

The code enumerates every allowed downset of the four-point chain, antichain and disjoint 2+2 order for four different p values, checking probabilities sum to one. It then runs the equivalent growth simulation: each new element independently selects earlier parents at fixed p and takes the transitive closure.

**Frozen blind comparison:** use `N=72`, 18 seeded target 4D Minkowski-diamond sprinklings to select p **only by comparable-pair fraction** from a 15-value grid; withhold 22 independent target sprinklings and generate 128 independent selected-p growth histories. Target training comparable density ≈**0.10176**, selected `p=0.04`; held-out 4D density ≈**0.09884** versus growth ≈**0.10551**. Despite similar order density, held-out mean maximum-chain lengths are **4.41** (4D sprinkled) versus **6.93** (sequential growth), so density-matching does not yield the same causal interval geometry.

A further diagnostic reweights the fixed CSG candidate pool using a finite-4D-BDG-like interval bracket `N−N0+9N1−16N2+8N3` at declared beta values. This action **presupposes dimension 4 in its coefficients**, its finite bounded histories have boundary effects, and reweighting an existing finite pool is not equivalent to generating dynamics with a quantum gravitational path integral. Effective sample size is reported for each tilt. **Do not claim the tilt dynamically selects 4D.**

**Producer:** `analysis/2026_11_03_csg_action_heldout.py`; **certificate:** `data/2026_11_03_csg_action_heldout.json`.

## Front B — Two-intervention quantum process tensors versus causal order

**Literature:** Taranto et al., *Non-Markovian Quantum Process Tomography*, PRX Quantum **3**, 020344 (2022), https://doi.org/10.1103/PRXQuantum.3.020344 ; Pollock et al. and process-tensor theory, https://doi.org/10.1103/PRXQUANTUM.2.030201 .

Build an explicit unnormalized five-qubit process Choi operator on

```text
(A_in, A_out, B_in, B_out, F), total Hilbert dimension 32.
```

The initial system A_in is maximally mixed. Compare two implementations: (i) a fresh environment with identity S–E steps (Markov process); (ii) initial Bell-pair system–environment with SWAP at both steps (memory bypass). Each process is constructed from Stinespring circuits with two unnormalized maximally entangled Choi links and final environment partial trace. Both are positive semidefinite (minimal numerical eigenvalue only ≈−3×10^-16 from floating-point roundoff), have trace exactly four, and satisfy

```text
Tr_F(T) = I_(B_out) tensor T_previous
Tr_(B_in)(T_previous) = rho_(A_in) tensor I_(A_out), rho=I/2.
```

The temporal causal-break intervention discards the slot-B incoming system and reprepares `|b>`; the first intervention previously reprepared `|a>`. Under identity, the output F is `b` regardless of `a`. Under environmental memory, the output F is `a` regardless of `b`. This is an explicit **operational memory witness** with *identical causal ordering and positive, normalized process tensors*. It is neither a superposition of spacetimes nor backwards signaling.

**Producer:** `analysis/2026_11_03_two_slot_quantum_memory_choi.py`; **certificate:** `data/2026_11_03_two_slot_quantum_memory_choi.json`.

## Front C — A dimension-selecting local-incidence action and the coupling-selection problem

Use only elementary incidence densities on candidate periodic hypercubic cell complexes with geometric D given as a **candidate label**. Each vertex has exactly `E/V=D` edges and `F_square/V=binom(D,2)` plaquettes. Consider

```text
epsilon_D = aD+b D(D−1)/2, b>0.
epsilon_(D+1)−epsilon_D=a+bD.
```

For D in `1..6`, the unique ground state is D=3 iff `−3b<a<−2b` and D=4 iff `−4b<a<−3b`. The Metropolis birth-death sampler proposes `D→D±1` with symmetric proposal and accepts according to `exp[-(ε_new−ε_old)/T]`. In six preset parameter cases, its 80,000 sampled dimension-state histories match the exact Boltzmann occupation probabilities within max absolute error 0.004.

The **negative conclusion** matters: the same local incidence rule selects dimensions **three, four, both at a boundary, or one** depending on freely chosen `a/b`. The process also uses global dimension steps, *not* local simplicial Pachner moves. Thus neither four dimensions nor a Lorentzian causal arrow is explained: this is a small model competition demonstrating how easy it is to *fit* a desired D.

**Producer:** `analysis/2026_11_03_incidence_dimension_phase_competition.py`; **certificate:** `data/2026_11_03_incidence_dimension_phase_competition.json`.

## Front D — Strictly local linearized spin-two Hamiltonian constraint closure and the inhomogeneity obstruction

On a **supplied** periodic three-dimensional 3×3×3 lattice, define real antisymmetric central differences

```text
D_i f(x)=[f(x+e_i)−f(x−e_i)]/2.
```

For commuting D_i, use canonical symmetric spatial h_ij and p_ij (off-diagonal p=2pi_ij), with linear constraints

```text
H0(q)=Σ_i D_i² tr(h)−Σ_i,j D_iD_j h_ij,
M_i(p)=Σ_j D_j pi_ij.
```

Use the explicit local DeWitt quadratic kinetic matrix `G` and standard linearized spatial Fierz–Pauli potential Hessian `K`. In the checked discrete formalism,

```text
{H0,M_i}=0, equivalently H0 M^T=0
H0 G=−2 Σ_i D_i M_i
M K=0.
```

Therefore the canonical linear Hamiltonian evolution `qdot=Gp`, `pdot=−Kq` preserves both scalar and momentum constraints *without nonlocal projectors*: H0dot is a local divergence of M, Mdot=0. All three maximum residuals vanish to numerical machine precision.

The 6 symmetric tensor components, constrained by one scalar and three momenta at each **nonzero** Fourier k, yield **two physical configurations**. The explicitly checked momentum representatives are `(1,0,0)`, `(1,1,0)`, `(1,1,1)`, with discrete physical squared dispersion `ω²=Σ sin² k_i`. At k=0 the six homogeneous modes remain; these are not claimed as propagating graviton helicities.

**Stress test:** replace `D_y` by `W D_y W` with x-dependent local positive weights W, preserving skew-adjointness and finite neighborhood locality. Then `[D_x,D_y']≠0`, and the naive constraints fail:

```text
max norm [D_x,D_y'] ≈ 0.32218
max |H0 M^T|        ≈ 0.05991
max |M K|           ≈ 0.03898
```

This identifies an exact *algebraic obligation* for emergent gravity: a candidate curvature/connection-dependent derivative must produce modified constraints whose brackets close. Using flat-space constraints unchanged on inhomogeneous discrete derivatives does not work.

**This is a standard linearized-gravity positive control, not emergence from W33 and not nonlinear GR.** The cubic spatial lattice, clocks and constraint/Hamiltonian formulas are inputs. The full hypersurface-deformation algebra, Lorentzian metric selection, universal matter stress-energy coupling, renormalized graviton, and physical G remain absent.

**Producer:** `analysis/2026_11_03_local_spin2_hamiltonian_closure.py`; **certificate:** `data/2026_11_03_local_spin2_hamiltonian_closure.json`.

## Front E — Interacting scale generation does not identify an absolute meter

For an *assumed* 1+1D large-N four-fermion/Gross–Neveu-style sharp-cutoff gap equation, the toy physical mass ratio is

```text
m/Lambda = 1 / sqrt(exp(2π/g_bare²)−1).
```

For any reference cutoff Lambda larger than the measured mass m, invert:

```text
g_bare² = 2π / ln[1+(Lambda/m)²].
```

Use deliberately **unitless** example mass targets `0.001,1`, and five arbitrarily chosen cutoffs `2,10,100,1000,1000000`. Every cutoff has a distinct pair of fitted dimensionless couplings which reproduces the *same* two masses. The inverse calculation proves the absolute cutoff is not identifiable from these two masses plus two free couplings. Requiring a single shared positive g for both species forces equal masses and cannot generate the chosen two-mass hierarchy.

For the continuum one-loop schematic `m=μ exp[-π/g_R²(μ)]`, the compensating running `d(g_R²)/d ln μ=−(g_R²)²/π` preserves m numerically to ~10^-12 relative across six μ values. This *explains* how dynamical transmutation produces a **relative mass scale** while retaining the need for an independently specified reference. It is not a derivation of the electron, proton, gravitational or cosmological hierarchy from W33.

**Producer:** `analysis/2026_11_03_transmutation_identifiability_firewall.py`; **certificate:** `data/2026_11_03_transmutation_identifiability_firewall.json`.

## Bonus — the exact two-species soft-graviton Ward universality requirement

Take a nonforward two-to-two massless scattering with two independent external particle species A and B, with incoming signed momenta `−p1,−p2` and outgoing `p3,p4`. In the representative rational momentum frame

```text
p1=(1,0,0,1); p2=(1,0,0,−1);
p3=(1,1,0,0); p4=(1,−1,0,0).
```

Momentum conservation holds. A soft-spin-two polarization gauge shift produces

```text
delta S = 2 Σ_i η_i κ_i (p_i·xi)
        = 2(κ_A−κ_B)(p3−p1)·xi.
```

The 4×2 species momentum matrix `[p3−p1,p4−p2]` has **rank one** and exact coupling nullspace **span{(1,1)}**. Hence gauge-invariant soft-graviton coupling for nontrivial two-species scattering is **universal**, a testable necessity for any proposal claiming a long-range massless spin-2 force. With the chosen null soft momentum `q=(5,3,4,0)` and rational gauge vector `xi=(1/3,2/5,-1/7,3/11)`, the symbolic variation is `(14/55)(κ_B−κ_A)`; zero exactly when couplings agree.

This rechecks the established Weinberg consistency theorem (https://doi.org/10.1103/PhysRev.135.B1049) in a small exact symbolic witness. It does not construct the graviton or prove universality for every possible scattering process.

**Producer:** `analysis/2026_11_03_spin2_soft_ward_universality.py`; **certificate:** `data/2026_11_03_spin2_soft_ward_universality.json`.

## Research verdict: the bottleneck is the intersection, not each model alone

The tests show six structural necessities that can each be achieved or imitated in a supplied model: covariant stochastic growth, completely positive temporal memory, tunable dimension selection, linear local first-class spin-2 dynamics, exponentially small generated mass ratios, and universal soft-graviton consistency. **No single internally derived model yet achieves all six**, and neither the project repo nor the literature supports asserting the TOE is solved.

A genuinely competitive next proposal needs a **frozen action**, a reproducible finite-size family, a selected causal/metric phase, a local continuum limit with curvature and massless spin two, and couplings fixed independently of fitting each target observable. The most stringent blinded evaluation will compare against nonmanifoldlike CSG histories and competing dimension-state actions and hold back causal, gravitational, and spectral observables as out-of-sample tests.

## Reproduction

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -m pytest -q -s -o addopts='' tests/test_20261103_five_dynamical_toe_fronts.py --maxfail=1
```

Each producer may also be run directly through `python analysis/<script>.py`. Outputs are pure JSON certificates in `data/`. These tests are focused, not the entire W33 repository suite.

## Independent scholarly references

- Rideout & Sorkin, *Classical sequential growth dynamics for causal sets*, PRD **61**, 024002: https://doi.org/10.1103/PhysRevD.61.024002 .
- Surya, *The causal set approach to quantum gravity*, Living Reviews in Relativity **22** (2019): https://doi.org/10.1007/s41114-019-0023-1 .
- *Non-Markovian Quantum Process Tomography*, PRX Quantum **3**, 020344 (2022): https://doi.org/10.1103/PRXQuantum.3.020344 .
- *Quantum Stochastic Processes and Quantum Non-Markovian Phenomena*, PRX Quantum **2**, 030201 (2021): https://doi.org/10.1103/PRXQUANTUM.2.030201 .
- Clemente et al., *Yang-Mills topology on four-dimensional triangulations*, PRD **113**, 034511 (2026): https://doi.org/10.1103/ljx7-qpqp .
- Weinberg, *Photons and Gravitons in S-Matrix Theory*, Phys. Rev. **135**, B1049 (1964): https://doi.org/10.1103/PhysRev.135.B1049 .
- Hertzberg & Sandora, *Special relativity from soft gravitons*, PRD **96**, 084048 (2017): https://doi.org/10.1103/PhysRevD.96.084048 .
- Gross & Neveu, *Dynamical symmetry breaking in asymptotically free field theories*, PRD **10**, 3235 (1974): https://doi.org/10.1103/PhysRevD.10.3235 .
