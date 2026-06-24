# BT1668 — Gauge-Twirl Bridge Support Test

## Purpose

BT1665 showed that the BT1662 bridge is gauge-fixed. BT1668 asks what remains if
that gauge-fixed selector is averaged over all 80 W33 Levi root gauges.

## Twirl

For each Levi root:

1. compute the deterministic cycle basis;
2. select the eight shortest cycles;
3. accumulate edge and vertex support.

This gives a root-gauge twirl of the eight-cycle bridge selector.

## Result

The twirl uses

\[
80\text{ roots}\times8\text{ cycles/root}\times8\text{ edges/cycle}=5120
\]

edge-incidence events.

It covers

\[
\boxed{160/160\text{ Levi edges}}
\]

and

\[
\boxed{80/80\text{ Levi vertices}.}
\]

The twirl sees

\[
156
\]

unique cycles, with maximum cycle reuse count

\[
28.
\]

Edge counts range from

\[
1\le c_E\le103,
\]

and vertex counts range from

\[
5\le c_V\le134.
\]

The effective edge support size is

\[
2^{H_E}=103.540949910565,
\]

and the effective vertex support size is

\[
2^{H_V}=65.02080937248.
\]

## Conclusion

The twirled bridge does not collapse to a sparse canonical embedding. It spreads
across the entire W33 Levi graph.

Thus the correct statement is:

\[
\boxed{
\text{the gauge-fixed bridge is useful, but the averaged bridge is global.}
}
\]

## Boundary

This is a root-gauge twirl, not yet a full \(\mathrm{Sp}(4,3)\) automorphism
twirl. It is enough to show that the deterministic bridge does not secretly
select a sparse natural support.

## Files

- `analysis/bt1668_gauge_twirl_bridge.py`
- `data/PART_BT1668_GAUGE_TWIRL_BRIDGE_results.json`
