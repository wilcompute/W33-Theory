# 2026-05-22 - Point-First Triad Reconstruction

## Core result

The point is the primitive object.

Under the local-axis to root-line map, each W33 point becomes a 3-root-line triad.  The triad has a clean A2-type signature:

```text
three mutually nonorthogonal root lines
absolute dot products all equal 1
two sign orientations sum to zero
```

## Reconstruction theorem

Start from the 40 point-triads only.

For two point-triads, count the number of orthogonal root-line pairs between them.  There are nine possible pairings.

The rule is exact:

```text
9 orthogonal pairs -> adjacent W33 points
3 orthogonal pairs -> nonadjacent W33 points
```

The script verifies:

```text
240 true W33 adjacent pairs have count 9
540 true W33 nonadjacent pairs have count 3
```

Therefore the W33 graph is recovered from the point-triads alone.

## Everything else follows

Once adjacency is recovered:

1. W33 lines are recovered as maximal 4-cliques.
2. Ordinary quadrangles are recovered from nonadjacent pairs and common neighbours.
3. The four lines through each point are recovered.
4. The local pencil-octahedron at each point is recovered as the line graph of the four-line pencil.

The script verifies:

```text
recovered graph = SRG(40,12,2,4)
recovered lines = 40
recovered quadrangles = 1620
recovered local octahedra = 40
```

## Meaning

This flips the architecture into a point-first form.

Old flow:

```text
W33 -> local octahedra -> 120 axes -> root lines -> triads and twelve-sets
```

New flow:

```text
point-triads -> W33 adjacency -> lines -> quadrangles -> local octahedra -> logical surface
```

So the point is not merely a vertex label.  It is the seed object from which the rest of the finite geometry unfolds.

## New code

- `analysis/w33_point_first_photon_triad_reconstruction.py`

When run, it writes:

- `data/w33_point_first_photon_triad_reconstruction.json`
