# W33 ↔ N12_58 Alignment (v3) — Four-center triads as the bridge

This bundle contains a concrete bijection between:

- **W33 points**: integers 0..39 from `W33_line_phase_map.csv`
- **N12_58 candidate points**: tau 3-cycles + fixed/complement-fixed points from `n12_58_candidate_w33_points_40_from_tau_cycles_and_fixed_complements_...csv`

## Hard facts recomputed from source files

- W33 has 40 points / 40 lines, each line has 4 points; each point lies on 4 lines.
- Collinearity graph is 12-regular; noncollinearity is 27-regular.
- Noncollinear triads: 3240, splitting into:
  - 2880 triads with **1 center**
  - 360 triads with **4 centers** (the “four-center triads”)

## Ray model invariant

Using the C⁴ rays, for noncollinear pairs:
- |<v_p|v_q>| = 1/sqrt(3)
- phases quantize cleanly to 12th roots; triad holonomy equals:
  - ±1 for 1-center triads
  - ±3 for 4-center triads

## Alignment objective used here (cover12)

For each mapped four-center triad (360 total), compute the union of N12 vertex-symbols appearing in its three N12 points.
- Score counts how many triads cover **all 12** symbols {0..9,a,b}.

## Best found in this run

- cover=12 : **307/360**
- cover=9  : 49
- cover=6  : 4

See:
- `best_w33_to_n12_mapping.csv`
- `best_n12_to_w33_mapping.csv`
- `w33_four_center_triads_mapped_to_n12.csv`

## Defect structure (why cover12 fails on 53/360)

The 53 non-covering four-center triads miss **exactly one** of the four disjoint 3-sets:
- 012, 345, 678, 9ab

These correspond exactly to the special fixed/complement-fixed points (F36, X35, F35, X36).
See `defective_four_center_triads.csv` and `fixed_point_structure.json`.
