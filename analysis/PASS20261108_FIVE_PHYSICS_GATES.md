# Five physics gates: gauge dispersion, local clock, native E6 mass lifting, photonic magic, and cosmology evidence

**Date:** 2026-11-08. **Code:** analysis/w33_20261108_five_physics_gates.py. **Tests:** tests/test_w33_20261108_five_physics_gates.py. **CI:** .github/workflows/w33_20261108_five_physics_gates.yml. **Certificate:** data/w33_20261108_five_physics_gates.json. **Desktop validation:** 16/16 focused tests passed in a separate temporary directory, with the original dirty repo checkout untouched.

**Claim boundary:** These are independent finite mathematical results, conditional physical/EFT constructions, calibrated synthetic tests, and a re-audit of existing likelihood scores. None establishes a quantum theory of gravity, measured SM masses/couplings, a working physical photon, a built fault-tolerant photonic computer, or evidence for a completed TOE.

## 1. Full temporal-gauge-invariant finite Maxwell fixture — and why it does NOT yet make photons

Use the **native 27-vertex, 108-edge, 36-triangle** Forty Points complex with integral incidence B1 (27×108), B2 (108×36), B1 B2=0, B2^T B2=3 I36. Let A(t) be a spatial edge 1-cochain and A0(t) a temporal vertex 0-cochain. Define:

- E=dot(A)−B1^T A0.
- F=B2^T A.
- S=∫dt (||E||²−||F||²)/2.

Under the *time-dependent* gauge transformation A→A+B1^T chi(t), A0→A0+dot(chi), **both E and F are exactly invariant**. Variation with respect to A0 imposes Gauss's law B1 E=0. This is stronger than just checking invariance of the triangle-curvature term.

The Hodge decomposition is orthogonal:

\[
\mathbb R^{108}
=\underbrace{\mathrm{im}\,B_1^\top}_{26}
\oplus\underbrace{H^1}_{46}
\oplus\underbrace{\mathrm{im}\,B_2}_{36}.
\]

For the unmodified magnetic operator K=B2 B2^T=3 P_coexact, the exact eigenvalue census is **0^72 ⊕ 3^36**. After removing 26 gauge gradients, **46 harmonic coordinates have zero magnetic restoring force**, and 36 coexact coordinates all oscillate with frequency sqrt(3) in the chosen kinetic units. The 27 translation momentum fibers split (coexact,H1,gradient) into (4,0,0)^1, (2,1,1)^12, (1,2,1)^8, (0,3,1)^6.

**Falsification:** This natural local triangle Maxwell action does **not** generate two dispersing, gapless electromagnetic polarizations. A momentum-dependent physical field/polarization selection requires more than the static harmonic group decomposition. Adding a local kinetic operator, dynamical matter, a suitable continuum limit or a physically motivated reduction could evade this *specific model* obstruction. Gauge charge normalization, alpha, speed of light and photon dispersion remain entirely undetermined.

Previous owners: PASS20260924_HISTORY_COMPACTIFICATION_BREAKTHROUGH, PASS20261108_S4_HARMONIC_QDUAL, PASS20261108_STABILITY_HODGE_COMPLETION. The new piece is the **full temporal gauge transformation, Gauss constraint, and complete action-level frequency obstruction**, independently verified from the boundary matrices.

## 2. Strict-null-local Lorentz-covariant evolution: exact stability bound and adversarial q=5 search

Previous repository theorems have already shown that a **translation-invariant, strictly null-supported, SL2(q)-congruence-covariant Hermitian Hamiltonian H0** automatically commutes with the larger GL2(q) congruence action, and cannot become exactly flat for odd prime-power q>=5. The full affine bound is |e^{-itH0}_{0d}|<=2/q², while uniform amplitude would require q^-3/2.

A new **quantitative perturbation bound**, valid even if E is spatially nonlocal or breaks the symmetry, follows from Duhamel's formula. For H=H0+E, H0,E Hermitian, at nonzero t,

\[
|e^{-itH}_{0d}|\le\frac{2}{q^2}+|t|\,\|E\|_{\rm op}.
\]

Therefore **perfect flatness requires**

\[
\boxed{|t|\,\|E\|_{\rm op}\ge q^{-3/2}-2/q^2.}
\]

This is a nonzero *time-normalized lower bound* on departure from the fully symmetric strictly null-local baseline; it is not a local-Hamiltonian impossibility theorem for every anisotropic graph.

At q=5, the amplitude gap is approximately 0.00944271910, the probability gap at the selected output is 0.0016. As an independent *heuristic*, divide the 24 nonzero null displacements into six projective-direction classes of four and choose one independent real hopping weight per class. Eight deterministic BFGS starts over these six weights found a best mean-squared probability deviation ≈2.24261145×10^-5 and largest single-output probability deviation ≈0.02497025, from the target 1/125.

