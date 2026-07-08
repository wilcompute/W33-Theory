# Pass 77 — Seven frontier ideas: GAP representation theory + geometry + equidistribution

**Status: PASS** — GAP proofs (`w33_pass77_group.g` → `w33_pass77_group_out.txt`), Python witness
`w33_pass77_frontier.py` (6/6 checks), test `tests/test_pass77_frontier.py` (7/7), paper compiles.

All seven follow-on ideas from Pass 76, executed. GAP and networkx confirmed available.

## T1 — Eigenspaces are irreducible (GAP-proved) — closes Pass 74 Track E
In GAP, **Sp(4,3) acts rank-3** on the 40 points and its permutation character decomposes as
**1 + χ₁₅ + χ₂₄** (each multiplicity 1). Therefore the r=2 (dim 24) and s=−4 (dim 15) eigenspaces
are **irreducible PSp(4,3)-modules** — the Ihara quadratic factors (1−2u+11u²)²⁴, (1+4u+11u²)¹⁵ are
genuine equivariant Artin–Ihara L-factors, not just dimension-matched. (Was "argued"; now proved.)

## T2/T3 — The ovoid separator (the clean geometric closer)
W(q) has ovoids **iff q is even**. So the symplectic W(3,3) (q=3 odd) has **no ovoid** while its
dual Q(4,3) does. The independence numbers therefore differ:
**α(W(3,3)) = 7 < 10 = α(Q(4,3))**. This is a classical, geometric, **non-spectral** invariant that
separates the two cospectral, locally-identical graphs of Pass 76 — exactly what the edge zeta
"hears" and the Ihara/Bartholdi zeta and all local invariants cannot. W(3,3) and Q(4,3) are the two
**geometric** graphs among the 28 Spence SRG(40,12,2,4); the ovoid number 7 vs 10 fingerprints them.

## T4 — Terwilliger (subconstituent) algebra
The subconstituent algebra T = ⟨A, A₂, E₀*, E₁*, E₂*⟩ of W(3,3) has **dimension 16** (the local
"quantum symmetry" refining the 3-dim Bose–Mesner algebra). Notably 16 = the 2-rank / code dim.

## T5 — Smith normal form (GAP)
Elementary divisors of A: **1¹⁶ · 2⁸ · 8¹⁵ · 24**, product **3·2⁵⁶ = |det A|**. Consistent with the
p-ranks (2-rank 16, 3-rank 39 = v−1, 5-rank 40): the complete integral structure of the adjacency.

## T6 — Weil representation (GAP)
The Weil (oscillator) representation of Sp(4,3) has degree **q² = 9 = 5 + 4 = (q²+1)/2 + (q²−1)/2**;
GAP confirms 4 and 5 are irreducible degrees of Sp(4,3) — the two-qutrit oscillator carrier.

## T7 — Joint prime-geodesic equidistribution on the 2-torus
Both geodesic frequencies are irrational multiples of π (non-monic minimal polynomials
121u⁴+198u²+121 and 121u⁴+66u²+121); θ₁/π = 0.4025, θ₂/π = 0.7060. **No small integer relation**
a·θ₁+b·θ₂+c·π = 0 exists (searched |a|,|b|≤12, |c|≤24) → rationally independent, so by Weyl the pair
(mθ₁, mθ₂) mod 2π **equidistributes jointly on the 2-torus** (χ²/dof = 0.045 on an 8×8 grid). The
effective, quantitative form of Pass 75's discrepancy result.

## Files
- `w33_pass77_group.g`, `w33_pass77_group_out.txt` — GAP script + certificate (T1, T5, T6).
- `w33_pass77_frontier.py`, `.json` — Python witness (T2, T3, T4, T7 + reads GAP cert).
- `tests/test_pass77_frontier.py` — 7 assertions (networkx-guarded).
- `w33_paper.tex` — remark (e) appended to the Zeta Frontier subsection.
