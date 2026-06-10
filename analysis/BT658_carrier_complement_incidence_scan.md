# BT658 — Carrier / Complement Incidence Scan

This executes the second BT656 next step: construct the incidence relation between the six regular 24-flag S4 carriers and the 16 complement flags.

BT657 corrected the boundary shape:

```text
16 complement flags = 4K4 = four complete W33 line fibers.
```

So the incidence scan is not a Q4 adjacency scan.  It is a scan of how the six 24-dimensional sign carriers attach to the four tetrahedral line-fiber cells.

## Raw adjacency incidence

Using Levi flag adjacency, each complement flag has:

```text
3 neighbors inside its own K4 component
3 neighbors outside the 16-complement layer
```

The outside adjacency is concentrated in only two of the six 24-orbits.

Across all 16 complement flags, adjacency to the six 24-orbits is:

```text
O0: 0
O1: 0
O2: 24
O3: 0
O4: 24
O5: 0
```

Equivalently, each of the four K4 complement cells has adjacency vector

```text
0,0,6,0,6,0.
```

So the raw adjacency relation sees a two-carrier active pair, not K4,4 and not all six one-factorization frames.

## Distance incidence to the six carriers

Aggregate distance profiles from the 16 complement flags to the six 24-orbits split into three paired carrier types:

```text
Far pair:
  d3: 96, d4: 288

Middle pair:
  d2: 48, d3: 192, d4: 144

Active pair:
  d1: 24, d2: 96, d3: 120, d4: 144
```

Each type occurs twice.

Thus the six regular carriers organize around the 16 complement boundary as

```text
6 = 2 far + 2 middle + 2 active.
```

## Interpretation

The complement layer is a four-cell tetrahedral router.  It does not couple evenly to all six regular carriers by raw flag adjacency.  Instead, adjacency selects one active carrier pair, while distance shells recover the full three-pair structure.

This points to a corrected next bridge:

```text
six S4 carriers -> three paired metric channels -> four K4 line-fiber cells.
```

The possible G2 signal is now the three-pair split rather than a literal K4,4 graph in the raw Levi flag adjacency.

## Boundary

No K4,4 or Q4 relation appears from raw Levi flag adjacency.  To recover the earlier Q4/K4,4 codec chain, one must define a secondary boundary relation, likely using antipodal/tomotope labels rather than the Levi flag graph edges.
