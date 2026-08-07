# Passes 4169-4176 — discrete C2, continuous Hawking disorder, backreaction, Gray locality, Levi-cover correction, erasure, Casimir, and axion reduction

Status: **PASS_EXACT_EIGHT_FRONT_WITH_C2_DISORDER_BACKREACTION_LOCALITY_LEVI_ERRATUM_AND_TOPOLOGICAL_BOUNDARIES**  
Frozen certificate: `data/PART_4169_4176_DISCRETE_C2_HAWKING_BACKREACTION_GRAY_LEVI_CASIMIR_AXION.json`  
Verifier: `analysis/w33_pass4169_4176_discrete_c2_hawking_backreaction_gray_levi_casimir_axion.py`

## Executive result

This packet executes the five physics targets following Passes 4153-4160 and three independent outside-box probes. The most important correction is Pass 4173: the point-line Levi graph of `W(3,3)` is the incidence graph of 40 points and 40 lines with 160 flags, hence it has 80 vertices and degree 4. The degree-6 / branching-5 assumption used in Pass 4157 is superseded. The correct Bethe branching factor is 3, giving `beta_c J = atanh(1/3) = ln 2 / 2` for a locally tree-like degree-4 comparison model. Moreover, the 1,620 base 8-cycle parity equations have coefficient rank 81 and augmented rank 82, proving that no signed 2-lift can simultaneously double every base 8-cycle. Therefore simple iterated 2-lifts of this Levi graph are not a large-girth route.

## Pass 4169 — discrete second-Chern compiler

Use the four-dimensional Wilson-Dirac control

`d(k) = (sin k1, sin k2, sin k3, sin k4, m + cos k1 + cos k2 + cos k3 + cos k4)`,

with `m=-3` and normalized Hamiltonian `H=dhat.Gamma` in the rank-two Clifford bundle from Pass 4153.

At the 16 time-reversal-invariant momenta the five mass values grouped by the number `N_pi` of pi coordinates are

`[1,-1,-3,-5,-7]`

with multiplicities `[1,4,6,4,1]` and oriented Dirac weights `[1,-4,6,-4,1]`. The exact lattice Dirac-count formula gives

`C2 = (1/2) sum_N C(4,N)(-1)^N sign(m+4-2N) = 1`.

Thus only 16 high-symmetry calibration points are required to certify which Wilson-Dirac topological phase the control law occupies. This is distinct from resolving the nonlinear response over the full four-dimensional control torus.

A central-difference pullback-volume quadrature converges as follows:

| N per control axis | points N^4 | C2 quadrature |
|---:|---:|---:|
| 9 | 6,561 | 0.5946000255592135 |
| 13 | 28,561 | 0.7790565590712333 |
| 17 | 83,521 | 0.8634781119933770 |
| 21 | 194,481 | 0.9079770972936995 |
| 25 | 390,625 | 0.9340136375103706 |
| 29 | 707,281 | 0.9504670029565596 |

Among the audited meshes, `N=29` is the first below 5 percent response-integration error. Its phase step is `2 pi / 29 = 0.21666156231653746` rad. The important engineering distinction is therefore: **16 calibration points certify the topological sector; hundreds of thousands of naively sampled nodes are needed for a 5-percent brute-force response integral.** This motivates adaptive curvature sampling rather than a uniform four-dimensional sweep.

Boundary: exact finite Wilson-Dirac phase certification and numerical response quadrature; no fabricated 4D pump.

## Pass 4170 — continuous Hawking disorder and thermal mobility edge

The nine-cell, 38-dimensional Nambu Hawking chain is extended beyond binary corners in two ways.

### Correlated Gaussian audit

Generate 512 deterministic samples with covariance

`C_ij = exp(-|i-j|/2)`

and transform the local parameters by

`r_j -> r_j exp(0.35 x_j)`,

`Gamma_j -> logistic(logit Gamma_j + 0.25 x_j)`.

Results:

