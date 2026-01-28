# Triangle Cocycle Orbit Under Monomial Symmetry

We test how the triangle phase cocycle changes under the **monomial symmetry group**
(order 243). For each symmetry g, we compute the transformed triangle labeling
and check whether it is **cohomologous** to the original (i.e., differs by a
coboundary in C^2).

## Results
```
Monomial group size: 243
mag_mod2  (|phase| class): 243 / 243 cohomologous
sign_mod2 (sign class):    243 / 243 cohomologous
mod3      (k mod 3):         3 / 243 cohomologous
```

## Interpretation
- The **Z2 magnitude** and **Z2 sign** cocycles are *cohomology-invariant* under
  the full monomial symmetry group.
- The **Z3 cocycle** is **not** invariant: only **3** symmetries preserve its
  cohomology class, while **240** move it to a distinct class.

This shows the Z3 triangle phase class is **highly symmetry-breaking**, while
its Z2 reductions are cohomologically rigid.

Script: `tools/witting_triangle_cocycle_orbit.py`
