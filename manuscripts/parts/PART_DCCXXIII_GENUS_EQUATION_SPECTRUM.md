# Part DCCXXIII — The Genus-Equation Spectrum and the W(3,3) Primitives

**Bridge:** `verify_dccxxiii_genus_equation_spectrum.py` — Verified
**Tests:** `tests/test_dccxxiii_genus_equation_spectrum.py` — 21/21 pass
**Data:** `data/dccxxiii_genus_equation_spectrum.json`

---

## 1. The two genus equations (Császár & Szilassi) are one equation

The Császár polyhedron (V = 7, every pair of vertices adjacent) and the
Szilassi polyhedron (F = 7, every pair of faces adjacent) are each other's
duals. Their existence equation — the Heawood–Ringel formula for the
genus of the complete graph K_n — is the same in both cases:

$$
\boxed{\;\; g(K_n) \;=\; \frac{(n-3)(n-4)}{12} \;=\; \frac{n^2 - 7\,n + 12}{12} \;\;}
$$

with n = V for Császár-type, n = F for Szilassi-type.

The numerator is **exactly the DCCXXII quadratic** x² − 7 x + 12 =
(x − q)(x − (q+1)), and the denominator is **exactly the DCCXXII codec
size** 12 = q(q+1). So the genus equation is

$$
\text{genus} \;=\; \frac{\text{DCCXXII quadratic at n}}{\text{DCCXXII codec}}.
$$

The whole toroidal-hinge structure of the W(3,3) program is hiding in
plain sight inside the K_n genus formula.

---

## 2. The integer-solution spectrum

Writing m = n − 4, the integer-genus condition is 12 | m(m+1). Since
gcd(m, m+1) = 1, by CRT this requires m mod 12 ∈ {0, 3, 8, 11}. The
first ten integer-spectrum entries:

| n | m mod 12 | g | identification |
|---:|---:|---:|---|
| 3 | 11 | 0 | trivial (K_3 = triangle, not a polyhedron) |
| **4** | 0 | **0** | **tetrahedron** (sphere; q + 1) |
| **7** | 3 | **1** | **Császár / Szilassi** (torus; q + (q+1)) |
| **12** | 8 | **6** | **K_12 hypothetical** (codec / W(3,3) valency; q(q+1)) |
| 15 | 11 | 11 | K_15 |
| 16 | 0 | 13 | K_16 |
| 19 | 3 | 20 | K_19 |
| 24 | 8 | 35 | K_24 (= 2 q!, multiplicity of eigenvalue 2 in W(3,3)) |
| **27** | 11 | **46** | **K_27** = q^q lines on a cubic surface = dim E₆ fund rep |
| 28 | 0 | 50 | K_28 |
| 31 | 3 | 63 | K_31 |
| 36 | 8 | 88 | K_36 |
| 39 | 11 | 105 | K_39 |
| **40** | 0 | **111** | **K_40** = K_v (W(3,3) point count) |

The residue pattern {0, 3, 8, 11} mod 12 is itself an interesting
fingerprint: 0 + 11 = 11, 3 + 8 = 11 — i.e., {0, 11} and {3, 8} are the
two complementary pairs summing to 11.

---

## 3. The W(3,3) primitives in the spectrum

| W(3,3) primitive | value | in spectrum? | g |
|---|---:|:---:|---:|
| q | 3 | ✓ | 0 |
| q + 1 | 4 | ✓ | 0 |
| q + (q+1) = Heawood | 7 | ✓ | 1 |
| q(q+1) = codec | 12 | ✓ | 6 |
| q^q | 27 | ✓ | 46 |
| v (W(3,3) points) | 40 | ✓ | 111 |
| mu eigen-multiplicity | 24 | ✓ | 35 |
| g eigen-multiplicity | 15 | ✓ | 11 |
| **q! = 2q** | **6** | **✗** | — |
| **q^(q+1) = H₁** | **81** | **✗** | — |

**Eight W(3,3) primitives sit ON the genus lattice. Only two sit OFF
it: q! = 6 and H₁ = 81.**

These two are exactly the *saturation* primitives — q! = |S₃| = |D₃| is
the order at the Master Equation saturation point itself, and H₁ = 81 is
the protected logical content of W(3,3). The lattice contains the
"graph" structure; the off-lattice values are the *information* structure.

