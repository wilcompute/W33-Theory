# Pass 89 — The arithmetic census of the 28 SRG(40,12,2,4) graphs, and a graded 2-adic ladder

**Status: PASS** — GAP census `w33_pass89_census.g` (Smith normal forms of A and L for all 28,
over McKay's graph6 list) → `w33_pass89_census_out.txt`; witness `w33_pass89_census.py` (11/11
checks); test `tests/test_pass89_census.py` (7/7).

Pass 88 separated the two GQ(3,3) graphs by their Smith group, critical group, and 2-rank. This
pass computes all three for **all 28** and reads off the census.

## The census
- **Exactly 4 distinct Smith groups and 4 distinct critical groups**, both with distribution
  **{17, 8, 2, 1}** — and it coincides graph-for-graph with the **2-rank partition** {16:17, 14:8,
  12:2, 10:1}. So the 2-rank, the Smith group, and the critical group all induce the *same* 4-class
  partition of the 28.
- **Every critical group has 5-Sylow (ℤ/5)²³** — constant across the family. This is **Ducey's
  theorem**: the Sylow-p subgroup of the critical group of an SRG is determined by (v,k,λ,μ) unless
  p | (r−s); here r−s = 6 = 2·3, so only p=2 is "difficult," and indeed *all* the variation is 2-adic.
- **The two generalized quadrangles sit at opposite extremes:** the symplectic **W(3,3) is generic**
  (2-rank 16, shared with 16 others); its dual, the parabolic quadric **Q(4,3), is the unique
  extreme** (2-rank 10, alone).

## The graded 2-adic transfer ladder (Wil's two observations)
Ordering the 4 classes by 2-rank (16→14→12→10), both the Smith and critical group counts run
**arithmetic progressions** — each rung is the Pass-88 balanced 2-adic transfer applied one more
time (entries transferred each side: 0, 2, 4, 6; Q's 6 matches the Pass-88 W↔Q transfer):

| 2-rank | Smith ℤ/2 | ℤ/4 | ℤ/8 | | Critical ℤ/2 | ℤ/10 | ℤ/40 | ℤ/80 | ℤ/160 |
|---|---|---|---|---|---|---|---|---|---|
| 16 (W) | 8 | 0 | 15 | | 0 | 8 | 1 | 0 | 14 |
| 14 | 10 | 2 | 13 | | 2 | 8 | 1 | 2 | 12 |
| 12 | 12 | 4 | 11 | | 4 | 8 | 1 | 4 | 10 |
| 10 (Q) | 14 | 6 | 9 | | 6 | 8 | 1 | 6 | 8 |

- **Smith:** ℤ/2 **+2**, ℤ/4 **+2**, ℤ/8 **−2** per rung (ℤ/24 constant) — the "+2 between 8 and 10,
  −2 between 15 and 13" observation.
- **Critical:** ℤ/2 **+2**, ℤ/80 **+2**, ℤ/160 **−2** per rung, while **ℤ/10 (count 8) and ℤ/40
  (count 1) stay constant** — the 5-carrying, parameter-determined part (10=2·5, 40=8·5, 80=16·5,
  160=32·5). Because L ≡ A mod 2 but the 5 multiplies through the fixed eigenvalue part, the critical
  ladder is the Smith ladder with a factor of 5 on the invariant part.

So the whole family of 28 is **stratified into 4 rungs of a purely 2-adic transfer ladder**, with
W(3,3) at the bottom and Q(4,3) at the top — a clean arithmetic organization of Spence's 28 graphs.

## Grounding (internet)
Brouwer–van Eijl (p-ranks of SRGs), Ducey (critical group from SRG parameters, arXiv 1910.07686),
Peter Sin (Smith normal forms of SRGs), Spence (the 28 graphs).

## Files
- `w33_pass89_census.g`, `w33_pass89_matrices.g`, `w33_pass89_census_out.txt` — GAP inputs + certificate.
- `w33_pass89_census.py`, `.json` — witness (11 checks).
- `tests/test_pass89_census.py` — 7 assertions.
