# Five physical gates and two falsifiers: Witting detector identifiability, Petz decoding, postselected two-ququart gates, and Gauss-preserving gauge dynamics

**Date:** 2026-11-21. **Audited baseline:** `wilcompute/W33-Theory` `master` at `1e45ad2f66a975bd86b3e0ea1c5f0d4f1d88f43f`. **Reproduction:** `analysis/toe_20261121_five_physical_gates_decoder_blinding_z2.py`; `data/toe_20261121_decoder_calibration_teleport_gauge_falsifiers.json`; `tests/test_toe_20261121_five_physical_gates_decoder_blinding_z2.py`.

**Research provenance / limits:** The Witting/Hermitian 40-ray, 45-chart, 27-schedule construction and 4→9⊗5 Stinespring Naimark channel are **prior committed repo constructions**. Previous versions proved a 24D hidden-chart one-photon decoder, a 25-bin compressed measurement and a >1.097 coherent-information capacity lower bound, but did not demonstrate identifiable ray-dependent efficiency, an explicit decoder, a conditional gate implementation or dynamical gauge-link constraints. In addition, the repo **already has** fully dynamical \(\mathbb Z_2\) matter-gauge prototypes: `analysis/toe_20261104_matter_dynamical_z2_flux_competition.py`, `analysis/toe_20261105_two_connected_c4_gauge_matter_gauss.py`, and `analysis/toe_20261105_gauss_dressed_page_information.py`. The gauge advance in this pass is **independent exact integration of a local square-lattice Gauss model with a 45-state chart internal sector**, not the first discovery of dynamics or Gauss law in this repository.

External mathematical references checked here:
- Petz/transpose recovery and optimality caveats: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.134.200602 and https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.128.220502.
- Quantum gate teleportation background and photonic resource constraints: https://www.nature.com/articles/srep45353; the paper's optical controlled-SWAP realization does **not** establish the present gate or its resource probability.
- Genuine \(\mathbb Z_2\) gauge-matter lattice Hamiltonians and Gauss constraints: https://www.nature.com/articles/s42005-023-01237-6 and https://doi.org/10.1093/PTEP/PTAA171.
- Calibration/identifiability: https://arxiv.org/abs/2609.13584 and https://www.nature.com/articles/ncomms14485; gate-set tomography gauge freedoms are related as an analogy, not identical to the exact nuisance-parameter ambiguity derived below.
- Gauge-field truncation caution, 2026: https://doi.org/10.22331/q-2026-09-24-2216.

## Front 1 — Exact **no-go** for uncalibrated blind ray-dependent efficiencies

Prior one-photon tomography uses the \(45\times40\) binary chart/ray incidence H, with \(HH^\top=6I-2A+2J\), and hidden chart selection \(w={\bf1}_{45}/45+x\), \(x\in\ker K^\top\) of dimension24. Define the *ideal mixed-input* global ray-label probabilities \(t_i=(H^\top w)_i/8\). If detector i has an unknown chart-independent efficiency \(\eta_i>0\), the actual **unconditioned** ray-report probability for *any* known ququart source \(\rho\) is
\[
\boxed{p_i(\rho)=4\eta_i\, t_i\,\mathrm{Tr}(\rho P_i), \quad
p_{\emptyset}(\rho)=1-\sum_i p_i(\rho).}
\]
The full quantum experiment depends only on the **40 products** \(\eta_i t_i\), not on the two parameter families separately. For *any* alternative positive chart distribution \(w'\) with \(t'_i>0\), if \(\eta'_i=\eta_i t_i/t'_i\) also stays in \((0,1]\), every labeled ray probability and no-click probability for **all possible input states** is identical. In particular, changing only a 24D hidden-chart direction can always be offset by an allowed small detector perturbation. The Jacobian of observed p with respect to x and η therefore has a **24D exact nullspace**.

The code constructs two distinct positive chart laws and two physically admissible (0,1] detector vectors, probes all 40 Witting pure states plus the mixed state, and verifies exact equality of all readouts. **No increase in the diversity or quantity of known input states alone resolves this confounding** under the stated model. This is a structural identifiability obstruction, not a finite-statistics complaint.

