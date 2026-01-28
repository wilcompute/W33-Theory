# TOE Coupling Artifacts (2026-01-10)

This folder captures an explicit, *computable* coupling between:

- Orbit-0 N12_58 flipgraph transport in the **2T (binary tetrahedral)** internal clock (24 states),
- its **projective shadow** (12 projective classes `sec3_m`), and
- the **W(3,3)** measurement layer (40 lines, with 27 rainbow lines).

## Key computed facts

1. **Edge transport uses only 4 elements of 2T** on orbit-0 edges: `e`, `e*`, `(0 1 2)`, `(0 2 1)`.

2. **Projective visibility:**
   - `e` and `e*` act as the identity on projective classes.
   - `(0 1 2)` and `(0 2 1)` act nontrivially on projective classes (phase cycling + sector permutation).

3. The **defect edges** (delta4) are exactly those with `edge_elem_2T = e*` (central holonomy). Hence:
   - **defect parity/curvature is invisible projectively** (but visible in the full 2T lift).

4. The node-0 boundary line winners `(22, 8, 17)` share the fixed classes:
   - `sec0_m2` and `sec1_m0`, differing only in sector-2/sector-3 phases.

## Files

- `edge_elem_to_projective_action.csv`: induced permutation of the 12 projective classes for each edge element.
- `orbit0_edges_with_projective_images.csv`: every orbit-0 edge annotated with projective images of sector representatives.
- `edge_elem_projective_visibility.csv`: identity vs visible elements.
- `W33_lines_to_projective_quartets.csv`: every W33 line’s projective quartet/signature.
- `switchpoints_mu1p25_with_delta4_distance.csv`: lambda switchpoints annotated by distance to delta4 endpoints.
- `node0_boundary_winners_with_quartets.csv`: boundary winners enriched with projective quartets.
