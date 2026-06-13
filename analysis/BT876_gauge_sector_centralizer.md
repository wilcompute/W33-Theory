# BT876 — The Gauge Sector Is the Centralizer of the Generation Symmetry: 12 = 8 + 3 + 1

**Status: PROVEN (machine-verified, `analysis/bt876_gauge_sector_centralizer.py`, data `data/bt876_gauge_sector_centralizer.json`)**

The capstone of the BT858–875 matter-sector arc, now turned to the gauge side.
The generation symmetry R is the long-root transvection (BT874); its
centralizer is the gauge group, and the 12 = k gauge bosons decompose as the
Standard-Model gauge group.

## The theorems

- **T1:** R is a 40-class transvection, so **|C(R)| = 25920/40 = 648 = the
  point parabolic Stab(p₀)** = 3^{1+2}:2A₄, with R central in it. The gauge
  group is literally *the centralizer of the generation symmetry* — what
  commutes with generation-cycling is exactly what fixes p₀.
- **T2 (unifies BT864/874/875):** C[40] under R has grade multiplicities
  **22 + 9 + 9** = BT864's transvection split, and it decomposes
  transparently: the **13 = 1+12 gauge perp-plane is fixed** (grade 0), the
  **27 matter shell splits 9+9+9**, so 22 = 13 (gauge) + 9 (diagonal matter)
  and 9 + 9 are the off-diagonal generations. BT864's "mystery split" is just
  gauge-plane + matter-diagonal.
- **T3/T4 (the gauge group):** C(R) acts transitively on the 12 gauge
  neighbors with permutation rank 3 (suborbits [1,2,9]). The valency-2
  orbital is the **4 lines through p₀** (4 disjoint triangles K₃, eigenvalues
  2×4, −1×8). C(R) acts on those 4 lines as **A₄**, so the rank-3
  multiplicity-free decomposition is

```text
C[12] = 1 ⊕ 3 ⊕ 8
      = U(1) hypercharge ⊕ SU(2) weak ⊕ SU(3) gluons
```

the **Standard-Model gauge group adjoint**: the 1 and 3 from the 4-line space
(A₄'s 4-point rep = 1+3), the 8 from the within-line traceless (gluon) octet.
12 = k = 8 + 3 + 1, derived as a module, not asserted.

## Reading

The substrate's 1+12+27 split is the full Standard-Model anatomy under the
generation symmetry R:

| sector | dim | under R (generation) | under C(R) (gauge) |
| --- | --- | --- | --- |
| self | 1 | fixed | the pole p₀ |
| gauge | 12 | **fixed** (R is gauge-blind) | **1 ⊕ 3 ⊕ 8 = U(1)×SU(2)×SU(3)** |
| matter | 27 | **9+9+9 graded** (3 generations) | the Heisenberg/Yukawa shell |

R fixes the gauge sector pointwise (generations carry identical gauge charges)
and grades the matter sector (three generations with the Yukawa texture) —
and the gauge group itself is C(R), decomposing as exactly SU(3)×SU(2)×U(1).
The Standard-Model gauge group and the three generations are the two
eigen-data of one long-root transvection on the W(3,3) point set.

## Open

- The hypercharge normalization (the U(1) trivial summand) and the weak-mixing
  angle from the 3-vs-8 relative structure — a substrate sin²θ_W check against
  Pillar's 3/13.
- Whether the A₄ on the 4 lines lifts to S₄ in PGSp (the parity/chirality
  doubling) — ties to BT869's polar-pair involution.
