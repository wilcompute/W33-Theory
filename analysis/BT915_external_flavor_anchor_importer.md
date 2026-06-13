# BT915 — External Flavor Anchor Importer

BT915 replaces BT912's hand-entered comparison constants with a versioned external-anchor file:

```text
data/external_flavor_anchors_20260613.json
```

## Schema

```text
external_flavor_anchors/v1
```

The anchor file records:

- source keys and URLs;
- CKM/Cabibbo comparison anchor;
- NuFIT-style PMNS comparison anchors;
- charged-lepton masses for Koide recomputation.

## Guardrail

The importer does not fit anything. It reads the external anchors, validates source keys, recomputes residuals/pulls against the fixed internal fractions, and writes a deterministic comparison ledger.

## Internal values

\[
\sin\theta_C=\frac3{\sqrt{178}},\quad
\sin^2\theta_{12}=\frac4{13},\quad
\sin^2\theta_{13}=\frac2{91},\quad
\sin^2\theta_{23}=\frac7{13},\quad
Q=\frac23.
\]

## Witness

```text
analysis/bt915_external_flavor_anchor_importer.py
data/PART_BT915_EXTERNAL_FLAVOR_ANCHOR_IMPORTER_results.json
```
