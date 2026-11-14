# 2026-11-14: Minimal unknown-charge readout, adaptive tomography, and a 47-axis erasure-robust full E6 qubit decoder

## Purpose and scientific boundary

This pass closes a previously unstated assumption in the repository's 12-axis J-odd logical-qubit readout: the decoder was **given** one of 180 minimal integral quaternionic charge points. We now first infer that charge using the 27 J-even Pauli coordinates, then reconstruct an arbitrary pure logical state on its CP1 twistor fiber. We give exact nonadaptive and single-sensor-erasure optima inside a restricted *separated Pauli measurement architecture*, plus an explicit ideal shot-noise budget and full 8×8 reconstruction.

Nothing here derives a spacetime action, an experimental photon device, or a Theory of Everything.

## 1. Exact theorem: 21 of 27 even Pauli observables suffice, and are necessary

Let the canonical E6 signed cubic have 45 triple supports among the 27 coordinates. Its 135-edge 2-section is the degree-10 Schläfli graph; every unordered edge appears in exactly **one** triple. The 180 charges have exactly three nonzero entries ±1 on one triple, subject to the specified sign product.

For a fixed measured coordinate subset M, let U be its complement. Then **M distinguishes all 180 charges if and only if U is independent in the Schläfli graph**:

- If U contains an edge (u,v), choose its unique supporting triple. The four permitted sign patterns include a pair differing only by simultaneous flips at u and v; both charges yield identical measurements on M.
- If U is independent, each triple has at least two measured coordinates. Distinct cubic supports cannot share two measured coordinates because an edge belongs to exactly one triple, and distinct permitted sign patterns on the same support differ at two coordinates. Therefore no two charges produce the same measurement vector.

The graph has independence number **6**, with **72** maximum independent six-sets. Consequently the optimal number of fixed J-even observables is **27-6=21**. We enumerate and check all 72 corresponding optimal menus, each yielding 180 unique ternary signatures.

### Adaptive measurement, ideal exact-expectation model

A deterministic entropy-greedy decision tree using the first valid 21-menu identifies all 180 charges with **8.0 expected queried axes** (uniform prior) and **worst-case 14**. These are *executed* depth counts, not an assertion of global adaptive optimality. Combined with three adaptive J-odd logical Bloch axes, the ideal full-state workflow uses **11 expected / 17 worst-case settings**, versus 24 settings when all 21 charge axes are measured nonadaptively. The universal installed no-erasure menu has 21 J-even plus 12 J-odd axes = **33**.

Producer: analysis/toe_20261114_E6_180charge_minimal_even_readout.py
Certificate: data/toe_20261114_E6_180charge_minimal_even_readout.json

### Conservative finite-shot charge-label guarantee

For a fixed known Pauli readout visibility eta, assume each shot is independent with outcome in ±1 and expectation eta z_i, where z_i is -1,0 or +1. Estimate each coordinate from n shots, divide by eta, then round to the nearest of -1,0,+1. Hoeffding plus the 21-axis union bound gives a sufficient per-axis sample count:

    n >= (8/eta^2) log(2*21/alpha).

For alpha=0.05, n=54 at eta=1 (1,134 total prepared copies per charge) and n=85 at eta=.8 (1,785 total). The bound is conservative and assumes calibrated independent identical preparations, no drift, and visibility independent of the coordinate.

## 2. End-to-end unknown charge + hidden qubit

Producer: analysis/toe_20261114_E6_full_unknown_charge_twistor_decoder.py
Certificate: data/toe_20261114_E6_full_unknown_charge_twistor_decoder.json

Using the committed native-coordinate-to-signed-Pauli dictionary, the 21 ternary expectations identify z, then construct the rank-two complex quaternionic projector

    Pi = (I8 + sum_{i=0}^{26} z_i P_i)/4.

For its corresponding tritangent, choose one J-odd Pauli from each of the three logical cosets covered by the fixed optimal 12-axis menu; let L_a=Pi Q_a Pi and r_a=<psi|Q_a|psi>. Then

    rho = (Pi + r_1 L_1 + r_2 L_2 + r_3 L_3)/2.

This was checked for **four random pure states on every one of the 180 fibers** (720 reconstructions) without supplying the charge label. Maximum density-matrix-entry error is **4.45e-16**, minimum fidelity greater than 0.999999999999999. Finite-shot charge-label simulations under calibrated visibility identified 719/720 trials at eta=1 using 54 shots/axis and 718/720 at eta=.8 using 85 shots/axis. These are stochastic outcomes under an ideal model, not device performance and not an end-to-end noisy density reconstruction after a misidentified charge.

