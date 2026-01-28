# Standardization of Names, Counts, and Groups (Canonical)

This file defines the **canonical** terminology and numeric facts used in this
repository. Any document that conflicts with this file should be treated as
legacy or updated to match these standards.

---

## 1) Core Objects

**Geometry (canonical):**
- **W(3,3)** denotes the **symplectic generalized quadrangle** of order (3,3)
  inside the projective space **PG(3,3)**, constructed from a nondegenerate
  alternating (symplectic) form on **F\_3^4**.
- **Points:** 40 (all projective points are isotropic for a symplectic form).
- **Lines:** 40 totally isotropic lines.
- **Incidence:**
  - Each line contains **4 points**.
  - Each point lies on **4 lines**.

**Graph (canonical):**
- **W33** denotes the **point (collinearity) graph** of W(3,3).
- **SRG parameters:** **(v, k, λ, μ) = (40, 12, 2, 4)**.
- **Edges:** 240.
- **Spectrum:** 12^1, 2^24, (-4)^15.

**Naming rule:**
Use **W(3,3)** for the incidence geometry and **W33** for the point graph.

---

## 2) Symmetry Groups (Canonical)

**Full incidence symmetry:**
- **Aut\_inc(W(3,3)) ≅ Sp(4,3) ≅ W(E6)**
  **Order:** **51,840**.

**Point-graph symmetry:**
- **Aut\_pts(W33) ≅ PSp(4,3)**
  **Order:** **25,920** (index 2 in Sp(4,3), since ±I acts trivially on
  projective points).

**Legacy note:**
Any references to **155,520** or **PGU(3,3)** as *the* automorphism group of
W33/W(3,3) are **deprecated** in this repo. If such a number appears, it should
be treated as legacy or corrected to the canonical values above.

---

## 3) Witting / E8 Interface (Canonical)

- **240 E8 roots ↔ 240 Witting vertices** in C^4 (realified in R^8).
- **40 Witting rays ↔ 40 W(3,3) points** (6 vertices per ray).
- **W33 edges ↔ E8 roots** via the explicit Coxeter 6‑cycle construction
  (see `FINAL_TOE_PROOF.md`, `tools/sage_e8_order6_orbits.py`,
  `tools/sage_e8_root_edge_bijection.py`).

---

## 4) Quick Canonical Summary

```
W(3,3) (symplectic GQ, PG(3,3)) → 40 points, 40 lines, 4 points/line, 4 lines/point
W33 = point graph(W(3,3))       → SRG(40,12,2,4), 240 edges
Aut_inc(W(3,3))                → Sp(4,3) ≅ W(E6), order 51,840
Aut_pts(W33)                   → PSp(4,3), order 25,920
```
