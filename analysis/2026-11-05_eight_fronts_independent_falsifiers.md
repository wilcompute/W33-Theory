# November 5, 2026 — Eight independent TOE falsifier controls

**Status:** eight executed finite models with assertions and JSON certificates.
**Not** a new unified physical theory, experimental result, or original
discovery of the individual models.

## Prior-art and repository cross-checks

The existing 215-page `papers/forty_points/main.pdf` is the baseline.
Earlier repository scripts already cover: lattice gauge matter-flux on C4
(`analysis/toe_20261104_matter_dynamical_z2_flux_competition.py`);
null-history spectral clock (`analysis/w33_20261105_general_q_null_clock_continuum_guard.py`);
reset immune temporal memory (`analysis/toe_20261104_reset_immune_quantum_memory_falsifier.py`);
Landau chirality (`analysis/w33_pass11697_11698_chirality_vacuum.py`);
Witting/440 physical readout
(`analysis/toe_20261104_witting_A5_unitary_lift_and_fisher.py`).
The present work does not relabel any of these established tracks as a new
discovery. It supplies *new orthogonal controls and explicit limitations*.

Relevant external research:
- 2025 trapped-ion qudit lattice gauge simulations: https://www.nature.com/articles/s41567-025-02797-w
- 2024-2025 non-Hermitian skin effect: https://www.nature.com/articles/s41377-024-01667-z
- 2011 rigorous detection/postselection loophole: https://doi.org/10.1103/PhysRevA.83.032123
- Aubry-André localization is standard: https://doi.org/10.1103/PhysRevB.110.054202

## First five, completing the requested follow-through

### 1 — Native dynamical action: a finite-size Wilson flux *negative control*

For one coherent matter excitation hopping on a periodic ring, the exact
gauge-invariant Wilson sectors \(\Phi\in\{0,\pi\}\) have band minima

\[
E_\Phi=\min_{k=0}^{n-1}[-2J\cos((2\pi k+\Phi)/n)].
\]
With \(J=1\), \(\Delta_n=E_\pi-E_0=2[1-\cos(\pi/n)]\).
The finite ring prefers zero flux, but the preference vanishes like
\(\pi^2/n^2\); it cannot, by itself, select a nonzero thermodynamic energy
density gap or Einstein/Standard-Model vacuum. The prior C4 Gauss-law
Hamiltonian already shows matter flux competition; this is the new
finite-size scaling closure.

### 2 — Weighted continuum graph: a positive *locality control*

Compare the normalized Laplacian of a 64x64 toroidal nearest-neighbor lattice
to the growing-field fully connected affine-null graphs. Define
\(d_s(t)=2t \mathrm{Tr}(L e^{-tL})/\mathrm{Tr}(e^{-tL})\).
The local lattice approaches dimension 2 at mesoscopic diffusion times;
the null graph's normalized spectral gap remains O(1) in growing q.
A smooth low-frequency sector requires an added spatial neighborhood and
couplings. That input is not derived by the W33 incidence relations.

### 3 — Temporal memory: experimentally testable exact power

For a three-time qutrit experiment with trusted reference, a trusted
entanglement-breaking reset, and no quantum bypass, the ideal post-reset
Bell fidelity is \((1+8p)/9\). If no-clicks are assigned an independent
maximally mixed trit, the *all-trials* fidelity is \((1+8\eta p)/9\).
Separability requires \(\le 1/3\); thus visibility needs
\(\eta>1/(4p)\). For \(p=.35,\eta=.85\), an exact one-sided binomial
test at 3000 trials supplies a decision threshold, false-alarm bound,
and power. This is an analytic experimental design *conditional on
trusted interventions*, not measured quantum memory.

### 4 — Chirality/vacuum: finite CP selection no-go

Enumerate all \(2^{16}=65,536\) configurations of a periodic 4x4 Ising
analogue, with CP modeled by global spin reversal. An even action
makes the finite-volume signed expectation exactly zero at zero source,
although \(\langle |m|\rangle\neq0\); an explicit source field reverses
the sign of \(\langle m\rangle\) when reversed. The theorem is simply
pair cancellation. A CP-even finite model does not select nature's
handedness; a vacuum selection mechanism, boundary datum, or
thermodynamic order of limits is still required.

### 5 — Photonic hardware falsifier: how much information is actually read out?

The Witting ququart ray-projector overlap Gram is exactly
\(G=(2I+J-A_{\mathrm{W33}})/3\); the native 40-effect POVM
\(E_j=P_j/10\) satisfies the resolution of the identity.
For \(\rho_i=(1-\epsilon) I_4/4+\epsilon P_i\), equiprobable
binary discrimination at \(\epsilon=.2\):
- Orthogonal rays: measured total variation \(2\epsilon/5\)
  versus optimal Helstrom trace distance \(\epsilon\).
- Nonorthogonal ray pair, squared overlap 1/3: measured total variation
  \(\epsilon/3\) versus Helstrom distance \(\epsilon\sqrt{2/3}\).

Therefore the native fixed Witting 40-outcome measurement is *not*
Helstrom-optimal even for these two simple classes. This is a
falsifiable readout-efficiency budget; the ultimate optimum requires
pair-adapted measurement. No experimental processor is claimed.

