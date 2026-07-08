# Pass 86 — MacWilliams dual [40,24] of C₂(W): E₆ and E₈ in the code

**Status: PASS** — witness `w33_pass86_macwilliams_dual.py` (5/5 checks), test
`tests/test_pass86_macwilliams_dual.py` (5/5). Self-contained (Pass 85 enumerator + sympy).

C₂(W) = [40,16,8] is self-orthogonal (Pass 85), so C ⊆ C⊥ with **C⊥ = [40,24,6]**. The dual
dimension **24 = the gauge eigenspace multiplicity** (SRG eigenvalue r=2) and the moonshine/Leech
"24". The MacWilliams identity gives the dual enumerator *exactly* as a polynomial transform
`W_{C⊥}(x,y) = (1/2¹⁶)·W_C(x+y, x−y)` — no enumeration of the 2²⁴ dual codewords.

## Result
- **Dual [40,24,6]**, total 2²⁴ codewords ✓, self-orthogonal containment A_i(C) ≤ A_i(C⊥) ✓.
- Dual low weights: {0:1, **6:240**, 8:2205, 10:23760, 12:182560, …}.

## E₆ and E₈ appear naturally
- **C₂(W): 45 minimum-weight (weight-8) codewords = the 45 tritangent planes** of the cubic
  surface (**E₆**).
- **C⊥: 240 minimum-weight (weight-6) codewords = 240 = the E₈ root count = the edge count of
  W(3,3)** (**E₈**).

So the code / dual-code pair of W(3,3) carries both the E₆ (45 tritangent planes) and E₈ (240 roots)
orbit numbers as its minimum-weight geometry, with the moonshine 24 as the dual dimension — the
coding-theory face of the same exceptional structure the graph's spectrum and zeta encode.

## Files
- `w33_pass86_macwilliams_dual.py`, `.json` — witness + certificate (5 checks).
- `tests/test_pass86_macwilliams_dual.py` — 5 assertions.
