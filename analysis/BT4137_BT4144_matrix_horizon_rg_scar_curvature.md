# Passes 4137–4144 — Matrix Wilson pumping, an extended Hawking lattice, microscopic RG, autonomous scars, and finite-size curvature

## Evidence status

All eight fronts are finite and deterministically checked by `analysis/w33_pass4137_4144_matrix_horizon_rg_scar_curvature.py`. The frozen semantic certificate is

`d16f8ab7ce51f2953cfd4866e7a716e31a271b3337a05b6105b367736bcecb6d`.

The results below are group-theoretic, Gaussian, Markovian, finite-clock, transfer-matrix, circuit-information, and band-topological statements. They do not establish continuum QCD, observed Hawking radiation, physical spacetime, a thermodynamic phase transition, anyons, gravity, cosmology, or a theory of everything.

## Pass 4137 — Matrix-valued Wilson pumping

The color space `(3 tensor anti-3)^tensor3` contains six independent contraction singlets. Their Gram eigenvalues are

`2/9, 8/9, 8/9, 8/9, 8/9, 20/9`.

Choose three orthonormal singlet channels and couple one bright combination to an auxiliary level. The remaining rank-two dark bundle carries the Wilczek–Zee connection. For a tripod loop with `cos(theta0)=1/3`, the loop angle is `2 pi/3` and two conjugate control loops yield

`Uy=[[-1/2,-sqrt(3)/2],[sqrt(3)/2,-1/2]]`,

`Uz=diag(exp(-2 pi i/3),exp(+2 pi i/3))`.

Their group commutator has trace `-1/4` and eigenphase cosine `-1/8`; it is neither the identity nor a center phase. The Wilson response is therefore genuinely matrix-valued on a gauge-invariant singlet doublet. This is the finite realization of the non-Abelian adiabatic gauge structure introduced by Wilczek and Zee, Phys. Rev. Lett. 52, 2111 (1984).

## Pass 4138 — Nine-cell Hawking scattering lattice

Nine localized squeezing cells were stitched into one Gaussian scattering chain. The annihilation space has 19 modes: one outgoing channel, nine partner channels, and nine environment channels; the Nambu map is 38 dimensional.

At `omega=0.3`, `kappa=0.4`:

- paraunitary residual: `1.10329258424e-15`;
- outside occupation: `0.0119589377087`;
- lossless outside occupation: `0.0246202620861`;
- greybody ratio: `0.485735597242`;
- total partner occupation: `0.0245530327208`;
- environment occupation: `0.0125940950121`;
- pair-balance residual: `6.94e-18`;
- partner center: cell `4.00482241038`;
- partner RMS width: `1.19773663119` cells;
- outside/partner logarithmic negativity: `0.208535299833`.

The lattice dispersion at inside flow `u=-0.5` and `omega=0.3` has roots `1.04940641366` and `3.10844862713` with opposite group velocities `0.255722058179` and `-0.477910385025`, explicitly exhibiting the ultraviolet partner branch. A cavity embedding is stable for round-trip attenuation below `0.991140273564`; attenuation `0.4` leaves margin `0.5964`.

This extends the exact single horizon cell into a spatial transfer chain with frequency-resolved greybody loss, partner localization, entanglement degradation, and UV mode conversion. It remains an analogue finite Gaussian model, consistent with the BdG and Floquet analogue-Hawking literature, not an observation of gravitational radiation.

## Pass 4139 — Microscopic channel-balance RG

Four independent local Markov channels each contribute one quarter of the deterministic scale drift and independent noise. Summing them gives

`ds = gamma[ln(80)-4s] dt + sqrt(2D) dW`.

The Fokker–Planck stationary law is

`p_inf proportional exp[-gamma Phi(s)/(4D)]`,

with `Phi(s)=1/2[ln80-4s]^2`. The exact mean is

`s*=ln80/4=1.09550665867`,

and the Fokker–Planck gap is `4 gamma`. The deterministic spectral dimension is exactly

`ln80/s*=4`.

For `gamma=1`, `D=0.01`, the stationary variance is `0.0025`, the mean noisy spectral dimension is `4.0083850191`, and the probability of `s<0` is about `1.04e-106`. Relative entropy obeys

`d D_KL(p||p_inf)/dt = -D integral p [partial_s ln(p/p_inf)]^2 ds <= 0`.

Thus the prior channel-balance flow is derived from a local stochastic controller rather than merely postulated. This remains a model of scale selection, not a derivation of physical spacetime.

