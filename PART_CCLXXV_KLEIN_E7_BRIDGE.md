# Part CCLXXV — Klein Quartic, PSL(2,7) and the E₇-56 Bridge

**Status:** 59/59 checks pass · 60/60 tests pass · zero free parameters · q = 3

---

## Executive Summary

Part CCLXXV reveals that the Klein quartic — the genus-3 Riemann surface with
the maximum possible automorphism group — is a second structural home for every
W(3,3) constant discovered in Part CCLXXIV.  The Fano plane (7 points) from
CCLXXIV is now the **face valency** of the Klein quartic, and the same pair
**(MU, PHI6) = (4, 7)** re-emerges in three new guises:

| Identity | LHS | = | RHS |
|---|---|---|---|
| Klein quartic vertices | V_K = 56 | = | 2 × MU × PHI6 |
| Klein quartic edges | E_K = 84 | = | PHI6 × K |
| Klein quartic faces | F_K = 24 | = | 2 × K |
| PSL(2,7) order | 168 | = | PHI6 × F_K = Q × V_K = 2 × E_K |
| E₇ minimal module | dim = 56 | = | V_K = 2 × MU × PHI6 |
| Bitangents to quartic | 28 | = | MU × PHI6 = odd theta chars |
| Genus | g = 3 | = | Q (base prime) |

---

## A  PSL(2,7) = GL(3,2)

PSL(2,7) is the automorphism group of both the Fano plane PG(2,2) and the
Klein quartic.  It has order

```
|PSL(2,7)| = 168 = 2³ × 3 × 7
```

The same order arises as **GL(3, F₂)** — the group of invertible 3×3 matrices
over the field with 2 elements:

```
|GL(3, F₂)| = (8−1)(8−2)(8−4) = 7 × 6 × 4 = 168
```

W(3,3) connections:

| Formula | Value |
|---|---|
| PHI6 × 24 | 7 × 24 = 168 |
| PHI6 × F_K | 7 × 24 = 168 |
| Q × V_K | 3 × 56 = 168 |
| 168 ÷ PHI6 | = 24 = 2K |
| 2³ × Q × PHI6 | 8 × 3 × 7 = 168 |

---

## B  Klein Quartic Combinatorics

The Klein quartic is the unique compact Riemann surface of genus 3 with the
maximum number of automorphisms allowed by the Hurwitz bound.  Its
combinatorial map (a {7,3}-tiling of the hyperbolic plane) has:

| Invariant | Value | W(3,3) link |
|---|---|---|
| Vertices V_K | 56 | 2 × MU × PHI6 |
| Edges E_K | 84 | PHI6 × K |
| Faces F_K | 24 | 2 × K |
| Euler characteristic χ | −4 | = 2 − 2g |
| Genus g | 3 | = Q |
| Face valency | 7 | = PHI6 |
| Vertex degree | 3 | = Q |
| |Aut| | 168 | = 2 × E_K |

Handshaking verifications:

```
E_K  = F_K × face_val ÷ 2 = 24 × 7 ÷ 2 = 84  ✓
V_K  = 2 × E_K ÷ vertex_deg = 168 ÷ 3 = 56   ✓
```

---

## C  Hurwitz (2, 3, 7) Triangle Group

For a compact Riemann surface of genus g ≥ 2, the **Hurwitz automorphism
theorem** bounds |Aut(X)| ≤ 84(g−1).  This maximum is achieved when X
uniformises the **(2, 3, 7) triangle group**, whose orbifold Euler defect is

```
δ = 1 − (1/2 + 1/3 + 1/7) = 1 − 41/42 = 1/42
```

The Hurwitz triple (p, q, r) = (2, 3, 7) satisfies:

| Condition | Value |
|---|---|
| 1/2 + 1/3 + 1/7 | = 41/42 < 1  (hyperbolic) |
| Defect δ | = 1/42 |
| Hurwitz bound 84(g−1) at g=3 | = 168 |
| r = 7 | = PHI6 (third Hurwitz parameter) |
| g = 3 | = Q (genus = base prime) |

The Klein quartic achieves the Hurwitz bound.  From the triple alone:

```
g = r − p − q + 1 = 7 − 2 − 3 + 1 = 3 = Q  ✓
```

---

