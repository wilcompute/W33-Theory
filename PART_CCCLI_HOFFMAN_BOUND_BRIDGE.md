# PART CCCLI — Hoffman Bound and Maximum Independent Sets in W(3,3)

## Overview

The **Hoffman ratio bound** gives an eigenvalue-based upper bound on the independence number of a regular graph:

$$\alpha(G) \leq \frac{V \cdot |s|}{k + |s|}$$

For W(3,3) with $V=40$, $k=12$, $s=-4$:

$$\alpha(W(3,3)) \leq \frac{40 \cdot 4}{12 + 4} = \frac{160}{16} = 10$$

This bound is **tight**: W(3,3) has independent sets of exactly size 10, making it a **Hoffman-tight graph**.

## Key Formula

| Quantity | Value |
|---|---|
| $V$ (vertices) | 40 |
| $k$ (degree) | 12 |
| $s$ (smallest eigenvalue) | $-4$ |
| $\|s\|$ | 4 |
| $k + \|s\|$ (Hoffman denominator) | 16 |
| $\alpha(W(3,3))$ | **10** |
| Hoffman bound | $40 \cdot 4 / 16 = 10$ (tight) |

## Coclique Structure

Let $S$ be a maximum independent set ($|S| = 10$). By the SRG property ($\mu = 4$):

- Every vertex **outside** $S$ has exactly $\mu = 4$ neighbours in $S$
- Edges from $S$ to $V \setminus S$: $\alpha \cdot k = 10 \cdot 12 = 120$
- Cross-check: $(V - \alpha) \cdot \mu = 30 \cdot 4 = 120$ ✓

## Identities

| Identity | Value |
|---|---|
| $\alpha = 10$ | $= $ ALPHA (fine-structure proxy) |
| $V - \alpha = 30$ | $= 2 \cdot$ MULT\_S $= $ ALPHA $\cdot$ GENERATIONS |
| $\alpha \cdot k = 120$ | $= 5 \cdot$ SU5\_ADJ |
| $V / \alpha = 4$ | $=$ MU $= $ ABS\_S $=$ K4 vertex count |
| Hoffman denom $= 16$ | $= 2^4 = $ EDGES / MULT\_S |
| $\alpha / V = 1/4$ | $= |s| / (k + |s|)$ |

## Physics Bridge

| Mathematical fact | Physics interpretation |
|---|---|
| $\alpha = 10$ | ALPHA (fine-structure proxy in W(3,3) units) |
| $V - \alpha = 30 = $ ALPHA $\cdot$ GENERATIONS | 3 generations × 10 |
| Hoffman denom $= 16 = 2^4$ | Electroweak gauge bosons squared: $(W^+, W^-, Z, \gamma)^2$ |
| $\alpha \cdot K = 120 = 5 \cdot 24$ | SU(5) adjoint copies |
| $V / \alpha = 4 = $ MU | Four-fold structure: 4 EW gauge bosons, 4 = MU |
| MULT\_R $= 24 = $ SU5\_ADJ | W(3,3) multiplicity = SU(5) adjoint dimension |

## Verification

27 checks, all pass (PASS 27/27).

Groups:
1. Hoffman bound computation (5 checks)
2. Tightness and structural consistency (5 checks)
3. Complement and coclique properties (5 checks)
4. Physics connections (6 checks)
5. Related bounds and ratios (6 checks)

## File Index

| File | Description |
|---|---|
| `exploration/PART_CCCLI_HOFFMAN_BOUND_BRIDGE.py` | Bridge: Hoffman bound, 27/27 checks |
| `tests/test_hoffman_bound_cccli.py` | Tests: 71 tests, all pass |
| `PART_CCCLI_hoffman_bound_results.json` | Results JSON |
| `PART_CCCLI_HOFFMAN_BOUND_BRIDGE.md` | This file |
