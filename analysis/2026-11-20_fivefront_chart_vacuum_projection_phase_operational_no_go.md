# Five follow-through gates: stable 45-chart action, exceptional projection obstruction, parity tomography, coherent phase, and continuum collapse

**Date:** 2026-11-20 (America/New_York). **Status:** 28/28 focused tests verified on the Windows research checkout. All conclusions are finite mathematical constructions or explicitly specified statistical/hypothetical models. **No completed TOE, experimental quantum advantage, measured photonic hardware result, anomalous chiral spectrum, Lorentzian Einstein dynamics, or unfitted Standard Model prediction.**

Producer: [toe_20261120_nextfive_falsifiers.py](toe_20261120_nextfive_falsifiers.py). Tests: [test_toe_20261120_nextfive_falsifiers.py](../tests/test_toe_20261120_nextfive_falsifiers.py). Frozen JSON: [toe_20261120_nextfive_falsifiers.json](../data/toe_20261120_nextfive_falsifiers.json).

## Provenance and what is genuinely new here

**Existing repo ownership:** Pass11177 already constructs the 45 symplectic two-qutrit factorization charts and identifies the chart disjointness graph with GQ(4,2), SRG(45,12,3,3). Pass11657 already identifies those 45 charts with Burkhardt/Hesse mirror nodes; Pass11681 already knows 240 E8 root restrictions to 40 projective Witting rays. Pass11663 establishes the odd two-qutrit representation of Witting rays. Previous November 20 work already computes 45×40 purity, the unique noncommuting-pair conditional frame selection, octonionic H(3), displaced Wigner parity, and the 40-reflection commutant no-go. Prior October 9 and November 18 reports already discuss naive graph continuum failure. None of these are claimed new.

**Independent incremental work:** (i) construct and certify a *symmetry-invariant incidence-derived quartic chart potential*, its exact degenerate minima, amplitude fluctuation coefficients and conditional thermal source gap; (ii) exhaustive search over all 1,093 natural 7-to-6 projective projection centers for the Q(6,3) source model; (iii) prove that discarded-label randomized Wigner readout is a classical garbling of direct parity, with exact 40x variance cost and valid size/power shot analysis; (iv) distinguish the six E8 scalar lifts from actual coherent relative-phase preparations, with exact PGM copy-success; (v) independently quantify the preexisting bounded-diameter/spectral dimension obstacle using the Gromov–Hausdorff diameter inequality.

## 1. Constructive 45-chart incidence action and symmetric vacuum-selection limit

Let \(\mathcal F\) be the 45 unordered orthogonal symplectic-plane decompositions \(V=\mathbb F_3^4=P\oplus P^\perp\). Let \(M_{Fv}=1\) iff \(v\) lies in one of the two four-ray factor planes; \(M\) is a **45×40 binary matrix** with row sum 8, column sum 9, real rank 25. Its Gram matrix \(K=MM^\mathsf T\) has

- \(K_{FF}=8\);
- distinct-chart intersections \(K_{FG}=0\) for 270 unordered pairs, \(K_{FG}=2\) for 720;
- spectrum \(72^1,12^{24},0^{20}\);
- the known GQ(4,2) disjointness graph SRG(45,12,3,3).

Introduce **new, explicitly postulated** normalized complex chart amplitudes \(\psi_F\), \(p_F=|\psi_F|^2\ge0\), \(\sum_Fp_F=1\), and a positive coupling \(J\). The geometric *quartic in amplitudes* toy action is

\[
V(\psi)=-\frac J2\,p^\mathsf T Kp
=-\frac J2\sum_{v=1}^{40}\left(\sum_F M_{Fv}|\psi_F|^2\right)^2.
\]

It is invariant under every symmetry permuting the W33 rays and 45 tensor charts compatibly. Because off-diagonal entries of \(K\) are at most 2,

