# Part DCXX — Tomotope/Toroidal Bi-Scale Automaton Bridge

This part fuses linear and quadratic horizon systems into one deterministic regime automaton.

---

## 1. Input horizons

Linear directional horizons:

```text
(8,14).
```

Quadratic energy horizons:

```text
(4,7).
```

---

## 2. Joint-state dynamics

Define joint state at time `t`:

```text
(L_regime(t), E_regime(t)).
```

The observed distinct joint states are exactly:

```text
L_pre|E_pre
L_pre|E_mid
L_pre|E_full
L_mid|E_full
L_full|E_full
```

So the combined system is a 5-state deterministic cascade.

---

## 3. Cascade ordering

Energy reaches full resolution first:

```text
t=7.
```

Linear reaches full resolution later:

```text
t=14.
```

Hence the two-scale chain has a strict ordering of terminal transitions.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_biscale_automaton_bridge.py
```

Output:

```text
data/tomotope_toroidal_biscale_automaton_bridge.json
```

with full timeline, joint-state order, and identity checks.
