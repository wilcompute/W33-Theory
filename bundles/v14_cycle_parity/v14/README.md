W33 ↔ N12_58: Cycle parities, loop lifts, and canonical Z2 gauge (v14)

This bundle operationalizes the plan:
1) Treat the 90 center-quads (four-center triad components) as a 2-cover of the 45-point quotient Q.
2) Use the precomputed Z2 voltage/sign on Q edges (quotient_Q_edges_with_Z2_voltage.csv).
3) Fix a *canonical gauge* by selecting a BFS spanning tree from root 0 and choosing vertex flips g[v] so that
   every tree edge has canonical voltage 0. This yields deterministic canonical voltages on all Q edges:
       w_canon(u,v) = w_raw(u,v) XOR g[u] XOR g[v]
4) Identify where each 2T cycle lives in the 2-cover by mapping its W33 center_quad to quad_id and then to the
   corresponding gq42_point and sheet (quad0/quad1 under the canonical gauge).
5) Compute per-cycle:
   - commutator parity: (-1)^{#moves} using the universal commutator phase (-1) per K4 move
   - triad holonomy phase product: Π exp(2πi h/12) with h ∈ {3,9} giving factors ±i
   - total complex phase = commutator_sign * holonomy_phase

Files:
- canonical_gauge_assignment.csv
    gq42_point -> (quad0, quad1) after canonical gauge fixing
- quotient_Q_edges_with_Z2_voltage_canonical.csv
    all 720 Q edges with raw and canonical voltages
- 2T_cycle_phase_parity_and_lift_summary.csv
    5 nontrivial 2T cycles with gq42_point, sheet, commutator sign, holonomy phase, total phase
- 2T_cycle_witness_enriched_with_gauge_and_commutator.csv
    the 60-step witness table (from portlaw_v7) with quad_id, gq42_point, canonical sheet, and commutator factor
- Q_triangle_voltage_parity_stats_canonical.json
    triangle parity distribution under the canonical gauge
- Q_triangle_parity1_sample.csv
    sample of nontrivial (parity=1) triangles in Q with edge voltages

Repro notes:
Inputs are read from:
- /mnt/data/center_quad_scheme_v12/*
- /mnt/data/center_quad_gq42_v13/*
- /mnt/data/center_quad_graph_v11/center_quad_nodes.csv
- /mnt/data/portlaw_v7/cycle_witness_portlaw_solver.csv
- /mnt/data/proj_data/data/_n12/n12_58_2t_holonomy_nontrivial_cycles.csv