## Three deliberately orthogonal new experiments

### 6 — Non-Hermitian skin topology

An asymmetric Hatano-Nelson hopping model with \(t_R=1.5,t_L=.5\)
has a periodic spectrum encircling zero with winding +1.
Under open boundary conditions its spectrum is real but its right
eigenvectors pile up against one boundary. This is well-known
non-Hermitian topology, **not** evidence that quantum mechanics is
fundamentally nonunitary. A future connection to laboratory-controlled
dissipation would require a fully specified open-system dilation.

### 7 — Incommensurate potential and scale selection

The golden-frequency Aubry-André model with hopping 1 and
on-site modulation \(\lambda\cos(2\pi\alpha j)\), with
\(\alpha=(\sqrt5-1)/2\), was diagonalized for 55, 89, 144 sites.
Near-zero-mode mean inverse participation ratios separate
extended (\(\lambda=1\)), critical (\(\lambda=2\)) and localized
(\(\lambda=3\)) finite-size regimes. This is a **known** metal-insulator
transition with a new repository-local numerical control; it is
*not* a derivation of a cosmological or particle mass hierarchy.

### 8 — Collider selection can counterfeit a PR box

Let two independent hidden bits \(u,v\) be local outcomes, independent
of chosen measurement settings \(x,y\). A central, forbidden-in-
loophole-free-Bell-tests herald retains only trials where
\(u\oplus v=xy\). In selected data, all four correlators equal those of a
PR box and CHSH=4. But only 50% of trials survive each setting;
assigning independent random no-click values produces CHSH=2.
This is a concrete adversarial counterexample to overinterpreting
postselected quantum/interference observables. It is the well-known
detection-loophole mechanism, *not* an actual Bell violation.

## Executable contract and epistemic ledger

Producer: `analysis/toe_20261105_eight_fronts_controlled.py`.
Certificate: `data/toe_20261105_eight_fronts_controlled.json`.
Regression: `tests/test_toe_20261105_eight_fronts_controlled.py`.

Each item has an analytic predicted formula, numerical enumeration,
a counterexample or falsifier condition, and a bounded status.
Five continuations and three independent physical/foundational
controls have been executed. No full TOE solved, no empirical
constants derived, no physical laboratory experiment conducted.


## Stronger cross-checks on the three orthogonal experiments

**6 — Similarity-metric firewall.** The open Hatano–Nelson chain with
\(t_R=1.5,\ t_L=.5\) is *exactly* similar to a real symmetric tridiagonal
matrix by \(D_{jj}=(t_L/t_R)^{j/2}\):
\(H_{\rm OBC}=D H_{\rm sym}D^{-1}\).
Its conventional right-eigenvector probability density is boundary
localized, but its left-right **biorthogonal** site weights reduce
to the symmetric-chain weights. The latter's mean position is the
geometric centre, while right-only means are near the boundary.
The similarity has a rapidly growing condition number: skin response is
real and experimentally meaningful in ordinary coordinates, but
interpreting it as fundamental direction selection is metric-dependent.
**Original research hypothesis to investigate:** in any emergent
non-Hermitian substrate, test whether the distinguished physical inner
product neutralizes the apparent arrow before claiming a spacetime arrow.

**7 — Effective finite-size participation exponents.** Fit
\(\mathrm{IPR}\sim N^{-D_2^{\mathrm{eff}}}\) across 55, 89 and 144 sites,
separately at \(\lambda=1,2,3\). The three fitted slopes distinguish
decaying participation from nearly saturated localization, but they
are only finite-size diagnostic exponents, not thermodynamic critical
exponents. **Original research hypothesis:** a candidate geometrical
hierarchy should predict its participation exponent *and* remain
stable under changes of approximant before being compared to masses.

**8 — Blind-herald firewall.** The exact postselected PR example reaches
conditional CHSH=4 only because the acceptance event explicitly
references both setting choices. If the herald is fixed independently
of measurement settings (here choose \(u=v\) before settings),
the retained data give CHSH=2. **Original research hypothesis:**
every proposed retrocausal or temporal-interference witness should
publish a causal DAG for the herald and an all-trials randomized
no-click result, not only its conditional score.


### A stronger, genuinely *local* detection-loophole model

The central joint-herald example above is intentionally a weak adversarial
control because it reads both measurement settings. We independently built a
strictly local-detector construction. Shared source randomness is
\(\lambda=(x_*,y_*,u)\) with three independent fair bits. Alice's
outcome is \(a=u\), Bob's outcome is \(b=u\oplus(x_*y_*)\).
Alice clicks only when her local input \(x=x_*\); Bob clicks only when
Bob's **own** input \(y=y_*\). Neither device knows the remote actual
setting, and the detectors do not communicate.

Conditional on both detectors clicking, \(a\oplus b=xy\) identically,
so postselected CHSH=4. Yet each local detector clicks with probability
1/2 and coincident detection probability is 1/4 for every input pair.
Assign independent fair output bits on the noncoincident events: the
all-trials CHSH is only 1. This is a fully local example of a
detection-loophole counterfeit. It makes the requested *physical*
falsifier sharper: publish both local efficiencies and the unfiltered
statistic, never only the postselected correlation. The mechanism is
established Bell-test prior art, not evidence for superquantum signalling.
