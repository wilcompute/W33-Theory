# TOE Flux Toggle: Projector Reconstruction + Node0 Sensitivity (2026-01-10)

## What we reconstructed (from legacy reconstruction scripts)
The W(3,3) line measurement used in `apply_W33_measurements_to_time_evolution_20260109T210928Z.py` is **purely mask-based**:

- Let `psi(t)` be the 59×24 amplitude matrix reshaped from the 1416-vector.
- Define the clock marginal:
  - **global:** `clock_mass[k] = sum_node |psi[node,k]|^2`
  - **node-local:** `clock_mass_node0[k] = |psi[node0,k]|^2`
- Each W33 rainbow line `L` has a 0/1 mask vector `mask_L[k]` with exactly 8 ones.
- The line “probability” is:
  - `prob_L = sum_k mask_L[k] * clock_mass[k]`
  - and the recorded **density** is `density_L = prob_L / 8`.

No additional phase tables are used here; it is linear in `|psi|^2`.

## Transport/flux toggle
We toggled **only** the 4 delta4 defect edges by replacing their transport element:
- `e*  -> e`

This removes the **central Z2 holonomy** while keeping the rest of the connection unchanged.

## What happens to switchpoints (winner among lines 22/8/17)
We computed stabilities as:
- `stability_density = mean(density(t))/std(density(t))` with **sample std (ddof=1)**
- time grid: `t = 0,0.25,...,2.0` (9 points)
- seed: node0, clock_state 0

### Global clock marginal (summing over all nodes)
- Switchpoints are **identical** with vs without flux (winner schedule unchanged).
- Flux does shift the **stability values** slightly upward (mean Δ ≈ 0.000825) but does not flip winners.

### Node0-local clock marginal (using only node0 amplitudes)
- Flux **does** change winners on **5 / 147** grid points.
- Specifically, at μ=0.75 and λ in [0.40,0.43], flux makes line 22 win while no-flux makes line 8 win.
- At μ=1.00 and λ=0.47, flux makes line 22 win while no-flux makes line 17 win.
- The derived switchpoints differ accordingly (see CSVs).
