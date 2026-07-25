# Pass 115: LaTeX Draft — Section 4 (E6/E8 Confluence)

## File: PAPER_SECTION4_E6E8.tex (~8 pages)

### Theorems Included

| Theorem | Statement | Proof Method |
|---------|-----------|-----|
| T7 | Aut(W(3,3)) = W(E6), order 51840 | PSp(4,3) + exceptional isomorphism |
| T8 | disc(Lambda_C) = E8/2E8, O+(8,2) plus-type | Constr-A + coset analysis |
| T9 | 255 cosets = {1}+{135}+{120} (3 W(E6) orbits) | Orbit-stabilizer + GAP |
| T12 | Leech chain explicit via disc = glue group | Niemeier construction |

### Moonshine Chain (tikzcd)

W(3,3) --code--> C=[40,16,8] --Constr.A--> Lambda_C
                                               |
                                           disc = E8/2E8
                                               |
                                   E8 --phi--> E8/2E8 --glue--> Leech -> Monster

### Key Numbers Table

| Number | W(3,3) role | E6/E8 role |
|--------|------------|------------|
| 78 | Ihara amplitude | dim(E6) |
| 240 | 2 * edges | E8 root count |
| 45 | A_8 of C_2 | E6 tritangent planes |
| 135 | isotropic disc cosets | O+(8,2) polar graph |
| 120 | anisotropic disc cosets | E8 roots / {\u00b11} |
