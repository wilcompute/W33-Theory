# BT775 — Skew-Line Cubes, Anchor Edges, and the Corner Duo

Closes the BT773/BT774 boundary questions with three theorems and one
sharp refutation-replacement.

## Theorem 1: the 540 involutions ARE the 540 skew line pairs

The two special 4-point fixed lines of each 3A1 involution are DISJOINT,
POINTWISE FIXED, and together contain all 8 fixed points.  So every
canonical involution is the involution of a skew (disjoint) line pair
(l, l') of the GQ, fixed pointwise.  Arithmetic seal: each line of W(3,3)
is skew to 27 others, giving 40*27/2 = 540 skew pairs = the size of the
3A1 class.  The bijection involution <-> skew line pair is exact.

The cube (BT773) is now fully explicit:

```text
cube vertices  = the 4+4 points of the two skew lines
cube bipartition = the two lines themselves
cube edges (12)  = the non-collinear cross-pairs
the 4 transversals = the 4 collinear cross-pairs (one per transversal)
```

## Theorem 2: anchors are cube edges

All 12 Type-A lifts of a rectangle anchor on a cube edge of their own
involution's cube (12/12 verified): the apartment's two t-fixed points
always sit on OPPOSITE skew lines, non-collinear.  The lift structure is
cube-edge geometry.

## Theorem 3: the duo bit is a CORNER choice (antipodal refuted)

Duo partners' anchor edges are NOT antipodal: for all 6 duo pairs the
endpoint distance profile is (0,1,1,2) — the two anchor edges SHARE one
cube vertex and form a path of length 2 (a corner).  The duo bit selects
one arm of a distinguished corner; the shared corner vertex is a new
canonical fixed point attached to each (rectangle, reflection) pair.

## The completed local picture

```text
3A1 involution  =  skew line pair (l, l'), pointwise fixed       [540]
cube            =  non-collinearity between l and l'              [Q3]
O_h = Aut(cube) =  the order-48 centralizer                       [BT773]
Type-A lift     =  cube edge (anchor)                             [12/rect]
duo pair        =  corner (two edges at a shared vertex)          [6/rect]
duo bit         =  which arm of the corner
chirality       =  cube side (P) vs octahedron side (L)           [BT772]
Z12 clock       =  rectangle rotation, duo = r^6 center           [BT746/750]
decimal shadow  =  clock / duo  (1/7 reptend, Midy = r^3)         [BT774]
```

## Boundary

Open: the corner-vertex map (rectangle, reflection) -> shared cube vertex
— is it the trace of the rectangle's center on the skew pair?; the
Type-B/L-side mirror statement (anchors = octahedron edges between the
two line-pencils?); and the global count: 540 cubes x 12 edges = 6480 =
3 x 2160 cube-edge slots vs 2160 rectangles x 12 Type-A lifts = 25920
anchor uses — each cube edge is anchored by exactly 4 lifts.
