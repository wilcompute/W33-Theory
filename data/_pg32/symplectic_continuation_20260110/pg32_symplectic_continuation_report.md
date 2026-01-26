# PG(3,2) / symplectic doily continuation (2026-01-10)
Inputs: tomotope->projective quartets (15 rainbow completions) + Z3 phase-function model on sectors.
## Core facts
- The 'sum-of-phases' constraint holds for all 15 tomotope rainbow lines: m0+m1+m2+m3 ≡ 1 (mod 3).
- Coefficients (a0,a1,a2,a3) with f(u1,u2)=a0+a1 u1+a2 u2+a3 u1u2 satisfy a0-a1-a2+a3 ≡ 1 (mod 3).
- This defines an affine hyperplane with exactly 27 Z3 solutions.
- Mapping each solution to a 4-bit support vector b_i = 1[a_i≠0] gives exactly 15 nonzero vectors in F2^4, i.e. the 15 points of PG(3,2).

## Tomotope selection bias (measured)
- Tomotope realizes 15 rainbow lines but only 10 distinct PG points under the support map.
- The 5 missing PG points are: 0001, 0011, 0100, 0110, 1000.
- These 5 missing points are all **fiber_size=1** points (unique Z3 lift in the hyperplane), i.e. tomotope is avoiding a specific subset of the 'rigid' directions.

## Symplectic polarity: the doily W(2)
- Using the standard symplectic form ⟨x,y⟩ = x0 y1 + x1 y0 + x2 y3 + x3 y2 over F2, the 15 PG points determine exactly 15 totally-isotropic lines (the doily / GQ(2,2)).
- Tomotope coverage across these 15 doily lines splits evenly: 5 lines with 3/3 points hit, 5 lines with 2/3 hit, 5 lines with 1/3 hit.
- Fully hit doily lines (points listed as 4-bit vectors):
  - 0101 1010 1111
  - 0101 1011 1110
  - 0010 1100 1110
  - 0111 1001 1110
  - 0111 1010 1101

## Missing-point subgeometry
- The induced collinearity subgraph on missing points has edges:
  - 0011 -- 1000
  - 0011 -- 0100
  - 0100 -- 0110
  - 0001 -- 1000
  - 0001 -- 0100
  This forms a 4-cycle (0001-1000-0011-0100-0001) plus a pendant (0100-0110).
