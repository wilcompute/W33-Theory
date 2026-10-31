# Eight-front W33 server continuation: an exact 4-hop cycle projector, compiled 160-rail encoder, optical resource accounting, quantum clocks, error-corrected Floquet edge, and gravity no-gos

**31 October 2026 — executed source/certificate/test suite.** This is a set of reproducible mathematical models, not an observed theory of everything. GitHub-only final publication, no authorized local desktop used.

## Previous work and parallel commits: attribution and honest scope

Read existing master at `15b3e3288fed8ba560a3c37ededafb3e4ad86749` and its recent parallel track including `b2f932159f68`, `149219895934`, `6343cdf59b72`, `7a57f8250496`. These establish the W33 81-dimensional Steinberg homology/Levi bridge, the native 13-Jones-tick SWAP, rank-one Jones f4 Strange projector, seven-direction Turán clock, and the previous all-120-tick transfer spectrum and two-site quantum toy. The parallel q=9 *240* is **not E8**, and the 216+216 signed-vector chiral partition is not to be conflated with 108+108 support splitting. Neither old result is represented as a fresh physics discovery here.

**New producer** `analysis/w33_20261031_eight_front_server_campaign.py`; **10 independent regression checks** `tests/test_w33_20261031_eight_front_server_campaign.py`; **machine-readable numerical certificate** `data/w33_20261031_eight_front_server_campaign.json`. All mathematical models have externally supplied boundary conditions, clocks, interactions, and physical hardware assumptions. Distinguish the five requested fronts (optical compiler, Strange heralding, local quantum clock, error-corrected edge, link curvature) from three deliberately outside-box probes (local projector/phase law, qutrit erasure code, Lorentz positive-metric no-go). Because optical and edge fronts each have an additional probe, there are eight producer modules.

## Front 1 / outside-box A — Exactly local polynomial projector on the 160 Levi flag rails

Let D be the integer 80×160 oriented incidence matrix of the W33 point-line Levi graph, with columns +1 on a line node and -1 on the incident point. Its rank is 79 and its cycle kernel has dimension **81** (previously known). Put B=DᵀD, the signed edge-space Hodge Laplacian. Its distinct nonzero eigenvalues are **8, 4, 4±√6**; therefore the exact orthogonal projector onto ker D is a degree-four polynomial:

\[
P=\frac{(8I-B)(4I-B)((4I-B)^2-6I)}{320}.
\]

The script performs the proof using **integer 160×160 arithmetic**: C=320P satisfies C=Cᵀ, C²=320C, DC=0, Tr C=25920, every diagonal entry C_ii=162. Hence P is rank81 with uniform rail diagonal **81/160**, without eigensolver approximation. This is a precisely local four-hop operator in the flag adjacency B. It is *not* an automatically available deterministic photonic postselection projector; implementing the polynomial requires a suitable unitary dilation, measurement/LCU or another physical resource.

One experimentally discriminating consequence: independent Gaussian rail-phase noise θ_j~N(0,σ²), a normalized |ψ> in ker D, and a perfect mathematical decoder satisfy

\[
\mathbb E_θ\,\|P\operatorname{diag}(e^{iθ_j})ψ\|^2
=e^{-σ^2}+(1-e^{-σ^2})\frac{81}{160}.
\]

This result is input-state-independent, follows by the scalar characteristic function of independent phases and the constant diagonal of P, and was checked by 1,400 seeded Monte Carlo trials at each σ. Predicted survival: σ=.15 → **.989015**, σ=.35 → **.943074**, σ=.7 → **.808734**, σ=1.5 → **.558291**. These are *conditional code-space probabilities in an ideal lossless model*, not detector data.

## Front 2 — An explicit 160-output-port, 81-input-port passive encoder

Take the orthonormal real 160×81 basis Q=null(D). Compile Q by a concrete bottom-up *adjacent-rail real Givens rotation* elimination. The code returns **8,416 two-mode operations**, rather than only citing a generic unitary-synthesis theorem. It inverses the full gate list onto 81 identity inputs and verifies the reconstructed Q in double precision at **1.12×10⁻¹³ Frobenius residual**. The source recreates the gate parameters and records the SHA256 of the numeric gate list in JSON. For the chosen elimination convention the simple worst-case pair count is 9,639. The Givens basis is version-dependent; an exact 4-hop projector is the basis-independent code specification. This is a mathematical encoder, not calibrated MZIs or a loss/noise-certified chip. For background on adjacent two-mode meshes see Reck et al., PRL73 (1994) 58 and Clements et al., Optica3 (2016) 1460.

