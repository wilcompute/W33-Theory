# BT855 — The Dark Sector Is K₅-Complete: Dodecahedra as Double Covers

**Status: PROVEN (machine-verified, `analysis/bt855_dark_sector_k5_complete.py`, data `data/bt855_dark_sector_k5_complete.json`)**

The dodecahedra were the last residents of the dark sector outside the K₅
calculus (BT854). They fold in via the classical antipodal-cover fact — and
the whole zoo turns out to be graded by K₅ edge-relations.

## T1 — The K₅-relation census (constant on every orbit)

Each dark line carries a distinguished K₅ edge (its shadow class). For every
A₅-orbit of dark pairs, the relation between the two lines' edges is
*constant*:

| orbit | size | K₅ relation of the pair's edges |
| --- | --- | --- |
| matching | 10 | **same** (the 2-element shadow fibers) |
| chiral tetrad partitions | 30 + 30 | **adjacent** |
| chiral dodecahedra | 30 + 30 | **disjoint** |
| meeting frame | 60 | **adjacent** |

## T2 — The dodecahedra are antipodal double covers of the dark-chart Petersen

For both chiral dodecahedra:

- **antipodes = matching partners**: the unique distance-5 vertex from any
  dark line is exactly its shadow partner;
- **quotient by the matching = the Petersen graph** on the 10 dark charts,
  with adjacency = **disjointness of K₅ edges** — i.e. the Kneser graph
  K(5,2) in edge labels (15 quotient edges, all disjoint pairs).

So each dark dodecahedron is the **antipodal double cover of the Kneser
graph of the dark charts**, deck transformation = the shadow matching. The
schedule's hemi-dodecahedron (BT836: Petersen on the 10 contexts) and the
dark sector's full dodecahedron are now *quotient and cover of the same K₅
pattern*: {5,3}₅ = {5,3}/antipode, realized inside one compass as
schedule-versus-dark. The Petersen graph appears **three ways in one
needle**: schedule skeleton, dark-chart Kneser quotient, and (doubled) the
two chiral dodecahedra.

## T3 — The meeting frame is the doubled Johnson graph

The 60 meeting pairs project onto exactly the **30 adjacent K₅ edge-pairs,
each with multiplicity 2** — the meeting frame is a 2-fold lift of the
Johnson/triangular graph T(5) = L(K₅). Both classical graphs on C(5,2)
(Kneser = Petersen and Johnson = T(5)) appear as the dark sector's skew and
meeting relations respectively.

## The closed statement

> The pentad core's 20 dark lines form the total space of the canonical
> 2:1 cover of the K₅ edge-set (fibers = the shadow matching). Under the
> core A₅, the pair-orbits realize: the fibers (matching), the vertex stars
> twice (tetrads, chiral), the Kneser double covers twice (dodecahedra,
> chiral = the two lifts of Petersen), and the Johnson double (meeting).
> Nothing in the dark sector is outside the K₅ calculus.

## Machine reading

The dark half of a compass needle is a *complete combinatorial dual* of its
control data: chart labels (fibers), chart caches (stars), routing covers
(Kneser lifts), and congestion structure (Johnson double). Reconstruction
routes now go through any of four independent encodings, and the two
chiralities of every layer give the dark sector its own parity bit.

## Open

- The chirality correlation matrix: left/right tetrads vs left/right
  dodecahedra vs LEFT/RIGHT pentads (BT845) — one global Z₂ or independent?
- Lift to all 216 cores: do the 216 dark double covers glue into a global
  2:1 cover of the 540-chart atlas (compare the BT845 chart double cover —
  1080 = 540×2 again)?
