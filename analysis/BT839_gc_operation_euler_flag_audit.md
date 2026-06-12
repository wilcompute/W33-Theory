# BT839 - Grünbaum-Coxeter Operation Euler/Flag Audit

## Summary

BT839 treats the Desktop Grünbaum-Coxeter note as data.  It transcribes the base
tables for the 11-cell, 57-cell, tomotope partial a, and tomotope partial b,
then the four operation tables for the 11-cell, 57-cell, and tomotope:
rectified, truncated, maximal expanded, and omnitruncated.

The first invariant is simple and sharp:

```text
all base tables have Euler charge 0
all 11-cell operation tables have Euler charge -11
all 57-cell operation tables have Euler charge -57
all tomotope operation tables have Euler charge -4
```

So Wythoff operations turn neutral GC/tomotope carriers into fixed negative
charges equal to the corresponding vertex-family count.

## Full-Flag Bridges

| family | omnitruncated vertices | identity |
|---|---:|---|
| 11-cell | 660 | `PSL(2,11) = 11*A5 = k*N_eff` |
| 57-cell | 3420 | `PSL(2,19) = 57*A5 = k*g*19` |
| tomotope | 96 | half of BT814's 192 full flags |

The 57-cell has an extra W33 completion:

```text
BT837 Petersen homes = 3240
k*g sentinel sheet   = 12*15 = 180
3240 + 180           = 3420
```

So W33 already carries most of the 57-cell full-flag count as Petersen homes;
the missing part is exactly one `k*g` sentinel sheet.

## 600 / 24 / 120 Pairing

The strongest orientation currently supported by the data is:

```text
11-cell  -> 600-cell
tomotope -> 24-cell
57-cell  -> 120-cell
```

The 57-cell to 120-cell link is the cleanest: the 57-cell cells are
hemi-dodecahedra, while the 120-cell cells are dodecahedra.

The tomotope to 24-cell link is through the already verified runtime lift:
`f = 24`, and the 24-cell has 24 vertices and 96 edges, matching the tomotope
truncated/omnitruncated runtime boundary.

The 11-cell to 600-cell link is more subtle.  It is not a direct cell match,
because the 600-cell has tetrahedral cells.  The link is through the
icosahedral/hemi-icosahedral local structure and the `2I -> A5` symmetry
quotient: the 600-cell vertices form the binary icosahedral group, while the
11-cell flag count is `11*A5`.

The swapped orientation is recorded as a weaker alternate:

```text
11-cell -> 120-cell via hemi-dodecahedral vertex figure
57-cell -> 600-cell via hemi-icosahedral vertex figure
```

but it scores lower because neither is a direct cell match.

## Boundary

BT839 does not assert that the full 11-cell or 57-cell embeds into W33, nor that
the 600-cell/120-cell embeds through these abstract polytopes.  The theorem is
a table-level flag, Euler, cell-type, and symmetry alignment.

## Top 3 Next Moves

1. Search for the missing `k*g = 180` sentinel sheet completing BT837's 3240
   Petersen homes to the 57-cell's 3420 flags.
2. Build the 11-cell `660 = 11*A5` carrier explicitly from the W33 schedule
   library, rather than leaving it as a flag-count/symmetry identity.
3. Test whether the tomotope `96` half-flag boundary is literally the 24-cell
   edge graph (`96` edges) under the chart stabilizer.
