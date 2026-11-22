# Five experimentally motivated W33 falsifiers from an open-ended November 2026 literature search

**Date:** 22 November 2026. **Starting baseline:** wilcompute/W33-Theory at b16296299a2b1add941a81b15d0f4eca94d9db54. **Executable**: analysis/toe_20261122_experiment_driven_five_fronts.py. **Regression suite**: tests/test_toe_20261122_experiment_driven_five_fronts.py (20 tests). **Producer's JSON**: data/toe_20261122_experiment_driven_five_fronts.json. **Frozen independently calculated summary**: data/toe_20261122_experiment_driven_fivefronts_frozen.json. **Workflow**: .github/workflows/witting-experimental-fivefronts.yml.

## How the research directions were selected

Rather than follow the preceding sequence of optical mesh optimizations, the search began with broad 2025–2026 experiments in photonic contextuality, high-dimensional Bell nonlocality, indefinite causal order, Z2 gauge interference and non-Hermitian topology. This yielded five *different operational observables* to compare with W33/Witting finite geometry. A second search followed the causal-inequality loopholes, the binarization loophole, semi-device-independent randomness certification and the photonic Klein bottle. Then the existing repo was searched to prevent rediscovery.

Relevant prior repo material and differences:
- analysis/toe_20261120_symplectic_order_sic_switch.py already uses a quantum switch for **qutrit Pauli operators on W(3,3)**; the new experiment uses **ququart Householder reflections of all 40 actual Witting rays** and proves a pairwise **chirality-blindness** limitation.
- analysis/toe_20261104_contextuality_compatibility_detection_budget.py already identifies why one-hot single-photon detector parity without operational context equivalence does **not** certify contextuality; the new test computes **raw and chart-conditioned min entropy under Witting detector coarse-graining**.
- analysis/w33_pass4403_4405_magnetic_w33.py already threads magnetic phases through the W33 graph and computes its spectrum; the new test builds an explicit **two-arm, local-gauge-invariant readout** of a loop's Wilson sign.
- Previous 25-bin ray-detector Pareto work optimizes chart privacy/Fisher efficiency. The new test applies **a true two-party, 40-outcome, maximally-entangled-ququart POVM** and measures how that same detector grouping destroys correlations. It does not assume that correlation is a Bell violation.
- Earlier Császár/Szilassi toroidal and maniplex-topology work concerns *orientable* surfaces. The new 6×6 and 8×8 Klein controls provide a **nonorientable double-cover and orientation-holonomy negative control**; they do not equate Klein square grids with those polyhedra.

### Experiment 1 — 2026 indefinite causal-order Bell-like experiments ⇒ a Witting reflection switch

Published comparator: *Experimental violation of a Bell-like inequality for causal order*, Science Advances (2026), https://doi.org/10.1126/sciadv.aee2912, which reports an experimental Bell-like causal-order inequality violation using photonic time bins and long fiber delay, but explicitly notes that the demonstration is not device-independent or loophole-free. Background: an integrated generalized multidimensional quantum switch, PRL 135, 160202 (2025), https://doi.org/10.1103/39vh-84n1.

**New Witting test:** For each normalized Witting ray v_i define the unitary reflection U_i=I4−2P_i, P_i=|v_i><v_i|. Prepare a control in |+>, an independent maximally mixed ququart target rho=I4/4, and coherently apply U_i U_j or U_j U_i in the two control branches. The antisymmetric-control probability is

p_minus(i,j) = ||[U_i,U_j]||_F²/(4*4) = 2 r_ij(1−r_ij), with r_ij=Tr(P_iP_j)=|<v_i|v_j>|².

The 780 unordered pairs of the Witting 40-ray system split into **240 orthogonal pairs** with r=0 and p_minus=0, and **540 nonorthogonal pairs** with r=1/3 and **p_minus=4/9**. Exact 4×4 matrix calculations agree to at most 4.45e-16. A control-coherence factor 0<=v<=1 gives p_minus(v)=(1−v)/2+v p_minus(1), a useful distinguishable dephasing control.

**Negative result:** Complex conjugation of every ray leaves every r_ij unchanged. Thus this two-reflection protocol **cannot** detect the oriented Witting triangle/Bargmann phases, even though the latter carry additional information. It only reads pairwise incidence and coherent-order interference. **It does not violate a device-independent causal inequality, prove retrocausality or reconstruct spacetime.**

### Experiment 2 — Photonic contextuality-certified randomness ⇒ an exact four-bit entropy tradeoff

Published comparator: Genzini et al., *On-Chip Semi-Device-Independent Quantum Random Number Generator Exploiting Contextuality*, PRX Quantum 7, 033022 (4 August 2026), https://doi.org/10.1103/62lv-gmsz. They report KCBS contextuality violation and **0.077±0.002 bits of *certified* conditional min-entropy** per qutrit-chip round, under their specified SDP and semi-device-independent assumptions.

