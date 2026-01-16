W33 ↔ N12_58 2T cycle loop-realization (delta-multiset matching)
Generated: 2026-01-12

Core claim in this bundle
-------------------------
Using the C^4 ray realization of W33 (the 40-point, 40-line generalized quadrangle GQ(3,3)),
we can define a Z8-valued phase label on each W33 LINE via:

  k12(L) = quantized Arg(det(B_L)) in Z12, where B_L is the 4x4 matrix whose columns are the 4 rays on line L,
          after per-ray gauge fixing (first nonzero component real-positive).
  k8(L)  = k12(L) mod 8.

For adjacent lines L,M (sharing a point), define an *even* step delta:

  delta(L,M) = 2 * min( (k8(M)-k8(L)) mod 8, (k8(L)-k8(M)) mod 8 )

This yields deltas in {0,2,4,6,8}. We restrict matching to {0,2,4,6} to mirror N12_58 2T deltas.

Result
------
For each of the five nontrivial 2T cycles in:
  data/_n12/n12_58_2t_holonomy_nontrivial_cycles.csv

with lengths: 4, 9, 11, 17, 19
and delta multisets given in that file,

we found an explicit SIMPLE cycle in the W33 line graph (40 lines, 12-regular adjacency by intersection)
whose step-delta multiset matches exactly.

See:
  w33_matching_cycles_for_n12_2t_delta_multisets.csv
  w33_matching_cycles_details/cycle_len*.json

Files
-----
- w33_line_det_phase_labels.csv
- w33_line_graph_edge_deltas_z8_scaled.csv
- n12_58_2t_cycles_parsed.csv
- w33_matching_cycles_for_n12_2t_delta_multisets.csv
- w33_matching_cycles_details/*.json
- scripts_find_w33_line_cycles_matching_n12_2T.py

Next investigations suggested
-----------------------------
1) Integrate N12 'supports' sequences: attempt to assign a 12-vertex label to each W33 line-cycle
   (or to each step) consistent with the listed support 4-sets.
2) Replace per-ray gauge fixing with an Aut(W33)-equivariant gauge (e.g., orbit-stabilizer gauge)
   and see whether the same Z8 delta cycles persist canonically.
3) Interpret delta values 0/2/4/6 as discrete 'time steps' in a Z8 clock; compare to your earlier
   Z8×Z5 discussions and to the ±3 holonomy events on four-center triads.
