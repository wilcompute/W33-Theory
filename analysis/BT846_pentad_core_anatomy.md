# BT846 — Pentad Core Anatomy: The Schedule Is Reconstructible From Its Pentads

**Status: PROVEN (machine-verified, `analysis/bt846_pentad_core_anatomy.py`, data `data/bt846_pentad_core_anatomy.json`)**

The pentad core's signature [5,5,10,20] on lines and [20,20] on points is now
explained term by term — with one refutation that turned into the best theorem
of the chain.

## T1 — One shared 20-point world

The two chiral pentads P₁, P₂ of a core cover the **same 20 points**, and that
20-set is one of the core's two point orbits. (Forced locally: each line of P₁
meets 4 lines of P₂ — its full point budget — so its points all lie in
cover(P₂).) The point signature [20,20] = **covered / dark**: the pentads
illuminate exactly half the substrate.

## T2 — Refutation → reconstruction theorem

**Conjectured:** the 20-line orbit = the 20 transversal slots of the 5 matching
charts. **FALSE — better:** each of the 5 charts has its 4 common transversals
(BT794), but the 5 bundles overlap and yield only **10 distinct lines** —
and those 10 lines are **exactly the marked schedule**, each schedule line
serving exactly **2 of the 5 charts** (10 × 2 = 20 = 5 × 4 ✓).

> **Reconstruction theorem.** From a pentad pair alone, the schedule is
> recovered: form the deleted matching (each line of P₁ with its unique skew
> partner in P₂ — 5 charts), take the union of their common-transversal
> bundles — that union **is** the timetable. The pentad core does not just
> mark its schedule; it *generates* it.

## T3 — The dark sector

The 20 uncovered points: each schedule line carries exactly 2 dark + 2 lit
points; each 20-orbit line carries exactly 3 dark + 1 lit. The 20-line orbit
is the dark sector's carrier (a 3-to-1 dark/lit incidence), left as the one
remaining structure to name.

## The completed dictionary for one pentad core

| orbit | identity |
| --- | --- |
| 5 + 5 (lines) | chiral pentad pair, maximal partial spreads (BT845) |
| 10 (lines) | the schedule = common transversals of the 5 matching charts |
| 20 (lines) | dark-sector carrier (3 dark : 1 lit per line) |
| 20 (points) | lit = cover(P₁) = cover(P₂) |
| 20 (points) | dark |

## Machine reading

With BT845's chart double cover: every core stores 5 charts; by this
reconstruction the charts' transversal bundles *are* the timetable. So the
compass hierarchy closes operationally — **pentads → charts → schedule** — and
conversely a schedule determines its 6 pentad cores (BT844). The icosahedral
compass layer is a lossless codec between routing glue (charts) and
measurement timetables (spreads).

## Open

- Name the 20-line dark carrier (orbit under the core ≅ A₅ on 20: the
  icosahedral edge count — is it the icosahedron's edge skeleton in line
  space?).
- The 2-charts-per-schedule-line map: schedule line → pair of charts is a
  (10, 5) double cover — which 2-regular graph on the 5 charts (pentagon or
  pentagram)?
