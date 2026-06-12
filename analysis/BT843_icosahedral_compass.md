# BT843 — The Icosahedral Compass: Two A₅ Classes, Two 216-Sets, One D₄ Flag Stabilizer

**Status: PROVEN (GAP + python, `analysis/bt843_icosahedral_compass.py`, GAP witnesses `.tmp/gap_bt843*.g`, data `data/bt843_icosahedral_compass.json`)**

BT837 found 216 = 6³ icosahedral cores. BT843 identifies the G-set — and
discovers there are **two different icosahedral compasses** in the substrate.

## GAP facts

PSp(4,3) has exactly **two conjugacy classes of A₅**, both with normalizer
**S₅** and **216 conjugates each**, and Out = 2 does **not** fuse them. They are
distinguished by their degree-40 orbit signatures:

| class | on lines | on points | marks |
|---|---|---|---|
| **spread compass** | **[10, 30]** | [20, 20] | its unique spread (BT836/837 cores) |
| **pentad compass** | **[5, 5, 10, 20]** | [20, 20] | two distinguished line *pentads* — an F₅ = 5 echo (BT813: "icosa sees 5 = F₅ tritangents") |

Both 216-actions are transitive of **rank 10**, imprimitive with a **unique
block system of size 6** (quotient = a 36-set; the 5-suborbit = the 5
same-block partner cores). But they are **not isomorphic G-sets**:

```
spread compass suborbits: [1, 5, 10, 10, 20, 20, 20, 30, 40, 60]
pentad compass suborbits: [1, 5, 10, 10, 20, 20, 30, 30, 30, 60]
```

Same group, same normalizer type, same rank, same blocks — different
mutual-position spectra. The substrate contains two inequivalent ways of
being icosahedral.

## T1 — The Petersen flags are a single coset geometry

The 3240 Petersen flags (schedule, core, 15-orbit pair) of BT837 form **one
transitive PSp orbit** with stabilizer of order 8 of type **D₄** (element
orders [1,2,2,2,2,2,4,4], non-abelian). So the hemi-dodecahedral edge
structure of the whole library is the coset geometry PSp(4,3)/D₄.

## T2 — Honest refutation: 3240 ≠ 3240

The complement graph Q has exactly 3240 triangles (Pillar 109). Computed
orbit split under PSp: **[360, 2880]** (stabilizers of order 72 and 9). The
Petersen flags are transitive with stabilizer D₄ of order 8. **The two
3240-sets are NOT isomorphic G-sets** — the count match is numerology only.
(Recorded so nobody chases this bijection again.)

## Machine reading

- The spread compass is the clock-bearing: each core points at its unique
  timetable. The **pentad compass is new hardware**: each of its 216 cores
  distinguishes two 5-line pentads — a natural F₅ register (5 = F₅ appears in
  the tier ratio 27/80 = 3³/(2⁴·5) and in BT813's icosa–polar [5,40] row).
  Conjecture: the pentad pairs are the operational home of the F₅ factor.
- 216 = 6³ cores per compass; 216 is also the Hessian-group order in the
  Pillar-69 chain (648 = 3·216) — the rank-10 suborbit data above is the
  fingerprint any future identification must match.

## Open

- Identify the pentad compass's 36-quotient (the blocks of 6): is it the
  same 36 schedules, or a dual 36-set?
- What incidence structure do the 216 + 216 cores form together (joint
  orbitals of the two compasses)?
- The pentads themselves: 216 cores × 2 pentads = 432 pentad slots; how many
  distinct 5-line pentads, and what geometry do they tile?