**Fix:** A separately trusted reference run with known uniform chart-selection weights \(w_{\rm ref}=1/45\) makes \(t^{\rm ref}_i=1/40\) and yields \(\eta_i=40p_i^{\rm ref}(I_4/4)\), when **no-click launches are counted**. Calibrated target counts yield \(t_i=p_i^{\rm target}/\eta_i\); then \(x=P_{24}\frac23H(t-{\bf1}_{40}/40)\). Exact arithmetic recovers x; seeded full-multinomial simulations at 20k, 200k, 2M calibration AND target launches demonstrate finite-shot uncertainty. In one seeded 2-million/2-million test the L2 bias error is approximately .00175, with no universal guarantee. This corrects the earlier unconditional expectation of 3.2M detected photons: that figure assumed *known* and lossless ray labels; it does not include calibration overhead.

If efficiencies vary arbitrarily by chart and detector port, calibrating one global η_i is no longer sufficient.

## Front 2 — Real, trace-preserving Petz quantum recovery

For the previously committed 4→9 channel with five explicit 9×4 Kraus matrices \(K_j\), define \(\tau=I_d/d\) on a code subspace \(d=4\) or2 and \(\sigma=\mathcal N(\tau)\). The transpose-channel/Petz recovery has Kraus matrices
\[
R_j=\tau^{1/2}K_j^\dagger\sigma^{-1/2}.
\]
The code constructs the inverse sqrt on the support of σ and adds a completion Kraus operator for any output orthogonal to that support. It explicitly verifies \(\sum_jR_j^\dagger R_j=I_9\), and that recovery composed with the encoding channel is trace preserving.

For maximally mixed logical input, entanglement fidelity is
\[
F_e(\mathcal R\circ\mathcal N)=\frac1{d^2}
\sum_{\alpha,j}\left|\operatorname{Tr}(R_\alpha K_j)\right|^2,\qquad
F_{\rm avg}=\frac{dF_e+1}{d+1}.
\]
The **full ququart** yields \(F_e=0.61108960516\), \(F_{\rm avg}=0.68887168413\). A fixed-seed search of 300 random orthonormal *two-dimensional subcodes* (each a 4×2 isometry; best explicit coefficients frozen) finds \(F_e=0.90349720672\), \(F_{\rm avg}=0.93566480448\). The search is *not* globally optimized, and this is not a fault-tolerance threshold. The 2D subcode is a concrete one-logical-qubit *recoverable code for a single use*, but no error syndrome circuit, photonic decoder hardware or many-use coding theorem has been physically implemented. It strengthens prior positive coherent-information **capacity** bounds with a distinct finite-use, explicitly executable **recovery map**.

## Front 3 — A mathematically exact conditional gate, with explicit resource circularity

Every chart has a rank6 projector \(\Pi_z=3Q_z/4\) on two ququarts, so at \(t=3\pi/8\),
\[
U_z=e^{-itQ_z}=I_{16}+(-1-i)\Pi_z.
\]
The term \(I+(-1-i)\Pi\) is exactly unitary because it applies \(-i\) on the rank6 subspace and identity elsewhere. A **generic** gate-teleportation construction prepares the normalized entangled resource
\[
|\Phi_{U_z}\rangle=(I_{16}\otimes U_z)|\Phi_{16}\rangle,
\quad |\Phi_{16}\rangle=16^{-1/2}\sum_{a=1}^{16}|a,a\rangle,
\]
and Bell-projects the 16D two-ququart input together with the resource's first 16D register onto \(|\Phi_{16}\rangle\). The accepted branch is \(U_z|\psi\rangle/16\) for **every** input state, hence
\[
\boxed{p_{\rm accepted}=1/256=0.390625\%.}
\]
Verified on all45 U_z and 135 seeded random input states, with maximum amplitude error below numerical precision. The two 16D resource registers require **four additional ququarts**, in addition to the two input ququarts; a joint d=16 Bell measurement is needed. Other Bell outcomes require U-dependent corrections and are **not** claimed successful.

