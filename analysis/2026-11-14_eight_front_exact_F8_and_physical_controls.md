# 2026-11-14 — Eight independent fronts: an exact F8 witness and seven TOE falsifier controls

**Scope:** Independently implemented finite/mathematical controls after reading current GitHub master and local parallel experiments. They do not solve a theory of everything. We expressly do **not** overwrite the locally uncommitted Pass 12670 tick action, hexagonal E6 holonomy results, or the current E6 STU worktree.

**Concurrent stronger result (Pass 12671, commit 3d06c2738):** While this rational-state witness was being computed, another assistant published an exact algebraic pure state attaining the proposed cyclotomic value (exact upper bound, still no matching global lower bound). **Our strictly larger rational bound is now superseded as the best upper bound**; it remains an independent simple-integer witness, baseline cross-check and fully reproducible comparison. See `analysis/PASS12671_F8_EXACT_WITNESS_RANK3_PAULI_STABILISER.md`. Claims below referring to the *previous* rational benchmark are historical comparisons only.

## Most consequential outcome: new exact rational upper bound for nine F8 MUB certainty

Producer: `analysis/toe_20261114_f8_exact_rational_witness_refinement.py`.
Certificate: `data/toe_20261114_f8_exact_rational_witness_refinement.json`.

The existing Pass 12669 reports a high-precision candidate for `c8=64 min F`, where for a normalized `A` on an 8x8 complex matrix,

`F(A)=sum_ab |A_ab|^4 + sum_{t=0}^7 sum_kl |(Xi(A o Phi_t)Xi/8)_kl|^4 - 9/64`.

Here `Xi_ka=(-1)^Tr(ka)`, `Phi_t,ab=(-1)^Tr(tab)`, using GF(8) modulo `x^3+x+1`. Its proposed minimum is `(47-32 cos(2pi/9))/9`, but numerical optimization + integer-relation recovery is not a global proof.

Instead of another floating-point computation, round the **128 real coordinates** from the committed high-precision numerical minimizer at decimal scale `10^18`, obtaining exact integer complex amplitudes `z_ab = r_ab + i s_ab`. Divide by `sqrt(N)`, where `N=sum_ab(r_ab^2+s_ab^2)`. Every fourth moment is then rational, because all Fourier/chirp signs are integers and the common norm cancels:

- `S0=sum_ab (r_ab^2+s_ab^2)^2`.
- `Z_t,kl = sum_ab Xi_ka Phi_t,ab Xi_bl z_ab` (Gaussian integers).
- `64 F = [64(8^4 S0 + sum_tkl |Z_t,kl|^4) - 9*8^4*N^2]/(8^4*N^2)`.

The numerator, denominator, integer coordinates and exact-arithmetic producer are all stored in the certificate. **This yields a rigorous upper bound on the true infimum**:

`c8 <= 2.498508646688078097058159464691852002600732143379528554416635...`

The displayed digits are a presentation of an **exact rational fraction**, not a floating-point optimization. Previous recorded rational-witness value: `2.4985086592218817`. Compared with the **unproved** cyclotomic candidate `2.498508646688078097058159464691851826005929...`, the new witness is numerically about `1.76595e-34` higher, roughly 26 orders of magnitude closer. This does **not** certify equality or a global lower bound. F8 MUB validity follows the prior construction and is cross-checked against independent integer Walsh/field controls; an additional floating NumPy contraction in the tests confirms the rational result.

The closest outstanding task is an **exact matching lower bound**, e.g. a valid globally nonnegative SOS or SDP dual witness. A very close upper bound alone cannot establish the infimum.

## The remaining four primary fronts

### 1. Curved-flux compactification stability: a fully specified homogeneous counter-control

Producer: `analysis/toe_20261114_seven_orthogonal_front_controls.py`, function `two_sphere_homogeneous_adS`.

Use a conditional 9D Einstein-Maxwell action with independent positively normalized magnetic 2-form fluxes on two round spheres, internal `S2 x S2`, and external `d=5`. For `x=exp(u+v)`, `y=exp(u-v)` and dimensionless flux/curvature coefficients `A=7/5,B=2`, the 5D Einstein-frame homogeneous potential is

`V(u,v)=(14/5) exp(-20u/3) cosh(4v)-4 exp(-14u/3) cosh(2v)`.

At the unit-radius solution `u=v=0`, the exact result is:

- `dV=(0,0)`;
- `V*=-6/5` (AdS sign);
- `Hess_{u,v} V=diag(112/3,144/5)`, both strictly positive.

Hence **both** homogeneous volume and relative-radius fluctuations are stabilized **in this model**. It is not an E6 generalized Scherk-Schwarz solution and does not establish the higher-dimensional full Einstein equations, all moduli, non-homogeneous KK fluctuation stability, or a de Sitter/Minkowski vacuum. The spheres have positive curvature, unlike the previously analyzed flat `T4`; the result does not evade its topology guard by pretending it is a torus.

