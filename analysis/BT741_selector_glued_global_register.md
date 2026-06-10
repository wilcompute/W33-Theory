# BT741 — Selector-Glued Global Register

Executes the BT740 boundary: lift the exact braid functor from per-chart
homology classes to the selected Levi cycles, i.e. compute what survives when
the 240 local K33 registers are glued along shared selected cycles.

## The gluing

Each chart carries the local register `H_1(K33;F2) = F2^4` (BT740: bit-flip =
`sigma^5 = Z`, exact).  For a family of lift records, whenever two rectangles
in different charts lift to the SAME Levi 8-cycle, their homology classes are
identified.  The global register is the F2-quotient

```text
R_glob = (sum over 240 charts of F2^4) / <class identifications>,
ambient dim = 960.
```

## Results (exact GF(2) ranks)

```text
family                          cycles  rank  GLOBAL DIM  components
BT718 sheet (1110, ch 011/far)     710   858     102      56 (dims 1,2,3 and one 32)
mask 1110 bundle (3 channels)     1306   956       4       1   <- FLAT
Type-A orbit bundle (12 sheets)   1620   960       0       1
Type-B orbit bundle (12 sheets)   1620   960       0       1
all 24 sheets                     1620   960       0       1

per-mask bundles (convention-dependent labels):
1110: 4   1101: 15   1011: 10   0111: 8
1100: 0   1001: 4    0110: 2    0011: 0
```

## Theorem (existence of a flat global register)

There exists a single-mask lift bundle (mask 1110 in the BT699 edge-order
convention) whose gluing is CONNECTED with TRIVIAL F2-HOLONOMY: the relation
rank is exactly 956 = 960 - 4, so all 240 local registers fuse into one
global

```text
R_glob = F2^4,    dim 4 = mu.
```

Combined with BT740, the global register carries the exact braid action:
each global bit-flip is the 5-letter braid word `sigma^5 = Z` applied in any
chart — the gluing guarantees chartwise consistency.  W(3,3) supports a
global 4-bit Fibonacci braid register.

## Theorem (equivariant collapse)

The equivariant gluings — either D4-orbit bundle (multiplicity-16 uniform)
and the full 24-sheet correspondence (multiplicity-32 uniform) — have
relation rank 960: the global register collapses to 0.  Full symmetry
over-glues; every register direction is killed by some monodromy loop.

This is the BT705 principle one level up: just as a single Levi presentation
needs the tomotope hinge datum, a global register needs a bundle (gauge)
choice.  Symmetric aggregation preserves sector rank (BT739) but kills the
register quotient; selection preserves the register but breaks equivariance.

## Diagnostics

- The single BT718 sheet is too little gluing: 56 components, fragmented
  dims (42 ones, 11 twos, 2 threes, one 32-dim giant component), total 102.
- Mask-bundle flatness is special, not generic: masks 1100/0011 collapse to
  0 even at bundle level; 1101 fragments into 11 components (dim 15).
- The mask labels themselves are edge-order-convention artifacts (the same
  caveat as BT713/BT718); the theorem is an existence statement for the
  convention class.

## Boundary

Open: a geometric (hinge-style) characterization of WHICH lift bundles are
flat — the conjecture is that flatness corresponds to the tomotope hinge
classes of BT705, which would make the global F2^4 register canonical given
hinge data.  Also open: explicit global braid-word generators realizing the
four logical bits through the BT535 holonomy framework.
