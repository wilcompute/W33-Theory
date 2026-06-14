# BT985 — Edgewise heat-trace convergence on the fat tower

BT984 checked individual Whitney-0/P1 eigenvalues. BT985 checks the actual
spectral-action observable on the same exact seed:

```text
H_N(t) = sum_{i <= N} exp(-t lambda_i).
```

The domain is the unit square with Dirichlet boundary, whose continuum spectrum
is known:

```text
lambda_{m,n} = pi^2(m^2+n^2),  m,n >= 1.
```

This is a flat/boundary seed, so BT985 is **not** an Einstein--Hilbert curvature
proof. It is the numerical spectral-side witness needed after BT983: on a
shape-regular edgewise tower, the heat trace itself stabilizes toward the
continuum value.

## Result

Using the first 80 FEM eigenvalues where available, the relative error against
the exact same-truncation heat trace drops as follows:

| level | vertices | triangles | min angle | eigs | err t=0.01 | err t=0.02 | err t=0.05 | err t=0.1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 289 | 512 | 45.0 | 80 | 8.7521e-02 | 5.4907e-02 | 3.2350e-02 | 2.7229e-02 |
| 5 | 1089 | 2048 | 45.0 | 80 | 2.5288e-02 | 1.4917e-02 | 8.3983e-03 | 6.9484e-03 |
| 6 | 4225 | 8192 | 45.0 | 80 | 6.6048e-03 | 3.8171e-03 | 2.1205e-03 | 1.7463e-03 |

At level 6:

```text
H_80(0.05) FEM   = 0.578753309700355
H_80(0.05) exact = 0.5799831778300211
relative error   = 0.0021205237956514024
```

## Reading

This is the spectral-action counterpart to BT984's eigenvalue convergence. The
fat edgewise tower keeps the shape-regularity hypothesis and makes the heat
trace converge numerically. That supports the BT983 claim that R3 should be
attacked by edgewise/fat refinement, not by pushing the non-shape-regular
barycentric tower harder.

## Witnesses

```text
analysis/bt985_edgewise_heat_trace_convergence.py
data/bt985_edgewise_heat_trace_convergence.json
```
