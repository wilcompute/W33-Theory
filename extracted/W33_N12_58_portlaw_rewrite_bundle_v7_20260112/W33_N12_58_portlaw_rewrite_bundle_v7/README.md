# W33 canonical ports + N12_58 port-law rewrite (v7)

This bundle does three things:

1) **Canonical port labeling per K4 component**
   - Each W33 four-center triad belongs to a unique K4 component (90 total).
   - Each component has:
     - a **center quad** C (the 4 common neighbors of any pair in the outer quad),
     - an **outer quad** P (4 mutually noncollinear points),
     - 4 triad states = the 3-subsets of P, naturally labeled by the **excluded point** in P.
   - Each directed move between triads swaps excluded points x↔y.
   - The move is canonically labeled by the **perfect matching index** on P that contains the pair {x,y}:
       idx=0: (p0,p1)(p2,p3)
       idx=1: (p0,p2)(p1,p3)
       idx=2: (p0,p3)(p1,p2)
     where P is ordered increasingly by W33 point id (deterministic).

2) **Gauge-invariant commutator (Bargmann 4-cycle) on every directed move**
   - For any directed move within a K4 component, the Z12 commutator phase is **identically 6**,
     i.e. the complex phase is **-1**.
   - See: `w33_k4_moves_directed_commutator.csv` and `commutator_phase_summary.json` (in earlier v6 bundle).

3) **Rewrite of the phase-aware 2T loop solver in rem_idx→add_idx terms**
   - From the flip audit `n12_58_flip_delta_audit_all_edges.csv`, we compute:
       rem_idx, add_idx ∈ {0,1,2}
     where indices refer to the 3 matchings of the support 4-set {s0<s1<s2<s3}.
   - We derive a **port-law** that constrains the allowed K4 port (matching index) on each transport step.
   - Crucially, the reduced key law depends only on:
       **(delta_from_nodes, rem_idx, add_idx)**
     i.e. it is expressed purely in `rem_idx → add_idx` terms plus the delta label already present in the audit.
   - The reduced port-law reproduces the **exact same** minimal-cost witnesses as the earlier v3 holonomy solver
     for the 5 nontrivial 2T cycles:
       per-cycle costs = [2,4,5,9,9], total = 29.

Files:

- `w33_k4_components.csv`
- `w33_k4_edges_undirected.csv`
- `w33_k4_moves_directed_commutator.csv`
- `w33_four_center_triads_with_ray_holonomy.csv`
- `n12_58_flip_delta_audit_with_matching_indices.csv`
- `port_law_reduced_key.json`
- `cycle_witness_v3_holonomy_solver.csv`
- `cycle_witness_portlaw_solver.csv`
- `witness_equivalence_check.json`

