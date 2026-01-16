# PG(3,2) shadow of the Z3 hyperplane of phase-functions

We represent each rainbow-line phase-function by coefficients (a0,a1,a2,a3) in Z3^4 with constraint:
a0 - a1 - a2 + a3 ≡ 1 (mod 3).

This hyperplane has 27 points (≅ Z3^3). Binarizing coefficients by support (nonzero → 1, zero → 0) yields
exactly the 15 nonzero 4-bit patterns, i.e. the 15 points of PG(3,2).

Key computed facts:
- All 27 phase-functions cover all 15 PG(3,2) points via support-pattern fibers.
- The tomotope-derived 15 phase-functions occupy only 10 of those 15 PG points (with multiplicity),
  leaving 5 PG points absent in the tomotope image.
- A canonical 'one-per-fiber' completion (15 phase-functions) gives an explicit lift of PG(3,2)
  into the Z3 hyperplane; it matches the tomotope choices on the 10 present fibers, and adds the 5 missing fibers.

Files:
- phase_functions_27_hyperplane_with_pg32_shadow.csv
- tomotope15_phase_functions_with_pg32_shadow.csv
- missing12_phase_functions.csv
- pg32_point_fiber_sizes_and_tomotope_counts.csv
- canonical_pg32_lift_15_phase_functions.csv
- PG32_lines_35.csv
- PG32_lines_with_zero_coeff_sum_under_canonical_lift.csv
