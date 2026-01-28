# Pair-Phase vs Symplectic Form (F3^4)

We tested whether the **pairwise Pancharatnam phase** between Witting rays can be
expressed by a low-degree algebraic rule in the F3^4 coordinates obtained from
the ray->F3 graph isomorphism.

## Setup
- Use the explicit ray->F3 mapping (graph isomorphism Witting orthogonality ↔ W(3,3)).
- For each **non-orthogonal** ray pair (540 pairs), compute:
  - `k` where phase = k * (pi/6) (k mod 12),
  - symplectic form `omega(x, y)` in F3 (values 1 or 2 for non-orth pairs).

## Distribution by omega
```
omega=1: {0: 15, 1: 54, 2: 3, 3: 42, 4: 6, 5: 10, 6: 3, 7: 19, 8: 6, 9: 5, 10: 3, 11: 71}
omega=2: {0: 33, 1: 91, 2: 9, 3: 13, 4: 6, 5: 17, 6: 9, 7: 8, 8: 6, 9: 30, 10: 9, 11: 72}
```
Both omega classes realize **the full phase lattice**; omega does not select a single phase
class, so the pairwise phase is **not** a simple function of omega alone.

## Bilinear search (mod 3)
We attempted to fit the phase class `k mod 3` as a **bilinear+linear** form over GF(3):

```
k mod 3 = x^T A y + a^T x + b^T y + c  (over GF(3))
```

**Result:** no solution exists (linear system inconsistent).

## Quadratic search (mod 3)
We then allowed a **full quadratic polynomial** in the 8 variables (x0..x3, y0..y3):

```
k mod 3 = sum_i ai vi + sum_i bi vi^2 + sum_{i<j} cij vi vj + c
```

**Result:** no solution exists. Even quadratic degree does **not** capture the mod-3 class.

## Conclusion
Pairwise phases are **more structured than omega**, but **not** reducible to a low-degree
algebraic rule in the symplectic coordinates. This supports the view that the pair-phase
structure is a **higher-order cocycle** (or requires additional discrete labels beyond F3^4).

Script: `tools/witting_pair_phase_symplectic.py`
Output: `artifacts/witting_pair_phase_symplectic.json`
