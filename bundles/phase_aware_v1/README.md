# W33 ↔ N12_58 phase-aware 2T-loop realization (v1)

This bundle uses **your** W33 ray realization (C^4 vectors) to attach a **Z12 phase label** to each oriented noncollinear pair,
and then a **Z12 holonomy** to each W33 four-center triad (the 360 special noncollinear triples in GQ(3,3)).

It then realizes the 5 nontrivial N12_58 2T cycles (from `n12_58_2t_holonomy_nontrivial_cycles.csv`) as closed walks
in the **W33 four-center triad adjacency graph** (share 2 points), while enforcing a **phase-aware constraint** derived from
the cycle edge deltas (from `n12_58_flip_delta_audit_all_edges.csv`):

- delta == 2  ⇒ require triad holonomy = 9 (mod 12)
- delta == 6  ⇒ require triad holonomy = 3 (mod 12)
- delta in {0,4} is left unconstrained in this v1 run (reserved for later refinement).

Objective minimized:
- the number of **cover-12** four-center triads used along the walk (cover-12 triads trivially satisfy any support-set).

## Key outputs

- `phase_aware_2T_cycle_witness_walks.csv`  
  Step-by-step witness walks for all 5 nontrivial 2T cycles, including delta, required holonomy (when applicable),
  chosen triad, triad holonomy, and cover-size diagnostics.

- `phase_aware_run_summary.json`  
  Per-cycle and total minimal cover-12 usage under the phase constraints.

- `w33_four_center_triads_with_ray_holonomy.csv`  
  (and the richer table `w33_four_center_triads_with_ray_holonomy.csv` in this bundle) four-center triads + holonomy.

- `w33_noncollinear_edge_phases_k_mod12.csv`  
  Oriented noncollinear edge phase labels.

## Results (this run)

Per-cycle minimal cover-12 usage:
{0: 1, 1: 4, 2: 6, 3: 10, 4: 11}

Total minimal cover-12 steps across the 5 cycles:
32

Cover-12 triads among the 360 four-center triads under the current mapping:
276 / 360

## Reproduction

Run the scripts from the repository root (or adjust paths):

1. Recompute ray phases and triad holonomies:
```bash
python scripts_recompute_w33_ray_holonomy.py \
  --w33_csv data/_workbench/02_geometry/W33_line_phase_map.csv \
  --rays_csv data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv \
  --outdir .
```

2. Phase-aware loop realization:
```bash
python scripts_phase_aware_loop_realization.py \
  --w33_csv data/_workbench/02_geometry/W33_line_phase_map.csv \
  --rays_csv data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv \
  --n12_cycles_csv data/_n12/n12_58_2t_holonomy_nontrivial_cycles.csv \
  --n12_audit_edges_csv data/_n12/n12_58_flip_delta_audit_all_edges.csv \
  --w33_to_n12_mapping_csv w33_to_n12_mapping.csv \
  --outdir .
```