## 3. Sharp one-axis-erasure theorem and 47-sensor decoder

A proper J-even menu omits at least one axis u. Since every graph vertex has degree ten, some measured neighbor v of u exists; loss of v leaves two adjacent unmeasured coordinates and causes a signed-charge collision. Therefore **to tolerate arbitrary failure of any one installed J-even sensor, all 27 must be installed**. The full set is sufficient because losing one leaves a one-element independent unmeasured set.

For the odd Pauli logical menu, the known 135 four-element logical cosets must each be hit at least twice. A 20-axis construction in six-bit Pauli labels is

    [1,3,12,13,14,15,21,22,24,25,36,38,40,41,42,43,49,50,62,63].

The exact 135×36 incidence check verifies twofold coverage. An independent OR-Tools CP-SAT search returned **INFEASIBLE** for 19 or fewer odd axes. Hence a **47-axis globally installed menu** (27 even + 20 odd) is sufficient and minimal **within the separated fixed-Pauli charge/logic architecture** to tolerate any single missing axis.

After any one axis fails, dynamically select an optimal 21-even menu avoiding it (each vertex belongs to at least one of the 72 sixers) plus three remaining odd logical axes, so the protocol still queries only **24 distinct settings per state**. We tested **all 47 failed-axis possibilities × all 180 charges = 8,460 independent random pure-state reconstructions** with worst matrix-entry residual **4.45e-16**.

Producer: analysis/toe_20261114_E6_47axis_erasure_robust_readout.py
Certificate: data/toe_20261114_E6_47axis_erasure_robust_readout.json

### Physical caveats

The 21/27/47 lower bounds apply to fixed J-even Pauli coordinate measurements for charge, and fixed J-odd Pauli logical axes for the fiber. They are **not** lower bounds for joint entangled POVMs, arbitrary continuous HP3 charge points, or correlated measurement channels. A missing sensor is not a lost quantum carrier, an error-correcting code, or hardware failure tolerance beyond the specified axis-availability model.

## 4. Relation to the simultaneous five physics fronts

A concurrent research pass published an independently developed five-front extension as [GitHub commit 8897f165](https://github.com/wilcompute/W33-Theory/commit/8897f165f37eb44e927d4adcabe5e17734d449a9): (i) four-copy estimation of the design fourth-moment discrepancy 1/9 vs 1/33, with power under visibility; (ii) an ExFT five-vs-six section cross-constraint audit and a toy symmetric interface barrier (not a vacuum-selection action); (iii) noisy reconstruction conditional on known charge and an optimal **20-axis** odd one-sensor-dropout menu; (iv) constructive one-radian fixed-angle gate words that are physically meaningful as ideal unitaries but very deep; and (v) PySAT/CaDiCaL re-encoding of the n=5 size-eight maximal-Pauli-MUB question. Its bounded-conflict CDCL runs remain **UNDECIDED**; a verified external UNSAT certificate does not yet exist.

This present work is separate and independently checks the 20-axis twofold covering optimum and demonstrates how that result composes with previously published 180-charge twistor geometry. Do not attribute the parallel five-front claims or code to this independent contribution.

### Scholarly context

- Hohm and Samtleben, *Exceptional Field Theory I: E6(6) covariant form of M-theory and type IIB*, https://arxiv.org/abs/1312.0614 . The section constraint and its M/IIB alternatives are established theory, not independently derived from this tomography model.
- Qin et al., *Optimal Allocation of Pauli Measurements for Low-Rank Quantum State Tomography*, https://arxiv.org/abs/2411.04452 . Optimal shot allocation and low-rank tomography have extensive prior literature; our sharp 21/27/47 counts concern only the specific signed 180-charge finite ensemble.
- Kueng and Gross, *Qubit stabilizer states are complex projective 3-designs*, https://arxiv.org/abs/1510.02767 . The projective design framework predates these signed E6 calculations.

## Independent further falsifiers

1. Identify joint even/odd Pauli menus or general POVMs beating 33 ideal or 47 one-sensor-erasure installed axes; this would not refute the restricted theorems.
2. Stress the 47-axis construction with correlated detector noise, wrong visibility calibration, and sensor cross-talk; quantify any breakdown.
3. Extend charge identification to a continuum of HP3 charge points, where 180 distinct ternary signatures no longer apply.
4. Build a short-word synthesis of the compact USp8 gate set from its one fixed irrational rotation; the verified naive fixed-angle compiler has unfavorable pulse counts.
5. Obtain an externally checkable UNSAT certificate for the five-qubit Pauli MUB size-eight exclusion, and a physical section-selection mechanism from an actual ExFT action. Neither follows from finite incidence identities.
