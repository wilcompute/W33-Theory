# BT713 — Selector Sheet Rank Filter Theorem

This continues the selector chain at the exact point left open by BT708. BT696 proved that each centered local $K_{3,3}$ rectangle has 24 valid center-gauge lift presentations to Levi 8-cycles. BT699 split those presentations as

```text
24 = 8 square-orientation masks × 3 residual Fano-channel choices.
```

BT705 then interpreted the intended geometric selector as

```text
24 -> 3 -> 1,
```

where the first reduction is a $D_4$ / square-orientation choice and the second is a Fano/tomotope hinge channel choice. BT713 adds the missing hard filter: **not every one of the 24 candidate selector sheets carries the full Levi Hodge sector.**

## Local computation

The script rebuilds $W(3,3)$ as the symplectic polar graph over $\mathbb F_3^4$ and verifies:

```text
|V(W33)| = 40
|E(W33)| = 240
W33 degree = 12
40 GQ lines
160 Levi flags
```

The point-line Levi graph has

```text
80 vertices
160 flag edges
beta_1 = 160 - 80 + 1 = 81.
```

The computation then repeats the BT696/BT699 lift enumeration:

```text
centered K33 rectangles = 2160
valid lifts per rectangle = 24
unique Levi 8-cycles = 1620
presentation multiplicity per Levi 8-cycle = 32
2160 * 24 = 51840 = 1620 * 32.
```

## New result

For each of the 24 selector sheets, choose exactly one signed Levi 8-cycle per rectangle and compute the rank of the resulting signed flag-incidence rows over a large prime field. The rank target is the Levi cycle-space dimension:

```text
rank target = beta_1(Levi) = 81.
```

The result is:

```text
rank 81: 19 sheets
rank 76:  1 sheet
rank 70:  4 sheets
```

So:

```text
19 / 24 selector sheets are Hodge-complete.
5 / 24 selector sheets are rank-defective.
```

At the mask-bundle level, retaining all three residual channels for one mask gives:

```text
0011: 81
0110: 81
0111: 81
1001: 76
1011: 81
1100: 81
1101: 81
1110: 81
```

Thus seven of the eight square-orientation masks are Hodge-complete, and the unique mask-level defect is

```text
1001 -> rank 76.
```

## Interpretation

This is the first purely algebraic filter on the selector architecture:

```text
local rectangle selector
  -> signed Levi cycle rows
  -> rank-81 Hodge test.
```

The consequence is sharp:

```text
The tomotope/Fano hinge selector cannot be arbitrary.
It must land in a rank-81 sheet, or at least in a rank-81 mask bundle, to carry the protected E4/H1 sector.
```

This also reframes the BT708 open target. Instead of asking for any $S_{\rm hinge}$, the next executable target is now:

```text
construct the geometric hinge selector and verify it chooses one of the 19 full-rank sheets,
or explain why it passes through one of the seven full-rank mask bundles before final channel selection.
```

## Boundary

The residual-channel ordering used in this verifier is a deterministic local ordering of the three valid cycles inside each mask. The invariant conclusion is the rank filter itself: the 24 candidate selector sheets are not equivalent under the Levi Hodge test.
