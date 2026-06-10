# BT716 — Selector Rank Filter and Chart-Levi Bridge Paper Insert

This is the manuscript-ready content for BT713-BT715.

## Selector rank filter

Each centered local K33 rectangle has 24 valid Levi 8-cycle lift presentations. BT699 split these as:

```text
24 = 8 square-orientation masks x 3 residual Fano/tomotope channels
```

BT713 proved that the 24 selector sheets are not equivalent:

```text
rank 81: 19 sheets
rank 76: 1 sheet
rank 70: 4 sheets
```

So a physical hinge selector must land in a rank-81 sheet or a rank-81 mask bundle.

## Rank-complete hinge representative

BT714 uses the representative:

```text
mask = 1110
residual channel = 0
```

For the signed selector matrix S_hinge:

```text
rank(S_hinge) = 81
rank(D_Levi) = 79
D_Levi S_hinge^T = 0
rank(D_Levi) + rank(S_hinge) = 160
```

Therefore:

```text
rowspace(S_hinge) = ker(D_Levi) = im(E4)
```

where E4 is the protected Levi Hodge idempotent CC^T / 160.

## Chart-side bridge

The corrected chart-overlap operator satisfies:

```text
H H^T = 9I + A_Gamma
```

The chart 81-sector is the positive eigenspace 8^81, not a nullspace. The hinge selector gives full comparison rank:

```text
rank(E_chart -> E4) = 81
```

So the local K33 chart sector and the Levi H1/E4 sector are the same protected 81-dimensional Hodge sector after hinge selection.

Boundary: this proves the bridge for a rank-complete hinge representative. It does not prove uniqueness of the final tomotope/Fano hinge among the 19 full-rank sheets.
