# Next-five independent research: exact 270-mediator compiler, 24-variable genus-six gauge, D9 flux moment maps, F8 rank-five census, two-epoch photonic drift

**2026-11-15** · Main repository: `wilcompute/W33-Theory` · Scope: five orthogonal follow-ups plus a sixth pure-state resource theorem. These are rigorously checked finite constructions and conditional statistical models; they are **not** a full Theory of Everything or a derivation of observed particle physics.

Reviewed previous work through `22d86867f`: the W33 45 octets / Schläfli 27-line dictionary and full four-copy quantum operation (`4d217e7d5`); the eight-dimensional F8 near-tight integer SOS (`212d80effc`); genus-six planar-dual geometry and numerical searches. The current work adds new independent tests without altering those existing source files.

## 1. Full four-copy W33→E6 quantum map through 270 intermediate modes

**Producer:** `analysis/toe_20261115_E6_270mode_two_stage_compiler.py`. **Certificate:** `data/toe_20261115_E6_270mode_two_stage_quantum_compiler.json`.

Existing work constructed a \(27\times22680\) full-rank integer map \(M\) on distinct-four-rail bosonic basis states, with \(M M^T=1440I+24A_{27}+60(J-I-A_{27})\) and eigenvalues \(\{2640^{(1)},1344^{(20)},1560^{(6)}\}\). It did not give an operational decomposition.

Reconstruct **only from the previously saved 45 eight-ray octet supports** (no numpy, no networkx): all 780 W33 point pairs appear in either one or three octet supports. The 540 support-multiplicity-one pairs are precisely the nonadjacent point pairs; 12 belong to each octet. Every disjoint-octet pair is an edge in the 45-vertex \(\operatorname{SRG}(45,12,3,3)\), of which there are 270. Each such pair owns exactly one of 27 maximal five-clique cubic-line labels.

Define a binary intermediate map \(U\), shape \(270\times22680\), where \(U_{e,S}=1\) precisely when four-ray subset \(S\) splits into two nonadjacent point pairs belonging to the disjoint octets \(e=(i,j)\). Each intermediate row has 144 nonzeros; input-column support size is **one for 6,480 quartets**, **two for 16,200 quartets**. The exact matrix \(U U^T\) is \(144I_{270}+2A_{270}\), with \(A_{270}\) the adjacency of a **60-regular simple graph** on 270 modes, with 8,100 edges. Those edges connect *different* cubic-line fibers; each fiber of ten mediators is independent.

Because \(U U^T\) is positive semidefinite, nonnegative, and has constant row sum 264, its **maximum eigenvalue is exactly 264** (Perron and the maximum-row-sum bound; uniform vector attains it). Define \(B\), shape \(27\times270\), by setting \(B_{\ell,e}=1\) when the octet-pair mediator \(e\) belongs to cubic-line label \(\ell\). Each of the 27 rows has 10 ones, with no overlapping supports: \(B B^T=10I_{27}\). Integer enumeration verifies

\[
M=B U,\qquad K_1=\frac{U}{\sqrt{264}},\quad
K_2=\frac{B}{\sqrt{10}},\quad
K_2K_1=\frac{M}{\sqrt{2640}}.
\]

Both \(K_i\) are **individually contractive** Kraus success maps with canonical failure complements. Since the top singular vector of \(U\) is sent through the top singular vector of \(B\), the two-stage composition *saturates* the optimal one-step norm: **no additional abstract heralding penalty**. Stage two can be seen as 27 independent **10-input coherent combiners**, implementable on a hypothetical single-excitation 270-rail register by choosing the uniform output ports of 10×10 Fourier interferometers. Stage one is still a nontrivial quantum operation on four coherent photons; no passive-linear-optical / low-depth hardware compilation of \(K_1\) is claimed.

### An exact, perfectly transmitted entangled source

Each quartet has decomposition count \(m(S)=1\) or 2. The four-photon state

\[
|\Psi_*\rangle = \frac{\sum_{S}m(S)|S\rangle}{\sqrt{6480+4(16200)}}
=\frac{\sum_{S}m(S)|S\rangle}{\sqrt{71280}}
\]

has **no repeated-mode Fock amplitudes** and is therefore not \(|\psi\rangle^{\otimes4}\) for any one-photon state. It is the normalized right singular vector of \(K\) at singular value one, giving \(K|\Psi_*\rangle=|+_{27}\rangle\) and success probability **exactly one**. This is a *resource-state identity*, not free or efficient state preparation. For comparison, the prior uniform four-copy product input heralds at 19.8818%; random-phase and Haar averages are about 0.0138% and 0.0119%.