**Critical caveat:** Preparing \(|\Phi_{U_z}\rangle\) may be as difficult as performing U_z itself. This is an *exact mathematical postselected protocol*, **not a physically bootstrapped KLM implementation** and not a resource-efficient solution to the actual heralded gate problem. It is a rigorous reference envelope for any later physical implementation.

## Front 4 — Genuine \(\mathbb Z_2\) Gauss-invariant matter/link Hamiltonian coupled to Witting chart sectors

Construct a square of four matter qubits and four link qubits, raw dimension 256. Use Pauli matrices X,Z, with **four local gauge generators**
\[
G_v=Z_{m,v}X_{\ell,v-1}X_{\ell,v},\qquad G_v|\psi_{\rm phys}\rangle=+|\psi_{\rm phys}\rangle.
\]
A local gauge-invariant Hamiltonian is
\[
H_g=-t\sum_{v=0}^{3}X_{m,v}Z_{\ell,v}X_{m,v+1}
-g\sum_\ell X_\ell-m\sum_vZ_{m,v}-\kappa W,\qquad
W=\prod_{\ell=0}^{3}Z_\ell.
\]
Every \([H_g,G_v]\) and \([W,G_v]\) vanishes by exact matrix multiplication. The physical Gauss+ Hilbert subspace has **dimension16**, constructed explicitly via link-X eigenstates with matter occupations fixed by Gauss law. For fixed (t,g,m)=(.4,.5,.6), scanning \(\kappa=0,.1,.25,.5,.8\) changes the ground Wilson-loop expectation from ~.00878 to ~.39244, demonstrating real plaquette competition within the **toy** Hamiltonian.

Introduce a separate 45-level Witting chart *internal* Hilbert space with adjacency A and internal energy \(\Delta(12I-A)\), whose spectral decomposition is uniform1, 20D and 24D. An imposed gauge-invariant coupling \(-\lambda W\otimes P_{24}\) shifts the 24D branch relative to others; for \(\Delta=.01,\lambda=1\), it makes that branch lowest. This is engineered via the very projector being tested and **not a mechanism of spontaneous sector selection**.

**More revealing independent test:** instead couple the Wilson operator to a *single chart-state defect* \(D=|z=0\rangle\langle z=0|\), which does not commute with the three chart spectral projectors:
\[
H_{\rm combined}=H_g\otimes I_{45}+
\Delta I_{16}\otimes(12I_{45}-A)
-\lambda W\otimes D.
\]
The full gauge-physical Hilbert dimension is 16×45=720. Sparse exact diagonalization of its lowest eigenstate gives *internal sector weights*:
- λ=0: uniform ~1, 20D~0, 24D~0.
- λ=.3: uniform .9713, 20D .01976, 24D .00892.
- λ=1: uniform .04645, 20D .50795, **24D .44560**.
- λ=2: uniform .02768, 20D .46712, **24D .50520**.

This **genuine mixing** is qualitatively stronger than shifting the 24D sector alone and respects the four Gauss laws, because W is gauge invariant. But it remains a finite, externally engineered 45-level defect coupled to existing known \(\mathbb Z_2\) toy gauge physics, not emergent SU(3), electroweak interaction, gravity, or spacetime.

## Front 5 — Exact information leakage from globally labeled ray outcomes

If an unknown chart Z is sampled uniformly from45, and a **fixed chart** is reused for n independent maximally mixed input photons with globally labeled Witting-ray detector outcomes, each chart has eight equally likely ray labels. The posterior on charts is uniform among all charts compatible with the entire observed ray sequence. Enumerate all sequences exactly, not by Monte Carlo. For \(n=1,2,3,4\):

| Photons from a fixed chart | \(I(Z;\text{rays})\), bits | Optimal chart-identification success |
|---:|---:|---:|
| 1 | 2.321928 | 1/9 = 11.11% |
| 2 | 4.303131 | 5/9 = 55.56% |
| 3 | 5.145143 | 31/36 = 86.11% |
| 4 | 5.398984 | 96.18% |

