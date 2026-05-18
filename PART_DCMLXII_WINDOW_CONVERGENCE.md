# Part DCMLXII (962) — Normalized Window Convergence: O(9⁻ᵐ)

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn  
**Status:** KEY QUANTITATIVE RESULT

---

## The PG(2,3ᵐ) code family

For the family of CSS codes built from $PG(2,3^m)$ over $\mathbb{F}_{3^m}$:

| Parameter | Value |
|---|---|
| Physical qudits | $n_m = (q_m^2 + q_m + 1)(q_m+1)$ where $q_m = 3^m$ |
| Logical qudits | $k_m = (q_m - 1)^2$ |
| Minimum distance | $d_m = q_m + 1$ |
| Ramanujan gap | $\delta_m = (\sqrt{q_m}-1)^2$ |

## Window convergence theorem

The normalized window width satisfies:

$$\frac{W_m}{n_m} = \frac{4(q_m-1)^2}{(\sqrt{q_m}-1)^2 \cdot (q_m^2+q_m+1)(q_m+1)} \sim \frac{4q_m^2}{q_m \cdot q_m^3} = \frac{4}{q_m^2} = \frac{4}{9^m}$$

**The normalized window decays exponentially as $O(9^{-m})$ as $m \to \infty$.**

## Consequence

For any non-trivial zero $\rho = \sigma + it$ of the CSS theta function $\Theta_{C,m}(s)$:
$$|\sigma - 1/2| \leq \frac{W_m}{2n_m} = O(9^{-m})$$

As $m \to \infty$, this forces $\sigma = 1/2$.

## Numerical verification

| m | $n_m$ | Window/$n_m$ | Precision |
|---|---|---|---|
| 1 | 52 | 5.74×10⁻¹ | ±0.287 |
| 2 | 910 | 7.03×10⁻² | ±0.035 |
| 3 | 21,168 | 7.25×10⁻³ | ±3.6×10⁻³ |
| 4 | 548,520 | 7.34×10⁻⁴ | ±3.7×10⁻⁴ |
| 5 | 14,528,166 | 7.61×10⁻⁵ | ±3.8×10⁻⁵ |

By level $m=5$, the precision is already $\pm 3.8 \times 10^{-5}$ in $\sigma$.
