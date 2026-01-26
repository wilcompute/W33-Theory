# Harmonic lift and geometry-only flux-sensor predictor (2026-01-10)

## Harmonic lift of the Z2 defect cocycle on orbit-0

We treat the orbit-0 defect cocycle as a Z2-valued 1-cochain:
- c(e)=1 iff delta_sum_mod8(e)=4 (four defect edges)
- c(e)=0 otherwise

### (A) Continuous least-squares lift (angle potential)
Solve min ||B·theta - b||^2 with b=pi on defect edges and 0 otherwise, gauge-fixed by theta[0]=0.

Outputs:
- `orbit0_harmonic_lift_theta_and_mincut_labels.csv` (columns `theta_ls`, `theta_mod_2pi`)

### (B) Best ±1 lift under hard defect constraints (minimum cut)
Enforce defect edges to cross the cut (XOR=1 on each delta4 edge) and minimize the number of nondefect edges crossing.

Result:
- Minimum number of nondefect edges that must cross = **6**
- The six forced nondefect cut edges are saved in `orbit0_min_cut_nondef_edges.csv`

This gives a concrete “domain wall” picture: the Z2 flux cannot be realized as a pure cut without paying 6 extra crossings elsewhere.

## Geometry-only predictor for W(3,3) flux sensitivity

Using the canonical W(3,3) ray solution (40 rays in C^4), define the sector-parity operator:
- Q12 = diag(1, -1, -1, 1)

For each W33 basis (line), compute:
- Var_Q12(line) = variance over the 4 basis rays of <v|Q12|v>

Observation:
- Var_Q12 takes only three values across the 40 lines: 1/9 (27 lines), 1/3 (12 lines), 1 (1 line).
- The most flux-sensitive bases (by measured mean_abs_delta) lie overwhelmingly in the **low variance** class Var_Q12=1/9.

This is a “pure measurement-geometry” discriminator: the flux sensors live in the class of bases that do *not* sharply diagonalize Q12.

Files:
- `geometry_predictor_vs_observed_flux_sensitivity.csv`
- `Q12_variance_groups_vs_observed_stats.csv`
