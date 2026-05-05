# Part CCXCVI: Hoffman Ratio Bound for W(3,3)

## Overview

The **Hoffman ratio bound** (Delsarte–Hoffman bound) gives a spectral upper bound
on the independence number α(G) of a k-regular graph with smallest eigenvalue λ_min:

$$\alpha(G) \leq \frac{n \,|\lambda_{\min}|}{k + |\lambda_{\min}|}$$

For W(3,3) with n = 40, k = 12, λ_min = −4 (= S_EIG):

$$\alpha \leq \frac{40 \times 4}{12 + 4} = \frac{160}{16} = 10$$

This bound is **achieved**: α(W(3,3)) = 10, confirming that W(3,3) is a
*Delsarte graph*. Every quantity in the formula connects to SRG constants and SM
values.

---

## 1. Hoffman Bound Calculation

| Quantity | Value | Source |
| --- | --- | --- |
| n = V | 40 | W(3,3) vertex count |
| k = K | 12 | SRG degree |
| λ_min = S_EIG | −4 | negative SRG restricted eigenvalue |
| \|λ_min\| | 4 | = EW_GAUGE_4 |
| Numerator | 160 | = V × EW_GAUGE_4 |
| Denominator | 16 | = K + EW_GAUGE_4 = EW_GAUGE_4² |
| Bound | 10 | = α(W(3,3)) ✓ |

---

## 2. Key Identities

### Denominator = 16 = EW_GAUGE_4²

$$K + |\lambda_{\min}| = 12 + 4 = 16 = 4^2 = \text{EW\_GAUGE\_4}^2$$

The denominator is the square of the electroweak gauge count.

### Numerator = 160

$$V \times |\lambda_{\min}| = 40 \times 4 = 160 = V \times \text{EW\_GAUGE\_4}$$

Alternatively, from the edge count:

$$\text{EDGES} \times \frac{Q-1}{Q} = 240 \times \frac{2}{3} = 160$$

### ALPHA = V / EW_GAUGE_4 = 10

$$\alpha = \frac{V}{\text{EW\_GAUGE\_4}} = \frac{40}{4} = 10$$

The independence number is exactly V divided by the electroweak gauge count.

---

## 3. W(3,3) is a Delsarte Graph

A graph G is a *Delsarte graph* if α(G) exactly equals the Hoffman bound.
W(3,3) achieves α = 10 = Hoffman bound, confirming this property. Delsarte
graphs are deeply connected to linear programming bounds for codes and the
association scheme structure.

---

## 4. Clique Bound from Complement

Applying the Hoffman bound to the complement G̅ = SRG(40, 27, 18, 18) gives an
upper bound on the clique number ω(G) = α(G̅):

| Quantity | Value |
| --- | --- |
| Complement degree k̄ | 27 |
| Smallest eigenvalue of G̅ | −3 |
| Complement numerator | 40 × 3 = 120 |
| Complement denominator | 27 + 3 = 30 |
| Clique bound ω ≤ | 120/30 = **4** |

This yields ω(W(3,3)) ≤ 4 = EW_GAUGE_4. The bound is tight: maximum cliques in
W(3,3) have exactly 4 vertices (the "lines" of the GQ(3,3) structure from Part
CCXCIV).

---

## 5. Product Identity α × ω = V

$$\alpha(W(3,3)) \times \omega(W(3,3)) = 10 \times 4 = 40 = V$$

The product of the independence number and clique number equals the vertex count.
This is a striking multiplicative constraint: covering V vertices by α independent
sets each of size ω matches the partition structure of GQ(3,3) spreads and ovoids.

---

## 6. Summary Table

| Quantity | Value | Notes |
| --- | --- | --- |
| Hoffman numerator | 160 | = V × EW_GAUGE_4 |
| Hoffman denominator | 16 | = EW_GAUGE_4² |
| Hoffman bound | 10 | = α (tight) |
| α(W(3,3)) | 10 | = V / EW_GAUGE_4 |
| ω(W(3,3)) | 4 | = EW_GAUGE_4 (clique = gauge) |
| α × ω | 40 | = V |
| Is Delsarte | True | bound achieved |
| Checks pass | 27/27 | ✓ |

---

## 7. Connections to Earlier Parts

- **Part CCXCIII** — Lovász theta: ϑ(G̅) = α(G) = 10 confirms ALPHA = 10.
- **Part CCXCIV** — GQ(3,3): maximum cliques (ω = 4) are the lines of GQ(3,3)
  with s + 1 = 4 points each (= EW_GAUGE_4 = POINTS_PER_LINE from that part).
- **Part CCXCV** — Seidel matrix: |λ_min| = |S_EIG| = 4 feeds into both the
  Hoffman formula and the Seidel eigenvalue τ_r = −5 = −(1 + 2r).
- **Part CCLXX** — W(3,3) core: all SRG parameters used directly here.
