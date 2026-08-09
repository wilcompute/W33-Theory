# Part MCXCIII: Reye Tomotope/24-Cell Common Spine

## Claim Boundary

MCXCIII is a finite incidence-isomorphism theorem. It does not assert continuum
dynamics. It proves that the Reye configuration is the same combinatorial spine
on both sides:

```text
tomotope edge-triangle medial layer
= 24-cell axis-hexagon incidence layer
= Reye (12_4,16_3).
```

## Source Check

The online dLib record for *The Tomotope* exposes the paper metadata and TXT/PDF
entries. The local PDF text extraction confirms Section 6: the tomotope medial
layer `I_{1,2}` is the Levi graph of Reye's configuration, with automorphism
group order `576`.

Independent 24-cell references give the other side: the 12 antipodal axes and
16 hexagonal central planes of the 24-cell form the same Reye configuration.

## 24-Cell Construction

The verifier builds the 24-cell directly from the D4 roots:

```text
vertices = permutations of (+/-1,+/-1,0,0) = 24.
```

Opposite vertices pair into axes:

```text
24 / 2 = 12 axes.
```

A hexagonal central plane is detected as a two-dimensional rational span
containing exactly six D4 roots. The verifier finds:

```text
16 hexagon planes.
```

The axis-plane incidence is:

```text
12 axes * 4 = 16 hexagons * 3 = 48.
```

The resulting Levi graph is isomorphic to the same cube-model Reye graph used
in MCLXXXII.

## Tomotope Match

From MCLXXXII:

```text
tomotope edges                 = 12,
tomotope triangles             = 16,
tomotope edge-triangle incidences = 48.
```

Thus the exact dictionary is:

```text
tomotope edges      <-> 24-cell axes,
tomotope triangles  <-> 24-cell hexagon planes,
tomotope medial I12 <-> 24-cell Reye incidence graph.
```

This upgrades the earlier count-shadow into an explicit common Levi graph.

## Symmetry Lock

The common Reye graph has automorphism group order:

```text
|Aut(Reye)| = 576.
```

The live tomotope automorphism packet is:

```text
|Aut(T)| = 96.
```

So:

```text
576 = 6 * 96.
```

The D4/F4/24-cell side gives:

```text
|W(F4)| = 1152,
rotational symmetry of the 24-cell = 1152 / 2 = 576.
```

Therefore:

```text
|Aut(Reye)| = 6*|Aut(T)| = |W(F4)|/2.
```

The factor `6=q!` is the triality/six-channel lift between the tomotope
automorphism packet and the full 24-cell rotational Reye symmetry.

## Horizon Anchor

MCXCII uses the same 12 Reye points and 16 Reye lines as the seed inside the
K12 orientable horizon completion. So the chain is now:

```text
Q4 antipodal quotient
-> Reye
-> tomotope medial layer
-> 24-cell axis/hexagon layer
-> K12 genus-six horizon.
```

This is the exact reason the Reye configuration is the hinge between the
tomotope and the 24-cell.

## Source Alignment

- dLib record for Monson, Pellicer, Williams, *The Tomotope*:
  https://www.dlib.si/details/URN%3ANBN%3ASI%3ADOC-9CLAKPQM?language=eng
- Monson, Pellicer, Williams, *The Tomotope* PDF:
  https://bmonson.ext.unb.ca/fields/tom.pdf
- Reye configuration overview with the 24-cell axis/hexagon realization:
  https://en.wikipedia.org/wiki/Reye_configuration
- 24-cell overview with the Reye axis/hexagon realization:
  https://en.wikipedia.org/wiki/24-cell

## Artifacts

- Analysis: `analysis/w33_reye_tomotope_24cell_common_spine.py`
- Tests: `tests/test_w33_reye_tomotope_24cell_common_spine.py`
- Result: `PART_MCXCIII_REYE_TOMOTOPE_24CELL_COMMON_SPINE_results.json`
