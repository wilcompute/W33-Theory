# Q4 / Fano Square Commutator Lift Theorem

Date: 2026-05-29

This combines the Fano wedge-dot law with the Q4 antipodal cover.

The previous theorem proved the axis-level law:

```text
Q4 / antipodal = K4,4
```

with the tetrahedral hinge selecting an affine/Fano split:

```text
4 affine points + 3 directions = 7 Fano axes.
```

The new theorem tests the square-face lift.

## Main result

Q4 has 24 square faces. Under antipodal complement, these form 12 quotient square cycles in

```text
Q4 / antipodal = K4,4.
```

These 12 quotient cycles split as:

```text
6 hinge cycles      = affine-line wedge commutators
6 non-hinge cycles  = dual dot/contraction commutators
```

Therefore:

```text
24 Q4 square faces
= 6 affine Fano lines * 2 commutator types * 2 antipodal Q4 lifts.
```

This is the precise square-face version of the earlier slogan:

```text
Q4 edges lift individual wedge/dot transitions.
Q4 square faces lift Fano-line commutator loops.
```

## Affine-line commutators

Let the four hinge-neighbor axes be affine points of AG(2,2), and let the three hinge-nonneighbor axes be directions / points at infinity.

For an affine line

```text
L = {p, p+d}
```

with direction `d`, there are two quotient square cycles.

### Primal / wedge cycle

```text
{hinge, d, p, p+d}
```

This cycle passes through the tetrahedral hinge and represents the wedge completion loop:

```text
p wedge (p+d) -> d.
```

### Dual / dot cycle

Let the three directions be

```text
d, d1, d2.
```

Then the dual cycle is

```text
{p, p+d, d1, d2}.
```

This avoids the hinge and represents the contraction-side commutator: the line direction is omitted, while the complementary directions encode the dual contraction frame.

So every affine line has:

```text
one primal wedge quotient square
one dual dot quotient square.
```

Each quotient square has two antipodal lifts in Q4, giving the factor of two.

## Verified counts

The verifier checks:

```text
Q4 square faces = 24
antipodal square pairs = 12
quotient square cycles = 12
six hinge/primal cycles
six non-hinge/dual cycles
non-hinge quotient edges = 12 point-direction incidences
```

and therefore:

```text
24 = 6 * 2 * 2.
```

## Tetrahedron flag interpretation

The 24 square faces of Q4 equal the 24 tetrahedron flags:

```text
Q4 square faces = 24 = tetrahedron flags.
```

This is no longer just a count. It now has a commutator meaning:

```text
Q4 square face = antipodal lift of a Fano affine-line commutator.
```

The six affine lines provide the six edge-like directions in the tetrahedral/Cl4 layer, and the two commutator types correspond to the wedge and dot sides.

## Tomotope bridge survives

The quotient graph still recovers the tomotope f-vector:

```text
V = 4  hinge-neighbor affine point axes
E = 12 non-hinge point-direction incidences
F = 16 quotient edges
C = 8  antipodal axes
```

So:

```text
(V,E,F,C) = (4,12,16,8).
```

## Updated architecture

```text
Q4 vertices     = 16 local 12-flag codecs
Q4 edges        = lifted wedge/dot transitions
Q4 square faces = lifted Fano commutator loops = tetrahedron flags
Q4/antipodal    = K4,4 axis graph
hinge choice    = AG(2,2) + line at infinity
Fano lines      = commutator constraints
```

## Compressed theorem

```text
The six affine Fano lines each produce two quotient commutator squares: one primal wedge square through the tetrahedral hinge and one dual dot square avoiding the hinge. Each quotient square has two antipodal lifts in Q4. Thus the 24 square faces of Q4 are exactly the lifted wedge/dot commutator loops, matching the 24 flags of the tetrahedron.
```

## Honest boundary

This proves the square-face commutator lift. The next valid test is to build the actual chain complex: Q4 vertices as codec states, Q4 edges as transition operators, Q4 square faces as commutator relations, and then compute boundary ranks / homology over F3 to see whether the resulting ternary fibered complex lands in the known H1=81 phase-frame rank.
