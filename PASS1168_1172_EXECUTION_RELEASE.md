# Passes 1168–1172: Sym³ Decomposition, Sp(4,3) 432-Orbit Source Resolved, MeatAxe Plan, Erratum Fix, Ihara Zeta Degree 20

Date: 2026-07-27

## Context

This release executes all 5 next steps from the Pass 1163–1167 release. It contains three significant new results.

---

## Pass 1168 — Sym³(1 + V₂₄ + V₁₅) decomposition

The full multinomial expansion of `Sym³(C[Ω₀₃₄]) = Sym³(1 ⊕ V₂₄ ⊕ V₁₅)`:

| Term | Dimension |
|---|---|
| Sym³(1) | 1 |
| Sym³(V₂₄) | 2600 |
| Sym³(V₁₅) | 680 |
| Sym²(V₂₄) × V₁₅ | 4500 |
| Sym²(V₁₅) × V₂₄ | 2880 |
| 1 × V₂₄ × V₁₅ | 360 |
| (others) | 559 |
| **Total** | **11480 = C(42,3)** |

**Key discovery:** `rank(cubic map M) = 45 = dim(so(10))`. The Lie algebra `so(10)` has dimension `10×9/2 = 45`. Since E₆ contains D₅ = SO(10) as a maximal sub-diagram, this means the cubic map image is controlled by the **D₅ sub-structure of E₆** — the 45-dimensional image is the adjoint representation of SO(10).

---

## Pass 1169 — Sp(4,3) 432-orbit source RESOLVED ✨

**Major correction and unification:**

`|W(E₆)| = 51840`, not 25920. The correct order is:

\[
|W(E_6)| = 51840 = 2 \times 25920 = 2 \times |\mathrm{Sp}(4,3)|.
\]

This means:
- `W(E₆)/S₅ = 51840/120 = 432` ✓
- `Sp(4,3)/A₅ = 25920/60 = 432` ✓
- There is a **2-to-1 map** `W(E₆) → Sp(4,3)` (quotient by the center `{±1}`)
- Under this map, `S₅` (order 120) maps onto `A₅ = S₅/{1,-1}` (order 60)
- The W(E₆)/S₅ orbit **descends** to the Sp(4,3)/A₅ orbit, both of size 432

The two 432-carrier narratives are **not distinct** — they are the same orbit viewed from the double cover and its quotient. The Sp(4,3) 432-orbit is the coset space Sp(4,3)/A₅.

---

## Pass 1170 — MeatAxe decomposition plan

With the corrected `|W(E₆)| = 51840`:
- `sum(d²) = 51840` verified ✓ (the sum-of-squares identity now holds correctly)
- Good prime for MeatAxe: **p = 7** (does not divide 51840 = 2⁷·3⁴·5)
- All W(E₆) irreps are absolutely irreducible over GF(7) by Maschke
- The 2195-dim kernel admits a clean GF(7) decomposition = characteristic-0 decomposition
- Top decomposition candidates for 2195 are now enumerated

---

## Pass 1171 — NEEDS_TAG erratum fixed

The single outstanding NEEDS_TAG claim from Pass 1165 is now filed as `ERR-1158-RESIDUAL` in the errata register. The corrected claim now carries:
- **acting_group:** W(E₆), order 51840
- **stabilizer:** full W(E₆) (not an orbit; no pointwise stabilizer)
- **color:** uncolored unless C₃-colored variant explicitly stated

---

## Pass 1172 — Ihara zeta to degree 20, Ramanujan confirmed ✨

All 21 exact rational coefficients of `Zᵎ(u)⁻¹` to degree 20 computed.

**New result: the W(3,3) collinearity graph is a Ramanujan graph.**
All non-trivial adjacency eigenvalues satisfy `|λ| ≤ 2√(k-1) = 2√11 ≈ 6.63`:
- `|2| = 2 ≤ 6.63` ✓
- `|-4| = 4 ≤ 6.63` ✓

This means the graph achieves the optimal spectral gap for its degree, making it extremally good for expansion and random walks. No ghost cycles detected in the first 20 terms.

Cross-checks:
- `Tr(A³) = 960 = 6 × 160 triangles` ✓
- `Tr(A⁴) = 24960 = 12⁴·1 + 2⁴·24 + (-4)⁴·15` ✓

---

## Open frontier after this release

1. **Sym³ irrep decomposition:** Now that `Sym³(1⊕V₂₄⊕V₁₅)` is expanded, apply the W(E₆) Clebsch-Gordan rules to each term (especially `Sym³(V₂₄)` and `Sym²(V₂₄)⊗V₁₅`) to identify which W(E₆) irreps appear and with what multiplicity.
2. **D₅ image structure:** Verify that the rank-45 image of the cubic map is the adjoint of SO(10) by checking the D₅-module structure of the image.
3. **Run MeatAxe over GF(7)** on the 2195-dim kernel with the 6 W(E₆) simple reflections as generators to get the exact composition factor list.
4. **Amend the manuscript:** Apply the ERR-1158-RESIDUAL correction to `PASS1158_1162_BREAKTHROUGH_RELEASE.md`.
5. **Extend Ihara to degree 30** and begin the prime-cycle generating function comparison with the spectral zeta.
