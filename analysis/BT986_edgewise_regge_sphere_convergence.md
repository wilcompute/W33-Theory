# BT986 — Edgewise Regge curvature convergence proxy on the sphere

BT985 checked the spectral/heat-trace side on a flat seed. BT986 checks the
geometric/Regge side on a curved seed with known smooth target: the unit
2-sphere.

The construction starts from the octahedron, applies edgewise midpoint
subdivision, and projects new vertices back to $S^2$. For each level it computes
planar-chord triangle area, vertex angle deficits, and the 2D Regge scalar
curvature integral

```text
int R dA  ~=  2 * sum_v deficit(v).
```

For the unit sphere the smooth targets are

```text
area = 4*pi,
sum deficits = 4*pi,
int R dA = 8*pi.
```

## Result

| level | vertices | triangles | min angle | area rel. err | Regge scalar rel. err | max deficit |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 6 | 8 | 60.0000 | 4.4867e-01 | 2.8272e-16 | 2.0944 |
| 1 | 18 | 32 | 49.2105 | 1.7098e-01 | 7.0679e-16 | 0.7532 |
| 2 | 66 | 128 | 46.0906 | 4.8660e-02 | 9.8951e-16 | 0.2233 |
| 3 | 258 | 512 | 45.2752 | 1.2588e-02 | 5.7957e-15 | 0.0717 |
| 4 | 1026 | 2048 | 45.0690 | 3.1744e-03 | 1.6115e-14 | 0.0196 |
| 5 | 4098 | 8192 | 45.0173 | 7.9533e-04 | 8.0967e-14 | 0.0050 |
| 6 | 16386 | 32768 | 45.0043 | 1.9894e-04 | 2.8950e-13 | 0.0013 |

## Reading

The total Regge scalar integral is already exact to roundoff by discrete
Gauss--Bonnet on the closed sphere. The nontrivial convergence witnesses are:

1. the projected edgewise tower remains fat, with minimum angle tending to
   roughly $45^\circ$;
2. the chordal area converges to $4\pi$;
3. the local curvature concentration decays: max deficit
   $2.094395102393195 \to 0.001265738656563542$.

This gives the curved geometric counterpart to BT985. Together, BT985/BT986
make BT983 executable on model seeds: spectral heat trace and Regge curvature
both behave correctly on the fat tower.

## Witnesses

```text
analysis/bt986_edgewise_regge_sphere_convergence.py
data/bt986_edgewise_regge_sphere_convergence.json
```
