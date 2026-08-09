# PART CCCLVII: Two-Graph Structure of W(3,3)

## Overview

Part CCCLVII establishes the **two-graph structure** naturally carried by the strongly regular graph W(3,3) = SRG(40,12,2,4). A two-graph on a vertex set V is a collection T of 3-subsets (triples) such that every 4-subset contains an even number of T-triples. Given a graph G on V, the "switching class" two-graph takes a triple {i,j,k} to be odd if and only if it contains an **odd number of edges** of G. SRG(40,12,2,4) yields a two-graph of size 4480 with deep links to Standard Model constants.

---

## SRG Parameters

| Symbol | Value | Meaning |
|--------|-------|---------|
| V | 40 | Vertices |
| K | 12 | Degree |
| λ | 2 | Common neighbours (adjacent) |
| μ | 4 | Common neighbours (non-adjacent) |
| EDGES | 240 | Total edges |
| mult_r | 24 | Multiplicity of eigenvalue r = 2 |
| mult_s | 15 | Multiplicity of eigenvalue s = −4 |

---

## Triple Partition

Every 3-subset of V falls into exactly one class by its edge count:

| Class | Count | Formula |
|-------|-------|---------|
| 0-edge triples | 3240 | V · 3^4 = 40 · 81 |
| 1-edge triples | 4320 | (by subtraction) |
| 2-edge triples | 2160 | EDGES · (K−1−λ) = 240 · 9 |
| Triangles (3-edge) | 160 | V · K · λ / 6 = V · EW4 |
| **Total** | **9880** | C(40,3) |

The partition sums to 9880 = C(40,3) (parity check passes).

---

## Two-Graph Size

The two-graph T consists of all **odd** triples (1-edge or 3-edge):

$$|T| = \text{triples}_1 + \text{triples}_3 = 4320 + 160 = 4480$$

Equivalent formula via SRG parameters:

$$|T| = \frac{V \cdot K \cdot (V-K)}{3} = \frac{40 \cdot 12 \cdot 28}{3} = 4480$$

---

## Vertex Regularity

Each vertex v lies in exactly **336 odd triples**:

$$r_v = \frac{3 \cdot |T|}{V} = \frac{3 \cdot 4480}{40} = 336$$

This equals $K(V-K) = 12 \cdot 28 = 336$, and factors as:

$$336 = K \cdot (\text{SU5\_ADJ} + \mu) = 12 \cdot (24 + 4)$$

---

## Pair Counts

The two-graph is also **pair-regular** (a property of strongly regular switching classes):

| Pair type | Count of odd triples containing it |
|-----------|-----------------------------------|
| Adjacent (edge) | 20 = 2 · ALPHA |
| Non-adjacent | 16 = 2 · (K − μ) |
| Difference | 4 = EW\_GAUGE\_4 |

---

## Physics Connections

| Identity | Value | Interpretation |
|----------|-------|----------------|
| triangles = V · EW\_GAUGE\_4 | 160 = 40 · 4 | Triangles encode electroweak gauge dimension |
| triples\_0 = V · GENERATIONS^4 | 3240 = 40 · 81 | Zero-edge triples count generation ladder |
| odd\_per\_edge = 2 · ALPHA | 20 = 2 · 10 | Fine-structure inverse in two-graph pairing |
| odd\_per\_nonedge = 2(K−μ) | 16 = 2 · 8 | Non-edge pairing |
| diff = EW\_GAUGE\_4 | 4 | Electroweak gauge group dimension |
| r\_v = K(V−K) | 336 = 12 · 28 | Vertex regularity from degree-complement product |
| K(SU5\_ADJ + μ) | 336 = 12 · 28 | SU(5) adjoint plus weak hypercharge |

---

## Verification

All **27 checks pass** (27/27):

- Triple partition completeness (10 checks)
- Two-graph size identities (6 checks)
- Vertex regularity (7 checks)
- Pair counts and physics (4 checks)

```
status: PASS, checks_pass: 27, checks_total: 27
```

---

## Files

| File | Description |
|------|-------------|
| `exploration/PART_CCCLVII_TWO_GRAPH_BRIDGE.py` | Bridge with 27 verified checks |
| `tests/test_two_graph_ccclvii.py` | Test suite (96 tests) |
| `PART_CCCLVII_two_graph_results.json` | Machine-readable summary |
| `PART_CCCLVII_TWO_GRAPH_BRIDGE.md` | This document |
