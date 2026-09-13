# Reye routing, batch compilation, robust controls and Clifford frames

All five followups from `W33_REYE_FIVE_FOLLOWUPS.md` are executed. The runnable
W33 artifact is `w33_reye_network_robust_frames.py` and its frozen JSON; the
transaction implementation lives in companion Holotrade. These are finite
mathematical/software checks and explicitly synthetic control models.

## 1. Arbitrary connectivity with declared costs

`route(n, costs, a, b)` takes directed positive-integer CNOT costs. A SWAP needs
both directions and costs `min(2*c_ab+c_ba, c_ab+2*c_ba)`. The compiler moves the
control, performs the terminal CNOT, and reverses the swaps, preserving every
spectator. Dijkstra runs on twice the SWAP costs, excluding the destination
from interior paths, and minimizes over the terminal edge. Positive costs
allow the minimum to be attained by a simple path.

An independent exhaustive simple-path oracle matches all 210 ordered cases on
rings, stars and complete graphs with two through six qubits and asymmetric
costs. Full basis permutations verify the coherent gate, including spectators.
A direct edge costing 100 loses to a two-edge route costing 7. Disconnected
requests fail explicitly. Costs can encode an integer pulse or duration budget;
no hardware cost is inferred. Available tile-local and port CNOTs must be
supplied as actual graph edges. This is optimal in the declared routing grammar,
not among all CNOT circuits or placements. Prior optical graph-profile comparison
`w33_pass4652_weighted_holonet_routing_pareto.py` solves a different objective.

## 2. Beyond individual conjugation templates

`commute_reduce` moves a Pauli rotation through a commuting interval to merge
with an equal word, stopping at an anticommuting barrier. Angles are exact
rational multiples of pi; cancellation never silently drops global phase.
The batch of all 63 prior compiled rotations shrinks from **337 to 301 pulses**,
with full matrix discrepancy about `1.15e-15`. Eighty seeded random circuits
also pass full coherent comparisons. A three-pulse commuting sandwich reduces
to its middle pulse even though the matching terms are not adjacent.

This crosses template boundaries and leaves the former isolated-template cost
certificate intact. The optimization rule is established prior art, not a new
quantum compilation principle: [PCOAST](https://arxiv.org/abs/2305.10966) develops
Pauli commutation-based optimization. No global batch optimum is claimed.

## 3. Robust sector controls and their failure boundary

For sector projector `Q=(I+s Z2)(I+t X3)/4`, define `P=X1 Q`, `R=Y1 Q`
(and cyclic axes). They form a Pauli algebra on the selected two-dimensional
sector and vanish on its complement. The added analog control assumption is
simultaneous phased quadratures: `cos(phi) P + sin(phi) R`. Each quadrature is
a sum of four commuting base controls. This is not a compilation of that sum
into sequential fixed-axis pulses under the same error model.

With `R_P(theta)=exp(-i theta P)`, theta=pi/4 and
`phi=acos(-theta/(2*pi))`, use the symmetric BB1 sequence with angles
`theta/2, pi/2, pi, pi/2, theta/2` and axes `P, P_phi, P_3phi, P_phi, P`.
Its ideal matrix equals the selected gate and is identity on the other sectors.
BB1/composite compensation is prior art; see
[composite two-qubit gates](https://arxiv.org/abs/1503.08788).
The repository already contains SK1 on H1 in
`BT4065_BT4072_explicit_qsp_dirac_magic_gauge.md` and a spectral-notch extension
in `BT4073_BT4080_engineering_outside_box.md`. We cite these rather than claiming
composite-pulse protection is new here.

The new calculation tests all twelve Reye sector/axis settings on eight noise
rows, checking trace preservation, full average gate fidelity and worst-sector
leakage. At 3% common amplitude error, worst average infidelity falls from
`1.2336e-4` to `2.9913e-10`. Duration increases ninefold. At Markov dephasing
rate 0.001 in normalized Rabi units, fidelity falls from `0.9993024` (base)
to `0.9937610` (BB1). The mixed row with amplitude 0.03, detuning/crosstalk
0.001 and dephasing 0.0001 also gets worse: `0.9998058` versus `0.9992961`.
Static detuning and crosstalk are not compensated by this construction.

Thus amplitude-only success does not justify enabling BB1 unconditionally.
Calibration must determine whether the longer sequence helps the actual error
budget. These are synthetic parameters, not measured performance or a threshold.

## 4. Multi-step dual receipts in Holotrade

Companion `js/w33-dual-witness.js` now supports `dual-chain-v1`. The hashed
pre-execution policy includes `maxSteps` (1 through 256), geometry and allowed
move hashes. The verifier derives every intermediate vector with BigInt,
checks each move has zero incidence image and approved identity, verifies
actual negative mass against every strict-descent step, and matches the final
endpoint. The existing exact rational feasible dual with zero l1 gap proves
final global negative-mass optimality because four-regular incidence fixes
the coordinate sum. Intermediate states need not be optimal.

All eight transaction tests pass. New signed end-to-end cases have lengths
1, 2, 3 and 8 and repeat an existing certified circuit from a farther point
in the same fibre. Mutation tests cover truncation, extension, wrong moves,
summary drift, policy downgrade and invalid arithmetic. This does not expand
the certified circuit library. Legacy and one-step tests still pass; test
attestation verdicts are simulated. Full contract:
Holotrade `analysis/OCTET_DUAL_WITNESS_TRANSACTIONS.md`.

## 5. Exact Clifford action in the Schur kernel coordinates

Import the previously certified conjugator S from
`w33_schur_cross_kernel_matrices.json`, for which `S^-1 A S=Z` and `S^-1 B S=X`.
The new explicit generators are `S H S^-1` and `S diag(1,i) S^-1`; their entries
are exported exactly, and both preserve the supplied metric `diag(2,1)`.
Conjugation produces permutations of the sixteen labelled kernel matrices
`i^p A^a B^b`. Their closure has **24 elements**. All **6144** combinations
of frame map and kernel multiplication are checked exactly. Exported generator
words allow every frame transformation to be reconstructed.

Completeness: a unitary normalizer fixes scalars, sends Z to one of six signed
Pauli axes, and sends X to one of four signed anticommuting axes. These 24
possibilities are all attained. The kernel of conjugation is U(1), since X
and Z generate the full matrix algebra. Thus the full unitary normalizer is a
central extension by U(1), not a finite group of order 24. The finite maps are
projective Clifford classes and give an exact frame-update interface.

Normalizing the kernel is not proof of preserving its original quartic or the
whole eleven-block Schur configuration. That larger geometric action remains
separate. This is an explicit lift in existing coordinates of the standard
one-qubit Clifford normalizer, not a new classification of Clifford groups.

## Reproduction and intake

```
OPENBLAS_NUM_THREADS=1 python3 analysis/w33_reye_network_robust_frames.py
# Companion Holotrade:
node --test tests/w33-certified-decoder-transaction.test.js
```

GitKraken fetched both remotes before work: no commits beyond W33 `d06cf22d8`
and Holotrade `f985703` at intake. Result-index, source, JSON and visible-doc
searches checked the named constructions and exposed the older SK1 work.
The historical full-manuscript reading backlog is not represented as complete.
