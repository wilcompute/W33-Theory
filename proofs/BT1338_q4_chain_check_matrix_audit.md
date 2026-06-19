# BT1338 -- Q4 Chain Check Matrix Audit

## Purpose

BT1338 executes the stabilizer/check-matrix extraction requested after BT1336.

## Extracted object

The script constructs the literal cubical Q4 chain complex:

```text
C2 -> C1 -> C0
```

with:

```text
|C0| = 16 vertices
|C1| = 32 edges
|C2| = 24 square faces
```

It exports the explicit sparse supports for:

```text
partial_1: edge -> two endpoint vertices
partial_2: square face -> four boundary edges
```

## Rank result

Over F2:

```text
rank(partial_1) = 15
rank(partial_2) = 17
n_edges = 32
k_naive = 32 - 15 - 17 = 0
```

## Consequence

The literal contractible 4-cube chain complex does not by itself produce a [[32,4,4]] code. It produces no logical qubits under the naive CSS rank formula.

Therefore the W33 [[32,4,4]] object requires one additional certificate layer:

```text
toroidal quotient / gauge quotient / check-rank reduction preserving d=4
```

## Interpretation

This is not a dead end. It localizes the missing mathematical object precisely. The next stabilizer task is no longer vague: construct the quotient or gauge subsystem that reduces total independent check rank by four while preserving the distance-4 logical operators.

## Files

```text
tools/bt1338_extract_q4_chain_checks.py
data/bt1338_q4_chain_check_matrices.json
```
