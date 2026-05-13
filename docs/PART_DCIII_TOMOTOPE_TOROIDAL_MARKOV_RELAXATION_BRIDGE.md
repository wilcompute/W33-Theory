# Part DCIII — Tomotope/Toroidal Markov Relaxation Bridge

Part DCII gave the closed-form nontrivial mode packet. This part extracts its decay scale.

---

## 1. Nontrivial spectral radius

For

```text
lambda_k = 1/8 + (3/4) cos(2*pi*k/7),  k=1..6,
```

define

```text
rho = max_k |lambda_k|,
gamma = 1 - rho.
```

`gamma` is the active-sector relaxation gap.

---

## 2. Packet-resolution damping horizon

Use the packet-resolution threshold:

```text
epsilon_packet = 1/24.
```

Define `t*` as the smallest integer with:

```text
rho^t* <= 1/24.
```

This gives a finite damping horizon for nontrivial active transport remnants at packet resolution.

---

## 3. Why this matters for the bridge chain

Earlier parts locked counts and moments:

```text
21/16 -> 21 -> 42 -> 168.
```

This part adds kinetics: how quickly nontrivial active transport decays beneath one-packet granularity.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_markov_relaxation_bridge.py
```

Output:

```text
data/tomotope_toroidal_markov_relaxation_bridge.json
```

with `rho`, `gamma`, `t*`, and identity checks.
