# BT1853 — Optical Code Compiler

BT1853 compiles the K12/F12 face-and-edge structure into a finite GF(3) optical incidence code.

## Code parameters

```text
total symbols = 72
payload edge symbols = 66
parity symbols = 6
rate = 11/12
field = GF(3)
```

## Payload

The 66 payload symbols are the complete-pair edge rotations:

```text
edge {i,j} <-> F12 rotation R_ij
```

## Six parity rows

Group edges by cyclic distance `d = 1,...,6` on `Z/12Z`.

```text
d = 1: 12 edges + one parity symbol -> row weight 13
d = 2: 12 edges + one parity symbol -> row weight 13
d = 3: 12 edges + one parity symbol -> row weight 13
d = 4: 12 edges + one parity symbol -> row weight 13
d = 5: 12 edges + one parity symbol -> row weight 13
d = 6:  6 antipodal edges + one parity symbol -> row weight 7
```

Each parity symbol stores the negative cyclic-distance class sum over GF(3).

## Link to BT1852

BT1852 showed:

```text
44 face words close mod 12
32 ordinary flat faces
12 antipodal-flat faces
0 nonzero-twisted faces
```

Therefore the sixth parity row has a distinguished role: it stores the antipodal sheet check, not generic curvature.

Boundary: this is a finite syndrome/check compiler.  It is not yet a proof of quantum code distance.
