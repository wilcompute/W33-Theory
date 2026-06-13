# BT864 — The Triality Census: Generation Symmetry Is Matter-Blind but Gauge-Visible

**Status: PROVEN (exhaustive over all 800 order-3 elements / 4 classes, `analysis/bt864_triality_census.py`, data `data/bt864_triality_census.json`)**

BT863 showed every order-3 symmetry splits the 81-dim matter (Steinberg)
register identically as 27+27+27 — so the choice of "physical triality"
**cannot be read from the matter sector at all.** BT864 asks where the four
order-3 classes *do* differ: the gauge/point sector.

## The census

PSp(4,3) has exactly 4 classes of order-3 elements (800 elements):

| class size | fixed points | fixed lines | fixed schedules | gauge split (C[40 points]) | identity |
| --- | --- | --- | --- | --- | --- |
| 40 | **13 = Φ₃** | 4 | 0 | **22 + 9 + 9** | transvection (fixes its axis plane PG(2,3)) |
| 40 | 13 = Φ₃ | 4 | 0 | 22 + 9 + 9 | transvection (inverse class) |
| 240 | 4 = μ | 1 | **6 = q!** | **16 + 12 + 12** | "matter triality" candidate |
| 480 | 4 = μ | 7 | 3 | 16 + 12 + 12 | regular order-3 |

(Gauge split = multiplicities of 1, ω, ω² on the 40-point permutation
module: trivial-multiplicity = #orbits = f + (40−f)/3, nontrivial each
(40−f)/3.)

## The physics reading

> **Generation symmetry is matter-blind but gauge-visible.**
> All four classes split the protected matter register 27+27+27 (BT863) —
> the three generations are *identical* to the matter/Steinberg sector. But
> the gauge sector (the 40-point module) sees the class: transvections grade
> it 22+9+9, the regular classes 16+12+12. This mirrors the Standard Model
> exactly: the three generations carry *identical gauge charges* (matter
> sector blind to generation) yet differ entirely through their *Yukawa /
> mass couplings* (gauge-sector–visible structure). Here it is a theorem
> about where an order-3 symmetry's eigenvalue degeneracy lives, not a
> modeling assumption.

## Which class is the physical triality?

- The **transvections** (size 40, the root elements) fix a whole PG(2,3)
  plane of 13 = Φ₃ points and **no schedule** — too much gauge structure
  fixed; they are the "color-rotation"-like elements, deep in the gauge
  sector.
- The **240-class** fixes only μ = 4 points but **6 = q! schedules** — the
  natural candidate for the physical generation triality: it acts almost
  freely on points (matter-like) while preserving a q!-family of complete
  measurement programs (the timetable library's order-3 symmetry, the
  operational home of generation cycling).
- The **480-class** (regular) fixes 4 points, 7 lines, 3 schedules.

The Pillar 68 texture-triality R (9 free 3-orbits on the 27-shell, CKM/PMNS
grading) acts *within a point stabilizer* on the 27 non-neighbours, so its
ambient class is determined by how it sits over a fixed base point — the
240-class (μ fixed points, one of which can be the base) is the consistent
lift; pinning the exact correspondence to Pillar 68's Yukawa grading is the
remaining step.

## Open

- Restrict each class to a point stabilizer and identify the one realizing
  Pillar 68's R (9 free orbits on the 27-shell) exactly.
- The 6 vs 3 schedule-fixing (240 vs 480 class) vs the 6/3 in the BT835
  overlap law — same q!/q split appearing in the timetable symmetry.
