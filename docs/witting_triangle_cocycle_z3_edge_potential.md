# Z3 Edge Potential for Triangle Phase Cocycle

We solve the oriented coboundary equation over GF(3):

```
  x_ij + x_jk - x_ik = t_ijk   (mod 3)
```

where `t_ijk = k mod 3` is the triangle phase class and `x_ij` is an edge potential
assigned to each **non-orthogonal** pair.

## Result
A solution exists (as expected from the corrected cocycle analysis). One canonical
solution (free variables set to zero) yields the following edge-label distribution:

```
Edge label distribution: {0: 150, 1: 195, 2: 195}
```

So the Z3 cocycle can be expressed as an **edge potential** on the 540 non‑orth edges.
The labels are not uniform; they split into a 150/195/195 pattern.

We also tabulated edge-label counts by support-size of the two rays (number of nonzero
components in each ray), written to the text output for inspection.

Script: `tools/witting_triangle_cocycle_z3_edge_potential.py`
Output: `docs/witting_triangle_cocycle_z3_edge_potential.txt`
