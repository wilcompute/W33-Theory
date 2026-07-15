# W(3,3) Chiral Program — Honest Synthesis (Passes 158–315)

*Written at Pass 316, after Pass 311 measured the retraction rate and found the
program was accumulating claims faster than it consolidated them. This document
states what is **established**, what was **retracted**, and what is **open**. It
supersedes the framing of any earlier pass it contradicts.*

---

## 1. What is established

These survived the forced/chosen test (Pass 302) and the scope test (Pass 311).
Every one is **spectral, algebraic, or representation-theoretic** — basis-free by
construction.

### 1.1 The rank law (the strongest result)

For the F₂ line–point incidence matrix of W(3,q):

| | statement | status |
|---|---|---|
| **char-0 rank** | rank = v − g = ½(q²+1)(q+2) **for every q** | proved from SRG multiplicities (266) |
| **the sentinel** | g = ½q(q²+1) = multiplicity of the SRG eigenvalue −(q+1) | proved (266) |
| **odd q** | rank₂ = char-0 rank; **no 2-modular drop** | verified q = 3,5,7,9,11,13,17,25,27 (238/260/262/267/272/277) |
| **even q** | rank₂ = Tr(Bᵗ) + 1, B = [[4,2],[2,5]] | verified t = 1..5 (256) |
| **δ** | = # even invariant factors = # non-lifting kernel directions | two independent proofs (271/276) |
| **the "+1"** | = the all-ones vector ⟨j⟩; Tr(Bᵗ) = dim(C/⟨j⟩) | proved (270) |
| **the "+8"** | forced by Cayley–Hamilton: c(1 − Tr B + det B) = 1−9+16 | proved (261) |

**The mechanism**: the dichotomy is *defining vs cross characteristic*. Reduction
mod p is faithful iff p ∤ q; the drop needs a **proper** prime power (p | q, t ≥ 2)
— which is why δ(2) = 0. Characteristic 2 was never special (281: q=9 has a
3-rank drop of 26).

### 1.2 The CSS family

**[[(q+1)(q²+1), q²+1, q+1]]**, with k·d = n exactly, k ~ n^{2/3}, d ~ n^{1/3}
(224/229/239). q=3 gives the committed [[40,10,4]].

### 1.3 The physics selections (all branching arithmetic — Pass 306 verified)

- **225**: half-spinor 2^{(q²−1)/2} = 16 (one generation) **only at q=3** — unique.
- **227**: shadow rank ≤ 8 (max exceptional) **only at q=3** — unique.
- **230**: the E₆ cubic = {1·10·10, **16·16·10**} — magic *is* the GUT Yukawa.
- **231**: E₈ → E₆×SU(3) forces **three generations**.
- **235**: the democratic Yukawa has rank 1 → **one heavy generation**, no fit.

**225 and 227 are each independently sufficient to force q=3** (313).

### 1.4 The forced-field ladder (298)

| structure | field |
|---|---|
| tetrahedron K₄ | **Q** (equilateral) |
| Fano/Heawood clock | **Q(√2)** = √q, order 2 |
| **substrate W(3,3) Levi** | **Q(√6)** = √2q, q=3 |

Levi(PG(2,q)) → Q(√q); Levi(GQ(q,q)) → Q(√2q). Both verified directly.

---

## 2. What was retracted

**Five retractions, all from the metric/coordinate/over-read side. Zero from the
spectral side** (311).

| claim | fate | by |
|---|---|---|
| "√21 is absent from the substrate" (279/285) | **FALSE** | 286 |
| "√21 is the unique metric invariant of the Szilassi pole" (290/291) | **WITHDRAWN** | 293, 299 |
| "det(B) = \|F₂⁴\| = ambient" (275) | **REFUTED** (det(B₃)=76≠81) | 281 |
| "Koide's field can never come from the substrate" (300) | **OVER-READ** | 304 |
| "Aut(Császár)=AGL(1,7) is a genuine tie" (305) | **DEFLATED** (7 ∤ 51840) | 309 |
| "the TBM field is a third selection argument" (308) | **DECORATIVE** | 313 |

Plus two **tautologies** deflated: the "trace law" (287) and "42 = 2qΦ₆" (309).

### The three failure modes

1. **Coordinate artefacts** — refutable by another drawing (279/285, 290/291, 275).
2. **Correct results over-stated** — the pass is *right*, the framing exceeds the
   proof (300, 305, 308). Harder to catch.
3. **Unbuilt objects** — claims with no content at all (315). Worst: can't be
   refuted *or* used.

---

## 3. What is open

| question | status |
|---|---|
| **det(B_p)** — 16 at p=2, 76 at p=3, no closed form | **the last real gap** (287) |
| **rank₃W(3,27) = 8353?** | char-3 tower is a **2-point fit**; prediction untested → **CONJECTURE** (314) |
| **the even-q δ = 0,1,27,423** | closed form is Tr(Bᵗ)+1, but *why* B = [[4,2],[2,5]]? |
| **the clock↔machine coupling** | **asserted, never built** — girth/order/size all obstruct (310/315) |
| **Koide's 2/3** | sharply stated (a null ray of the S₃ Minkowski metric, 257) but **underived**; FN accommodates rather than derives (274) |
| **θ₂₃** | **generic** given the other angles (283) — may need no mechanism |

---

## 4. The operational prior (311)

1. **Trust spectral/algebraic/representation-theoretic claims by default.**
2. **Treat metric or basis-dependent claims as provisional** until a second
   realization or basis is checked.
3. **Treat any claim whose scope exceeds its proof as an over-read** — regardless
   of which side it came from.
4. **A claim that names no object is not a claim.** Name the map or state the
   open question.

On this arc's evidence, this prior would have caught all five retractions before
publication.

---

## 5. The honest headline

The program has **two theorems that stand** — the rank law (verified to q=27) and
the CSS family — plus a set of **representation-theoretic selections that
independently force q=3** and identify magic with the GUT Yukawa. Everything
geometric that was *metric* has been retracted. The substrate's own forced field
is **Q(√6)**, and the toroidal/Koide thread is closed on three independent
grounds.

*The single most valuable next computation is `det(B₅)` (~60 min, validated
implementation in Pass 314): it is spectral, so it lands on the side that does not
retract, and it is the last unexplained quantity in the rank story.*