**New Witting calculation:** Choose a hidden Witting chart z uniformly among45 and uniformly select one of its8 included rays. Every ray occurs in nine charts, so the 40-outcome marginal is p(i)=1/40. Its **raw observed classical** min-entropy is log2(40)=5.321928 bits. Given the chart z but no ray outcome, each of8 labels is equally likely, giving classical conditional min-entropy exactly3 bits.

For a detector that individually resolves 24 of40 ray labels and pools the other16 in a single coarse outcome, the pooled event has marginal probability16/40=0.4. Thus the maximum outcome probability increases by factor16, and **raw min entropy decreases by exactly log2(16)=4 bits** to log2(2.5)=1.321928 bits. For each of the three studied 25-bin layouts, the coarse bin also dominates the conditional per-chart guessing probability, giving the same 1.321928 bits with chart identity known.

**Critical caution:** These are CLASSICAL distributional min-entropies and nothing more. Against adversaries holding an exact outcome copy, the min entropy is zero. Neither a Witting noncontextuality inequality nor semi-DI adversarial quantum side-information bound was established by these data. In particular, 1.321928 **must not** be presented as certified random bits, or directly compared as a security rate to the PRX experiment's 0.077±0.002.

### Experiment 3 — Four-dimensional Bell binarization-loophole closure ⇒ a genuine 40×40 outcome test

Published comparator: *Binarization-Loophole-Free Observation of High-Dimensional Quantum Nonlocality*, PRL 136, 240201 (16 June 2026), https://doi.org/10.1103/ydch-vgmy. The experiment uses true four-dimensional photonic path-mode entanglement and multioutcome detectors, avoiding the **unjustified replacement of one multioutcome measurement by independently configured binary tests**. The loophole is analyzed in https://doi.org/10.1103/PhysRevA.111.042433.

**New Witting test:** For a fixed maximally entangled ququart pair |Phi4>=(1/2)sum_a |a,a>, measure Alice with the full40-outcome POVM E_i=P_i/10 (because sum_i P_i=10 I4), and Bob with F_j=conjugate(P_j)/10. Their exact normalized joint probability is

p(i,j)=Tr(P_i P_j)/400.

The 1600 entries are completely fixed by ray overlap: 40 diagonal pairs have overlap1, 1080 ordered nonorthogonal offdiagonal pairs overlap1/3, and 480 pairs overlap0. Because the marginals are uniform1/40, their **one-setting classical mutual information** is

I(A;B) = 0.2 + 0.9 log2(4/3) = **0.57353374935 bits**.

Coarse-graining both sides with the Witting 24-singleton-plus-16-pool detector gives:

| Measurement | Alice–Bob mutual information |
|---|---:|
| Full40×40 | 0.573534 bits |
| Older25×25 | 0.234500 bits |
| Newer Fisher/privacy Pareto25×25 | **0.223422 bits** |
| One-shot chart-minimum-leakage25×25 | 0.223961 bits |

A detector optimized to leak less information about the hidden chart can also preserve **less information about a bipartite quantum state**. This is an example of a task-dependent measurement tradeoff under the data-processing inequality.

**Essential negative control:** One fixed joint setting always admits the trivial local-hidden-variable construction lambda=(i,j) distributed as p(i,j), with deterministic local outputs. **Absolutely no Bell inequality is violated or excluded by these one-setting correlations.** Actual DI nonlocality requires multiple choices of settings, simultaneous multioutcome readout, loss controls and a specified inequality. **Coarse-graining a genuine simultaneous 40-outcome measurement is *not itself* the specific “binarization loophole”;** that loophole comes from treating uncharacterized separately configured binary measurements as one joint measurement.

### Experiment 4 — Dynamical Z2 Aharonov–Bohm physics ⇒ a local-gauge-invariant W(3,3) graph interferometer

Published comparator: *Aharonov–Bohm interference in a Z2 lattice gauge theory on a hybrid qubit–oscillator quantum computer*, Nature Physics 22, 1565–1571 (October 2026), https://doi.org/10.1038/s41567-026-03400-6. It measures real gauge-dynamical flux/charge interference on a hybrid ion device, not just a static graph phase.

**New W33 test:** Use the 40 isotropic points of W(3,3) with the canonical GF(3) symplectic collinearity graph, degree12, **240 edges** and graph cycle rank240−40+1=**201**. Every one of the540 nonadjacent pairs has four common neighbors. Select the four-cycle **0→36→9→37→0**, and give each edge a static Z2 link U_uv∈{−1,+1}. Two equal-amplitude paths from0 to9 have products a1=U_0,36 U_36,9 and a2=U_0,37 U_37,9. Their interference in a balanced final beam splitter yields

P_plus = |a1+a2|²/4 = (1+W)/2, W=a1*a2=U_0,36 U_36,9 U_9,37 U_37,0.

With W=+1: P_plus=1; with W=−1: P_plus=0. We applied **400 independent randomized local Z2 gauge transformations** g_uv→s_u g_uv s_v to positive and negative flux configurations and obtained zero change to either the Wilson sign or the interference probability.