### 2. Explicit local CPTP qutrit gate control

Function `qutrit_cptp_gate`. Prepare `|+>_3 |0>_3`, apply an ideal controlled-SUM unitary, and then a dephasing channel on the first qutrit with `p=1/4`. Verify exactly specified Kraus completeness `sum K†K=I`, output positivity, trace=1, preservation of the second qutrit's reduced state (no superluminal signalling), output purity `17/24`, and entanglement negativity `3/4`. This is a reproducible quantum-channel control, not a derived hardware gate, holonet dynamics, or fundamental tick time.

### 3. Continuum locality/spectral-dimension control

Function `w33_cycle_continuum_control`. For the W(3,3) collinearity graph, combinatorial Laplacian spectrum is `0^1, 10^24, 16^15`. Its finite heat trace therefore equilibrates exponentially; it cannot itself support an extended infrared four-dimensional diffusion plateau. For an explicitly inserted length-256 cycle `C256` at diffusion time `t=10`, the Cartesian products yield `d_s(W33 x C256) ~= 1.01318` and `d_s(W33 x (C256)^4) ~= 4.05272`. The second figure comes from **four spatial cycle factors deliberately added**, not from W33 alone, and is a Riemannian diffusion signature, not a Lorentzian spacetime construction. This complements, rather than duplicates, prior general-q spectral no-go work.

### 5. Photonic erasure and heralding resource budget

Function `photonic_loss_erasure_budget`. In a **hypothetical** loss-only 40-mode single-photon carrier, choose a logical 16D subspace (4 ideal logical qubits), per-passage photon survival `49/50`, 20 passages and four independent heralded conditional gates succeeding with probability `4/5`. Exact success is `(49/50)^20 (4/5)^4 ~= 0.27345`. A naive four-photon, equally deep comparison is `(49/50)^80 (4/5)^4 ~= 0.08137`. This counts idealized survival only: it excludes fabrication errors, mode-dependent loss, correlated faults and gate infidelity. The textbook single-channel erasure-capacity expression, `4 max(0,2 eta_total -1)`, is a separate asymptotic benchmark, **not** a working fault-tolerance threshold or an actual single-photon universal-quantum-computing construction.

## Three additional outside-the-box controls

### 6. Reversible causal-shift clock

A 31-site discrete shift unitary transports a one-particle marker exactly one site per tick, gives a finite front of one hop/tick, and is exactly invertible after ten forward moves. Thus finite causal propagation **does not itself generate a thermodynamic arrow of time** or establish a value for `c` without externally chosen length/time units.

### 7. Operational Wilson-cycle interferometer

A square with a nonzero `Z3` link sum remains nontrivial under **all 81** vertex-gauge assignments. Its gauge-invariant loop flux corresponds to an ideal equal-arm relative-phase interference bright-port probability `1/4`, contrasted with `1` for trivial flux. This is a finite Wilson-phase falsifier, not a derivation of exceptional gauge gravity or a demonstration of physical E6 holonomy.

### 8. Randomness/encryption operational distinction

An injective deterministic generator mapping 8 random seed bits to 16 output bits occupies only 256 of 65,536 possible 16-bit words. The total-variation distance from the *true uniform 16-bit distribution* is exactly `255/256`. Thus full-distribution distinguishability is mathematically large even if a computationally bounded observer without the generator description cannot distinguish a secure pseudorandom stream. `Unknown`, `computationally unpredictable`, and `ontically quantum-random` are distinct notions.

## Prior-art filter and reproducibility

- Parallel local `analysis/w33_pass12670_tick_rate_minkowski_action.py`: four null-ray proper-time action; not touched.
- Parallel local `analysis/toe_20261114_multi_holonomy_common_section.py` and related C6/differential-form scripts: not touched.
- Existing `analysis/w33_20261009_toe27_heat_spectral_dim_and_sector_no_go.py`: already rules out simple raw graph continuum; we use **Cartesian cycle-factor controls** instead.
- Existing `analysis/PASS12669_F8_CONSTANT_CLOSED_FORM_COS_2PI_9.md`: numerical identification; our output adds an exact rational upper-bound witness.
- Test: `py -3 -m pytest tests/test_toe_20261114_eight_orthogonal_fronts.py -q`; certificate producers each write their own JSON.
- External contextual research, not relied upon for exact proof: Hohm & Samtleben on E6 ExFT, https://arxiv.org/abs/1506.01065 ; Prieto–Quirant–Shukla on non-geometric-flux no-go conditions, https://arxiv.org/abs/2402.13899 ; Singh et al. on time-bin photonics, https://arxiv.org/abs/2507.08102 .

**Research integrity:** all claims are strictly conditional on the defined state/graph/channel/model. There is no full E6 compactification, proof of optimal MUB certainty, emergent Einstein dynamics, universal optical gate or completed TOE.
