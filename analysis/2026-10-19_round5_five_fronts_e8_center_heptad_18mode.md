# W33 round 5: Five independent fronts — E8 matter, seven-tick outcomes, single-photon optics, 248D Jacobi, and falsifiability
**19 October 2026.** Baseline: prior October 19 commit 34e9c5ab7 and concurrent Passes 12058-12059, Pass398. All code executed in a separate clean worktree. **No new TOE prediction or laboratory experiment is established.**

## 1. SU9/E8 center obstruction to nine fundamental fermions

The repo's Pass11681 and Pass11687-91 already build the standard A8 grading e8=sl9+Lambda3(C9)+Lambda3(C9)* of dimensions 80+84+84. The scalar omega*I9, omega^3=1, lies in SU9 and acts trivially on sl9, Lambda3 and Lambda6, hence on ALL e8 adjoint 248. But it acts nontrivially as omega on the fundamental V=C9. Therefore **the fundamental 9 is not a linear representation of the embedded SU9/mu3 group**. In particular the previously studied nine independent fundamental fermion modes with H=I-(P+Q)/2 do not follow from e8 ADJOINT matter alone. This is a strict representation-theoretic obstruction, **not** a no-go for separately added 9 matter fields after a gauge lift or suitable symmetry breaking. The chemical potential mu=.5 also remains a supplied choice; the repo does not derive it from E8. A three-fermion representation Lambda3(C9) of dimension 84 is not equivalent to nine independent one-particle fermion modes.

## 2. Exhaustive outcome labels of one W33 maximum noncommuting heptad

The previous mathematical reduction proved every global finite-T minimizer of F+kappa*C must assign one outcome label to each occupied W33 point, leaving 40 continuous masses plus discrete k(p) in {0,1,2}. For ONE maximum noncommuting seven-point set, fix uniform masses s_p=1/7. Exhaustively diagonalize 9x9 Pauli projector sums for **3^7=2187 assignments**. Find **five distinct eigenvalue spectra** to 10 decimals. At T=.5, energy min = -0.464573662239, max = -0.463335098147, spread = .001238564091. All have exactly C=4/7, so outcome choice changes Gibbs energy without changing the kappa term. All-k=0 is rank 973 of 2187 on this heptad; it is not the best assignment. This does NOT solve continuous mass optimization, other heptads, or the complete negative-kappa phase diagram. The five classes motivate exact stabilizer-orbit quotient and interval global bounds.

## 3. Explicit 18-mode ONE-PHOTON trace interferometer

Let W=U_P(theta)U_Q(theta)U_P(-theta)U_Q(-theta) with Q=GPG-dagger, G=CZ(F3 tensor I3), P=|0><0| tensor I3. An ideal passive-linear circuit can use a SINGLE photon with path as 2D ancilla and an internal 9D register. It acts by the 18x18 unitary

    (H2 tensor I9) diag(I9,W) (H2 tensor I9).

Prepare one photon in path 0 and internal basis |j>, j in 0,...,8. The difference of probabilities for output path 0 vs 1 equals Re(W_jj). Nine equally weighted preparations produce the normalized trace ReTr(W)/9, WITHOUT a second target photon or optical photon-photon nonlinearity. The W arm compiles into **four rank-three projector phase pulses, two G and two G-dagger blocks**, and the two path couplers. Matrix checks confirm ideal deficit 8/27 and commuting-null zero, and 18-mode unitarity/compilation at ~1e-15. Important hardware caveats: coherent nine-mode transforms, optical routing, calibrated phase, leakage and loss still demand a real device study. This is an existing DQC1 / optical mode strategy, not a claim to have invented single-photon trace interferometry. External prior art: https://link.springer.com/article/10.1140/epjqt/s40507-022-00142-1 and https://link.springer.com/article/10.1007/s13538-025-02006-2.

## 4. Repository 248-coordinate injection and mixed Lie bracket verification

Use the EXISTING repo analysis/w33_pass11681_e8_from_two_qutrits.py elementary basis, pseudoinverse Slp, E.bracket(gamma=-1), E.jacobi_certificate, and Pass11687-91 E8Data.act. Construct explicit 248x80 J with column j = [Slp @ vec(Pa-Pb); zeros84; zeros84]. J has rank 80 and exactly reconstructs the Pauli contrast basis. Conjugation of five determinant-normalized Clifford generators F1, S1, CZ, SUM, SWAP intertwines with the repository E8 coordinate action; full 248D mixed bracket is preserved on random elements and the existing all-27-grade Jacobi certificate reproduces gamma=-1. Jacobi residual ~1.29e-13; bracket automorphism residual ~1.97e-13. This is a concrete map into the repo's **elementary sl9 plus exterior tensor coordinate basis**, NOT a normalized 248-root Chevalley basis or an E8(-24) real-form identification. The mixed bracket and Jacobi closure are acknowledged as **prior repository result Pass11681**, not claimed as newly discovered.

## 5. Conditional extra-dynamics falsifier and optical calibration identifiability

Specify hypothetical W_eta(theta,epsilon)=exp(i eta K)*U_P(theta)U_Q(theta+epsilon)U_P(-theta)U_Q(-theta-epsilon), K=i[P,Q] Hermitian. Eta is an assumed extra-coupling parameter; epsilon is phase calibration offset. One echo angle cannot identify both. Eight preselected angles .35 to 2.7 rad yield 8x2 local sensitivity matrix with singular values .85257 and .06847; the two parameters are locally identifiable in the ideal model. Under an **ideal independent binomial photon model** and 100,000 trials PER ANGLE, conditional Cramer-Rao sigma(eta) is ~.00914, excluding losses/drifts and other systematics. A commuting null is insensitive to K and does not identify eta by itself. This defines a possible *protocol to falsify an extra-gate model if eta is predicted independently*. It is NOT a novel parameter-free TOE law: the same eta model is conventional quantum dynamics if it simply adds a Hamiltonian. Without a physical mechanism fixing eta, sign and units, data-fitting eta proves nothing about W33 being fundamental.

## Reproducibility

- analysis/w33_20261019_round5_e8_fermion_center_and_heptad.py -> data/w33_20261019_round5_e8_fermion_center_and_heptad.json
- analysis/w33_20261019_round5_single_photon_18mode_trace.py -> data/w33_20261019_round5_single_photon_18mode_trace.json
- analysis/w33_20261019_round5_e8_repo_248_jacobi.py -> data/w33_20261019_round5_e8_repo_248_jacobi.json
- analysis/w33_20261019_round5_conditional_anomaly_identifiability.py -> data/w33_20261019_round5_conditional_anomaly_identifiability.json
- tests/test_w33_20261019_round5.py reproduces checks.

**Physics firewall:** the center obstruction is an exact algebraic no-go for one PARTICULAR matter assignment; seven-heptad census exact combinatorial exhaustion with numerical eigenvalues; 18-mode interferometer an ideal transfer matrix; E8 Jacobi uses existing repo; eta still unpredicted. No TOE discovery or hardware demonstration is claimed.
