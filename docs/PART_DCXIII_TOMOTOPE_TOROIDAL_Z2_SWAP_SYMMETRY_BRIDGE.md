# Part DCXIII — Tomotope/Toroidal $\mathbb{Z}_2$ Swap-Symmetry Bridge

This part formalizes the `21+21` split as an explicit order-2 symmetry.

---

## 1. Involution definition

Define swap involutions:

```text
sigma_dir: forward <-> backward,
sigma_fam: csaszar <-> szilassi.
```

Each satisfies:

```text
sigma^2 = id.
```

---

## 2. Invariants under swap

Directional pair:

```text
forward + backward = 21 + 21 = 42.
```

Family pair:

```text
csaszar + szilassi = 21 + 21 = 42.
```

Both sums are fixed by the corresponding swap action.

---

## 3. Weighted closure invariance

With stabilizer factor `4`:

```text
42 * 4 = 168.
```

So weighted active closure is also swap-invariant.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_z2_swap_symmetry_bridge.py
```

Output:

```text
data/tomotope_toroidal_z2_swap_symmetry_bridge.json
```

with explicit involution actions, order-2 checks, and invariant certificates.
