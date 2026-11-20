# November 20: W33 CSS decoder, H27/SU3 quotient, and four independent TOE controls

**Baseline**: W33-Theory master 31d247e0c3d04ec828ced9c22f7a454005d0ce2c. This packet is bounded finite mathematics, not a proven Theory of Everything, photonic device, singular-G2 compactification or emergent Einstein dynamics.

**1. New ideal CSS decoder.** The parallel mixed Levi/repetition ternary CSS [[638,81,dX=3,dZ=8]] code already exists (9c9d65d). We reconstruct the Levi geometry and H_X/H_Z sparse parity checks, then enumerate 1276 nonzero single-X and 1276 nonzero single-Z Pauli error syndromes. Every within-type single-error syndrome is unique; no collisions. The weight-3 X logical explicitly gives a weight-two-vs-weight-one syndrome collision on a repetition triple. Ideal single-qudit lookup is not fault-tolerant syndrome extraction. See https://arxiv.org/abs/2608.31040.

**2. New H27 center identification.** Nine flavor generators U,V obey UVU†V†=omega I9. At the SIC vacuum Q*_(a,b)=X^b Z^a(1,-1,0), Q*U=ZQ* and Q*V=XQ*. The flavor center therefore coincides with the SU3 color center on fundamental triplets, and acts trivially on gauge-invariant color observables. After quotient by that color gauge transformation, the effective flavor action factors through H27/Z3~Z3². This does not prove discrete anomaly cancellation or a full E8 field sector. Center identification has known precedent in Heisenberg quivers: https://www.sciencedirect.com/science/article/abs/pii/S0550321306004883.

**3. Native-qutrit memory adversarial calibration.** With Beyer et al.'s three-time witness (https://arxiv.org/abs/2611.17268), previously derived measured-frequency upper bounds and reference gamma=.75, epsilon=.01, an independent per-distribution total-variation calibration bound tau yields W_upper(tau)=6[2 sqrt((a+tau)(b+tau))+(b+tau)] - (1/2)sum_j max(0,|3r_j-1|-3tau), a=1-2epsilon/3, b=epsilon/3, r=((1+2gamma)/3,(1-gamma)/3,(1-gamma)/3). It crosses zero at tau=0.00983009795. At tau=.001, W_upper=-.6818046. With a separate 21-coordinate Hoeffding confidence contract, 214,000 accepted trials per each of seven settings is a conservative model-conditional planning figure. No physical measurements or pairwise-process certification.

**4. Fifth-order optical drift.** For each of nine Weyl modes, sample at ±h_j, ±2h_j, ±3h_j and combine paired settings with signed weights 3/2,-3/5,1/10. Exact cancellation through detector-polynomial degree five with fixed trace is verified despite different h_j; sixth-order drift leaves residual ~5.06e-5 in a seeded model. Compared with a uniform six-exposure mean, variance inflation is 7.86 at equal per-exposure noise. This is a calibrated simulated SU3 character, not an implemented quantum circuit.

**5. Charged chirality caution.** On an even-periodic naive 1D lattice, sin(k) vanishes at k=0 and pi with opposite slopes +1,-1. The zero net oriented count is verified for N=12,24,48. This is classical fermion doubling, not a theorem ruling out singular G2/ADE charged matter with inflow; no 7D physical Dirac problem has yet been specified.

**6. Causal longest-chain control.** Uniform-volume Minkowski diamond sprinklings of size n=48,96,192,384 (24 samples per n) yield finite-n log-height scaling 0.5695 (1+1D) and 0.3288 (3+1D), while pair-comparability stays near .5 and .1. Finite estimates do not prove asymptotic exponents or gravitational field equations.

The complete six-front Python producer, 24 tests, numerical JSON certificate and extended report are available in the separately supplied reproducibility ZIP in this conversation. The GitHub executable and 11 focused tests here are independently reproducible for the two primary new algebraic advances.

## Five independent next steps
1. Specify E8 representation/messenger data for the H27 center quotient and explicitly check discrete mixed anomalies.
2. Add repeated noisy CSS syndrome-extraction schedules, hooks and fault-tolerant decoding.
3. Implement a loss-aware process-tomography verification of actual three-time memory and classical two-time reductions.
4. Optimize the fifth-order Weyl readout with finite counts and drift/jitter under a physical photon circuit.
5. Independently construct a charged singular G2/ADE index and a continuum-valid causal-gravity action.
