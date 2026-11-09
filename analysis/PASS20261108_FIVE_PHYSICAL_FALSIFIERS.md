# Five post-Pass12632 physical falsifiers: Maxwell, E6 vacuum, complex clock, photonic injection, cosmology repair

**Date:** 2026-11-08. **Repository:** wilcompute/W33-Theory.
**Producer:** `analysis/w33_20261108_five_physical_falsifiers.py`.
**Tests:** `tests/test_w33_20261108_five_physical_falsifiers.py`.
**Frozen machine result:** `data/w33_20261108_five_physical_falsifiers.json`.
**Prerequisite:** `analysis/PASS12632_HALOFIT_SCF_BUG.md` explicitly retracts earlier shear interpretations. Do NOT use stale S8 Shapley values as physical evidence.

## Evidence firewall

These five tasks execute finite geometric or algebraic checks, numerical local optimization, an ideal circuit, and a **withdrawal-aware CLASS control check**. They do not derive gauge charge normalization, electroweak masses/mixings, gravity, two experimental gapless photons, a physical photonic quantum computer, or new cosmological detection. Independent external observational inference is not available in this packet.

## Front I — A local square-curvature completion is FULL rank, but completely gapped

Use the original Forty Points null graph on 27 vertices \(\operatorname{Sym}_2(\mathbb F_3)\), with 108 edges along the four null directions
\[
(1,0,0),\quad(0,0,1),\quad(1,1,1),\quad(1,2,1).
\]
The original 36 oriented triangular face boundaries form an edge-face incidence \(B_\triangle\in\mathbb Z^{108\times36}\), with rank 36. Its vertex-edge incidence \(\partial_1\) has rank 26.

For every ordered vertex \(x\) and unordered pair \(i<j\) of the four directions, add the oriented local square
\[
x\to x+d_i\to x+d_i+d_j\to x+d_j\to x.
\]
There are **162 distinct squares**, with \(\partial_1 B_\square=0\). Explicit integer matrix construction and numerical rank verification give
\[
\operatorname{rank}[B_\triangle\ B_\square]=82=108-26.
\]
The characteristic-zero rank is proved without relying only on floating SVD: row reduction modulo 101 gives rank 82, while \(\partial_1[B_\triangle\ B_\square]=0\) and \(\operatorname{rank}\partial_1=26\) force an upper bound 82. The integer matrix also exactly satisfies \(K(K-3I)(K-6I)(K-9I)(K-12I)=0\), with matching integer trace moments of orders 1 through 4. Thus \(H^1\) over the reals vanishes for the enlarged 2-complex. The equal-weight magnetic curvature operator has the **complete exact integral eigenvalue census**
\[
\boxed{\operatorname{spec}(B_\triangle B_\triangle^T+B_\square B_\square^T)
=0^{26}\oplus3^4\oplus6^{12}\oplus9^{40}\oplus12^{26}.}
\]
The zero eigenspace is *precisely gauge gradients*. Every positive physical magnetic eigenvalue is at least 3 in these fixed units. A finite torus with this complete set of cell relations has **no remaining gapless transverse modes**. It demonstrates that completing local faces can remove the 46 unwanted harmonic modes, but ordinary equal-stiffness completion does not produce two photons. A controlled continuum limit, correct polarization content and Lorentz dispersion require an additional mechanism.

This is a genuine new local construction relative to the previously established all-positive-*reweighted-triangle* no-go; not a no-go for all possible finite gauge theories.

## Front II — An E6-compatible invariant potential selects rank-three VEVs but leaves 477 flat scalars

Let \(\Xi\in\mathbb C^{81\times3}\) be three independent 81-component scalar multiplets and take the positive semidefinite, unitary-representation-covariant potential
\[
\boxed{V(\Xi)=\lambda\operatorname{Tr}\big[(\Xi^\dagger\Xi-v^2I_3)^2\big],\quad\lambda>0.}
\]
Any compact unitary E6 representation on the 81 coordinates leaves this potential invariant, as does a right U(3) action (an accidental flavor symmetry of the *potential*, not necessarily the mass couplings). The global minima satisfy \(\Xi^\dagger\Xi=v^2I_3\): there are indeed three independent VEV directions.

