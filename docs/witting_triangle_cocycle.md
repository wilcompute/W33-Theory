# Triangle Phase Cocycle Test

We treat the non-orthogonality graph on the 40 Witting rays as a 2-complex
(540 edges, 3240 triangles). We test whether triangle phase labels are **coboundaries**
of edge 1-cochains over GF(2) or GF(3).

## Setup
For each non-orth triangle (i,j,k), compute the Pancharatnam phase

```
phi_ijk = arg(<i|j><j|k><k|i>)
```

and quantize to `k` where phase = k * (pi/6).
We then solve linear systems for edge labels `x_e` so that:

```
 x_ij + x_jk + x_ki = t_ijk  (mod p)
```

### Labelings tested
- **Z2 magnitude class**: t=0 for |phase|=pi/6, t=1 for |phase|=pi/2
- **Z2 sign class**: t=0 for positive phase, t=1 for negative phase
- **Z3 class**: t = k mod 3

## Results
- **Z2 magnitude:** no solution (unsolvable)
- **Z2 sign:** no solution (unsolvable)
- **Z3 class:** no solution (unsolvable)

So none of these triangle phase labelings are coboundaries of edge labels. The
triangle phases define **nontrivial 2-cocycles** in these coefficient systems.

## Interpretation
This shows the triangle phase structure is not reducible to edge phase labels even
after collapsing to coarse Z2/Z3 classes. It behaves as a **genuine higher-order
cohomological invariant** of the non-orthogonality 2-complex.

Script: `tools/witting_triangle_cocycle.py`
Output: `artifacts/witting_triangle_cocycle.json`
