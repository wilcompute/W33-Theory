# BT1217 -- Holonet Lab-Readiness Scorecard

## Purpose

BT1217 fuses the latest experimental/protocol artifacts into one dashboard score:

- BT1212: lambda-lock adversarial robustness;
- BT1216: synthetic Clifford tomography recovery;
- BT1211: encoded q-invariance;
- BT1215: K3 geometry schema readiness;
- the known open hardware-threshold lane.

## Score

The current score is

\[
0.90 = 90\%.
\]

This means:

```text
protocol-ready_not_threshold-ready
```

## Components

| Component | Weight | Passes | Source |
|---|---:|---|---|
| Lambda-lock robustness | 0.30 | yes | BT1212 |
| Clifford tomography signature | 0.30 | yes | BT1216 |
| Encoded q-invariance | 0.20 | yes | BT1211 |
| K3 schema readiness | 0.10 | yes | BT1215 |
| Hardware threshold readiness | 0.10 | no | open GKP/Steinberg hardware threshold |

## Interpretation

The demonstrator is now protocol-ready as a falsification roadmap:

\[
q\text{-lock robustness}
+
\mathrm{Clifford}\text{-signature recovery}
+
\mathrm{encoded}\ q\text{-invariance}
\]

are all represented by executable artifacts.

The fault-tolerant machine remains not threshold-ready because the following are still open:

- physical GKP qutrit state generation,
- threshold squeezing,
- encoded syndrome recovery,
- cubic non-Gaussian resource preparation.

## Boundary

A 90 percent score is not a hardware-completion claim. It is a protocol-readiness claim. The hardware-threshold component is intentionally failed to prevent overclaiming.

## Files

- Code: `analysis/bt1217_holonet_lab_readiness_score.py`
- Result: `data/bt1217_holonet_lab_readiness_score_summary.json`
