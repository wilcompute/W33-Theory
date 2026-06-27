# BT1870 — Gauge-Contrast Quotient Construction

BT1870 turns the BT1865 commutation defect into subsystem bookkeeping.

## Starting point

The six cyclic-distance rows split as:

```text
one commuting global clock row = H1+H2+H3+H4+H5+H6
five noncommuting distance contrasts
```

The commutation defect has rank 5, exactly matching the five contrast directions.

## Quotient

```text
distance row space = span(H1,...,H6)
stabilizer subspace = span(H1+H2+H3+H4+H5+H6)
gauge contrast subspace dimension = 5
quotient dimension = 1
```

## Accounting

Payload accounting becomes:

```text
payload symbols = 66
face X rank = 42
global Z rank = 1
gauge contrasts = 5
```

The naive BT1868 skeleton had:

```text
k = 66 - 42 - 1 = 23
```

After accounting for the five contrast gauges:

```text
k_effective = 23 - 5 = 18
```

This matches the BT1862 payload kernel dimension.

## Interpretation

The five distance contrasts are not stabilizers and should not be discarded.  They are gauge handles.  The quotient recovers the 18-dimensional payload sector already seen by the combined GF(3) check complex.

## Remaining obstruction

The quotient does not hide the BT1869 failure.  The weight-2 X logical defect remains unless a dual/local Z structure is added.

Promising repairs:

```text
1. add dual face rows from the Szilassi face-adjacency side
2. promote distance contrasts into measured gauge checks with paired X partners
3. construct a hypergraph-product-like doubled K12/F12 code
```

Boundary: gauge quotient bookkeeping only; not a completed subsystem code or distance proof.
