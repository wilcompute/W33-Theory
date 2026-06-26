# BT1818--BT1820 execution summary

## BT1818 — Quartet operator labeling

BT1818 upgrades the hidden quartet from an abstract K4 to an operator-labeled local fibre square:

```text
00 -> I
01 -> X
10 -> Z
11 -> XZ
```

Interpretation:

```text
00 = origin / no half-shift
01 = position half-shift
10 = momentum half-shift
11 = both-quadrature half-shift / Y-like corner
```

The observed W(E6) hinge support is:

```text
(10,22,44)
```

and it maps to the diagonal edge:

```text
00 -> 11
```

so the observed defect is the XZ/both-quadrature flip inside the D4/GKP quartet.

Boundary preserved: this labels the quartet as a local fibre model. It does not claim the true BT1781 tuple data has already supplied canonical physical operators.

## BT1819 — Tuple-list pass/fail harness

BT1819 commits an executable harness:

```text
analysis/bt1819_tuple_list_pass_fail_harness.py
```

It accepts future true BT1781 materialized tuple data in any of these forms:

```text
list of records with table/label/table_label
object with rows list
object with counts dict or counts list in expected table order
```

The pass contract is:

```text
1. Reproduce the 9980 vector exactly.
2. Apply T010=-2, T210=-2, T222=+2.
3. F2 left-kernel evaluations vanish after correction.
4. F3 left-kernel evaluations vanish after correction.
```

Boundary preserved: no tuple rows are fabricated or embedded. The harness is ready for real tuple lists.

## BT1820 — Quartet law paper insert

BT1820 adds a manuscript-ready LaTeX insert:

```text
analysis/BT1820_quartet_law_paper_insert.tex
```

Core theorem statement:

```text
W(E6) selects the hidden quartet edge-slice.
The observed table defect is one oriented edge inside that slice.
The oriented edge law is two endpoint losses plus one edge-target gain, in units of 2.
```

For the observed edge:

```text
T010:-2, T210:-2, T222:+2
```

Syndrome cancellation:

```text
observed F3   = [0,2,1,1,1]
correction F3 = [0,1,2,2,2]
adjusted F3  = [0,0,0,0,0]
```

## Bottom line

```text
BT1818: the quartet is the local F2^2 D4/GKP Pauli square.
BT1819: the true tuple-list pass/fail harness is ready.
BT1820: the quartet fibre-law theorem is paper-ready.
```

## Files

- `analysis/bt1818_quartet_operator_labeling.py`
- `data/bt1818_quartet_operator_labeling.json`
- `analysis/bt1819_tuple_list_pass_fail_harness.py`
- `data/bt1819_tuple_list_pass_fail_harness_schema.json`
- `analysis/BT1820_quartet_law_paper_insert.tex`
- `analysis/BT1818_BT1820_execution_summary.md`
