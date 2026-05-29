# Antipodal Codec Quotient / Tomotope Theorem

Date: 2026-05-29

This continues the 16-codec flag theorem by testing the actual adjacency/boundary structure.

The result is strong:

```text
Q4 is the double cover of an antipodal K4,4 axis graph.
```

The 16 Q4 vertices are the 16 local 12-flag codecs:

```text
2 tetrahedral chiral codecs
7 Csaszar vertex codecs
7 Szilassi face codecs
```

Pair Q4 vertices by antipodal complement:

```text
x -> 1-x.
```

This gives 8 duality axes:

```text
1 tetrahedral chirality axis = {T_plus, T_minus}
7 toroidal dual axes = {Csaszar_i, Szilassi_i}
```

So the 16-codec system folds to an 8-axis system.

## Antipodal quotient

The verifier constructs Q4, pairs vertices by antipodal complement, and computes the quotient graph.

It checks:

```text
Q4 vertices = 16
Q4 edges = 32
antipodal axes = 8
quotient edges = 16
each quotient edge lifts to exactly 2 Q4 edges
quotient graph = K4,4
quotient degree sequence = 4,4,4,4,4,4,4,4
```

Thus:

```text
Q4 -> K4,4
```

is a 2-fold antipodal cover.

## Hinge axis and tomotope extraction

Choose the tetrahedral chirality pair as the distinguished hinge axis:

```text
{T_plus, T_minus}.
```

In the K4,4 quotient, this hinge axis has:

```text
4 adjacent toroidal axes
3 nonadjacent toroidal axes
```

So the distance split appears again:

```text
4 + 3 = d_Z + d_X.
```

Now extract incidence counts relative to the hinge axis:

```text
quotient axes = 8
quotient edges = 16
quotient edges incident to hinge axis = 4
quotient edges not incident to hinge axis = 12
```

This is exactly the tomotope f-vector:

```text
(V,E,F,C) = (4,12,16,8).
```

So:

```text
V_tomotope = 4  = hinge-incident quotient edges
E_tomotope = 12 = hinge-nonincident quotient edges
F_tomotope = 16 = all quotient edges
C_tomotope = 8  = all quotient axes
```

And:

```text
4 + 12 + 16 + 8 = 40 = W33 vertex count.
```

This is a major consolidation: the tomotope f-vector is not just numerically nearby. It is extracted from the antipodal quotient of the Q4 codec boundary after choosing the tetrahedral hinge axis.

## Flag accounting survives

Each codec has 12 flags:

```text
one codec = 12 flags.
```

Therefore:

```text
16 codecs * 12 flags = 192 flags.
```

The tetrahedral axis has two codecs:

```text
2 * 12 = 24 flags.
```

The seven toroidal axes each have a Csaszar and Szilassi endpoint:

```text
7 * 2 * 12 = 168 flags.
```

So:

```text
24 + 168 = 192.
```

This agrees with the earlier flag theorem:

```text
24 tetrahedron flags + 84 Csaszar flags + 84 Szilassi flags = 192 tomotope flags.
```

## Relation to Fano and PSL(2,7)

The seven toroidal axes are naturally the seven Fano positions:

```text
7 axes = Phi6.
```

Each axis carries a Csaszar/Szilassi dual pair:

```text
vertex codec <-> face codec.
```

Thus:

```text
7 axes * 2 endpoints * 12 flags = 168.
```

This is the PSL(2,7) count:

```text
168 = |PSL(2,7)|.
```

So the Fano symmetry appears as the toroidal part of the folded Q4 codec boundary.

## Final geometry

The structure is now:

```text
Q4 codec graph
  = 16 local 12-flag codecs
  = double cover of antipodal K4,4 axis graph
```

with:

```text
one tetrahedral hinge axis
seven toroidal Csaszar/Szilassi axes
```

and the tomotope is obtained by reading the quotient incidence relative to the hinge axis:

```text
(4,12,16,8).
```

## Compressed theorem

```text
Q4 vertices = 16 local flag codecs.
Antipodal Q4 axes = 8 duality axes.
One axis is tetrahedral chirality; seven axes are Csaszar/Szilassi toroidal duals.
The antipodal quotient is K4,4.
Relative to the tetrahedral hinge axis, K4,4 yields the tomotope f-vector (4,12,16,8).
```

This is exactly the missing adjacency/boundary test: the 16-codec packet is not just a count. It has a canonical quotient graph whose incidence recovers the tomotope.

## Honest boundary

This proves the Q4 antipodal quotient and tomotope f-vector extraction. The remaining hard test is to attach actual Csaszar and Szilassi incidence data to the seven toroidal axes using a Fano-plane labeling, then verify whether Q4 adjacency corresponds to allowed vertex-face codec transitions.
