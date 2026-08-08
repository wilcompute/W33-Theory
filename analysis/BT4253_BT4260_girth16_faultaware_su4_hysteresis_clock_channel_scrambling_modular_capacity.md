# BT4253-BT4260 — girth-16 covers, fault-aware holonomy, metastable spectrum, clock compression, channel bounds, and three outside-box probes

This packet executes the five physics targets left by canonical Passes 4214-4221 and adds three independent probes. All statements remain finite-model statements. In particular, no graph velocity is identified with physical c, no analogue-Hawking calculation is promoted to observed radiation, and no effective scale coordinate is promoted to physical spacetime.

## Pass 4253 — explicit girth >= 16 Levi cover

The corrected W(3,3) point-line Levi graph has 80 vertices, 160 edges, degree four and girth eight. Gauge fixing a BFS spanning tree leaves 81 cotree voltage variables. The complete short-cycle census through length fourteen is

- length 8: 1,620,
- length 10: 5,184,
- length 12: 43,200,
- length 14: 336,960,

for 386,964 simultaneous voltage constraints.

A deterministic Z_2731 assignment frozen in the certificate has nonzero voltage on every one of these cycles. Hence the 2,731-sheet cyclic cover has

- 218,480 vertices,
- 436,960 edges,
- certified girth at least 16.

Because the base girth is eight, every reduced closed walk of length less than sixteen is a simple cycle, so the exhaustive simple-cycle audit is sufficient for the stated lower bound. The construction uses 23.9974 times fewer sheets than the earlier Z_65537 cover, although it uses 7.6072 times more sheets than the girth-14 Z_359 construction because it certifies two additional units of girth. A girth-18 certificate remains open.

## Pass 4254 — fault-aware composite geometric CZ

The Pass-4215 controlled phase is recast as two oppositely oriented latitude loops on the |11>-bright-state Bloch sphere, at theta=pi/3 and theta=2pi/3. Their weighted solid-angle difference is exactly 2pi, so the computational phase is pi.

Under a common polar calibration shift delta, the combined geometric phase is

phi(delta) = pi cos(delta).

Therefore the first derivative vanishes at delta=0 and

phi(delta)-pi = -(pi/2) delta^2 + O(delta^4).

For delta=0.02 rad the phase error is -6.282975870e-4 rad, the corresponding average two-qubit gate infidelity from this phase error alone is 5.92137e-8, and the operator-norm phase error is 6.28298e-4.

For a uniformly traversed latitude loop with speed ratio omega/Omega=0.02, the exact nonadiabatic leakage probabilities are 3.05824e-4 and 2.93842e-4 for the two latitudes. Their sum is 5.99667e-4. The branch-swap composite cancels common-mode dynamical phase exactly for equal durations, but it does not cancel differential gap error: a 0.1% differential mismatch at omega/Omega=0.02 leaves 0.15708 rad of residual dynamic phase. Thus the construction is fault-aware, not fault tolerant.

## Pass 4255 — the metastable Fokker-Planck and Lindblad spectra

At the saturated coexistence point g=0.5700939873487846 and diffusion D=0.25, the overdamped scale model was discretized as a detailed-balance birth-death generator. The first two positive eigenvalues converge as the grid is refined:

| grid | metastable gap | next rate |
|---:|---:|---:|
| 301 | 4.39417505e-8 | 2.92770021 |
| 601 | 4.37953901e-8 | 2.92958653 |
| 1201 | 4.37516725e-8 | 2.93022768 |
| 2401 | 4.37527494e-8 | 2.93047264 |

The metastable lifetime is therefore about 2.28557e7 model-time units, while the next relaxation rate is 2.93047. The timescale separation is 6.6978e7. The previous Kramers rate sum, 4.50150e-8, is only 2.8849% above the finite-volume spectral gap, providing an independent consistency check.

The two-state coherent reduction at coexistence is H=-(Delta/2)sigma_x. With the unit-prefactor instanton demonstration Delta=exp(-7.7881701215)=4.14610878e-4 and pure dephasing gamma_phi/2(sigma_z rho sigma_z-rho), the Liouvillian changes from underdamped to overdamped at

gamma_phi = 2 Delta = 8.29221756e-4.

This is an exact two-state Lindblad crossover once Delta is specified; the absolute physical prefactor of Delta remains uncalibrated.

## Pass 4256 — exact three-local clock down to 45 auxiliaries

Pass 4217 used 13 optimal shared pair-conjunction ancillas, 24 final-condition ancillas and 24 dynamic transition flags, for 61 auxiliaries. But the data program is three repeats of the same eight adjacent-SWAP supports. A transition flag only needs to identify the data operation, not which repetition invoked it. Reusing one flag per distinct SWAP support therefore reduces the flag count from 24 to eight without changing the legal history graph.

The exact resource count becomes

13 + 24 + 8 = 45 auxiliaries,

or 50 qubits including the five Gray clock qubits. This is a 26.23% reduction from 61 auxiliaries and 53.125% from the original 96-auxiliary exact three-local construction. The legal gap remains 2 Omega, with perfect transfer at pi/(2 Omega) and full revival at pi/Omega.