- minimum logarithmic negativity: `0.0822919174978226`,
- median logarithmic negativity: `0.22075082740123242`,
- maximum logarithmic negativity: `0.5298852171115666`,
- PT symplectic eigenvalue range: `0.2943362676672688 ... 0.4605015312705039`,
- outgoing occupation range: `0.0017608585277201268 ... 0.08738981732735193`,
- finite-chain symplectic growth exponent `(1/9) ln sigma_max(S)` range: `0.006592499987486316 ... 0.04158653386556598`.

Every sampled correlated-Gaussian realization remains entangled.

### Quasiperiodic audit

For `alpha=(sqrt(5)-1)/2`, scan 721 phases using

`x_j=cos(2 pi alpha j + phi)`,

`r_j -> r_j exp(0.7 x_j)`,

`Gamma_j -> logistic(logit Gamma_j + 0.5 x_j)`.

The logarithmic-negativity range is

`0.24211601793444767 ... 0.27238456666720445`.

The worst phase in this mesh is `phi=1.769052173866097`, and the largest sampled outgoing occupation is `0.02199857901123363`.

### Thermal entanglement mobility edge

The local surface-gravity profile is inferred from the frozen `omega=0.3` squeezings via

`tanh r_j(omega) = exp(-pi omega/kappa_j)`.

With a uniform input thermal occupation `n_th`, the entanglement edge is defined by the exact Gaussian PPT equation

`nu_tilde_min(omega_c,n_th)=1/2`.

For the baseline chain:

| n_th | omega_c |
|---:|---:|
| 0.001 | 0.8567765667308878 |
| 0.002 | 0.7722108662984974 |
| 0.005 | 0.6613283634941842 |
| 0.010 | 0.5783917254706858 |
| 0.020 | 0.49664906601892156 |
| 0.050 | 0.3915096061401572 |
| 0.100 | 0.3156088998655878 |

At `omega=0.3`, the baseline thermal occupation threshold is `n_th=0.11593620709206182`. Above it the outgoing-versus-partner Gaussian state is PPT in this model.

The worst sampled quasiperiodic phase moves the mobility edge only modestly: at `n_th=0.01`, `omega_c=0.5866466253164031`.

Boundary: finite Gaussian audits and one-parameter mobility boundaries; not a theorem for arbitrary stochastic processes or observed Hawking radiation.

## Pass 4171 — scale-geometry backreaction

Couple the scale coordinate to occupation of a representative Levi mode whose scale-dependent frequency is

`omega(s)=2 exp(-s)`.

At inverse temperature one, let

`n_B(s)=1/[exp(2 exp(-s))-1]`

and use the minimal positive-feedback backreaction flow

`ds/dt = gamma [ln 80 - 4s + g n_B(s)]`.

At `g=1`, two fixed points exist:

- `s=1.5949469860997991`, with derivative `-1.5695092712387817`, hence stable;
- `s=2.5062250949365414`, with derivative `+2.1157059825802156`, hence unstable.

Their instantaneous spectral dimensions `ln80/s` are respectively

`2.7474434403550068` and `1.7484569297175743`.

The stable and unstable roots annihilate in a saddle-node at

`s_c = 1.9679175210441553`,

`g_c = 1.1252773999853873`,

with `d_s,c = 2.226732872599674`.

Thus the minimally backreacting one-mode model does **not** preserve `d_s=4`: occupation shifts the fixed point downward in spectral dimension, and sufficiently strong positive feedback destroys the stationary scale rather than producing two stable branches. A true bistable geometry requires an additional saturating nonlinearity.

Boundary: explicit one-mode backreaction model, not physical spacetime dynamics.

## Pass 4172 — exact locality reduction of the Gray history clock

The 25-state reflected-Gray history clock uses five clock qubits. Because adjacent legal words differ in one clock bit, each legal transition is a single clock-bit flip conditioned on the other four spectator literals and accompanied by a two-site data SWAP. Direct implementation is therefore 7-local.

For each transition, encode the conjunction of its four spectator literals using three static binary AND ancillas. The standard two-local penalty

`P_AND(x,y,z)=xy-2xz-2yz+3z`

is exactly zero iff `z=xy` and positive otherwise. A three-ancilla tree produces a flag `f_t` for the four spectators. The propagation term becomes

`f_t X_clock SWAP_data`,

which is exactly 4-local.

For 24 transitions:

