# Part DCIX — Tomotope/Toroidal Directional Split Bridge

This part makes the oriented transport shell split canonical by direction.

---

## 1. Directional decomposition on the 7-cycle

With step classes `d=1..6` (each carrying 7 transports):

- forward directions: `d in {1,2,3}`
- backward directions: `d in {4,5,6}`

Therefore:

```text
forward  = 3*7 = 21,
backward = 3*7 = 21,
total    = 42.
```

---

## 2. Match to dual-family shell

From the toroidal polyhedra side:

```text
Csaszar edges  = 21,
Szilassi edges = 21.
```

So the directional split matches the dual-family split numerically:

```text
forward/backward = 21/21 = Csaszar/Szilassi edge shell.
```

---

## 3. Weighted closure

With slot stabilizer `4`:

```text
(21 + 21) * 4 = 42 * 4 = 168.
```

So the directional shell closes to the same active packet weight as the family shell.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_directional_split_bridge.py
```

Output:

```text
data/tomotope_toroidal_directional_split_bridge.json
```

with directional counts, family-shell match checks, and weighted closure checks.
