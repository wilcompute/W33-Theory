# TOE story so far (2026-01-10 snapshot)

This is a narrative walkthrough of the TOE dataset snapshot. It is written to be read in order and to connect
the artifacts across PG(3,2), tomotope, W(3,3), and the Z2 flux toggle.

## 1) The tomotope and its 15 quartets
We start from the tomotope matched set: 15 triangles that map into W(3,3) rainbow lines and into a Z3
hyperplane of phase-function coefficients. This produces 15 rainbow quartets on the 12 projective classes.

Key artifacts:
- `data/_toe/take_it_all_way_20260110/toe_take_it_all_way_report.md`
- `data/_tomotope/tomotope_triangle_to_w33_rainbow_line_completion_20260110t043900z.csv`
- `data/_tomotope/tomotope_triangles_to_projective_triples_and_rainbow_lines_20260110t043900z.csv`

## 2) The Z3 hyperplane and its PG(3,2) shadow
The 27 phase-functions are the affine hyperplane:
  a0 - a1 - a2 + a3 = 1 (mod 3).
Binarizing coefficient support maps this Z3 hyperplane onto the 15 points of PG(3,2).

Facts:
- The full 27 cover all 15 PG(3,2) points.
- The tomotope 15 only hit 10 of those points.
- The 5 missing points form a 5-cap (ovoid) in PG(3,2).
- The 6 tomotope lines with sec0_m2 completion form another ovoid.

Key artifacts:
- `data/_pg32/shadow_20260110/report_pg32_shadow.md`
- `data/_pg32/continue_20260110/pg32_continuation_report.md`
- `data/_pg32/shadow_20260110/canonical_pg32_lift_15_phase_functions.csv`

## 3) Symmetry closure: D6 and D8 to 1296
Two explicit symmetry actions are computed:
- D6 from the incidence automorphisms of the (12 points, 15 lines) configuration.
- D8 from liftable doily symmetries acting on the 27 phase-functions.

Combined, they generate a 1296-element group acting transitively on the 27 hyperplane.
The tomotope 15 is stabilized setwise by the D6 subgroup (size 12), so there are 108
tomotope-equivalent configurations.

Key artifacts:
- `data/_toe/take_it_all_way_20260110/toe_take_it_all_way_report.md`
- `data/_toe/take_it_all_way_20260110/combined_group_size.txt`
- `data/_toe/take_it_all_way_20260110/generators_on_27.txt`

## 3b) A4 and 2T bridge (center quotient)
The A4 action induced on H^1 for N12_58 is a 12-element symmetry that should arise as the quotient
of the binary tetrahedral group (2T) by its central element. This is verified directly by collapsing
the 2T multiplication table under g ~ g*, which matches the A4 table exactly.

Key artifacts:
- `data/_workbench/05_symmetry/N12_extended_summary.md`
- `data/_workbench/05_symmetry/2T_to_A4_quotient_check.md`

## 4) Coupling to transport (2T clock and projective shadow)
Orbit-0 transport on the N12_58 flipgraph uses only 4 elements of the binary tetrahedral group (2T):
  e, e*, (0 1 2), (0 2 1).
Projectively, e and e* are invisible; only the 3-cycles move projective classes.
The four defect (delta4) edges are exactly those labeled e*.

This makes the central Z2 holonomy visible in the 2T lift but invisible in the projective shadow.

Key artifacts:
- `data/_toe/coupling_20260110/README_TOE_coupling.md`
- `data/_toe/coupling_20260110/orbit0_edges_with_projective_images.csv`
- `data/_toe/coupling_20260110/edge_elem_projective_visibility.csv`

## 5) Flux toggle effects (remove central Z2)
A flux toggle replaces e* with e on the four defect edges. Two measurement models were tested:

Mask-based W33 measurement (global vs node0-local):
- Global clock marginal: winners unchanged; stability values shift slightly upward.
- Node0-local marginal: 5 / 147 grid points flip winners.

Rank-1 projector W33 measurement:
- 7 / 51 grid points flip winners.

Key artifacts:
- `data/_toe/flux_toggle_node0_20260110/README_flux_toggle_node0.md`
- `data/_toe/true_projector_w33_20260110/README_true_projector_flux_test.md`

## 5b) Native C24 projectors (measurement in the clock fiber)
Native C24 projectors are built by lifting canonical W33 rays into the 24-state clock fiber:
  r_tilde = r âŠ— u
where u is a parity-minus eigenvector under z -> z+3. This creates a measurement layer that
lives directly in the clock space, so gauge and measurement share the same fiber.

Key artifacts:
- `data/_toe/native_w33_projectors_c24_20260110/checkpoint_native_C24_projectors_20260110.json`
- `data/_toe/native_w33_projectors_c24_20260110/native_C24_projector_stabilities_flux_vs_noflux_keypoints.csv`
- `data/_toe/native_w33_projectors_c24_20260110/native_C24_projector_winners_keypoints.csv`

## 5c) Native C24 full-grid scan
The native C24 projector model was scanned across the full 51-point (lambda, mu) grid. In this
embedding, the flux vs no-flux winner differs at every grid point (51/51), and the flux-sensitive
lines are dominated by {8, 3, 14, 36, 7, ...}.
In the winner signature, no-flux winners sit entirely in the low Q12-variance class, while
flux winners split between low and mid classes.

Key artifacts:
- `data/_toe/native_fullgrid_20260110/README.md`
- `data/_toe/native_fullgrid_20260110/nativeC24_fullgrid_winners_flux_vs_noflux.csv`
- `data/_toe/native_fullgrid_20260110/nativeC24_line_flux_response_ranking_summary.csv`
- `data/_workbench/04_measurement/native_C24_fullgrid_summary.md`
- `data/_workbench/04_measurement/native_C24_winner_signature.md`

## 6) Flux sensitivity ranking and response law
Across the lambda/mu grid, the most flux-sensitive lines are identified, and a response law
regresses stability shifts on defect mass and central coherence.

Key artifacts:
- `data/_toe/flux_response_rankings_20260110/report.md`
- `data/_toe/flux_response_law_20260110/README_flux_response_law.md`

## 7) Geometry-only reductions and predictors
Independent of dynamics, a Z2 cocycle is computed on orbit-0 edges, and quartet features
are linked to flux response coefficients. A geometry-only predictor using a sector-parity
operator (Q12) shows that the most flux-sensitive bases cluster in a low-variance class.

Key artifacts:
- `data/_toe/geometric_reduction_20260110/README.md`
- `data/_toe/harmonic_lift_geometry_predictor_20260110/REPORT.md`

## 7b) Domain-wall mincut and W33 sensors
A pure graph invariant is computed by forcing the four defect edges to cross a cut and
minimizing non-defect spillover. The optimal cost is 6, and the spillover is anchored
near node 20. On the measurement side, the same Q12 variance statistic concentrates
the most flux-sensitive lines in the low-variance class.

Key artifacts:
- `data/_toe/domainwall_to_w33_sensors_20260110/REPORT.md`
- `data/_toe/domainwall_to_w33_sensors_20260110/summary.json`
- `data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv`

## 8) Where to go next
The dataset already encodes a chain:
  tomotope -> Z3 hyperplane -> PG(3,2) shadow -> symmetry closure -> 2T transport -> Z2 flux -> W33 response.
Next steps could include a single reproducible pipeline, or a narrative paper draft that formalizes
the coupling and the measurement models.


