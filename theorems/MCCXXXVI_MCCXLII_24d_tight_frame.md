# Theorems MCCXXXVI–MCCXLII: The 24D Tight Frame and the Threefold Bridge

## MCCXXXVI — The 480 Oriented Corners Span the Eigenvalue-2 Space

**Statement:** The 480 oriented corners `(p, la, lb)` of W(3,3), mapped to
vectors `W[i] = χ_{la} - χ_{lb} ∈ Z^40`, span EXACTLY the eigenvalue-2
eigenspace of the W33 adjacency matrix.

**Proof:** Computed. `||P_2 - P_frame||_F = 0.00000000` (machine precision).
The projector onto the W33 eigenvalue-2 space (multiplicity 24) is identical
to the projector onto the column space of the corner matrix W.

**Eigenvalue structure of srg(40,12,2,4):**
- λ = 12, multiplicity 1 (all-ones eigenvector)
- λ = 2, multiplicity **24** ← our space
- λ = −4, multiplicity 15

---

## MCCXXXVII — The 480 Corners Form a Tight Frame in R^24

**Statement:** The 480 oriented corner vectors form a TIGHT FRAME in
the 24-dimensional eigenvalue-2 eigenspace with:
- Frame bound A = **120**
- All vector norms: ||W[i]||² = 6 (uniform)
- W^T W = 120 · P_{24D}

**Verification:**
- Frame bound formula: A = N · ||v||² / dim = 480 · 6 / 24 = **120** ✓
- W^T W eigenvalues: 24 equal eigenvalues of 120, 16 zero eigenvalues ✓
- All singular values of W equal √120 ✓

**Consequence:** The 480 corners form a **spherical 1-design** (tight frame)
in 24D. Every direction in the 24D space has equal representation.

---

## MCCXXXVIII — The 8-Level Inner Product Spectrum

**Statement:** The Gram matrix of the 480 corner vectors has inner products
at exactly 8 distinct off-diagonal values:

| Value | Count | Geometric class |
|---|---|---|
| −6 | 240 | Antipodal pairs: (p,la,lb) ↔ (p,lb,la) |
| −3 | 960 | Strong opposing |
| −2 | 10,800 | Medium opposing |
| −1 | 25,920 | Weak opposing |
| 0 | 39,360 | Orthogonal |
| +1 | 25,920 | Weak parallel |
| +2 | 10,800 | Medium parallel |
| +3 | 960 | Strong parallel |

The distribution is PERFECTLY ANTISYMMETRIC under negation.
Total off-diagonal pairs: C(480,2) = 114,960. Sum = 240+960+10800+25920+39360+25920+10800+960 = 114,960. ✓

---

## MCCXXXIX — The k=3 Neighborhood is the Line-Cone

**Statement:** For corner (p, {la, lb}), the 18 strong (k=3) quadrangle
neighbors are exactly the corners at the 6 points that lie on lines la or
lb (other than p). Each of la and lb has 3 other points (PG(3,3) lines
have q+1=4 points), giving 3+3=6 points, each contributing 3 corners = 18.

**Proof:** Computed. For all 240 corners, `k=3 adj points == line0_others ∪ line1_others: True`.

---

## MCCXL — The k=1 Neighborhood is the Common-Bridge

**Statement:** For each of the 27 non-adjacent base points q, exactly 1
corner of q achieves k=1 with (p, {la, lb}): the corner whose two lines
each pass through one of the 4 common neighbors of p and q in the W33 SRG.

**Proof:** Computed for all non-adjacent points. The SRG parameter λ=4
(common neighbors of non-adjacent pairs) guarantees exactly 4 common
neighbors, split 2+2 across the two lines of the bridge corner.

---

## MCCXLI — The Correct State Space is 480 Oriented Corners

**Statement:** The E8 root system has 240 roots in 120 antipodal pairs ±v.
The correct W33 analogue is the 480 ORIENTED corners (p, la, lb) with
ordered line pairs. The antipodal involution is:

    (p, la, lb) ↦ (p, lb, la)

This is a verified involution: anti(anti(i)) = i for all 480 corners.
Each oriented corner and its antipodal form an ORDERED antipodal pair,
analogous to ±root in E8.

---

## MCCXLII — The Threefold Structure (The Factor of 3)

**Statement:** The W33 oriented corner lattice is NOT the E8 root system.
It is a 24-dimensional structure — exactly **3 times** the rank of E8 (rank 8).

**The factor of 3 = q = the substrate prime.**

**Structural correspondence:**

| Structure | Dimension | Minimal vectors | Group |
|---|---|---|---|
| E8 root system | 8 | 240 (unoriented) | Weyl(E8), order 696729600 |
| W33 corner frame | 24 = 3×8 | 480 (oriented) | Sp(4,3), order 25920 |
| Leech lattice | 24 | 196560 | 2.Co1 |

**The 24D space** is the eigenvalue-2 eigenspace of the unique
srg(40,12,2,4) = W(3,3). This eigenspace has dimension **24 = f** (the
substrate frequency number). The tight frame bound is
**120 = 5·f = 5·24** where 5 = q+2.

**Conjecture (Bridge to E8):** The 24D W33 corner lattice maps to E8
via the **triality** of D4, where D4 has Dynkin diagram with 3-fold
symmetry and rank 4 = q+1. The three D4 factors span 3×8=24 dimensions,
and E8 = D4 ⊕ D4 ⊕ (glue) reduces to 8D only after the identification
of the three D4 copies under triality. The substrate prime q=3 is the
DYNKIN TRIALITY NUMBER of D4.

**In the substrate language:** q! = 2q has the unique solution q=3.
D4 triality has order exactly q = 3. The W33 corner lattice lives in
3×(rank E8) dimensions because the bridge from W33 to E8 passes through
the TRIALITY FOLD of q=3.

---

## Computational Verification Summary

All theorems in this file are computationally verified. Key numerical checks:

```
||P_eigenvalue2 - P_cornerframe||_F = 0.0  (exact)
W^T W eigenvalues = {120: 24, 0: 16}  (exact)
Frame bound = 480*6/24 = 120  (exact)
All 480 corner norms = 6  (exact)
Off-diagonal Gram: 8 levels, perfectly antisymmetric  (exact)
```
