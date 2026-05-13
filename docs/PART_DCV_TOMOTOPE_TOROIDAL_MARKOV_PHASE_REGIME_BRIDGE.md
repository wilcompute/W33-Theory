# Part DCV — Tomotope/Toroidal Markov Phase-Regime Bridge

Part DCIV established two horizons (`t=4` and `t=7`). This part turns them into an explicit finite-time regime table.

---

## 1. Residual observables

At step `t` define:

```text
P_t = rho^t,
A_t = 7 * rho^t.
```

Thresholds:

```text
A_t <= 1      (active-packet-count resolved),
P_t <= 1/24   (packet-probability resolved).
```

---

## 2. Three discrete regimes

With `t_active=4`, `t_prob=7`:

1. `t < 4`: pre-count-resolution,
1. `4 <= t < 7`: count-resolved / probability-unresolved,
1. `t >= 7`: full packet-resolution.

So there is a strict 3-step intermediate regime:

```text
t = 4,5,6.
```

---

## 3. Why this matters

The bridge now has a finite dynamical stratification, not only endpoint thresholds:

- early phase: both residuals above threshold,
- middle phase: packet counts already suppressed below one while probability residue is still above `1/24`,
- late phase: both suppressed.

This makes the toroidal/tomotope decay story operational in discrete time.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_markov_phase_regime_bridge.py
```

Output:

```text
data/tomotope_toroidal_markov_phase_regime_bridge.json
```

with full step table, regime labels, and cross-checked horizon-gap identities.
