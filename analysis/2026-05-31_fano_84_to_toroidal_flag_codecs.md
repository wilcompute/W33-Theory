# Fano 84 to Toroidal Flag-Codecs

Date: 2026-05-31

This connects the Fano 84 chart-codec to the recurring 84 flags of Csaszar and Szilassi at the abstract incidence-codec level.

Previous theorem:

```text
Fano 84 = 7 chart axes * 12 local chart states.
```

This theorem identifies the local 12 as the directed-edge codec of the affine tetrahedron.

## Local K4 codec

Choose a Fano line as the line at infinity. Its complement is an affine chart

```text
AG(2,2),
```

with four affine points.

A local chart state is

```text
affine anchor p + infinity direction d.
```

Since the direction d determines the non-anchor point

```text
q = p + d,
```

this is exactly a directed affine edge

```text
p -> q.
```

Therefore each chart has

```text
4 affine anchors * 3 directions = 12 directed edges.
```

Equivalently, since the four affine points form K4:

```text
12 = 6 undirected K4 edges * 2 orientations/sides.
```

The verifier checks:

```text
12 directed edges
6 undirected edges, each appearing twice
3 outgoing edges per affine vertex
3 incoming edges per affine vertex
3 directions, each appearing four times
reverse closure under p->q <-> q->p
```

So the local 12 is precisely a directed tetrahedral-edge codec.

## Global Fano 84

The Fano plane has seven possible chart axes:

```text
7 Fano lines = 7 choices of line at infinity.
```

Each chart has 12 directed K4-edge states.

Thus:

```text
84 = 7 * 12.
```

So:

```text
Fano 84 = seven chart axes * local directed-tetrahedron-edge codec.
```

## Csaszar 84

Csaszar has:

```text
7 vertices
21 edges
14 triangular faces
84 flags
```

At each vertex, the degree is 6. The local flag count at one vertex is:

```text
6 incident edges * 2 sides = 12.
```

Therefore:

```text
Csaszar flags = 7 vertex axes * 12 local vertex flags = 84.
```

## Szilassi 84

Szilassi is dual:

```text
14 vertices
21 edges
7 hexagonal faces
84 flags
```

At each face, the boundary size is 6. The local flag count at one face is:

```text
6 boundary edges * 2 sides = 12.
```

Therefore:

```text
Szilassi flags = 7 face axes * 12 local face flags = 84.
```

## Abstract bridge

At this level, all three 84s share the same structure:

```text
Fano atlas:
    7 chart axes * 12 directed K4-edge states

Csaszar:
    7 vertex axes * 12 local vertex flags

Szilassi:
    7 face axes * 12 local face flags
```

The duality is exactly what we expected:

```text
Csaszar uses vertex axes.
Szilassi uses face axes.
Fano supplies chart axes.
```

The local 12 is the same abstract codec:

```text
6 local edges * 2 orientations/sides.
```

## What is proved and what is not

Proved:

```text
Fano 84 and toroidal 84 share the exact decomposition seven axes times a local directed-K4 12-codec.
```

Not yet proved:

```text
A canonical Csaszar/Szilassi flag labeling by Fano chart states.
```

To prove the canonical labeling, we still need to choose a bijection from the seven Fano chart axes to the seven toroidal vertex/face axes and compare adjacency/chirality relations.

## Compressed theorem

```text
Each Fano affine chart has 12 states: four affine anchors times three infinity directions, equivalently the 12 directed edges of the tetrahedral K4. Across the seven Fano chart axes this gives 84 states. Csaszar decomposes as seven vertex axes times twelve local vertex flags, while Szilassi decomposes as seven face axes times twelve local face flags. Thus Fano 84, Csaszar 84, and Szilassi 84 share the same abstract seven-axis directed-K4 local codec, with Csaszar using vertex axes and Szilassi using dual face axes.
```

## Honest boundary

This proves the abstract 84-codec bridge. The next hard step is to build an explicit seven-axis labeling, likely using the Fano plane itself: Csaszar vertices as Fano points, Szilassi faces as Fano lines, and flags as incident chart-edge states.
