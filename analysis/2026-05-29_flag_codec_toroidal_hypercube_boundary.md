# Flag Codec / Toroidal Hypercube Boundary Theorem

Date: 2026-05-29

This continues the ternary knight / Q4 / genus-lift chain using the flag-count hint.

The key correction is that the denominator 12 in the genus equations is not merely a divisor. It is the local flag codec:

```text
12 = q(q+1) = 3*4.
```

This 12-flag codec appears simultaneously in the tetrahedron, Csaszar, Szilassi, and the Q4/tomotope packet.

## Tetrahedron: the self-dual hinge

The tetrahedron has

```text
V=4, E=6, F=4.
```

A closed map has 4 flags per edge, so

```text
flags(K4) = 4E = 24.
```

Equivalently, it has 4 triangular faces and each triangle has 6 flags:

```text
4 * 6 = 24.
```

The tetrahedron is self-dual:

```text
V=F=4.
```

And its 24 flags split by orientation:

```text
24 = 12 + 12.
```

So the tetrahedron contributes two local 12-flag chiral codecs.

## Csaszar: seven vertex codecs

Csaszar has

```text
V=7, E=21, F=14,
genus=1,
triangular faces.
```

It is the maximal vertex-adjacency side: K7 embedded on the torus.

Flag count:

```text
4E = 4*21 = 84.
```

Since every vertex has degree 6, the flags incident at one vertex are

```text
2*degree = 12.
```

Therefore:

```text
84 = 7 * 12.
```

So Csaszar decomposes into seven vertex-based 12-flag codecs.

## Szilassi: seven face codecs

Szilassi is dual to Csaszar:

```text
V=14, E=21, F=7,
genus=1,
seven hexagonal faces.
```

Flag count:

```text
4E = 4*21 = 84.
```

Since each face is a hexagon, the flags on one face are

```text
2*6 = 12.
```

Therefore:

```text
84 = 7 * 12.
```

So Szilassi decomposes into seven face-based 12-flag codecs.

## The 16-codec packet

Now combine the self-dual hinge with the two toroidal duals:

```text
Tetrahedron: 2 codecs
Csaszar:     7 vertex codecs
Szilassi:    7 face codecs
```

So:

```text
2 + 7 + 7 = 16.
```

And since each codec has 12 flags:

```text
16 * 12 = 192.
```

This is exactly the tomotope flag count.

So the corrected flag packet is:

```text
24 + 84 + 84 = 192
```

but the deeper codec decomposition is:

```text
(2 + 7 + 7) * 12 = 16 * 12 = 192.
```

## Relation to Fano / 168

The two toroidal polyhedra together have

```text
84 + 84 = 168.
```

And

```text
168 = 7 * 24.
```

So the toroidal dual pair carries seven tetrahedron-flag units.

This is exactly the PSL(2,7) / Fano number that keeps appearing:

```text
168 = |PSL(2,7)|.
```

In codec terms:

```text
168 = 14 * 12 = (7+7) * 12.
```

That is: seven Csaszar vertex codecs plus seven Szilassi face codecs.

## Dual genus equations

The complete graph triangular embedding formula is

```text
g = (n-3)(n-4)/12.
```

For Csaszar, the natural variable is vertex count:

```text
g = (v-3)(v-4)/12.
```

With v=7:

```text
g = (7-3)(7-4)/12 = 1.
```

For Szilassi, the dual equation swaps vertex and face count:

```text
g = (f-3)(f-4)/12.
```

With f=7:

```text
g = (7-3)(7-4)/12 = 1.
```

The tetrahedron sits in the middle because

```text
v=f=4,
g=(4-3)(4-4)/12=0.
```

So the self-dual tetrahedron is the genus-zero hinge between the two genus-one dual maxima:

```text
max vertex adjacency <-> self-dual hinge <-> max face adjacency
Csaszar              <-> tetrahedron     <-> Szilassi
```

## Mod-12 closure residues

The triangular complete-graph genus expression is integral exactly for

```text
n = 0,3,4,7 mod 12.
```

This is the W33 packet:

```text
0, q, chi, Phi6 = 0,3,4,7.
```

The interpretation is:

```text
3 = q      = minimal triangular loop
4 = chi    = tetrahedral self-dual closure
7 = Phi6   = toroidal K7 closure
0 mod 12   = full codec-period closure
```

## Hypercube boundary link

The Q4 router has

```text
16 vertices
32 edges
24 square faces
```

The new identification is:

```text
Q4 vertices = 16 local 12-flag codecs.
```

And:

```text
Q4 square faces = 24 = tetrahedron flags.
```

From the previous ternary knight theorem:

```text
full Gray clock ternary ticks = 16*3 = 48 = 2*tetrahedron flags.
```

And the induced snake/coil subclock gives:

```text
8*3 = 24 = tetrahedron flags.
```

So the toroidal boundary needed to realize Q4 is not accidental. The Q4 boundary supplies the 16 slots into which the tetrahedron/Csaszar/Szilassi flag codecs fit.

## Final compressed theorem

```text
12 = local flag codec = q(q+1)
24 = tetrahedron flags = 2 codecs
84 = Csaszar flags = 7 vertex codecs
84 = Szilassi flags = 7 face codecs
168 = toroidal dual-pair flags = 14 codecs = |PSL(2,7)|
192 = total hinge-plus-torus flags = 16 codecs = tomotope flags
16 = Q4 vertices = codec slots
24 = Q4 square faces = tetrahedron flags
48 = Q4 full Gray clock ternary ticks = 2 tetrahedron flags
```

So the clean architecture is:

```text
Tetrahedron supplies the self-dual 2-codec hinge.
Csaszar supplies seven vertex-adjacency codecs.
Szilassi supplies seven face-adjacency codecs.
Q4 supplies the toroidal boundary layout for all 16 codecs.
The tomotope packages the resulting 192 flags.
```

## Honest boundary

This proves the finite flag-codec accounting and its compatibility with the Q4 toroidal boundary. It does not yet assign each of the 16 codecs to a unique Q4 vertex with a canonical adjacency-preserving map. That is the next valid test: build the explicit 16-codec adjacency graph and compare it to Q4 / toroidal-knight adjacency.
