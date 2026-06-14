# BT1033 — R3's leading physical action converges geometrically, term by term

**Status: breakthrough framing. The Einstein–Hilbert + Standard-Model
Lagrangian converges on the fat tower with no spectral asymptotic interchange;
only a higher-derivative Weyl² correction remains.** Script
`analysis/bt1033_spectral_action_term_by_term_geometric.py`, data
`data/bt1033_spectral_action_term_by_term_geometric.json`.

## The idea

BT1032 isolated the one genuinely-hard piece of the spectral route: extracting
the *asymptotic* Seeley–DeWitt coefficients requires the `n↔Λ` limit
interchange. But there is a structural fact that dissolves this for the
*physical* terms:

> **Every Seeley–DeWitt coefficient `a₂ₙ` is an integral of a local
> curvature/connection invariant** (Gilkey; confirmed in the spectral-action
> literature). And on a *shape-regular* (edgewise) tower, each such curvature
> integral has a **geometric realization that converges as a single `mesh→0`
> limit** — no cutoff limit, hence no interchange.

So one routes *each term of the spectral action* through its geometric
quantity, not through the heat-trace asymptotics. The EH term (a₂ = ∫R = Regge
deficit) is the instance BT986 already verified.

## The term-by-term map (with W(3,3)'s exact coefficients)

W(3,3) finite moments: `Tr_F(1)=dim H_F=440`, `Tr_F(D_F²)=1920`,
`Tr_F(D_F⁴)=16320`.

| spectral-action term | physical | W(3,3) coeff | geometric realization | converges via | status |
| --- | --- | --- | --- | --- | --- |
| Λ⁴ | cosmological constant | 440 | vol (R₀) | CMS intrinsic volume | converges |
| Λ² | **Einstein–Hilbert** (Newton G) | 440 | ∫R = Regge deficit (R₂) | **Cheeger–Müller–Schrader** | **verified (BT986)** |
| Λ² | Higgs mass | 1920 | ∫√g | CMS R₀ × moment | converges |
| Λ⁰ | **Yang–Mills** kinetic | 1920 | ∫F² | Wilson/plaquette → F² (classical) | converges |
| Λ⁰ | Higgs kinetic | 1920 | ∫\|Dφ\|² | FEEC/Whitney gradient | converges |
| Λ⁰ | Higgs potential | 16320 | V(φ) | exact finite moment | exact |
| Λ⁰ | Gauss–Bonnet (topological) | 440 | χ = ∫Pfaffian | discrete Gauss–Bonnet–Chern | **exact (χ)** |
| Λ⁰ | Weyl² (conformal, higher-deriv.) | 440 | ∫C² | *not* a Lipschitz–Killing curvature | **OPEN** |

## What this establishes (honest)

- The **entire leading physical action** — cosmological constant, **Einstein–
  Hilbert gravity**, **Yang–Mills**, **Higgs**, and the topological Gauss–
  Bonnet term — converges **term by term** on the shape-regular edgewise tower,
  each as a single `mesh→0` geometric limit. The `n↔Λ` interchange of BT1032 is
  **not needed for any physical term.**
- This is the **classical action functional** (the spectral action is one); the
  quantum field theories built on it (e.g. Yang–Mills existence) are separate,
  harder, and not part of R3 (which is the *derivation of the action*).
- The W(3,3) finite factor contributes only the exact moments
  `{440, 1920, 16320}` as the term coefficients — no limit on the F-side.

## The one residual

Only the **higher-derivative Weyl² (conformal gravity)** term `∫C²` sits in the
spectral basket: `∫C²` is not a Lipschitz–Killing curvature, so CMS does not
deliver it, and its discrete convergence is subtle (the Weyl tensor of a
piecewise-flat space concentrates on codimension-2 and does not converge
pointwise). It is *not* part of the Einstein–Hilbert + Standard-Model
Lagrangian — it is a higher-derivative correction.

## Net effect on R3

R3's *physical content* — deriving the Einstein–Hilbert + Standard-Model action
as the `mesh→0` limit of the W(3,3) × (edgewise 4-seed) spectral action — is now
reduced to **established geometric convergence theorems applied term by term**
(CMS for the curvature integrals, classical lattice gauge for ∫F², FEEC for the
Higgs gradient, exact moments for the F-couplings), with the Einstein–Hilbert
instance verified (BT986). The remaining genuinely-open piece is the
higher-derivative Weyl² coefficient — a real but physically-subleading residual.

## Sources

- Gilkey, *Invariance Theory, the Heat Equation, and the Atiyah–Singer Index
  Theorem* — Seeley–DeWitt coefficients as local curvature integrals.
- Cheeger–Müller–Schrader, CMP 92 (1984) 405 — Lipschitz–Killing curvature
  convergence on fat triangulations.
- Chamseddine–Connes, *The Spectral Action Principle*, CMP 186 (1997) 731 —
  the `a₄` (Weyl² + GB + YM + Higgs) term structure.
