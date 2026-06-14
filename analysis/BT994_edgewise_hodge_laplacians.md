# BT994 — Edgewise Hodge/Laplacian operators on CP2_9/K3_16 level 1

BT994 extends BT992 from boundary ranks to sparse Hodge-Laplacian certificates.
For each degree,

```text
L_k = d_k^T d_k + d_{k+1} d_{k+1}^T.
```

The exact harmonic dimensions follow from

```text
dim ker L_k = dim C_k - rank d_k - rank d_{k+1}.
```

## CP2_9 level 1

```text
chain dimensions    = [45, 414, 1236, 1440, 576]
boundary ranks      = [44, 370, 865, 575]
Laplacian nnz       = [873, 9306, 15846, 12006, 3456]
harmonic dimensions = [1, 0, 1, 0, 1]
total harmonic      = 3
```

A local low-spectrum pilot finds the expected near-zero modes in degrees 0, 2,
and 4.

## K3_16 level 1

```text
chain dimensions    = [136, 2640, 9440, 11520, 4608]
boundary ranks      = [135, 2505, 6913, 4607]
Laplacian nnz       = [5416, 165916, 182368, 110870, 27648]
harmonic dimensions = [1, 0, 22, 0, 1]
total harmonic      = 24
```

The middle-degree K3_16 Laplacian is large enough that stochastic/Chebyshev heat
estimators are the right next spectral tool; naive middle-degree eigensolve is
not the right production path.

## Witnesses

```text
analysis/bt994_edgewise_hodge_laplacians.py
data/bt994_edgewise_hodge_laplacians.json
```
