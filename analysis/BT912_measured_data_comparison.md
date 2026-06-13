# BT912 — Measured-data Comparison Layer

BT912 separates the exact internal Holonet profile values from external experimental comparison anchors.

## Guardrail

This is **not** a fit. The internal values are fixed:

\[
\sin\theta_C=\frac3{\sqrt{178}},\qquad
\sin^2\theta_{12}=\frac4{13},\qquad
\sin^2\theta_{13}=\frac2{91},\qquad
\sin^2\theta_{23}=\frac7{13},\qquad
Q_{\rm Koide}=\frac23.
\]

The external values are comparison anchors and should be refreshed whenever a formal PDG/NuFIT table import is added.

## Comparison summary

| observable | internal | external anchor | status |
|---|---:|---:|---|
| Cabibbo \(\sin\theta\) | 0.2248595 | 0.22484 ± 0.00044 | inside 1σ |
| PMNS solar \(\sin^2\theta_{12}\) | 0.3076923 | 0.308 ± 0.012 | inside 1σ |
| PMNS reactor \(\sin^2\theta_{13}\) | 0.0219780 | 0.02215 ± 0.00060 | inside 1σ |
| PMNS atmospheric \(\sin^2\theta_{23}\) | 0.5384615 | 0.55 ± 0.06 | inside 1σ, octant-broad |
| Koide \(Q\) | 0.6666667 | 0.6666613 from charged-lepton masses | close |

## Boundary

The module reports residuals and pulls. It does not tune any substrate number.

## Witness

```text
analysis/bt912_measured_data_comparison.py
data/PART_BT912_MEASURED_DATA_COMPARISON_results.json
```
