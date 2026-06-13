# BT913 — Sentinel-coordinate Dynamics

BT913 turns the BT910 leftover coordinate into an explicit monitor.

The profile decomposition is

\[
\mathbb C^9=(2+2+2+2)+1.
\]

The final \(+1\) coordinate is not matter content. It is the sentinel/provenance coordinate for the four profile planes.

## Dynamics law

\[
E_{\rm sentinel}
=
\sum_i (s_i-s_i^*)^2
+\mathbf 1_{\rm stale\ release}
+E_{g=15}.
\]

The target values are

\[
s_i^*\in\left\{\frac9{178},\frac4{13},\frac2{91},\frac7{13}\right\}.
\]

## Cases

| case | sentinel energy |
|---|---:|
| exact profile, clean release | 0 |
| reactor plane shifted from \(2/91\) to \(3/91\) | 0.000120758... |
| stale release artifact | 1 |
| external \(g=15\) fault channel \(15/40\) | 0.375 |

## Result

\[
\boxed{\text{The neutral coordinate is dynamically useful as a monitor: it detects profile drift, stale artifacts, and }g=15\text{ fault energy.}}
\]

It still does not add a new generation or sterile state.

## Witness

```text
analysis/bt913_sentinel_coordinate_dynamics.py
data/PART_BT913_SENTINEL_COORDINATE_DYNAMICS_results.json
```
