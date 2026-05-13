# Part DCVI — Tomotope/Toroidal Markov Energy Bridge

Part DCV tracked linear residual amplitudes. This part tracks quadratic oriented-channel energy.

---

## 1. Energy proxy

Define:

```text
E_t = 42 * rho^(2t),
```

where `42` is the oriented transport count and `rho` is the nontrivial spectral radius.

---

## 2. Two energy thresholds

1. One-channel energy threshold:

```text
E_t <= 1.
```

1. Packet-probability energy threshold:

```text
E_t <= 1/24.
```

Minimal horizons from the executable certificate:

```text
t_one_channel = 4,
t_packet_energy = 7.
```

---

## 3. Interpretation

At quadratic mode level the same split persists:

- by `t=4`, residual oriented energy is below one channel;
- by `t=7`, residual oriented energy is below packet-probability scale.

So the count/probability bifurcation is stable under squaring (energy view).

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_markov_energy_bridge.py
```

Output:

```text
data/tomotope_toroidal_markov_energy_bridge.json
```

with thresholds, horizons, minimality checks, and derived energy values.
