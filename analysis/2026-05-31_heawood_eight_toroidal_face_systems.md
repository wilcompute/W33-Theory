# Heawood Eight Toroidal Face Systems

Date: 2026-05-31

This interprets the index

```text
336 / 42 = 8
```

from the previous Szilassi/Heawood symmetry-factor theorem.

Previous theorem:

```text
Aut(Heawood skeleton) = 336
Aut(Szilassi toroidal map) = 42
```

so the toroidal map group has index 8 inside the full Heawood graph automorphism group.

This theorem identifies what those eight cosets actually are.

## Main object

A Szilassi toroidal map structure on the Heawood graph is a choice of seven hexagonal face cycles such that every graph edge lies in exactly two hexagons.

The concrete dual of the Csaszar rotation system supplies one such seven-hexagon system.

Now act on that system by the full Heawood automorphism group.

## Verified result

The verifier constructs:

```text
Aut(Heawood) = 336
```

split as:

```text
168 Fano collineations
168 Fano dualities / polarities
```

Then it applies every automorphism to the chosen seven-hexagon toroidal face system.

The orbit has exactly:

```text
8 distinct seven-hexagon systems.
```

These split as:

```text
4 systems from collineations
4 systems from dualities / polarities
```

So:

```text
8 = 4 + 4.
```

Each of the eight systems satisfies:

```text
7 hexagons
all cycles length 6
every Heawood edge appears in exactly two hexagons
stabilizer size 42
```

Thus every system is a valid toroidal Szilassi-style face system on the same Heawood skeleton.

## Meaning of the factor 8

The factor

```text
8 = 336 / 42
```

is the number of toroidal face systems carried by the Heawood graph in the orbit of the concrete Szilassi system.

So the hierarchy is:

```text
choose one of 8 toroidal seven-hexagon systems:
    symmetry drops to 42

forget which system was chosen:
    symmetry rises to 336
```

This is much sharper than saying "extra symmetry." The eight cosets are eight concrete toroidal face structures.

## Four plus four split

The eight systems split into two classes:

```text
4 collineation images
4 duality/polarity images
```

This suggests the index 8 has a natural form:

```text
8 = 2 * 4
```

where:

```text
2 = point-line side / polarity side
4 = affine-chart normalization side
```

This is exactly the kind of structure we expected from the Fano affine-chart story.

## Relation to previous codecs

Earlier:

```text
Fano plane = seven AG(2,2) charts.
```

Now:

```text
Heawood skeleton = eight possible toroidal seven-hexagon systems.
```

So the toroidal map is additional structure placed on the Fano/Heawood incidence skeleton.

The factor 8 measures the possible choices of that additional toroidal face-system structure.

## Compressed theorem

```text
The concrete Szilassi dual supplies a seven-hexagon face system on the Heawood graph. Acting on this system by the full 336-element Heawood automorphism group gives exactly eight distinct seven-hexagon systems. Each system covers every Heawood edge twice, has seven valid 6-cycles, and has stabilizer order 42. The eight systems split into four collineation images and four duality/polarity images. Therefore 336/42=8 is literally the number of toroidal Szilassi face systems in this Heawood orbit.
```

## Honest boundary

This proves the concrete meaning of the index 8. The next hard step is to classify the four collineation-side systems: determine whether they correspond to the four affine points of an `AG(2,2)` chart, four choices of line-at-infinity normalization, or another invariant of the Fano plane.
