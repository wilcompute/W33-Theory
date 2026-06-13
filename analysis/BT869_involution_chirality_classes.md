# BT869 — The Two Chirality Involutions: 45+36 Is the Polar-Pair Axis

**Status: PROVEN (exhaustive over all 315 involutions, `analysis/bt869_involution_chirality_classes.py`, data `data/bt869_involution_chirality_classes.json`)**

BT868 found two chirality types from the involution value χ_St(g³) ∈ {9, −3}.
BT869 names them: PSp(4,3) has **exactly two** involution classes, and they
are precisely those two types.

| class | size | fixed pts | fixed lines | χ_St | Steinberg split | identity |
| --- | --- | --- | --- | --- | --- | --- |
| polar-pair | **45** | 8 (= cube Q₃) | 16 | **+9 = q²** | **45 + 36** | central involution of a hyperbolic polar pair (centralizer (2T×2T), order 576) |
| reflection | 270 | 0 (fixed-point-free) | 4 | **−3 = −q** | 39 + 42 | the other involution type |

## The polar-pair self-reference

The dominant chirality involution (the one an order-6 g³ usually lands on)
is the **45-class**, and three 45's coincide:

- **class size = 45** (the number of involutions of this type up to nothing —
  it is a single conjugacy class of size 45),
- **= the number of hyperbolic polar pairs** {L, L^⊥} (BT810: index-45
  maximal, stabilizer (2T×2T):2),
- **= dim of its +1 eigenspace on the Steinberg matter register**.

Its 8 fixed points carry the **cube graph Q₃** under non-collinearity — the
BT773 involution-cube theorem, here for the inner 45-class — and its
centralizer has order 25920/45 = 576 = |2T × 2T|, the two-24-cell group of
BT810. So **the chirality Z₂ of the matter register is the central
involution that swaps a polar pair L ↔ L^⊥**, and the left/right split of
matter (45 + 36) is sized by the tritangent-plane count (45) and the
double-six count (36) — two of the five Schläfli geography indices.

## Reading

The session's chirality bit is now pinned to concrete substrate geometry, on
both sides of the duality:

- **BT862**: H₂ is the *sign-twisted* line module (chirality lives in the top
  homology, the oriented timetable carrier).
- **BT857/746/772**: chirality = axis type (the Weyl Z₂).
- **BT868**: chirality is one factor of the order-6 Z₃×Z₂ matter grading.
- **BT869 (now)**: the chirality involution *is* the polar-pair central
  swap; its matter eigenspaces are 45 (tritangents) + 36 (double-sixes).

Matter's left/right asymmetry and the 24-cell polar-pair geometry are the
same Z₂.

## Open

- The 270-class (fixed-point-free, χ_St = −3): its centralizer (order 96)
  and whether it is the chart-group O_h involution (BT811) — the
  "non-geometric" chirality.
- Lift to PGSp(4,3): how the inner 45/270 involutions relate to the outer
  540 anti-symplectic (duality) involutions of BT746/775.
