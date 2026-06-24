# BT1677 — Gauge-Fixed Bridge Survival Metric

## Purpose

BT1677 quantifies how much clock--Levi bridge signal survives as the bridge is
averaged over larger gauge families.

There are two different notions of survival:

1. **oriented cycle-subspace survival**;
2. **all-positive support-amplitude survival**.

They should not be conflated.

## Oriented cycle-subspace survival

A fixed BT1662 gauge selects 8 Levi cycles.  As an oriented cycle subspace, those
8 directions live in

\[
H_1(L_{W33}),
\qquad
\dim H_1=81.
\]

Thus the fixed-gauge trace survival is

\[
\boxed{8.}
\]

The relative fraction is

\[
\frac{8}{81}=0.09876543209876543.
\]

If the full automorphism average acts irreducibly on the relevant \(H_1\) sector,
the expected averaged subspace projector is

\[
\frac{8}{81}P_{H_1}.
\]

That preserves trace but forgets the chosen bridge basis.

## Support-amplitude survival

For all-positive edge support vectors, the Hodge-cycle energy decays under partial
root twirls:

\[
\begin{array}{c|c|c|c}
\text{roots} & \text{edge events} & \text{support edges} & H_1\text{ energy} \\
\hline
1 & 64 & 45 & 0.12181818181818174 \\
2 & 128 & 69 & 0.10559006211180129 \\
4 & 256 & 95 & 0.0688172043010756 \\
8 & 512 & 113 & 0.04437317784256601 \\
16 & 1024 & 138 & 0.025854383358098552 \\
40 & 2560 & 145 & 0.030692758476350383 \\
80 & 5120 & 160 & 0.02639211670014884
\end{array}
\]

The full automorphism support twirl is the uniform edge vector, whose Hodge-cycle
energy is

\[
6.148618940382545\times10^{-16}.
\]

So full support averaging kills the homological signal in numerical precision.

## Interpretation

A fixed oriented bridge keeps 8 chosen \(H_1\) directions.  Support averaging does
not.  The bridge is therefore a gauge-fixed homology object, not a visible sparse
support object after symmetry averaging.

## Files

- `analysis/bt1677_gauge_bridge_survival_metric.py`
- `data/PART_BT1677_GAUGE_BRIDGE_SURVIVAL_METRIC_results.json`
