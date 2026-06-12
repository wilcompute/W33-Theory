# BT856 — The Dark Charts ARE the Mirror Bus

**Status: PROVEN (machine-verified over all 216 cores, with exact G-set isomorphism, `analysis/bt856_dark_mirror_bus.py`, data `data/bt856_dark_mirror_bus.json`)**

The biggest unification of the compass arc: the middleware's 2160-slot D₁₂
mirror bus (BT815 — the chart-transversal/antipode slot space, the machine's
global transport object) is **the same PSp-set** as the compass layer's dark
charts.

## The three steps

1. **Census (all 216 pentad cores).** Each core carries 10 dark charts
   (shadow matching, BT854): 216 × 10 = **2160** slots, and every one of the
   540 skew pairs occurs as a dark chart in **exactly 4** cores —
   2160 = 540 × 4, the *same factorization* as the BT815 repair atlas.
2. **Stabilizer.** The stabilizer of one (core, dark chart) slot has order
   12 with profile {1:1, 2:7, 3:2, 6:2} — the **D₁₂ profile** — hence the
   slot space is transitive of degree 25920/12 = 2160.
3. **G-set isomorphism.** The slot stabilizer is **conjugate in PSp** to the
   BT815 antipode-slot stabilizer (stabilizer of a (chart, transversal)
   pair), proven by direct search over all 25920 elements. Two transitive
   G-sets with conjugate stabilizers are isomorphic:

```text
(core, dark chart) slots  ≅  the 2160-slot D12 mirror bus     (as PSp-sets)
```

## Why the multiplicity-4 matches

A dark chart's transversal tetrad **is** its schedule shadow (BT854), so the
4 cores hosting a given skew pair as dark chart all have schedules
containing that pair's 4 common transversals — the dark-side multiplicity 4
and the BT815 transversal multiplicity 4 are the same 4.

## Machine reading

The mirror bus was defined abstractly (BT815) as the antipode-slot space
with its 24·45·48 = 51840 runtime lift. It now has a **hardware
identification**: a bus slot = one icosahedral needle's dark chart. The
compass chain closes end to end:

```text
pentads -> lit charts -> schedule          (BT845/846: reconstruction)
schedule -> K5 edges <-> dark charts       (BT847/854: shadow bijection)
(core, dark chart) -> mirror bus slot      (BT856: G-set isomorphism)
```

The icosahedral compass layer is not a parallel structure to the middleware
— it *generates* the middleware: timetables from its lit side, the
transport bus from its dark side. Routing state (mirror slots) is dark-
sector data; measurement state (schedules) is lit-sector data; one A₅ per
needle holds both.

## Open

- Push the isomorphism to the runtime lift: does the 24·45·48 factorization
  (BT826) read naturally on (core, dark chart) coordinates?
- The chirality correlation question (BT855 open) — now sharper: does the
  bus inherit a chirality grading from the dark dodecahedra's two lifts?
