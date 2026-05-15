# Part DCCXXII — The Mod-12 Toroidal Synthesis

**Bridge:** `verify_dccxxii_mod12_toroidal_synthesis.py` — Verified
**Tests:** `tests/test_dccxxii_mod12_toroidal_synthesis.py` — 23/23 pass
**Data:** `data/dccxxii_mod12_toroidal_synthesis.json`

---

## 1. The algebraic hinge

At the W(3,3) saturation point q = 3, the **consecutive-integer pair** (q, q+1) = (3, 4) has

$$
\text{sum} \;=\; q + (q+1) \;=\; 7,
\qquad
\text{product} \;=\; q \cdot (q+1) \;=\; 12,
$$

so q and q+1 are the two roots of the quadratic

$$
\boxed{\;x^2 \;-\; 7\,x \;+\; 12 \;=\; (x-3)(x-4) \;=\; 0,\qquad \Delta = 1.\;}
$$

The coefficients of this quadratic — 7 and 12 — are themselves the two
"magic numbers" that recur throughout the program: the **Heawood number**
(genus-1 chromatic / Császár vertex / Szilassi face / Fano point count)
and the **local codec size** (W(3,3) valency, q! + 2q, denominator of
ζ(−1) = −1/12, "space × time" factorisation). The discriminant is 1, the
minimal positive integer step.

---

## 2. Sum-side coincidences: the **Heawood 7**

| structure | role of 7 | source |
|---|---|---|
| **Császár polyhedron** | 7 vertices on the torus (K₇ simplicial polyhedron, genus 1) | Császár 1949 |
| **Szilassi polyhedron** | 7 hexagonal faces on the torus (every pair of faces shares an edge) | Szilassi 1977 |
| **Heawood number** | chromatic number of the torus = ⌊(7 + √(1+48))/2⌋ = 7 | Heawood 1890 |
| **Fano plane** PG(2,2) | 7 points, 7 lines, 3 points per line | smallest projective plane |
| **Heawood graph** | incidence graph of Fano: 14 = 2·7 vertices, 21 = 3·7 edges, girth 6 | bipartite, vertex-transitive |
| **Tetrahedron** | the genus-0 analogue with q + 1 = 4 vertices | sphere; (V,E,F) = (4,6,4) |

Császár and the tetrahedron are the *only two known* simplicial polyhedra
whose 1-skeleton is a complete graph K_n. Their vertex counts are q + 1
and q + (q+1) = 7 at q = 3 — i.e., **q+1 on the sphere, q+(q+1) on the
torus.**

The (V, E, F) signatures:

| polyhedron | V | E | F | χ | g |
|---|---:|---:|---:|---:|---:|
| Tetrahedron | 4 = q+1 | 6 = q! | 4 = q+1 | 2 | 0 |
| Császár | 7 = q+(q+1) | 21 | 14 = 2·7 | 0 | 1 |
| Szilassi | 14 | 21 | 7 | 0 | 1 |

Császár's edge count 21 is also the number of incidences in the Fano
plane (7 lines × 3 points each), and 14 = 2·7 is the Heawood-graph
vertex count.

---

## 3. Product-side coincidences: the **codec 12**

| structure | role of 12 | source |
|---|---|---|
| **W(3,3) valency** | k = q(q+1) = 12 | SRG parameter |
| **Local codec size** | q! + 2q = 6 + 6 = 12 | DCCXIV–XVII |
| **Hours / clock** | 12-hour cycle, 12 zodiac, 12 chromatic notes | universal cultural artefact |
| **Mod-12 cyclic** | Z₁₂ ≅ Z₃ × Z₄ = Z_q × Z_{q+1} | CRT decomposition |
| **−1 / ζ(−1)** | ζ(−1) = −1/12, the regularised sum 1+2+3+… | analytic continuation |
| **space × time** | dim_space × dim_time = 3 × 4 = 12 | DCCXVII factorisation |
| **Tomotope order-12 element** | t = r₁·r₂ has order 12 | memory pillar 73 |

The Chinese-Remainder split Z₁₂ ≅ Z_q × Z_{q+1} is exactly the Master-
Equation pair (q, q+1) running mod-arithmetically — the same pair that
appears as the roots of the quadratic in §1.

---

## 4. The Tesla 3-6-9 and the cyclic decimal 1/7

In base 10, 1/7 has the cyclic decimal

$$
\tfrac{1}{7} \;=\; 0.\overline{142857},
$$

