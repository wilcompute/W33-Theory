# BT1255 -- Full-Order Edge Graph Regime Classifier

## Purpose

BT1255 globalizes the BT1252 polar path tetrahedron by classifying the polar/nonpolar edge graphs for every full-order diameter regime.

## Regime edge graphs

```text
diam10_A: zero K2+2I,   nonzero K4-e
diam10_B: zero 2K2,     nonzero C4
diam10_C: zero empty,   nonzero K4
diam12:   zero P3+I,    nonzero paw
diam14:   zero P4,      nonzero P4
```

## Globalization of the polar path tetrahedron

BT1248 showed that the diameter-14 full-order regime is a single orbit of size 12,960.  BT1252 showed that one representative has zero/nonzero edge split

\[
K_4=P_4\sqcup P_4.
\]

Therefore every diameter-14 full-order four-set is a polar path tetrahedron up to the \(Sp(4,3)\) action.

## Consequence

The diameter-14 regime is the unique self-complementary edge-split regime.  This explains why its pair law is balanced:

\[
9^3 24^3.
\]

The diameter-10 regimes are locally too fast, and the diameter-12 regime is intermediate.  The BT1228/BT1233 recovery target is the self-complementary polar path tetrahedron.

## Files

- Code: `analysis/bt1255_full_order_edge_graph_regime_classifier.py`
- Result: `data/bt1255_full_order_edge_graph_regime_classifier_summary.json`
