# BT1899-BT1901 summary

Executed BT1899-BT1901.

## BT1899

Added a combined Holonet insert:

```text
papers/BT1899_holonet_residual_and_guard_insert.tex
```

It combines the BT1896 residual-language clarification with the BT1897 guard-envelope theorem:

```text
finite machine-complete architecture, with remaining physical/continuum identifications classified
2^11 = 2048
2048 - 1600 = 448 = 7*64
64 = 24 dark + 24 loss + 16 parity
```

## BT1900

Added the demonstrator raw-shot schema and validator:

```text
schemas/bt1900_demonstrator_raw_shot_schema.json
analysis/bt1900_demonstrator_raw_shot_validator.py
```

The validator checks required raw-shot fields, tetrad/slot/tick/time-bin ranges, logical-pair labels, witness classes, booleans, and the 640-record basis-local schedule integrity.

## BT1901

Added the contextual-fraction estimator:

```text
analysis/bt1901_contextual_fraction_estimator.py
```

It reads the BT1900 JSONL shot table, estimates the diagonal contextual signal rate, subtracts the dark-reference click rate, corrects by the loss-probe estimate, and checks compatibility with target contextual fraction 1/10 under a z=2 normal window.

Boundary: TeX insert, raw-data validator, and first-pass estimator only; no continuum residual solution, hardware threshold, or final statistical analysis is claimed.
