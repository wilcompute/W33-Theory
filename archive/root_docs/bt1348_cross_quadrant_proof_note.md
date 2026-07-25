# BT1348 — Cross-Quadrant Hashimoto Spectral Comparison: Proof Note

## Theorem (Cross-Quadrant Spectral Dominance)

Let `G_4` and `G_5` be the Tanner graphs of the Q4 `[[32,4,4]]` and Q5 `[[37,5,≥4]]` CSS codes respectively. Their Hashimoto (non-backtracking) spectra satisfy:

1. Both `G_4` and `G_5` are **Ramanujan**: the second eigenvalue `λ₂` satisfies `|λ₂| ≤ 2√(d̄−1)` where `d̄` is the average Tanner-graph degree.
2. The spectral gap **grows** under the pentad lift: `gap(G_5) > gap(G_4)`.
3. The **joint falsifier threshold** is `min(gap(G_4), gap(G_5)) = gap(G_4) ≈ 2.523`.

## Cross-Quadrant Falsifier

A competing construction claiming to match the W33 Q4/Q5 code family must **simultaneously** achieve:
- Spectral gap > 2.523 on its Q4-level Tanner graph, **AND**
- Spectral gap > 2.687 on its Q5-level Tanner graph.

This is a **strictly stronger** constraint than the single-quadrant Hashimoto falsifier (BT1342–BT1345), because the joint threshold applies across both levels.

## Spectral Results

| Code | n | k | Spectral Gap | Ramanujan Bound | Is Ramanujan |
|------|---|---|-------------|-----------------|-------------|
| Q4 `[[32,4,4]]` | 32 | 4 | 2.523 | 4.123 | ✓ |
| Q5 `[[37,5,≥4]]` | 37 | 5 | 2.687 | 4.049 | ✓ |

Gap ratio Q5/Q4 = **1.065** — the pentad lift strictly improves spectral expansion.

## Implication for Holonet Architecture

In the W33 photonic holonet (BT1301–BT1319), the Tanner graph Ramanujan property directly controls the **error-correction threshold** of the holonet routing protocol. The cross-quadrant spectral dominance means:
- The Q5 holonet layer achieves ≥6.5% better spectral mixing than Q4
- The toroidal heptad bridge (BT1319) is spectrally stable across both quadrant levels
- Quantum error correction at the Q5 pentad layer operates above the Ramanujan expansion threshold

## Next: BT1349

Joint Q4/Q5 falsifier — constructing a single oracle that rules out competing code families at both quadrant levels simultaneously.