\[
p^\mathsf TKp\le 8\sum_Fp_F^2+2\sum_{F\ne G}p_Fp_G
=2+6\sum_Fp_F^2\le8,
\]

with equality iff one \(p_F=1\). Consequently the **entire global minimum set** is 45 symmetry-related pure-chart sectors, modulo their individual global phase, each of energy \(-4J\). The uniform state has energy \(-0.8J\). For a fixed vacuum \(F\), the normalized amplitude perturbations \(\psi_G=\epsilon\), \(G\ne F\), have

\[
V-V_F=J(8-K_{FG})|\epsilon|^2+O(|\epsilon|^4).
\]

Thus the 44 nonselected modes have **positive quadratic coefficients \(8J\) with multiplicity 12 and \(6J\) with multiplicity 32**. These are *toy curvature coefficients*, not physical particle masses or canonically normalized Hessian eigenvalues.

The previous externally specified **noncommuting-ray pair** gives a diagonal conditional 45-chart Hamiltonian with energies \(0^1,(1/2)^{16},1^{28}\), gap \(1/2\). A commuting pair gives \(0^3,(1/2)^{12},1^{30}\). Each of the 45 charts is selected by exactly 12 of the 540 noncommuting pairs. At inverse dimensionless temperature \(\beta=10\), the conditional selected-chart Boltzmann weight is

\[
P_\star=[1+16e^{-5}+28e^{-10}]^{-1}=0.90164955\dots.
\]

By eigenvalue perturbation theory, an additive Hermitian perturbation of operator norm strictly below \(1/4\) cannot close this conditional gap.

**Interpretation:** a mathematically clean **symmetric, degenerate spontaneous-selection candidate**, not a uniquely derived local relativistic field action. Its 45-chart field, coupling \(J\), physical spatial locality, gauge constraints and quantum dynamics are assumptions still to justify. A finite system with symmetry-preserving tunneling need not settle in one classical minimum.

## 2. Exact projective obstruction to the naive \(G_2(3)\rightarrow\) three-qutrit map

The natural 364-point hexagon model is a projective null quadric \(Q(6,3)\subset PG(6,3)\), represented by seven field coordinates with quadratic norm \(-a^2-u\cdot v\). The projective three-qutrit Pauli direction space is \(PG(5,3)\), also 364 points.

A rank-six **linear** map \(\mathbb F_3^7\to\mathbb F_3^6\) is projective quotient by one projective kernel point \(w\). Exhaustively enumerate all 1,093 potential \(w\):

| Kernel center type | Centers | Image behavior for the 364 quadric points |
|---|---:|---|
| isotropic | 364 | undefined at \(w\), a source point |
| anisotropic norm one | 351 | 238 distinct images, 112 singletons + 126 doubletons |
| anisotropic norm two | 378 | 247 distinct images, 130 singletons + 117 doubletons |

Every possible linear quotient either is undefined at a source point or identifies at least 117 pairs of distinct source points. This is a **complete no-go for linear projection of this natural coordinate model**. It is *not* a no-go for every possible nonlinear incidence map, arbitrary re-embedding, or operator representation. The natural H(3) quadratic space and the known even-characteristic perfect symplectic embedding are different structures; see GAP FinInG and classification literature.

## 3. Randomized Witting-40 measurement has a 40-fold ideal variance penalty

For the previous all-directions two-qutrit eigenvalue-**one** projector protocol, averaging the binary 'phase 0' acceptance effect over 40 settings produces

\[
E_{\mathrm{yes}}=\frac{13I+3P}{40}
=0.40\,P_{\mathrm{even}}+0.25\,P_{\mathrm{odd}}.
\]

This binary POVM is **exactly simulated by ideal displaced parity** followed by a classical binary randomization: accept with probability 0.40 conditional on even and 0.25 conditional on odd. It is therefore Blackwell-dominated by direct parity measurement for that *aggregated single-coordinate task*. This conclusion **does not hold when the selected setting \(v\) and full three-valued Pauli outcome are retained**; the full 120 ticks can reconstruct more.

