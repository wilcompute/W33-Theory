# BT1862 — Homology / Logical-Basis Computation

BT1862 replaces BT1859's upper/lower-bound language with exact GF(3) linear algebra for the combined check complex.

## Matrix

```text
symbols = 72
edge symbols = 66
parity symbols = 6
face rows = 44
distance rows = 6
total rows = 50
field = GF(3)
```

## Exact ranks

```text
rank(face rows) = 42
rank(distance rows) = 6
rank(combined 44+6 rows) = 48
rank(combined rows on payload edges only) = 48
```

So the row dependencies are:

```text
face-row dependencies = 2
combined-row dependencies = 2
```

## Kernel dimensions

```text
full 72-symbol kernel dimension = 24
payload-only 66-edge kernel dimension = 18
parity/gauge degrees = 6
```

## Classical check-code distance

The combined check complex has no nonzero words of weight 1, 2, or 3.  A weight-4 word exists:

```text
edge(1,5) + edge(2,5) + 2*edge(5,8) + 2*edge(5,9) = 0 syndrome
```

Therefore:

```text
classical check-code distance = 4
```

## Interpretation

The 44 face rows plus 6 distance/parity rows improve the raw six-row compiler from BT1856's distance 2 to a classical check-code distance of 4.  The remaining payload logical space is 18-dimensional, plus 6 parity/gauge degrees in the full 72-symbol system.

Boundary: this is exact GF(3) classical linear algebra.  It is not yet a quantum CSS/subsystem distance theorem, because commutation, gauge fixing, and quantum logical operators remain to be constructed.
