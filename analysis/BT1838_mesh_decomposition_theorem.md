# BT1838 — Mesh Decomposition Theorem

BT1835 assigned exact matrices to the optical primitives.  BT1838 lowers those matrices into mesh schedules.

## Universal two-mode mesh law

For an `N x N` unitary, a triangular Givens/Reck/Clements-style nullification mesh uses

```text
N*(N-1)/2 two-mode rotations
N output phases
```

when used as a direct exact compiler target.

## Schedules

### Qutrit sorter `F3`

```text
dimension = 3
two-mode rotations = 3
output phases = 3
```

### C12 winding analyzer `F12`

```text
dimension = 12
two-mode rotations = 66
output phases = 12
```

### D4 quartet encoder `H2 tensor H2 / 2`

Because the D4 glue register is `(Z2)^2`, the exact encoder is separable:

```text
layer 1: H2 on first bit
layer 2: H2 on second bit
balanced 50/50 couplers = 4
```

### Permutation primitives

```text
D4 parity ancilla: 6 logical XOR gates plus 2 chi offsets, dimension 256
K4 comparator: 2 bitwise XORs plus one multi-control flag, dimension 32
C12 phase-slip guard: equality flag on 144 valid clock pairs, dimension 288
```

## Interpretation

The continuous optical pieces are now reduced to exact two-mode mesh counts.  The discrete comparator/parity pieces are reduced to reversible permutation networks.

Boundary: this is a schedule theorem and resource count.  A later generated artifact should print the full numeric F12 phase table.