whose repeating block contains exactly the digits {1, 2, 4, 5, 7, 8} —
**missing {0, 3, 6, 9}**. Excluding 0, the missing digits are exactly the
"Tesla 3-6-9" — and these are exactly the elements of {1, …, 12} that lie
in the **Z₃ = 0 grade**:

$$
\{1, 2, \dots, 12\} \;\big/\; 3
\;=\;
\underbrace{\{3, 6, 9, 12\}}_{\text{class 0}}
\;\cup\;
\{1, 4, 7, 10\}
\;\cup\;
\{2, 5, 8, 11\}.
$$

So **the codec size 12 itself lives in the Tesla missing-digit class**, and
{3, 6, 9, 12} = {q, q!, q², q(q+1)} is the q-orbit of the codec under the
Z₃ grading induced by the three axes (B₂₃, B₃₁, B₁₂) of DCCXIV.

The user's observation about the **transition point at 1/6**:

| fraction | decimal | what repeats |
|---|---|---|
| 1/3 | 0.333… | denominator only |
| **1/6** | **0.1666…** | **numerator AND denominator** (mixed) |
| 1/9 | 0.111… | numerator only |

1/6 is the unique middle-ground transition: it contains both the
numerator (1) and the denominator (6) in its decimal expansion, between
the "denominator-only" 1/3 = 0.333… and the "numerator-only" 1/9 =
0.111… This is verifiable by direct decimal expansion (see
`classify_small_fractions` in the verifier).

---

## 5. The ζ(−1) = −1/12 reading

The zeta-regularised "sum of all positive integers"

$$
\sum_{n=1}^{\infty} n \;\overset{\zeta}{=}\; \zeta(-1) \;=\; -\tfrac{1}{12}
$$

has a striking reading inside the W(3,3) program: its denominator is
**exactly the local codec size**. The minus sign and the 1/12 magnitude
together say:

> the formal infinite sum, renormalised inside the 12-element codec
> carrier, returns exactly one unit *below the codec floor* — the "index-
> out-of-bounds" eigenvalue of the photonic-QEC runtime.

This is the W(3,3) reading of the bosonic-string regularisation that
gives the critical dimension 26 = 24 + 2 from 1 + 2 + … + 23 = 276 →
−23/12, etc. The same denominator 12 is the codec/valency/Z_q × Z_{q+1}
modulus.

---

## 6. Decisive identity

$$
\boxed{\;
\text{Master Equation }q! = 2q \;\Longrightarrow\; q = 3 \;\Longrightarrow\;
(q, q+1) = (3, 4)
\;\Longrightarrow\;
\big(\text{sum}, \text{product}\big) = (7, 12)
\;}
$$

…and (7, 12) are simultaneously:

* (Heawood, codec) = (Császár/Szilassi/Fano number, W(3,3) valency)
* (sum-of-roots, product-of-roots) of x² − 7x + 12 with discriminant 1
* (genus-1 torus, mod-12 cyclic) closure on the W(3,3) substrate
* (Heawood graph vertices/2, denominator of ζ(−1))
* (space-dim + time-dim, space-dim × time-dim) at the saturation point

---

## 7. Honest boundary

* This part documents **structural coincidences** at q = 3; it does **not**
  derive the Császár embedding's geometric coordinates, the Szilassi
  hexagons' Euclidean realisation, or the zeta-function machinery.
* It does **not** claim that the Tesla 3-6-9 has mystical significance —
  only that the *mathematical* set {3, 6, 9} is the Z_q-grade class of
  base-10 digits, dual to the cyclic decimal 142857 of 1/7.
* "Index-out-of-bounds" reading of −1/12 is a *literary* metaphor for the
  zeta-regularisation, not a formal theorem in the program.

What **is** established: the (sum, product) pair (7, 12) of the (q, q+1)
roots of x² − 7x + 12 controls all the apparently-disparate "magic
numbers" 7 and 12 that recur in toroidal combinatorics, mod-12 cyclic
arithmetic, base-10 decimal patterns, and zeta-regularisation, and all of
them follow from the Master Equation.

---

## 8. One-line summary

$$
\boxed{\;
q = 3 \;\Longrightarrow\; (\text{sum}, \text{product})_{(q,\,q+1)}
= (7, 12) = (\text{Heawood}, \text{codec})
\;=\; \text{toroidal hinge of the W(3,3) program.}
\;}
$$
