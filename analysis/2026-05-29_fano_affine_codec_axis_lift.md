# Fano / Affine Codec Axis Lift Theorem

Date: 2026-05-29

This continues the antipodal Q4 codec quotient theorem.

Previous result:

```text
Q4 antipodal quotient = K4,4.
```

Choosing the tetrahedral chirality axis as the hinge gave:

```text
4 hinge-neighbor axes
3 hinge-nonneighbor axes
```

and extracted the tomotope f-vector:

```text
(4,12,16,8).
```

The new result identifies those seven non-hinge axes as the Fano plane in affine form.

## Axis split

Let the tetrahedral chirality axis be the distinguished hinge axis.

Then the seven remaining axes split as:

```text
4 hinge-neighbor axes     = affine points of AG(2,2)
3 hinge-nonneighbor axes  = directions / points at infinity
```

So:

```text
7 toroidal axes = 4 affine points + 3 points at infinity = PG(2,2).
```

This is exactly the standard decomposition of the Fano plane into an affine plane plus a line at infinity.

## Non-hinge K4,4 edges

In the K4,4 quotient, the edges not incident to the tetrahedral hinge axis are exactly the edges between the four affine-point axes and the three direction axes.

There are:

```text
4 * 3 = 12
```

such edges.

The verifier checks that these 12 edges are exactly the affine point-direction incidences of AG(2,2).

Thus:

```text
12 tomotope edges = 12 affine point-direction incidences.
```

## Reconstructing the Fano plane

From the four affine points and three directions, reconstruct the seven Fano lines:

```text
1 line at infinity
6 affine lines
```

The verifier checks:

```text
Fano points = 7
Fano lines = 7
each line has 3 points
each point lies on 3 lines
Fano flags = 21
every pair of points lies on a unique line
```

So the seven toroidal axes are not just seven objects. They canonically carry the full Fano-plane incidence geometry once the tetrahedral hinge axis chooses the affine split.

## Tomotope extraction revisited

The tomotope f-vector becomes an affine/Fano incidence vector relative to the hinge:

```text
V = 4  affine points
E = 12 affine point-direction incidences
F = 16 all quotient edges
C = 8  all axes = hinge plus seven Fano points
```

So:

```text
(V,E,F,C) = (4,12,16,8).
```

This gives a much better interpretation of the prior extraction:

```text
4 = affine points
12 = affine point-direction incidences
16 = Q4-antipodal quotient edges
8 = hinge + Fano points
```

## Flag-codec reading

Each of the seven Fano axes carries one Csaszar vertex codec and one Szilassi face codec:

```text
7 axes * 2 endpoints * 12 flags = 168.
```

So:

```text
168 = |PSL(2,7)|
```

is the toroidal Fano-axis flag count.

The hinge axis carries the two tetrahedral chiral codecs:

```text
2 * 12 = 24.
```

Together:

```text
24 + 168 = 192.
```

## Compressed theorem

```text
Q4 / antipodal = K4,4.
Choosing the tetrahedral axis as hinge turns K4,4 into AG(2,2) plus a line at infinity.
The seven non-hinge axes are the seven Fano points.
The 12 non-hinge quotient edges are affine point-direction incidences.
Adding the line at infinity reconstructs all seven Fano lines.
The tomotope f-vector (4,12,16,8) is the affine/Fano incidence vector relative to the hinge.
```

## Honest boundary

This proves the Fano/affine incidence lift at the axis level. The next valid test is to attach concrete Csaszar vertex labels and Szilassi face labels to the seven Fano axes, then test whether Fano line triples correspond to legal triple interactions of vertex-codec/face-codec pairs.