**Boundary:** Graph cycle rank201 is NOT the topology/genus of a spacetime or surface. The links are assigned static classical signs; no Gauss-law-constrained matter/gauge evolution, dynamical flux entanglement or actual ion experiment is reproduced. This differs from prior repository magnetic-spectrum work by introducing an **operational readout that explicitly cancels local gauge-frame choices**.

### Experiment 5 — Photonic nonorientable exceptional topology ⇒ an orientability negative control

Published comparator: *Non-Hermitian exceptional topology on a Klein bottle photonic circuit*, Light: Science & Applications 15, article390 (October 2026), https://doi.org/10.1038/s41377-026-02516-x, and *Counterintuitive collision of exceptional points on nonorientable manifolds*, Nature Communications (2026), https://www.nature.com/articles/s41467-026-76508-1. Their exceptional-point and Fermi-arc phenomena arise in **non-Hermitian devices**, not in an ordinary graph adjacency matrix.

**New finite negative control:** Construct L×L square grids with identical vertex count L², 2L² edges, degree4. The orientable torus has horizontal and vertical periodic identifications. The nonorientable Klein analogue has a reflected vertical seam: (x,L−1) is identified with (L−1−x,0). The gluing induces a Z2 orientation-transition sign −1 around a loop traversing that seam once. Its genuine connected **double cover**, checked explicitly with a sheet-exchange automorphism, has 2L² vertices. A torus control has orientation holonomy+1.

| L | Torus minimum adjacency eigenvalue | Klein minimum eigenvalue | First odd-length Klein closed walks |
|---|---:|---:|---|
| 6 | −4 | −3.732050808 | 336 walks of length7 |
| 8 | −4 | −3.847759065 | 576 walks of length9 |

For these even-period toroidal grids, all odd closed-walk counts vanish because the graph is bipartite. The particular Klein discretizations possess orientation-twisted odd loops, so their spectra differ despite matching degree/counts. **Odd graph cycles are NOT in general equivalent to nonorientability**: these values depend on the chosen lattice and size, whereas the Z2 orientation cocycle concerns gluing topology. Nor do these real symmetric adjacency matrices reproduce exceptional points, laser amplification or non-Hermitian skin effects.

This gives an **orientability control** relevant to toroidal Császár/Szilassi hypotheses without claiming that either polyhedron *is* a square-grid Klein bottle.

## Synthesis: a five-layer observability hierarchy, not a TOE claim

These five external experimental advances expose **distinct invariants that the same finite mathematical substrate may or may not preserve**: (1) controlled operation order measures two-point overlaps but misses oriented phases; (2) marginal outcome unpredictability does not certify adversarial randomness; (3) single-setting bipartite correlations need not be nonlocal and are fragile to coarse grouping; (4) Wilson loops cancel local gauge-frame choices but static links alone do not make a dynamical gauge field; (5) orientation holonomy distinguishes nonorientable gluing from ordinary toroidal topology, beyond simple degree counts. The mathematical negative controls are essential. None is a measured W33 prediction or establishes a complete physical unification.

## Exact reproducibility and operational boundary

The full independent executable and its JSON output are available in the current conversation sandbox; the repository source and 20 new regression tests were committed through the GitHub connector. The independent sandbox executed the complete five-front producer and **all 20 tests passed**. The dedicated GitHub workflow was **queued**, not yet reported successful; therefore do not claim GitHub CI completion. Desktop Commander remained online but reported a hard **monthly call limit of zero**; one read-only attempt was rejected by the service, which explicitly instructs no retry or reconnect. The Windows working tree and parallel commits were not disturbed.

## Five independent strongest next research steps

1. **Full device-independent two-setting Bell falsifier.** Construct at least two physically implementable *joint* 4-outcome ququart analyzer settings per party from Witting bases, calculate a specific high-dimensional Bell inequality and detector-loss threshold, and compare against classical/local and lower-dimensional bounds. Do not repackage one-setting mutual information as a Bell violation.
2. **Phase-sensitive three-operation Witting switch.** Design an interferometric process genuinely sensitive to the signed imaginary Bargmann triangle product, unlike the pairwise reflection switch; test complex-conjugated and classical-dephased controls, with known experimental order visibility.
3. **Dynamic W33 gauge interferometry.** Couple the exact graph Wilson-loop readout to Gauss-law-respecting matter and quantized Z2 links, then predict AB interference visibility as flux becomes entangled and undergoes real-time dynamics.
4. **Adversary-aware Witting QRNG certification.** Develop a valid prepare/measure contextuality inequality with robust operational equivalence, no-click accounting, an SDP guessing-probability bound against side information and finite-key extraction. Only then quote secure bits.
5. **Synthetic nonorientable optical topology.** Build a manufacturable Klein-twisted Witting/Császár-related voltage-cover interferometer, test orientation reversal with phase-sensitive transport and identify whether non-Hermitian exceptional topology survives realistic loss and exceptional-point perturbations. Preserve an orientable torus control.

**Bottom line:** The five experiments suggest *new falsification methodologies* for the W33 program. The math is verified; the leap from finite geometry to physical laws is emphatically still an open hypothesis.
