# BT1827 — Cyclic Residue / Winding Protection Theorem

## Context

BT1824 identified the fourth commuting finite operator

```text
C(x0,x1,x2)=sum_i (x_i - x_{i+1}) mod 12
```

inside the finite tuple algebra on the local `12 = 3 x 4` fibre.  The open physical layer from BT1826 was to realize the commuting finite operators as actual hardware/syndrome terms, not just as algebraic labels.

BT1827 resolves the first and cleanest of those terms.

## Theorem

The BT1824 cyclic-residue operator is exactly a discrete winding-number syndrome:

```text
C = 12 * winding.
```

For ordered triples on the 12-clock,

```text
(x0,x1,x2) in (Z/12)^3,
```

the residue always lands in

```text
0, 12, 24.
```

So the normalized quantity

```text
w = C/12
```

is an integer winding sector.

## NetworkX verifier

I built the collision-free ordered configuration graph of three distinct points on the 12-cycle:

- vertices: ordered triples with three distinct clock positions;
- edges: move exactly one coordinate by one clock step `+1` or `-1`, while remaining collision-free.

The verifier proves:

```text
total basis                  = 12^3 = 1728
collision-free vertices       = 1320
collision-free edges          = 3240
connected components          = 2
component sizes               = 660 + 660
component windings            = 1 and 2
```

Most importantly:

```text
every collision-free one-step move preserves C.
```

In the full one-step graph on all `1728` states, there are

```text
792
```

residue-changing edges, and every one of them touches a collision state.

Thus:

```text
changing C requires a collision / phase-slip boundary.
```

## Counts

The full residue profile is:

```text
C = 0   : 12
C = 12  : 1056
C = 24  : 660
```

The collision profile is:

```text
distinct              : 1320
double collision      : 396
diagonal collision    : 12
```

Once double collisions are removed, the `C=12` sector loses its collision part and becomes the second clean 660-sector:

```text
w = 1 : 660
w = 2 : 660
```

## Symmetry

Cyclic rotation of the ordered triple preserves the winding sector:

```text
(x0,x1,x2) -> (x1,x2,x0)
```

Orientation reversal swaps the two collision-free winding chambers:

```text
(x0,x1,x2) -> (x0,x2,x1)
```

with profile:

```text
w=1 -> w=2 : 660
w=2 -> w=1 : 660
```

## Interpretation

This is the missing hardware reading of the BT1824 `C` term:

```text
C is a topological winding/phase-slip syndrome on a 12-bin optical clock.
```

A collision-free perturbation cannot change it.  To change the syndrome, the system must pass through a collision state, i.e. a discrete phase slip.  This is exactly the kind of term that can be read by a winding/OAM/time-bin photonic register before we attempt the harder physical realization of the remaining BT1824 terms:

```text
P = strand mismatch projector
G = D4 glue parity
E = K4 quartet edge energy
```

## Boundary

BT1827 does not yet construct the full optical circuit for `P,G,E`.  It proves that `C` is already a genuine topological sector label, so the physical realization problem has now been split:

```text
C = topological winding syndrome, solved structurally.
P,G,E = remaining local Hamiltonian/syndrome terms.
```

## Files

```text
analysis/bt1827_cyclic_residue_winding_protection.py
data/bt1827_cyclic_residue_winding_protection.json
analysis/BT1827_cyclic_residue_winding_protection.md
```
