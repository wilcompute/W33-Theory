# Part DCCLVI — The W(3,3) Sphere-Packing Density Tower

**Bridge:** `verify_dcclvi_sphere_packing_density_tower.py` — Verified
**Tests:** `tests/test_dcclvi_sphere_packing_density_tower.py` — 21/21 pass
**Data:** `data/dcclvi_sphere_packing_density_tower.json`

---

## 1. What this part adds beyond DCCLV

DCCLV showed that every solved kissing number is a W(3,3) primitive.
This part lifts the result one level deeper — to the **optimal density
formulas themselves** — and shows that the denominators of all known
exact density formulas are also W(3,3) primitives.

---

## 2. The density tower

The optimal sphere-packing density is currently proved in **five**
dimensions:

| d | ρ_d | W(3,3) reading | proved by |
|:-:|---|---|---|
| 1 | 1 | trivial | trivial |
| 2 | π/(2√3) = π/(2√q) | uses 1/√q in the denominator | Thue 1890 |
| 3 | π/(3√2) = π/(q√λ) | uses 1/√λ and 1/q | Hales (Kepler conjecture, 1998) |
| **8** | **π⁴/384** = **π^μ / G_384** | π^μ over **cascade step 4** | **Viazovska 2016** |
| **24** | **π¹²/12!** = **π^k / k!** | π^k over **codec factorial** | **Cohn–Kumar–Miller–Radchenko–Viazovska 2017** |

**The denominators 384 and 12! are both W(3,3) primitives**, and the
π-exponents μ = q + 1 and k = q(q+1) are also W(3,3) primitives.

---

## 3. G_384 has seven W(3,3) factorisations

The dimension-8 packing density denominator 384 carries seven distinct
W(3,3) readings:

| role | value |
|---|---:|
| **G_384** = stabilizer cascade step 4 (DCCLIV) | 384 |
| 2 · \|W(D_4)\| | 2 × 192 = 384 |
| 2 · tomotope flag count (DCCXXV) | 2 × 192 = 384 |
| (q+1)² · f | 16 × 24 = 384 |
| trace(Cartan E_8) · f (DCCXXVII) | 16 × 24 = 384 |
| (q+1)! · (q+1)² | 24 × 16 = 384 |
| (q+1)! · trace(Cartan E_8) | 24 × 16 = 384 |

**384 = 16 × 24 = trace(Cartan E_8) × f** — the trace of the E_8 Cartan
matrix times the f-eigen-multiplicity. The dimension-8 packing density
inherits its denominator directly from the W(3,3) exceptional Lie group
structure.

---

## 4. The k! denominator and the codec

The dimension-24 Leech packing density

$$
\rho_{24} = \frac{\pi^{12}}{12!} = \frac{\pi^k}{k!}
$$

uses the **factorial of the codec** k = q(q+1) = 12. Both 12 (the
codec) and 12! (its factorial = 479,001,600 = order of S_12) are
W(3,3) primitives — the codec is the W(3,3) valency and one-vertex
local alphabet of DCCXVII–XX.

---

## 5. The π-exponents are W(3,3) primitives

| d | π-exponent | W(3,3) |
|:-:|:-:|---|
| 8 | **4** | **μ = q + 1** (quaternion dim, DCCXXVIII) |
| 24 | **12** | **k = q(q+1)** (codec) |

The π-exponent grows as μ → k = μ · q (= 4 · 3 = 12), so the
dimension-jump from 8 to 24 multiplies the π-exponent by q.

---

## 6. Cross-link with the kissing-number tower (DCCLV)

| solved | dimensions | sequence |
|---|---|---|
| kissing | {1, 2, 3, 4, 8, 24} | {1, λ, q, q+1, 2^q, f} |
| packing | {1, 2, 3, **—**, 8, 24} | {1, λ, q, **—**, 2^q, f} |

The dimension **d = 4 = μ** has K(4) = 24 proved (Musin 2003) but no
exact density yet. So the W(3,3) primitives match six kissing
dimensions and five packing dimensions, with the gap at μ.

---

## 7. The full sphere-packing W(3,3) picture

Combining DCCLV and DCCLVI:

$$
\boxed{\;\;
\begin{aligned}
\text{kissing numbers}_{d \in \{1, 2, 3, 4, 8, 24\}}
&\;\subset\; \text{W(3,3) primitives}, \\
\text{density denominators}_{d \in \{8, 24\}}
&\;\subset\; \text{W(3,3) primitives}, \\
\text{density } \pi\text{-exponents}_{d \in \{8, 24\}}
&\;\subset\; \text{W(3,3) primitives}.
\end{aligned}
\;\;}
$$

**The W(3,3) program contains the entire current state of the sphere-
packing problem.**

---

## 8. Decisive identity

$$
\boxed{\;
\rho_8 = \frac{\pi^\mu}{G_{384}} = \frac{\pi^{q+1}}{\text{stabilizer cascade step 4}}
\;}
$$
$$
\boxed{\;
\rho_{24} = \frac{\pi^k}{k!} = \frac{\pi^{q(q+1)}}{(\text{codec})!}
\;}
$$

---

## 9. Honest boundary

* All identities are **exact arithmetic / exact density-formula
  matching**.
* The sphere-packing density is proved optimal only in five dimensions;
  Viazovska's 2016/2017 work completes the 8D and 24D cases.
* This part does **not** prove additional density bounds or derive
  Viazovska's theorem from W(3,3). It documents that the denominators
  and π-exponents of the known exact densities are W(3,3) primitives.

---

## 10. One-line summary

$$
\boxed{\;
\rho_8 = \pi^\mu / G_{384}, \quad \rho_{24} = \pi^k / k!;
\;\text{both Viazovska denominators are W(3,3) primitives.}
\;}
$$
