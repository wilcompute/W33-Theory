# Part CCCCCXCVII — Tomotope Six-Kernel Vertex Lift

Part CCCCCXCVI identified the six-slot action with the tetrahedral edge action of `S4`. This part makes the lift explicit at generator level.

---

## 1. Input

Use the bridge payload:

```text
data/tomotope_six_kernel_s4_edge_bridge.json
```

with conjugator `pi` satisfying:

```text
pi * G_tomotope * pi^{-1} = G_tetra_edges.
```

---

## 2. Generator lifting

For each tomotope slot generator `g`:

```text
g_tetra = pi * g * pi^{-1}.
```

Then match `g_tetra` against the standard edge-action table induced by all vertex permutations in `S4` on tetrahedron vertices `{0,1,2,3}`.

Each matched vertex permutation is an explicit lift:

```text
g_tetra = edge_action(v_g),  v_g in S4.
```

---

## 3. Certificate

The lift is certified by two exact checks:

1. every `p0..p3` slot generator admits a vertex lift,
2. the lifted vertex generators generate a group of order `24`.

So the tomotope six-kernel dynamics are not only edge-conjugate to `S4`, but carried explicitly by vertex-level `S4` generators.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_six_kernel_vertex_lift.py
```

Output:

```text
data/tomotope_six_kernel_vertex_lift.json
```

containing conjugated edge generators, explicit vertex lifts, and summary invariants.
