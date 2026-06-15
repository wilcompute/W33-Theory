# BT1078 — Bridge matrix skeleton

BT1078 builds an explicit sparse skeleton for the BT1074 bridge map.

## Dimensions

```text
F : C^162 -> C^240
```

with the split

```text
slot side  = 96 + 66
chain side = 96 + 144.
```

## Ordered basis convention

Use slot ordering:

```text
first 96 basis vectors  = slot physical block
last 66 basis vectors   = slot complement block
```

Use chain ordering:

```text
first 96 basis vectors  = E0 + E16
next 144 basis vectors  = E4 + E10
```

## Sparse skeleton

The bridge skeleton is the partial identity injection:

```text
F[i,i] = 1              for i=0..95
F[96+j,96+j] = 1       for j=0..65
```

All other entries are zero.

## Rank and intertwining checks

```text
shape(F) = 240 x 162
rank(F)  = 162
F^T F    = I_162
```

The first 96 slot directions map onto the 96 chain physical block. The 66 complement directions map into the first 66 dimensions of the 144-dimensional chain complement. Therefore 78 chain complement dimensions remain unused.

## Boundary

This is the canonical sparse bridge skeleton after choosing ordered block bases. It is not yet the W33-incidence bridge; the future incidence bridge must replace this ordered partial identity with a natural map from slot labels to chain coordinates.
