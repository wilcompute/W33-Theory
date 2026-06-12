# BT854 — The Dark Charts Are the K₅ Edges: The Core's Geometry Closes

**Status: PROVEN (machine-verified, `analysis/bt854_dark_chart_transversal_duality.py`, data `data/bt854_dark_chart_transversal_duality.json`)**

Closing BT853's opens. One conjecture refuted, and the refutation completes
the pentad core's local geometry into a single self-referential K₅ calculus.

## Refutation first

**Conjectured:** the 10 dark charts' transversal tetrads are the 10 K₄
components. **FALSE** — all ten transversal tetrads land **inside the
schedule** (and the K₄-tetrads' own internal pairs have mixed transversals).

## The theorem that replaced it

Each dark line meets exactly 4 schedule lines (its **schedule shadow** — the
spread partitions the points, so a 4-point line meets exactly 4 spread lines).
Verified:

- **The dark matching is shadow-pairing**: the two lines of each dark chart
  share their entire 4-line schedule shadow (that *is* why the canonical
  matching exists).
- In the K₅ labeling (schedule lines = K₅ edges on the 5 lit charts, BT847),
  the ten shadows are **exactly the ten "edge + opposite triangle"
  configurations** of K₅ — each shadow consists of one distinguished edge e
  plus the triangle on the complementary 3 vertices, and all 10 edges occur
  exactly once:

```text
CANONICAL BIJECTION:   dark chart  <->  K5 edge  <->  schedule line
shadow(D(e)) = {e} ∪ triangle(K5 \ e)
```

## The completed K₅ calculus of a pentad core

| object | count | K₅ role |
| --- | --- | --- |
| lit charts (deleted matching) | 5 | vertices |
| schedule lines | 10 | edges (BT847: line ↔ the 2 lit charts it serves) |
| dark charts (matching orbit) | 10 | edges again — via shadow = edge + opposite triangle |
| transversal glue | — | lit charts: 2 per line (BT846); dark charts: 4 per chart, all in-schedule |

Every schedule line now has a **canonical dark chart partner** (same K₅
edge), and the dark partner's shadow contains the partner line itself plus
the opposite triangle — the structure is self-referential and rigid. The
pentad core stores its timetable three ways: as transversals of its lit
charts (BT846 reconstruction), as the K₅ edge set (BT847), and as the
shadow-paired dark matching (new).

## T3 — The tetrads are the K₅ vertices (twice, chirally)

A tetrad contains **no** matching pair (second refutation): its 4 lines lie
in 4 distinct shadow classes. Their distinguished K₅ edges form a **star at
one common vertex**, and the 5 tetrads of each chiral partition mark all 5
vertices exactly once:

```text
5 lit charts        = K5 vertices
10 schedule lines   = K5 edges       (BT847)
10 dark charts      = K5 edges again (shadow bijection)
5 + 5 chiral tetrads = K5 vertices again, twice (star centers)
```

**Every A₅-orbit structure of the pentad core is a K₅ element.** The
vertices are stored three ways (lit charts, left tetrads, right tetrads),
the edges two ways (schedule lines, dark charts) — the dodecahedra and the
meeting frame are the only non-K₅ residents of the dark sector.

## Open

- Redundancy budget: the timetable is recoverable from lit charts, dark
  matching, shadows, or tetrad stars — quantify the machine's erasure
  tolerance (how many dark/lit lines can be lost while the schedule
  reconstructs).
- The dodecahedra vs the K₅ calculus: the dodecahedron is the order-5
  Cayley-ish object the K₅ misses — relate its pentagon faces to the K₅
  5-cycles.