At two-qutrit \(\rho=I_9/9\), the parity expectation is \(\mu=1/9\), the aggregated acceptance probability is \(p=1/3\). Estimating \(\mu=(40p-13)/3\) from binary samples has variance coefficient \((40/3)^2 p(1-p)=3200/81\) per trial. Estimating \(\mu\) from \(\pm1\) parity outcomes has variance coefficient \(1-\mu^2=80/81\). The **exact ratio is 40**. Since the target Wigner coordinate is \(\mu/9\), its variance ratio is also 40.

**Correction to earlier 410-shot shorthand.** A Hoeffding calculation of 410 for gap \(13/40-1/4=0.075\) controls just an alternative-side tail at the *null mean*, not both the false-positive rate and power. For the simple ideal hypotheses \(\mathsf H_0:p\ge0.325\), \(\mathsf H_1:p=0.25\), a deterministic lower-count binomial test needs **791 accepted/detected binary trials** for a 1%-size and 99%-power target: reject if at most 226 yes outcomes; exact false-positive 0.00958470899, power 0.9901453594. If boundary decisions may be randomized, the Neyman–Pearson calculation reaches this goal at **785 trials**. A conservative midpoint Hoeffding guarantee for both errors below 1% requires **1,638 trials**. In the ideal pure parity-odd alternative, direct parity is deterministically negative; **seven** independent negative outcomes yield false-positive probability at most \(2^{-7}<.01\) and power one.

These are **ideal detected-shot** comparisons, not losses/efficiencies, hardware resource costs or composable QKD security. The direct parity is a tensor product of single-qutrit parity observables, but experimental architecture can make it harder than local Pauli readout.

## 4. The six E8 root phases require genuinely new coherent data

In the preexisting E8 root → projective Witting ray map, six unit scalars above a ray give identical rank-one projectors. No amount of measuring the ray alone distinguishes the six labels; equal prior guessing success is \(1/6\).

For a **hypothetical new physical encoding**, introduce an external coherent reference and six *distinct* equatorial control-qubit states

\[
|\chi_k\rangle=(|0\rangle+e^{2\pi i k/6}|1\rangle)/\sqrt2.
\]

Their \(n\)-copy Gram matrix has six eigenvalues

\[
\lambda_r(n)=\frac6{2^n}\sum_{j\equiv r\;(\mathrm{mod}\;6)}{n\choose j},
\quad r=0,\ldots,5,
\]

and a square-root/pretty-good measurement with success

\[
P_{\rm PGM}(n)=\frac1{36}\left(\sum_{r=0}^5\sqrt{\lambda_r(n)}\right)^2.
\]

Verified against explicitly constructed complex Gram matrices for \(n=1,\ldots,5\). \(P_{\rm PGM}(1)=1/3\), \(P_{\rm PGM}(2)\approx0.4857022604\), and \(P_{\rm PGM}(14)\approx0.9909582654\); **14 is the first copy count above 99% for this encoding and measurement**. No finite \(n\) gives exact zero error because adjacent phase states have nonzero overlap \((\sqrt3/2)^n\).

This is an explicit **resource accounting distinction**: the coherent relative-phase control encodes new observable information. It does not extract a global phase from the projective Witting state, nor prove that the six E8 root phases are physically available coherent control variables.

## 5. No-go for the naive finite polar-graph-to-Lorentzian spacetime continuum

**Important prior-art warning:** the repository already analyzed finite graph Laplacian spectral dimension and bounded-distance obstacles (Oct 9 and Nov 18). The present result is an independent Gromov–Hausdorff lower-bound calculation, not a first discovery.

Point-collinearity graphs of \(W(3,q)\) have diameter two; those of \(H(q)\) have diameter three. Give each adjacency edge a physical length \(\ell_q=1/q\). Their entire graph-metric diameters are therefore \(2/q\) and \(3/q\), tending to zero. For any compact unit-diameter continuum metric space \(X\),

