# Six executed W33/Witting research fronts: positive quantum capacity, optimal 24D tomography, optical error budgets, local Hamiltonian compilation, and noncollapsing geometry

**Date:** 2026-11-21. **Audited baseline:** commit `47af4e9a2796a9e30c741e8c25d2de5b781f9958`, `master`, `wilcompute/W33-Theory`. Executable `analysis/toe_20261121_capacity_fisher_schmidt_locality.py`; frozen certificate `data/toe_20261121_capacity_fisher_schmidt_locality_sixfront.json`; offline regression `tests/test_toe_20261121_capacity_fisher_schmidt_locality.py`.

## Source-and-precedent audit

Repo read: the baseline 45-chart/27-deck and 4-to-9 Naimark implementations, `analysis/2026-11-21_tight_24D_mesh_coherent_9x5_Hamiltonian_continuum.md`, `analysis/w33_20261109_phase_fisher_information.py` (already studies nine-mode classical Fisher calibration), `analysis/toe_20261104_witting_A5_unitary_lift_and_fisher.py` (already owns A5 Witting POVM FI), `analysis/w33_20261031_floquet_coherent_dressing.py` (already explores local SU3 Floquet dressing), `analysis/w33_20261008_photonic_coherent_fabrication_guard.py` (already owns telescoping optical error guards). Search also found previous `analysis/w33_20261109_q8_schmidt_witness.py`, `analysis/2026-11-19_TOE_five_physics_fronts_singlet_cups_hierarchy_capacity.md`, `analysis/w33_20261102_216_route_holevo_capacity.py`. These are prior art, **not** claimed discoveries of this pass.

Public literature surveyed in this turn (not all full texts read): Clements et al., *An Optimal Design for Universal Multiport Interferometers*, https://arxiv.org/abs/1603.08788 ; Reck et al., *Experimental realization of any discrete unitary operator*, https://doi.org/10.1103/PhysRevLett.73.58 ; *Limitations for adaptive quantum state tomography in the presence of detector noise*, https://journals.aps.org/pra/abstract/10.1103/3q13-xpc8 (2026); *Fast quantum measurement tomography with optimal error bounds*, https://doi.org/10.22331/q-2026-07-15-2162 ; *Detecting positive quantum capacities of quantum channels*, https://www.nature.com/articles/s41534-022-00550-2 ; KLM, *A scheme for efficient quantum computation with linear optics*, https://www.nature.com/articles/35051009 ; *No-go theorem for passive single-rail linear optical quantum computing*, https://www.nature.com/articles/srep01394 ; operator Schmidt rank, https://doi.org/10.1016/j.laa.2018.07.018 ; Cartesian graph products, https://mathworld.wolfram.com/GraphCartesianProduct.html .

The *new* results below are audited numerical constructions/elementary finite-model consequences of existing quantum and graph theory. They **do not** establish experimental quantum advantage, unusual fundamental constants, the Einstein equations, a relativistic spacetime or a TOE.

## Front 1 — An actual strictly positive quantum-capacity lower bound (strongest result)

The previous pass constructed \(\mathbb C^4\to\mathbb C^9\otimes\mathbb C^5\) by Witting rows \(B_{i,*}=\langle r_i|/\sqrt{10}\) for i=1,...,40, padded with five zero rows. \(B^\dagger B=I_4\). Its 40 nonzero computational-basis click projectors realize the same informationally complete Witting POVM \(\{P_i/10\}\). **The output row assignment matters:** the channel that discards the C5 factor changes under an arbitrary permutation of the 45 output rows; the full POVM does not (after classical click relabeling).

