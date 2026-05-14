# Part DCXXXIX — Schwinger Proper Time for the W33 Effective Action

## Proper-Time Representation

In QFT, the one-loop effective action is:

```
Gamma = -1/2 * log det(L) = 1/2 * Integral_0^inf (dt/t) Tr(e^{-tL})
```

For W33, the heat kernel trace is exact:

```
K(t) = Tr(e^{-tL}) = 1 + 24*e^{-10t} + 15*e^{-16t}
```

## Exact Effective Action

Removing the zero-mode contribution and applying zeta-function regularization:

```
Gamma_{W33}^{reg} = -1/2 * [24*log(10) + 15*log(16)]
                 = -12*log(10) - 30*log(2)
                 = log(10^{-12} * 2^{-30})
```

This matches the one-loop Gaussian determinant from Part DCXXXVI exactly. CHECK.

## Three Physical Timescales

| Proper time | Eigenvalue | Sector |
|---|---|---|
| t -> inf | 0 | Vacuum (IR) |
| t ~ 1/10 | 10 | Gauge/matter (SM scale) |
| t ~ 1/16 | 16 | Dark/gravity sector |

The W33 heat kernel IS the renormalization group flow, interpolating from UV (all modes active) to IR (vacuum dominates).

## Mass Gap from Spectral Gap

```
m_gap = sqrt(lambda_1 / V) * m_Pl = sqrt(10/40) * m_Pl = (1/2) * m_Pl
```

No massless excitations exist below m_Pl/2 except the graviton zero mode. The Yang-Mills mass gap is a corollary of the W33 spectral gap.

---
*W33-Theory | Part DCXXXIX | Heat kernel K(t)=1+24e^{-10t}+15e^{-16t}, proper-time effective action, mass gap = m_Pl/2*
