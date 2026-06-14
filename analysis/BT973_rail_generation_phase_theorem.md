# BT973 — Rail generation and phase bookkeeping theorem

BT973 writes the first downstream theorem using the final selector rails.

## Selector data

```text
final selector = [[3,68], [4,42], [38,65], [90,144]]
rail support sums = [12,12,14,22]
rail xor masks = [71,46,91,234]
```

## Generation faces

```text
[(0,1,3), (0,2,3), (1,2,3)]
```

Complementary face:

```text
(0,1,2)
```

## Phase bookkeeping

```text
phase scores = [16,16,19,27]
ABI light-rail order = [1,0]
```

## Boundary

This is selector-fixed gauge/bookkeeping data. It does not assert fitted CKM/PMNS constants or field-label predictions.

## Witness

```text
paper/BT973_rail_generation_phase_theorem_insert.tex
tools/integrate_bt973_rail_generation_phase_w33.py
data/bt973_rail_generation_phase_theorem.json
```
