# 2026-05-22 - Octahedron Quadrangle Corner Codec Theorem

## Breakthrough

The local pencil-octahedra are the missing bridge between the recent octahedron commits and the minimal logical flag/quadrangle surface.

For each W33 point `p`:

```text
O_p = L(K4_pencil(p))
f(O_p) = (6,12,8)
```

The local octahedron pieces have direct global meanings:

```text
40 * V(O) = 240 = local angle/corner states
40 * E(O) = 480 = directed carrier / local codec slots
40 * F(O) = 320 = signed X_min vectors
```

Antipodal face-pairs of each local octahedron give the four projective flags through `p`:

```text
40 * 4 = 160 = projective X_min flags
40 * 8 = 320 = signed X_min vectors
```

## Quadrangle corner theorem

Every ordinary quadrangle has four corners. At each corner `p`, the two incident quadrangle edges determine two lines through `p`, hence one vertex of the local octahedron `O_p`.

The certificate verifies:

```text
240 local octahedron vertices
each lies on exactly 27 quadrangle corners
```

Therefore:

```text
240 * 27 = 1620 * 4 = 6480.
```

## Meaning

The minimal logical objects can now be read through local octahedra:

| W33 / logical object | octahedral meaning |
|---|---|
| projective X_min flags | antipodal face-pairs of local octahedra |
| signed X_min vectors | oriented faces of local octahedra |
| directed carrier 480 | local octahedron edge slots |
| W33 edge count 240 | local octahedron corner/angle states |
| Z_min quadrangles | four-corner gluing rules between local octahedra |

So quadrangles glue the local closure-clock octahedra through their octahedral corner states.

## Machine certificate

Added:

- `analysis/w33_octahedron_quadrangle_corner_codec.py`
- `data/w33_octahedron_quadrangle_corner_codec.json`

The script reconstructs W(3,3), builds the local pencil-octahedra, enumerates all ordinary quadrangles, maps each quadrangle corner to a local octahedron vertex, and checks the double count.
