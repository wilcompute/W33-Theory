# 2026-05-22 - Levi Cycle Quotient Exact Sequence Theorem

## Breakthrough

The protected `81` is now identified as the **cycle rank of the Levi graph** of `W(3,3)`.

The Levi graph has:

```text
vertices = 40 points + 40 lines = 80
edges    = point-line flags = 160
connected = true
```

Therefore its first Betti number / cycle rank is

```text
160 - 80 + 1 = 81.
```

This is exactly the rank of the signed phase matrix.

## Exact sequence

The signed point/line relations are the cut/local-relation space of the Levi graph:

```text
rank = 80 - 1 = 79.
```

The full flag module has dimension

```text
160.
```

Therefore:

```text
0 -> cut(Levi)_79 -> R^Flags_160 -> cycle(Levi)_81 -> 0
```

The signed phase matrix `A` realizes this quotient into the quadrangle frame.

## Meaning

Previously:

```text
160 = 81 + 79
```

Now:

```text
160 flags = 81 Levi cycles + 79 Levi cuts
```

or:

```text
protected phase image = cycle space of the W33 Levi graph
nullspace = local point/line cut relation space
```

This makes the homological interpretation exact. The protected `81` is not just an analogy or a spectral rank; it is the cycle rank of the point-line incidence graph.

## Machine certificate

Added:

- `analysis/w33_levi_cycle_quotient_exact_sequence.py`
- `data/w33_levi_cycle_quotient_exact_sequence.json`

The script reconstructs W(3,3), builds the Levi graph, verifies connectedness, computes cycle rank `81`, verifies the signed local relation rank `79`, and checks that the quotient dimension equals the signed phase rank.
