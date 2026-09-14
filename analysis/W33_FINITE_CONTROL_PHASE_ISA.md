# Finite controls, durable continuations and an exact phase ISA

This executes the five followups from `W33_REYE_PORTS_FRAMES_ECHO_STREAMS.md`.
The additional TOE investigation connects the existing projective/phase-fibre
work to observable computational interfaces. It supplies an explicit map and
an obstruction, not a new group classification or a particle identification.

## 1. Finite-duration imperfect echoes

`w33_reye_finite_control_costs.py` replaces instantaneous echoes by square pulses
with finite Rabi speed, always-on X2 crosstalk, and a separate fractional echo
amplitude error. The sector drive is off during each echo. Five parameter pairs,
four cycle counts and all twelve sector/axis settings are simulated using full
8 by 8 matrices. Certificate rows report worst infidelity and leakage.

At speed 100 and zero echo error, sixteen cycles have infidelity 1.44e-9.
With 0.1% echo amplitude error, the sixteen-cycle infidelity becomes 0.05498,
while one cycle gives 0.0002675. Sixteen-cycle leakage is still only 2.17e-9:
**small leakage can coexist with a large coherent logical error**. At 1% echo
error, no echoes wins among the tested counts. Duration includes every echo.
This is a synthetic Hamiltonian experiment, without measured calibration,
detuning, pulse shaping or open-system noise. It does not overturn the previous
ideal-echo result; it tests assumptions that result explicitly excluded.

## 2. Optimize the native implementation

For each of the 63 synthesized Pauli rotations, the new search enumerates
alternative shortest native conjugation templates (cap 32), carries a beam of
16 candidate programs, and performs exact rational-angle commuting merges.
The same ordered target program costs **264 native pulses versus 301**, a
37-pulse reduction. Full-unitary maximum entry error is 1.293e-15; every emitted
word belongs to the declared native alphabet. The certificate stores the actual
program, not only a gate count. Beam width and template limits preclude a global
optimality claim. This repairs the previous abstract-frame/native-cost gap by
optimizing the lowered realization directly.

## 3. Durable continuation with a rollback boundary

Holotrade `scripts/w33_checkpoint_store.py` stores checkpoints and a separately
trusted revision/digest anchor in attached SQLite databases. DELETE journals,
FULL synchronization and one transaction cover both heads. Revision compare-
and-swap rejects stale writers. Reads compare the anchor and checkpoint heads
and hash the stored wire before exposing it.

`js/w33-durable-dual-stream.js` binds that storage to the existing decoder:
replay validates the policy and every move, and saves require strict extension
of the current prefix. Twelve decoder transaction tests pass, including real
process restart, before/after-commit crashes, stale writes, prefix rollback,
wire corruption, restoring an old data file, and resumed signed delivery.
The existing continuation transaction regression is also run separately.

The anchor must remain outside the data rollback adversary's authority.
Restoring both files defeats this scheme. This is a local trusted-storage
contract, not hardware monotonicity, remote attestation or exactly-once delivery.
The SQLite multi-file atomicity condition is documented in its official
[ATTACH documentation](https://www.sqlite.org/lang_attach.html); WAL is
intentionally excluded. Prior W33 `w33_durable_microstep_owner.py` already owns
SQLite guest durability and explicitly excludes restored-database detection.
This packet adds the independent anchor to the Holotrade stream path.

## 4. Exact multiplication for all 48 quartic lifts

Prior `w33_schur176_sixteen_line_fibre_structure.py` owns the A4/48 classification;
`w33_schur_cross_kernel_matrices.py` owns its Pauli kernel and chart. The new
`w33_schur48_phase_isa.py` builds the complete executable algebra:

    omega = (-1 + i sqrt(3))/2
    C = omega * (-I + i(X+Y+Z))/2, C^3 = I
    U(p,a,b,k) = i^p Z^a X^b C^k

Here p is modulo 4, a,b modulo 2, and k modulo 3. Conjugation by C gives an
explicit order-three automorphism alpha of the Pauli16 kernel. Multiplication
is `(g,k)(h,l) = (g alpha^k(h), k+l mod 3)`. The JSON stores all 48 matrices,
all 2304 products, a 12 by 12 projective table and its central phase cocycle.
All 110592 associativity triples and 1728 cocycle triples pass. Exact generator
identities plus exact closure prove quartic preservation; the Hessian character
is omega^(2k), with kernel order 16. This finite gate group alone is not a
universal quantum gate set.

## 5. Schedule for both memory exposure and overlap

The control certificate exhausts 108 normalized schedules for four disjoint
CNOT jobs sharing two hard ports. The synthetic score is
`L = 8 * memory_rate * duration + overlap_rate * cross_port_overlaps`.
For memory rate .001 and overlap penalty .1, four ticks with no overlap score
.032, versus .216 for the fastest two ticks. With rates .1 and .001 the
minimum-duration schedule wins. Chosen schedules reproduce the full 256-state
permutation. The reported `(1-exp(-2L))/2` is the parity probability for this
scalar Markov exposure model, not a general many-qubit fidelity formula.
Optimality applies only to the enumerated bounded schedule model.

## Additional TOE connection: equivalence depends on the observer interface

The existing `w33_projective_phase_fibre_dichotomy.py` already distinguishes
projective data from central phase completions; the previous Clifford compiler
already retains scalar phase. The new bridge makes the distinction directly
executable in the quartic group. The projective Z and X classes commute, but
any exact lifts have commutator -I. The cocycle entries are 0 and 2 modulo 4.
Rephasing a section adds a coboundary whose antisymmetric part is zero on this
commuting pair. Therefore **no scalar convention removes the phase extension**.
This is the standard Pauli obstruction instantiated in this existing geometry.

There are two precise observation maps. Standalone channels identify U and iU.
For a known phase-referenced implementation, controlled U is diag(I,U), and
controlled iU is a different circuit. Applied to a plus ancilla, the four
central lifts give Bloch coordinates (1,0,0), (0,1,0), (-1,0,0), (0,-1,0).
The exact witness checks these outcomes. A compiler/cache/receipt interface
that promises coherent control must therefore retain the phase cocycle and
phase-reference contract; a projective cache key alone loses required data.
This is a concrete VM design consequence, not evidence that global phase is
observable without a reference. Control of a completely unknown unitary is
not available from black-box circuit access alone; see
[Araujo et al., Quantum circuits cannot control unknown operations](https://arxiv.org/abs/1309.7976).

This suggests an operational TOE research question: which additional observer
interfaces distinguish completions that a geometric quotient identifies?
The present witness answers only the known coherent-control case. It does not
derive spacetime dynamics, particle masses, quantum gravity, or a device.

## Intake and reproduction

W33 baseline: 47c1b2401. Holotrade intake: 1518cf9 through 5500c22, five parallel
commits, with the full net diff read. The parallel orientation/stabilizer results
are credited there to Passes 4811/4814 and BT170; this packet does not claim them.
The two-27 source samples some group checks, so its prose is not imported as a
new independently exhaustive proof. Full historical semantic intake and the
older full-paper reading backlog remain incomplete.

Run `OPENBLAS_NUM_THREADS=1 python3 analysis/w33_reye_finite_control_costs.py`
and `python3 analysis/w33_schur48_phase_isa.py`. In Holotrade run
`node --test tests/w33-certified-decoder-transaction.test.js` and the existing
`tests/w33-continuation-transaction-crossrepo.test.js`. Workflows retain these
checks. No hardware data was collected.
