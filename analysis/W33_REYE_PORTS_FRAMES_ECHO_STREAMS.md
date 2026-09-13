# Shared-port circuits, Clifford frames, echoed sectors and resumable proofs

This executes all five followups from `W33_REYE_ROUTING_ROBUST_FRAMES.md`.
The W33 artifact is `w33_reye_scheduled_frames_echo.py` and its JSON. The
companion runtime module is Holotrade `js/w33-dual-stream.js`.

## Shared-port simultaneous operations

`schedule(operations)` accepts directed CNOT operands, positive integer duration,
and named exclusive port resources. Input-order dependencies are retained on
every qubit. A deterministic earliest-start list heuristic overlaps operations
only when all their qubit and declared port intervals permit it. Both endpoint
buses are reserved for each crossing in the demonstration.

Two disjoint six-qubit routed operations take 26 ticks serially and **19 ticks**
with the shared buses. All dependencies and resource intervals are checked;
the scheduled and serial circuits agree on all 4096 basis states, hence on
arbitrary superpositions. A separate disjoint-qubit example confirms that an
extra shared port still forces serialization. The earlier one-bus experiment
reached 14 ticks; it is superseded by the stricter two-endpoint model, not
reported as the final result. Durations are declared abstract costs. This is
not an optimal makespan or an analog concurrency/hardware-bandwidth proof.

## Clifford propagation with a native-cost audit

`frame_compile` represents a product as non-Clifford Pauli rotations followed
by a terminal Clifford. Quarter-turn conjugation updates signed Pauli words;
rational angles and a physical realization of the terminal frame retain global
phase. Sixty seeded random circuits pass full coherent matrix comparisons.

The batch of 63 prior synthesized rotations factors into 63 abstract rotations
with no terminal frame. Relowering gives 337 native pulses, then the previous
commuting pass gives 301. **The abstract count 63 is not a physical pulse count.**
This batch does not improve on the former 301-pulse result.

There is a concrete gain beyond commuting-only reduction: the native sequence
`R_ZII(pi/4) R_XII(pi/7) R_ZII(-pi/4) R_YII(-pi/7)` becomes identity under
Clifford propagation, removing four pulses; commuting-only reduction leaves
all four. The mechanism is established compiler prior art, including
[Pauli-rotation optimization](https://arxiv.org/abs/1903.12456) and
[PCOAST](https://arxiv.org/abs/2305.10966). Earlier repository uses of Clifford
frame actions (`BT1450_BT1452_quartic_schedule_clifford.md` and
`BT1419_BT1421_frontend_unitary_magic_optimizer.md`) are distinct finite models,
not evidence that transformed Pauli rotations are free native operations.

## Joint amplitude and crosstalk suppression

Let `Q=(I+s Z2)(I+t X3)/4` and use the previous phased selected-sector controls.
The echo `E=Z2` commutes with each selected control Hamiltonian H and
anticommutes with modeled crosstalk `C=X2`. Split each BB1 segment of duration
`dt` into N symmetric cycles:

`exp(-i dt H_plus/(4N)) E exp(-i dt H_plus/(2N)) E exp(-i dt H_plus/(4N))`,

where `H_plus=(1+epsilon)H+cross*C`. Since E reverses C while preserving H,
the average crosstalk cancels. Full matrices test the residual at finite N,
without replacing the product by an average-Hamiltonian approximation.
The phase of implementing E via `R_Z2(pi/2)=-i E` must be corrected per pair.

All twelve sector/axis settings pass four signed joint-error cases. At amplitude
error 0.03 and crosstalk 0.01, worst full-register average infidelity is:

| Sequence | Worst infidelity | Worst sector leakage |
|---|---:|---:|
| Base selected rotation | 1.7680e-4 | 5.8392e-5 |
| BB1 alone | 3.1611e-3 | 2.1227e-3 |
| BB1 with 4 echo cycles per segment | 1.1271e-7 | 2.5294e-7 |
| BB1 with 16 echo cycles per segment | 7.2591e-10 | 9.6138e-10 |

The 16-cycle construction uses **160 echo pulses**, assumed instantaneous and
error-free, plus simultaneous phased sector controls. BB1 already has ninefold
base duration before those echoes. Thus the new result is conditional joint
suppression in a named ideal control model. It does not establish finite-pulse
robustness, detuning/dephasing protection or device performance. The prior
negative mixed-noise finding remains valid. Dynamic correction is established
literature; see [multiqubit dynamically corrected gates](https://arxiv.org/abs/2008.01168).

## Incremental exact proofs and resumable checkpoints

Holotrade `createDualStream(policy, header)` verifies every submitted move and
actual negative-mass decrease as records arrive. Ordered prefix digests bind
record indices, moves and summaries. Admission of a whole chunk is atomic.
Accepted prefixes explicitly report that optimality has not yet been verified.
`finish(dual)` runs the existing exact rational final-optimality verifier and
returns a receipt accepted by the signed transaction path.

`checkpoint()` exports bounded JSON history. `resumeDualStream` requires the
caller to supply a trusted expected checkpoint digest and replays the history.
A self-supplied hash is not authentication. Resume is O(history length); the
module supplies no independent storage durability, rollback prevention or
exactly-once delivery. Ten transaction tests pass, including serialized resume
into signed delivery, failed-chunk rollback, tampering with/without rehashing,
wrong order, absent trusted identity and recovery from an invalid final dual.

## Which Clifford frames preserve the actual quartic?

The prior `w33_schur176_sixteen_line_fibre_structure.py` already proves that
`phi(u,v)=u(u^3-v^3)` has projective stabilizer A4, with four scalar lifts per
symmetry. This followup identifies that group inside the **specific 24 Clifford
frame maps** constructed in the previous packet.

For each exported generator word in H and diag(1,i), form T and evaluate the
actual polynomial in the supplied Pauli chart `phi(S(x,y))`. Exactly **12 of
24** frames preserve it up to a unit-modulus multiplier a. The exact lift
condition `lambda^4*a=1` supplies four phase choices for each accepted frame:
**48 exact quartic-preserving lifts**. The JSON gives every accepted word,
its permutation of the sixteen kernel labels, multiplier, and phase equation.
All five quartic coefficients are compared exactly, not just root samples.

Evaluating the actual Hessian in the same chart gives the phase-corrected
character `b/a`; its three cube-root values occur four times each. Consequently
only four projective frames (sixteen scalar lifts) preserve both quartic and
Hessian. This recovers the existing K16 kernel through explicit Clifford maps.
It does not establish a global action on all eleven Schur blocks. The A4/48
classification is prior-owned; the concrete frame correspondence is the new
integration. External geometric source already cited by the prior witness:
[Nurowski's Schur/Reye study](https://arxiv.org/abs/2609.10751).

## Validation and intake

```
OPENBLAS_NUM_THREADS=1 python3 analysis/w33_reye_scheduled_frames_echo.py
# Companion Holotrade
node --test tests/w33-certified-decoder-transaction.test.js
```

GitKraken found no W33 commits after `0c10ea1ff` at intake. Holotrade `850d577`
was read in full (350 diff lines: source, certificate, tests) and pulled without
conflicts. That nucleus-bound work remains prior-owned; its general planar
improvement is conditional and q=7 is a recorded run, not recomputed here.
Historical full-manuscript reading and physical calibration remain outstanding.
