# BT984 — Edgewise fat-tower Laplacian convergence check

BT983 found the real R3 obstruction: the old barycentric refinement tower is
not shape-regular, so the Cheeger--Müller--Schrader / Dodziuk--Patodi / FEEC
theorems do not apply to that tower. BT984 turns the corrected route into an
executable spectral check on a seed whose continuum answer is known exactly.

## Numerical seed

Domain: unit square with Dirichlet boundary.

Continuum spectrum:

```text
lambda_{m,n} = pi^2 (m^2+n^2),  m,n >= 1
lambda_1 = 2 pi^2 = 19.739208802178716
```

Discretization: P1 finite-element / Whitney-0-form generalized eigenproblem

```text
K u = lambda M u
```

with exact element stiffness and mass matrices.

## Edgewise tower result

The edgewise/Freudenthal--Kuhn tower preserves the 45 degree minimum angle of
the square seed and drives the first eigenvalue toward the continuum value:

| level | vertices | triangles | min angle | lambda1 | rel. err |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2 | 25 | 32 | 45.0000 | 22.86577594 | 1.583937e-01 |
| 3 | 81 | 128 | 45.0000 | 20.50554490 | 3.882304e-02 |
| 4 | 289 | 512 | 45.0000 | 19.92978984 | 9.654948e-03 |
| 5 | 1089 | 2048 | 45.0000 | 19.78679229 | 2.410608e-03 |
| 6 | 4225 | 8192 | 45.0000 | 19.75110084 | 6.024575e-04 |

The leading error drops by roughly the expected quadratic scale under halving
mesh width, consistent with the Whitney/P1 FEM convergence route.

## Barycentric control

The barycentric tower is included only as a shape-regularity control. At these
small levels it can still produce plausible eigenvalues, but its simplex quality
collapses:

| level | vertices | triangles | min angle | lambda1 | rel. err |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 11 | 12 | 18.4349 | 22.96189057 | 1.632630e-01 |
| 2 | 45 | 72 | 8.9726 | 21.53826615 | 9.114131e-02 |
| 3 | 233 | 432 | 3.9302 | 20.71521651 | 4.944513e-02 |
| 4 | 1329 | 2592 | 1.8003 | 20.17322252 | 2.198739e-02 |

So BT984 does **not** claim that barycentric FEM instantly fails numerically.
The point is stricter: barycentric loses the uniform fatness hypothesis, hence
it is not a valid carrier for the named convergence theorems in R3.

## Reading

BT984 supplies the first computational witness for the corrected R3 route:

1. edgewise refinement remains fat/shape-regular;
2. Whitney-0/P1 low eigenvalues converge to the known continuum spectrum;
3. barycentric refinement remains the wrong theorem-carrier because its angles
   collapse, even when finite low-level spectra look benign.

This directly supports the BT983 reframe: R3 is no longer "try the old
barycentric tower harder"; it is "redo CP2_9/K3_16 on the edgewise tower, then
verify the heat-trace / Regge curvature estimates on that fat tower."

## Witnesses

```text
analysis/bt984_edgewise_laplacian_convergence.py
data/bt984_edgewise_laplacian_convergence.json
```