Within the frozen architecture in which a single dynamic flag directly controls one two-site SWAP and no extra selector control is permitted, eight flags are necessary for the eight distinct SWAP supports. Combined with the earlier exact 13-pair MILP optimum and the 24 unique final conditions, 45 is optimal in this architecture. It is not a global lower bound over all history-clock encodings.

## Pass 4257 — communication bounds for the complete 19-mode horizon

The complete horizon circuit defines a distinct effective communication channel from the initial outside signal mode to the detected outside output mode. The other 18 input modes are treated as the Gaussian environment. This should not be confused with the outside-versus-partners entanglement of the generated Hawking state.

For the baseline circuit the effective phase-insensitive attenuator parameters are

- transmissivity tau = 0.28300959407755605,
- spontaneous output occupation = 0.011958937708661351,
- added quadrature noise y = 0.37045414066988325,
- effective thermal environment occupation nbar = 0.016679355274322738.

Across the frozen 512-sample correlated-disorder ensemble,

- tau ranges from 0.1204016017 to 0.5113024216,
- effective nbar ranges from 0.0020018892 to 0.1788218751,
- 510 samples have tau <= 1/2,
- only two samples have tau > 1/2,
- none is entanglement breaking.

The known thermal-attenuator zero-capacity result for tau <= 1/2 therefore certifies zero unassisted quantum capacity for 510/512 effective signal channels. For the two samples above one half, an explicit scan over single-mode Gaussian thermal inputs finds no positive coherent information, but that is deliberately not promoted to zero unrestricted quantum capacity: thermal-attenuator capacity with nonzero environment temperature is a nontrivial problem, and recent work demonstrates that non-Gaussian inputs can beat the optimized single-mode Gaussian coherent information in some regimes.

Primary context: Lami et al., arXiv:2003.08895; Rosati, Mari & Giovannetti, arXiv:1801.04731; Mele et al., arXiv:2607.27449.

The resource overlay is striking. At n_th=0.005 the generated outside-partner state remains PPT-entangled in 512/512 disorder realizations, even though outside->partner steering survives in only 228, reverse steering in 482, and positive state coherent information in 415. State entanglement and signal-channel quantum capacity are therefore distinct resources in this model.

## Pass 4258 — outside box: exact spectral-form-factor scrambling falsifier

The Levi adjacency spectrum is 4^1, (-4)^1, (sqrt6)^24, (-sqrt6)^24 and 0^30. Therefore the normalized trace amplitude is

A(t) = [30 + 2 cos(4t) + 48 cos(sqrt(6)t)]/80,

and K(t)=|A(t)|^2. Irrationality of 4/sqrt(6) removes cross terms in the infinite-time average, giving

<K> = 2054/6400 = 0.3209375.

A nondegenerate 80-level reference plateau would be 1/80=0.0125. The exact Levi plateau is therefore 25.675 times larger. The huge degeneracies and quasiperiodicity make the bare Levi quantum walk a poor stand-in for a random-matrix-like scrambler. This is a useful falsifier, not a claim about generic many-body dynamics on the architecture.

## Pass 4259 — outside box: exact modular spectrum of the Levi vacuum

For the harmonic kernel K=5I-A_Levi and the point-versus-line bipartition, the incidence singular values are 4^1, (sqrt6)^24 and 0^15. The local symplectic eigenvalues are

nu_4 = 1/sqrt(3),

nu_sqrt6 = (1/4) sqrt(2 + 10/sqrt(19)).

The corresponding bosonic entanglement-Hamiltonian energies epsilon=ln[(nu+1/2)/(nu-1/2)] are

- epsilon_4 = 2.63391579385, multiplicity 1,
- epsilon_sqrt6 = 4.03202440074, multiplicity 24,
- epsilon=infinity for the 15 uncoupled zero-singular-value channels.

The total point-line entropy is 2.45529738720 nats and the logarithmic negativity is 6.98041873907 nats. Thus the entire modular spectrum collapses to only two finite energy scales plus fifteen exact spectators.

## Pass 4260 — outside box: channel volume versus ballistic speed

The degree-four high-girth tree limit has branching factor three, radial dispersion

E(q)=2 sqrt(3) J cos q,

and maximum radial group velocity

v_max=2 sqrt(3) J.

The ball volume is exactly

B(r)=2*3^r-1.

Hence the asymptotic logarithmic accessible-volume rate along a ballistic front is

v_max ln 3 = 3.80570460359 J nats per unit time,

or

v_max log2 3 = 5.49047115868 J address bits per unit time.

For a girth-16 cover, the radius-seven tree ball contains 4,373 vertices and the ballistic front reaches radius seven at 2.02072594216/J. This sharpens the capacity-versus-speed separation: node count grows exponentially with radius, while radial speed grows only as the square root of branching. The quantity is not a strict Lieb-Robinson velocity and is not physical c.

## Evidence boundary

The packet freezes a deterministic certificate, a self-contained verifier and focused regression. Pass 4253 exhaustively checks 386,964 base cycles. Pass 4257 uses a fixed 512-sample correlated-disorder seed. All quantitative claims are tied to these explicit finite models.
