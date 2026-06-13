# BT930 — Chain-to-tetracode \(E_8\) map search

BT930 independently maps the BT925/BT928 chain symplectic form into the W33 tetracode \(E_8\) witness.

## Target witness

The target is the MCCCLXXXVIII tetracode \(E_8\) root-system packet:

```text
four A2 planes + W33-derived ternary tetracode glue -> 240 roots.
```

The imported packet verifies:

- root count 240;
- rank 8;
- source profile 24 A2 roots + 216 tetracode-glue roots;
- simple-root Gram determinant 1.

## Result

BT930 extracts the tetracode simple-root Gram, reduces it mod 2, builds a symplectic basis, and finds a mod-2 isometry from the BT928 chain basis:

```text
M^T G_tetracode M = B_chain mod 2.
```

The integral 0/1 lift has determinant 1 and gives a positive-definite determinant-1 \(E_8\) Gram in tetracode metric coordinates.

## Honest boundary

As in BT929, this is an explicit basis-dependent isometry, not a canonical selector. But BT929 and BT930 now independently link the same chain shadow to both metric \(E_8\) witnesses: vertex and tetracode.

## Witness

```text
analysis/bt930_chain_to_tetracode_e8_map_search.py
data/bt930_chain_to_tetracode_e8_map_search.json
```
