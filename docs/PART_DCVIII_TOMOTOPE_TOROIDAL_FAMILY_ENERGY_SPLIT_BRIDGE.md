# Part DCVIII — Tomotope/Toroidal Family Energy-Split Bridge

Part DCVII fixed the exact edge-shell identity:

```text
42 = 21 + 21.
```

Part DCVI defined quadratic oriented energy:

```text
E_t = 42 * rho^(2t).
```

This part combines them into an exact family split.

---

## 1. Equal family energy shares

Define:

```text
E_C(t) = 21 * rho^(2t),
E_S(t) = 21 * rho^(2t).
```

Then:

```text
E_t = E_C(t) + E_S(t),
E_C(t) = E_S(t) = E_t/2.
```

So Csaszar and Szilassi carry equal quadratic residual at every step.

---

## 2. Family-level horizons

Use thresholds on one family shell:

1. half-channel family threshold:

```text
E_family <= 1/2.
```

1. packet family threshold:

```text
E_family <= 1/48.
```

Minimal horizons from the executable bridge:

```text
t_half_family   = 4,
t_packet_family = 7.
```

---

## 3. Interpretation

The same `4/7` split survives after dual-family decomposition:

- by `t=4`, each family drops below half-channel energy;
- by `t=7`, each family drops below packet-probability energy scale.

So the damping structure is not an artifact of aggregation; it is stable per family.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_family_energy_split_bridge.py
```

Output:

```text
data/tomotope_toroidal_family_energy_split_bridge.json
```

with exact split identities, per-family horizons, and minimality checks.
