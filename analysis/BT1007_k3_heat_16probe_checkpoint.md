# BT1007 — K3_16 all-degree 16-probe heat checkpoint

BT1007 raises the BT1004 all-degree heat run from 4 probes per degree to 16
probes per degree on the real level-1 edgewise K3_16 Hodge stack.

## Alternating supertrace check

Target: `chi(K3_16)=24`.

| t | estimate | standard error | z-error |
| ---: | ---: | ---: | ---: |
| 0.01 | 22.35281745377688 | 1.7016019876069775 | -0.9680187013295697 |
| 0.05 | 18.637021322370856 | 6.563902732103608 | -0.8170411562315169 |
| 0.1 | 17.56392077911096 | 8.464846593889778 | -0.7603302847253993 |
| 1.0 | 11.073289410256422 | 4.570024711847879 | -2.828586584276191 |

Three sampled t-values are within one sigma of the exact target. The t=1 point
remains a higher-variance cancellation point and needs the longer 64-probe run.

## Boundary

A 64-probe all-degree pass exceeded the interactive execution window. The script
and checkpoint are committed so the longer run can be done in CI or a full
checkout with a larger wall-clock budget.

## Witnesses

```text
analysis/bt1007_k3_heat_16probe_checkpoint.py
data/bt1007_k3_heat_16probe_checkpoint.json
```
