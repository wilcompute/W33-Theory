# BT776 — The Corner is the Chart Center; the L-Mirror Points at Other Cubes

Closes the three BT775 boundary questions, exactly.

## T1: the duo corner vertex IS the chart center (6/6)

Every duo pair's two anchor edges share precisely the chart center p0.
The picture per (rectangle, reflection): t_k fixes p0 (it stabilizes the
chart), so p0 is a cube vertex of Fix(t_k); the cube graph Q3 gives p0
exactly 3 incident cube edges; the two duo lifts anchor on two of those
three.  The duo bit = which edge through the center.  The hinge datum is
now completely geometric:

```text
choose a reflection (dihedral phase, 6 ways)
   -> a skew-line cube containing the chart center
choose an arm (duo bit, 2 ways)
   -> one of the cube edges through the center
```

## T2: the Type-B mirror anchors on OTHER cubes (12/12 TT, disjoint)

All 12 L-anchors are pairs of TRANSVERSALS (never a special skew line),
and the two transversals are DISJOINT.  But a disjoint line pair is
itself the axis of another 3A1 involution (BT775: skew pairs = the 540
class).  So the Type-B anchor map sends each lift to ANOTHER cube:

```text
Type-A anchor: an edge of its own cube       (internal)
Type-B anchor: the axis of a different cube  (external)
```

Chirality (BT772: P vs L) is thus also the internal/external dichotomy —
self-reference vs cross-reference in the 540-cube web.  The induced
self-map of the 540-class (cube -> anchored cubes) is a new canonical
structure on the involution variety.

## T3: each cube edge is anchored by exactly 4 lifts

PSp(4,3) is transitive on the 6480 = 540 x 12 (cube, edge) slots
(orbit computed exactly), and the anchor assignment is equivariant, so
the 25920 Type-A anchor-uses distribute uniformly: 25920/6480 = 4 lifts
anchor every cube edge.  Combined with T1, the 4 lifts anchoring a given
edge (v, w) are the duo arms at chart centers v and w — 2 + 2, one duo
pair from each endpoint's side.

## Boundary

Open: the cube-web graph (540 nodes, edges = Type-B anchoring) — degree,
connectivity, spectrum, and whether it is a known strongly regular or
distance-regular graph on the 540 skew pairs; and whether the 4 = mu
anchors-per-edge tie to the mu = 4 gauge centers per nonedge (the lift
construction's own multiplicity).
