# Pass 97 — The 5-adic mirror: why E₈ lives at p=2 and nowhere else

**Status: PASS** — witness `w33_pass97_five_adic_mirror.py` (11/11 checks), test
`tests/test_pass97_five_adic_mirror.py` (5/5). Self-contained (build_graph + GF(p) ranks + eigenvalue
arithmetic).

## The asymmetry
The critical group of W(3,3) is K = (ℤ/10)⁸ ⊕ ℤ/40 ⊕ (ℤ/160)¹⁴ (Pass 82), of order
**|K| = 2⁸¹ · 5²³** — exactly two primes. This pass explains why the two behave so differently, from
the SRG eigenvalue arithmetic (k,r,s)=(12,2,−4): **r−s=6, k−r=10, k−s=16.**

Ducey's theorem: the p-part of the critical/Smith group is parameter-determined **unless p | (r−s)**.
Here r−s = 6, so the only "bad" primes are 2 and 3.

| prime | Ducey | k−r=10 | k−s=16 | result |
|---|---|---|---|---|
| **2** | bad (2\|6) | ✓ | ✓ | rich, 2⁸¹; code-lattice disc form **E₈/2E₈ = O⁺₈(2)** (Pass 92) |
| **3** | bad (3\|6) | ✗ | ✗ | **trivial** — necessary ≠ sufficient |
| **5** | good (5∤6) | 5‖10 | ✗ | **(ℤ/5)^{f−1} = (ℤ/5)²³**, f=mult(r)=24 — elementary by theorem |

## Mechanism (the missing 1)
Mod 5 the valency **k=12 collides with r=2** (12≡2), so A is **not diagonalizable** mod 5:
nullity(A−2I)=24 but nullity((A−2I)²)=25 — a single **size-2 Jordan block** couples the all-ones
vector to the r-eigenspace. With the spanning-tree normalization 1/40 (one factor of 5), (ℤ/5)²⁴
becomes (ℤ/5)²³.

## Reading
The exceptional **E₈ structure of W(3,3) is intrinsically a p=2 phenomenon**: it needs both
2 | (r−s) (a bad prime, leaving room for non-parameter-determined structure) **and** the doubly-even
self-orthogonal binary code. No odd prime qualifies — 3 is bad but empty, 5 is good hence elementary.
**There is no "E₈ at 5,"** and that asymmetry is exactly why E₈ appears at 2 alone.

## Files
`w33_pass97_five_adic_mirror.py`, `.json`; `tests/test_pass97_five_adic_mirror.py`.
