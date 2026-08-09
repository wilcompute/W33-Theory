# Part CCLXXX: Finite Geometry over GF(3), Incidence Structures, and the W(3,3) Configuration Bridge

**Series:** Theory of Everything — W(3,3) SRG(40,12,2,4) Atlas
**Part:** CCLXXX (280)
**Date:** 2026-05-04
**Checks:** 247/247 pass | **Tests:** 23/23 pass

---

## Abstract

Part CCLXXX establishes a comprehensive bridge between classical finite geometry over
GF(3), incidence designs, and the constants of the strongly regular graph W(3,3) =
SRG(40,12,2,4). Every projective and affine space count, every design parameter, and
every collineation group order in this atlas resolves to a W(3,3) constant.

---

## 1. GF(3) Field Arithmetic

The prime field GF(3) has characteristic Q = 3. Its tower of extensions gives

| Extension | Elements | Mult-order |
|-----------|----------|------------|
| GF(3) | Q = 3 | 2 |
| GF(9) | Q² = 9 | 8 |
| GF(27) | Q³ = 27 = LINES₂₇ | 26 |
| GF(81) | Q⁴ = 81 | 80 |

The Frobenius endomorphism x ↦ x³ = x in GF(3), and the product of all
nonzero elements equals −1 mod 3 (Wilson-type identity). Nonzero squares in
GF(3) form {1}.

---

## 2. Projective Space Point Counts

For PG(n, 3) the point count is (Q^{n+1} − 1)/(Q − 1):

| Space | Points | W(3,3) constant |
|-------|--------|-----------------|
| PG(0,3) | 1 | — |
| PG(1,3) | MU = 4 | Q + 1 = 4 |
| PG(2,3) | Φ₃ = 13 | Q² + Q + 1 |
| PG(3,3) | V = 40 | Q³ + Q² + Q + 1 |
| PG(4,3) | 121 | Q⁴ + Q³ + Q² + Q + 1 |

The vertex count V = 40 of W(3,3) equals the number of points in PG(3,3).
The difference PG(3,3) − PG(2,3) = 27 = Q³ = LINES₂₇.

---

## 3. Affine Space Point and Line Counts

For AG(n, 3):

| Space | Points | Lines | Connection |
|-------|--------|-------|------------|
| AG(1,3) | Q = 3 | — | |
| AG(2,3) | Q² = 9 | K = 12 | Q(Q+1) = 12 |
| AG(3,3) | Q³ = 27 = LINES₂₇ | 117 = Q²·Φ₃ | |

AG(2,3) has exactly K = 12 lines, with MU = 4 lines through each point.
The incidence identity Q²(Q+1) = K·Q confirms V_lines · pts_per_line = L · Q.

AG(3,3) has LINES₂₇ = Q³ = 27 points — the same as the number of lines on
the cubic surface E₆.

---

## 4. Steiner Systems

### 4.1 S(2,3,9) — The Affine Plane AG(2,3)

| Parameter | Value | W(3,3) |
|-----------|-------|---------|
| v | Q² = 9 | |
| k | Q = 3 | |
| b (blocks) | K = 12 | |
| r (replication) | MU = 4 | |
| Parallel classes | MU = 4 | |
| Blocks per class | Q = 3 | |

S(2,3,9) is resolvable with MU = 4 parallel classes of Q = 3 blocks each.

### 4.2 S(2,4,13) — The Projective Plane PG(2,3)

| Parameter | Value | W(3,3) |
|-----------|-------|---------|
| v | Φ₃ = 13 | |
| k | MU = 4 | |
| b (blocks) | Φ₃ = 13 | symmetric |
| r (replication) | MU = 4 | |
| Order | Q = 3 | k − 1 = Q |

S(2,4,13) is the unique symmetric 2-design of order Q = 3.

---

## 5. PG(3,3) Atlas

PG(3,3) is self-dual with V = 40 points and V = 40 planes. Its line count:

$$\text{lines} = \frac{(Q^4-1)(Q^3-1)}{(Q^2-1)(Q-1)} = 130 = \Phi_3 \cdot \Phi_4$$

Key data:

