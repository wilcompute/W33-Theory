# Pass 93 — A second SRG out of W(3,3): SRG(135,70,37,35) from the glue group

**Status: PASS** — witness `w33_pass93_srg135.py` (6/6 checks), test `tests/test_pass93_srg135.py`
(4/4). Self-contained (GF(2) linear algebra).

## Result
The 135 nonzero **isotropic** cosets of C₂(W)=[40,16,8] in C⊥ (the (ℤ/2)⁸ glue group of Pass 92),
joined when their Hamming inner product is 0 mod 2, form the strongly regular graph
**SRG(135,70,37,35)** — the **O⁺₈(2) polar graph** — with spectrum **{70¹, 7⁵⁰, (−5)⁸⁴}**.

| | vertices | degree | λ | μ | spectrum |
|---|---|---|---|---|---|
| built from W(3,3)'s glue | 135 | 70 | 37 | 35 | 70¹, 7⁵⁰, (−5)⁸⁴ |

## Why it matters
This is a **second** strongly regular graph falling directly out of W(3,3) — not from its adjacency,
but from the arithmetic of its binary code. The 40-point **E₆** generalized quadrangle W(3,3)
generates the 135-point **E₈** polar graph through its own code-lattice glue group: an explicit
**E₆ → E₈ bridge** inside a single finite object. (135 + 120 = 255 = 2⁸−1, the isotropic + anisotropic
split of Pass 92.)

## Grounding
E₈ lattice: the graph on the 135 isotropic vectors of E₈/2E₈, joined at inner product 0 mod 2, is
SRG(135,70,37,35) with O⁺₈(2) symmetry.

## Files
`w33_pass93_srg135.py`, `.json`; `tests/test_pass93_srg135.py`.