**Do not infer nonexistence from this search.** It neither proves a global minimum nor searches all complex hopping patterns, translation-broken operators, all optical routing strategies or all evolution times with a fixed independent normalization. The exact earlier SL2-covariant no-go remains the only rigorous exclusion within its hypotheses.

## 3. Native E6×SL3 81-state mass tensor: representation-covariant rank-three scalar candidates

The existing D-flat work defines a signed **1,620-record**, 81×81 alternating mass map M(Phi) of generic rank **78**, hence nullity three. Prior passes showed that a *single* nonholomorphic invariant bilinear B(Phi)=conj(Phi)conj(Phi)^T raises its rank to 79, and that arbitrary SVD-fitted rank-three corrections can in principle produce rank 81.

This pass asks a more physically structured question: **can three independently transforming scalar fields Xi_a, each in the same 81-dimensional unitary representation, contribute three separately invariant, rank-one, nonholomorphic EFT spurions?** The schematic operator is

\[
\sum_{a=1}^3 (c_a/\Lambda)
  (\Xi_a^\dagger \chi)(\Xi_a^\dagger\psi)+{\rm h.c.}
\]

where chi and psi are *distinct* matter multiplets with suitable conjugate Lorentz and other charges, subject to permissions not shown here. Under the declared compact common representation, each Xi_a†χ or Xi_a†ψ is an invariant inner product. The resulting matrix additions are B_a=conj(Xi_a)conj(Xi_a)^T.

The code reconstructs the actual M from the 1,620 records and uses a frozen deterministic set of three generic complex Xi_a vectors, without choosing kernel singular vectors. It obtains **mass matrix ranks [78,79,80,81]**. In contrast, repeating the same aligned Phi-derived spurion can only raise the rank to 79. This is a *constructive representation-covariant-form rank-three existence witness*, not a derived physical vacuum.

The full-rank synthetic determinant has phase ≈**−2.6672953 radians** for the declared arbitrary complex fields. This is an especially important adversarial control: **lifting all three modes does not automatically solve strong CP**. The 81×81 determinant is not the determinant of the observed SM up- and down-quark sectors, and its phase is **not** an observable theta-bar. No Standard Model branching, anomaly cancellation, dynamical scalar potential, D/F-flat vacuum, admissible EFT cutoff, CP-real ultraviolet completion or one-loop Nelson–Barr stability has been established. Those must be supplied before calling this a mass mechanism.

Prior owner: analysis/w33_20261001_dflat_cartan_mass_loop.py, especially its existing single-Phi dimension-five rank-one operator. Novelty relative to that owner is the explicit three-*independent scalar* rank census and the generic determinant-phase warning, not the invariant-inner-product idea.

## 4. The Gaussian clock's exact non-Clifford boundary: ninth-root qutrit phase and magic negativity

The higher-prime determinant Gaussian clock was shown in the prior PASS20261108_ODD_PRIME_CLIFFORD_COMPILER to be a **three-qudit Clifford circuit**. This front adds a directly specified non-Clifford resource familiar from the existing Forty Points Section 4:

\[
T=\operatorname{diag}(1,\zeta_9,\zeta_9^{-1}),\qquad
\zeta_9=e^{2\pi i/9}.
\]

Because x³≡x (mod 3), a cubic **third-root** phase ζ3^(x³) is just Pauli Z: it is **not magic**. A ninth-root cubic phase is different. Conjugation by T sends Pauli X to an operator whose maximum Hilbert–Schmidt overlap with *any* qutrit Pauli monomial is exactly **1/sqrt(3)**, not one; T therefore does not normalize the qutrit Pauli group.

Injected into a uniform qutrit state |+>, the nine-point discrete Wigner distribution has **three negative entries of approximately −0.0977094713**; its total L1 norm is **1.5862568277**, and its Wigner logarithmic negativity (mana) is

\[
\boxed{\mathcal M=\log \|W\|_1=0.4613770443489666.}
\]

