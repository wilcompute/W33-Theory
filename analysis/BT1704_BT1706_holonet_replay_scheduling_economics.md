# BT1704-BT1706 - Holonet Replay, Scheduling, and Retry Economics

BT1701-BT1703 made the packet inspectable and fault-classified. BT1704-BT1706
turn the runtime layer into an operational model.

## BT1704 - replay runner

The 72-tick event log is replayed twice from the same initial state. Both runs
produce the same cursor, vertex, Hesse, and Pauli registers. The replay ends at:

```text
HESSE_WORD:5:DONE
```

with final corrections `X^1`, `Z^2`, and time-frame bit `1`.

## BT1705 - shared-bus time division

The finite `2160` mirror bus is scheduled as one packet per time slice. Three
profiles are certified:

```text
depth1_burst      40 packets arrive at once
depth2_wavefront  1600 packets arrive in 40 waves of 40
depth2_sequential 1600 packets arrive one per slice
```

All profiles are collision-free, every packet is served once, and Jain fairness
is exactly `1`. The wavefront profile exposes the engineering cost honestly:
finite shared-bus reuse is fair, but it has a bounded queue and latency.

## BT1706 - retry economics

BT1706 attaches symbolic rates to the BT1703 fault exits:

```text
LOSS       -> retry/reprogram or local dark closeout
DARK_CLICK -> local dark-reference termination
PARITY     -> CSS syndrome handoff
```

The verifier computes expected retry load, CSS handoff load, local termination
load, and guard-budget pressure for three deterministic profiles. These are
parameterized calculations, not measured hardware thresholds.
