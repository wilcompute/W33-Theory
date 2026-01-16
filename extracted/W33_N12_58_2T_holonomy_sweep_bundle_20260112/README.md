# W33 ↔ N12_58: 2T-holonomy–aware embedding sweep (2026-01-12)

This bundle contains a **constraint-preserving annealing sweep** that aligns the N12_58-derived 40-point candidate set
to the W33 (= GQ(3,3)) 40-point incidence geometry.

## Inputs (from your repository data)
- `data/_workbench/02_geometry/W33_line_phase_map.csv`
- `data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv`
- `data/_n12/n12_58_candidate_w33_points_40_from_tau_cycles_and_fixed_complements_*.csv`
- `data/_n12/n12_58_candidate_lines_from_size12_orbits_tau_cycle_sets_*.csv`
- `data/_n12/n12_58_2t_holonomy_nontrivial_cycles.csv`

## Constraints enforced
- The **7 unique 4-point N12 blocks** map to **7 W33 lines** (a size-7 partial spread).
- The **3 unique 2-point N12 blocks** map to **collinear W33 pairs**.
- Remaining 6 points map bijectively to remaining W33 points.

## Scoring
Primary score:
- Among the **360 W33 four-center triads**, maximize the number whose mapped N12 triple covers all 12 vertex symbols
  (interpreting `a→10`, `b→11`).

Secondary score (tie-break / defect-focused):
- On defect triads only, maximize weighted inclusion of N12 **2T support 4-sets**.
  Weights are derived from frequency across the 5 nontrivial 2T cycles.

## Best result in this run
- Four-center triads: 360
- cover(12) triads: **302 / 360**
- defects: 58

See:
- `best_n12_to_w33_mapping.csv`
- `best_w33_to_n12_mapping.csv`
- `w33_four_center_triads_mapped_to_n12_with_holonomy_and_2T_support_score.csv`
- `2T_cycle_support_inclusion_stats_over_w33_four_center_triads.csv`

## Notes on holonomy
For each oriented noncollinear pair (p,q), we quantize the phase of ⟨v_p|v_q⟩ to Z12.
For any four-center triad (a,b,c), the cycle holonomy h(a,b,c) is always **±3 mod 12** (i.e. 3 or 9),
split evenly 180/180 in this realization.