The one-ray identity gives chart posterior 9 possible charts because each ray occurs in exactly9 charts; \(I(Z;\mathrm{ray})=\log_2(45/9)=\log_2(5)\). Reusing a chart repeatedly therefore makes it identifiable rapidly. This is **not cryptographic security**: even one globally labeled ray leaks chart information; chart IDs need not be explicitly logged to leak.

The **24-resolved-ray plus 16-ray merged detector**, previously proven sufficient for local 24D identifiability, has one-shot chart information of **1.43591773 bits**, versus 2.32192809 for all40 ray labels. This quantifies a concrete *information-versus-privacy* tradeoff: the coarsened 25-bin scheme has worse Fisher information but leaks less chart information. A fresh random chart each independent shot changes repeated-chart inference; this table applies specifically to one fixed chart reused n times.

## Front 6 — The one-photon 24D model has 15 independent goodness-of-fit constraints

The 40-component labeled-ray probability vector has simplex dimension39, while the assumed hidden chart-bias model spans only24 nonuniform directions. It must satisfy **15 independent linear constraints** beyond probability normalization. Define the orthogonal projector
\[
Q_{24}=H^\top P_{24}H/12,\quad Q_1=J_{40}/40,\quad
R=I_{40}-Q_1-Q_{24}.
\]
Here \(R^2=R\) and \(\operatorname{rank}R=15\) are verified. At the uniform operating point with N independent labeled photons, the statistic
\[
\chi_{\rm model}^2=40N\left\|R(\widehat p-{\bf1}_{40}/40)\right\|_2^2
\]
approaches \(\chi^2_{15}\) asymptotically under correctly calibrated i.i.d. multinomial draws. A fixed-seed 400-replicate simulation at N=20000 gives mean **14.70867**, consistent with expected15.

**Limitation:** an adversarial detector distortion *inside the 24D model subspace* passes all15 constraints, potentially giving a completely false yet mathematically consistent chart estimate. A model-residual test can reject certain wrong hardware models, but it **cannot replace the independent efficiency calibration required by Front1**.

## Reproduction, safeguards and scientific boundaries

Run from `C:\Repos\Theory of Everything`:
```powershell
python analysis/toe_20261121_five_physical_gates_decoder_blinding_z2.py
python tests/test_toe_20261121_five_physical_gates_decoder_blinding_z2.py
```
The producer checks its own exact algebra and writes a machine-readable JSON certificate. The tests rederive all six fronts with seeded randomness. The previous 73 Witting regression tests should also be run before a push.

All claims here are **algebraic identities or simulations with explicitly assumed physical inputs**. No Witting photonic chip, heralded six-ququart optical setup, cryptographically hidden chart, self-organizing Standard Model gauge group, Einstein field equation, or TOE has been built or observed. No universal physical constant was inferred from these numerics.

## Top five independent next steps

1. **Blind single-photon detector with independent reference run:** design an explicit 45-chart control protocol with randomized chart per launch and stable ray mapping; quantify whether hardware calibration data can eliminate the nuisance gauge without exposing the per-shot chart ID to a third party.
2. **Petz decoder circuits and noise bounds:** build a 9→2 coherent recovery from the stored best 4×2 code subspace, measure entanglement fidelity under amplitude damping, phase drift and Naimark misrouting, and compare to a variational or SDP-optimal recovery.
3. **Noncircular heralded two-ququart phase primitive:** find a genuinely implementable resource-state preparation that does not assume access to the target U_z; quantify ancillary photon count, nonlinearity, Bell-analyzer success and herald detector inefficiency.
4. **Gauge-geometry phase structure:** extend the finite Gauss-preserving gauge model to connected spatial plaquettes and compare chart-local defect mixing with a **fully PGU-symmetric** gauge-invariant coupling; ask whether the 24D structure survives without tuning in its own projector.
5. **Joint privacy–Fisher experimental design:** optimize which 24 ray labels to resolve to minimize chart mutual information while maximizing worst-case Fisher information after realistic detector confusion; search for hardware-feasible Pareto-optimal 25-bin sensors.
