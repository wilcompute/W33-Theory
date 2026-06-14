# BT957 — Final combined E8 selector theorem

BT957 combines BT951, BT954, and BT956.

## Exact support layer

```text
support minimum = 60
support-minimal decompositions = 6
support profile = [6, 6, 6, 6, 6, 8, 10, 12]
shared pair = (90,144)
```

## Dual metric layer

Both independent metric gauges select the same support-minimal decomposition:

```text
[(3,68), (4,42), (38,65), (90,144)]
```

Vertex metric score:

```text
trace = 38
frobenius_squared = 444
max_abs_entry = 8
min_eigenvalue = 0.010596380201028571
```

Tetracode metric score:

```text
trace = 56
frobenius_squared = 1320
max_abs_entry = 16
min_eigenvalue = 0.004850303102819915
```

## Theorem insert

```text
paper/BT957_final_e8_selector_theorem_insert.tex
tools/integrate_bt957_final_selector_w33.py
```

## Reading

The selector is now fixed by exact support minimality plus agreement of the vertex and tetracode metric gauges.

## Remaining refinement

Identify the full transported tetracode stabilizer orbit of the selected minimizer.
