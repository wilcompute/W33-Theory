# Part CCCCCXCVI — Tomotope Six-Kernel S4 Edge Bridge

Part CCCCCXCV produced an induced action of the published tomotope generators on six kernel slots. This part identifies that action structurally.

---

## 1. Starting point

From

```text
data/tomotope_six_kernel_generator_alignment.json
```

we have four slot generators in `S6` (from `p0..p3`) acting on:

```text
{k1,k2,k3,k4,k5,k6}.
```

---

## 2. Generated subgroup profile

Taking closure under composition gives a finite subgroup of `S6` with:

```text
order = 24,
transitive slot action,
cycle-type distribution:
  1 element of type 1-1-1-1-1-1,
  9 elements of type 2-2-1-1,
  8 elements of type 3-3,
  6 elements of type 4-2.
```

This is the exact fingerprint of the tetrahedral edge action of `S4`.

---

## 3. Tetrahedral model comparison

Build the standard action of `S4` on tetrahedron vertices `{0,1,2,3}` and induce it to the six edges:

```text
(01),(02),(03),(12),(13),(23).
```

This yields a 24-element subgroup of `S6`.

A direct conjugacy search in `S6` finds a permutation `pi` such that:

```text
pi * G_tomotope * pi^{-1} = G_tetra_edges.
```

So the tomotope six-slot action is conjugate to the canonical `S4`-on-edges representation.

---

## 4. Bivector dictionary closure

With the edge order above, use the canonical slot dictionary:

```text
k1 -> B01,
k2 -> B02,
k3 -> B03,
k4 -> B12,
k5 -> B13,
k6 -> B23.
```

Thus the six-slot kernel from CCCCCXCIV/CCCCCXCV is now dynamically identified with the tetrahedral bivector edge packet, not just counted as six labels.

---

## 5. Executable artifact

Script:

```text
scripts/tomotope_six_kernel_s4_edge_bridge.py
```

Output:

```text
data/tomotope_six_kernel_s4_edge_bridge.json
```

containing summary invariants, cycle distribution, conjugator, and the bivector-slot dictionary.
