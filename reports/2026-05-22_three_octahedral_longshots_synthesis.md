# 2026-05-22 - Three Octahedral Long Shots and the W33 Logical Surface

## Starting point from repo commits

Recent octahedron commits established three exact arithmetic layers:

1. The octahedron has W33-native Laplacian spectrum

```text
Spec(L_O) = (0,4,4,4,6,6)
tau(O) = 384
```

2. One octahedron per W33 point gives the chain-lift counts

```text
40*(6,12,8) = (240,480,320)
```

3. The local codec split uses the octahedron pattern

```text
8 faces + 3 axes + 1 identity = 12
```

The new work tested three long shots to connect those octahedral facts to the minimal logical flag/quadrangle surface.

---

## Long shot 1: quadrangle-corner hypergraph spectrum

### Question

If quadrangles glue the local pencil-octahedra through corner states, does the corner incidence matrix have meaningful spectrum?

### Result

Yes.

Rows are the 240 local octahedron corner states.
Columns are the 1620 ordinary quadrangles.

The incidence matrix `B` satisfies:

```text
shape(B) = 240 x 1620
rank(B) = 240
row degree = 27
column weight = 4
total incidence = 240*27 = 1620*4 = 6480
```

The corner Gram spectrum is

```text
Spec(BB^T) = 108^1 + 60^24 + 36^15 + 30^60 + 20^81 + 18^44 + 12^15.
```

### Why it matters

The multiplicities include:

```text
1,24,15     = W33 adjacency multiplicities
81          = Levi cycle rank / protected phase dimension
```

So the corner hypergraph appears to be a transfer layer from local octahedral codec states to W33 modules and Levi homology.

---

## Long shot 2: local octahedron faces are signed Xmin

### Question

Do the 40 local octahedra explain the 320 signed `X_min` vectors?

### Result

Yes.

Each local octahedron has eight faces, and these faces split into four antipodal pairs.

Globally:

```text
40*8 = 320 = signed X_min vectors
40*4 = 160 = projective X_min rays
```

Thus:

```text
signed X_min vectors  = oriented local octahedron faces
projective X_min rays = antipodal face-pairs
```

The local edge-face codec matrix for one octahedron has shape

```text
12 x 8
```

with:

```text
rank = 7
nullity = 1
```

Across 40 local octahedra:

```text
480 x 320
rank = 280
nullity = 40
```

### Why it matters

This connects the recent octahedral SM-codec layer directly to the minimal logical surface:

```text
local octahedron faces = X_min phase states
local octahedron edges = 480 carrier / codec slots
```

---

## Long shot 3: local octahedron axes form a canonical 120-set

### Question

Does the repeated 120 in the repo have an intrinsic W33 source from local octahedra?

### Result

Yes.

Each local octahedron has three axes. Across 40 W33 points:

```text
40*3 = 120
```

This gives a canonical W33 120-set: local pencil-octahedron axes.

Each axis sees exactly 54 quadrangle corners, so:

```text
120*54 = 1620*4 = 6480.
```

### Honesty boundary

This does not prove an explicit bijection to an external 120-set. It proves the W33 side: there is a canonical internal 120-set that can now be tested against E8 root-pair and 600-cell structures.

---

## Integrated dictionary after these tests

| W33/local object | octahedral meaning | logical/chain meaning |
|---|---|---|
| 40 W33 points | 40 local pencil-octahedra | local closure-clock patches |
| 240 local octahedron vertices | corner/angle states | quadrangle-corner transfer rows |
| 480 local octahedron edges | codec slots | directed carrier / C1 prime |
| 320 local octahedron faces | oriented sign faces | signed X_min vectors |
| 160 face-pairs | antipodal local faces | projective X_min rays |
| 1620 quadrangles | four-corner gluing loops | Levi octagon cycle generators |
| 120 local axes | 3 axes per point | candidate root-pair interface |
| 81 Levi cycles | cycle space | protected phase/homology sector |

---

## New files

Code:

- `analysis/w33_octahedron_corner_hypergraph_spectrum.py`
- `analysis/w33_octahedron_faces_are_signed_xmin.py`
- `analysis/w33_octahedron_axes_120_e8_longshot.py`

Data:

- `data/w33_octahedron_corner_hypergraph_spectrum.json`
- `data/w33_octahedron_faces_are_signed_xmin.json`
- `data/w33_octahedron_axes_120_e8_longshot.json`

Reports:

- `reports/2026-05-22_octahedron_corner_hypergraph_spectrum.md`
- `reports/2026-05-22_octahedron_faces_are_signed_xmin.md`
- `reports/2026-05-22_octahedron_axes_120_set.md`

---

## Next best target

The most promising next test is to compare the canonical W33 120-axis set against existing repo work on E8 root pairs / 600-cell vertices. The target question is:

```text
Can the 120 local octahedron axes carry the same orbit or incidence structure as the 120 E8 root pairs?
```

If yes, the local gauge-codec axes would become the missing intrinsic W33 side of the E8 root-pair correspondence.
