# Part MDCLXXXII: Clifford Antipodal / W33 Spread Incidence Bridge

## Claim Boundary

MDCLXXXII is an incidence-conservation theorem.  It identifies the exact
transport load between the raw Clifford `L/R` selector and the W33 spread
selector.

It does not construct the missing symplectic selector.

## Input

MDCLXXXI proved that the `36` raw Clifford `L/R` cross-pairs and the `36` W33
spreads are count-equal but not scheme-equal.

The UQCA/TQC bridge says the missing selector should live at the edge/vertex
scale interface:

```text
UQCA edge layer / TQC vertex layer = 240 / 40 = 6 = q!
```

## Clifford Antipodal Design

Each Clifford `L/R` cross-pair is two shared great decagons in the `600`-cell.
Those two decagons contain `20` vertices, or `10` antipodal pairs.

So the raw Clifford selector is a block design:

```text
points = 60 antipodal 600-cell addresses
blocks = 36 L/R cross-pairs
block size = 10
replication = 6
incidences = 60 x 6 = 36 x 10 = 360
```

Its profiles are:

```text
block intersections: 0:180, 2:450
point-pair cooccurrence: 0:600, 1:720, 2:450
```

## W33 Line-Spread Design

The W33 selector is also a `36`-block, size-`10` design, but on W33 lines:

```text
points = 40 W33 lines
blocks = 36 spreads
block size = 10
replication = 9
incidences = 40 x 9 = 36 x 10 = 360
```

Its profiles are:

```text
spread intersections: 1:360, 4:270
line-pair cooccurrence: 0:240, 3:540
```

## Bridge Identity

The exact selector-level transport equation is:

```text
36 x 10 = 60 x 6 = 40 x 9 = 360
```

Equivalently:

```text
60 / 40 = 9 / 6 = 3 / 2
```

The raw Clifford side has more points with lower replication.  The W33 spread
side has fewer points with higher replication.  Total incidence is conserved.

## Reading

This is the selector form of the UQCA/TQC scale bridge.

The Clifford side gives the antipodal `600`-cell address system:

```text
60 addresses, each used 6 times
```

The W33 side gives the symplectic line system:

```text
40 lines, each used 9 times
```

The missing selector must therefore transport:

```text
60 antipodal addresses at replication 6
      -> 40 W33 lines at replication 9
```

That is the precise finite target for the next breakthrough.

## Artifacts

- Analysis: `analysis/w33_clifford_antipodal_spread_incidence_bridge.py`
- Tests: `tests/test_w33_clifford_antipodal_spread_incidence_bridge.py`
- Result: `PART_MDCLXXXII_CLIFFORD_ANTIPODAL_SPREAD_INCIDENCE_BRIDGE_results.json`
