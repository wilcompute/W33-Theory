# BT1367--BT1369 -- Phase Gauge, Q6 Equivariance, and Generation-Time Scheduler

## Summary

This packet executes the three open moves after BT1364--BT1366:

1. build the global qutrit phase gauge over all W33 skew-line matchings and
   test quadrangle holonomy;
2. upgrade the Q6/tomotope flag bridge from count equality to a verified
   equivariant group-action certificate;
3. push the `2160 = 45 * 3 * 16` grading against the
   Steinberg generation/chirality data.

## BT1367 -- Phase Gauge Holonomy

BT361 gives one overlap-4 perfect matching between the three qutrit phase
sheets for every skew pair of W33 lines.  BT1367 treats those matchings as an
`S3` connection on the 40-line skew graph.

The global spanning-tree gauge exists, but the connection is not flat.  Around
all simple skew-line quadrangles:

```text
quadrangles = 59670
identity holonomy = 11070
transposition holonomy = 29160
3-cycle holonomy = 19440
```

So the selector phase bundle has real finite curvature.  The next correction
problem is now precise: find a cochain that changes this holonomy profile, not
merely a prettier phase labeling.

## BT1368 -- Q6 Equivariant Flag Lift

The visible tomotope flag CSV coordinates do not automatically make a Q6 edge
model equivariant.  BT1368 therefore tests the group action directly.

Inside `Aut(E(Q6)) = C2^6 : S6`, with the six Q6 directions read as the six
edges of a K4, there is a unique `S3`-invariant `2^4` translation subspace
whose edge action has:

```text
order = 96
orbits = 96 + 96
order profile = {1:1, 2:27, 3:32, 4:36}
```

This exactly matches `Aut(tomotope)` on the true 192-flag model.  GAP verifies
the two permutation groups are isomorphic.  Since both actions are regular on
each 96-point orbit, the isomorphism plus a base edge/flag choice gives an
actual equivariant bijection orbit-by-orbit.

Boundary: this proves the group-action lift.  It does not claim the naive
human-readable flag CSV coordinates are already the equivariant Q6 coordinates.

## BT1369 -- Generation-Time Scheduler

BT1366 gave:

```text
2160 = 45 * 3 * 16
```

BT1369 tests this against the Steinberg data:

```text
BT863: 81 = 27 + 27 + 27
BT868: order-6 grading has 15 positive-chirality channels per generation
BT1366: 135 sixteen-slot phase orbits
```

The scheduler shape is:

```text
135 = 5 * 27
    = 3 generations * 3 time residues * 15 positive-chirality channels

2160 = 135 * 16
```

Thus each Steinberg generation state receives five sixteen-slot tomotope
register lanes, or 80 slots.  Equivalently, each generation phase gets a
45-geometry time wheel, and `45 = 3 * 15` is the time-residue lift of the
positive-chirality branch in BT868.

Boundary: this is a verified dimensional and character-profile scheduler.  A
basis-level action of the 2160 slots on the Steinberg module remains the next
objectwise test.

## Verification

```bash
python3 analysis/bt1367_global_qutrit_phase_gauge_holonomy.py
python3 analysis/bt1368_q6_tomotope_equivariant_flag_lift.py
python3 analysis/bt1369_steinberg_generation_time_scheduler.py
python3 tests/test_bt1367_bt1369_phase_q6_scheduler_lifts.py
python3 -m py_compile analysis/bt1367_global_qutrit_phase_gauge_holonomy.py analysis/bt1368_q6_tomotope_equivariant_flag_lift.py analysis/bt1369_steinberg_generation_time_scheduler.py tests/test_bt1367_bt1369_phase_q6_scheduler_lifts.py
python3 -m json.tool data/bt1367_global_qutrit_phase_gauge_holonomy.json
python3 -m json.tool data/bt1368_q6_tomotope_equivariant_flag_lift.json
python3 -m json.tool data/bt1369_steinberg_generation_time_scheduler.json
```