## 2. Genus-six dual: exact affine gauge reduction 36→24 parameters

**Producer:** `analysis/toe_20261115_genus6_affine24_exact.py`. **Certificate:** `data/toe_20261115_genus6_affine24_exact_certificate.json`.

The abstract neighborly \(K_{12}\) genus-six map is \(V=12,E=66,F=44\). Its face-complete dual is \(V=44,E=66,F=12\), with 12 planar eleven-gonal faces in any geometric realization. The previous plane ansatz \(z=a_i x+b_i y+c_i\) has **36** coefficients.

Four generic planes of an arrangement bound an affine tetrahedron, whose four triple-intersection vertices can be taken to \(0,e_1,e_2,e_3\) by a unique nonsingular affine change of variables. The reference planes become

\[
x+y+z=1,\qquad x=0,\qquad y=0,\qquad z=0.
\]

The remaining eight face planes are generically expressible as \(a_i x+b_i y+c_i z=1\): **24 free coordinates**, an exact quotient by the 12-dimensional real affine group. The integer incidence source `FACETS_ONE` is reused unchanged.

On the previously optimized 8-crossing candidate, the verifier performs all plane–vertex reconstructions and transformations with rational numbers parsed *exactly from their saved base-ten strings*; all 44 vertices map exactly, and all 12 individual face boundary cycles retain **eight** proper self-crossings. An affine equivalence preserves planar-face straightness and self-intersections, so the gauge fixing is mathematically lossless for generic embedded-polyhedron existence. It does **not** convert a failed candidate into an embedding.

