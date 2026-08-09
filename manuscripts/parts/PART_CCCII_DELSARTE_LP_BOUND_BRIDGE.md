# Part CCCII — Delsarte Linear Programming Bound for W(3,3)

## Summary

| Field | Value |
|-------|-------|
| Part | CCCII (302nd part) |
| Checks | 27/27 |
| Tests | 54/54 |
| Status | PASS |

## Overview

**Delsarte's linear programming bound** (1973) gives tight upper bounds on the
sizes of independent sets (codes) and cliques in distance-regular graphs,
using only the eigenvalues of the association scheme.  No computation of
actual combinatorial structures is required — purely spectral.

For SRG(n, k, λ, μ) the two bounds are:

$$\alpha(G) \leq \frac{n \cdot (-s)}{k - s} \quad \text{(Hoffman / independence bound)}$$

$$\omega(G) \leq 1 + \frac{k}{-s} \quad \text{(Delsarte clique / ratio bound)}$$

For W(3,3) = srg(40, 12, 2, 4), $s = -4$:

$$\alpha(W) \leq \frac{40 \cdot 4}{12 + 4} = \frac{160}{16} = \mathbf{10} = \alpha$$

$$\omega(W) \leq 1 + \frac{12}{4} = \mathbf{4} = \omega$$

**Both bounds are achieved exactly** — W(3,3) is LP-tight.

## Key Identities

### LP Duality Product

$$\alpha(W) \cdot \omega(W) = 10 \cdot 4 = 40 = V$$

This is the same product identity satisfied by the Lovász theta numbers
$\vartheta(W) \cdot \vartheta(\bar{W}) = 40$ (Part CCCI) — the two coincide
because the LP bound is tight.

### LP Duality Sum

$$\alpha(W) + \omega(W) = 10 + 4 = 14 = \vartheta(W) + \vartheta(\bar{W})$$

The LP sum also equals the theta sum from Part CCCI.

### Spread Identity

$$\alpha \cdot \left(1 + \frac{K}{\mu}\right) = 10 \cdot (1 + 3) = 40 = V$$

This expresses that the 10-element independent set is "maximally spread" — every
vertex outside it has exactly $\mu = 4$ neighbours inside.

### Fractional Chromatic Number

$$\chi_f(W) = \frac{V}{\alpha} = \frac{40}{10} = 4 = \text{EW\_GAUGE\_4}$$

### Complement LP

The complement $\bar{W}$ = srg(40, 27, 18, 18) with $s_{\bar{W}} = -3$:

$$\alpha(\bar{W}) \leq \frac{40 \cdot 3}{27 + 3} = \frac{120}{30} = 4 = \omega(W)$$

The complement independence bound equals the clique number of $W$ — perfect
duality.

## SM Encoding Table

| Quantity | Value | SM Meaning |
|----------|-------|------------|
| $\alpha(W)$ | 10 | ALPHA (coupling proxy) |
| $\omega(W)$ | 4 | EW\_GAUGE\_4 |
| $\chi_f(W)$ | 4 | EW gauge factor (fractional chromatic) |
| Clique cover bound | 10 | ALPHA (dual cover) |
| $\alpha \cdot \omega$ | 40 | State-space dimension $V$ |
| $\alpha / \omega$ | 5/2 | Ratio = $\vartheta/\vartheta_{\bar W}$ |
| $\alpha + \omega$ | 14 | Theta sum (CCCI) |
| LP code rate bound | $\approx 0.557$ | $\log_2(10)/\log_2(40)$ |

## SM Coupling Proxy Hierarchy

The LP bounds give an ordering of SM coupling proxies:

$$\frac{1}{\alpha(\bar{W})} = \frac{1}{4} > \frac{1}{K} = \frac{1}{12} > \frac{1}{K_2} = \frac{1}{27}$$

This matches the expected GUT-scale ordering $g_1 > g_2 > g_3$ for the SM
gauge couplings.

## Files

| File | Description |
|------|-------------|
| `exploration/PART_CCCII_DELSARTE_LP_BOUND_BRIDGE.py` | Bridge (27/27 checks) |
| `tests/test_delsarte_lp_bound_cccii.py` | Test suite (54/54) |
| `PART_CCCII_delsarte_lp_bound_results.json` | Machine-readable summary |
| `PART_CCCII_DELSARTE_LP_BOUND_BRIDGE.md` | This document |
