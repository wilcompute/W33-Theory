# BT780 — The Rank-32 Cube-Web Suborbit Atlas

BT779 proved that the 540-node cube-web permutation character has orbital
rank 32.  BT780 opens that rank up geometrically.  Fix one cube chart, compute
its 48-element stabilizer inside PSp(4,3), and split all 540 cube charts into
stabilizer suborbits.  These 32 suborbits are the actual rank-32 relations.

## Exact output

```text
group order: 25920
base stabilizer order: 48
suborbits: 32
orbit size profile: {1: 1, 3: 1, 4: 2, 6: 2, 8: 3, 12: 11, 24: 9, 48: 3}
web distance shells: {0: 1, 1: 6, 2: 30, 3: 99, 4: 228, 5: 176}
web adjacency is orbit 1 of size 6
```

So the cube web has diameter 5 with shell sequence

```text
1, 6, 30, 99, 228, 176
```

and the immediate web-neighbor relation is not fuzzy: it is exactly suborbit
`R01`, of size 6.

## The first routing states

```text
R00: size  1, distance 0, relation {equal:2}, overlap 8
R01: size  6, distance 1, relation {transversal2:2}, overlap 4
R02: size  6, distance 2, relation {zero_side:2}, overlap 0
R03: size 24, distance 2, relation {equal:1, zero_side:1}, overlap 4
R04: size  3, distance 3, relation {zero_side:2}, overlap 0
R05: size 24, distance 3, relation {one_side:1, transversal2:1}, overlap 3
R06: size 24, distance 3, relation {one_side:1, transversal2:1}, overlap 3
R07: size 24, distance 3, relation {transversal2:1, zero_side:1}, overlap 2
R08: size 24, distance 3, relation {one_side:2}, overlap 2
```

The complete JSON stores all 32 orbit rows and the full 32 x 32 web quotient
matrix.

## What changed conceptually

BT777 gave the cube-web graph.  BT778 found the double-count theorem and the
Ramanujan sentinel.  BT779 decomposed the web module.  BT780 adds the missing
control surface: every chart-to-chart relation now has a finite state label.

This is the formal routing theorem in embryonic form:

```text
local cube routing = inside a Q3 chart
apartment-hop routing = move between rank-32 chart states
maximum chart distance = 5
```

The graph-theory phrase is that the web is distance-diameter 5 but orbital-rank
32.  The physics/computation phrase is sharper: the hypercube layer is a
32-symbol transport alphabet, not merely a 6-regular graph.

## New conjectural bridge

The suborbit size profile

```text
1, 3, 4, 4, 6, 6, 8, 8, 8, 12^11, 24^9, 48^3
```

looks like the local cube symmetry group of order 48 being seen through three
successive quotients: fixed chart, half-chart symmetries, and full stabilizer
packets.  This is exactly the layer where the cyclic/dihedral split from BT778
should be located: the D6 antipode slot is likely not a separate object but one
of the rank-32 stabilizer states induced by forgetting the Z12 rectangle clock.

## Validation

Run:

```bash
python3 analysis/bt780_rank32_suborbit_atlas.py
```