For the input \(\rho=I_4/4\), the original row order gave \(S(\mathcal N(\rho))=2.6231625884\) bits, \(S(\mathcal N^c(\rho))=2.1887408625\) bits, hence
\[
I_c(\rho,\mathcal N)=0.43442172587\quad\text{qubits per use}.
\]
A concrete fixed permutation (in the JSON certificate, using 0-based rows)
\[
(0,22,14,19,6,7,2,11,33,38,35,40,23,31,10,
 32,8,43,29,36,27,44,9,15,21,16,12,25,3,37,
 13,41,20,5,34,26,30,17,42,24,18,39,28,1,4)
\]
increases the exact same input's coherent information to
\[
\boxed{I_c(I_4/4,\mathcal N_{\rm routed})=1.08670848982
\text{ qubits per channel use}.}
\]
The code recomputes both channel and complementary-channel output density matrices from explicit 9x5x4 isometry amplitudes, verifies trace normalization and positivity, and **independently crosschecks** \(S(B)-S(E)=S(B)-S(RB)\) against the explicit 36x36 normalized Choi matrix with rank5. A 100-seed random-permutation sample gives a numerical comparison distribution. The supplied optimized permutation is a reproducible constructive witness, **not a proven global optimum**.

By the standard Lloyd–Shor–Devetak coding theorem, \(Q(\mathcal N)\ge \max_\rho I_c(\rho,\mathcal N)\). Therefore, for this ideal **9-output-dimensional** channel, **unassisted asymptotic quantum capacity is provably positive** and in fact at least 1.0867 qubits/use via the explicit input. This is MUCH stronger than last turn's Choi non-entanglement-breaking certificate. No symmetry intertwiner or real-world photonic realization is implied. Retaining the C5 factor would instead give the obvious perfect 4-to-45 isometry.

**Erasure robustness, but different output dimension:** append a heralded orthogonal erasure flag to the output (now C10) and erase the C9 output with probability p, putting the full former output into the environment. For the same \(\rho=I_4/4\), \(I_c(p)=(1-p)I_c(0)-2p\). The explicit routed lower bound stays positive when \(p<I_c(0)/(I_c(0)+2)\approx0.352\). This is a **separate** C4-to-C10 erased channel; it does NOT establish the loss tolerance of the original C4-to-C9 physical photonic hardware.

## Front 2 — A locally **A- and E-optimal** exact 24D photon-statistics theorem

Use the 540 nonorthogonal input ray-pairs a,b and a classical chart selection distribution \(w_z=1/45+x_z\), where \(x\) belongs to the 24-dimensional \(-3\) chart eigenspace. The matched-event probability with unknown chart label has, at the uniform \(x=0\) point, the same value for all 540 probes:
\[
p_0=2/15,\qquad p_0(1-p_0)=26/225.
\]
Let each probe's derivative vector be \(r_{ab}\in\mathbb R^{24}\) in an orthonormal basis of the hidden eigenspace. The previous tight-frame identities imply
\[
\sum_{a<b,\ a\not\perp b}r_{ab}r_{ab}^{\mathsf T}=I_{24}/3,\qquad
\|r_{ab}\|_2^2=2/135\text{ for every probe}.
\]
One Bernoulli trial at any probe therefore contributes fixed Fisher trace \(5/39\), independent of which probe is chosen. For any experimental allocation of \(N\) independent launches, the total local Fisher trace is fixed, \(\operatorname{tr}F_N=5N/39\). The arithmetic–harmonic mean inequality for a positive full-rank 24x24 matrix implies
\[
\boxed{\operatorname{tr}(F_N^{-1})\ge
24^2/(\operatorname{tr}F_N)=4492.8/N.}
\]
Uniform allocation over all 540 probes has \(F_N=(5N/936)I_{24}\) and **attains equality**. It is consequently locally A-optimal (minimum trace inverse) **and E-optimal** (maximum minimum eigenvalue) among ALL classical allocations of the 540 existing probes at the uniform operating point. As a necessary Cramér–Rao condition for locally unbiased estimators, L2 MSE 1e-6 requires at least 4.4928 billion launches; this is NOT a guarantee that any estimator attains the bound.

A noiseless minimal set of 24 independent probes requires just 24 *settings* but yields less information per launch because it is anisotropic. One reproducible 24-probe local-search candidate (indices saved in JSON) gives \(\operatorname{tr}(F_N^{-1})=11681.28/N\), a factor2.60 loss versus the 540-probe tight frame; a platform-dependent pivoted-QR baseline gives another positive value. The 24-probe set is not proven optimal among sparse subsets.

