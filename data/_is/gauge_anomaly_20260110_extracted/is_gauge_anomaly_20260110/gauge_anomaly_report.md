# Gauge-test: is the “missing-sector completion is constant” anomaly removable?

## Inputs used
- tomotope triangle → W(3,3) rainbow completion table: `tomotope_triangle_to_W33_rainbow_line_completion_20260110T043900Z.csv`
- derived completion dataframe `comp` (15 matched tomotope triangles)

## Baseline observation (raw labeling)
- 15 matched triangles produce 15 completed quartets.
- Missing-sector counts: {0: 6, 1: 3, 2: 3, 3: 3}
- For the 6 triangles whose triple is missing **sector 0**, the completion is **always** the same class:
  - completion class: ['sec0_m2']
  - completion m-counts: {2: 6}

Equivalently: among the 15 completions, there is a block of 6 completions that all coincide to one single projective class (here labeled `sec0_m2`).

## Gauge group tested
I tested all 144 “product-structure-preserving” relabelings of the 12 projective classes of the form

- sector action: full affine group AGL(2,2) on Z2×Z2 (24 actions), acting on sector labels (0, 1, 2, 3)
- phase action: affine group on Z3 (6 actions), m ↦ a m + b (mod 3), a ∈ {1,2}, b ∈ {0,1,2}

Total: 24×6 = 144 relabelings.

## Result: invariance (within this gauge family)
The weighted per-sector entropy score is invariant:

- min weighted entropy over 144 actions: 0.5999999999999998
- max weighted entropy over 144 actions: 0.5999999999999998

Interpretation:
- The anomaly **cannot be “smoothed out”** by any relabeling that preserves the (sector, m) product structure.
- What can change is only *which* sector label carries the 6 occurrences, and *which* m-label the constant completion is called (it cycles across {0,1,2} under m-affine shifts).

## Why this is structurally pinned (not a labeling accident)
The key combinatorial invariant is:

> there exist 6 completed quartets whose missing-class-to-complete is identical across all 6.

No permutation of labels can turn “six identical completions” into a distribution across three different completion classes; a relabeling can only rename that single class.

So, unless we change the underlying best-fit map itself (or change the sector decomposition concept), the “constant completion for the 6-triangle block” is a real feature of this tomotope→W(3,3) completion data, not an artifact.

## Files written
- `baseline_triangle_completion_table.csv`
- `gauge_transform_search_results.csv`

## Additional invariant (tomotope-point view)
Completion class `sec0_m2` corresponds to tomotope point `24-` under the best-fit map.
Across all 15 completed quartets, the missing completion point frequencies are:

tomotope_point  count
           24-      6
           12-      1
           34+      1
           23-      1
           13+      1
           12+      1
           24+      1
           14+      1
           13-      1
           23+      1

See `missing_completion_tomotope_point_frequency.csv` and `completion_quartets_with_tomotope_points.csv`.
