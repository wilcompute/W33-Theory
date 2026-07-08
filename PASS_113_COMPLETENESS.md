# Pass 113: {17,8,2,1} Completeness Analysis

## Main Finding

The {17,8,2,1} partition = **Smith 2-rank partition** = **F_2-rank(A) partition**
= **dim(C_2(G)) partition** (binary code dimension).

| dim(C_2(G)) | Count | 2-rank |
|-------------|-------|--------|
| 16 | 17 | 16 |
| 14 | 8 | 14 |
| 12 | 2 | 12 |
| 10 | 1 | 10 |

W(3,3) has dim(C_2) = 16, in the top rung.
Q(4,3) is in the same rung as W(3,3) (both rung of size 2) or different rung.

## Completeness

- **2-rank level**: {17,8,2,1} ladder is COMPLETE as a coarse separator.
- **Within each rung**: full Smith 2-Sylow structure may further split.
  W(3,3) and Q(4,3) have the same 2-rank but different Smith 2-Sylow.
- **Open**: Are all 17 top-rung graphs Smith-group-identical?
  Requires full GAP SNF computation for all 28 graphs.

## Paper Clarification Needed

Section 3 Theorem 3.2 should clarify that {17,8,2,1} is the 2-rank partition.
Within each class, the full Smith group is an additional refinement.
