# Five computation follow-ups, 2026-09-09

Four software investigations executed; the physical reset experiment remains
blocked by missing instrument measurements. This packet extends the existing
`W33_EIGHT_COMPUTATION_EXPERIMENTS.md`, not a claim of new universality.

## Redundant guest ABI

`w33_redundant_guest_abi.py` implements the existing Program/Instruction
INC/DECJZ/HALT interface with two logical registers represented by four roots.
The store-free verifier derives the branch, route and post-state, and binds the
proof to the program image and consumer-supplied expected parent. Each INC
increments P; each nonzero DEC increments N; equality selects zero. Induction
therefore preserves the existing natural-number counter semantics. Three guest
programs on 25 input pairs each pass 550 differential transitions against
`w33_authenticated_counter_machine.py`; six malformed/stale receipts are rejected.
The existing primitive owns the arithmetic result. Stateful exactly-once
consumption and serialized wire-format integration remain separate work.

## Two-qutrit target compilation

`w33_native_qutrit_seed_frontier.py` compiles the existing ternary eraser into
F, F-dagger, equality-controlled X, and equality-controlled
R9 = diag(exp(2 pi i k/9)). This is a declared logical target basis, not a
hardware calibration or complete fault-tolerant decomposition.
Let V = F-dagger R9 F, so V cubed = X. An A-controlled V followed by two
commutators that shift B by s=1,2 produces the exponent
1 + 2 delta(B,b) - delta(B,b-1) - delta(B,b-2) = 3 delta(B,b)
when A is active; otherwise all factors cancel. B is restored exactly.
Each doubly controlled shift becomes 19 elementary gates with no added ancillas.
The nine-qutrit eraser compiles to 44 gates, 24 of them two-qutrit gates.
All 18 control-level/direction gadgets pass all 27 basis inputs (486 checks),
and an arbitrary complex state passes the full 19683-dimensional circuit.
Removing a gate is detected. General controlled-qutrit synthesis is prior art:
[Yeh and van de Wetering](https://arxiv.org/abs/2204.00552) and
[Zi, Li and Sun](https://arxiv.org/abs/2303.12979). No optimality is asserted.

## Fresh-seed placement

Enumerating all 16 fixed subsets of four observations, with uniform three-bit
input and independent two-bit seeds at masked positions, gives:

| Retained seed bits | Minimum input leakage (bits) |
|---:|---:|
| 0 | 3 |
| 2 | 2.827819531 |
| 4 | 2.512799852 |
| 6 | 2.340619383 |
| 8 | 2.005034616 |

At four bits, only alternating subsets {0,2} and {1,3} attain the minimum.
Probabilities come from exact counts; logarithms are numerical. This is an
optimum within the stated finite policy family, not among all randomized or
adaptive channels. Retained seed storage is distinct from conditional seed
entropy: each masked position leaves 0.5 bit conditional on final counter and
record. Resetting retained seeds is a separate operation.

## Pencil dual geometry (Holotrade)

The companion `analysis/signed_pencil_dual_geometry.py` in Holotrade reads the
existing exact sampler certificate. For incidence B and dual y, define point
potential h=B-transpose y. The nonnegative gap sum(|x_p|-h_p x_p) vanishes at
an optimum, forcing zeros where |h|<1 and signs on saturated points.
Mass 12: 16 forced zeros, 18 positive/6 negative saturated points; active-column
rank 22 gives optimal affine dimension at most 2. Mass 16: 28 positive/12
negative saturated points; the latter induce a 5-regular graph; rank 25 gives
dimension at most 15. These are upper bounds, not exact face dimensions.
Separation margins 2 and 4 enforce negative mass at least 1 and 2 respectively.
These interpret two existing representatives, not a new census.

## Physical reset

Live readiness still reports BLOCKED_NO_PHYSICAL_DATA; no energy counters or
reset-work samples were supplied. The analyzer's synthetic controls remain
excluded from physical evidence. Four of five investigations are completed at
the software/mathematical scope stated above; physical collection is unfinished.