## Front 3 — Asymmetric QND heralding noise exposes *state identity*, not merely negativity

The previously found f4 idempotent prepares the qutrit Strange eigenstate S=(|1>-|2>)/√2 from a supplied qutrit parity measurement R|j>=|-j mod3>. Its opposite even parity component E=(|1>+|2>)/√2 is itself **Wigner-negative**. Starting with |1>, both true parity outcomes occur with probability 1/2. Let f_n be the classical false-negative rate for S and f_p the false-positive rate for E. For the recorded minus herald,

\[
p_{\rm herald}=\frac{1-f_n+f_p}{2},\qquad
F_S=\frac{1-f_n}{1-f_n+f_p}.
\]

The heralded state is F_S|S><S|+(1-F_S)|E><E|. Wigner negativity **vanishes only at F_S=1/2** for this two-pure-state mixture; it returns for wrong-parity-dominated heralds. Consequently negativity is **not** a certificate of Strange fidelity. The simulator also multiplies the nominal heralding rate by an explicitly stipulated independent photon transmission factor; a failed |0> input produces false herald with probability f_p. All 6 asymmetric parameter triples pass exact density-matrix/Wigner checks. None of this synthesizes a physically free controlled-R QND coupler. See Jain & Prakash, Phys. Rev. A102,042409 (2020), DOI 10.1103/PhysRevA.102.042409.

## Front 4 — Local quantum clock length scaling: a clearly identified truncation

Use a bona fide 7-clique of *pairwise noncommuting W33 directions*, one fixed tick outcome each, and a **periodic 7-state-per-site quantum Hamiltonian**

\[
H_N=\epsilon\sum_{i=1}^{N}\mathbf1_{s_i\ne s_{i+1}}
-h\sum_i|+_7\rangle\langle+_7|_i,\qquad
\epsilon=-\tfrac23,
\]

with fixed N-periodic boundary and externally supplied local transverse mixing. The source diagonalizes the actual sparse 7^N×7^N Hamiltonian for N=2,3,4,5 (dimensions **49, 343, 2401, 16807**) at h=.12 and .5, checking positive *finite-size* gaps. For h=.12 the gaps are approximately **.09039, .08173, .06882, .07580** respectively, and energy/site tends near -0.762 across these finite sizes. For h=.5 the gaps are **.41529, .42403, .37770, .39839**. These observations do not establish a thermodynamic phase, and **this is NOT the full 120-local-state quantum Hamiltonian**. The earlier exact 120-label 1D *classical transfer* remains a separate result.

## Front 5 / outside-box B — An exact three-qutrit erasure code in the anomalous Floquet edge

Use the **previously known** [[3,1,2]]_3 quantum code (a standard perfect-tensor/quantum-polynomial construction):

\[
|s_L\rangle=\frac1{\sqrt3}\sum_{t\in\mathbb F_3}
  |t,s+t,s+2t\rangle.
\]

The source builds the full complex 27×3 isometric encoder and, for all three possible *known erased-site positions*, constructs a unitary 9×9 remaining-two-site decoder D_erased. It proves by explicit matrix multiplication that D†_erased Tr_erased(VρV†) D_erased = (I_3/3)⊗ρ for arbitrary logical ρ, including a seeded nontrivial complex superposition. This exactly corrects **one erasure** and independently reproduces the general survival curve 1−3p²+2p³ for i.i.d. erasures.

