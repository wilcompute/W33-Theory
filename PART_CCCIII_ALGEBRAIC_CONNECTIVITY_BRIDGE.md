# Part CCCIII — Algebraic Connectivity (Fiedler Value) of W(3,3)

## Summary

| Field | Value |
|-------|-------|
| Part | CCCIII (303rd part) |
| Checks | 27/27 |
| Tests | 49/49 |
| Status | PASS |

## Overview

The **algebraic connectivity** (Fiedler value) of a graph $G$ is the
second-smallest eigenvalue of its Laplacian matrix $L = D - A$:

$$a(G) = \lambda_2(L)$$

For a $k$-regular graph, Laplacian eigenvalues are $\lambda_i(L) = k - \mu_i(A)$
where $\mu_i(A)$ are the adjacency eigenvalues.

W(3,3) adjacency eigenvalues: $K=12$, $r=2$, $s=-4$, giving Laplacian eigenvalues:

| Laplacian $\lambda$ | Multiplicity | Origin |
|---------------------|-------------|--------|
| 0 | 1 | $K - K$ (connectivity) |
| 10 | 24 | $K - r = 12 - 2$ |
| 16 | 15 | $K - s = 12 - (-4)$ |

## Algebraic Connectivity

$$a(W) = \lambda_2(L) = K - r = 12 - 2 = \mathbf{10} = \alpha$$

The Fiedler value equals ALPHA — the SM fine-structure proxy — and also equals
the Hoffman independence bound and Lovász theta number from Parts CCCII/CCCI.

## Laplacian Spectral Radius

$$\lambda_{\max}(L) = K - s = 12 + 4 = \mathbf{16} = \text{EW\_GAUGE\_4}^2 = 4^2$$

The spectral radius encodes the electroweak gauge factor squared.

## Key Identities

### Normalised Laplacian

The normalised Laplacian $\mathcal{L} = I - D^{-1/2} A D^{-1/2}$ has eigenvalues $\theta_i = \lambda_i / K$:

$$\theta_1 = 0, \quad \theta_2 = \frac{10}{12} = \frac{5}{6}, \quad \theta_3 = \frac{16}{12} = \frac{4}{3}$$

Weighted sum: $\sum_i m_i \theta_i = 24 \cdot \frac{5}{6} + 15 \cdot \frac{4}{3} = 20 + 20 = 40 = V$

### Kirchhoff Index

The resistance distance sum (Kirchhoff / Wiener index):

$$R(W) = V \cdot \sum_{i>0} \frac{1}{\lambda_i} = 40 \cdot \left(\frac{24}{10} + \frac{15}{16}\right) = \frac{267}{2}$$

### Cheeger Isoperimetric Bounds

$$h(G) \geq \frac{a(G)}{2} = 5, \qquad h(G) \leq \sqrt{2K \cdot a(G)} = \sqrt{240} \approx 15.49$$

Remarkably: $2K \cdot a(G) = 2 \cdot 12 \cdot 10 = 240 = |E(W)|$ — the Cheeger
upper squared equals the edge count.

### Eigenvalue Product and Sum

$$\lambda_2 \cdot \lambda_{\max} = 10 \cdot 16 = 160 = V \cdot \text{EW} = 40 \cdot 4$$

$$\lambda_2 + \lambda_{\max} = 10 + 16 = 26 = 2K + 2$$

$$\lambda_{\max} - \lambda_2 = 6 = K/2$$

## SM Encoding Table

| Quantity | Value | SM Meaning |
|----------|-------|------------|
| $a(W) = \lambda_2(L)$ | 10 | ALPHA (Fiedler = coupling proxy) |
| $\lambda_{\max}(L)$ | 16 | $\text{EW}^2 = 4^2$ |
| Connectivity ratio | 5/8 | $\lambda_2 / \lambda_{\max}$ |
| Cheeger lower | 5 | $a(G)/2$ |
| $\lambda_2 \cdot \lambda_{\max}$ | 160 | $V \cdot \text{EW} = 40 \cdot 4$ |
| Kirchhoff index | 267/2 | Exact rational network measure |
| Spectral gap $\lambda_2 - 0$ | 10 | ALPHA |

## Files

| File | Description |
|------|-------------|
| `exploration/PART_CCCIII_ALGEBRAIC_CONNECTIVITY_BRIDGE.py` | Bridge (27/27 checks) |
| `tests/test_algebraic_connectivity_ccciii.py` | Test suite (49/49) |
| `PART_CCCIII_algebraic_connectivity_results.json` | Machine-readable summary |
| `PART_CCCIII_ALGEBRAIC_CONNECTIVITY_BRIDGE.md` | This document |