The minimum set is a complex Stiefel manifold \(V_3(\mathbb C^{81})\), of real dimension
\[
2\cdot81\cdot3-3^2=\boxed{477}
\]
inside 486 real scalar coordinates. The quadratic potential Hessian has 9 positive normal eigenvalues \(8\lambda v^2\) and **477 flat tangent eigenvalues** at any such vacuum, before gauge fixing or adding interactions. An explicit numerical normal-versus-tangential curvature check confirms the expansion.

Using the *native 1620 signed cubic records* reconstructs the 81×81 complex alternating mass matrix of rank 78. A deterministic Gram-orthonormal \(\Xi\) then supplies three rank-one nonholomorphic EFT bilinears and lifts rank to 81. The earlier exact Pfaffian/determinant identity still applies; the resulting determinant phase is generic and nonzero.

**Obstruction:** This potential alone cannot isolate a vacuum or explain the observed CKM/PMNS hierarchy, SM chirality/anomaly cancellation, or \(\bar\theta\). Three VEVs with rank 81 are a necessary algebraic capacity witness, not a physical mass spectrum. Generic flavor-breaking and radiative corrections require separate full-theory analysis; gauge-orbit flat directions must not be counted as physical massless particles without specifying the gauge group.

## Front III — Native q=5 null-local clock: 24 real parameters from 12 complex Hermitian pairs

The null cone in \(\operatorname{Sym}_2(\mathbb F_5)\cong\mathbb F_5^3\) has 24 nonzero displacement vectors grouped in six projective directions, or **12 antipodal pairs**. Fix a translation-invariant Hermitian Hamiltonian with complex coefficients \(c_v\) on each of the 12 representative vectors and \(c_{-v}=\overline{c_v}\). There are 24 independent real parameters (versus the previous six equally weighted real direction classes).

The exact finite Fourier spectrum is
\[
\lambda(k)=2\sum_{v\in C}\big[\operatorname{Re}(c_v)\cos(2\pi k\cdot v/5)
+\operatorname{Im}(c_v)\sin(2\pi k\cdot v/5)\big].
\]
The propagated amplitude from the origin is the 3D inverse discrete Fourier transform of \(e^{-i\lambda(k)}\). Minimize
\[
L(c)=\frac1{125}\sum_{x\in\mathbb F_5^3}\Big(|U_{x0}(1)|^2-\frac1{125}\Big)^2.
\]
The producer checks analytic gradients against independent centered finite differences and uses four deterministic L-BFGS-B starts, including the actual preceding best six-parameter couplings as a nested feasible seed.

Results from the frozen producer:
- Previous six-real baseline loss: approximately **2.242611446×10⁻⁵**.
- New complex Hermitian 24-real best loss: approximately **1.135767544×10⁻⁵**.
- Improvement factor approximately **1.97**.

The search remains a **bounded numerical heuristic**; none of the four starts finds exact flatness. This does not prove a global minimum or a no-go for complex hopping, magnetic cocycles, translation-breaking models, or time-dependent controls. It does show the old six-real search was materially incomplete.

## Front IV — An exact ninth-root qutrit magic injection, plus an intensity-only null witness

Define \(T_9=\operatorname{diag}(1,\zeta_9,\zeta_9^{-1})\), \(\zeta_9=e^{2\pi i/9}\), and \(t_j\) its three entries. Prepare a separate ancilla qutrit in
\[
|A\rangle=T_9|+\rangle=3^{-1/2}\sum_jt_j|j\rangle.
\]
For input \(|\psi\rangle=\sum_xa_x|x\rangle\), apply **controlled-SUM\(^{-1}\)** from data to ancilla:
\(|x,j\rangle\mapsto|x,j-x\rangle\). Measure the ancilla in the computational basis and obtain outcome \(m\in\{0,1,2\}\), each with probability \(1/3\). The unnormalized output is \(\sum_xa_xt_{x+m}|x\rangle/\sqrt3\). Correct with the feedforward diagonal
\[
C_m=\operatorname{diag}(t_x/t_{x+m})_x.
\]
The producer tests all three complete branches against random normalized complex data states and verifies each \(C_m\) is a **single-qutrit Clifford** by conjugating Pauli X into the Pauli group. Hence the ideal logical correction circuit implements \(T_9\) with deterministic accepted outcomes, assuming ideal operations/detection.