Schewe (2010, https://arxiv.org/abs/0801.2582) **proved nonrealizability of the minimal triangulated genus-six primal**. Bokowski and Kevin H. (2025, https://www.mdpi.com/2073-8994/17/4/622) discuss unsuccessful geometric attempts for the **nontriangular dual**; primal nonrealizability does not itself imply dual nonrealizability. An exact SAT/interval/oriented-matroid attack on 24 canonical variables and global face intersections is now the next search.

## 3. D9 product \(S^2\times S^2\): all six magnetic isometry compensators

**Producer:** `analysis/toe_20261115_D9_flux_compensator_SO3xSO3.py`. **Certificate:** `data/toe_20261115_D9_SO3xSO3_flux_moment_maps.json`.

On a round sphere of radius \(r\), let \(n\in S^2\), \(\omega(u,v)=n\cdot(u\times v)\), and \(F=f r^2\omega\). For three standard rotations \(K_a=e_a\times n\), the **exact moment-map identity** is

\[
\iota_{K_a} F = d\mu_a,\qquad \mu_a=f r^2 n_a,
\qquad F(K_a,K_b)=\epsilon_{abc}\mu_c.
\]

It is checked using exact rational arithmetic on six points of \(S^2\), three rotations and tangent vectors at each point. The independent spheres give all six protected \(\mathfrak{so}(3)\oplus\mathfrak{so}(3)\) generators and the existing Maxwell \(u(1)\).

The geometric overlap factors on one \(S^2\) are

\[
\int_{S^2} K_a\cdot K_b\,dV = \frac{8\pi r^4}{3}\delta_{ab},\qquad
\int_{S^2}\mu_a\mu_b\,dV=\frac{4\pi f^2r^6}{3}\delta_{ab}.
\]

Multiplying by the second sphere's area gives the exact rational \(\pi^2\)-normalized coefficients in the certificate. Cross-sphere averages vanish. These are **gauge-kinematic/normalization constraints** needed by a genuine metric–Maxwell mixed KK calculation; they are not the physical full mass matrix. All six Killing modes must appear as protected massless gauge directions in the dynamically mixed spectrum.

## 4. F8: 148-code rank-five purity-structure falsifier

**Producer:** `analysis/toe_20261115_F8_rank5_logical_coset_census.py`. **Certificate:** `data/toe_20261115_F8_rank5_logical_coset_census.json`.

Using the repo's exact F8 multiplication and field trace, a fixed-seed randomized algorithm attempted 200 five-generator commuting Pauli subgroups whose entire nonidentity span lies *outside* the F8 regulus's 567 covered observables. **148 attempts completed rank five**. For every such subgroup, the 128-element symplectic centralizer splits into its subgroup and three logical-Pauli cosets of 32 elements each. Their covered-observable counts are exactly **(3,3,3)** for all 148 tests.

This strongly supports—but does **not** exhaustively prove—the structural conjecture that every uncovered rank-five subgroup has equal three-three-three logical weights. Each verified code inherits the exact encoded-qubit purity law \(C(\rho)=6\operatorname{Tr}(\rho^2)-3\) for states confined to its two-dimensional eigenspace, once the matrix trace-dual basis convention is used.

The parallel Pass12674 exact degree-eight SOS bound \(64F\ge2.498508646\) applies to its specified eight-dimensional \(T\) code space and nearly meets the exact upper witness. **The pure-state global \(64\)-dimensional optimum remains unproved**; mixed-state zero-certainty examples do not disprove positive pure-state lower bounds.

## 5. Photonic calibration: two-epoch drift impossibility and qualified remedy

**Producer:** `analysis/toe_20261115_photonic_two_epoch_drift.py`. **Certificate:** `data/toe_20261115_photonic_two_epoch_drift_certificates.json`.

The prior observable-specific calibration needs 16 rail contrasts rather than all 256 detector-matrix elements. This pass exposes an important failure mode: choose a detector confusion matrix equal to identity at times \(t=0\) and \(t=1\), but replace one column by a smooth one-rail shift of strength \(\sin^2(\pi t)\). All endpoint calibrations are perfect; at \(t=1/2\) one rail's detector contrast is **wrong by 1**. There is **no endpoint-only statistical confidence guarantee** without known temporal regularity.

If each true contrast \(\mu_j(t)=w^T C(t)[:,j]\) obeys an independently calibrated curvature condition \(|\mu_j''(t)|\le M\) over a normalized observation interval \([0,1]\), linear interpolation between two independent full-contrast calibrations obeys

\[
|\mu_j(t)-[(1-t)\mu_j(0)+t\mu_j(1)]|\le \frac{M}{2}t(1-t)
\le M/8.
\]

Split failure probability 0.01 into .0025 for **32** simultaneous endpoint contrasts, .0025 for two parity-flip references, and .005 for the five witness means. The union-Hoeffding sample allocation with contrast precision \(r=.01\) produces **2,103,112 sufficient accepted calibrations**, including both parity references. Under an **illustrative, not measured** \(M=0.2\) curvature bound and the previously frozen synthetic five-setting witness, the conditional joint 99% fidelity lower bound becomes **0.9083843902**. This bound cannot be used for hardware until a validated curvature bound and a time-aligned reference-preparation protocol exist.

## Reproduction / independent regression

```powershell
py -3 analysis/toe_20261115_E6_270mode_two_stage_compiler.py
py -3 analysis/toe_20261115_genus6_affine24_exact.py
py -3 analysis/toe_20261115_D9_flux_compensator_SO3xSO3.py
py -3 analysis/toe_20261115_F8_rank5_logical_coset_census.py
py -3 analysis/toe_20261115_photonic_two_epoch_drift.py
py -3 -m pytest tests/test_toe_20261115_nextfive_270_gauge_F8_drift.py -q
```

There are five new producer/certificate pairs plus this report and a dedicated test suite. Exact checks are distinguished from randomized F8 sampling and simulated/calibration-assumption-dependent photonic statements. Existing repo source, papers, and parallel worktree files are untouched.

## Five nonsequential high-value next research experiments

1. **Photon multiphoton compiler:** Synthesize sparse stage-one \(U:\operatorname{Sym}^4(\mathbb C^{40})\to\mathbb C^{270}\) from elementary gates or a linear-optics-plus-measurement architecture. Determine whether its exact 60-regular mediator graph is exploitable as a local circuit and bound entangled-state-preparation resources.
2. **Genus-six realizability:** Formulate exact plane-order sign/interval constraints in the 24-dimensional canonical gauge for each of 59 abstract dual maps; a zero local crossing penalty is only one necessary step.
3. **D9 fluctuation theory:** Use the explicit \(\mu_a\) basis to gauge-fix the coupled vector sector, prove six exact null eigenvectors, and compute all massive/ghost spectra with flux quantization rather than trusting raw Hodge eigenvalues.
4. **F8 exact classification:** Prove or falsify the all-uncovered-rank-five \((3,3,3)\) coset theorem by exhaustive orbit reduction and leverage it toward a purity-aware global optimality bound.
5. **Drift-aware photonic experiment:** Independently measure the second-derivative or Lipschitz calibration envelope and implement time-interleaved rail-reference shots, with a real optical fidelity threshold rather than a synthetic example.
