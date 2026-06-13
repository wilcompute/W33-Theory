# BT868 — The Joint Generation × Chirality Grading

**Status: PROVEN (exhaustive over all order-6 classes, `analysis/bt868_joint_generation_chirality_grading.py`, data `data/bt868_joint_generation_chirality_grading.json`)**

The session's two matter-sector threads unify. An order-6 element g factors as
g² (order 3 = **generation**, BT863) × g³ (order 2 = **chirality**, BT862's
sign-twist), so its Z₆ = Z₃ × Z₂ eigengrading on the Steinberg matter register
is the *joint* structure. Because χ_St vanishes on every 3-singular power
(χ(gᵏ) = 0 for k ∈ {1,2,4,5}, all of order divisible by 3), only χ(1) = 81 and
the involution value χ(g³) survive, and the six multiplicities collapse to a
clean factored grading:

```text
m_j = (81 + (-1)^j · χ(g³)) / 6,    chirality halves (81 ± χ(g³))/2,
each chirality half = 3 equal generations  (m_0 = m_2 = m_4, m_1 = m_3 = m_5).
```

## The census (all order-6 classes)

| class sizes | χ(g³) | Z₆ multiplicities | chirality split |
| --- | --- | --- | --- |
| 360, 720, 720, 1440 | **9 = q²** | 15,12,15,12,15,12 | **45 + 36** |
| 2160 | **−3 = −q** | 13,14,13,14,13,14 | **39 + 42** |

- The generation 3-fold degeneracy holds in **every** class (verified):
  generation and chirality **factor independently** — the matter register
  carries a genuine Z₃ × Z₂ bigrading, jointly diagonalized by the order-6
  symmetries.
- The chirality split is geometry, not noise. The dominant family
  (χ(g³) = q²) splits **45 + 36** — exactly two of the five Schläfli
  geography indices (45 tritangent planes / polar pairs, 36 double-sixes /
  spreads). The second family (χ(g³) = −q) splits **39 + 42 = qΦ₃ + (81−qΦ₃)**
  — 39 = the gauge-sector dimension im ∂₀ of the single-photon paper.

## Reading

The Standard-Model picture sharpens once more: the matter register has two
commuting internal gradings — **generation** (Z₃, matter-blind per BT864) and
**chirality** (Z₂, the sign-twisted/oriented carrier per BT862) — and an
order-6 substrate symmetry diagonalizes both at once. The chirality halves are
not arbitrary: for the dominant involution type they are the substrate's own
45 and 36, tying the left/right matter split to the tritangent/double-six
geometry. Generation × chirality = 3 × 2 = 6 is the order of the symmetry that
sees both, and 6 = q! — the off-diagonal history count of the single-photon
paper's q² = q + q! master split.

## Open

- Identify the two involution types (χ_St = 9 vs −3) as substrate classes
  (the 2A/2B split; polar-pair central involutions vs reflections).
- The 45+36 chirality split vs the actual left/right Weyl chirality of
  BT746/772 (axis type): is the dominant order-6 chirality the same Z₂?
