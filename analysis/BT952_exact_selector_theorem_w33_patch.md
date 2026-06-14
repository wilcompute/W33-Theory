# BT952 — Exact selector theorem patch for w33_paper.tex

BT952 writes the new support-minimal result into a theorem insert for the heavy-math manuscript.

## Superseded claim

The earlier support-76 selector candidate is false as a minimum.

## New exact theorem

```text
minimum support sum = 60
minimizer count = 6
unique sorted support profile = [6, 6, 6, 6, 6, 8, 10, 12]
```

The six minimizing decompositions all share the hyperbolic pair `(90,144)` in the BT925 mask gauge.

## w33 patch files

```text
paper/BT952_exact_e8_selector_theorem_insert.tex
tools/integrate_bt952_exact_selector_w33.py
data/bt952_exact_selector_theorem_w33_patch.json
```

## Boundary

The full quotient under the transported tetracode stabilizer is not asserted yet. The quotient problem has been reduced to a sharply finite target: six support-60 minimizers.

Run in a full checkout:

```bash
python tools/integrate_bt952_exact_selector_w33.py
```
