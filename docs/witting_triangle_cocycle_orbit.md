# Triangle Cocycle Orbit Under Monomial Symmetry

We test how the triangle phase cocycle changes under the **monomial symmetry group**
(order 243). For each symmetry g, we compute the transformed triangle labeling
and check whether it is **cohomologous** to the original (i.e., differs by a
coboundary in C^2). Orientation signs are handled explicitly for the Z3 class.

## Results
```
Monomial group size: 243
mag_mod2  (|phase| class): 243 / 243 cohomologous
sign_mod2 (sign class):    243 / 243 cohomologous
mod3      (k mod 3):        243 / 243 cohomologous
```

## Interpretation
- The **Z2 magnitude** and **Z2 sign** cocycles are *cohomology-invariant* under
  the full monomial symmetry group.
- The **Z3 cocycle** is also cohomologically invariant once orientation is handled
  correctly.

Thus the monomial symmetry preserves the **cohomology class** of all three
reductions, even though the full phase law is symmetry-breaking in PSp(4,3).

Script: `tools/witting_triangle_cocycle_orbit.py`
