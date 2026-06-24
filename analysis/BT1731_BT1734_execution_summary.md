# BT1731-BT1734 execution summary

Executed the three requested next moves plus the 64/64/192 lift.

## BT1731

Added `analysis/bt1731_q2025_aut_generators.py`.

The q2025 red quotient has automorphism group size 2: identity plus one nontrivial involution. The q2025 blue quotient is rigid with automorphism group size 1. These are low-symmetry fingerprints for the two new q2025 48-bus charts and distinguish them from the cyclic Reye/BT1715 chart, whose automorphism group size is 576.

## BT1732

Added `analysis/bt1732_girth8_obstruction_search.py`.

The stored Hesse/Fano cocycle witness is connected, cubic, and has the count profile `63/63/189`. It has no 4-cycles and no 6-cycles. The bounded census records exactly 54 cycles of length 8 and 75 cycles of length 10. The next search target is therefore explicit: remove the 8-cycle layer first, then the 10-cycle layer.

## BT1733

Added `analysis/bt1733_master_atlas_table.py` and generated `analysis/BT1733_master_16_cell_atlas.md`.

The atlas indexes every master cell by knight order, cell coordinate, Gray bits, Clifford grade, q2025 slot, genus axes, Latin symbol, magic-square label, and Hesse/exceptional block.

Verified profile:

```text
Clifford grades: 1,4,6,4,1
Hesse/exceptional: 9+7=16
Genus incidences: 16*3=48
Q4 half-edge bit slots: 16*4=64
Tomotope flag lift: 64*3=192
```

## BT1734

Added `analysis/bt1734_64_64_192_tomotope_bit_lift.py`.

The 64/64/192 suggestion has a clean carrier interpretation:

```text
Q4 vertices = 16
Q4 bit directions per vertex = 4
bit slots = 16*4 = 64
local axis channels = R,C,S = 3
incidences = 64*3 = 192
```

The verifier constructs a bipartite `64/64/192` carrier with degree 3 on both sides. This is not a replacement for split-Cayley `63/63/189`; it is the framed 64-bit/tomotope-flag lift of the 16-cell Q4 substrate.
