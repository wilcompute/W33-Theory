# W33 Walsh-qutrit hardware bridge — decision record (2026-10-23)

**Purpose:** Resolve a critical gap between the 40-line-bus fractal network's 4-port XOR switch and its proposed qutrit quantum-processing core. Keep finite-geometry identities, simulated components, and unbuilt optical devices rigorously separate.

## What is now established

1. **Three logical dimensions inside four coherent optical rails.** The nontrivial columns (V) of (H_2\otimes H_2) form an isometry (V:\mathbb C^3\to\mathbb C^4). Every ideal XOR mask (m\in\mathbb F_2^2) satisfies (P_mV=VD_m), where (D_m=\mathrm{diag}_{s=1,2,3}(-1)^{s\cdot m}). Hence ideal XOR routing has **zero auxiliary leakage** in this particular encoding; it is not the naive three-spatial-ports code previously found to leak.

2. **Established metaplectic gate, new project embedding.** (D_1=\mathrm{diag}(-1,1,-1)), up to global sign and basis permutation, is the existing qutrit metaplectic reflection (R\). It is not a new gate species. Reference: Glaudell, Ross, van de Wetering, and Yeh, *Qutrit Metaplectic Gates Are a Subset of Clifford+T*, TQC 2022, https://doi.org/10.4230/LIPIcs.TQC.2022.12 .

3. **Rigorous infinite-projective-order witness.** For (A=F_3D_1), exact symbolic algebra yields (\operatorname{tr}A=-1/\sqrt3\), (\det A=-i\). The trace's field norm in (\mathbb Q(\sqrt3)) is (-1/3), hence it is not an algebraic integer. Finite projective order would force all eigenvalues to be roots of unity and the trace to be an algebraic integer, contradiction. **This does NOT prove density, quantum universality, or any multi-qutrit entangler.**

4. **Quantified rail-phase fragility.** For a maximally mixed Walsh-encoded qutrit and 4 differential optical rail phases (\phi_j\), auxiliary leakage is (\bigl(1-|\sum_j e^{i\phi_j}/4|^2\bigr)/3\). Independent iid Gaussian phase noise of standard deviation (\sigma\) obeys the exact expectation \(\mathbb E[p_{aux}]=(1-e^{-\sigma^2})/4\). For (\sigma=0.1\) rad the expected leakage is about **0.00249**. Uniform phase does not produce auxiliary leakage; differential attenuation can. This is not a complete quantum-process fidelity or worst-case error guarantee.

5. **An inter-bus rank obstruction and its construction.** Under the *hypothetical* one-mode-per-W33-point embedding in \(\mathbb C^{40}\), 240 line pairs intersect in one point (direct Walsh-code overlap rank 1; singular values 0.75,0,0) and 540 are disjoint (rank 0). Direct overlap cannot transport an arbitrary qutrit. A deliberately supplied 40-mode permutation that swaps 3 rail pairs for intersecting lines, or 4 for disjoint lines, maps the full code isometry exactly. All 780 pairs checked. The true optical netlist contains 160 point-line incidences and may require independent waveguides for each incidence; the 40-mode rank model is not already a built link.

6. **A second control frame is essential.** Accumulate optical scalar phase (e\in\mathbb Z_4) *and* Walsh logical XOR mask \(M\in\mathbb F_2^2\):
   \[
   e'=e+\operatorname{popcount}(m)\pmod4,\qquad M'=M\oplus m.
   \]
   The encoded net operation is \(i^eD_M\) and its ideal correction is \(i^{-e}D_M\). Two consecutive mask-01 switches have \(M=0\) yet \(e=2\), so either two-bit frame alone is insufficient. A uniform unknown mask completely dephases an equal-superposition qutrit into \(I_3/3\), even though no auxiliary leakage occurs. This distinguishes **logical decoherence** from **physical loss/leakage**.

7. **Actual dual-frame RTL simulation.** \(\texttt{hardware/w33_walsh_qutrit_frame.sv}\) and \(\texttt{hardware/tb_w33_walsh_qutrit_frame_20261023.sv}\) passed Icarus Verilog 12. The randomized 1,200-cycle run recorded **368 accepted commands and 416 stalls**. This is HDL simulation, not an FPGA bitstream, timing closure, electrode output or photon measurement.

8. **A further four-rail three-cycle induces qutrit Pauli X.** The full 24-element \(S_4\) group of rail permutations stabilizes the uniform auxiliary mode and acts faithfully by signed permutations on the Walsh qutrit. The physical permutation (0\mapsto0,1\mapsto2,2\mapsto3,3\mapsto1\) induces a logical 3-cycle (X_3^{-1}\). Conjugating by the separately compiled qutrit Fourier transform gives (Z_3^{-1}=\mathrm{diag}(1,\omega^2,\omega)\). **The current XOR-only optical switch cannot perform the order-three rail permutation; an additional optical switching primitive is needed.**

## Optical validation gates

A credible first test chip must support four phase-coherent rail inputs/outputs, a measured complex (4\times4\) scattering matrix for all requested masks and the rail three-cycle, prepared Walsh qutrit inputs, monitored uniform auxiliary output, tunable differential phase, controlled attenuation, calibrated detector/reference paths, plus a real foundry PDK and DRC/LVS. The qutrit Fourier processor must be verified separately. Long-range transport between buses must preserve all four rails, with optical timing/phase/loss budgets. None of those physical gates has been signed off here.

## Machine-readable evidence and reproducibility

- `analysis/w33_walsh_encoded_qutrit_interface_20261023.py`: character-subspace and encoded F3 algebra.
- `analysis/w33_walsh_qutrit_metaplectic_noise_20261023.py`: exact non-algebraic-integer trace proof, analytic Gaussian leakage and seeded Monte Carlo.
- `analysis/w33_walsh_qutrit_interbus_rank_20261023.py`: exhaustive 780 line pairs, all full-transfer permutations.
- `analysis/w33_walsh_qutrit_s4_affine_bridge_20261023.py`: exact 24-rail group representations and qutrit X/Z.
- `hardware/w33_walsh_qutrit_frame.sv`: scalar + logical frame controller and ready/valid handshake.
- `papers/fractal_holonet_walsh_qutrit_bridge_20261023.tex`: mathematical proofs, optical engineering gates and limitations.

**Evidence labels:** exact mathematics, passed Python regressions, Icarus HDL simulation, and *unimplemented* physical photon circuitry. No theory-of-everything, photonic universality, or fault-tolerance claim follows solely from these results.