| Item | Count | Identity |
|------|-------|---------|
| Points | V = 40 | Q³+Q²+Q+1 |
| Planes | V = 40 | self-dual |
| Lines | 130 | Φ₃·Φ₄ = 13·10 |
| Lines per point | Φ₃ = 13 | |
| Points per line | MU = 4 | Q+1 |
| Spread size | Φ₄ = 10 | Q²+1 |

A spread of PG(3,3) consists of Φ₄ = 10 disjoint lines partitioning all V = 40 points.

---

## 6. Collineation Groups

| Group | Order | W(3,3) |
|-------|-------|--------|
| GL(2,3) | 48 = 4K | (Q²−1)(Q²−Q) |
| SL(2,3) | 24 = 2K | binary tetrahedral |
| PSL(2,3) ≅ A₄ | K = 12 | |
| PGL(2,3) ≅ S₄ | 2K = 24 | |
| GL(3,3) | 11232 | |
| SL(3,3) | 5616 | |

PSL(2, p) orders satisfy:
- PSL(2,3) = K = 12 ← A₄
- PSL(2,5) = 5K = 60 ← A₅
- PSL(2,7) = 14K = 168
- PSL(2,11) = 55K = 660
- PSL(2,9) = 30K = 360 = COXETER_E8 · K

AUT(W(3,3)) = 51840 = W(E₆) is divisible by both PSL(2,3) and PSL(2,5).

---

## 7. Elliptic Quadric and Ovoid

The elliptic quadric Q⁻(3,3) in PG(3,3) has Q²+1 = Φ₄ = 10 points and forms an
ovoid. Every tangent plane meets it in a single point, giving MU = 4 tangent lines per
point (Q+1 = 4). The spread size Q²+1 = Φ₄ equals the ovoid size, a deep duality.

The hyperbolic quadric Q⁺(3,3) has (Q+1)² = 16 points.

---

## 8. Generalized Quadrangle GQ(2,4)

GQ(2,4) is the unique generalized quadrangle with parameters (s,t) = (2,4):

| Parameter | Value | W(3,3) |
|-----------|-------|--------|
| Points | LINES₂₇ = 27 | (s+1)(st+1) |
| Lines | 45 | (t+1)(st+1) |
| Points per line | Q = 3 | s+1 |
| Lines per point | 5 | t+1 |

The collinearity graph of GQ(2,4) is the Schläfli graph SRG(27,10,1,5), connecting
this construction to the 27 lines on a cubic surface.

---

## 9. Hermitian Variety U(3, Q²)

The Hermitian curve/unital over GF(Q²) embedded in PG(2,Q²) has Q³+1 = 28 points
and block size Q+1 = MU = 4:

| Parameter | Value | W(3,3) |
|-----------|-------|--------|
| Points | Q³+1 = 28 | MU·Φ₆ = 4·7 |
| Blocks | 63 | Q²·Φ₆ = 9·7 |
| Block size | MU = 4 | Q+1 |
| Replication | Q² = 9 | |

Note Q³+1−1 = Q³ = LINES₂₇: the unital has one more point than LINES₂₇.

---

## 10. Spreads and Packings in PG(3,3)

A spread of PG(3,3) partitions V = 40 points into Φ₄ = 10 lines of MU = 4 points each:

$$\Phi_4 \cdot \text{MU} = 10 \cdot 4 = 40 = V$$

Each regulus in a regulus-free spread has size MU = Q+1 = 4.
Total lines 130 = Φ₃·Φ₄.

---

## 11. Design Theory — Fisher and Bose-Mesner

Fisher's inequality b ≥ v holds: for S(2,3,9) we have K = 12 > Q² = 9. For S(2,4,13)
equality holds (symmetric design, b = v = Φ₃ = 13).

The Bose-Mesner algebra of W(3,3) has dimension 3 (one class for each of: equal, adjacent,
non-adjacent). The complement of PG(2,3) as a graph has λ = 6, k = Q².

---

## 12. Witt Design S(5,6,12)

The Witt design S(5,6,12) is the unique 5-design on K = 12 points:

| t-design level | λ_t | W(3,3) |
|----------------|-----|--------|
| 5 | 1 | |
| 4 | MU = 4 | |
| 3 | K = 12 | |
| 2 | COXETER_E8 = 30 | |
| 1 (r) | 66 | |
| 0 (b) | 132 = 11K | |

