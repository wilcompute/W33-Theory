# 2026-05-22 - Signed 3-adic Flag Tight-Frame Theorem

## Breakthrough

The signed phase matrix is not just a rank certificate. It is a finite tight frame.

Let

```text
A[flag,quadrangle] ∈ {-1,0,+1}
```

be the signed projective phase matrix for the visible/nonvisible flag-quadrangle pairing.
Let `U=|A|` be the unsigned incidence matrix and

```text
S = A A^T.
```

Then:

```text
|S| = U U^T      entrywise
S^2 = 160 S
rank(A) = 81
```

Therefore:

```text
S/160 is an exact rank-81 projector
S/81 is the Gram matrix of 160 unit vectors in R^81
```

with frame bound

```text
160/81.
```

## 3-adic angular structure

Each row of `A` has norm squared `81`. Off diagonal entries of `S` are exactly

```text
±1, ±3, ±9, ±27.
```

Therefore the normalized absolute inner products are

```text
1/81, 1/27, 1/9, 1/3
```

or, in descending order,

```text
3^-1, 3^-2, 3^-3, 3^-4.
```

So the signed flag surface is a `3`-adic angular frame.

## Entry distribution

Off diagonal signed distribution:

```text
-27: 648
 -9: 1296
 -3: 5724
 -1: 5076
  1: 7884
  3: 2916
  9: 1584
 27: 312
```

Including diagonal:

```text
81: 160
```

Spectrum:

```text
160^81 + 0^79
```

## Interpretation

The unsigned layer gives the flag association scheme.
The signed layer is a phase-lift of that scheme that destructively interferes down to the protected `81`-dimensional homology sector.

```text
unsigned flags: 160-dimensional combinatorial surface
signed phases: rank-81 tight frame / projector
```

This is the most precise current meaning of the phrase:

```text
phase protects homology
```

## Machine certificate

Added:

- `analysis/w33_signed_flag_tight_frame.py`
- `data/w33_signed_flag_tight_frame.json`

The script reconstructs W(3,3), builds the signed matrix, verifies `|AA^T|=UU^T`, verifies `S^2=160S`, computes rank `81`, and records the signed entry distribution.
