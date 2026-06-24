# BT1728-BT1730 execution summary

Executed all three requested next moves.

## BT1728: q2025 48-bus chart classifier

Added `analysis/bt1728_q2025_chart_classifier.py`.

Result:

- The q2025 red quotient is a connected linear `(12_4,16_3)` chart with beta1 21 and automorphism group size 2.
- The q2025 blue quotient is a connected linear `(12_4,16_3)` chart with beta1 21 and automorphism group size 1.
- The BT544 cyclic Reye chart and BT1715 Klein-Latin chart are isomorphic and have automorphism group size 576.
- Red, blue, and cyclic Reye are pairwise non-isomorphic except for the BT544/BT1715 match.

Conclusion: q2025 supplies genuinely new low-symmetry 48-bus charts, not merely another copy of the cyclic Reye/tomotope chart.

## BT1729: Hesse/Fano girth-8 cocycle witness

Added `analysis/bt1729_hesse_fano_girth8_cocycle.py`.

Result:

- Direct Fano x Hesse product: nine disconnected components.
- New cocycle witness: connected cubic incidence graph with 63 points, 63 lines, and 189 incidences.
- It eliminates all 4-cycles and all 6-cycles.
- It reaches girth 8, with remaining cycles only at lengths 8 and 10 below the split-Cayley target.

Conclusion: the split-Cayley obstruction is now sharply reduced to the 8/10-cycle layer.

## BT1730: Cl4/Q4 master 16-cell fusion chart

Added `analysis/bt1730_cl4_q4_master_16_cell_fusion.py`.

Result:

A single `4x4` XOR-Latin chart now carries:

- q2025 line slots `0..15`,
- genus/tomotope axes `R,C,S`,
- Freudenthal Hesse/exceptional cell labels,
- toroidal knight order,
- Q4 Gray bits,
- Clifford grade.

The verifier proves that the toroidal knight tour maps to a Q4 Gray cycle and that its Clifford-grade layer profile is:

```text
1, 4, 6, 4, 1
```

Conclusion: BT1730 fuses the active q2025/genus/magic-square/Clifford/knight/Gray layers into one verified 16-cell carrier chart.
