# BT1724-BT1727 execution summary

Executed the three requested next steps plus the fourth Clifford/knight/Q4 track.

## Repo mining anchors

The relevant older repo work was not under one obvious name.  The key anchors were:

- `analysis/w33_BREAKTHROUGH_157_Cl4_Q4_knight_gray_unification.py`: Cl4, Q4, toroidal 4x4 knight tour, and Gray code are already identified as the same 16-vertex substrate, with Clifford grade profile `1+4+6+4+1`.
- `tools/bt1412_toroidal_q4_oscillator_boundary.py`: the Q4/toroidal oscillator boundary layer.
- `tools/h27_latin_cube_search.py`: H27 fails as a naive `3x3x3` Latin cube, so the positive object has to be a quotient/cover rather than a cube.
- `analysis/w33_witting_reye_toroidal_tomotope_collapse.py`: the positive Latin/Reye model already existed as a cyclic `(12_4,16_3)` chart with 48 incidences and cycle rank 21.
- `verify_dccli_pascal_diagonal_w33_generator.py`: Pascal/Fibonacci exceptional Coxeter ladder, including the `1,2,2,3,5` multiplier pattern.

## BT1724: q2025 quotient pairing

Added `analysis/bt1724_q2025_reye_quotient_pairing.py`.

Explicit pairings fold both q2025 red and corrected-blue `(24_2,16_3)` domains into connected linear `(12_4,16_3)` quotients with beta_1 = 21.

Important twist: the quotients are **not** isomorphic to the BT544/BT1715 cyclic Reye/Klein-Latin chart.  So q2025 gives a distinct connected 48-bus chart rather than a copy of the earlier parity/cyclic Reye bus.

## BT1725: Hesse/Fano girth repair boundary

Added `analysis/bt1725_hesse_fano_girth_repair.py`.

The direct `Fano x Hesse` product has nine disconnected components.  The Hesse/Fano monodromy witness is connected, 3-regular, has 63 points, 63 lines, and 189 incidences, and kills all 4-cycles.  Its girth is still 6, not 12.

So the split-Cayley target is now sharply bounded: preserve connectivity and 4-cycle-freeness, then kill the remaining 6, 8, and 10 cycles.

## BT1726: master 16-cell chart

Added `analysis/bt1726_master_16_cell_chart.py`.

A single 4x4 XOR-Latin chart now carries:

- 16 q2025 domain lines,
- 12 genus/tomotope axes and 48 incidences,
- the Freudenthal magic-square split into 9 Hesse cells plus 7 exceptional/octonionic cells,
- the Coxeter sums 78 and 66.

Boundary: this is the master indexing chart, not yet a complete incidence/bracket embedding.

## BT1727: Clifford / knight / Q4 / Gray theorem

Added `analysis/bt1727_clifford_knight_q4_gray.py`.

The verifier constructs the toroidal 4x4 knight graph and proves it is isomorphic to Q4.  It extracts a closed 16-step knight tour and maps it through the Q4 isomorphism to a 4-bit Gray cycle.  The Hamming-weight layers are exactly:

```text
1, 4, 6, 4, 1
```

So the 4x4 oscillator substrate is simultaneously:

```text
Cl4 grade algebra + Q4 topology + knight dynamics + Gray-code information.
```

This is the cleanest bridge into the user's 1+4+6+4+1 clue.
