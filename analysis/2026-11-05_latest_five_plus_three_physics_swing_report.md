# November 5, 2026 — TOE research: five physical fronts plus three independent home-run attempts

**Science/evidence discipline.** All eight research fronts below are **computationally executed**, with explicit source code, numerical certificates, and scoped tests. None constitutes a complete Theory of Everything or a new experimentally confirmed law. Several underlying identities are textbook; their role here is to **falsify insufficient unified models** and expose missing dynamics. Numerical results are conditional on stated EFT and lattice assumptions.

**Git intake:** baseline \`6fdfcfefb0dcb5e9f78668b3e2a02d23b7849a68\`; master at intake \`b2431bb76dc1a0eeb464695b5da47f86d90d3d1c\`. The comparison had 14 new commits, 101 modified paths, and 22,372 added lines / 312 deleted lines. We inspected changed paths and key contemporary scientific notes, plus GitHub and external literature. This **does not** claim reading every one of the 101 modified files in full. The unchanged-inventory PQ determinant obstruction, native determinant-line torus regulator and full physical Yukawa equation are already authored in the recent parallel commits. The PQ-assisted trinification complete-multiplet candidate already reaches a two-loop putative crossing near \(3.5\times10^{16}\) GeV with conditional axion/UV caveats; this packet does **not** rediscover it.

## Executable research matrix

| Workstream | Producer | Certificate |
|---|---|---|
| 1. Covariant double-Abelian gauge matrix | \`analysis/toe_20261105_new_front1_abelian_matrix.py\` | \`data/toe_20261105_new_front1_abelian_coupling_matrix.json\` |
| 2. Calibrated causal manifoldness counterexample | \`analysis/toe_20261105_new_front2_causal_manifold_guard.py\` | \`data/toe_20261105_new_front2_causal_matching_no_manifold.json\` |
| 3. Local gauge-invariant many-body dynamics | \`analysis/toe_20261105_new_front3_z2_gauge_pairs.py\` | \`data/toe_20261105_new_front3_z2_gauss_pairs.json\` |
| 4. PMNS/flavor falsifier and \`m_ee\` bound | \`analysis/toe_20261105_new_front4_flavor_rank2.py\` | \`data/toe_20261105_new_front4_flavor_rank2_selection.json\` |
| 5. Two **gapless** species velocity locking | \`analysis/toe_20261105_new_front5_gapless_velocity_lock.py\` | \`data/toe_20261105_new_front5_gapless_velocity_locking.json\` |
| 6. Proton \`Z9\` selection + B−L compatibility | \`analysis/toe_20261105_new_swingA_z9_proton_rule.py\` | \`data/toe_20261105_new_swingA_z9_proton_quality.json\` |
| 7. Global quantum-information Page curve | \`analysis/toe_20261105_new_swingB_page_information.py\` | \`data/toe_20261105_new_swingB_page_information_transfer.json\` |
| 8. Dark-energy SN calibration + BAO & PPD audit | \`analysis/toe_20261105_new_swingC_de_calibration.py\` | \`data/toe_20261105_new_swingC_cosmology_calibration_guard.json\` |

Regressions: \`tests/test_toe_20261105_latest_five_plus_three_swing.py\`; execute \`python -m pytest -q --noconftest tests/test_toe_20261105_latest_five_plus_three_swing.py\`. Each fixture **recalculates all generators**; it cannot pass on outdated JSON alone. All eight independent producers also run standalone. The existing main repository checkout is dirty; work is restricted to the isolated existing \`C:\Repos\TOE-Next5-20261105\` worktree. Do not stage unrelated H27 archaeology work residing there.

## 1. Two-\(U(1)\) kinetic mixing: the complete matrix is the observable object

Use **noncanonical** kinetic terms
\[
\mathcal L_{\rm kin}=-\frac14F^T K F,\quad
K_{\rm UV}=\begin{pmatrix}g_Y^{-2}&0\\0&g_{BL}^{-2}\end{pmatrix}
\]
and charges coupling to the unrescaled gauge potential. The one-loop inverse kinetic matrix obeys
\[
\frac{dK}{d\ln\mu}=-\frac{B}{8\pi^2},\qquad
B=\frac23\sum_{\rm Weyl}n_f\,q_f q_f^T+
  \frac13\sum_{\rm complex~scalar}n_s\,q_s q_s^T .
\]
The Weyl inventory is **three SM generations plus three \(N^c\)**,
Higgs \(H\) and \(B-L=-2\) scalar \(S\), and one vectorlike
\((3,2)_{1/6}\) with \(B-L=1/3\), including its conjugate.

In **un-normalized physical hypercharge Y** rather than SU5-normalized
\(\sqrt{3/5}\,Y\), we find
\[
B_{Y,BL}=\frac{52}{9},\quad B_{BL,BL}=\frac{116}{9}.
\]
The code recomputes all fermion and scalar traces rather than copying
the previous certificate.

For the *illustrative, unbroken-basis* boundary
\(g_Y=0.36,g_{BL}=0.20\) at \(\mu_0=10^{10}\) GeV,
run to \(1.3163\times10^{15}\) GeV. The kinetic matrix stays positive
and its canonicalized off-diagonal ratio is
\(\chi_K=K_{12}/\sqrt{K_{11}K_{22}}\simeq-0.06956628\).
The value is **not a precision model prediction**: charges,
input \(g_{BL}\), mass matching and the kinetic convention are stated,
and the previous ~0.031 benchmark used a different leading-log
normalization and low-energy assumptions. Do not conflate them.

Under arbitrary nonsingular gauge-field coordinate changes
\(A=M A'\), the charges transform \(q'=M^T q\), while
\(K'=M^T K M\) and \(B'=M^T B M\).
The quantity \(q^T K^{-1}q\) is invariant; verified numerically
for nontrivial unimodular transformations and rescalings.
A vectorlike-threshold subtraction at the *separately fitted*
\(M_Q=2.1189\times10^7\) GeV gives an off-diagonal inverse kinetic
contribution \(\Delta K_{YBL}\simeq-0.1010\) over the stated
range; it is a formal isolated contribution, not a fully matched
broken-phase EFT.

**Open physical question:** implement a *simultaneously* two-loop
\(U(1)_Y\times U(1)_{B-L}\times SU(3)\times SU(2)\) RGE with all
thresholds, UV GUT field content, and proper broken-phase matching.
**Relevant prior art found during research:** Davidson & Gorbahn,
Phys Rev D114 055020 (11 Sep 2026),
https://doi.org/10.1103/cjy8-36vv derives two-loop
field-reparametrization-covariant running and invariants. The present
producer intentionally stops at the exact one-loop matrix and does
**not** claim to reimplement that paper's two-loop equations.

## 2. Causal spacetime: even a tuned global dimension-4 signature is insufficient

Compare genuinely **flat 4D Minkowski** Alexandrov sprinklings of 420
events against 420-event **metric-free transitive percolation** growth.
The *only* calibration target for the second is the fraction of
unordered event pairs which are causally related:
\[
r_4=\frac{\Gamma(5)\Gamma(2)}{2\Gamma(6)}=0.1.
\]
Tune the growth bond probability with independent calibration seeds,
then test on five **separate** seeds for each ensemble. The
calibration found \(p\simeq0.012656507\) with expected global relation
fraction \(0.100015\).

| Observable, 5 replicate mean/median | Minkowski-4 supplied | Metric-free percolation |
|---|---:|---:|
| Whole-poset causal relation fraction | 0.0978293 | 0.0945221 |
| Longest-chain mean | 7.4 | 12.8 |
| Interior-interval median dimension | 4.01270 | 2.20338 |

**Subtle finite-size bug found and corrected:** including the *two
already comparable interval endpoints* in the related-pair fraction
adds deterministic ancestor/descendant links, biasing the estimated
dimension toward low values. The first naive run gave about 2.93
even for the genuine supplied 4D sprinklings. Recomputing the
Myrheim-Meyer fraction using only the **interior interval events**
recovers 4.013 in the Minkowski control. The certificate retains the
naive estimates explicitly to prevent reintroducing this error.

This is a **counterexample to geometric reconstruction from one global
order invariant**, not a proof that transitive percolation is the
correct model or that a genuinely quantum causal action cannot select
\(d=4\). Reference: Rideout–Sorkin, Phys Rev D61 024002 (2000);
Meyer, Phys Rev D accepted Feb 2026,
https://doi.org/10.1103/klxp-f94q .

## 3. Gauge-invariant multiparticle dynamics beyond high-dimensional single photons

A four-site \(1+1\)D staggered-fermion \(Z_2\) lattice gauge theory,
three link qubits, total full Hilbert space \(2^7=128\).
Open-boundary Gauss constraints:
\[
G_j=(-1)^{n_j}X_{j-1,j}X_{j,j+1},\qquad
H=-t\sum_j(c_j^\dagger Z_{j,j+1}c_{j+1}+h.c.)
-h\sum_j X_{j,j+1}+m\sum_j(-1)^j n_j .
\]
All four \([H,G_j]\) are exactly zero. In the sector fixed by
staggered reference occupation \(1010\), link electric \(X=+1\):
- entire Gauss-invariant Hilbert space has **8** states;
- fixed bare occupation number 2 sector has **6** states;
- starting in reference staggered vacuum, exact evolution at \(t=0.5\)
  generates mean **0.615674** particle–antiparticle pair excitations
  relative to that sea;
- full-128D unitary evolution has gauge leakage below \(10^{-12}\);
- **removing the gauge-link \(Z\) from hopping** violates local Gauss
  law and yields leakage approximately **0.745964**.

This is a genuine local occupation-number/gauge transport experiment.
**Critical limitation:** bare fermion number remains conserved. Pair
production means particle/hole excitations relative to the staggered
Dirac sea; this is NOT producing 3+1D electrons and positrons from
the physical empty Fock vacuum, no continuum QED proof. Prior art
includes staggered lattice gauge simulations:
Nature Phys 2025 https://doi.org/10.1038/s41567-025-02797-w
and PRResearch 2026 quantum \(Z_2\) gauge sampling.

## 4. Predictive neutrino ansätze face current solar + reactor constraints

Use NuFIT v6.1 (2025, without-SK 3σ one-dimensional marginal ranges,
not a full correlated 6-parameter fit), conservative Cartesian
products:
\[
\sin^2\theta_{12}\in[0.2893,0.3295],\quad
\theta_{13}\in[8.26^\circ,8.95^\circ]\text{ (normal ordering)}.
\]
An exactly TM2 second trimaximal PMNS column demands
\[
\sin^2\theta_{12}=\frac{1}{3(1-\sin^2\theta_{13})}
\in[0.34036,0.34160],
\]
entirely outside this range. The TM1 first-column condition instead
gives a solar-angle value within the supplied interval.
The old tribimaximal \(\theta_{13}=0\) is also excluded.

In a **rank-two type-I seesaw** with one exactly massless light
*Majorana* neutrino, the effective neutrinoless-double-beta mass is
a sum of **two** vectors in the complex plane. Applying triangle
inequality over the conservative independent 3σ ranges gives
\[
|m_{ee}|_{\rm NO}>0.00117296\ \mathrm{eV},\qquad
|m_{ee}|_{\rm IO}>0.01538025\ \mathrm{eV}.
\]
Monte Carlo scans over the supplied independent intervals and
Majorana phase-minimized amplitudes confirm the analytic
inequalities. They are **conditional model bounds**, not measured
observations of \(0\nu\beta\beta\), evidence for Majorana neutrinos,
a unique vacuum selection, or exclusion of generic free-Yukawa
seesaw models.

Recent comparison data NuFIT v6.1:
https://www.nu-fit.org/?q=node/309 and
https://global-nu.org/results.html .
The October 2026 Bari preliminary comparison independently
emphasizes the small allowed solar interval.

## 5. Two gapless species still do not share a cone under generic local coupling

Previous on-site coupling acquired one common acoustic speed only by
gapping the second species. Here preserve **both exact shift
symmetries** and hence both massless sectors. Two local scalar fields
with standard time kinetic terms and gradient coupling \(\kappa\):
\[
V=\frac12(\partial_x\phi)^T
\begin{pmatrix}v_A^2&\kappa\\\kappa&v_B^2\end{pmatrix}
(\partial_x\phi).
\]
Their low-frequency squared-velocity eigenvalue discriminant is
\[
D=(v_A^2-v_B^2)^2+4\kappa^2.
\]
It is exactly zero for *real* \(\kappa,v_i\) only if
\(v_A=v_B\) AND \(\kappa=0\). Thus a generic **Gaussian derivative**
coupling **splits**, rather than locks, the two independent gapless
velocities. With bare \((1,1.2)\), coupling \(\kappa=0.8\) yields
two velocities approximately \((0.62474,1.43168)\); both remain
gapless. Higher-species random symmetric positive matrices confirm
the elementary matrix degeneracy principle.

This is not an interacting RG no-go. An exact unifying symmetry or an
interacting non-Gaussian fixed point could restore common limiting
speed; neither is demonstrated. The observed
GW170817/GRB170817A graviton–photon fractional speed bound
\(-3\cdot10^{-15}<\Delta v/c<7\cdot10^{-16}\)
is **for gravity versus electromagnetism under emission assumptions**,
not a bound on the two hypothetical scalar modes:
https://dcc.ligo.org/P1700308/public .

## Swing A (unrelated): exact proton protection may be a discrete symmetry, not just a huge GUT mass

Follow Davighi, Greljo & Ponce Díaz,
*Axion Quality from Exact Proton Stability*,
https://arxiv.org/abs/2609.01712 (1 Sep 2026),
which introduces a consistent **flavor-nonuniversal** \(U(1)_X\)
completion, not merely an arbitrary \(\mathbb Z_9\) assignment.

Take a low-energy residual \(Z_9\) with quark charge \(+1\),
anti-quark charge \(-1\), leptons/Higgs charge 0.
Then every gauge-invariant operator has
\[
q_{Z_9}=3\Delta B\bmod9,\qquad
\Delta B=0\bmod3\text{ for an allowed operator}.
\]
The independent finite brute-force screen enumerates **202**
combinations with nonzero baryon number passing conservative
necessary SM color-triality/SU2 parity/hypercharge/Lorentz-even
checks, with up to eight LH Weyl fields and two Higgs. All 202
\(\Delta B=1,2\) candidates are forbidden by the \(Z_9\) residue.
Explicit familiar dimension-six operators \(QQQL\),
\(u^cu^cd^ce^c\), \(u^cd^cd^cN^c\) are forbidden.
A schematic \((u^cd^cd^c)^3N^c\) has dimension 15 and
\(\Delta B=-3\), permitted by the **selection rule**; nonzero
spin/color/Grassmann contractions require enough flavors.

**Integration obstruction:** our previous *minimal B−L seesaw*
uses primitive integer generator \(3(B-L)\), giving quarks \(+1\),
leptons \(-3\), \(N^c+3\), scalar \(S=-6\). Higgsing only \(S\)
leaves a \(Z_6\), **not** the desired lepton-neutral \(Z_9\).
One cannot silently label the minimal B−L seesaw's residual
symmetry as the paper's exact-proton-protecting \(Z_9\).
A genuinely different \(U(1)_X\), additional Higgs inventory
and discrete anomaly check are required. This is an immediate
cross-sector consistency filter, not a new discovery of the published
\(Z_9\) idea. Nor does proton stability alone solve axion quality.

## Swing B (unrelated): information return distinguishes a Page curve from endless pair creation

A completely **unitary** eight-qubit pure state is scrambled by a
Haar-random ensemble (100 samples per partition). Label \(k\) of
the eight qubits as radiation, the rest as an evaporating black hole.
The mean von Neumann entropy matches **Page's exact finite-size
formula**:
\[
\mathbb E[S_R]=
[\psi(d_Rd_B+1)-\psi(\max(d_R,d_B)+1)
-(\min(d_R,d_B)-1)/(2\max(d_R,d_B))]/\ln2.
\]
For \(k=4\), \(S_R\simeq3.28194\) bits. As all eight qubits
transfer, \(S_R\to0\).

Compare a Hawking **pair-only** model that creates a fresh maximally
entangled outgoing qubit and a permanently hidden partner each
step; after eight emissions its radiation entropy is **8 bits**.
The latter can be unitary in an *enlarged permanently hidden*
Hilbert space, but it cannot yield complete purification of an
evaporated finite black hole unless information/partners transfer
back or remain in a remnant. This is a simple quantum-information
guard; the actual Page curve in evaporating gravitational spacetime
is highly nontrivial. Neither the geometry, horizon dynamics,
energy conservation nor an island formula is constructed.

Prior art: Page 1993; random-circuit Page curve tutorials;
finite-N island analysis in 2026,
https://www.sciencedirect.com/science/article/pii/S0370269326008312 .

## Swing C (unrelated): dark energy can be confounded with redshift-dependent supernova calibration

Build **synthetic**, flat FLRW luminosity distances for the published
DES-Dovekie 2026 central **illustrative** combination
\(\Omega_m=0.330,\ w_0=-0.803,\ w_a=-0.72\)
(Popovic et al, MNRAS548, 2026, stag632).
The model is NOT refitted to observed SNe, BAO or Planck. Compare
its SN distance modulus to LCDM and fit only two LCDM
photometric nuisance parameters:
\[
\delta\mu_{\rm nuisance}(z)=a+b\frac{z}{1+z}.
\]
Across 90 mock SN redshifts \(0.06<z<1.35\),
the maximum residual **after** calibration refitting is
\(0.018403\) magnitudes. With a synthetic uncorrelated
\(\sigma_\mu=0.1\) mag per point, the expected SN \(\chi^2\)
difference is small. This is a *degeneracy test*, not evidence
that Dovekie has such an unmodelled drift.

Independent synthetic **radial + transverse** BAO at seven
redshifts with one common adjustable \(H_0r_d\) scale partly break
the degeneracy: an exact mean generated under this CPL example
gives expected LCDM misfit \(\chi^2\simeq11.88\) at 1%
fractional precision per BAO observable, but only \(\sim1.32\)
at 3%. Full survey covariance, CMB, perturbation growth,
redshift selection, prior volume and SN systematics matter.

**Separate audit of actual repo PPD calculations:** the previous
\`analysis/toe_uv/class_ppd.py\` calls CLASS on 24 nominal
Fisher-posterior draws per held-out fold but computes
\(\ln(\sum_{\rm valid}e^{-\chi^2/2}/n_{\rm valid})\).
Several models fail to return CLASS results and the lost samples
are silently omitted from the average. Under one conservative
alternate rule that **invalid draws carry zero likelihood**,
the elpd decreases by
\(\ln(n_{\rm valid}/24)\). Example cumulative SN+BAO
penalties are \(-1.099\) for \`exp_infl1\` and \(-0.656\)
for \`free_neg_infl2\`. If failures are numerical rather than
physically excluded points, assigning zero is not a justified
correct answer either; convergence and reliable rerunning are
needed. The parent 24-draw claimed ranking is therefore less
precise than its two-decimal printed values suggest. The parent
properly retracted the strong fading-vs-CPL claim.

2026 DESI/dark-energy context:
https://doi.org/10.1093/mnras/stag632 ;
https://doi.org/10.1103/dqxw-yp1j ;
https://doi.org/10.1093/mnras/stag1607 .
These observational analyses report substantial dependence on
datasets, calibration and priors.

## Integrated conclusions

The candidate TOE must deliver **one common consistent action**
with all gauge, matter, temporal and gravitational degrees of
freedom, not eight mutually unrelated input Hamiltonians.

The strongest discoveries of *missing requirements* in this
packet are:
1. The full \(U(1)^2\) coupling matrix and representation-covariant
observables, not merely individually running gauge couplings.
2. **Finite-size estimator correction** for causal intervals and a
tuned-global-order counterexample to manifold identification.
3. A Gauss-constrained Fock-space interaction that gives genuine
staggered particle–antiparticle excitations; retaining global
particle-number constraints is important.
4. A current-neutrino-data filter capable of rejecting exact
trimaximal mixing and exact \(m_{ee}=0\) within rank-two assumptions.
5. An elementary strict Gaussian no-go for two independent massless
species acquiring one cone through generic local gradient mixing.
6. A genuine **group compatibility obstruction** between a
minimal B−L seesaw remnant \(Z_6\) and a proton-protecting \(Z_9\).
7. A conservation-of-information test distinguishing standard Page
scrambling from permanently hidden partners.
8. A quantitative synthetic SN calibration counterexample and
posterior-draw failure accounting for the recent cosmology ranking.

All effects have substantial mathematical/physics prior art; no
priority claim is made, and the repo's other assistants' independent
parallel discoveries are explicitly recognized. Next progress
should select or falsify a parameter-reducing **joint** action with
observable outcomes, not infer physical necessity from graph
cardinality coincidences.
