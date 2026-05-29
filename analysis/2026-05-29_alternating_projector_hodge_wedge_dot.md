# Alternating Projector / Hodge-Star / Wedge-Dot Theorem

Date: 2026-05-29

This turns the previous flag-codec/Fano-axis picture into an operator algebra.

The guiding idea was:

```text
AG(2,2) / affine layer -> alternating projector
PG(2,2) / Fano layer   -> projective closure
tetrahedron            -> Hodge star
Csaszar                -> wedge / maximal vertex adjacency
Szilassi               -> dot / contraction / maximal face adjacency
```

The verifier confirms the finite operator version.

## Important group clarification

Strictly:

```text
AG(2,2)
```

is the affine plane with four points.

Its full affine symmetry group is

```text
AGL(2,2).
```

The verifier checks:

```text
|AGL(2,2)| = 24
AGL(2,2) acting on four affine points = S4
```

The even subgroup is

```text
A4 < S4,
|A4| = 12.
```

So the alternating object is not the affine plane itself, but the alternating/even subgroup of the affine symmetry group.

## Alternating projector

On the 24 tetrahedron flags, average over the A4 action:

```text
P_A = (1/|A4|) sum_{g in A4} g.
```

The verifier checks:

```text
P_A^2 = P_A
rank(P_A) = 2
```

So the A4-average projector collapses the 24 flags to two chiral flag-codec sectors.

Separately, the diagonal chirality projectors have ranks

```text
12 and 12.
```

Thus:

```text
A4 averaging sees the two orbit sectors.
chirality projectors isolate the two 12-flag codecs.
```

This is the precise alternating projector layer.

## Tetrahedral Hodge star

Represent a tetrahedron flag as

```text
(a,b,c,d)
```

where:

```text
vertex = a
edge = {a,b}
face = {a,b,c}
opposite vertex = d
```

Define the tetrahedral Hodge star / duality map by reversing the incidence chain:

```text
*(a,b,c,d) = (d,c,b,a).
```

The verifier checks:

```text
*^2 = 1
* preserves chirality
* commutes with the A4-average projector
* swaps vertex and face incidence
* sends each edge to its opposite edge
* preserves opposite-edge axes
```

This is exactly the self-dual hinge role of the tetrahedron.

## Wedge and dot/contraction layer

On the 16-blade Boolean/tetrahedral exterior algebra, the grade row is

```text
1,4,6,4,1.
```

This is simultaneously:

```text
Cl4 grade row
Pascal row 4
tetrahedron face lattice
Q4 Hamming-weight layering
```

Define unsigned support-level operators:

```text
wedge_i: add generator i if absent
dot_i: remove generator i if present
```

Then the Hodge star on blades satisfies, for each generator i:

```text
* wedge_i = dot_i *
```

at the incidence-support level.

So Hodge star conjugates exterior expansion to contraction:

```text
wedge <-> dot.
```

This is the exact operator interpretation of the Csaszar/Szilassi duality:

```text
Csaszar  = vertex/wedge/maximal-vertex-adjacency side
Szilassi = face/dot/contraction/maximal-face-adjacency side
tetrahedron = Hodge-star hinge conjugating the two
```

## Projective Fano closure

The verifier also checks the projective closure:

```text
PG(2,2) has 7 points and 7 lines.
Aut(PG(2,2)) = GL(3,2), order 168.
```

It verifies:

```text
projective group order = 168
Fano lines are preserved
the group is transitive on the 21 point-line flags
```

Thus the affine/alternating tetrahedral layer closes projectively into the Fano/PSL(2,7) layer.

## Final operator dictionary

```text
A4 alternating projector:
    chirality projector on tetrahedral 12+12 flag codecs

Hodge star:
    tetrahedral self-dual vertex-face duality, edge-axis preservation

Wedge:
    Csaszar maximal-vertex adjacency / exterior expansion

Dot product / contraction:
    Szilassi maximal-face adjacency / interior contraction

PG(2,2):
    projective Fano closure with automorphism group 168
```

## Compressed theorem

```text
AGL(2,2)=S4 acts on the four affine/tetrahedral points.
A4<S4 gives the alternating projector splitting 24 flags into two chiral codec sectors.
The tetrahedral Hodge star commutes with that alternating projector and swaps vertex-face incidence while preserving edge axes.
On the 16-blade Cl4/Q4 layer, Hodge star conjugates wedge to dot/contraction.
PG(2,2) closes the affine alternating layer to the 168-element Fano projective symmetry.
```

## Honest boundary

This proves the finite operator dictionary. The remaining hard step is to attach the actual seven Csaszar vertex codecs and seven Szilassi face codecs to Fano labels and verify a concrete wedge/dot incidence law on line triples.