**Interpretation:** under the precise toy model, reweighting or adaptively selecting among these same probes cannot beat uniform allocation locally at x=0 without using a prior or introducing different observables. Stronger proposals should target detector noise, a different measurement interface, collective measurement, or nonlinear constraints, rather than advertising savings from 24 settings alone. Literature on detector readout noise limiting adaptive advantages (PRA, 2026) reinforces this caution.

## Front 3 — Optical control noise evaluated across all 540 selectors

Take all 45 previously certified 8x8 Reck-style adjacent-rail decompositions. Perturb every 2x2 gate G by a coherent overrotation \(D(g)G\), \(D(g)=\operatorname{diag}(e^{ig},e^{-ig})\), with g=1e-4 radians. Reconstruct each **unitary** and evaluate *actual output mode probabilities* for every Witting input ray and all 540 nonorthogonal source pairs. All **540** retain the same maximizing chart in this seeded, systematic-error scenario. The script also checks that the 8x8 reconstruction error is bounded by d*g, where d<=28 is the count of 2x2 optical components.

A separate **worst-case** guarantee follows from telescoping unitary product errors: if every 2x2 programmed gate has operator norm error <=g, the full Naimark network error is <=28g. The two-copy event probability changes by at most 56g in one chart under this norm bound. Since the ideal probability margin between winning and runner-up charts is 1/12, comparison of two corrupted charts stays positive if \(1/12>112g\). Thus an explicit sufficient (but conservative) error budget is
\[
\boxed{g<1/1344\approx0.00074405}
\]
per two-mode gate. This is an *operator-norm* per-gate criterion; g in radians only for our specific phase-overrotation model. It is not a measured integrated-photonics tolerance. The repo's prior `w33_20261008_photonic_coherent_fabrication_guard.py` contains a comparable general telescoping approach and deserves citation rather than claiming it newly invented.

## Front 4 — The 45 chart interactions each need exactly **eight** tensor-product operator terms

Each 16x16 two-ququart Hermitian operator \(Q_z=\sum_{i\in S_z}P_i\otimes P_i\) has **operator Schmidt rank exactly8** when bipartitioned as \(\mathbb C^4\otimes\mathbb C^4\). Every one of the 45 has the same singular values of the operator realignment matrix:
\[
\boxed{\operatorname{singular}(\mathcal R(Q_z))
=(2,2,\underbrace{2/3,\ldots,2/3}_{6},0^{(8)})}.
\]
That is already a **lower bound of eight tensor-product summands** in any decomposition \(\sum_{k=1}^m A_k\otimes B_k\) of Q_z.

We also construct an explicit *matching eight-term decomposition*, not just a lower bound. Each Hermitian chart splits \(\mathbb C^4\) into two orthogonal rank2 subspaces with projectors \(L_z,R_z\). Use their intrinsic encoded qubit Pauli matrices \(X_L,Y_L,Z_L\) and \(X_R,Y_R,Z_R\). The two tetrahedral qubit SIC identities give
\[
\boxed{Q_z=L_z\otimes L_z+R_z\otimes R_z
+\frac13\sum_{\sigma=X,Y,Z}\bigl(
\sigma_{L,z}\otimes\sigma_{L,z}
+\sigma_{R,z}\otimes\sigma_{R,z}\bigr)}.
\]
This contains two block-identity product terms and **six qubit-Pauli correlator products**, and reconstructs every 16x16 Q_z to numerical precision. The source controlled Hamiltonian has 45 branches and remains a nontrivial hardware-control problem; eight operator products is **not** an eight-gate implementation or a gate-depth lower bound.

**Crucial physical boundary:** KLM measurement-induced nonlinearity and the passive single-rail linear-optics no-go results mean that exact two-copy entanglement generation cannot be assumed to follow from passive interferometers alone. This is a symbolic product-operator compilation, not an implemented two-photon entangler.

## Front 5 — A non-collapsing spatial *countermodel* with a 45-state internal Witting fiber

