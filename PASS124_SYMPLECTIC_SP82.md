# Pass 124 — The symplectic capstone: Sp(8,2) unifies the two W(3,3) glue graphs

**Status: PASS** — witness `w33_pass124_symplectic_sp82.py` (10/10 checks), test
`tests/test_pass124_symplectic_sp82.py` (5/5). Self-contained (F₂⁸ quadratic geometry + numpy).

## The result

Passes 93 and 120 built *two* strongly regular graphs from the W(3,3) code-lattice glue group
(ℤ/2)⁸ = E₈/2E₈. Pass 124 shows they are the two halves of **one** graph.

Put the plus-type quadratic form Q on F₂⁸ (the E₈/2E₈ form) with polar (alternating) form
B(x,y) = Q(x+y)+Q(x)+Q(y). The **orthogonality graph on the 255 nonzero vectors** — join x∼y iff
B(x,y)=0 — is

> **SRG(255, 126, 61, 63)**, spectrum **{126¹, 7¹³⁵, (−9)¹¹⁹}**,

the (perp form of the) **symplectic graph Sp(8,2)**; its complement is the standard symplectic
graph SRG(255,128,64,64). Its automorphism group is **Sp(8,2)**, order **47 377 612 800**.

## The E₈ quadratic form splits it into the two W(3,3) graphs

The symplectic (alternating) form B alone cannot see the difference between the 255 vectors — it is
vertex-transitive under Sp(8,2). The **quadratic refinement Q** (the actual E₈ structure) cuts the
255 into two subconstituents:

| Q-value | vertices | induced graph | source |
|---|---|---|---|
| Q = 0 | 135 isotropic | **SRG(135,70,37,35)** | Pass 93 |
| Q = 1 | 120 anisotropic | **SRG(120,63,30,36)** | Pass 120 |

So the two W(3,3) glue graphs are *exactly* the O⁺₈(2)-subconstituents of Sp(8,2). 135 + 120 = 255.

## The symmetry tower locks together

```
W(E6)_pair [51840]  <_[6720]  O⁺₈(2):2 [348364800]  <_[136]  Sp(8,2) [47377612800]
```

- the first subgroup is specifically Pass 117's ordered-pair embedding, not
  Pass 125's nonconjugate code embedding;
- index **6720 = 120·56** is precisely the ordered anisotropic-pair orbit of Pass 117;
- index **136 = 135 + 1** is the number of isotropic vectors including 0 (the O⁺₈(2) stabilizer
  index in Sp(8,2)).

The symbols denote subgroup indices, not normal inclusions.

## The prime shift 3 → 2

W(3,3) is the symplectic-polarity graph on the
(3⁴−1)/(3−1) = 40 points of PG(3,3). Its full projective automorphism group is
**PGSp(4,3) ≅ W(E6)**; **Sp(4,3)** has the same order as \(W(E_6)\) but is not
the faithful 40-point group. So

> **The F₃ symplectic polar graph W(3,3) generates, through its E₈/2E₈ glue, the F₂ symplectic graph Sp(8,2)
> over F₂.**

A symplectic-to-symplectic bridge across the prime shift **3 → 2** — the two Ducey "bad primes" of
r − s = 6 = 2·3 (Pass 97). The exceptional E₆/E₈ refinement (the quadratic form Q) is what turns the
featureless symplectic 255 into the arithmetically rich 135 + 120 split.

## Files
- `w33_pass124_symplectic_sp82.py`, `.json` — witness (10 checks).
- `tests/test_pass124_symplectic_sp82.py` — 5 assertions.
