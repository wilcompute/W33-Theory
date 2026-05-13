# Part DCXI — Tomotope/Toroidal Horizon Duality Bridge

Part DCX (linear directional residuals) and Part DCVI (quadratic energy residuals) produce matching threshold families at different powers of `rho`.

---

## 1. Two decay scales

Linear directional scale:

```text
F_t ~ rho^t.
```

Quadratic energy scale:

```text
E_t ~ rho^(2t).
```

---

## 2. Exact horizon correspondences

Observed minimal horizons:

```text
linear half threshold:    t = 8,
energy one-channel:       t = 4,
linear packet threshold:  t = 14,
energy packet threshold:  t = 7.
```

So:

```text
8 = 2*4,
14 = 2*7.
```

Hence the exact duality law:

```text
t_linear = 2 * t_quadratic
```

for matched threshold families.

---

## 3. Interpretation

Switching from linear residual amplitude to quadratic transport energy halves the minimal discrete damping horizon while preserving the same structural threshold semantics.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_horizon_duality_bridge.py
```

Output:

```text
data/tomotope_toroidal_horizon_duality_bridge.json
```

with exact horizon values, factor checks, and duality identity checks.
