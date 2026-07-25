# Pass 76 — A cospectral, locally identical, non-isomorphic mate of W(3,3)

**Status: PASS** — witness `w33_pass76_cospectral_mates.py` (8/8 checks), test `tests/test_pass76_cospectral_mates.py` (5/5), paper compiles clean.

Closes the loop flagged after Pass 75: produce an **actual** second SRG(40,12,2,4) and separate it
from W(3,3) — and it turns out sharper than expected.

## Track 1 — Q(4,3), the dual GQ, is the mate (Q(4,3) / parabolic quadric: 0 hits in index.html)
The parabolic-quadric generalized quadrangle **Q(4,3)** in PG(4,3) (dual of the symplectic
W(3,3); the two GQs are non-isomorphic for q=3 odd) has a collinearity graph that is:
- **SRG(40,12,2,4)** and **cospectral** with W(3,3), but
- **non-isomorphic** to W(3,3) (verified by an exact networkx isomorphism test), and
- **locally identical**: every vertex neighborhood is **4K₃** and every μ-graph (the 4 common
  neighbors of a non-edge) is **4K₁** — in *both* graphs.

So at the real parameters (40,12,2,4), **neither the spectral (Ihara/Bartholdi) zeta nor any local
invariant** separates W(3,3) from Q(4,3) — only a global invariant (edge zeta / isomorphism) does.
This is strictly **sharper than the Shrikhande/rook** demonstrator of Pass 75, where a *local*
invariant (C₆ vs 2K₃ neighborhoods) already sufficed. Two generalized quadrangles that are
spectrally and locally indistinguishable, yet globally distinct.

## Track 2 — Godsil–McKay switching is rigid (GM switching: 0 hits)
W(3,3) admits **no size-4 Godsil–McKay switching set** (exhaustive over all C(40,4) 4-subsets):
the generalized quadrangle's uniform 4K₃ local structure makes it switching-rigid at that scale.
The cospectral mate therefore comes from the dual geometry Q(4,3), not from local switching.

## Track 3 — integral invariants (Smith/p-rank: ~0 hits)
- **det(A) = 12·2²⁴·(−4)¹⁵ = −3·2⁵⁶**.
- **2-rank = 16** (the binary code [40,16,8]), **3-rank = 39 = v−1**, **5-rank = 40** (A invertible mod 5).

## Files
- `w33_pass76_cospectral_mates.py`, `.json` — witness + certificate (8 checks).
- `tests/test_pass76_cospectral_mates.py` — 5 assertions (networkx-guarded for the iso claim).
- `w33_paper.tex` — remark (d) appended to the Zeta Frontier subsection.
