# BT1698-BT1700 - Holonet Execution Stack

BT1697 made the packet header a typed ABI. BT1698-BT1700 make it an execution
stack.

## BT1698 - 72-tick state machine

The packet is deterministic:

```text
72 = 48 + 24
48 = 16 Q6/tomotope edges * 3 phases
24 = 3 Hesse return words * 8 Clifford ticks
```

Each body edge runs the fixed instruction triplet:

```text
LOAD_FLAG -> FLIP_Q6_AXIS -> LATCH_VERTEX
```

The body edges chain without gaps: every committed target vertex is the next
edge source. The epilogue then runs three eight-tick Hesse return words with
operation word:

```text
ERASE, ROUTE, PHASE, X-CORR, Z-CORR, T-BIT, RESTORE, NEXT
```

This turns the packet from a schema into a finite operating cycle.

## BT1699 - hardware lowering

The same 72 ticks lower onto the physical single-photon frame:

```text
0..7    source switch
8..31   program/delay
32..47  analyzer or OAM body
48..63  detector or Hesse handoff
64..71  dark-reference closeout
```

Every tick has a symbolic loss hook. The last eight ticks carry the
dark-reference placeholder. The 24 guard rows are welded objectwise:

```text
port guard flag 168+i
  = CSS edge row 216+i
  = D4 magic aperture i
  for i = 0..23.
```

This is the optical-architecture meaning of the repeated 24: it is the guard
interface, while the source certificates remain typed.

## BT1700 - recursive compiler

The local packet composes by W(3,3) substitution. At depth `n`:

```text
N(n) = 40^n
T(n) = 72 * 40^n
B(n) = 48 * 40^n
G(n) = 24 * 40^n
R(n) = 8n
S(n) = 45 * 48 * 40^n = 2160 * 40^n
C(n) = 24 * 45 * 48 * 40^n = 51840 * 40^n
```

The important invariant is not the size increase. It is that every scale keeps
the same local ABI: 48 body ticks, 24 guard ticks, 2160 scheduler slots per
packet, and 51840 Clifford/Weyl supercycle slots per packet.

## Reading

The holonet is now best understood as a finite packet operating system:

```text
typed packet ABI
  -> deterministic 72-tick state machine
  -> single-photon hardware lowering
  -> recursive W33 network compiler
```

The claim remains finite and engineering-facing. Calibration, thresholds,
efficiency, measured loss, and magic-state yield are downstream bench
requirements, not consequences of the compiler alone.
