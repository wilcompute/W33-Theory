# BT1225 -- Recent Artifacts Verifier

## Purpose

BT1225 adds a lightweight CI-style verifier for the latest holonet/R3 packet.

It checks BT1218 through BT1224 for:

- required file presence,
- BT1218 protocol-readiness boundary,
- exact BT1219 single-qutrit closure,
- exact BT1221 two-qutrit closure,
- BT1223 blocking of mock R3 samples,
- BT1224 Clifford dashboard pass.

## Result

All checks pass:

```text
passes_all_checks = true
```

The verifier confirms:

\[
|SL(2,3)|=24,
\qquad
|Sp(4,3)|=51840,
\]

and that mock R3 samples remain blocked from candidate status.

## Files

- Code: `analysis/bt1225_recent_artifacts_verifier.py`
- Result: `data/bt1225_recent_artifacts_verifier_summary.json`

## Boundary

This is a consistency verifier for repository artifacts. It does not replace full CI, local execution, or hardware validation.
