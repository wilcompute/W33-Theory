# BT837 — The Schedule Library Is Itself a Classical Geometry

**Status: PROVEN (machine-verified, `analysis/bt837_schedule_library_geometry.py`, data `data/bt837_schedule_library_geometry.json`)**

BT836 put the Grünbaum–Coxeter hemicells inside every schedule. BT837 zooms
out: the library of all 36 schedules carries its own classical geometry, and
the Petersen structures distribute over the substrate with perfect uniformity.
Three exact theorems.

## T1 — Skew pairs and the apartment count

W(3,3) has exactly **540 skew line pairs** (the chart count). Each schedule
(spread) contains C(10,2) = 45 internal pairs — all skew. Census over all 36
schedules:

```
every skew pair lies in EXACTLY 3 schedules
36 × 45 = 1620 (schedule, pair) flags = 540 × 3 = #apartments of the Tits building
```

The apartment count 1620 is literally the flag count of the (schedule ⊃ skew
pair) incidence relation.

## T2 — The near-partner graph is SRG(36, 15, 6, 6)

Two schedules share 4 lines (near, 15 partners) or 1 line (far, 20 partners) —
the BT835 overlap law. The **near graph** on the 36 schedules is strongly
regular with parameters

```
SRG(36, 15, 6, 6)   —   λ = μ = 6, verified exhaustively
```

This is the *other* classical rank-3 graph of U₄(2) ≅ PSp(4,3) (the rank-3
action on the 36 cosets of S₆). So the substrate's timetable library is itself
a strongly regular geometry of the substrate's own group: **W(3,3) =
SRG(40,12,2,4) on states, SRG(36,15,6,6) on schedules** — the machine's
configuration space and its control space are the two rank-3 geometries of one
group.

## T3 — Petersen homes: the 6³ icosahedral cores

- Every spread stabilizer contains **exactly 6 icosahedral A₅ cores** (the
  conjugacy class of 2I/center inside S₆), and the 6 cores give **6 distinct
  Petersen splits** of the 45 internal pairs. Globally: 36 × 6 = **216 = 6³
  icosahedral cores** in PSp(4,3), each marking its unique spread (its
  [10,30] line-orbit 10-set).
- **T3b (within one schedule):** every internal pair is a Petersen edge under
  exactly **2 of the 6 cores** (forced: S₆ permutes the cores transitively and
  is transitive on the 45 pairs; 6×15 = 45×2).
- **Global census:** every one of the 540 skew pairs is a Petersen edge in
  exactly **6** (schedule, core) structures — never 0, never anything else:

```
3 schedules per pair × 2 cores per schedule = 6 Petersen homes per skew pair
total Petersen flags = 36 × 6 × 15 = 3240 = 540 × 6
```

3240 is also the triangle count of the complement graph Q (Pillar 109) — a
coincidence to chase.

## Machine reading

- The controller's timetable-switch graph (BT835) is not ad hoc — it is the
  U₄(2) rank-3 geometry. Routing in the *control plane* enjoys the same
  strongly-regular guarantees as routing in the *data plane* (W33 itself):
  any two timetables have exactly 6 common near-neighbors, whether or not
  they are themselves near.
- Every skew pair (= chart, = potential hypercube glue) has exactly 3
  schedule homes and exactly 6 hemi-dodecahedral (Petersen) homes: the GC
  cell structure of BT836 is not an accident of one spread but a perfectly
  uniform fibration over the whole library.

## Open

- Identify the 216 = 6³ icosahedral cores as a named G-set (index 216 = 25920/120;
  normalizer order 120 — S₅ or A₅×Z₂?) and connect to the 216-element Hessian
  group of Pillar 69.
- The 3240 Petersen flags vs the 3240 triangles of Q (Pillar 109): bijection?
- Lift T2 to the Clifford level: does the near-graph SRG admit the same
  hypercube-chart atlas treatment as W33 itself (rank-3 ⇒ charts on the
  μ-graph)?
