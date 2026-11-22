# TOE continuation — five constructive fronts, two extra exact Witting/Hessian theorems

**Research date:** 2026-11-22. **Basis:** live `wilcompute/W33-Theory` master, preceding Witting/H27/cubic and causal certificates, eight independent Python producers and an offline regression bundle. The results below are **finite mathematical constructions, engineering benchmarks and scoped negative controls**, not a derived TOE, observed matter spectrum, real spacetime theory or operating photonic prototype.

## Reproducibility and ownership

From the repository root, with Python 3.12+, numpy, sympy, scipy and pytest:

```sh
python -m pytest -q tests/test_toe_20261122_next5_constructive_fronts.py
for f in analysis/toe_20261122_next5_*.py; do python "$f"; done
```

New proofs/tests use canonical zero-based Witting rays and W33 projective symplectic coordinates. Exact results are verified by integer arithmetic, permutation groups and reduction at primes 7,13,19,31,37,43; optical benchmarks use seeded floating-point simulations. Each producer writes the matching `data/toe_20261122_next5_*.json`. An isolated GitHub Actions workflow is included.

**Existing repository prior art:** `toe_20261122_discrete_witting_dense_su4.py` proves four-fixed-gate SU4 density; `toe_20261122_witting_one_phase_three_fixed.py` establishes the Hessian order 648 and the 27+12+1 ray orbit split; `w33_address_operator_h27_intertwiner_obstruction.py` proved the rank-nine incompatibility between regular address and scalar-center E6 operator H27; `toe_20261118_H27_Fourier_minimal7_E6_tensor_embedding.py` had noncommutative Fourier and ancilla constructions; `toe_20261122_causal_orientation_no_go.py` counted 1620 chordless W33 C4s. The present pass **does not relabel any of those as discoveries**. It supplies the exact site-selection classification, the binary-tetrahedral centralizer/double coset, a new sparse explicit operator map, a finite causal dynamics toy model, a gauge-invariant SUSY toy flat branch, and hardware falsifiers.

## 1. Discrete optical compiler: exact Hessen/H27 coset reduction

Let 
`H=<R5(omega),R26(omega),R33(omega)>`, `|H|=648`; let `D=I-2P36`, `D^2=I`. The H action on the 40 canonical Witting rays has orbits of sizes **27,12,1**, with ray **25** fixed and ray **36** in the regular 27 orbit. Its ray-36 stabilizer `I=Stab_H(36)` has order **24**, element order profile

```
{1:1, 2:1, 3:8, 4:6, 6:8},
Z(I)=C2, [I,I]=Q8 (order 8), I/[I,I]=C3.
```

It is the binary tetrahedral `SL(2,3)=Q8 ⋊ C3` (the isomorphism identification is standard math). The normal H27 subgroup `N` of order27 intersects `I` trivially and generates H with it: `H=N ⋊ I`. Since a unitary stabilizing ray36 commutes with its rank-one projector, **D centralizes I**. Six exact prime-field matrix computations independently verify `H∩DHD=I` and that every member of I commutes with D. Thus

\[
\boxed{HDH=HDN,\quad |HDH|=648\cdot27=17,496,\quad \frac{648^2}{|HDH|}=24.}
\]

A single-D-stage compiler need evaluate **17,496** distinct representatives, rather than **419,904** redundant products. The group is finite at this stage; this does not conflict with the whole four-generator group being dense. The 648-member H has a word-diameter **9** in the six-letter mirror/inverse alphabet under BFS. Full `HDN` exhaustive optimization on three seeded Haar U4 targets gives projective Frobenius distances **0.6573, 0.6439, 0.7161**, improved from the depth-five brute-force errors **0.7468, 0.8801, 0.7976**. These are still far from usable approximate synthesis. A 648² independent brute-control matched the reduced optimum for the first target. No claim of near-optimal arbitrary-depth compilation or physical loss advantage is made.

The depth-five initial search actually contains **1,675** projectively distinct words—not the initially reported 2,063. The discrepancy came from choosing a floating-point maximum-magnitude pivot among tied matrix entries, producing unstable phase representatives. The revised pivot chooses the first entry with amplitude above a stable threshold, and the full H-subgroup is indexed by **exact ray permutations**; finite-field arithmetic then secures the structural counts.

