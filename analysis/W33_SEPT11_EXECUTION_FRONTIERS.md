# September 11: current intake and five execution frontiers

Four software/mathematical follow-ups are executed below. Physical reset
collection remains blocked by absent instrument data. This extends
`W33_FIVE_COMPUTATION_FOLLOWUPS.md` and credits the intervening parallel work.

## What changed

GitKraken intake covers W33 `ffbb297ff..3d981d09e` (146 commits, 124 net-changed
paths) and Holotrade `49c10ab..a1df519` (147 commits, 109 paths). The manifest
`W33_SEPT11_CHANGE_INTAKE.json` hashes all 233 paths and records Python syntax,
JSON parse results, declared certificate status and source summaries. These are
structural checks, not independent theorem verification. Detailed source review
focused on the existing guest/compiler, durable owner, observer observability,
support min-entropy, E7/D4 Pauli normal form, and Holotrade hybrid decoder/traps.
A complete semantic read of all 38,595 diff lines and all intermediate commits
is still unfinished; the manifest does not count as that reading.

The intervening W33 work establishes the 85-state Marcelis model's exact
four-output observability, contextuality terminology corrections, Heawood/spread
and binary-tetrahedral phase comparisons, and Schur/E7/Pauli object maps.
`w33_e7_d4_presymplectic_reye_normal_form.py` explicitly distinguishes a
rank-two restricted symplectic form from a nondegenerate two-qubit space.
Those carrier distinctions must survive any VM/compiler interpretation.

Holotrade now has mass-40 depth-five birth summaries, Steinberg M8 matrix units,
representation-history commitments, and actual radius-two traps escaped by a
hybrid circuit decoder. In particular, the proposed escape search has already
been done: `octet_circuit_decoder_trap_certificate.json` owns the two mass-28
examples. We add an independently checkable stopping certificate below.
Mass-40 census completeness and the full M8 theorem are recorded prior results;
this packet does not rerun those large computations.

## 1. Durable redundant guests

`w33_durable_redundant_guest.py` wraps the existing two-register guest ABI in an
SQLite owner. It reuses the transaction and fault-boundary machinery from
`w33_durable_microstep_owner.py`, with a separate guest table/schema.
Every submission obtains the writer lock, reads the current authoritative head,
verifies the receipt against it, and atomically replaces both guest state and
its exact four-root live closure. Installation creates trusted nonnegative
counters and binds each pair to its process session. Duplicate or foreign
receipts cannot consume the same current head twice.

`tests/test_w33_durable_redundant_guest.py` passes four tests: restart after every
step across nine transfer guests; real process death before and after commit;
competing writers with exactly one acceptance plus cross-process/forged-control
rejection; and wrong-image/missing-closure rejection. This is macro-receipt
consumption, not durable interruption inside each arithmetic microstep.
Database rollback attacks, physical power failure and external I/O remain
outside the claim. Snapshot cost is proportional to live closure, not constant.

## 2. Controlled ninth-root phases in Clifford+T

`w33_qutrit_clifford_t_compiler.py` lowers every gate of the previous target ISA
into F, X, S, SUM and T, where S=diag(1,1,omega),
T=diag(1,zeta,zeta^-1), omega=zeta^3 and zeta^9=1.
All arithmetic in phase exponents is modulo 9. Two identities do the work:

    2[(a+b+c)^3-(a+b)^3-(a+c)^3-(b+c)^3+a^3+b^3+c^3] = 3abc
    7b^3-2(b+a)^3-2(b-a)^3 = 3 delta(a,0)b

The first compiles product-controlled addition; the second compiles an
equality-controlled shift. Cubing a residue modulo 3 is well-defined modulo 9,
so SUM parity computation, T powers and uncomputation implement the identities
exactly. Fourier conjugation converts phases to shifts.

For a controlled R9=diag(1,zeta,zeta^2), compute a control-equality flag f into
one clean qutrit, compute f*b into a second, apply R9=T*S to that workspace,
and uncompute. Both workspaces return to zero, including on superpositions.
The full original eraser compiles to 794 gates on 11 qutrits, with 252 T-power
instructions (524 unit T/T-inverse applications). All 54 controlled-R9 basis
checks pass; an arbitrary complex state over all 19,683 original basis states
is embedded and checked through the full 177,147-dimensional circuit, with
maximum error below 1e-15. Removing S is detected by a phase-sensitive control.

This is a logical fault-tolerant gate-set decomposition, not a demonstration of
physical fault tolerance, a threshold, a calibrated pulse sequence, or optimal
T count. General controlled-qutrit synthesis is established prior art:
[Yeh and van de Wetering](https://arxiv.org/abs/2204.00552).

## 3. Adaptive privacy and guessing probability

`w33_adaptive_observer_privacy.py` synthesizes public causal policies with exact
Bayesian beliefs. At each output, the policy chooses masking using only past
public observations, time and remaining budget. Decisions themselves are
public; no secret state or future noise is available to the policy. Bellman
recursion exhausts deterministic causal policies in the finite declared model.
A separate forward traversal checks probability normalization, worst-case
budget and objective. Guessing scores are rational; Shannon logs are numerical.

For four carry timings of a uniform three-bit counter, one mask uses two fresh
seed bits. The optimum guessing probabilities compare as follows:

| Maximum masks | Best fixed subset | Adaptive optimum |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 15/16 | 7/8 |
| 2 | 53/64 | 49/64 |
| 3 | 49/64 | 351/512 |
| 4 | 665/1024 | 665/1024 |

At a four-bit worst-case retained-seed budget, the adaptive policy leaves
0.659380617 Shannon bits, versus 0.487200148 for the prior best fixed subset.
The guessing-optimal selected policy uses 9/8 masks on average; this does not
claim a global minimum expected storage among tied privacy-optimal policies.

The new parallel four-sample Marcelis observability theorem supplies a second
model. Instead of jitter, a mask suppresses one trace output completely:

| Maximum suppressions | Best fixed schedule | Adaptive optimum |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 77/85 | 71/85 |
| 2 | 57/85 | 47/85 |
| 3 | 15/85 | 15/85 |
| 4 | 1/85 | 1/85 |

Thus the exact observation map can be used to compile a better privacy policy,
not only an observer that decodes the hidden state. These are classical
side-information statements; they do not bound arbitrary quantum adversaries.

## 4. Dual-certified circuit escape receipts (Holotrade)

The companion `analysis/octet_dual_gap_receipts.py` reuses the two frozen
mass-28 traps and their known circuit. It verifies all 8,280 radius-two
endpoints, then constructs rational dual receipts for the circuit endpoints.
For incidence B, dual y and h=B-transpose*y,

    gap(x) = ||x||1 - y.e = sum_p (|x_p|-h_p*x_p) >= 0.

The receipt checker validates dual feasibility, the move digest, unchanged line
image, strict negativity descent and zero endpoint gap. Both known escapes
reduce negative mass 2 to the certified optimum 1, and gap 2 to zero.
`python3 -S analysis/octet_dual_gap_receipts.py --check` passes without any
solver or site packages, including three corruption controls. The portable
receipt therefore avoids trusting a caller-supplied optimum scalar. Discovery
uses SciPy; checking does not. The existing hybrid decoder remains unchanged.

## 5. Physical reset

`w33_reset_readiness_20260911.json` records BLOCKED_NO_PHYSICAL_DATA: no live
powercap energy counter or supplied reset-work sample is available. Two
provenance rejection controls pass. Synthetic analyzer fixtures are excluded
from physical results. Instrument collection remains unfinished.