The Mathieu group M₁₂ acts 5-transitively on the K = 12 points of this design.

---

## 13. Mathieu Groups

| Group | Order | W(3,3) connection |
|-------|-------|-------------------|
| M₁₁ | 7920 | |
| M₁₂ | 95040 = 11·M₁₁ | acts on K = 12 points |
| M₂₂ | 443520 | |
| M₂₄ | 244823040 | acts on 2K = 24 points |

M₁₂/M₁₁ = K = 12. M₂₄ acts on 24 = 2K points via the Witt design S(5,8,24).

---

## 14. Projective Lines

| Line | Points | W(3,3) |
|------|--------|--------|
| PG(1,3) | MU = 4 | Q+1 |
| PG(1,9) | Φ₄ = 10 | 9+1 |
| PG(1,11) | K = 12 | 11+1 |

The three key W(3,3) constants MU, Φ₄, K arise as point counts of projective lines over
prime powers 3, 9, 11 respectively.

---

## 15. Oval and Arc Theory

In PG(2,3) (odd characteristic):
- Maximum arc (oval) has size Q+1 = MU = 4
- Each point of the oval has Q = 3 secant lines through it
- Total secants = 6; external lines = Q = 3
- No nucleus (odd q), no hyperoval

Maximum cap (arc) in PG(3,3): Q²+1 = Φ₄ = 10 points (the elliptic quadric).

---

## 16. Transport Edge Count

$$270 = \text{TRANSPORT\_EDGES} = \Phi_4 \cdot Q^3 = 10 \cdot 27$$

Cross-checks:
- 270 = Q²·COXETER_E₈ = 9·30
- 270 = EDGES + COXETER_E₈ = 240 + 30
- 270 = Q·Q²·Φ₄ = 3·9·10
- 270 ÷ Φ₄ = Q³ = LINES₂₇

---

## 17. Combinatorial Master Table

| Identity | LHS | RHS | W(3,3) |
|----------|-----|-----|--------|
| V·K/2 = EDGES | 40·12/2 | 240 | edge count |
| Φ₃·Φ₄ = 130 | 13·10 | 130 | PG(3,3) lines |
| Q²+Q+1 = Φ₃ | 9+3+1 | 13 | |
| Q³+Q²+Q+1 = V | 27+9+3+1 | 40 | |
| Q(Q+1) = K | 3·4 | 12 | AG(2,3) lines |
| V = Φ₄·MU | 10·4 | 40 | spread×line |
| Q³+1 = MU·Φ₆ | 28 | 4·7 | unital pts |
| TRANSPORT = Φ₄·Q³ | 10·27 | 270 | |

---

## 18. W(3,3) Geometry Atlas Summary

Every finite geometric space attached to GF(3) maps to W(3,3):

| Structure | Key count | W(3,3) |
|-----------|-----------|--------|
| AG(2,3) | K = 12 lines | |
| PG(2,3) | Φ₃ = 13 points | |
| PG(3,3) | V = 40 points | |
| AG(3,3) | Q³ = 27 pts | LINES₂₇ |
| S(2,3,9) | K = 12 blocks | |
| S(2,4,13) | Φ₃ = 13 blocks | symmetric |
| GQ(2,4) | LINES₂₇ = 27 pts | |
| Ovoid Q⁻(3,3) | Φ₄ = 10 pts | spread size |
| Unital U(3,3) | 28 pts | MU·Φ₆ |
| PG(1,11) | K = 12 pts | |
| W(E₆) | AUT = 51840 | |

---

## Source

- Bridge: [exploration/PART_CCLXXX_FINITE_GEOMETRY_BRIDGE.py](exploration/PART_CCLXXX_FINITE_GEOMETRY_BRIDGE.py)
- Tests: [tests/test_finite_geometry_cclxxx.py](tests/test_finite_geometry_cclxxx.py)
- Results: [PART_CCLXXX_finite_geometry_results.json](PART_CCLXXX_finite_geometry_results.json)

**Total checks:** 247/247 | **Tests:** 23/23
