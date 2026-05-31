# Singer Hexagon Affine Completion Canonicality

Date: 2026-05-31

This resolves the boundary from the Singer quotient local-12 theorem.

Previous theorem:

```text
84 directed toroidal flags = 12 Singer orbits of length 7.
```

A reference Szilassi hexagon intersects each Singer orbit exactly once, so the Singer quotient local-12 is natively the directed side-codec of one Heawood hexagon:

```text
12 = 6 C6 boundary carriers * 2 orientations.
```

The question was whether the bridge from this directed `C6` codec to the affine directed-`K4` codec is canonical.

## Main answer

The answer splits into two parts:

```text
Affine completion point:
    canonical

Directed C6 -> directed K4 bijection:
    orientation-relative
```

## Canonical affine completion

A Heawood hexagon alternates between:

```text
3 Fano point vertices
3 Fano line vertices.
```

Let the three Fano point vertices be:

```text
p, q, r.
```

The missing fourth affine point is:

```text
x = p + q + r.
```

The verifier checks this for all seven hexagons in the concrete Singer cycle.

This completion is independent of cyclic orientation because it only depends on the unordered set `{p,q,r}`.

So each Singer hexagon canonically determines an affine `AG(2,2)` chart:

```text
{p, q, r, x}.
```

## Singer equivariance

The verifier checks that the Singer generator transports completions correctly:

```text
completion(g · hexagon) = g · completion(hexagon).
```

Thus the seven affine completions form a Singer-equivariant 7-cycle.

So the canonical completion is globally compatible with the concrete Singer phase.

## Orientation-relative C6 -> K4 bijection

To map the directed `C6` side-codec to directed `K4` edges, one needs a cyclic orientation of the hexagon.

The verifier checks:

```text
with the concrete cyclic orientation, each hexagon gives a bijection
12 directed C6 flags -> 12 directed K4 edges.
```

It also checks Singer-equivariance of these bijections:

```text
transporting the C6->K4 bijection by the Singer generator gives the next hexagon's C6->K4 bijection.
```

So the concrete toroidal/Singer phase supplies a coherent orientation across all seven hexagons.

## Orientation reversal

The verifier also reverses the cyclic orientation of a reference hexagon.

Result:

```text
reversal preserves the same 12 directed-K4 image set
but changes the pointwise bijection.
```

Therefore the directed-codec identification is not orientation-free.

It is canonical only after choosing the cyclic orientation supplied by the toroidal rotation/Singer phase.

## Correct statement

The corrected bridge is:

```text
C6 side-codec:
    native Singer quotient local-12

AG(2,2) completion:
    canonical from p+q+r

C6 -> K4 directed-edge bijection:
    depends on cyclic orientation

Singer/toroidal phase:
    supplies coherent orientation across all seven hexagons
```

## Relation to earlier work

This clarifies why the local 12 keeps appearing in slightly different forms:

```text
C6 side-codec:
    six boundary carriers * two sides

K4 edge-codec:
    six tetrahedral edges * two orientations
```

They are not natively the same graph.

But each Singer hexagon canonically completes to an affine tetrahedron, and the toroidal orientation gives a compatible bijection between the two local 12-codecs.

## Compressed theorem

```text
For each hexagon in the concrete Singer phase, the three Fano point vertices p,q,r determine a canonical fourth affine point x=p+q+r, completing the hexagon's Fano triangle to AG(2,2). These completions are Singer-equivariant. The bijection from the hexagon's 12 directed C6 side-flags to the 12 directed K4 edges of the completed affine chart is not orientation-free; reversing the hexagon changes the pointwise bijection. However, the concrete toroidal/Singer phase supplies a coherent cyclic orientation, making all seven C6->K4 bijections Singer-equivariant.
```

## Honest boundary

This proves the canonical completion and orientation-relative bijection. The next hard step is to compare these seven affine completions with the eight Singer/Sylow toroidal systems and determine whether changing the Sylow-7 choice changes the affine completion atlas by conjugation only, or introduces genuinely different local K4-codec identifications.
