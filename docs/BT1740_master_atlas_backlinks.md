# BT1740 Master Atlas Backlinks

This note turns the BT1737 atlas into a navigation hub instead of a standalone page.

## Primary atlas

- `docs/BT1737_master_16_cell_atlas.html`
- `analysis/BT1733_master_16_cell_atlas.md`
- `analysis/bt1733_master_atlas_table.py`

## Verified carrier layers

- q2025 low-symmetry 48-bus charts: `analysis/bt1728_q2025_chart_classifier.py`, `analysis/bt1731_q2025_aut_generators.py`
- Hesse/Fano cocycle descent: `analysis/bt1729_hesse_fano_girth8_cocycle.py`, `analysis/bt1735_hesse_fano_8cycle_descent.py`, `analysis/bt1738_hesse_fano_8cycle_44_witness.py`
- Master 16-cell fusion: `analysis/bt1730_cl4_q4_master_16_cell_fusion.py`
- Clifford/Q4/knight/Gray theorem: `analysis/bt1727_clifford_knight_q4_gray.py`
- 64-bit/tomotope framed lift: `analysis/bt1734_64_64_192_tomotope_bit_lift.py`
- Self-frame puncture boundary: `analysis/bt1736_self_frame_puncture_64_to_63.py`, `analysis/bt1739_self_frame_incidence_real_boundary.py`

## Count-law hub

```text
16 master cells
16*3 = 48 local genus/tomotope incidences
16*4 = 64 Q4 bit slots
64*3 = 192 framed tomotope flags
64/64/192 minus one three-channel self-frame = 63/63/189
Clifford grades = 1,4,6,4,1
Hesse/exceptional split = 9+7=16
```

## Reading order

1. Open the atlas page.
2. Read BT1730 for the fused 16-cell chart.
3. Read BT1734 and BT1736/BT1739 for the 64-bit self-frame lift.
4. Read BT1729, BT1735, and BT1738 for the current split-Cayley cocycle boundary.
5. Read BT1728 and BT1731 for the low-symmetry q2025 48-bus classifiers.

Boundary: this note is a docs navigation layer. It does not add new mathematical claims beyond the cited verifier scripts.
