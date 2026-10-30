# 2026-05-22 - Z3 Voltage Cover of the W33 Complement

## Breakthrough

The noncollinear transport graph is a connected 3-sheet cover of the W33 complement.

Base graph:

```text
W33 complement on 40 points
regular degree = 27
spectrum = 27^1 + 3^15 + (-3)^24
```

Cover graph:

```text
120 point-slots = 40 point-triads * 3 slots
noncollinear perfect-matching transport edges
regular degree = 27
spectrum = 27^1 + 3^75 + (-3)^24 + (-9)^20
```

The base spectrum embeds into the cover spectrum, and the extra fiber spectrum is

```text
3^60 + (-9)^20
```

## Parity gauge and Z3 voltage

Initially, perfect-matching transports are permutations of three slots.  A parity gauge exists on the 40 base points such that every transport becomes cyclic.

After this gauge, every directed noncollinear edge carries a voltage in

```text
Z3
```

The voltage is antisymmetric:

```text
v(q,p) = -v(p,q) mod 3
```

The voltage distribution is:

```text
0: 420
1: 330
2: 330
```

for directed transport edges.

## Curvature / holonomy

For each pairwise noncollinear triple, sum the three directed voltages around the triangle.

The result is exact:

```text
voltage sum 0 <=> 4-centered triple
voltage sum 1 or 2 <=> 1-centered triple
```

Counts:

```text
4-centered triples: 360, all voltage sum 0
1-centered triples: 2880, split as 1440 with sum 1 and 1440 with sum 2
```

## Meaning

This turns the previous Z3 holonomy observation into a genuine voltage-cover structure:

```text
point = 3-slot triad
noncollinear relation = perfect-matching transport
transport graph = connected 3-cover of W33 complement
curvature = voltage sum on noncollinear triples
flat triangles = four-centered triples
curved triangles = one-centered triples
```

This is the cleanest current finite model of a phase-transport layer over the point geometry.

## New code

- `analysis/w33_z3_voltage_cover.py`

When run, it writes:

- `data/w33_z3_voltage_cover.json`
