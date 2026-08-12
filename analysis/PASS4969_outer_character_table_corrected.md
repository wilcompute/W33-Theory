# Pass 4969 — Outer Character Table: PSp(4,3) Extension (Corrected)

**Date:** 2026-08-12  
**Status:** EXECUTED — corrected basis at v=40

## Automorphism Tower

```
PSp(4,3)  ⊂  PSp(4,3):2  ⊂  G₃₂
|25920|       |51840|        |155520|
```

The outer automorphism Z₂ of PSp(4,3) acts on the adjacency matrix eigenspaces:
- r = +2 eigenspace (dimension 24): swapped orientation
- s = −4 eigenspace (dimension 15): swapped sign

This Z₂ is the **graph automorphism** interchanging the two non-trivial eigenspaces.

## Character Staircase (Corrected)

The irreducible characters of PSp(4,3) at degrees:

| Degree | Representation | Combinatorial Object |
|--------|---------------|---------------------|
| 1 | Trivial | All-ones vector |
| 12 | Gauge shell | k-neighbors of a vertex |
| 24 | r-eigenspace | m_r = 2k = 24 = |S₄| |
| 15 | s-eigenspace | m_s = v - 2k - 1 = 15 |
| 40 | Permutation rep | 40 vertices |
| 240 | Edge rep | 240 edges = |E₈ roots| |
| 2160 | W₂₄₀ face rep | W₂₄₀ polytope faces |

Staircase: **40 → 240 → 2160** at successive symmetry levels.

## Identity: m_r = |S₄|

From the July 2026 corrected commit (Perplexity Pass 5):
> m_r = 2k = 24 = |S₄| (r-eigenspace dim = 4-gluon permutation group order)
> m_r - m_s = 9 = q²

This is the key physical identity: the r-eigenspace dimension counts the
permutations of 4 gluon colors, while m_s = 15 = dim(SU(4)) − 1 counts
the generators of color SU(4) → SU(3) symmetry breaking.

## Outer Automorphism Physical Interpretation

The Z₂ outer automorphism swaps:
- Matter sector (27-shell, E₆ rep) ↔ Anti-matter sector
- This is the CPT symmetry at the graph level

## Cross-References

- Perplexity Pass 5 commit: m_r=24, m_s=15 corrected from 26/13
- BT1057_full_162_slot_table.md: 162 = q² × m_s = 9 × 18? Check.
- MCCXXXVII: v = 40 = q×p_Ih + Φ₆
