# BT1260 -- Cross-Regime Labelled Geodesic Comparison

## Purpose

BT1260 compares labelled geodesic tensors across all full-order edge-graph regimes from BT1255.

## Summary table

```text
regime              zero graph   diameter   channel spread   diameter endpoint first-set sizes
diam10_A            K2+2I        10         67               8:16
diam10_B            2K2          10         0                6:32, 7:40, 8:76
diam10_C            empty_4I     10         0                8:3
diam12              P3+I         12         339              7:4, 8:1
diam14_polar_path   P4           14         172              8:1
```

## Consequence

The labelled geodesic tensor refines both the unlabelled sphere and the polar/nonpolar edge graph.  Two diameter-10 regimes are total-channel balanced, while diameter 12 has the largest total-channel spread.  The polar path diameter-14 regime is characterized by the longest diameter and a unique all-channel endpoint.

## Boundary

These channel totals are anchored to representative labellings.  They are label-sensitive by design; under relabelling, the multiset is the stable comparison object.

## Files

- Code: `analysis/bt1260_cross_regime_labelled_geodesic_comparison.py`
- Result: `data/bt1260_cross_regime_labelled_geodesic_comparison_summary.json`
