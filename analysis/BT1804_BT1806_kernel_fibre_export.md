# BT1804--BT1806 kernel geometry, fibre ansatz, and Schlaefli export

## BT1804 — kernel geometry

BT1804 interprets the BT1801 left-kernel basis against the transported Hesse table rows.

The key structural result is that the two binary relations are not arbitrary:

```text
F2 relation 0 = all nine nonconcurrent tables with delta = 1
F2 relation 1 = all nine nonconcurrent tables with delta = 2
```

Both halves are balanced across the three Hesse coordinates `i`, `j`, and `s`, and each has double-six column total `6` for every one of the 36 double-six checks.

The ternary relations behave differently. Their count-vector evaluations are:

```text
F3 relation count sums mod 3 = [0, 2, 1, 1, 1]
```

So the observed count vector respects the binary defect split but fails four of the five ternary double-six/E6 relations. That isolates the missing layer: binary Hesse geometry is visible, but ternary fibre geometry is still unresolved.

## BT1805 — nonuniform fibre ansatz

BT1805 tests the constrained `12 = 3 x 4` table-local fibre idea against the BT1801 relations.

Observed syndrome:

```text
F2_eval = [0, 0]
F3_eval = [0, 2, 1, 1, 1]
```

A table-local model can fit the counts tautologically, but the meaningful question is how far the observed vector is from the pure ternary double-six constraints. The nearest even-count repair found is tiny:

```text
T010: 578 -> 576  (-2)
T210: 578 -> 576  (-2)
T222: 560 -> 562  (+2)
L1 adjustment size = 6
adjusted F3_eval = [0,0,0,0,0]
```

This says the missing fibre rule is not a global failure of the H27/E6 scaffold. It is a very small ternary correction concentrated on the special triple `T010`, `T210`, `T222`.

## BT1806 — Schlaefli orbit export

BT1806 exports the exact orbit-classification payload:

```text
Schlaefli graph: 27 vertices, 216 edges, SRG(27,16,10,8)
Tritangent supports: 45 triples
BT1795 image: 18 support-line indices
Expected automorphism order: 51840
```

Committed portable files:

```text
data/bt1806_schlafli_graph.dimacs
analysis/bt1806_schlafli_orbit_export.gap
analysis/bt1806_schlafli_orbit_export.sage
```

The DIMACS file gives the Schlaefli graph with explicit coordinate-labelled vertices. The GAP and Sage files include the tritangent support triples and the BT1795 image, so the W(E6) orbit/stabilizer computation can be run outside NetworkX.

## Bottom line

```text
BT1804: binary kernel = Hesse delta split; ternary kernel = genuine E6/fibre obstruction.
BT1805: pure F3 syndrome is missed by only a three-table even correction.
BT1806: exact Schlaefli/E6 orbit payload exported in DIMACS/GAP/Sage form.
```

## Files

- `analysis/bt1804_kernel_geometry.py`
- `data/bt1804_kernel_geometry.json`
- `analysis/bt1805_nonuniform_fibre_ansatz.py`
- `data/bt1805_nonuniform_fibre_ansatz.json`
- `analysis/bt1806_schlafli_orbit_export.py`
- `data/bt1806_schlafli_orbit_export.json`
- `data/bt1806_schlafli_graph.dimacs`
- `analysis/bt1806_schlafli_orbit_export.gap`
- `analysis/bt1806_schlafli_orbit_export.sage`
