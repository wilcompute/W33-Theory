# Preserved-27 vs hyperplane D8 conjugacy check

Result: no conjugating bijection exists between the preserved-27 automorphism action and the hyperplane D8 action.

Evidence:
- Exhaustive search over all D8 generator pairs (order-4 r, order-2 s with srs=r^{-1}) found no equivariant mapping.
- The permutation cycle-type multisets differ, so the actions are not conjugate in S27.
- The central involution (r^2) fixes 7 points in the preserved-27 action but only 3 in the hyperplane action (no size-4 orbit is stabilized by the center in the hyperplane case).
  - Preserved-27 has a 4-point orbit with center stabilizer; hyperplane does not.
- Searching D8 subgroups inside the full 1296 closure (adding the affine involution) still yields zero matches to the preserved-27 cycle-type.

Cycle-type counts (lengths sorted):

| cycle_type | preserved27 | hyperplane_D8 |
| --- | --- | --- |
| 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 | 1 | 1 |
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 | 0 | 2 |
| 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 | 3 | 0 |
| 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 | 2 | 3 |
| 1 2 2 2 4 4 4 4 4 | 2 | 0 |
| 1 2 4 4 4 4 4 4 | 0 | 2 |

Notes:
- Order distributions match (1×1, 5×2, 2×4), but cycle-type structure does not.
- Orbit sizes alone (8,4,4,4,4,2,1) are insufficient to identify the action.

See `preserved27_vs_hyperplane_D8_cycletypes.csv`, `preserved27_vs_hyperplane_D8_cycletype_counts.csv`, `preserved27_vs_hyperplane_D8_stabilizers_summary.md`, and `hyperplane1296_affine_involution_summary.md`.
