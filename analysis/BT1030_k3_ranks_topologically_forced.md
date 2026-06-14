# BT1030 — The K3 level-2 boundary ranks are topologically forced (R3 clarifier)

**Status: clarifying observation on the active R3 edgewise program. Verified.**
Script `analysis/bt1030_k3_ranks_topologically_forced.py`, data
`data/bt1030_k3_ranks_topologically_forced.json`.

The edgewise-refinement program (BT984–BT1029) is grinding the K3₁₆ **level-2
middle boundary ranks** d₂ = 42345, d₃ = 110593 via sharded F₂ elimination in
CI (BT1015–1029). This note records that all four ranks are *exactly
determined* by the f-vector and the K3 Betti numbers, and draws the R3
consequence.

## All four ranks are forced (verified)

Each edgewise refinement of K3₁₆ is again a triangulation of the **same** smooth
4-manifold K3, so by the de Rham theorem (combinatorially: Dodziuk — the
simplicial cohomology of *any* triangulation equals the de Rham cohomology) its
homology is K3's, **b = (1,0,22,0,1)**, at *every* level. Given the f-vector,
`b_k = dim C_k − rank d_k − rank d_{k+1}` pins every rank top-down:

| | rank d₁ | rank d₂ | rank d₃ | rank d₄ |
| --- | ---: | ---: | ---: | ---: |
| forced by (f, Betti) | 2775 | **42345** | **110593** | 73727 |
| BT1005/1006 targets | 2775 | 42345 | 110593 | 73727 |

**Exact match**, with χ = Σ(−1)ᵏfₖ = 24 = Σ(−1)ᵏbₖ. (CP²₉ level-2 likewise:
forced ranks (458, 5518, 13825, 9215), χ = 3.)

## What this means for the compute

- The exact middle-rank grind **re-derives topologically-fixed numbers** — it
  is a *triangulation-validity consistency check*, not new convergence data.
- Validity is already pinned **cheaply**: the level-2 complex is a closed
  pseudomanifold (every 3-face in exactly two 4-faces — BT1006 verified the
  `{2: 184320}` incidence), is connected, has χ = 24, and is a refinement of
  the known K3₁₆ triangulation. Those (already-computed) facts force the ranks;
  the heavy F₂ elimination of d₂, d₃ adds confidence but no new information.

## What R3 actually needs (the massive sector)

The spectral action splits cleanly:

- **Harmonic / zero-mode sector** = homology = topology: exact at every level
  (already correct at level 1, b = (1,0,22,0,1)). It does not need the
  refinement limit.
- **Massive / nonzero-spectrum sector**: this carries the Seeley–DeWitt
  coefficient `a₂ ~ (1/6) ∫ R √g` = the **Einstein–Hilbert term**. *Only this
  sector needs the refinement limit.*

So the R3-relevant convergence quantity is the **massive heat trace**
`Tr' e^{-tΔ}` (zero modes removed) and its small-t `a₂` — exactly what the
stochastic/Chebyshev estimators (BT1004) target. The exact rank grind is
orthogonal to it.

## Constructive suggestion

Redirect the K3 level-2 compute budget from exact middle-rank F₂ elimination
(topologically redundant) to the **massive-sector a₂ convergence**: extract the
subleading `a₂` coefficient from the (zero-mode-subtracted) heat trace across
levels and check it tracks `(1/6)∫R` on the edgewise tower — the direct
numerical link between the spectral and geometric (Regge/CMS) routes, and the
genuine R3 endpoint.

(No criticism intended of the careful BT1005–1029 validation work; this is a
note on where the remaining compute most advances R3.)
