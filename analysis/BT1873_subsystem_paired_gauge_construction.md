# BT1873 — Subsystem Paired-Gauge Construction

BT1873 reuses the five distance contrasts correctly.

## Starting point

BT1872 supplies the stabilizer parent:

```text
[[66,13,3]]_3
```

with:

```text
X checks = 44 face rows, rank 42
Z checks = 12 signed dual vertex-star rows, rank 11
```

## Gauge input

BT1865 found that the six cyclic-distance rows decompose into:

```text
one global clock-sum direction
five distance contrasts
```

The five contrasts caused the naive CSS failure, but they are still useful as gauge refinements.

## Paired-gauge construction

The rank-5 commutation defect gives five canonical gauge pairs:

```text
5 Z-gauge distance contrasts
5 X-gauge partners from independent face-row combinations
```

So the subsystem accounting is:

```text
n = 66
stabilizer parent k = 13
gauge qudits r = 5
logical qudits after gauge accounting = 8
```

Candidate notation:

```text
[[66,8,>=3;5]]_3
```

The `>=3` is conditional on the BT1872 low-weight screen and still needs a full all-weight subsystem-distance proof.

## Important correction

The BT1869 weight-2 X defect is not fixed by the five contrast gauges.  It is fixed by the BT1872 dual vertex-star Z checks.  After that, the five distance contrasts can be treated as gauge refinements.

Boundary: finite symplectic gauge construction only; full gauge decoder and all-weight subsystem distance proof remain open.
