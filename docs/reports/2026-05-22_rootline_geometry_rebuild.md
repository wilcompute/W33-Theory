# 2026-05-22 - Root-Line Triads and 12-Sets Rebuild W33 Geometry

## Breakthrough

The explicit 120-axis to 120-root-line map now reconstructs the full W33 incidence geometry inside the root-line layer.

## Construction

Using the explicit graph isomorphism:

- each W33 point becomes a 3-root-line triad;
- each W33 line becomes a 12-root-line set, built from the four point-triads on that line.

## Result

The script verifies:

```text
40 triads
40 twelve-sets
160 triad/twelve-set incidences
```

Each triad lies in 4 twelve-sets.
Each twelve-set contains 4 triads.

The twelve-set intersection rule is:

```text
intersection size 3: 240 pairs
intersection size 0: 540 pairs
```

Joining two twelve-sets when their intersection has size 3 gives

```text
SRG(40,12,2,4)
```

with the same spectrum as W33.

## Meaning

This is stronger than the previous result. We no longer merely map 120 W33 local axes to 120 root lines. The mapped triads and twelve-sets rebuild the point-line incidence geometry:

| W33 object | root-line reconstruction |
|---|---|
| point | 3-line triad |
| line | 12-line set containing 4 triads |
| point-line incidence | triad contained in twelve-set |
| line intersection | twelve-sets intersect in 3 root lines |
| nonintersection | twelve-sets are disjoint |

So W33 is reconstructible from the internal organization of the 120 root lines induced by the local-octahedral axis map.

## New code

- `analysis/w33_rootline_geometry_rebuild.py`

When run, the script writes:

- `data/w33_rootline_geometry_rebuild.json`
