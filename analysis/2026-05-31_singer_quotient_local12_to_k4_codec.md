# Singer Quotient Local-12 to K4 Codec

Date: 2026-05-31

This resolves the next local-codec question from the concrete Singer phase theorem.

Previous theorem:

```text
84 directed toroidal flags = 12 Singer orbits of length 7.
```

The question was:

```text
What exactly are the 12 local phases?
```

## Main result

Choose one reference Szilassi hexagon in the concrete toroidal system.

The verifier checks that this reference hexagon is a cross-section for the Singer action:

```text
each of the 12 Singer flag orbits meets the reference hexagon exactly once.
```

Therefore the Singer quotient local-12 is exactly:

```text
12 directed side-flags of one Heawood hexagon.
```

Equivalently:

```text
6 boundary incidences * 2 directions/sides = 12.
```

So the native quotient codec is a directed `C6` side-codec.

## Native C6 codec

The reference Heawood hexagon has six vertices and six boundary edges.

The local 12 consists of the two directed orientations of each boundary edge.

The verifier checks:

```text
12 directed C6 edges
6 undirected carriers
each C6 endpoint has directed outdegree 2
```

So the native local object is:

```text
directed C6.
```

## Comparison with affine K4 codec

The affine-chart codec from earlier was:

```text
12 directed edges of K4 = 6 K4 edges * 2 orientations.
```

The verifier confirms an important correction:

```text
directed C6 is not intrinsically the same graph as directed K4.
```

Reason:

```text
C6 endpoint graph:
    6 vertices of degree 2

K4 endpoint graph:
    4 vertices of degree 3
```

So they are not natively graph-isomorphic.

## Fano-triangle completion bridge

A reference Heawood hexagon alternates between:

```text
3 Fano points
3 Fano lines
```

Those three Fano points form a Fano triangle.

Adding the missing fourth affine point

```text
x = p + q + r
```

completes that triangle to an `AG(2,2)` affine chart with four points.

After choosing the cyclic orientation of the hexagon, the verifier builds a bijection:

```text
12 directed C6 side-flags
    ->
12 directed K4 edges of the completed affine chart.
```

So the bridge is real, but it requires extra structure:

```text
Fano-triangle affine completion + cyclic orientation.
```

## Correct statement

The correct relationship is:

```text
Singer quotient local-12:
    natively directed C6 side-codec

Affine chart local-12:
    natively directed K4 edge-codec

Bridge:
    Fano-triangle completion turns C6 side-codec into K4 edge-codec by a bijection
```

They share the abstract form:

```text
6 carriers * 2 orientations/sides.
```

But their native graphs differ.

## Compressed theorem

```text
The 84 directed toroidal flags split into 12 Singer orbits of size 7. A reference Szilassi hexagon intersects each orbit exactly once, so the quotient 12 is the directed side-codec of a C6 hexagon. This native C6 codec is not graph-isomorphic to the affine directed-K4 codec. However, the hexagon is a Fano triangle of three points and three lines; adding the missing fourth affine point completes it to AG(2,2), and the cyclic orientation gives a bijection from the 12 directed C6 flags to the 12 directed K4 edges.
```

## Honest boundary

This proves the local quotient structure and corrects the naive C6=K4 identification. The next hard step is to determine whether the Fano-triangle completion is canonical for the concrete Singer phase or depends on the reference hexagon / orientation choice.
