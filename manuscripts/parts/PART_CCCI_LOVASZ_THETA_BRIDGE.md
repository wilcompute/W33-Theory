# Part CCCI — Lovász Theta Function of W(3,3)

## Summary

| Field | Value |
|-------|-------|
| Part | CCCI (301st part) |
| Checks | 27/27 |
| Tests | 46/46 |
| Status | PASS |

## Overview

The **Lovász theta number** $\vartheta(G)$ is the celebrated semidefinite-programming
bound on the Shannon zero-error capacity of a graph, introduced by Lovász (1979).
For vertex-transitive strongly regular graphs it has the elegant closed form

$$\vartheta(G) = \frac{-n\,s}{k - s}$$

where $s$ is the smallest restricted eigenvalue.

For W(3,3) = srg(40, 12, 2, 4):

$$\vartheta(W) = \frac{-40 \cdot (-4)}{12 - (-4)} = \frac{160}{16} = 10 = \alpha$$

The theta number equals the Hoffman independence bound and the SM fine-structure
proxy ALPHA simultaneously — a triple coincidence that is a structural constraint.

## Key Identities

### Product Identity (Lovász 1979)

For vertex-transitive graphs:
$$\vartheta(G) \cdot \vartheta(\bar{G}) = V$$

For W(3,3): $\vartheta(W) \cdot \vartheta(\bar{W}) = 10 \cdot 4 = 40 = V$ ✓

### Complement Theta

The complement $\bar{W}$ = srg(40, 27, 18, 18) has smallest restricted eigenvalue
$s_{\bar{W}} = -1 - r_W = -3$:

$$\vartheta(\bar{W}) = \frac{-40 \cdot (-3)}{27 - (-3)} = \frac{120}{30} = 4 = \text{EW\_GAUGE\_4}$$

This is a remarkable encoding: the complement theta equals the electroweak gauge
factor 4.

### Ratio Encoding

$$\frac{\vartheta(W)}{\vartheta(\bar{W})} = \frac{10}{4} = \frac{5}{2} = \frac{\alpha}{\text{EW}} \cdot \frac{1}{2}$$

### SM Coupling Proxies

The theta numbers and graph parameters give a hierarchy of SM coupling proxies:

| Coupling | Proxy | Value |
|----------|-------|-------|
| $g_1^2$ (U(1)) | $1/\vartheta(\bar{W})$ | 1/4 |
| $g_2^2$ (SU(2)) | $1/K$ | 1/12 |
| $g_3^2$ (SU(3)) | $1/K_2$ | 1/27 |

The ordering $g_1 > g_2 > g_3$ matches the GUT-scale unification hierarchy.

## Interpretation

| Quantity | Value | Physical Meaning |
|----------|-------|-----------------|
| $\vartheta(W)$ | 10 | Lovász theta = Hoffman bound = ALPHA |
| $\vartheta(\bar{W})$ | 4 | EW gauge factor |
| $\vartheta(W) \cdot \vartheta(\bar{W})$ | 40 = V | Product identity encodes state space |
| $\chi_f(W) \geq V/\vartheta(W)$ | $\geq 4$ | Fractional chromatic lower bound |
| $\Theta(W) \leq \vartheta(W)$ | $\leq 10$ | Shannon capacity bounded by ALPHA |
| $\vartheta(W) + K$ | 22 | Sum with valency |
| $\vartheta(W) + \vartheta(\bar{W})$ | 14 | Sum of theta numbers |

## Files

| File | Description |
|------|-------------|
| `exploration/PART_CCCI_LOVASZ_THETA_BRIDGE.py` | Bridge (27/27 checks) |
| `tests/test_lovasz_theta_ccci.py` | Test suite (46/46) |
| `PART_CCCI_lovasz_theta_results.json` | Machine-readable summary |
| `PART_CCCI_LOVASZ_THETA_BRIDGE.md` | This document |
