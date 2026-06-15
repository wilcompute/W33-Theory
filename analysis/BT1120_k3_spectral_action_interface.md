# BT1120 — K3 spectral-action interface skeleton

BT1120 converts the BT1117 target ledger into a concrete script interface.

## Script

```text
tools/bt1120_k3_spectral_action_interface.py
```

The script validates a K3 spectral-action result JSON and emits a normalized envelope.

## Required input fields

```text
operator_convention
metric_source
volume_normalization
A0
A2
A4
curvature_convention
refinement_h
topological_checks
```

The topological checks must include:

```text
chi
signature
b2
intersection_signature
```

## Attached finite W33 prefactors

The schema records the seed-independent finite prefactors:

```text
mH2_over_v2 = 14/55
lambda_H = 7/55
finite_a2_over_a0 = 14/3
finite_a4_over_a2 = 55/7
```

## Boundary

BT1120 is an interface and validation skeleton.  It does not compute a K3 metric, curvature integral, or spectral-action value.
