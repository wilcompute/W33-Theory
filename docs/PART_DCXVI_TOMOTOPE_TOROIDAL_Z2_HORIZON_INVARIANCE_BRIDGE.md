# Part DCXVI — Tomotope/Toroidal $\mathbb{Z}_2$ Horizon-Invariance Bridge

This part proves that the swap involution preserves directional damping horizons.

---

## 1. Swap-invariant directional horizons

Because forward and backward counts are both `21`, their threshold horizons coincide:

```text
t_half(forward)   = t_half(backward)   = 8,
t_packet(forward) = t_packet(backward) = 14.
```

So horizon data is invariant under the DCXIII swap.

---

## 2. Compatibility with linear/quadratic duality

From DCXI energy horizons:

```text
energy half horizon   = 4,
energy packet horizon = 7.
```

Duality remains valid under swap invariance:

```text
8 = 2*4,
14 = 2*7.
```

---

## 3. Executable artifact

Script:

```text
scripts/tomotope_toroidal_z2_horizon_invariance_bridge.py
```

Output:

```text
data/tomotope_toroidal_z2_horizon_invariance_bridge.json
```

with swap-invariance checks and duality-preservation checks.
