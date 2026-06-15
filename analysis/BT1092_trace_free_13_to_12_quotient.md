# BT1092 — Explicit 13-to-12 trace-free quotient matrix

BT1092 turns the BT1090 reservoir intertwiner into an explicit linear algebra object.

## Fixed block

Let the fixed/gauge-perp block be

```text
F13 = span(e0, e1, ..., e12).
```

Its scalar trace line is

```text
u = e0 + e1 + ... + e12.
```

The trace-free quotient has dimension

```text
13 - 1 = 12.
```

## Quotient matrix

Use the quotient map

```text
pi12 : F13 -> C^12
```

given by the 12 by 13 matrix whose row `i` is

```text
e_i^T - e_12^T,  i=0,...,11.
```

Equivalently,

```text
pi12(x0,...,x12) = (x0-x12, x1-x12, ..., x11-x12).
```

## Checks

```text
rank(pi12) = 12
ker(pi12) = span(1,1,...,1)
pi12(u) = 0
```

Thus `pi12` is exactly the trace-removal quotient required by BT1090.

## Reservoir intertwiner update

The BT1090 map can now be written explicitly as

```text
K = (1/3) * [pi12 pr_F13(0) + pi12 pr_F13(1) + pi12 pr_F13(2)].
```

It has rank 12 when the three fixed blocks are identified with the same gauge packet basis.

## Boundary

This fixes the linear quotient. The remaining representation choice is the basis identification

```text
C^12 ~= A1 direct_sum A3 direct_sum A8.
```

That identification belongs to the centralizer/gauge-module ledger rather than the quotient map itself.
