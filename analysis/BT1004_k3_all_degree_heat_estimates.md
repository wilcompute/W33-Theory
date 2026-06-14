# BT1004 — K3_16 all-degree heat estimates

BT1004 completes the BT1001 estimator stack for the real level-1 edgewise K3_16
complex: all five Hodge degrees now have sparse ordinary heat-trace estimates.

## Method

Random sign trace estimation with sparse `expm_multiply`, using 4 samples per
degree. This is a production path, but the probe count should be increased for
publication-grade error bars.

## Ordinary heat trace estimates

| degree | t=0.01 | t=0.05 | t=0.1 | t=1.0 |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 93.49825997525843 | 23.828572098032808 | 8.862118256082157 | 0.6323630057508847 |
| 1 | 2332.715712278456 | 1509.4397257089238 | 944.3979080560184 | 31.888104091591273 |
| 2 | 8732.962310204446 | 6516.706282971161 | 4683.469829532396 | 298.585644407897 |
| 3 | 10853.78321014873 | 8620.61047497486 | 6611.008956638205 | 472.82647830085045 |
| 4 | 4383.753309581125 | 3611.059094255581 | 2870.4673023887685 | 225.7236956538722 |

## Alternating supertrace check

Target: `chi(K3_16)=24`.

| t | alternating estimate | standard error | z-error |
| ---: | ---: | ---: | ---: |
| 0.01 | 23.714957333644207 | 5.642930898887824 | -0.05051322999754829 |
| 0.05 | 21.54374864099198 | 12.8475079397478 | -0.19118504308596976 |
| 0.1 | 7.392385483023462 | 13.745658784636523 | -1.2082079714897924 |
| 1.0 | 20.227120675078364 | 7.256123494496646 | -0.5199579813909105 |

All sampled values are within estimator error of the exact target.

## Witnesses

```text
analysis/bt1004_k3_all_degree_heat_estimates.py
data/bt1004_k3_all_degree_heat_estimates.json
```
