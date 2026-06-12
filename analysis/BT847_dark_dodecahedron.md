# BT847 — The Dark Dodecahedra and the Chart K₅

**Status: PROVEN (machine-verified, `analysis/bt847_dark_dodecahedron.py`, data `data/bt847_dark_dodecahedron.json`)**

BT846's two opens are closed, and the Grünbaum–Coxeter arc ends on its most
poetic note: the genuine dodecahedron — not just its hemi-quotient — lives on
every pentad core's dark sector, twice, chirally.

## T1 — The dark dodecahedra

The 190 pairs of the core's 20 dark lines split under A₅ as

```text
190 = 10 + 30 + 30 + 30 + 30 + 60
```

Exactly **two of the four 30-orbits are dodecahedron skeletons** (3-regular,
girth 5, diameter 5, connected — the profile that distinguishes the
dodecahedron from the Desargues graph). The other two 30-orbits are
3-regular girth-3 disconnected graphs (component structure not yet
identified). So each pentad core carries a **chiral pair of dodecahedra** on
its dark sector — echoing the chiral pentad pair on its lit sector.

The 57-cell's cell is the *hemi*-dodecahedron (BT836: the Petersen 15-orbit
on the schedule). The full unquotiented dodecahedron appears one level
deeper, on the dark lines, in two chiralities. The icosahedral compass
carries the entire {5,3} family: Petersen (= hemi-dodeca) on its schedule,
two dodecahedra in its dark sector, all under one A₅.

## T2 — The schedule is a K₅ on its charts

The map (schedule line → the 2 charts it serves) hits **all 10 = C(5,2)
chart pairs exactly once**: the 10 timetable lines are in canonical bijection
with the edges of K₅ on the 5 matching charts. With BT846's reconstruction
theorem the local geometry is now fully rigid:

```text
5 charts (deleted matching)  =  K5 vertices
10 schedule lines            =  K5 edges (each line = its chart pair)
transversal bundles          =  the edge-vertex incidence (4 per chart, 2 per line)
```

## The closed arc (BT836 → BT847)

Every measurement schedule of the photonic machine carries: the
hemi-icosahedron (K₆ on its hidden 6-set), 12 Petersen graphs = 4·K₁₀ (its
icosahedral compasses), 6 left + 6 right maximal-partial-spread pentads, a
chart K₅ per pentad core whose transversals regenerate the schedule, and a
chiral pair of dodecahedra per core in the dark sector. The 11-cell and
57-cell do not embed; their entire local geometry does — glued by Sp(4,3)
instead of PSL(2,11)/PSL(2,19).

## Open

- Identify the two girth-3 30-orbits (five K₄s each?) and the 10- and
  60-orbits of the dark pairs.
- Are the two dark dodecahedra swapped by the same chirality that swaps
  LEFT/RIGHT pentads (compute the correlation across all 216 cores)?
- Lift the chart K₅ to the Clifford layer: 5 charts = 5 commuting(?) routing
  contexts — the F₅ register conjecture, now with exact incidence to test.
