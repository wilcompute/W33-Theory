# Part CCXCIV: Generalized Quadrangle GQ(3,3) and the W(3,3) Collinearity Graph

## Overview

The strongly regular graph W(3,3) is the **collinearity graph** of the
*symplectic generalized quadrangle* W(3, q) over GF(3), equivalently written
GQ(s, t) = GQ(3, 3). A generalized quadrangle is an incidence geometry in which
every point off a line is collinear to exactly one point on that line. The four
SRG parameters (v, k, λ, μ) of W(3,3) are completely determined by the single
fact that s = t = 3 = Q (the ternary base).

---

## 1. Generalized Quadrangle GQ(s, t) — Definition

A **generalized quadrangle** GQ(s, t) is a point-line incidence system satisfying:

1. Every line contains exactly s + 1 points.
2. Every point lies on exactly t + 1 lines.
3. For every point P not on a line ℓ, there is exactly one point of ℓ collinear
   with P.

The count formulas are:

| Quantity | Formula | Value for GQ(3,3) |
| --- | --- | --- |
| Points | (s+1)(st+1) | 40 |
| Lines | (t+1)(st+1) | 40 |
| Points per line | s+1 | 4 |
| Lines per point | t+1 | 4 |
| Ovoid size | st+1 | 10 |
| Spread size | st+1 | 10 |

---

## 2. GQ(3,3) Parameters

For the symplectic GQ W(3, q) over GF(3) with q = 3 = Q:

$$s = t = q = 3 = Q$$

Both GQ parameters equal the ternary base. Since s = t, the GQ is *self-dual*
(isomorphic to its point-line dual), which forces Points = Lines = 40 = V.

| Parameter | Symbol | Value | SM meaning |
| --- | --- | --- | --- |
| s | s_GQ | 3 | Q (ternary) |
| t | t_GQ | 3 | Q (ternary) |
| st | — | 9 | Q² |
| Points per line | s+1 | 4 | EW_GAUGE_4 |
| Lines per point | t+1 | 4 | EW_GAUGE_4 |
| Points = Lines | (s+1)(st+1) | 40 | V |

---

## 3. W(3,3) SRG Parameters Recovered

For the collinearity graph of GQ(s, t):

$$v = (s+1)(st+1), \quad k = s(t+1), \quad \lambda = s-1, \quad \mu = t+1$$

Substituting s = t = 3:

| SRG param | Formula | Value | W(3,3) |
| --- | --- | --- | --- |
| v | (3+1)(9+1) | 40 | V = 40 ✓ |
| k | 3 × (3+1) | 12 | K = 12 ✓ |
| λ | 3 − 1 | 2 | LAM = 2 ✓ |
| μ | 3 + 1 | 4 | MU = 4 ✓ |

All four SRG parameters are determined by the single value Q = 3.

---

## 4. Ovoids and Spreads

**Ovoid**: a set of points with no two collinear — i.e., a maximum independent set
in the collinearity graph:

$$|\text{ovoid}| = st + 1 = 9 + 1 = 10 = \alpha(W(3,3))$$

This matches the Lovász independence number from Part CCXCIII, now derived
purely from GQ geometry.

**Spread**: a set of pairwise non-concurrent lines covering every point exactly once:

$$|\text{spread}| = st + 1 = 10 \text{ lines}, \quad 10 \times (s+1) = 10 \times 4 = 40 = V$$

A spread partitions all 40 vertices of W(3,3) into 10 disjoint 4-cliques.

---

## 5. Point-Line Incidences

The total number of (point, line) incident pairs is:

$$\text{Incidences} = \text{Points} \times (t+1) = \text{Lines} \times (s+1) = 40 \times 4 = 160$$

The double-counting identity confirms s + 1 = t + 1 (self-dual GQ).

---

## 6. Common-Neighbour Counts

In the collinearity graph:

- **Adjacent (collinear) pair** P ~ Q: both lie on exactly 1 common line, and
  that line has s − 1 = 2 other points on it →
  $$\lambda = s - 1 = 2 = \text{LAM}$$

- **Non-adjacent (non-collinear) pair** P ≁ Q: there are exactly t + 1 = 4 points
  collinear to both →
  $$\mu = t + 1 = 4 = \text{MU}$$

The GQ axiom directly forces the SRG μ-condition.

---

## 7. SM Connections

| Quantity | Value | SM interpretation |
| --- | --- | --- |
| Lines per point = t+1 | 4 | EW_GAUGE_4 |
| Points per line = s+1 | 4 | EW_GAUGE_4 |
| V − EW_GAUGE_4 | 36 | QUARKS_36 |
| Ovoid size = st+1 | 10 | α(W(3,3)) = spectral independence bound |
| s = t = q | 3 | Q (ternary, strong-force base) |

---

## 8. Summary Table

| Quantity | Value | Notes |
| --- | --- | --- |
| s = t | 3 | = Q, ternary base |
| Points = Lines | 40 | = V, self-dual GQ |
| Points per line | 4 | = EW_GAUGE_4 |
| Lines per point | 4 | = EW_GAUGE_4 |
| v (SRG) | 40 | = V ✓ |
| k (SRG) | 12 | = K ✓ |
| λ (SRG) | 2 | = LAM ✓ |
| μ (SRG) | 4 | = MU ✓ |
| Ovoid size | 10 | = α(W(3,3)) |
| Spread size | 10 | lines covering all 40 pts |
| Checks pass | 27/27 | ✓ |

---

## 9. Connections to Earlier Parts

- **Part CCXCIII** — Lovász theta: α = 10 derived spectrally; here α = 10 follows
  from GQ ovoid formula st + 1 = 10 — two independent derivations converge.
- **Part CCXCII** — Gleason weight enumerator: Gleason ring generators at degrees 4
  and 12 match EW_GAUGE_4 = 4 and K = s(t+1) = 12 respectively.
- **Part CCXCI** — Covering radius: spread lines (10 cliques of size 4) connect
  to the 10 coset representatives at maximum weight.
- **Part CCLXX** — W(3,3) core: V = 40, K = 12, LAM = 2, MU = 4 are the SRG
  parameters derived here entirely from s = t = 3 = Q.
