# Z6 Triangle Cocycle Test

We test the triangle phase class `k mod 6` and whether it is a coboundary in Z6.
Over Z6, solvability is equivalent to solvability mod 2 and mod 3 (CRT).
Orientation signs are handled explicitly.

## Results
```
Base solvable mod2: True
Base solvable mod3: True
Base solvable mod6: True
Orbit cohomology counts: {True: 243}
```

## Interpretation
The full `k mod 6` triangle class is **cohomologically trivial** (a coboundary)
and its cohomology class is **invariant** under the full monomial symmetry group.
This contrasts with the Z2 reductions (|phase| and sign), which remain nontrivial.

Script: `tools/witting_triangle_cocycle_z6.py`
