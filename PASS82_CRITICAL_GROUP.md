# Pass 82 — The critical group (sandpile group) separates the cospectral pair W(3,3) / Q(4,3)

**Status: PASS** — GAP script `w33_pass82_critical_group.g` → certificate
`w33_pass82_critical_group_out.txt`; witness `w33_pass82_critical_group.py` (6/6 checks); test
`tests/test_pass82_critical_group.py` (5/5). Self-contained on the committed Pass 73–77 spine.

## Context
Passes 76/77 proved W(3,3) and its dual GQ **Q(4,3)** are cospectral, **locally identical**, yet
non-isomorphic SRG(40,12,2,4) graphs — separated *geometrically* by the ovoid number
(α = 7 vs 10). This pass adds a purely **algebraic** separator and finds exactly where it lives.
(The parallel Pass 78–81 work covered the Terwilliger Wedderburn decomposition and the Spence
28-graph census; the **critical group / Laplacian Smith form is untouched** — 0 hits in the paper
and the whole Pass 73–81 spine.)

## Result
The critical group (sandpile group / graph Jacobian) K(G) = ℤⁿ / im(L), L = 12I − A, has order
equal to the number of spanning trees. From the Smith normal forms of the two Laplacians (GAP):

| graph | critical group K(G) | order | 2-Sylow | 5-Sylow |
|---|---|---|---|---|
| **W(3,3)** | (ℤ/10)⁸ ⊕ ℤ/40 ⊕ (ℤ/160)¹⁴ | 2⁸¹·5²³ | (ℤ/2)⁸⊕ℤ/8⊕(ℤ/32)¹⁴ | (ℤ/5)²³ |
| **Q(4,3)** | (ℤ/2)⁶ ⊕ (ℤ/10)⁸ ⊕ ℤ/40 ⊕ (ℤ/80)⁶ ⊕ (ℤ/160)⁸ | 2⁸¹·5²³ | (ℤ/2)¹⁴⊕ℤ/8⊕(ℤ/16)⁶⊕(ℤ/32)⁸ | (ℤ/5)²³ |

- **Same order** 2⁸¹·5²³ — forced, because cospectral ⇒ same Laplacian spectrum ⇒ same
  spanning-tree count (cross-checks the Pass 74 value 2⁸¹·5²³).
- **Same 5-Sylow** (ℤ/5)²³.
- **Different 2-Sylow** ⇒ the critical groups are **non-isomorphic**.

So the **critical group separates the cospectral, locally-identical pair**, and the separation is
located precisely in the **2-primary part** (the 5-part is blind to it). This is a new,
non-spectral, non-geometric invariant closing the same gap as the ovoid number — the algebraic
companion to Pass 77's geometric separator.

## Why it matters
Cospectrality guarantees identical Ihara/Bartholdi zeta, identical spanning-tree count, and here
even identical 5-Sylow of the sandpile group; the pair is nonetheless resolved by the 2-Sylow of
K(G). Together with the ovoid number (geometry) and the edge zeta (combinatorics), the sandpile
group (arithmetic of the Laplacian) is a third, independent way to "hear" the W/Q difference.

Note K(G) (from the Laplacian) is distinct from the adjacency Smith form 1¹⁶2⁸8¹⁵24 of Pass 77.

## Files
- `w33_pass82_critical_group.g`, `w33_pass82_critical_group_out.txt` — GAP script + certificate.
- `w33_pass82_critical_group.py`, `.json` — witness + certificate (6 checks).
- `tests/test_pass82_critical_group.py` — 5 assertions (reads the GAP cert; no live GAP needed).