This is a sharp **inside/outside dichotomy** for the W(3,3) integers.

---

## 4. The genus oscillator (linear arithmetic version)

Independent of the K_n genus formula, there is a *linear* genus oscillator
in the repo (CCCCCLXXIX, CCCCCLXXXI):

$$
v(h) \;=\; 4 + 3h, \qquad
E(h) \;=\; 6 + 15h, \qquad
F(h) \;=\; 4 + 10h,
$$

with Euler characteristic χ(h) = v − E + F = 2 − 2h.

| h | (V, E, F) | χ | genus | identification |
|---:|:---:|---:|---:|---|
| 0 | (4, 6, 4) | 2 | 0 | tetrahedron |
| 1 | (7, 21, 14) | 0 | 1 | Császár (V = 7, E = 21, F = 14) |
| 2 | (10, 36, 24) | −2 | 2 | hypothetical g = 2 |
| 3 | (13, 51, 34) | −4 | 3 | hypothetical g = 3 |

The increments are:

| Δv | ΔE | ΔF | Δχ | as mod 12 |
|---:|---:|---:|---:|---|
| 3 | 15 | 10 | −2 | (3, 3, −2 = q, q, −2) mod 12 |

So **each handle advances vertex/edge by q mod 12 and face by −2 mod 12**,
giving genus decrement Δχ = −2 = the residue of the local 12-clock.

The linear oscillator AGREES with the K_n spectrum at h = 0 (n = 4) and
h = 1 (n = 7) and DIVERGES afterwards: the oscillator's n = 10 at h = 2
is **not** in the K_n integer-genus spectrum, because (10−3)(10−4) = 42
and 42/12 = 3.5. The linear oscillator is a *triangulation* count, not
a complete-graph existence claim.

---

## 5. The three clocks at q = 3

| clock | modulus | origin | role |
|---|:---:|---|---|
| **mod-12** | 12 | codec = q(q+1) | local phase / K_n genus denominator / Z₁₂ = Z_q × Z_{q+1} / −1/ζ(−1) |
| **mod-7** | 7 | Heawood = q + (q+1) | toroidal color shell / Császár V / Szilassi F / Fano points/lines |
| **mod-10** | 10 | ΔF of the genus oscillator | face / decimal increment / base-10 of 1/7 (DCCXXII) |

The three clocks are coupled through (q, q+1) = (3, 4):

* 12 = q · (q+1)
* 7 = q + (q+1)
* 10 = ΔF = 2(q+1) + 2 = 2q + 4 (or equivalently 12 − 2)

So the same Master-Equation pair (3, 4) determines all three moduli.

---

## 6. Decisive identity

$$
\boxed{\;
g(K_n) = \frac{n^2 - 7\,n + 12}{12}
\;\Longrightarrow\;
\text{numerator} = \text{DCCXXII quadratic}, \;
\text{denominator} = \text{DCCXXII codec};
\;}
$$

and the integer spectrum

$$
\{n : 12 \mid (n-3)(n-4)\}
\;=\;
\{3, 4, 7, 12, 15, 16, 19, 24, 27, 28, 31, 36, 39, 40, 43, 48, \dots\}
$$

contains q, q+1, Heawood, codec, q^q, v of the W(3,3) program, but
*not* q! and *not* H₁.

---

## 7. Honest boundary

* **Existence**: only K₄ (tetrahedron) and K₇ (Császár) are known to be
  realised as concrete simplicial polyhedra. K_12, K_27, K_40 at integer
  genus exist as graph embeddings (Ringel–Youngs 1968) but are *not*
  known to be polyhedra.
* This part **identifies** the W(3,3) primitives sitting on the K_n
  graph-genus lattice; it does **not** construct K_12 or K_40 as
  polyhedra.
* The "three-clock" picture mod-12 / mod-7 / mod-10 is the consolidated
  reading of the CCCCCLXXIX / CCCCCLXXXI / CCCCCLXXXII chain — it does
  not derive new physics observables.

---

## 8. One-line summary

$$
\boxed{\;
\text{Csaszar/Szilassi genus equation} \;=\; \frac{\text{DCCXXII quadratic}}{\text{DCCXXII codec}}
\;=\; \frac{(n-q)(n-(q+1))}{q(q+1)};
\quad\text{spectrum contains q+1, 7, 12, 27, 40 but not q! or H}_1.
\;}
$$
