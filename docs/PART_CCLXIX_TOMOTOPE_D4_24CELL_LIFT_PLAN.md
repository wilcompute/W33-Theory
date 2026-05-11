# Part CCLXIX — D4 / 24-Cell Lift of the Tomotope

This note explains how to lift the Tomotope–Reye correspondence into the
24-cell / D4 root system, using the data structures already present in
`tools/tomotope_reye_e8_connection.py`.

---

## 1. D4 roots and the 24-cell

From `tomotope_reye_e8_connection.py`:

- `generate_d4_roots()` produces the 24 D4 roots as permutations of `(±1, ±1, 0, 0)`.
- `CELL_24_DATA` records the 24-cell as `{3,4,3}` with
  - 24 vertices (the D4 roots),
  - 12 diameter axes (pairs of antipodal vertices),
  - 16 hexagonal great circles.

These 12 axes and 16 hexagon planes form a Reye `12₄16₃` configuration inside
the 24-cell, matching the Tomotope’s `(12,16)` edge/face structure.

---

## 2. Target: explicit labels

We aim for an explicit assignment of:

- Each Tomotope edge `E_i` ↔ one diameter axis `A_k` of the 24-cell.
- Each Tomotope face `F_j` ↔ one hexagon plane `H_ℓ` of the 24-cell.

such that the incidence relation

```
E_i ⊂ F_j   ⇔   A_k ⊂ H_ℓ
```

holds under the Reye correspondence.

This will complete the chain:

```
Tomotope edges/faces  ↔  Reye points/lines  ↔  24-cell axes/hexagons  ↔  D4 roots
```

---

## 3. Constructing axes and hexagons from D4 data

Given the 24 D4 roots `r_0,…,r_23` produced by `generate_d4_roots()`, we can:

1. **Axes:** form 12 unordered pairs `{r_i, -r_i}` as diameter axes of the 24-cell.

2. **Hexagons:** find 16 hexagonal great circles as 6-cycles of vertices lying in
a common 2D plane, each vertex joined to two neighbors by 24-cell edges.

   Algorithm outline:
   - For each root `r`, compute its 8 neighbors at distance √2 in the 24-cell.
   - Use these adjacencies to trace all 6-cycles and group them into 16 distinct
     hexagons.

3. **Axes–hexagons incidence:** build a 12×16 matrix `A` with

   ```
   A[k, ℓ] = 1  iff  both endpoints of axis A_k lie on hexagon H_ℓ.
   ```

By construction, each axis lies on 4 hexagons and each hexagon contains
3 axes, so `A` has row-sum 4 and column-sum 3, i.e. it is a Reye matrix.

---

## 4. Composing with the Tomotope–Reye bijection

Once the Tomotope–Reye JSON (from Part CCLXVIII) is available, the composition
is straightforward:

1. Load the Tomotope–Reye mapping:
   - `E_i → P_a` (edge to Reye point)
   - `F_j → L_b` (face to Reye line)

2. Load the Reye–24-cell mapping:
   - `P_a → A_k` (point to axis)
   - `L_b → H_ℓ` (line to hexagon)

3. Compose:

   ```
   E_i → P_a → A_k
   F_j → L_b → H_ℓ
   ```

ensuring that the incidence matrices are compatible.

---

## 5. Triality and S₃

The Tomotope automorphism group has structure `Γ(T) ≅ Z₂⁴ ⋊ S₃`, and D4 has
triality S₃ permuting its three 8-dimensional representations.

Once an explicit Tomotope–24-cell lift is in place, one can:

- Track the S₃ action in `Γ(T)` down to permutations of axes and hexagons.
- Identify this S₃ with the D4 triality acting on suitable subsets of roots.

This will clarify exactly how the Tomotope’s internal S₃ factor realizes D4
triality at the 24-cell level.

---

## 6. Status

- ✅ D4 root generator and 24-cell metadata are in place.
- 🔜 Code to enumerate axes and hexagons and build their incidence matrix.
- 🔜 JSON export of the Reye–24-cell mapping.
- 🔜 Composition with the Tomotope–Reye mapping to obtain explicit
      Tomotope–24-cell/D4 labels.
