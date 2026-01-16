# W33 ↔ N12_58 line-set mutation + loop-realization optimization (v5)

This bundle exports the best mapping found under the following constraints:

- N12_58 has 7 size-4 point blocks (tau_3cycle orbit blocks) and 3 size-2 blocks.
- Each size-4 block is mapped to a *single* W33 line, and the 7 blocks map to 7 pairwise-disjoint W33 lines (a size-7 partial spread).
- Each size-2 block maps to a collinear pair of W33 points.
- The full mapping is a bijection between 40 N12 points and 40 W33 points.

Objective:

1) Minimize the total minimal number of **cover-12** four-center triads required to realize the 5 nontrivial N12 2T holonomy cycles as closed walks in the W33 four-center triad adjacency graph.
2) Secondary: maximize the number of **cover-12** triads among the 360 W33 four-center triads.

Key outputs:

- outputs/w33_to_n12_mapping.csv
- outputs/n12_to_w33_mapping.csv
- outputs/w33_four_center_triads_table.csv
- outputs/2T_cycle_witness_walks.csv
- outputs/run_summary.json

Reproduce:

    python3 scripts/reproduce_best_mapping_eval.py
