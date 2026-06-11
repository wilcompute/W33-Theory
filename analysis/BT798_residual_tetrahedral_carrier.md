# BT798 - Residual Tetrahedral Carrier

BT788 exposed one non-free compressed packet:

```text
16 + 16 + 8 + 8 = 48
```

BT798 identifies it.

## The Carrier

On directed W33 edges, the residual packet is exactly four disjoint directed
tetrahedra:

```text
4 * |E_dir(K4)| = 4 * 12 = 48.
```

On triangle-corners, the residual packet is the corner set of the same four
tetrahedra:

```text
4 * C(4,3) * 3 = 4 * 4 * 3 = 48.
```

So the edge residual and triangle residual are the same object.

The stronger fact is that those four tetrahedra are not abstract graph cliques.
They are exactly the four common transversal lines of the base skew-line pair.
For the base chart `(0,13)` the four lines are:

```text
{0,13,14,15}
{1,4,7,10}
{2,31,35,39}
{3,22,27,29}
```

## Structure

Each `K4` contains:

```text
one base antipode pair
one shadow antipode pair
all four cross edges between them
```

The micro-orbit classes are:

```text
8   base antipode matching, directed both ways
8   shadow antipode matching, directed both ways
16  base -> shadow cross edges
16  shadow -> base cross edges
```

This is the finite cost of killing the cube fixed diagonal bit.  The bit is not
thrown away; it is completed into the common-transversal tetrad.

## Why It Matters

Each tetrahedron has:

```text
4 vertices * 3 outgoing directions = 12 directed local moves.
```

That is exactly the unnormalized toroidal unit from BT789:

```text
(7-3)(7-4) = 4 * 3 = 12.
```

BT798 therefore fuses the three previous facts:

```text
BT787: R11 is the handle/cell octet
BT788: 480 has a residual 16+16+8+8 packet
BT789: the toroidal bridge is 4*3/12
```

into one concrete carrier: four tetrahedral phase packets.

## Validation

Run:

```bash
python3 analysis/bt798_residual_tetrahedral_carrier.py
```
