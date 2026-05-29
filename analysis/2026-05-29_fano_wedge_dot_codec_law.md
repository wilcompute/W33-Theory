# Fano Wedge-Dot Codec Law

Date: 2026-05-29

This executes the hard test left by the alternating-projector/Hodge theorem:

```text
Attach the seven Csaszar vertex codecs and seven Szilassi face codecs to Fano labels.
Then verify a concrete wedge/dot law on Fano line triples.
```

The result passes.

## Fano labeling

Label the seven nonzero points of F2^3:

```text
p1, p2, ..., p7.
```

The Fano line law is:

```text
a + b + c = 0
```

or equivalently:

```text
c = a + b.
```

Therefore every unordered pair `{a,b}` has a unique completion point `c`.

## Csaszar side: wedge completion

Csaszar is the maximal vertex-adjacency side. It has K7 as its vertex graph:

```text
7 vertices
21 vertex pairs / edges
```

For a pair of Fano-labeled vertex codecs `{a,b}`, define:

```text
{a,b} wedge-completes to c = a+b.
```

So each Csaszar edge is completed to a Fano line:

```text
{a,b} -> {a,b,a+b}.
```

The verifier checks:

```text
21 unordered pairs
7 Fano lines
each line contains 3 pairs
each completion point completes exactly 3 pairs
```

Thus the 21 Csaszar edges split as:

```text
7 lines * 3 pairs per line.
```

## Szilassi side: dot / contraction

Szilassi is the maximal face-adjacency side. Its seven faces are naturally labeled by the same seven Fano points/axes.

For a Fano line

```text
{a,b,c}
```

contract by one point, say `c`:

```text
dot_c({a,b,c}) = {a,b}.
```

The verifier checks that this contraction reverses the Csaszar wedge completion:

```text
{a,b} wedge-completes to c
and
dot_c({a,b,c}) = {a,b}.
```

So:

```text
wedge completion and dot contraction are inverse incidence correspondences.
```

## Local 12-flag codec on a Fano line

Each Fano line has three unordered pairs. With orientation, it has six directed pair flags:

```text
3 unordered pairs * 2 orientations = 6.
```

The local line codec combines:

```text
6 Csaszar-oriented edge flags
+
6 Szilassi-oriented dual flags
=
12 flags.
```

So one Fano line carries one full 12-flag codec.

Across seven lines:

```text
7 * 12 = 84.
```

This matches one toroidal side.

With both toroidal polarities:

```text
84 Csaszar wedge flags + 84 Szilassi dot flags = 168.
```

Then adding the tetrahedral Hodge hinge:

```text
168 + 24 = 192.
```

So the tomotope flag count is recovered from the explicit Fano wedge/dot law.

## Verified identities

The verifier checks:

```text
7 Fano points
7 Fano lines
21 unordered pairs
21 point-line flags
each pair lies on a unique line
each point lies on three lines
each completion point completes three pairs
wedge-dot inverse law
12 flags per local Fano-line codec
84 flags on Csaszar side
84 flags on Szilassi side
168 combined toroidal flags
192 after adding tetrahedral hinge flags
```

## Operator dictionary refined

The previous theorem gave:

```text
Hodge star conjugates wedge to dot.
```

This theorem supplies the actual Fano-axis law:

```text
wedge:      {a,b} -> c=a+b
contraction: ({a,b,c}, c) -> {a,b}
```

Therefore:

```text
Csaszar vertex codec pairs are exterior/wedge data.
Szilassi face codec contractions are interior/dot data.
The tetrahedron Hodge star mediates the duality.
The Fano plane supplies the line-triple law that makes the duality concrete.
```

## Compressed theorem

```text
For Fano labels a,b,c in F2^3\{0}, the line condition a+b+c=0 defines the codec law.
Csaszar wedge completion maps the vertex pair {a,b} to c=a+b.
Szilassi dot contraction maps the line {a,b,c} contracted by c back to {a,b}.
These two maps are inverse incidence correspondences.
Each Fano line carries a 12-flag local wedge/dot codec.
Seven lines give 84 flags per toroidal side; the two toroidal sides give 168; adding the tetrahedral 24 gives 192.
```

## Honest boundary

This proves the finite Fano wedge/dot codec law. The next hard step is to combine this line-triple law with the Q4 antipodal cover and test whether Q4 edges lift individual wedge/dot transitions while Q4 square faces lift Fano-line commutator loops.