For 27 logical modes, three stages of nine ideal tritters implement \(F_3^{\otimes3}\); all **729** input-output intensities equal \(1/27\). A ninth-root *input diagonal* does not change **any** of those intensities. Thus **729 correct intensity probabilities cannot certify the non-Clifford phase**, even in an ideal device; calibrated relative-phase interference or quantum process tomography is necessary.

**Hard physical boundary:** The controlled-SUM\(^{-1}\) is a genuine *two-qutrit entangling primitive*, not provided automatically by single-photon passive optics. The logical protocol is not a one-photon optical implementation. State preparation, heralding, gate error, feedforward latency, detector efficiency, routing and realistic loss all remain engineering tasks. The symbolic end-to-end success budget includes an entangling-gate success factor and 27 tritter transmissions; no measured numerical success is asserted.

## Front V — Withdraw old cosmic-shear rankings and replay only CLASS/Halofit controls

Pass12632 (\`analysis/PASS12632_HALOFIT_SCF_BUG.md\`) disclosed a serious model-dependent nonlinear power error in the original CLASS scalar-field Halofit path. Earlier fading/KLT scalar-field shear predictions and the old S8 hybrid ranking are **withdrawn**; merely recomputing Shapley arithmetic on invalid original-model power spectra cannot repair them.

Reproduce original and patched scalar-field controls against ordinary \(\Lambda\)CDM across \(z=0.01,1\) and \(k=0.1,1,3\;h/{\rm Mpc}\). The patched scalar-field path matches the ordinary \(\Lambda\)CDM Halofit boost to relative error below \(3\times10^{-6}\) at all six cells; the prepatch control drops to about 0.417 of the reference at \(k=3,z=0.01\). The existing training-fit archive shows fixed-parameter \(\Delta\chi^2<1.1\) across the listed models, which says **nothing** about unrerun nonlinear shear likelihoods.

**Fail-closed output:** The result certificate embeds the withdrawn file ledger and has \`fail_closed=true\`; there is **no refreshed DES/KiDS elpd, Bayes factor, or model-discovery claim**.

Independent external context: KiDS-Legacy extended cosmology, Reischke et al., *Astronomy & Astrophysics* **709 A82** (May 2026), https://doi.org/10.1051/0004-6361/202558581, finds no significant w0waCDM improvement over \(\Lambda\)CDM from shear+CMB lensing. This is not a validation or rejection of the repo's particular fading model.

## Reproduction and next research challenges

Run \`py -3 analysis/w33_20261108_five_physical_falsifiers.py\` and \`py -3 -m pytest -q tests/test_w33_20261108_five_physical_falsifiers.py\`.

**Five orthogonal next studies:** (1) design a *local gauge-covariant* 2-polarization continuum scaling of the 162-square augmentation; (2) identify gauge quotient and a radiatively stable phase-constrained E6 vacuum with anomaly-free Standard Model representations; (3) certify a global objective lower bound or find an exact flat q5 complex null-local Hamiltonian; (4) supply a physical controlled-SUM injection primitive compatible with the claimed single-photon resource and fault tolerance; (5) rerun DES and KiDS full-covariance shear likelihoods after the CLASS correction and independent inference checks.

**Provenance boundary:** Native graph and E6 arrays were reconstructed from source; optimizer is numerical; circuit is logical; CLASS audit is a replay of committed code outputs, not new CLASS likelihood execution or empirical cosmology discovery.