- AND ancillas per transition: 3,
- total static AND ancillas: 72,
- original locality: 7,
- exact reduced locality: 4.

Because the spectator bits do not change across their associated Gray transition, the legal flag constraints form an invariant subspace. Therefore the legal 25-state clock Hamiltonian is unchanged, including

- spectrum `-24 Omega,-22 Omega,...,+24 Omega`,
- legal spectral spacing/gap `2 Omega`,
- perfect-transfer time `pi/(2 Omega)`,
- full revival time `pi/Omega`.

For illegal-state penalty `Delta=40 Omega` and perturbation norm `epsilon=0.01 Omega`, the same block-separation estimate gives

`P_leak <= [0.01/(40-24-0.01)]^2 = 3.9111373939543984e-7`.

A further perturbative 4-to-3-local reduction can add one mediator per transition, raising the static ancilla count from 72 to 96. That step is deliberately not promoted as exact: the exact result of this pass is the 7-to-4 locality reduction.

Boundary: Hamiltonian locality accounting, not a hardware-optimal clock.

## Pass 4173 — explicit Levi-cover audit and correction of Pass 4157

The repository geometry constructor gives, at `q=3`,

`n=(q+1)(q^2+1)=40`

points and the same number of lines. Its committed census checks the number of flags as

`n(q+1)=40*4=160`.

Therefore the point-line Levi graph has

- 40 point vertices,
- 40 line vertices,
- 80 total vertices,
- 160 edges,
- degree 4 on both bipartite halves,
- girth 8.

This directly supersedes the degree-6 premise in Pass 4157.

The graph has exactly 1,620 simple 8-cycles. A signed 2-lift doubles a base cycle to length 16 exactly when the XOR of its eight edge signs is one. Requiring this for all 1,620 cycles gives a GF(2) linear system on the 160 edge signs. Its coefficient rank is 81 while the augmented rank is 82. Hence the system is inconsistent:

**No signed 2-lift can double all base 8-cycles simultaneously.**

Because a graph cover cannot introduce a shorter nonbacktracking cycle than the base girth and every 2-lift necessarily retains an 8-cycle, every such first 2-lift has girth exactly 8.

A deterministic SHA-256 signed-lift sequence confirms:

`(vertices,edges,girth) =`

`(80,160,8)`,

`(160,320,8)`,

`(320,640,8)`,

`(640,1280,8)`.

The correct locally tree-like degree-4 comparison has nonbacktracking branching `d-1=3`, so the Bethe instability is

`3 tanh(beta_c J)=1`,

or exactly

`beta_c J = atanh(1/3) = (ln 2)/2 = 0.34657359027997264`,

`T_c/J = 2/ln2 = 2.8853900817779268`.

The prior value `atanh(1/5)` from Pass 4157 is therefore not a property of the W(3,3) point-line Levi graph. Also, because simple iterated 2-lifts retain girth eight, they do not by themselves realize the large-girth hypothesis under which the Bethe limit is controlled.

Boundary: exact finite geometry and 2-lift obstruction; no experimental criticality is claimed.

## Pass 4174 — bonkers: Hawking greybody channel crosses the no-cloning capacity boundary

Treat the greybody stage as a pure-loss bosonic communication channel with effective transmissivity

`eta_eff = n_out / n_out_lossless`.

The baseline `omega=0.3` Hawking chain has

`eta_eff = 0.485735597242 < 1/2`.

A pure-loss bosonic channel is antidegradable for `eta<=1/2`, so its unassisted quantum capacity vanishes. The baseline channel therefore has

`Q=0` bits/use

in this effective-channel interpretation even though the outgoing mode remains entangled with the partner block.

Across the 512 previously frozen binary disorder patterns, recomputing the lossless reference for each pattern gives

`eta_eff in [0.3109129598611626, 0.7282862738005136]`.

Exactly 251 patterns lie below `1/2` and 261 above it. The largest effective pure-loss capacity in the set is

`Q_max = log2[eta/(1-eta)] = 1.4224182063347266` bits/use.

Thus the disorder ensemble straddles an information-theoretic no-cloning boundary even though every pattern in Pass 4154 remained Gaussian-entangled.

Boundary: effective pure-loss channel mapping, not a statement about black-hole information recovery.

