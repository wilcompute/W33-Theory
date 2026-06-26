# BT1815--BT1817 quartet fibre-law packet

## Commit-frontier read

The frontier after BT1806 already contained BT1807--BT1814 and the larger arithmetic/experimental closure stack. The relevant fibre thread says:

```text
BT1808: the three-table repair is T010, T210, T222 with (-2,-2,+2) and Hamming profile 1,2,3.
BT1809: the missing 12-symbol fibre should be modeled as 12 = 3 x 4, with a twisted section over H27/Schlaefli transport.
BT1812: W(E6) does not fix the defect; it places it in a distinguished 6-hinge slice.
BT1813: the six-hinge slice is naturally K4 on four hidden states.
BT1814: the next solver should scan 10 stabilizer slices, then test quartet-edge orientation.
```

BT1815--BT1817 therefore does not duplicate BT1807--BT1809. It executes the next layer: make the hidden quartet, oriented repair law, and reduced search contract explicit.

## BT1815 — Quartet slice geometry

BT1815 models the W(E6)-distinguished size-6 hinge slice as the six edges of a hidden K4 quartet:

```text
states = 00, 01, 10, 11
edges = C(4,2) = 6
Aut(K4) = S4, order 24
edge orbit size = 6
edge stabilizer order = 4
oriented edge count = 12
```

The observed defect support is:

```text
(10,22,44)
```

and, under the committed edge-to-hinge chart, corresponds to quartet edge:

```text
00 -- 11
```

## BT1816 — Oriented quartet fibre law

BT1816 turns the BT1805 near-miss into a local fibre rule:

```text
oriented K4 edge = two endpoint losses plus one edge-target gain, in units of 2
```

For the observed edge this is:

```text
T010: -2
T210: -2
T222: +2
```

The observed syndromes are:

```text
F2 = [0,0]
F3 = [0,2,1,1,1]
```

The correction has:

```text
F2 = [0,0]
F3 = [0,1,2,2,2]
```

After correction:

```text
F2 = [0,0]
F3 = [0,0,0,0,0]
```

So the hidden quartet edge orientation preserves the binary Hesse delta split and kills the ternary double-six obstruction.

## BT1817 — Quartet slice search reducer

The post-BT1812 search is now sharply reduced:

```text
816 all triples
 -> 54 Hesse hinges
 -> 10 W(E6) stabilizer slices
 -> one 6-edge K4 quartet slice
 -> one oriented quartet edge
```

This is the executable contract for the missing BT1781 tuple data:

```text
1. Reproduce the 9980 vector before repair.
2. Project the F3 obstruction into one W(E6) size-6 hinge slice.
3. Identify a K4 quartet edge orientation whose F3 correction syndrome is [0,1,2,2,2].
4. Verify F2 and F3 left-kernel evaluations vanish after correction.
```

## Bottom line

```text
W(E6) does not select a single defect.
W(E6) selects a hidden K4 edge-slice.
The observed table defect is one oriented edge inside that slice.
The fibre law is now localized to orientation on a 4-state D4/GKP quartet.
```

## Files

- `analysis/bt1815_quartet_slice_geometry.py`
- `data/bt1815_quartet_slice_geometry.json`
- `analysis/bt1816_oriented_quartet_fibre_law.py`
- `data/bt1816_oriented_quartet_fibre_law.json`
- `analysis/bt1817_quartet_slice_search_reducer.py`
- `data/bt1817_quartet_slice_search_reducer.json`
- `analysis/BT1815_BT1817_quartet_fibre_law_summary.md`
