# TOE geometric reduction artifacts (2026-01-10)

This folder contains **geometry-only** invariants of the N12_58 orbit-0 flipgraph plus a **coupling analysis** that links
W(3,3) line flux sensitivity back to (a) projective quartet structure and (b) the Z2 defect cocycle.

## Files

### Z2 cocycle + node potential
- orbit0_edges_Z2_cocycle.csv
  - Edge list with `is_defect` (delta_sum_mod8==4). This is the Z2-valued 1-cocycle c(e).

- orbit0_node_parity_potential_bfs.csv
  - A BFS tree-based Z2 'potential' p(v) with p(root)=0 and p(child)=p(parent) XOR c(tree_edge).
  - This gauges the cocycle into a set of chord residuals.

- orbit0_chords_cycle_parity_basis.csv
  - For each chord edge (non-tree edge) the fundamental cycle parity is `cycle_parity_odd = c(chord) XOR p(u) XOR p(v)`.
  - The count of `cycle_parity_odd==1` chords equals the number of odd-parity fundamental cycles under this gauge.

### Quartet → flux sensitivity reduction
- lines_with_quartet_features_and_response_coeffs.csv
  - Joins W33 line quartets to the previously fit flux-response coefficients (coef_delta_coh, etc.).

- quartet_feature_correlations.csv
  - Correlations between simple quartet features and response coefficients.

- ridge_importances_mean_abs_delta.csv
  - A small ridge model identifying which quartet features predict mean_abs_delta best (R^2≈0.34).

### Concrete traversal statistics (illustrative points)
- example_points_time_series_currents_and_coherence.csv
  - For a few (lambda,mu) points, records:
    - central coherence |Σ conj(psi[z])*psi[z+3]|
    - absolute defect-edge probability current (standard CTQW current formula)
    - defect mass
    - for both flux and no-flux models

- example_points_aggregates_currents_coherence.csv
  - Mean-over-time aggregates for the same points.

## Interpretation (short)
- The delta4 edges define a Z2 cocycle c(e). The BFS potential p(v) shows how that cocycle injects odd parity into specific chord cycles.
- Flux sensitivity of W33 bases correlates most strongly with phase-equality patterns across sectors (especially m1==m2) and the presence of sec0_m1/sec0_m2.
- At the dynamical level, removing the central e* flux increases the measured central-pair coherence, consistent with e* acting as a dephasing/twisting element under transport.
