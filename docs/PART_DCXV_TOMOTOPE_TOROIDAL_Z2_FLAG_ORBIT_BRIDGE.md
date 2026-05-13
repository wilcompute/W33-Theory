# Part DCXV — Tomotope/Toroidal $\mathbb{Z}_2$ Flag-Orbit Bridge

This part identifies the DCXIV weighted quotient (`84`) with a single toroidal polyhedron flag shell.

---

## 1. Quotient value

From DCXIV:

```text
168 --(Z2 quotient)--> 84.
```

---

## 2. Flag-shell match

From the dual packet bridge:

```text
Csaszar flags = 84,
Szilassi flags = 84,
dual total = 168.
```

Hence the quotient `84` matches each individual flag shell exactly.

---

## 3. Executable artifact

Script:

```text
scripts/tomotope_toroidal_z2_flag_orbit_bridge.py
```

Output:

```text
data/tomotope_toroidal_z2_flag_orbit_bridge.json
```

with equality checks between quotient count and per-family flag shells.