\[
d_{GH}(G_q,X)\ \ge\ \frac12|\operatorname{diam}(G_q)-1|
\ \longrightarrow\ \frac12.
\]

Therefore the *unmodified point graphs with shrinking edge length* cannot converge to a nontrivial unit-diameter four-dimensional Riemannian manifold. The observed spectra also show why a transient heat-trace 'dimension' is not an actual continuum dimension. For W33 its peak running dimension is about 3.718; for the 364-point hexagon it is about 5.826, both scale-dependent and tending back to zero at long times.

This does not rule out weighted/refined/nonlocal causal geometries, a new building complex with growing graph diameter, or fundamentally Lorentzian order structures. Any valid continuum proposal must give its metric/causal construction, graph refinement map, propagating modes, gravitational action and explicit convergence tests.

## Execution and reproducibility

    python analysis/toe_20261120_nextfive_falsifiers.py
    python -m unittest discover -s tests -p test_toe_20261120_nextfive_falsifiers.py -v

**28/28 focused tests passed on the authorized Windows research worktree after the corrected statistical update.** A separate self-contained sandbox implementation passed 27/27 tests, and earlier code covers 20 further baseline tests. Re-run the 20 baseline tests before claiming a combined suite status. No instrumentation/measurements of real physics are used.

## Current research decision

The best *constructive* direction is the chart incidence quartic: it generates stable local order-parameter vacua without naming a preferred Pauli pair. The key obstruction is that nothing in the present theory derives a spacetime-local degree of freedom carrying \(\psi_F\), a natural coupling \(J\), or a dynamical transition to relativistic matter. The G₂ quotient and E₈ scalar-phase shortcuts fail, while the Wigner-readout cost comparison gives an immediate experimentally relevant architecture choice.

### Five orthogonal next experiments

1. **Microscopic dynamics:** derive a local, gauge-consistent origin of the 45-chart condensate from an operator Hamiltonian, test domain walls, spectral gap and a real thermodynamic limit; no tuning of source pairs by hand.
2. **Exceptional bridge:** search for a nonlinear G₂ incidence embedding or an intertwiner into a suitable qutrit-operator/higher-tensor module, keeping quadrics/alternating forms and automorphism representations distinct.
3. **Operational optical benchmark:** perform detector-calibrated direct parity vs full 120-outcome Pauli/Witting tomography with a shared shot/energy budget, including SPAM, loss, setting identity and adversarial reporting.
4. **E₈ amplitude transport:** construct a precise physically controlled coherent channel with a reference clock, then test whether root-phase information is dynamically accessible or merely a basis gauge.
5. **Continuum theory:** construct a sequence of 4D-local complexes with growing combinatorial diameter and a Ward-consistent Lorentzian kinetic operator; independently audit chiral anomalies and one preregistered parameter-free prediction.

## External research checks

- Vlasov, *Scheme of quantum communications based on Witting polytope* (2025): https://arxiv.org/abs/2503.18431
- GAP FinInG, split Cayley hexagon embeddings: https://gap-packages.github.io/FinInG/doc/chap12_mj.html
- Low-dimensional hexagon embedding classification: https://doi.org/10.1112/jlms/54.3.566
- Bartlett–Rudolph–Spekkens, reference frames: https://doi.org/10.1103/RevModPhys.79.555
- Gross, odd-dimensional discrete Wigner: https://arxiv.org/abs/quant-ph/0602001
- Buscemi, statistical-model sufficiency: https://doi.org/10.1007/s00220-011-1402-5
- Coolsaet–Degraer–Spence, SRG(45,12,3,3): https://www.combinatorics.org/ojs/index.php/eljc/article/view/v13i1r32
- Mean-field Potts symmetry-breaking analogy: https://www.math.ucla.edu/~lchayes/lchayes_website_folder/old_publications_folder/bc_mft.pdf

