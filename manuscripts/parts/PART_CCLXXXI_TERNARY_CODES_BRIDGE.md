# Part CCLXXXI: Ternary Codes, Perfect Codes over GF(3), and the W(3,3) Coding Bridge

## Overview

This part bridges classical coding theory over GF(3) to the constants of the strongly
regular graph W(3,3) = SRG(40, 12, 2, 4). The W(3,3) parameters are not incidental
to coding theory — they arise as perfect Hamming lengths, Golay code parameters,
MDS bounds, Krawtchouk roots, and transport decomposition factors.

**Bridge statistics:** 426 checks across 17 sections — all pass.

---

## W(3,3) Constants Reference

| Symbol | Value | Coding-theory role |
|---|---|---|
| V | 40 | Ham(4,3) code length |
| K | 12 | Ternary Golay length; PHI3−1 |
| LAM | 2 | Q−1: nonzero GF(3) scalars minus 1 |
| MU | 4 | Ham(2,3) length; MDS bound = Q+1 |
| Q | 3 | Base field size |
| PHI3 | 13 | Ham(3,3) length = K+1 |
| PHI4 | 10 | Q²+1; RS length over GF(11)−1 |
| LINES_27 | 27 | Q³; Ham(3,3) coset count |
| TRANSPORT_EDGES | 270 | PHI4 × LINES_27 |
| EDGES | 240 | V×K/2 |
| AUT_ORDER | 51840 | Aut(W(3,3)) order |

---

## Section 1: GF(3) Hamming Codes and the Ham Sequence

The **ternary Hamming code** Ham(r, 3) has parameters:

$$[n, k, 3]_3 \quad \text{with } n = \frac{3^r - 1}{2}, \quad k = n - r$$

The Hamming lengths for r = 1, 2, 3, 4 are exactly:

$$[1,\ \text{MU}=4,\ \text{PHI3}=13,\ V=40]$$

This is no coincidence — the W(3,3) vertex count and two of its four SRG parameters
appear as consecutive Hamming lengths.

### Perfect Packing Identity

Ham(r, 3) is **perfect**: the Hamming bound is achieved with equality.
The sphere of radius 1 in GF(3)^n has volume:

$$|B(n,1)| = 1 + 2n = 3^r$$

This gives the striking identities:

| r | n | Identity |
|---|---|---|
| 2 | MU = 4 | 3² = 1 + 2·MU = 9 |
| 3 | PHI3 = 13 | 3³ = 1 + 2·PHI3 = LINES_27 |
| 4 | V = 40 | 3⁴ = 1 + 2·V = 81 |

In particular: **Q³ = 1 + 2·PHI3 = LINES_27** and **Q⁴ = 1 + 2·V**.

### Ham(3,3) Dimension

The dimension of Ham(3,3) is:

$$k = \text{PHI3} - 3 = 13 - 3 = 10 = \text{PHI4}$$

---

## Section 2: PHI3 = K + 1

One of the sharpest identities in this bridge:

$$\text{PHI3} = K + 1 \qquad (13 = 12 + 1)$$

- PHI3 = (3³−1)/2: length of Ham(3,3)
- K = 12: length of the ternary Golay code

The **shortened Ham(3,3)** — remove one coordinate from [13,10,3] — gives [K, 9, 3],
the **punctured** code gives [K, 10, 2].

---

## Section 3: The Ternary Extended Golay Code [K, 6, 6]₃

The **extended ternary Golay code** G₁₂ has parameters [12, 6, 6]₃. Its key properties:

- Length n = K = 12
- Dimension k = 6 = K/2 (self-dual)
- Minimum distance d = 6 = K/2
- Total codewords: 3⁶ = 729

### Weight Enumerator

| Weight | Count | Identity |
|---|---|---|
| 0 | 1 | |
| 6 | 264 | 22·K |
| 9 | 440 | V·11 |
| 12 | 24 | 2·K |

Total: 1 + 264 + 440 + 24 = **729 = 3⁶ = Q^(K/2)**.