Last pass proved the bare H(3,4) chart graph has diameter2, so shrinking its edge lengths collapses all geometry to a point. Here we explicitly **add local spatial structure**:
\[
\mathcal G_L=\mathrm{GQ45}\ \square\ C_L\ \square\ C_L\ \square\ C_L
\quad(L=4,8,16,32,64),
\]
the Cartesian product of the 45-point chart-collinearity graph and a 3D cycle lattice. This graph has \(45L^3\) nodes, constant degree **18**, and exact diameter \(2+3\lfloor L/2\rfloor\). Scaling each edge length by 1/L, the diameter tends to **3/2**, not zero. The finite GQ fiber collapses internally while the cycles converge to a **spatial 3-torus with L1 (taxicab) metric**; it is NOT a Euclidean-isotropic spatial continuum or Lorentzian spacetime.

The normalized random-walk/Laplacian first nonzero eigenvalue scales as \((2-2\cos(2\pi/L))/18\), i.e. proportional to L^-2. In a separate *directed* time lift with only stay/nearest-neighbor transitions, a signal travels at most one graph edge per clock step, providing a finite spatial propagation cone by construction. These statements were checked for the specified lattice sizes and sampled exact distance formulas. **This does not derive the extra lattice, physical dimensionality, time, relativistic light cones, Einstein equations or dynamics from W33.** Its value is a controlled counterexample to "fixed chart diameter means no possible extended fiber construction."

## Front 6 — A limited but useful joint-calibration symmetry

For the same 540 probes, the centered derivative vectors \(r_{ab}\) sum to exactly zero:
\[
\sum_{a<b,\ a\not\perp b}r_{ab}=0.
\]
Consider a simple observation model with an **unknown global throughput** \(s\in(0,1]\):
\[
p_{ab}=s\bigl(2/15+r_{ab}^{\mathsf T}x\bigr).
\]
At x=0, each pair has the same Bernoulli variance, and the Fisher-information *cross-block* between the unknown global throughput s and all 24 hidden chart-bias coordinates x is exactly **zero**. Hence global throughput and 24D hidden chart-bias scores are locally orthogonal at the uniform point, so estimating unknown common throughput need not cause a first-order Fisher penalty in that model. This is **not** true generically for port-dependent efficiencies, nonlinear optical crosstalk, drift or nonuniform chart weights; those nuisance parameters can overlap the hidden chart sector.

## Reproducibility and branch safety

```powershell
python analysis/toe_20261121_capacity_fisher_schmidt_locality.py
python tests/test_toe_20261121_capacity_fisher_schmidt_locality.py
python tests/test_toe_20261121_fivefront_tightframe_coherent_memory.py
python tests/test_toe_20261121_fivefront_physical_falsifiers.py
python tests/test_toe_20261121_27decks_fivefronts.py
python tests/test_toe_20261121_hermitian45_pauli_sic_bridge.py
```

The producer never uses the network and requires only the repo's existing numpy/scipy/Naimark geometry sources. The external searches above are provenance/background, with date and *established versus new* claims separated. The six test categories are independently checkable, while the user-local repo has many unrelated dirty parallel edits which must not be staged or overwritten. No real photonic detector measurement, reproducible QKD key rate, or direct empirical physical TOE prediction is claimed.

## Top five independent next steps

1. **Coherent 9x5 encoding optimization with symmetry constraints:** turn the constructive 1.0867 qubits/use capacity lower bound into a systematic graph-aware rail assignment (rather than unrestricted row swaps), optimizing both coding fidelity and physical optical routing cost.
2. **New measurement family to exceed the Fisher benchmark:** seek an implementation with more Fisher trace per photon than the restricted 540 pair-probe ensemble, including detector-loss nuisance parameters and finite-sample likelihood validation.
3. **Hamiltonian gate realization audit:** map the eight product-operator decomposition onto ancilla-photon KLM, spin-photon cavity, or nonlinear-material resources, with explicit herald success and failure probabilities.
4. **Dynamical 45-state internal fiber:** engineer and test a local gauge connection on the 3-torus product that retains a nontrivial internal H(3,4) sector at finite physical energy without a collapsing spectral gap or imposed nonlocal transfer.
5. **Second outside-the-box information-theory test:** probe additivity/nonadditivity of the coherent-information lower bound for two routed channel uses, and derive resource-normalized information/energy inequalities before making any universality claim.
