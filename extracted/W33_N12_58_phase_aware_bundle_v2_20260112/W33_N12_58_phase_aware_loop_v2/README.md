W33 ↔ N12_58 phase-aware loop realization (v2)

What this run adds versus v1:
- Keeps the ray-derived Z12 triad holonomy constraint for delta=2/6 edges:
    delta=2 -> triad holonomy 9 (mod 12)
    delta=6 -> triad holonomy 3 (mod 12)
- Adds a *transition* constraint (between consecutive chosen triads) for delta=0/4 edges:
    delta=0 -> consecutive triads must have the same holonomy (3->3 or 9->9)
    delta=4 -> consecutive triads must have different holonomy (3<->9)

Outputs:
- phase_aware_v2_2T_cycle_witness_walks.csv : step-by-step witness for all 5 nontrivial 2T cycles
- phase_aware_v2_run_summary.json : metrics and predicate definition

Notes:
- In W33, the 360 four-center triads partition into 90 disjoint K4 components, each determined by a center-quad.
  The witness walks occur inside two such components (see summary JSON).
