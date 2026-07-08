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
W(E6) [51840]  ◁₆₇₂₀  GO⁺₈(2) [348364800]  ◁₁₃₆  Sp(8,2) [47377612800]
```

- index **6720 = 120·56** is precisely the ordered anisotropic-pair orbit of Pass 117;
- index **136 = 135 + 1** is the number of isotropic vectors including 0 (the O⁺₈(2) stabilizer
  index in Sp(8,2)).

All three groups act on the 40 / 120 / 135 / 255 point sets rooted in W(3,3).

## The prime shift 3 → 2

W(3,3) itself **is** a symplectic graph: the collinearity graph SRG(40,12,2,4) is **Sp(4,3)**, the
symplectic-polarity graph on the (3⁴−1)/(3−1) = 40 points of PG(3,3). So

> **W(3,3) = Sp(4,3) over F₃ generates, through its E₈/2E₈ glue, the symplectic graph Sp(8,2)
> over F₂.**

A symplectic-to-symplectic bridge across the prime shift **3 → 2** — the two Ducey "bad primes" of
r − s = 6 = 2·3 (Pass 97). The exceptional E₆/E₈ refinement (the quadratic form Q) is what turns the
featureless symplectic 255 into the arithmetically rich 135 + 120 split.

## Files
- `w33_pass124_symplectic_sp82.py`, `.json` — witness (10 checks).
- `tests/test_pass124_symplectic_sp82.py` — 5 assertions.
