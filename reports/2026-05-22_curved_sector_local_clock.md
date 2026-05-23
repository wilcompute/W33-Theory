# 2026-05-22 - Curved Sector Local Z3 Clock

## Breakthrough

The curved sector also has a clean organization.

The flat curvature triples produced the 45-object tetrad-pair graph.  The complementary question was how the nonzero-curvature triples organize locally around each center point.

## Local centered triads

Fix a W33 point x.

The 12 neighbours of x are arranged into four lines through x.  Each line contributes three neighbours besides x.

A noncollinear triple centered at x is obtained by:

1. choosing three of the four pencil lines through x;
2. choosing one of the three neighbours on each chosen line.

So the number of centered triads at x is

```text
4 * 3^3 = 108.
```

## Z3 clock split

The script verifies that for every center x, these 108 triads split uniformly by curvature:

```text
F = 0: 36
F = 1: 36
F = 2: 36
```

Equivalently:

```text
108 = 36 + 36 + 36.
```

For each omitted pencil line, the 27 triads split as:

```text
F = 0: 9
F = 1: 9
F = 2: 9.
```

So locally:

```text
27 = 9 + 9 + 9.
```

## Global consistency

Across all 40 centers:

```text
40 * 108 = 4320 centered-triad incidences.
```

This matches the global curvature-center incidence count:

```text
flat 4-centered triples:       360 triples * 4 centers = 1440 incidences
curved +1 one-centered triples: 1440 triples * 1 center = 1440 incidences
curved +2 one-centered triples: 1440 triples * 1 center = 1440 incidences
```

So the global incidence split is:

```text
(4,F=0): 1440
(1,F=1): 1440
(1,F=2): 1440
```

## Meaning

At each point, the 12-neighbour pencil becomes a local Z3 curvature clock:

```text
center point
-> four 3-branch pencil choices
-> 108 centered triads
-> three equal curvature sectors
```

This is the local curved-sector counterpart to the global flat-sector 45-object geometry.

## New code

- `analysis/w33_curved_sector_local_clock.py`

When run, it writes:

- `data/w33_curved_sector_local_clock.json`
