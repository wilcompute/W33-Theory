# Pass 94 — The mates separate again: code-lattice discriminant forms of W(3,3) vs Q(4,3)

**Status: PASS** — witness `w33_pass94_dual_lattice.py` (9/9 checks), test
`tests/test_pass94_dual_lattice.py` (5/5). Self-contained (GF(2) + Arf invariant via symplectic
reduction).

## Result
W(3,3) and Q(4,3) are cospectral non-isomorphic SRG(40,12,2,4) (the Sunada–Gassmann pair, Pass 84).
Their binary codes already differ; this pass pushes the separation into the Construction-A
**code-lattice discriminant forms**. For a doubly-even self-orthogonal code C=[40,k] the glue group
C⊥/C=(ℤ/2)^{40−2k} carries the discriminant quadratic form q(v)=wt(v)/2 mod 2, whose type is fixed by
its Arf invariant:

| graph | code | glue rank (40−2k) | disc form | nonzero isotropic |
|---|---|---|---|---|
| **W(3,3)** | [40,16,8] | **8** | **O⁺₈(2) = E₈/2E₈** (Pass 92) | 135 |
| **Q(4,3)** | [40,10,12] | **20** | **O⁺₂₀(2)** | 524799 |

Both plus-type (Arf=0), both doubly-even — but of **different rank (8 vs 20)**. The method is validated
by reproducing W's known O⁺₈(2) with exactly 135 isotropic vectors.

## Why it matters
The cospectral mates, which share adjacency spectrum and much of the arithmetic tower, are told apart
**cleanly at the lattice level**: the E₈ form falls out of **W only** (its maximal 2-rank code → minimal
glue), never out of Q. "Can you hear the shape?" — yes, through the code-lattice. Note the glue ranks
**8 + 20 = 28**, the size of the SRG(40,12,2,4) census (Pass 89).

## Files
`w33_pass94_dual_lattice.py`, `.json`; `tests/test_pass94_dual_lattice.py`.
