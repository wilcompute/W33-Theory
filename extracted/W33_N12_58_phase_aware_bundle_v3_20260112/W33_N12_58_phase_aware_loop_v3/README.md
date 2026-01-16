# W33 ↔ N12_58 Phase-Aware Loop Realization (v3)

This bundle refines the phase-aware transport constraints for realizing the 5 nontrivial N12_58 2T cycles
as closed walks inside the W33 **four-center (±3 holonomy)** triad graph.

## Key idea
Each W33 four-center triad carries a **gauge-invariant Z12 holonomy** computed from the C^4 ray realization:
  h(a,b,c) = k(a,b)+k(b,c)+k(c,a) mod 12,
where k(p,q) is the quantized argument of <v_p|v_q> on oriented noncollinear pairs.

For four-center triads, holonomy is always 3 or 9 (±3).

Each N12_58 2T cycle step has:
- a support 4-set on {0..11} (a,b mapped to 10,11),
- a delta (mod 8),
- and in the audit table, removed/added phase sums (mod 8).

## v3 predicate
Node constraints:
- delta=2 => triad holonomy must be 9 (mod 12)
- delta=6 => triad holonomy must be 3 (mod 12)

Transition constraints use the *previous* edge's (delta, removed_sum, added_sum):
- delta_prev=0 => hol(prev)=hol(curr), plus:
    - removed=add=0 => hol(curr)=9
    - removed=add=4 => hol(curr)=3
    - removed=add=6 => no extra constraint
- delta_prev=4 => hol(prev)≠hol(curr), plus:
    - (removed,added)=(6,2) => direction 3->9 only
    - (removed,added)=(0,4) => no direction constraint

These subtype constraints were selected by a small brute search over possible refinements
to ensure feasibility of all 5 cycles while remaining as specific as possible.

## Outputs
- phase_aware_v3_cycle_summary.csv
- phase_aware_v3_2T_cycle_witness_walks.csv
- w33_four_center_triads_with_ray_holonomy.csv
- w33_noncollinear_edge_phases_k_mod12.csv
- phase_aware_v3_run_summary.json
- scripts_phase_aware_loop_realization_v3.py (reproducer)

