# Domain-wall cost vs W(3,3) flux sensors (orbit-0)

## Domain-wall (pure graph invariant)

We solve: minimize number of **non-defect** edges cut subject to all four delta4 defect edges crossing.

- defect edges (forced to cross): [(0, 20), (10, 12), (26, 27), (27, 45)]
- optimal non-defect cut cost: **6**
- non-defect spillover cut edges (forced by topology): [(12, 15), (13, 27), (19, 20), (20, 38), (20, 40), (20, 44)]

A notable structural fact: **5/6** spillover edges are incident to node **20**, so the cocycle’s minimal domain wall is geometrically anchored near node 20.

## Measurement-side discriminator (pure W(3,3) geometry)

Define sector-parity operator on C^4:
Q12 = diag(+1,-1,-1,+1)  (i.e. + on sectors {0,3}, - on {1,2}).

For each W33 basis (line) with four orthonormal rays {v_i}:
- compute q_i = <v_i|Q12|v_i>
- compute Var_Q12(line) = Var(q_i)

Observed line flux sensitivity (mean_abs_delta) is higher when Var_Q12 is lower:

 var_q_r  count     mean   median      max
0.111111     27 0.007745 0.004551 0.028922
0.333333     12 0.005597 0.003161 0.015444
1.000000      1 0.001289 0.001289 0.001289

In particular, 8/10 of the empirically top-10 flux sensors lie in the **low Var_Q12=1/9** class.

## Interpretation (mechanism-level)

- Orbit-0 curvature is a Z2 cocycle supported on 4 defect edges (central element e*).
- Any gauge that forces those defects to be “the only cut” is impossible; the minimal cut must include **6** additional edges (spillover/domain-wall cost).
- The only measurement channel that directly couples to that Z2 parity in the canonical W(3,3) C^4 layer is the character (+ on sectors {0,3}, - on {1,2}), encoded by Q12.
- Bases with low Var_Q12 are “balanced” across this parity channel, hence maximally sensitive to small coherence changes induced by central holonomy.

Files:
- orbit0_mincut_labels.csv
- orbit0_mincut_spillover_edges_nondefect.csv
- W33_lines_flux_sensitivity_with_Q12_variance.csv
- predicted_top15_by_geometry_only.csv
