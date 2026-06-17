# BT1257 -- Labelled Geodesic Tensor

## Purpose

BT1257 strengthens BT1254 from a labelled inverse-pair tensor to a shortest-geodesic first/last-channel tensor.

## Definition

For every group element at word distance \(d\), record the labelled generator channels that can occur as the first or last letter of at least one shortest word from the identity.

This preserves the unlabelled BT1233 sphere histogram:

\[
1,8,36,126,363,916,2052,4096,7396,12170,16916,7247,476,36,1.
\]

But it adds anchored channel incidence data.

## Result

Total first-channel incidences are:

```text
g1p=16197, g1m=16197
g2p=16025, g2m=16025
g3p=16025, g3m=16025
g4p=16197, g4m=16197
```

The last-channel totals are identical.

At the unique diameter-14 endpoint, every channel can occur as a first channel on some shortest geodesic, so the first-set size is 8.

## Consequence

BT1233/BT1242 are unlabelled symmetric invariants. BT1257 is a genuine labelled tomography layer: it can see anchored channel imbalance even when the unlabelled sphere is unchanged.

## Files

- Code: `analysis/bt1257_labelled_geodesic_tensor.py`
- Result: `data/bt1257_labelled_geodesic_tensor_summary.json`