## Pass 4140 — Autonomous static scar-history gadget

The eight nearest-neighbor SWAPs that shift one CDW branch are repeated three times, producing a 24-gate program whose data operation is `U_shift^3=I`. A monotonic Feynman history requires 25 clock states. The time-independent Hamiltonian is

`H=sum_t Omega sqrt[(t+1)(24-t)] (|t+1><t| tensor U_t + h.c.)`.

Its spectrum is the equally spaced ladder `-24,-22,...,22,24` in units of `Omega`. Perfect endpoint transfer occurs at

`T=pi/(2 Omega)`

with amplitude `1` and residual `6.66e-16`; the data has undergone exactly `U_shift^3=I`. The complete clock/data history revives at `pi/Omega` with residual `7.40e-15`. This is the engineered-coupling perfect-transfer mechanism of Christandl et al., now used as an autonomous computation history.

With an illegal-clock penalty `Delta Q` and perturbation norm `epsilon`, the subspace leakage is bounded by

`[epsilon/(Delta-epsilon)]^2`.

For `epsilon=0.01`, `Delta=20`, the bound is `2.50e-7`; the Duhamel endpoint infidelity bound is `2.47e-4`. The clock counts are minimal only within a monotonic history architecture; no global ancilla-minimality claim is made.

## Pass 4141 — Curvature finite-size scaling

For `N` independent dark-reservoir cells,

`Z_N=Z_1^N`, `g_N=N g_1`, and the third cumulant tensor also scales as `N`. The two-parameter Hessian scalar curvature therefore obeys exactly

`R_N=R_1/N`.

The single-cell sign change stays at `beta U=14.5791667571`, but its amplitude vanishes. Examples:

- `R_N(0,0)=-0.646027859685/N`;
- `R_N(20,0)=0.20080335723/N`.

A weakly coupled one-dimensional dark/bright macrosector model has a positive 2×2 transfer matrix. At `K=0.2` its eigenvalues at the single-cell crossing are `3.61914240484` and `3863.81225206`, giving correlation length `0.143406748975` cells. Perron–Frobenius analyticity forbids a finite-temperature singularity for finite positive weights and coupling. The curvature crossover therefore rigorously fades rather than sharpening into a critical point in these product and 1D limits.

## Pass 4142 — Bonkers: geometric phase-order transistor

A pump-branch control chooses whether the singlet doublet receives `Uy Uz` or `Uz Uy`. From input `|0>`, the output-state fidelity is exactly `7/16`, visibility is `sqrt(7)/4=0.661437827766`, relative phase is `-1.76092193014`, and state-vector distance is `3/2`.

Changing only the order of two geometric loops changes a measurable output. This is a finite holonomic phase-order switch, not an anyon transistor or fabricated device.

## Pass 4143 — Bonkers: causal-entropy throughput bound

The Levi graph has exact edge connectivity four. A two-qutrit unitary crossing a cut can change bipartite entropy by at most `2 ln3`; four simultaneous cut gates therefore transmit at most

`8 ln3 = 8.78889830934` nats per circuit layer.

For `N` cells each carrying a maximally mixed 3161-state dark reservoir, any circuit that establishes the full cross-cut entropy needs at least

`ceil[N ln3161/(8 ln3)]`

layers. The asymptotic lower bound is `0.916911702534 N`; for 80 cells it is 74 layers. Three coupler failures preserve connectivity, while a four-edge cut can disconnect the graph. This is a finite circuit bound, not a black-hole area law.

## Pass 4144 — Bonkers: charge-two synthetic monopole

Three orthonormal gauge-singlet contraction channels are treated as a spin-one triplet with

`H(k)=sin(kx) Sx + sin(ky) Sy + [-1+cos(kx)+cos(ky)] Sz`.

A 31×31 Fukui–Hatsugai–Suzuki audit gives band Chern numbers

`[-2.000000000000, 3.83e-17, 2.000000000000]`,

hence exact values `[-2,0,2]`. The adjacent-band gap is one on the audit grid. The control defect therefore carries synthetic monopole charge two. It is Berry curvature in a finite control manifold, not a physical magnetic monopole.

## Files

- Verifier: `analysis/w33_pass4137_4144_matrix_horizon_rg_scar_curvature.py`
- Certificate: `data/PART_4137_4144_MATRIX_HORIZON_RG_SCAR_CURVATURE.json`
- Regression: `tests/test_w33_pass4137_4144_matrix_horizon_rg_scar_curvature.py`
