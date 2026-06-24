# BT1662 — Clock-Levi Gauge Bridge Search

BT1659 set the boundary: the Heawood/Fano clock is not a literal subgraph of the W33 Levi graph. The bridge must therefore live in homology coordinates.

## Gauge datum

Choose a cycle-basis gauge on both sides:

- Heawood cycle basis rooted at clock node 0.
- W33 Levi cycle basis rooted at Levi point p0.
- Eight shortest cycles from the Levi basis, sorted deterministically.

This defines an injective coordinate map

\[
B:H_1(H)\to H_1(L_{W33}).
\]

In the chosen bases,

\[
B=[I_8\mid0_{8\times73}].
\]

## Verified dimensions

\[
\dim H_1(H)=8,
\qquad
\dim H_1(L_{W33})=81.
\]

Thus

\[
\operatorname{rank}B=8,
\qquad
81-8=73
\]

Levi coordinates remain outside the selected bridge.

## Meaning

The missing datum is a basis/gauge choice. With it, there is a concrete rank-8 clock-to-Levi homology bridge. Without it, the natural object remains the full rank-648 tensor coupling from BT1659.

## Files

- `analysis/bt1662_clock_levi_gauge_bridge_search.py`
- `data/PART_BT1662_CLOCK_LEVI_GAUGE_BRIDGE_results.json`
