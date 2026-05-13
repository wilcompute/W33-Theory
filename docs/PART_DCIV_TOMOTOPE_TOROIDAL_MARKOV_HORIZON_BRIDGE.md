# Part DCIV — Tomotope/Toroidal Markov Horizon Bridge

Part DCIII gave one damping horizon from the packet-resolution threshold `1/24`. This part separates two physically distinct finite horizons.

---

## 1. Two thresholds

Let `rho` be the nontrivial spectral radius.

Define:

1. **Probability-packet threshold**

```text
rho^t <= 1/24.
```

1. **Active-packet-count threshold** (7 active packets)

```text
7 * rho^t <= 1
   <=> rho^t <= 1/7.
```

---

## 2. Minimal horizons

The executable minimal integer horizons are:

```text
t_prob   = 7,
t_active = 4.
```

So one-active-packet-count damping occurs earlier than one-packet-probability damping:

```text
t_active <= t_prob.
```

---

## 3. Interpretation

- `t=4`: the residual active-mode packet count drops below one packet.
- `t=7`: residual mode amplitude drops below the `1/24` packet-probability resolution scale.

This cleanly separates count-level and probability-level damping horizons in the same finite chain.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_markov_horizon_bridge.py
```

Output:

```text
data/tomotope_toroidal_markov_horizon_bridge.json
```

with both thresholds, minimality checks, and derived bound values.
