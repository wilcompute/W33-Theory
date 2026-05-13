# Part DC — Tomotope/Toroidal Markov Ground Bridge

This part turns the `7+1` packet split into a finite transport dynamics statement.

---

## 1. State space

Use eight states:

```text
C1, C2, C3, C4, C5, S1, S2, G
```

where `G` is the ground packet state.

---

## 2. Exact transition law

For each active state (`Ci` or `Sj`):

```text
self:   1/8,
next:   3/8,
prev:   3/8,
ground: 1/8.
```

For the ground state `G`:

```text
stay in G: 1/8,
to each active state: 1/8.
```

All rows sum to `1` exactly.

---

## 3. Stationary law and packet weights

The stationary distribution is uniform on 8 states:

```text
pi(state) = 1/8.
```

Hence aggregate masses are:

```text
active mass = 7/8,
ground mass = 1/8.
```

Applying total tomotope packet weight `192` gives:

```text
active weight = (7/8)*192 = 168,
ground weight = (1/8)*192 = 24.
```

So the bridge recovers the exact `168/24` split as a stationary transport law.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_markov_ground_bridge.py
```

Output:

```text
data/tomotope_toroidal_markov_ground_bridge.json
```

with exact rational transition matrix, stationary distribution, and identity checks.
