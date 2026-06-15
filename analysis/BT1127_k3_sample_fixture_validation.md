# BT1127 — K3 sample fixture validation

BT1127 adds a minimal valid sample input for the K3 spectral-action interface.

## Files

```text
data/bt1127_k3_sample_input.json
data/bt1127_k3_sample_envelope.json
```

The sample input contains all required BT1120 schema keys and K3 topological checks:

```text
chi = 24
signature = -16
b2 = 22
intersection_signature = (3,19)
```

## Important boundary

The numeric entries are placeholders for schema validation.  They are not a computed K3 metric, curvature integral, or physical spectral-action value.

## Purpose

The fixture lets local/CI runs check the interface contract before the real geometry compute lane produces its first K3 result.
