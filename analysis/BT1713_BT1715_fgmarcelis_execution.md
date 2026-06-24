# BT1713-BT1715 fgmarcelis execution packet

I extracted and read the full 270-page fgmarcelis PDF locally. The useful lesson is that this document repeatedly connects our objects by projections, quotients, and coordinate changes rather than by naive equality.

Important motifs used here:

- Fano plane as a cube projection, with point-line duality visible from cube planes.
- Reye configuration, double-six, cubic surface, 24-cell, and 600-cell as one geometric chain.
- Klein quartic, harmonic cubes, Heawood graph, co-Heawood graph, Coxeter graph, Gewirtz graph.
- Steiner and MOG material, including the leftover 9-point AG(2,3) grid after deleting two hyperovals and its PG(2,3) closure.
- Penrose/Witting 40-state endpoint.

## BT1713

Added:

```text
analysis/bt1713_ring_hesse_functor.py
data/bt1713_ring_hesse_functor.json
```

Result:

```text
nonzero singular matrices of M2(F2) = P1(F2) x P1(F2) = 3 x 3 square.
```

The six row/column square contexts map to six affine Hesse lines in AG(2,3). The remaining two affine directions are qutrit-only closure directions. Fano times Hesse gives:

```text
7 * 9 = 63
```

split-Cayley readout addresses.

Boundary: exact for the two-qubit ring-square seed; the full split-Cayley line-incidence functor remains open.

## BT1714

Added:

```text
analysis/bt1714_toroidal_heawood_embedding.py
data/bt1714_toroidal_heawood_embedding.json
```

Result:

```text
5 Csaszar + 2 Szilassi = 7 realization labels.
```

These seven labels embed as the point side of the Fano/Heawood scheduler. Each realization has:

```text
3 Heawood execution slots,
4 co-Heawood buffer slots.
```

Globally:

```text
K7,7 = Heawood + co-Heawood
49   = 21       + 28.
```

Boundary: this is a scheduler embedding, not yet a coordinate parser for each 3D toroidal realization.

## BT1715

Added:

```text
analysis/bt1715_48_bus_axis_quotient.py
data/bt1715_48_bus_axis_quotient.json
```

Result: a 4 x 4 Klein-Latin bus realizes:

```text
(12_4,16_3) with 48 incidences.
```

Splitting every 4-valent axis into two 2-valent observations gives:

```text
(24_2,16_3) with 48 incidences.
```

Pairing observations over each axis quotients the 24-observation cover back to 12 axes. The same 16 cells with three phase labels give:

```text
16 * 3 = 48
```

Holonet ticks.

This is the objectwise 48-bus bridge: q2025-style cover, tomotope/Reye axis bus, and Holonet body ticks are connected by an explicit axis quotient over a shared 16-cell carrier.

## New architecture

```text
cube/Fano projection
-> Hesse leftover grid
-> Heawood/co-Heawood scheduler
-> Reye/tomotope 48-bus quotient
-> Witting/Penrose 40-state endpoint
```

The next proof target is to extract the q2025 red/blue domain labels and test whether they choose the same Klein-Latin chart as BT1715.