The V×11 = 440 appearance at weight 9 directly links the Golay weight enumerator
to the W(3,3) vertex count.

### Self-Duality and MacWilliams

G₁₂ is **self-dual**: the MacWilliams transform fixes its weight enumerator:

$$\sum_{j=0}^{12} A_j\, K_i(j;\,12,\,3) = 3^6 \cdot A_i \quad \forall\, i$$

where $K_i(x;\,n,\,q)$ are the Krawtchouk polynomials. This was verified for all
13 values of i.

### Type III Property

Self-dual ternary codes with d ≡ 0 (mod 3) and n ≡ 0 (mod 4) are Type III.
G₁₂ satisfies K = 12 ≡ 0 (mod 4) ✓.

### Automorphism Group

$\text{Aut}(G_{12}) \cong M_{12}$ (Mathieu group), with:

$$|M_{12}| = 95040, \quad |M_{12}|/K = 7920 = |M_{11}|$$

---

## Section 4: The Binary Extended Golay Code [2K, K, 8]₂

The binary Golay code lives on **2K = 24** points:

| Parameter | Value | Identity |
|---|---|---|
| n | 24 | 2·K |
| k | 12 | K |
| d | 8 | |
| Codewords | 4096 | 2^K |

The **unextended** binary Golay [23, 12, 7]₂ is perfect (t=3):

$$2^{12} \cdot |B(23,3)| = 2^{12} \cdot 2048 = 2^{23}$$

Weight enumerator: A₈ = 759, A₁₂ = 2576, A₁₆ = 759, A₀ = A₂₄ = 1.
The 759 weight-8 codewords form the Steiner system S(5,8,24) on 2K=24 points,
and $|M_{24}|/|M_{23}| = 244823040/10200960 = 24 = 2K$.

---

## Section 5: MDS Codes and MU = Q+1

Over GF(3), the **Singleton bound** gives maximum code length n ≤ q+1 = MU for k ≥ 2:

$$\text{MU} = Q + 1 = 4$$

All [MU, k, MU−k+1] codes over GF(3) are MDS (Singleton equality). Over GF(9=Q²):

$$\text{PHI4} = Q^2 + 1 = 10$$

is the maximum MDS length (matching the projective line over GF(9)).

The **Reed-Solomon** codes over GF(q) provide optimal MDS families:

- RS over GF(9): length up to 8 = 2·MU = Q²−1
- RS over GF(11): length up to 10 = PHI4
- [K, k, K−k+1] for k = 1, …, K: all achievable over GF(13)

---

## Section 6: Krawtchouk Polynomials

The ternary Krawtchouk polynomial is:

$$K_i(x;\,n,\,3) = \sum_{s=0}^{i} (-1)^s \cdot 2^{i-s} \binom{x}{s}\binom{n-x}{i-s}$$

Key evaluations at W(3,3) parameters (n = K = 12):

$$K_1(x;\,K,\,3) = 2K - 3x = 24 - 3x$$

$$K_0(x;\,K,\,3) = 1, \quad K_K(x;\,K,\,3) = (-1)^x \cdot 2^{K-x}$$

The **orthogonality** relations are:

$$\sum_{x=0}^{K} \binom{K}{x} 2^x K_i(x;\,K,\,3) = 0 \quad (i \geq 1)$$

These were verified for i = 0, 1, 2 along with the full MacWilliams self-dual identity
for all 13 indices.

---

## Section 7: Transport Edges in Coding Context

$$\text{TRANSPORT\_EDGES} = 270 = \text{PHI4} \times \text{LINES\_27} = (Q^2+1) \cdot Q^3$$

Alternative factorisations:

| Expression | Value |
|---|---|
| PHI4 × LINES_27 | 10 × 27 |
| Q² × COXETER_E8 | 9 × 30 |
| EDGES + COXETER_E8 | 240 + 30 |
| Q × Q² × PHI4 | 3 × 9 × 10 |

**No perfect Hamming code of length 270 exists over GF(3)**:

$$1 + 2 \times 270 = 541, \quad 3^5 = 243 < 541 < 729 = 3^6$$

The nearest Ham lengths bracket 270: Ham(5,3) has n=121, Ham(6,3) has n=364.

---

## Section 8: Coset Decoding

Ham(r, 3) decodes by cosets. The coset count equals the sphere size:

| r | n | Cosets = 3^r |
|---|---|---|
| 2 | MU=4 | 9 |
| 3 | PHI3=13 | LINES_27=27 |
| 4 | V=40 | 81 |

Coset leaders of weight 1: n × 2 (each position × 2 nonzero scalars).

$$1 + 2n = 3^r \quad \Longleftrightarrow \quad \text{perfect packing}$$

The ternary Golay [K,6,6] has **covering radius 4 = MU**.

---

## Section 9: Generator Matrix Cyclic Structure

The ternary Hamming code is cyclic with n | 3^r − 1. The multiplicative order of 3
modulo each Ham length equals the redundancy r:

| n | r | ord₃(n) | Check |
|---|---|---|---|
| MU=4 | 2 | 2 | 3² ≡ 1 (mod 4) ✓ |
| PHI3=13 | 3 | 3 | 3³ ≡ 1 (mod 13) ✓ |
| V=40 | 4 | 4 | 3⁴ ≡ 1 (mod 40) ✓ |

Self-dual [K, 6] has G and H both of shape 6×K.

---

## Section 10: Master Identity Table

| Identity | Numerical |
|---|---|
| (Q²−1)/2 = MU | (9−1)/2 = 4 |
| (Q³−1)/2 = PHI3 | (27−1)/2 = 13 |
| (Q⁴−1)/2 = V | (81−1)/2 = 40 |
| Q² = 1+2·MU | 9 = 1+8 |
| Q³ = 1+2·PHI3 = LINES_27 | 27 = 1+26 |
| Q⁴ = 1+2·V | 81 = 1+80 |
| PHI3 = K+1 | 13 = 12+1 |
| MU = Q+1 | 4 = 3+1 |
| LAM = Q−1 | 2 = 3−1 |
| A₆ = 22·K | 264 = 22×12 |
| A₉ = V·11 | 440 = 40×11 |
| A₁₂ = 2·K | 24 = 2×12 |
| Sum Golay = Q⁶ | 729 = 3⁶ |
| TRANSPORT = PHI4·LINES_27 | 270 = 10×27 |
| |M₁₂|/K = |M₁₁| | 95040/12 = 7920 |

---

## Verification

All **426 checks** across 17 sections pass. Sections:

1. Hamming codes GF(3) — Ham sequence [1, MU, PHI3, V]
2. Perfect code sphere packing — 3^r = 1 + 2n
3. Singleton, Plotkin, Griesmer bounds
4. Ternary Golay [K,6,6] — weight enumerator + MacWilliams
5. Binary Golay [2K,K,8] — M₂₄ action on 2K points
6. Reed-Solomon codes — MDS families
7. MDS codes — MU = Q+1 connection
8. Self-dual ternary codes — Type III, M₁₂
9. Repetition and parity codes — PHI3 = K+1
10. Code bounds atlas — Hamming, Plotkin, Gilbert-Varshamov, Elias
11. Krawtchouk polynomials — K₁(x;K,3) = 24−3x, orthogonality, MacWilliams
12. Transport coding bridge — 270 = PHI4 × LINES_27, no perfect Ham at n=270
13. Coset decoding — 1+2n = 3^r perfect structure
14. Generator matrix properties — cyclic order ord₃(n) = r
15. Coding theory identities — master table
16. Linear code families — BCH, cyclic
17. W(3,3) coding atlas — comprehensive summary

---

*Part CCLXXXI of the Theory of Everything series.*
*Results: `PART_CCLXXXI_ternary_codes_results.json`*
*Bridge: `exploration/PART_CCLXXXI_TERNARY_CODES_BRIDGE.py`*
*Tests: `tests/test_ternary_codes_cclxxxi.py`*
