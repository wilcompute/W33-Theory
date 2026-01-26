# PG(3,2) continuation results (2026-01-10)

Inputs:
- tomotope_triangle_to_W33_rainbow_line_completion_20260110T043900Z.csv
- tomotope_triangles_to_projective_triples_and_rainbow_lines_20260110T043900Z.csv
- tomotope_points_to_N12_58_projective_classes_bestfit_20260110T043900Z.csv

Key derived facts:
1. The 15 matched tomotope triangles produce 15 rainbow quartets with invariant (m0+m1+m2+m3) mod 3 = 1 (verified).
2. Each quartet corresponds to a unique coefficient vector (a0,a1,a2,a3) in Z3^4 satisfying a0-a1-a2+a3 = 1 (mod 3).
   There are exactly 27 such vectors (affine 3-space over Z3). Tomotope realizes 15 of them.
3. Mapping coefficients to a support vector in F2^4 by b_i = 1 iff a_i != 0 yields 15 distinct nonzero vectors,
   i.e. exactly the 15 points of PG(3,2). The tomotope 15 hit 10 distinct support points; 5 are missing.
4. The 5 missing support points form a 5-cap (no three collinear), i.e. an ovoid in PG(3,2).
5. The 6 tomotope lines whose completion is sec0_m2 yield 5 distinct support points; these also form an ovoid in PG(3,2).

Artifacts written:
- phase_functions_hyperplane_27_with_pg32_shadow.csv
- tomotope15_phase_functions_with_pg32_shadow.csv
- missing12_phase_functions.csv
- PG32_points_15.csv
- PG32_lines_35.csv
- W32_doily_isotropic_lines_15_standard_symplectic.csv
- ovoid_*_support_points.csv
- ovoid_intersections_with_PG32_lines.csv
- ovoid_line_intersection_summary.csv
