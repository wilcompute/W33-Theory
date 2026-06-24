# BT1665 — Gauge Bridge Naturality Test

## Question

BT1662 produced a concrete bridge

\[
H_1(H)\to H_1(L_{W33})
\]

after choosing cycle bases. BT1665 asks whether that deterministic recipe is
natural or merely gauge-fixed.

## Test

For each of the 80 possible W33 Levi roots:

1. compute a deterministic cycle basis;
2. select the eight shortest cycles;
3. record the selected support signature:
   - cycle lengths;
   - union edge count;
   - union vertex count;
   - pairwise edge-overlap count.

## Result

All selected cycles are 8-cycles, but the support signatures vary.

\[
\boxed{80\text{ roots tested}.}
\]

\[
\boxed{38\text{ distinct support signatures}.}
\]

The union edge count ranges from

\[
41\le |E_{\rm union}|\le53.
\]

The union vertex count ranges from

\[
34\le |V_{\rm union}|\le47.
\]

The pairwise edge-overlap score ranges from

\[
12\le O\le30.
\]

## Conclusion

The BT1662 bridge is not canonical. It is a valid gauge-fixed coordinate bridge,
but the chosen eight Levi cycles depend on the root/basis gauge.

The invariant statement is therefore:

\[
\boxed{
\dim H_1(H)=8,
\qquad
\dim H_1(L_{W33})=81,
}
\]

and a bridge requires extra gauge data.

## Boundary

This is a root-gauge naturality test, not a full automorphism-group orbit
classification. It is nevertheless enough to falsify canonicity of the
cycle-basis selector used in BT1662.

## Files

- `analysis/bt1665_gauge_bridge_naturality_test.py`
- `data/PART_BT1665_GAUGE_BRIDGE_NATURALITY_results.json`
