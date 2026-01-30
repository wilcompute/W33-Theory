# Pair-Phase Gauge Fits (mod 3)

We tested whether **gauge rephasing** of the 40 rays (phase shifts s_i in Z3)
allows the pairwise phase class `k mod 3` to be expressed by a low-degree
algebraic form in F3^4.

## Model
Let `k_ij` be the phase class (mod 3) for pair (i,j), and let s_i be a per-ray
phase shift (mod 3). We solve:

```
k_ij + s_i - s_j = f(x_i, x_j)   (mod 3)
```

Two choices of f were tested:
1) **Bilinear+linear** in (x_i, x_j)
2) **Full quadratic** polynomial in the 8 variables (x0..x3, y0..y3)

## Results
- **No gauge+bilinear solution** exists.
- **No gauge+quadratic solution** exists.

So even after optimal gauge rephasing, the pair-phase classes cannot be
captured by a low-degree polynomial in the F3^4 coordinates.

## Interpretation
The pairwise phases encode a **higher-order cocycle** that is not reducible to
simple algebraic invariants in the symplectic coordinate system, even up to
U(1) gauge freedom on the rays.

Script: `tools/witting_pair_phase_gauge_fit.py`
Output: `artifacts/witting_pair_phase_gauge_fit.json`