## Pass 4175 — bonkers: exact spectral Casimir attraction on the W(3,3) Levi graph

Let `L` be the 80-vertex degree-4 Levi Laplacian and take the massive Gaussian operator

`K=L+I=5I-A`.

Introduce two identical pinning defects of strength one at vertices `u,v`. By the matrix determinant lemma the two-defect interaction free energy relative to isolated defects is

`E_int(u,v) = (1/2) ln[1 - G_uv^2 / ((1+G_uu)(1+G_vv))]`,

where `G=K^-1`.

The Levi graph is distance regular enough that the required Green data are exactly constant by distance:

`G_uu = 211/855`,

`G(d=1)=10/171`,

`G(d=2)=13/855`,

`G(d=3)=1/171`,

`G(d=4)=4/855`.

Hence

`E_1 = 1/2 ln(1-625/284089) = -0.0011012191859481348`,

`E_2 = 1/2 ln(1-1/6724) = -7.436602973476341e-5`,

`E_3 = 1/2 ln(1-25/1136356) = -1.1000194923920593e-5`,

`E_4 = 1/2 ln(1-4/284089) = -7.04009687184613e-6`.

Because the logarithm argument is below one whenever `G_uv` is nonzero, the interaction is strictly negative: the two scalar pinning defects have an exact graph-spectral Casimir-like attraction, strongest at adjacent vertices and decaying by graph distance.

Boundary: finite Gaussian determinant interaction, not a measured electromagnetic Casimir force.

## Pass 4176 — bonkers: second-Chern dimensional reduction gives a 2pi axion winding

For the `C2=1` parent bundle from Passes 4153 and 4169, dimensional reduction identifies the change of the three-dimensional Chern-Simons invariant with the second Chern number. Writing the descendant magnetoelectric angle as `theta=2 pi P3`, one complete parent sweep gives

`Delta theta = 2 pi C2 = 2 pi`.

Thus the closed bulk returns to an equivalent `theta mod 2pi` sector, while a gapped boundary Chern-Simons level shifts by one. In electronic normalization that corresponds to a boundary Hall-sheet shift of one `e^2/h` unit.

Boundary: exact topological dimensional-reduction statement for the synthetic parent model; no axion particle or condensed-matter axion response has been observed here.

## Literature context

- H. M. Price et al., *Four-Dimensional Quantum Hall Effect with Ultracold Atoms*, Phys. Rev. Lett. 115, 195303 (2015): realistic synthetic-dimension protocols and second-Chern response extraction.
- A. Serafini et al., *Entanglement and purity of two-mode Gaussian states in noisy channels*, quant-ph/0310087: Gaussian entanglement degradation under noisy environments.
- L. Caha, Z. Landau, D. Nagaj, *The Feynman-Kitaev computer's clock: bias, gaps, idling and pulse tuning*, arXiv:1712.07395: locality/gap/clock tradeoffs.
- S. Kulkarni and D. Dhar, *Finite-size scaling functions of the phase transition in the ferromagnetic Ising model on random regular graphs*, arXiv:2110.02928: locally tree-like regular-graph Ising finite-size scaling.
- M. M. Wolf, D. Perez-Garcia, G. Giedke, *Quantum Capacities of Bosonic Channels*, quant-ph/0606132; F. Caruso and V. Giovannetti, Phys. Rev. A 74, 062307 (2006): degradability and pure-loss quantum capacity.
- X.-L. Qi, T. Hughes, S.-C. Zhang, Phys. Rev. B 78, 195424 (2008): second-Chern topological field theory and dimensional reduction to 3+1-dimensional magnetoelectric response.

## Evidence boundary

The frozen certificate promotes only finite Wilson-Dirac, Gaussian, one-mode backreaction, clock-gadget, finite graph-cover, pure-loss channel, Green-function determinant, and topological dimensional-reduction statements. The Pass 4157 degree-six assumption is explicitly superseded for the W(3,3) point-line Levi graph. No fabricated device, observed Hawking radiation, physical spacetime backreaction, experimental phase transition, black-hole information result, measured Casimir force, axion detection, gravity, cosmology, or theory of everything is established.