The *new W33 connection*, not the code itself, is to use three **consecutive moving boundary qutrits** from the native four-stage checkerboard SWAP Floquet drive. Each of these selected active carriers experiences two actual SWAP stages, i.e. 26 native ticks, irrespective of open L=4,6,8. Assuming each tick causes an independently *flagged erasure* of probability p_gate, their per-carrier erasure is q=1−(1−p_gate)^26. For p_gate=.001, .005, .01, the unencoded carrier survival is **.97432, .87781, .77004** and encoded recovery is **.99806, .95886, .86568** respectively. A geometric chiral boundary is not an error-correction code by itself. Code preparation, decoding, entanglement gates, unflagged depolarization and correlated losses remain excluded. Prior art: Pastawski et al., *Holographic quantum error-correcting codes*, JHEP06 (2015) 149, Appendix A.2; Tan, *Transversal gates of the ((3,3,2)) qutrit code*, 2026, arXiv:2601.19677.

## Front 6 — Curvature-bearing canonical lattice gauge control, without assuming GR

Build a **3×3×3 periodic spatial lattice** with site two-component real matter frames x_v,p_v and three directed U(1)/SO(2) link angles a_(v,mu) with canonically conjugate electric momenta E_(v,mu). Take the action/Hamiltonian sum

\[
\tfrac12\sum_v \|p_v\|^2+\tfrac12\sum_l E_l^2
+\tfrac12\sum_{v,\mu}\|x_{v+\mu}-R(a_{v\mu})x_v\|^2
+0.7\sum_{\square}(1-\cos(\operatorname{curl}a)).
\]

Under independent vertex rotations θ_v, the link shifts a_(v,mu)→a_(v,mu)+θ_(v+mu)−θ_v and the matter canonical pair rotates together; the action including **nontrivial plaquette curvature** is invariant to machine precision. A centered finite-difference local Ward derivative likewise vanishes (<1e-7). The canonical Gauss generator has matter charge p^T J x plus incoming-minus-outgoing electric flux. **This is an explicitly supplied Abelian gauge control, not non-Abelian Lorentz Einstein–Cartan/Palatini dynamics.** No Hamiltonian and diffeomorphism Dirac-constraint closure has been achieved. Compare Husain & Javed, *Anomaly in Canonical Semiclassical Gravity*, PRL137,031501 (2026), DOI 10.1103/q81l-xfkx, for why closure is a real consistency hurdle.

## Outside-box C — Positive Hilbert-space obstruction for a naive Lorentz frame

An internal Lorentz boost K_x in the 4-vector representation has real eigenvalues {+1,−1,0,0}; its finite transformation has eigenvalues e^{±θ},1,1. It preserves the indefinite Minkowski form η but **cannot** preserve any positive-definite constant inner product on that nontrivial real four-vector representation. Explicitly the naive previous ultralocal quadratic energy 0.5 p^Tηp runs through **−.5, −2, −8, −32** along scaled timelike p vectors and is unbounded below. This is a sharp ghost/positive-metric obstruction to that particular candidate Hamiltonian, not a no-go for constrained general relativity, physical unitary Lorentz representations or spin-two gravity.

## Reproducibility and publication

Run `python -m pytest -q tests/test_w33_20261031_eight_front_server_campaign.py` and `python analysis/w33_20261031_eight_front_server_campaign.py`. The campaign has **8 PASS producer modules** and **10 pytest tests** on the server Python environment. Frozen output contains all tested parameters, fidelity/exposure curves, optical gate digest and negative-control boundaries. The code references only the already-committed `analysis/w33_20261031_server_five_fronts.py` plus numpy/scipy/networkx.

## Top five mutually independent next investigations

1. **Hardware economy:** find a sparse/cycle-basis 160-port optical encoder requiring materially fewer than 8416 interferometers, and co-optimize topology and loss.
2. **Operational Wigner witness:** devise a herald verification circuit that distinguishes Strange fidelity from generic Wigner negativity and incorporates detector assignment errors.
3. **Longer quantum clock:** extend the *full 120-tick* quantum local space via MPO/DMRG and search for finite-size collapse and emergent order parameters, not just the 7-state truncation.
4. **Fault models of the edge:** combine the [[3,1,2]]_3 erasure decoder with actual noncommuting coherent and correlated faults and count the preparation/decoding resource overhead.
5. **GR constraints:** replace the Abelian control with a noncompact link/tetrad Palatini phase space, derive a scalar and spatial diffeomorphism constraint and test the complete first-class Poisson algebra under refinement.
