# Part DCX — Tomotope/Toroidal Directional Phase Bridge

Part DCIX fixed the directional split (`21+21`), and Part DCV fixed aggregate time regimes. This part combines them into directional time evolution.

---

## 1. Directional residuals

At time `t`:

```text
F_t = 21 * rho^t,
B_t = 21 * rho^t,
O_t = F_t + B_t = 42 * rho^t.
```

So forward and backward are exactly equal at every step.

---

## 2. Directional thresholds

Per direction:

1. half-resolution threshold:

```text
F_t <= 1/2.
```

1. packet-resolution threshold:

```text
F_t <= 1/48.
```

Minimal horizons:

```text
t_half_direction = 8,
t_packet_direction = 14.
```

---

## 3. Directional phase regimes

This gives three directional regimes:

- `t < 4`: direction pre-half-resolution,
- `4 <= t < 7`: half-resolved / packet-unresolved,
- `t >= 7`: full packet-resolution.

So the directional model has a 6-step intermediate window (`t=8..13`) for linear directional residuals.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_directional_phase_bridge.py
```

Output:

```text
data/tomotope_toroidal_directional_phase_bridge.json
```

with full table, regime labels, and cross-checks against DCIX/DCV horizons.