Sources: `analysis/toe_20261122_next5_compiler_photonics.py`, `analysis/toe_20261122_next5_hessian_coset_compiler.py`. Established context for mesh comparison: [Clements et al., Optica (2016)](https://doi.org/10.1364/OPTICA.3.001460); [GroupNames: SL2(F3) = binary tetrahedral](https://people.maths.bris.ac.uk/~matyd/GroupNames/T31.html).

## 2. New complete 40-site pi-gate classification

The three fixed order-three mirrors span a 3D complex subspace `S` and **fix its orthogonal line `L`, Witting ray25**, pointwise. This is verified exactly in Q(omega). Among the 40 rays:

- **27** rays have nonzero components in both S and L. They form a single H orbit containing 36; all corresponding rank-one pi gates are H-conjugate to D36, hence generate exactly the **same dense SU4-containing closed group** with H.
- **12** rays are inside S. Their pi gates preserve `S ⊕ L`, preventing dense SU4 regardless of compilation depth.
- **1** ray equals L: 25. D25 commutes with H and has determinant -1 while every H determinant is a third root of unity. Hence `<H,D25> ≅ H × C2` is finite of **order 1296**.

This gives a **necessary-and-sufficient site-selection rule for this specific three-mirror plus one-pi architecture**, not for arbitrary gate designs. **27 valid / 13 invalid** is a group-action theorem, not a numerological fit.

Producer: `analysis/toe_20261122_next5_phase_site_classification.py`.

## 3. E6/H27: exact sparse Witting address-to-operator partial intertwiner

The regular permutation module `C[H27]`, dimension27, has center eigenspace multiplicities **9+9+9**. The E6 trinification H27 *operator model* has nine copies of one 3D Schroedinger irrep with scalar center. The old repo rank-nine obstruction forbids an invertible 27→27 H27-linear map. Three regular address modules contain nine copies of the desired 3D irrep after selecting their omega-center sector, so an **81→27 surjective intertwiner** exists abstractly (minimum three regular copies only in the *uniform regular-copy source class*; not a universal minimal ancilla claim).

This pass constructs its **actual sparse entries** in canonical Witting ray order:

\[
T = \operatorname{diag}(T_9,T_9,T_9)\in \operatorname{Mat}_{27\times81}(\mathbb Z[\omega,1/3]),
\qquad
(T_9)_{a,j}\in\{0,1/3,\omega/3,\omega^2/3\}.
\]

Each `T9` has exactly **81 nonzeros**; full T has **243 nonzeros**, nine per row. The code stores the **9×27 table of exponents**, with -1 for zero, and an explicit derivation from the center Fourier projection and order-three orbit sums. It checks all coisometry and H27 generator identities using exact integer pairs `(a,b)` for `a+b*omega` and separately at six split primes:

\[
TT^\dagger=I_{27},\quad T\rho_{81}(x)=\bigl(I_9\otimes Z_3\bigr)T,\quad T\rho_{81}(y^{-1})=\bigl(I_9\otimes X_3\bigr)T,\quad T\rho_{81}(z)=\omega T.
\]

A second independent construction via normalized eigenvectors and Gram–Schmidt gives Frobenius residual below **4×10^-15**. That second map is numerical and is explicitly distinguished from the exact algebraic coefficient table. In both cases the **81 address coordinates are formal regular-representation labels**, not 81 orthogonal physical photon modes. Neither establishes E6 cubic-tensor preservation, an E6-root basis map, or a realistic photon-to-matter interaction.

Producers: `analysis/toe_20261122_next5_h27_exact_matrix.py`, `analysis/toe_20261122_next5_h27_explicit_intertwiner.py`.

## 4. Dynamical causality: finite W33 interval-action Metropolis model

Instead of assuming graph adjacency itself determines time, choose a total order `pi` of all 40 W33 points. Orient every W33 edge from earlier to later; the result is a DAG. Its **transitive closure** defines a causal poset. The code counts intervals containing exactly 0,1,2 interior events, named `N0,N1,N2`, together with ordering fraction and longest chain. Define an **illustrative dimensionless** action

\[
S(\pi)=0.06N_0-0.09N_1+0.045N_2.
\]

Use random adjacent-order swaps, accepted with `min(1, exp(-Delta S))`. This defines a finite, reversible, irreducible (on total orders) Markov chain. The code exactly enumerates **all 24 four-cycle total orders** and checks detailed balance for each adjacent-transposition transition. W33 symplectic transvections on 40 projective points generate a group of **order 25,920**; all 40 transformations preserve the edge relation and every action observable after relabeling. A 1,800-proposal seeded 40-point run accepts about **97.11%**, an indication of weak action discrimination at these illustrative coefficients, *not evidence of thermal equilibration*.

For different 40-point orders, the same undirected W33 graph produced ordering fractions **0.6846** and **0.9013**, with longest chains **10** and **20**. Thus the time structure is being supplied by additional orientation variables, not deduced from adjacency. No Lorentzian continuum, spin-two dispersion, Einstein–Hilbert coefficient, quantum state, or causal-set gravity prediction has been established. The present action is **not** the physical Benincasa–Dowker–Glaser action; it simply uses small-interval counts as candidate observables.

Producer: `analysis/toe_20261122_next5_causal_dynamics.py`. Physical context: [Benincasa–Dowker–Glaser causal set actions by quantum counting, Phys. Rev. Research (2026)](https://doi.org/10.1103/qdst-yrh6).

## 5. An explicit renormalizable E6×H27 supersymmetric flat **toy** branch

Take **three chiral matter 27_M**s transforming as one H27 Schroedinger family triplet, three vectorlike **27_H+27bar_H Higgs pairs** in triplet and contragredient-triplet family representations, and one neutral driving superfield X. Use the renormalizable, E6×H27-invariant superpotential

\[
W=X\bigl(\sum_i \langle\Phi_{H,i},\bar\Phi_{H,i}\rangle-\mu^2\bigr)
+y\sum_{ijk}h_{ijk}\,C_{E6}(\Psi_{M,i},\Psi_{M,j},\Phi_{H,k}).
\]

Here `C_E6` is the established symmetric invariant E6 cubic; `h_iii=a` and `h_ijk=b` for all-distinct family indices, otherwise zero. This symmetric family cubic is H27-invariant under its cyclic shift and clock because all surviving index triples have `i+j+k=0 mod3`.

At zero matter, X=0, and VEVs **only** in E6 singlet components

\[
\langle\Phi_{H}\rangle=(1,2,4),\quad
\langle\bar\Phi_{H}\rangle=(1,2,4),\quad\mu^2=21,
\]

every F term vanishes (including the matter-field F terms). The vectorlike Higgs VEVs are conjugate pairs, so **every E6 gauge D term cancels pairwise**, not just the surviving U1 Cartan D. The VEV breaks family H27 spontaneously. With **chosen** `a=2`, `b=1`, its SO10-singlet/10×10 matter cubic gives

\[
M_{10_M}=\begin{pmatrix}2&4&2\\4&4&1\\2&1&8\end{pmatrix},\qquad
\det M=-66,
\]

with nondegenerate positive singular values approximately **1.2288, 5.5489, 9.6799** in arbitrary units. All **three vectorlike 10_M**s can therefore be lifted at this specific algebraic point while the three chiral matter **16_M** multiplets remain. The additional 27_H+27bar_H Higgs matter is vectorlike and its mass spectrum remains unspecified.

**Crucial hostile boundary:** This is a flat *branch*, not an isolated vacuum: its singlet-only sector has **four complex flat moduli** after one holomorphic X constraint and one complexified U1 gauge orbit. The input values `3 families`, `a,b`, `mu`, and `(1,2,4)` were chosen; not a prediction. The full additional Higgs spectrum, mass thresholds, loop corrections, vacua, discrete flavor anomalies, proton decay and complete 4D anomaly/inflow constraints are not solved. Nothing here derives observed Yukawa hierarchies or an honest three-family compactification. This is a constructive counterexample only to the **unbroken H27 scalar-mass** restriction, by *spontaneously breaking* H27 in a gauge-compatible model.

Producer: `analysis/toe_20261122_next5_e6_susy_flat_branch.py`. Background: [a complete E6 GUT trinification model](https://inspirehep.net/files/4bd2ad587c4c9313ea9faa3f62dead1a); [E6 GUT mathematical construction](https://arxiv.org/abs/2102.13465).

## 6. Photonic hardware falsifiers and statistical test design

**Intensity-only channel identification is impossible without phase reference.** For the Witting fixed gate `U=R5(omega)`, choose `V=diag(e^{i pi/3},1,1,1) U`. Every basis input and output intensity `|U_ij|²` equals `|V_ij|²` *exactly*, but the two ideal unitary channels differ, with average gate fidelity **0.85**. A coherent input `U†(|0>+|1>)/sqrt2` followed by an X-basis output measurement distinguishes them: the `+` probability is **1** for U and **0.75** for V. Under *perfectly calibrated ideal* preparation/readout, **11 independent shots** yield at least 95% power to catch a pi/3 shift with zero ideal-model false alarm; for a **0.1 rad** shift this one-sided rule needs **1198 shots**. Real SPAM, loss, time drift and unknown phase eliminate these ideal guarantees; the repo's parallel detector-PovM work addresses different realistic issues.

**Passive two-photon no-go:** Encode two dual-rail qubits using two photons, one in rails (0,1) and one in rails (2,3). A passive 4×4 unitary U induces a deterministic leakage-free two-qubit transformation iff its physical mode matrix is block diagonal or block antidiagonal, yielding only local gates or a local gate plus swap. The proof uses the symmetric boson two-particle norm identity

\[
\|u\vee v\|^2=\|u\|^2\|v\|^2+|\langle u,v\rangle|^2,
\]

which vanishes iff at least one vector is zero. Zero two-photon AA and BB leakage for all four dual-rail computational input pairs forces the 2×2 mode blocks to be diagonal/antidiagonal under unitarity. This is a **known passive-linear-optics limitation**, checked explicitly for this optical alphabet; not a novel broad no-go. For Witting R5, the two-photon leakage probabilities on the four computational inputs are **7/9,7/9,1/3,1/3**. Thus the new dense one-photon SU4 gate set is not by itself a deterministic two-qubit entangler. Ancillas, conditional measurements, optical nonlinearities and other encodings escape the assumptions.

**Resource comparison:** The bounded compiler models phase jitter with 400 seeded draws per sigma and separates normalized conditional gate fidelity from uniform intensity loss. In a hypothetical per-two-mode-coupler transmission 0.98 and detector efficiency .85, a five-gate 20-coupler word has survival ~**0.5675**, whereas a six-coupler mesh has ~**0.7530**; this is a conditional apples-to-apples coupler-count comparison, not a measured physical advantage or exact mesh compilation of the target. The hardware program needs coherent process tomography, real chip losses, phase stability and switching latency.

Producers: `analysis/toe_20261122_next5_photonic_calibration_entangler.py`, `analysis/toe_20261122_next5_compiler_photonics.py`. Literature: [passive linear-optics no-go and dual-rail references (2013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3589727/); [nonlinear deterministic dual-rail proposals (2024)](https://www.nature.com/articles/s42005-024-01610-z).

## What is achieved vs. what is not

**Achieved:** two exact novel-to-this-repo Hessian/Witting geometric-control theorems, a complete 40-ray site selection, a full 24× search-space compression, an exact sparse Witting H27 matrix, a globally consistent finite reversible causal-order dynamics model, a renormalizable E6×H27 *toy* F/D-flat branch, and physical calibration/entanglement falsifiers. Source-specific tests verify the claims above; all scripts and frozen outputs are committed to master.

**Not achieved:** a physically efficient arbitrary-U4 compiler, any E6 cubic-preserving Witting photonic carrier map, full E6 phenomenological vacuum, a Lorentzian Einstein continuum and observed gravitational couplings, exact low-energy particle data, actual laboratory calibration, or a loss-tolerant multi-photon fault-tolerant computer. Strong gate algebra does not logically imply any of these.

## Five independent next falsification projects

1. **Multi-D Hessian compilation:** construct the exact `HDN D N ...` normal-form automaton, with provable metric-approximation convergence and noise-aware word optimization; test an explicit target ensemble beyond a single D stage.
2. **E6 cubic-preserving interface:** test whether the exact sparse H27 map extends to full E6 invariant tensor and gauge representation, including 27-vector norms and the Jordan cubic; publish a concrete obstruction if not.
3. **Causal quantum dynamics:** replace ad hoc Metropolis weights with a coherent quantum sum over causal orders, and test discrete Bianchi constraints, diffusion/spectral dimension and genuinely Lorentzian spin-two poles.
4. **Stabilized family-breaking vacuum:** lift the four complex E6/H27 flat moduli with permitted interactions, full supersymmetric D/F and anomaly checks, and calculate a robust chiral spectrum under perturbations.
5. **Photonic process-calibration experiment:** perform phase-referenced unitary tomography and two-photon leakage measurement for the proposed four-gate optical layout, compare hardware throughput and entanglement resources to a rectangular mesh.
