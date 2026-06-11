# BT773 — The Involution Cube Theorem

Hunting through the octahedron + mod-12 corpus (pencil octahedra BT508,
Richter octahedron BT507, octa-cube memory packet BT510/517/524, Z12/D12
clocks BT746/749) suggested that the fixed geometry of the canonical
presentation involutions should be a platonic object.  It is — one duality
twist away from the naive guess.

## Measured (canonical involution t of the test rectangle; exhaustive by
transitivity on the 540-class)

```text
Fix(t) = 8 points + 6 lines of W(3,3)
fixed points per fixed line: {2: 4 lines, 4: 2 lines}   (NOT 4,4,4,4,4,4)
fixed lines per fixed point: 2                           (NOT 3)
collinearity on the 8 fixed points: 4-regular
NON-collinear pairs: 12, exactly 3 per point
non-collinearity graph  =  CUBE GRAPH Q3      (networkx isomorphism)
|C_PSp(t)| = 48, acting FAITHFULLY on the 8 points with image 48
            =  Aut(Q3)  =  Z2 x S4  =  the full cube symmetry group O_h
```

## Theorem 1 (the cube)

The 8 fixed points of every 3A1 involution form a combinatorial CUBE under
non-collinearity: cube edges = the 12 hyperbolic (non-collinear) pairs.
The BT748 mystery order-48 inner centralizer is exactly the cube's full
symmetry group.  The BT748 coordinates upgrade to

```text
presentation pair  <->  (W33-cube tau, chirality, cube-symmetry element)
51840              =        540      x    2     x        48.
```

There are 540 cubes in W(3,3) (one per 3A1 involution), and each chirality
half-fiber is an O_h-torsor: the substrate's presentation space is a
bundle of cubes.

## Theorem 2 (the anchor bijection)

Across the 24 lifts of one rectangle, the (involution, anchor) data are
all DISTINCT: 12 P-anchors and 12 L-anchors, each used exactly once.
Lifts are faithfully labeled by their anchors.  12 + 12 = 24 = f, and the
12 matches the cube's 12 edges / the Z12 clock / the mod-12 layer of the
completed-prime-cube scripts (units {1,5,7,11} mod 12).

## Connection to the octa-cube memory corpus

The octa-cube packet (6,12,8) + (8,12,6) = (14,24,14) attached to each
"now" (BT510/517/524) now has a group-theoretic home: every presentation
involution carries the cube side (8 fixed points, 12 hyperbolic edges)
with O_h symmetry, while the pencil octahedra L(K4) at each point carry
the (6,12,8) side; chirality (BT772: P-axis vs L-axis) is the
cube-vs-octahedron duality direction inside Fix(t).  The Plucker/Q(4,3)
mirror swaps the two platonic faces of the same fixed geometry.

## Boundary

Open: the incidence role of the two special fixed lines (the ones
containing 4 fixed points each — an axis pair? their relation to the
2+2+2+2 line profile); whether the 12 P-anchors of a rectangle coincide
with the 12 cube edges of ITS lifts' involutions in a canonical pattern
(per-reflection: which 2 of 12); and pushing the cube bundle through the
BT760-771 Q(4,3) transport harness, where the cube/octahedron duality
should realize the chirality mirror explicitly.
