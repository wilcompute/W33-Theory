# BT995 — Edgewise heat-trace samples on real CP2/K3 seeds

BT995 moves the heat-trace check from square/sphere proxies to the real level-1
edgewise CP2_9 and K3_16 complexes.

For every finite Hodge complex, McKean--Singer gives the exact identity

```text
sum_k (-1)^k Tr(exp(-t L_k)) = chi
```

for all `t`. The large-time heat trace limit is the total harmonic dimension.

## Exact samples

| seed | chi | sampled supertrace t=0.01 | t=0.05 | t=0.1 | t=1.0 | large-time total heat limit |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CP2_9 | 3 | 3 | 3 | 3 | 3 | 3 |
| K3_16 | 24 | 24 | 24 | 24 | 24 | 24 |

Degreewise large-time limits:

```text
CP2_9: [1, 0, 1, 0, 1]
K3_16: [1, 0, 22, 0, 1]
```

## CP2 low-mode pilot

For CP2_9 only, a local low-spectrum pilot at `t=0.05` gives:

```text
degree 0 low5 = 3.5327647925
degree 1 low5 = 4.5487357452
degree 2 low5 = 4.8794247729
degree 3 low5 = 4.9157374583
degree 4 low5 = 4.9313609091
```

The K3_16 middle-degree Laplacian is large enough that production nonzero-mode
heat traces should use Hutchinson/Chebyshev or `expm_multiply` estimators on the
BT994 sparse Laplacians, not dense diagonalization.

## Witnesses

```text
analysis/bt995_edgewise_heat_trace_real_seeds.py
data/bt995_edgewise_heat_trace_real_seeds.json
```
