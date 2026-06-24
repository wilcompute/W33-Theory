# BT1720-BT1723 repo-mining execution

I searched beyond literal terms and used the repo's older aliases: H27 Latin cube, Hesse/AG(2,3), Reye/tomotope, Pascal diagonals, Fibonacci exceptional Coxeter ladder, octonion/E8 magic square, monodromy/holonomy, and the 4x4 axis-bus work.

## Repo clues used

- `tools/h27_latin_cube_search.py` searches whether the H27 layer can be modeled as a `3x3x3` Latin cube by labeling four H12 triangles with symbols in `F3`. Its recorded artifact says no base has a Latin-cube labeling. This says the missing object is not a naive H27 Latin cube.
- `analysis/w33_witting_reye_toroidal_tomotope_collapse.py` already contains the right positive Latin object: a concrete cyclic Reye model with four triads of three points, twelve cross-triad Latin lines, `(12_4,16_3)`, 48 incidences, and Levi cycle rank 21.
- `verify_dccli_pascal_diagonal_w33_generator.py` records the Pascal/Fibonacci exceptional ladder: triangular numbers generate W(3,3) primitives, and the exceptional Coxeter multipliers are Fibonacci values `1,2,2,3,5`.
- `tools/OCTONION_E8_CONNECTION.py` records the 4x4 Freudenthal-Tits magic square over `R,C,H,O`, with the exceptional cells in the octonionic row/column.

## BT1720: q2025 connected domain triples

Added `analysis/bt1720_q2025_connected_domain_triples.py`.

The red q2025 domain symplectic closure gives exactly 16 commuting triples on 24 observables, every observable degree 2. The blue domain initially failed the degree law with degree set `{1,2,3}`. A one-letter closure search found a unique correction in the visual transcription: `XXY -> XYY`. After that correction the blue domain also gives 16 triples, 48 incidences, and every observable degree 2.

Both red and corrected blue domains are connected. They are not isomorphic to the simple BT1715 disconnected parity cover. Therefore q2025 is not the naive parity split; it is a connected monodromy cover.

## BT1721: Hesse/Fano monodromy twist waypoint

Added `analysis/bt1721_hesse_fano_monodromy_twist.py`.

The direct `Fano x Hesse` product has nine disconnected Fano components. I replaced it by a three-direction Hesse schedule with oriented Fano-line systems from `Aut(Fano)`. The deterministic witness has 63 points, 63 lines, 189 incidences, degree 3, and is connected.

It still has short cycles, so it is not the split Cayley hexagon. This is a useful waypoint/falsifier: the missing monodromy must connect the nine Hesse cells while also killing the short cycles to reach girth 12.

## BT1722: genus/bus theorem insert

Added `analysis/bt1722_genus_bus_theorem_insert.py`.

The paper-ready theorem is now generated as text:

```text
The BT1715 48-bus has twelve axes arranged as 4+4+4 and sixteen cells,
each incident with three axes. The same 12 is the complete-graph genus
numerator at the K7 torus seed, (7-3)(7-4)=4*3=12. Csaszar reads n=V=7;
Szilassi reads n=F=7. The tetrahedral seed n=4 has zero numerator in both
primal and dual readings. Lifting the denominator object to n=12 gives
(12-3)(12-4)=72 and the payload C(12,2)=66.
```

## BT1723: added fourth move, magic-square Latin exceptional heptad

Added `analysis/bt1723_magic_square_latin_exceptional_heptad.py`.

This is the new outside-the-box bridge from the repo mining. Put the 4x4 Freudenthal magic square on the `F2^2` XOR Latin square. Then:

```text
16 magic-square cells = 9 non-octonionic cells + 7 octonionic exceptional cells.
```

The `9` non-octonionic cells form the `R,C,H` by `R,C,H` block, exactly the Hesse/AG(2,3) size. The `7` octonionic cells are the row/column `O` heptad:

```text
F4,F4,E6,E6,E7,E7,E8.
```

So the same 4x4 Latin chart decomposes as:

```text
Hesse 9-grid + exceptional/Fano heptad = 16-cell bus.
```

The Coxeter side also matches the repo's Pascal/Fibonacci result:

```text
h(G2),h(F4),h(E6),h(E7),h(E8) = 6,12,12,18,30
multipliers over q! = 1,2,2,3,5
sum all five = 78
G2+E6+E7+E8 = 66
```

Boundary: this is an exact chart/count bridge, not yet a Lie-bracket embedding into q2025 contextual incidence.
