# Z2 Cocycle Minimal Support (Heuristic)

We attempt to find sparse representatives of the two Z2 cocycles (magnitude and sign)
by adding coboundaries (edge columns of d1) and greedily reducing support using
bitset operations. Multiple random restarts were tried.

## Results
```
Initial mag support: 360
Initial sign support: 1620
Reduced mag support: 360
Reduced sign support: 360
```

The magnitude cocycle is already as sparse as possible in our heuristic and
matches exactly the number of |phase| = pi/2 triangles (360). The sign cocycle
can be reduced dramatically (1620 -> 360), suggesting its cohomology class has
a sparse representative of size 360 as well.

This indicates the Z2 cocycle classes may be pinned to a **360-triangle support**
subset, hinting at a rigid combinatorial substructure inside the 2-complex.

Script: `tools/witting_triangle_cocycle_z2_minimize.py`
Output: `docs/witting_triangle_cocycle_z2_minimize.txt`
