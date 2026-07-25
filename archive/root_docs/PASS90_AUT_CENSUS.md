# Pass 90 — Automorphism census of the 28: is the arithmetic ladder a symmetry ladder?

**Status: PASS** — GAP/GRAPE `w33_pass90_aut.g` → `w33_pass90_aut_out.txt`; witness
`w33_pass90_aut.py` (8/8 checks); test `tests/test_pass90_aut.py` (5/5).

Pass 89 stratified the 28 SRG(40,12,2,4) graphs into a 4-rung 2-adic ladder (2-ranks 16→14→12→10).
This pass computes |Aut| for all 28 (GRAPE/nauty) and asks whether that ladder is also a symmetry
ladder.

## |Aut| by rung
| 2-rank | #graphs | max |Aut| | mean | median |
|---|---|---|---|---|
| 16 (generic) | 17 | **51840** | 3125.6 | **9** |
| 14 | 8 | 144 | 43.5 | **48** |
| 12 | 2 | 384 | 288.0 | **384** |
| 10 (extreme) | 1 | **51840** | 51840 | 51840 |

## Findings
- **The two generalized quadrangles have |Aut| = 51840 = |Sp(4,3)| = |W(E₆)|**, dwarfing all 26
  others (next largest 648). They are graphs **#27 = Q(4,3)** and **#28 = W(3,3)** — dual GQs with
  isomorphic collineation groups. The E₆ thread (45 tritangent planes, dim E₆ = 78, …) reappears as
  the *symmetry* of the two extremal graphs.
- **Off the two GQ bookends, median symmetry rises as the 2-rank falls: 9 → 48 → 384** (ranks
  16 → 14 → 12). So the arithmetic ladder *is* broadly a symmetry ladder.
- **The anomaly is W(3,3):** it attains the maximal 51840 yet sits at the *generic* bottom rung
  (2-rank 16), hidden among 16 low-symmetry graphs (median |Aut| 9). Its dual Q(4,3) sits *alone* at
  the top rung (2-rank 10). The two dual GQs bookend the ladder — W at the bottom (generic 2-rank,
  maximal symmetry), Q at the top (extreme 2-rank, maximal symmetry).
- **Family invariant (Siegel mass):** Σ_{28} 1/|Aut| = **189457/51840**, so the number of *labelled*
  SRG(40,12,2,4) graphs is (189457/51840)·40!.

So the 2-adic arithmetic of the family and its symmetry are the same organizing principle, with the
symplectic GQ W(3,3) as the single high-symmetry graph hiding at the generic rung and its dual Q(4,3)
crowning the extreme — a clean picture of the whole SRG(40,12,2,4) family.

## Files
- `w33_pass90_aut.g`, `w33_pass90_aut_out.txt` — GRAPE certificate.
- `w33_pass90_aut.py`, `.json` — witness (8 checks).
- `tests/test_pass90_aut.py` — 5 assertions.
