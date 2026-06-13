# BT885 — The Yang-Mills Coupling to Matter: Steinberg Vanishing Filters the Flux to 1080

**Status: PROVEN (full census, `analysis/bt885_yang_mills_steinberg_coupling.py`, data `data/bt885_yang_mills_steinberg_coupling.json`)**

The gauge-matter coupling. The matter register is the Steinberg module
(BT861), and the gauge flux through a matter triangle is the Wilson loop
W = R_a R_b R_c (BT884). Their coupling is χ_St(W), and Steinberg vanishing
on 3-singular elements filters it sharply.

## The theorems

- **T1:** χ_St(W) = 0 on **all 160 collinear** triangles (flux order 3,
  3-singular) — the flat causal sector is invisible to the matter register.
- **T2:** on the 3240 matter triangles, χ_St(W) is nonzero **only on the
  360 order-2/4 loops**:

| flux order | count | χ_St(W) | substrate value |
| --- | --- | --- | --- |
| 2 | 180 | **+9** | +q² (the BT869 polar-pair central involution!) |
| 4 | 180 | **−3** | −q |
| 6 | 1440 | 0 | 3-singular (matter-invisible) |
| 12 | 1440 | 0 | 3-singular (matter-invisible) |

  The 2880 order-6/12 loops are 3-singular and matter-invisible; the matter
  register couples to gauge flux **only through the non-3-singular
  (quaternionic-square) sector**.
- **T3:** the total Steinberg gauge-matter coupling is

```text
Σ χ_St(W) over the 3240 matter triangles = 180·9 + 180·(−3) = 1080 = 540·2
```

— exactly the **chart double-cover count** (BT845/856, the 540 charts covered
twice). The Yang-Mills action S = Σ(1 − χ_St(W)/81) = 3240 − 1080/81 = 3226.67.

## Reading

Two exact identifications fall out:

1. **The order-2 flux is the chirality involution.** The 180 matter triangles
   whose Wilson loop has order 2 carry χ_St = +9 = q² — the Steinberg
   character of the **polar-pair central involution** (BT869). So the
   abelian-square flux on matter is precisely the matter-chirality Z₂. The
   gauge flux and the chirality involution are the same element on those 180
   triangles.
2. **The total coupling is the chart double cover.** Σ χ_St(W) = 1080 =
   540 × 2, the chart double-cover / mirror-bus count (BT845/856). The
   gauge-matter coupling, summed over all matter triangles, equals the
   transport-bus slot count — the same 1080 that the icosahedral compass
   double-covers. Gauge dynamics and the routing fabric meet at 1080.

So the matter register sees gauge flux only through its non-3-singular part,
that part is the chirality involution (χ_St = q²) plus the −q sector, and the
grand total is the chart double cover. This closes the gauge-dynamics arc
(BT876–885) with the gauge-matter coupling pinned to substrate invariants.

## Open

- The Yang-Mills action's variational structure: is 3226.67 = (3240·81 −
  1080)/81 a stationary point, and does the order-2/4 concentration drive a
  discrete equation of motion?
- 1080 = 540·2 (charts) = the gauge-matter coupling = the compass double
  cover (BT856): a triple identity (gauge / routing / compass) to unify.
