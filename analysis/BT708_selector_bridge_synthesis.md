# BT708 — Selector Bridge Synthesis

BT705--BT707 settle the next selector layer without overclaiming.

## Objects

```text
local K33 charts: 240
rectangles per chart: 9
total centered rectangles: 2160
valid Levi lifts per rectangle: 24
unique Levi 8-cycles: 1620
presentation multiplicity per Levi 8-cycle: 32
```

Therefore

```text
2160 * 24 = 51840 = 1620 * 32.
```

## Selector architecture

BT699 gave

```text
24 = 8 * 3.
```

BT705 identifies the geometric meaning:

```text
8 = square-orientation / D4 mask layer
3 = Fano diagonal channel layer
1 = tomotope hinge-selected channel
```

so the physical selector is

```text
24 -> 3 -> 1.
```

## Eigenspace comparison

BT706 records the corrected chart side:

```text
HH^T = 9I + A_Gamma
A_Gamma eigenvalue -1 with multiplicity 81
HH^T eigenvalue 8 with multiplicity 81
```

and the Levi side:

```text
E4 = CC^T / 160
rank(E4)=81.
```

The lex selector is rejected.  The all-lift average is balanced but not a selector.  The tomotope-hinge selector is the only viable functorial bridge.

## Braid layer

BT707 attaches the selected local rectangle cycles to the Fibonacci four-block register:

```text
beta1(K33)=4
four two-state Fibonacci blocks = 16 states
```

The braid representation is valid blockwise, but the final generator-respecting lift test remains open.

## Final status

```text
BT705: correct selector architecture
BT706: corrected chart81 / LeviE4 comparison and false-selector rejection
BT707: braid-functor architecture
BT708: synthesis and next executable target
```

## Next executable target

Build the hinge-selected matrix

```text
S_hinge : chart rectangles -> signed Levi flag edges
```

then test

```text
rank(Z_chart^T S_hinge)=81
D_Levi S_hinge^T = 0
image(S_hinge on chart81)=Levi E4.
```

That is the precise all-the-way completion criterion.
