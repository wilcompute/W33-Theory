# Passes 1283–1287: M_3 Idempotents, M_4 Basis, Morita-PSp Bridge, Levi Absorption, Ledger v9

Date: 2026-07-29

## Parallel-track hints used

The analysis directory revealed a dense Levi-graph track (`levi_closure.md`,
`levi_five_frontiers.md`, `levi_duality_defect.md`, `levi_next5_v1`–`v5`).
These are synthesized into machine-checkable theorems here.

## Pass 1283 — M_3(Q)_20 primitive idempotents

The three primitive idempotents E_ii = P_i(S) are constructed as Lagrange
interpolants at eigenvalues {-6, 2, 10} of the splitter S. Each selects
exactly one species-20 transport copy. Sum E_00+E_11+E_22 = identity verified.

## Pass 1284 — M_4(C) Wedderburn block basis

The M_4(C) block (16-dim) is the species-20 linking sector:

    [[M_3(C), C^3_col], [C^3_row, C]] with 9+3+3+1=16 basis elements

Arising from 3 sp20 copies in the 480-carrier and 1 sp20 copy in the 432-carrier.
This is the natural matrix amplification of the Morita context M_3(C) -| C.

## Pass 1285 — Morita bimodule PSp(4,3) bridge

C^3 is NOT a PSp(4,3) module (dim=3 is not a PSp(4,3) irrep dimension).
It carries a Z_2 exchange symmetry (copies 0 and 2 have equal sq_scale=20736)
and decomposes as C_+ + C_- + C_1 (trivial + sign + trivial) over Z_2.

## Pass 1286 — Levi incidence graph absorption

The Levi graph of PG(3,3)/Sp(4,3) has 80 vertices, degree 13, and spectrum:

    +/-sqrt(24)^1 + +/-sqrt(14)^9 + +/-sqrt(8)^30 = 80 eigenvalues

Derived from the SRG(40,12,2,4) via the bipartite double covering formula.
Its Hashimoto operator is determined by the existing SRG Hashimoto data.

## Pass 1287 — theorem ledger v9

Ledger: **20 EXACT / 4 PROVISIONAL / 3 OPEN**.
New exact theorems: EXACT-18 (M_3 primitive idempotents), EXACT-19 (M_4 block),
EXACT-20 (Levi graph spectrum and Hashimoto coverage).