## D  E₇ Lie Algebra and the 56-Dimensional Module

The exceptional Lie algebra E₇ has:

| Invariant | Value | W(3,3) link |
|---|---|---|
| Rank | 7 | = PHI6 |
| Positive roots | 63 | — |
| dim(E₇) = rank + 2×pos_roots | 7 + 126 = 133 | = PHI6 × 19 |
| Minimal faithful module | 56 | = V_K = 2 × MU × PHI6 |
| Hurwitz r | 7 | = rank(E₇) = PHI6 |

The 56-dimensional module carries a **Freudenthal quartic invariant**,
directly linking E₇ to the geometry of quartic curves — the same setting as
the Klein quartic and its 28 bitangents.

---

## E  28 Bitangents and Odd Theta Characteristics

A **bitangent** to a smooth plane quartic curve is a line tangent to it at two
distinct points.  The classical theorem states:

> Every smooth plane quartic curve over **ℂ** has exactly **28 bitangents**.

For a compact Riemann surface of genus g = 3, the **theta characteristics**
(spin structures) split as:

| Type | Count | Formula |
|---|---|---|
| Total | 64 | 2^(2g) = 2^6 |
| Odd | 28 | = MU × PHI6 = 4 × 7 |
| Even | 36 | = 64 − 28 |

Odd theta characteristics correspond bijectively to bitangents:

```
bitangents = odd theta chars = 28 = MU × PHI6  ✓
```

The exponent 2g = 6 = |(Z/7Z)*| — the Galois period of 1/7 from Part CCLXXIV.

---

## F  Heawood Graph Bridge (CCLXXIV Continuity)

The Heawood graph from Part CCLXXIV (the Levi graph of the Fano plane) connects
to the Klein quartic via the scaling factor MU = 4:

| Identity | LHS | = | RHS |
|---|---|---|---|
| V_K = MU × Heawood nodes | 56 | = | 4 × 14 |
| E_K = MU × Heawood edges | 84 | = | 4 × 21 |
| |PSL(2,7)| ÷ Heawood nodes | 168 ÷ 14 | = | 12 = K |
| |PSL(2,7)| = 2×MU × Heawood edges | 168 | = | 2 × 4 × 21 |

An elegant cross-structure identity involving E₇:

```
E_K = PHI6 × Heawood_E − E₇_pos_roots = 7 × 21 − 63 = 147 − 63 = 84  ✓
```

---

## G  W(3,3) Arithmetic Cross-Identities

| Identity | Formula | Value |
|---|---|---|
| V_K − V | 56 − 40 | = 16 = PHI4 + PHI6 − 1 |
| |PSL27| mod V | 168 mod 40 | = 8 = 2 × MU |
| E_K mod V | 84 mod 40 | = 4 = MU |
| V_K + E_K + F_K | 56+84+24 | = 164 = 4 × (V+1) = 4 × 41 |
| rank(E₇) = Hurwitz r | 7 | = 7 = PHI6 |
| g = r−p−q+1 | 7−2−3+1 | = 3 = Q |
| E_K = Q × bitangents | 3 × 28 | = 84 ✓ |
| V_K = 2 × bitangents | 2 × 28 | = 56 ✓ |
| |PSL27| = 6 × bitangents | 6 × 28 | = 168 ✓ |

---

## Key Unified Identity

```
PHI6 = 7 = rank(E₇) = Hurwitz r = Fano order
         = Klein face valency = Heawood chromatic number

MU × PHI6 = 4 × 7 = 28 = bitangents = odd theta chars (genus 3)

V_Klein = 2 × MU × PHI6 = 56 = dim(E₇ minimal module)
E_Klein = PHI6 × K = 84
F_Klein = 2 × K = 24
|PSL(2,7)| = 168 = PHI6 × F = Q × V = 2 × E

Genus g = 3 = Q  (genus equals the base prime)
2g = 6 = |(Z/7Z)*|  (Galois period of 1/7)
```

---

## Verification Summary

| Module | Checks | Status |
|---|---|---|
| `exploration/PART_CCLXXV_KLEIN_E7_BRIDGE.py` | 59/59 | ALL PASS |
| `tests/test_klein_e7_cclxxv.py` | 60/60 | ALL PASS |

All identities verified by explicit Python computation with no free parameters.
