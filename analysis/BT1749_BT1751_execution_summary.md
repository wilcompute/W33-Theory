# BT1749-BT1751 execution summary

Executed the three requested next moves from the BT1745-BT1748 frontier.

## BT1749: bounded coordinated cocycle search checkpoint

Added `analysis/bt1749_bounded_coordinated_cocycle_search.py`.

A local seeded 5000-trial coordinated 2-4 position probe from the BT1738 witness found no admissible no-4/no-6 candidate below the current best score:

```text
BT1738 choices = [459,595,435,694,87,544,347,839,561]
base score = (44 eight-cycles, 73 ten-cycles, diameter 9)
observed admissible improvements = 0
```

Boundary: this is a bounded checkpoint, not a global nonexistence theorem. The next engine should be structured voltage/backtracking rather than random local probing.

## BT1750: Coxeter-aware E8 hexagon bus invariants

Added `analysis/bt1750_coxeter_hexagon_bus_invariants.py`.

The E8 C^5 hexagons form 40 Witting-ray hexagons. The Coxeter element C permutes these 40 hexagons in eight 5-cycles. The BT1747 sorted 8-hexagon bus partition is not Coxeter-fixed; its orbit under C has size 5.

This gives the first Weyl-aware guardrail on the root-bus allocation:

```text
40 hexagons = eight Coxeter 5-cycles
5 buses = five 8-hexagon blocks
sorted bus partition orbit under C = 5
```

Boundary: Coxeter-aware, not full Weyl-group canonical.

## BT1751: Hesse-family channel derivation

Added `analysis/bt1751_hesse_family_channel_derivation.py`.

This closes part of the BT1748 derivation gap. In the selected Hesse AG(2,3) engine, every cell lies on exactly one selected row, one selected column, and one selected diagonal. Therefore the channel colors are geometrically forced:

```text
rows -> R
columns -> C
diagonals -> S
```

So the BT1748 channel weld no longer needs arbitrary sorted-neighbor coloring. The remaining open problem is deriving the nine Fano orientation choices from the 64-bit frame.