This is a direct numerical instance of the **known** Gross finite-dimensional Hudson theorem (D. Gross, *J. Math. Phys.* 47, 122107 (2006), https://arxiv.org/abs/quant-ph/0602001), not a novel magic-resource theorem. It supplies a verifiable algebraic resource **outside** the stabilizer/Clifford class but is not by itself a proof that the implemented physical architecture is universal or fault tolerant.

As an explicitly *synthetic* optical calibration control, independent Gaussian phase errors with σ=0.05 radians on 27 rails give the exact mean process-fidelity formula F=1/27+(26/27)exp(−σ²). A frozen 4,000-sample simulation gives **0.9976115** versus the analytical **≈0.9975957**. This model deliberately omits correlated drift, two-mode routing, insertion loss, state-injection success probability, heralding, detector noise and error correction. It is not a fabricated experiment.

## 5. Adversarial KiDS/KLT audit: arithmetic reproduces, interpretation is conditional

Independent reproduction here means **reading original committed numeric certificates and recomputing their arithmetic**, not processing the raw KiDS/DES catalogues with an independent likelihood. Source files: analysis/toe_uv/scorecard.json, shear_ppd.json, shear_ppd_desy5.json, shear_ppd_kids_dovekie.json, klt2_check.json, klt2_scan.json, klt_fit.json, data/w33_pass12631_kids_heldout.json, and the prior Pass12631 interpretation.

The exact Dovekie-training score decomposition relative to ΛCDM is:

| Model | BAO/SN holdout | DES Y3 shear holdout | KiDS-Legacy shear holdout | Algebraic sum |
|---|---:|---:|---:|---:|
| Fading c<0 | +5.6943 | −0.4180 | −0.5532 | **+4.7230** |
| CPL | +5.4831 | −2.1221 | −3.0431 | **+0.3179** |

The fading-minus-CPL combined difference is **+4.4051**, composed of a 0.2112 BAO/SN difference, 1.7040 DES shear difference and 2.4899 KiDS shear difference. Crucially **neither fading model nor CPL exceeds ΛCDM on the individual DES/KiDS shear scores** under these specific tests. The fitted fading model performs *closer to ΛCDM* than CPL. Thus the relative ranking is stronger than the evidence for an absolute detection of evolving dark energy.

The scoring used only **20 truncated Fisher samples per model**; the committed aggregates do not provide calibrated standard errors of the elpd differences or the full DES/KiDS joint data covariance. The two surveys have some overlapping sky coverage. Treating their scores as independent terms is an approximation; the combined +4.7230 must not be promoted to a calibrated Bayes factor, p-value, sigma detection, or unconditional model discovery.

**A sharper audit finding:** Five small-f KLT runs in the record end in the same numerical **'root must be bracketed'** solver error, including f=0.05, 0.10, 0.12 (with repeated shooting variants). This is a root-finder failure, **not proof that no physical dark-energy solution exists** in this parameter regime. Existing successful samples at f=0.15, 0.20, 0.25, 0.50 have large differences in χ²; the code accurately reproduces the f=0.25 χ² control, but it does not establish a complete exclusion threshold or existence theorem. A failed numerical shooting method cannot do that alone.

The reported need for discrete protection Z_N with N~140 remains contingent on UV operator coefficients, field excursion, charges and allowed symmetry-breaking operators. No full discrete-anomaly cancellation audit is contained in these source aggregates.

**External context, distinct from this repo:** KiDS-Legacy's official extended-cosmology study (https://arxiv.org/abs/2512.11041) finds no significant improvement of w0waCDM over ΛCDM using shear plus CMB lensing; that result neither confirms nor refutes the repo's specific interacting dark-energy model because the likelihoods and parameterizations differ.

## Full five-front validation and top five independent next experiments

All five fronts executed through the actual desktop repository imports (gauge topology, signed E6 tensor and historical score data), while the analyzed source and tests ran **in a separate temporary directory** to avoid interfering with ongoing local staged and unstaged parallel work. **16/16 focused tests passed**. GitHub Actions independently runs those tests and regenerates a separate artifact; report GitHub CI as passed only after the workflow completes.

**Independent subsequent moves:**

1. **Dynamical Maxwell:** derive a local translation-covariant continuum scaling of B2B2^T with a dispersing pair of transverse polarizations, positive energies and an independently normalized charged-matter representation. Explicitly test against this pass's 46 flat/gapless and 36 equally gapped modes.
2. **Local quantum-walk search:** extend the q5 six-direction search to controlled complex Hermitian, translation-breaking and magnetic-cocycle models; couple optimizer upper bounds to certified algebraic lower bounds rather than treating random failed starts as no-go theorems.
3. **E6 vacuum and strong CP:** find a scalar potential that selects three independent allowed Xi VEVs while retaining anomaly-free SM multiplets; calculate radiative theta-bar and real CKM/PMNS and mass ratios rather than relying on rank alone.
4. **Photonic engineering:** specify a practical non-Clifford phase implementation, state-injection/heralding scheme, complete 27-port tritter regrouping and phase/loss budget; test the 729-channel probabilities and gauge-invariant phase plaquettes experimentally.
5. **Independent cosmology replication:** run full KiDS COSEBI and DES shear likelihoods with calibration uncertainties, calibrated posterior predictive standard errors and overlapping-sky cross covariance; independently test alternate shooting brackets and dark-sector discrete anomaly constraints.
