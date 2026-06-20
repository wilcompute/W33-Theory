# BT1384 -- Exact S3 Gauge MaxSAT Export

## Purpose

BT1384 turns the BT1379 S3 gauge Max-2CSP frontier into a solver-ready weighted partial MaxSAT instance.

## Encoding

Variables:

```text
40 W33 line variables * 6 S3 labels = 240 one-hot label variables
540 skew-line constraints = 540 satisfaction variables
Total variables = 780
```

Hard clauses:

```text
one-hot line label constraints
root line fixed to identity
satisfaction variable equivalences for all 540 edges and all 36 label pairs
```

Soft clauses:

```text
one unit-weight soft clause per satisfaction variable
```

Counts:

```text
hard clauses = 20086
soft clauses = 540
total clauses = 20626
top weight = 541
```

## Objective

Maximize the number of identity residual edges.  The BT1373 witness has score:

```text
210
```

## Files

```text
tools/bt1384_export_s3_gauge_maxsat.py
data/bt1384_s3_gauge_maxsat_manifest.json
```

Running the tool emits the full WCNF file at:

```text
data/generated/bt1384_s3_gauge_maxsat.wcnf
```

## Boundary

BT1384 exports the exact instance.  It does not solve global optimality.  External MaxSAT/ILP/SAT solvers can now attack the 210-score frontier directly.
