# Fano Polarity Toroidal Flag Labeling

Date: 2026-05-31

This makes the abstract Fano-to-toroidal 84 bridge explicit.

Previous theorem:

```text
Fano 84 = seven chart axes * twelve directed-K4 local states.
```

This theorem gives a canonical Fano incidence labeling of the 84 abstract flags using polarity.

## Fano polarity

Represent the Fano plane as the nonzero vectors of `F2^3`.

Lines are triples

```text
{a,b,a+b}.
```

Use the polarity

```text
point n <-> line n^perp = {x != 0 : n·x = 0}.
```

The verifier checks that this is a bijection between the seven Fano points and the seven Fano lines.

## Fano chart state

A Fano chart state is:

```text
L = chosen line at infinity
p = affine anchor in PG(2,2) \ L
d = direction in L
q = p + d
M = line(p,q) = {p,q,d}
```

Since `M != L`, each state is equivalently:

```text
(L, M, orientation of the two affine points M\L).
```

There are:

```text
7 choices of L
6 choices of M != L
2 orientations of M\L
```

so:

```text
7 * 6 * 2 = 84.
```

The verifier checks this equivalence exactly.

## Szilassi labeling

Szilassi has seven face axes and complete face adjacency.

Use the Fano lines directly as face axes:

```text
face axis = L
adjacent face = M
side/orientation = ordered affine pair p -> q on M\L
```

The verifier checks:

```text
7 face axes
12 flags per face axis
6 adjacent face axes per face
2 orientations/sides per adjacent face
84 total flags
```

So the Fano line-pair state labels the abstract Szilassi face-flag codec.

## Csaszar labeling

Csaszar has seven vertex axes and complete vertex adjacency `K7`.

Use Fano polarity:

```text
vertex axis = polar(L)
adjacent vertex = polar(M)
side/orientation = ordered affine pair p -> q on M\L
```

The verifier checks:

```text
7 vertex axes
12 flags per vertex axis
6 adjacent vertex axes per vertex
2 orientations/sides per adjacent vertex
84 total flags
```

So the same Fano chart states label the abstract Csaszar vertex-flag codec after polarity.

## Duality

This realizes the Csaszar/Szilassi duality cleanly:

```text
Szilassi:
    Fano lines as face axes

Csaszar:
    polar Fano points as vertex axes
```

The dual swap is exactly Fano polarity.

## What is proved

This proves:

```text
Fano chart state = ordered distinct Fano line pair + orientation
```

and therefore:

```text
Fano 84 = Szilassi complete face-adjacency flags
```

while polarity gives:

```text
Fano 84 = Csaszar K7 vertex-adjacency flags.
```

## What is not yet proved

This is a canonical Fano incidence labeling of the abstract 84 flags.

It does not automatically identify a particular Euclidean realization of the Csaszar or Szilassi polyhedron with this labeling. For that, one must choose the seven geometric vertices/faces and compare actual embedding adjacency/chirality data.

## Compressed theorem

```text
A Fano chart state (L,p,d) is equivalently an ordered pair of distinct Fano lines (L,M) together with an orientation of M\L. This gives 7*6*2=84 states. Taking Fano lines as Szilassi face axes labels the 84 complete face-adjacency flags. Applying Fano polarity maps lines to points, giving Csaszar vertex axes and labeling the 84 K7 vertex-adjacency flags. Thus the Csaszar/Szilassi 84 duality is realized by Fano polarity at the abstract incidence-codec level.
```

## Honest boundary

This proves the explicit abstract flag labeling. The next hard step is to compare the two orientations: the Fano orientation p->q on M\L versus the chiral orientation of tetrahedral/toroidal flags, and determine whether the polarity preserves or reverses chirality.
