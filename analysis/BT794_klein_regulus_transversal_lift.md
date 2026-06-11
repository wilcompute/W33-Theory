# BT794 — Klein Regulus Transversal Lift

Every W33 skew-line chart has the same regulus profile.

```text
charts = 540
common isotropic transversals per chart = 4
same-ruling completion lines in PG(3,3) = 2
isotropic completion lines = 0
```

Thus each local chart is not merely a pair of skew lines with four accidental
transversals.  It is the W33-visible shadow of a hyperbolic grid/regulus:

```text
same ruling:       base line A, base line B, plus two non-isotropic completions
opposite ruling:   four isotropic common transversals
```

The cross incidence between the two rulings is uniform, and the same-ruling
lines are pairwise skew.

## Boundary

The lift is real, but W33 only sees the isotropic part.  The two completion
lines required by the full PG(3,3) grid exist outside the totally isotropic line
set.

This is the correct boundary statement:

```text
W33 chart = isotropic regulus shadow, not full isotropic Q+(3,3)
```

This feeds directly into BT795: the four common isotropic transversals are the
local four vertex carriers for the rank-4 middle layer.
