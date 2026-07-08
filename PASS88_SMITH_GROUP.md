# Pass 88 — Smith group, critical group, and the p-rank separator (a 2-adic transfer)

**Status: PASS** — GAP script `w33_pass88_smith_group.g` → certificate `w33_pass88_smith_group_out.txt`;
witness `w33_pass88_smith_group.py` (7/7 checks); test `tests/test_pass88_smith_group.py` (6/6).

A graph has two Smith-normal-form invariants: the **Smith group** coker(A) (cokernel of the
adjacency) and the **critical group** coker(L) (cokernel of the Laplacian = sandpile group). W(3,3)
and Q(4,3) are cospectral, so det(A) and det(L) agree — yet **both cokernels differ**, and so does
the most elementary invariant of all: the 2-rank of A.

## The separators
- **2-rank of A: 16 (W) vs 10 (Q)** ⇒ the binary codes are different: **C₂(W)=[40,16,8], C₂(Q)=[40,10,12]**.
  This is the *simplest* separator of the cospectral pair — and it corrects the Pass 84 "hearing
  hierarchy," which had listed only the ovoid number and critical group. The 2-rank is not spectral
  (Brouwer–van Eijl), so this is consistent with "the spectrum is deaf." 3-ranks both 39.
- **Smith group** coker(A): S(W) = (ℤ/2)⁸⊕(ℤ/8)¹⁵⊕ℤ/24, S(Q) = (ℤ/2)¹⁴⊕(ℤ/4)⁶⊕(ℤ/8)⁹⊕ℤ/24 —
  both order 3·2⁵⁶, different structure.
- **Critical group** coker(L): different (Pass 82), both order 2⁸¹·5²³.

## The 2-adic transfer (observation credited to Wil)
Aligning the two Smith diagonals (both sorted ascending):
```
positions:  1-10 | 11-16 | 17-24 | 25-30 | 31-39 | 40
A_W:        1    |  1    |  2    |  8    |  8    | 24
A_Q:        1    |  2    |  2    |  4    |  8    | 24
                    Q=2W    (agree)   W=2Q
```
The factor of 2 **switches sides across the central band of eight agreeing 2's**: 6 low-side entries
go 1→2 (Q gains a 2), and *symmetrically* 6 high-side entries go 8→4 (W keeps the 2 Q loses). The
net 2-adic valuation transfer is **0**, so the total valuation 56 is conserved — |S(W)| = |S(Q)| =
3·2⁵⁶ — while the group structure changes. This is precisely why two cospectral graphs (equal
determinant) can have different Smith groups: the 2-adic valuation is redistributed, not created or
destroyed, in a balanced 6-up/6-down reflection about the central 2-band.

## Grounding (internet)
- Brouwer–van Eijl, *p-rank of adjacency matrices of SRGs*, J. Alg. Combin. 1 (1992) 329–346.
- Haemers–Peeters–van Rijckevorsel, binary codes of strongly regular graphs.
- W(3) and Q(4,3) are graphs **#3 and #23** in Brouwer's SRG(40,12,2,4) database (the two GQ(3,3)
  point graphs).

## Files
- `w33_pass88_smith_group.g`, `.txt` — GAP Smith-normal-form certificate.
- `w33_pass88_smith_group.py`, `.json` — witness (7 checks; p-ranks + C₂(Q) computed directly).
- `tests/test_pass88_smith_group.py` — 6 assertions.
