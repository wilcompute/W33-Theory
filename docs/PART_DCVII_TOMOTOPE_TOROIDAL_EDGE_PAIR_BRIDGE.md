# Part DCVII — Tomotope/Toroidal Edge-Pair Bridge

This part formalizes the identity highlighted in review:

```text
oriented transport count = 42 = 21 + 21 = Csaszar edges + Szilassi edges.
```

---

## 1. Dual-edge shells

- Csaszar edge shell: `21`
- Szilassi edge shell: `21`

Combined dual-edge shell:

```text
21 + 21 = 42.
```

---

## 2. Transport equivalence

From the transport bridge:

```text
unoriented transports = 21,
oriented transports   = 42.
```

So:

```text
unoriented transports = each single-edge shell,
oriented transports   = combined dual-edge shell.
```

---

## 3. Weighted closure

With slot stabilizer `4`:

```text
42 * 4 = 168,
```

matching the active tomotope packet weight.

So the chain is now explicit:

```text
21 (single edge shell)
 -> 42 (dual-edge/oriented transport shell)
 -> 168 (stabilizer-weighted active packet shell).
```

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_edge_pair_bridge.py
```

Output:

```text
data/tomotope_toroidal_edge_pair_bridge.json
```

with exact identity checks and weighted closure checks.
