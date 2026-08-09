# Part CVI — SRG Layer Decomposition of the Complete-Pair Weyl Tail

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Part CV connected the missing Weyl degree tail to

```text
binomial(40,2)=780.
```

This part decomposes that identity through the SRG atoms of W(3,3).

W(3,3) has strongly regular graph parameters

```text
(v,k,lambda,mu)=(40,12,2,4).
```

For each point,

```text
k=12
```

points are collinear neighbors, while

```text
40 - 1 - 12 = 27
```

points are non-neighbors.

Thus

```text
39 = 12 + 27.
```

## 1. Hidden-layer multiplier

The hidden heavy count is

```text
20 = 40/2.
```

Multiplying the local split by 20,

```text
20*39 = 20*12 + 20*27.
```

That is

```text
780 = 240 + 540.
```

So the complete-pair count decomposes as:

```text
binomial(40,2) = #W33 edges + #W33 nonedges.
```

## 2. Weyl-tail refinement

The missing Weyl degrees satisfy

```text
sum d_tail = 780 = 20(12+27).
```

The missing Weyl exponents satisfy

```text
sum e_tail = 760 = 780 - 20.
```

The degree/exponent defect is one per hidden layer:

```text
sum(d_tail - e_tail)=20.
```

## 3. q=3 layer readings

For q=3,

```text
12 = q(q+1),
```

```text
27 = q^3,
```

```text
39 = q^3 + q(q+1).
```

The triangle count also factors:

```text
160 = 20*8
```

with

```text
8 = q^2 - 1.
```

The points and lines factor as

```text
40 = 20*2.
```

## 4. Meaning

The hidden heavy 20-sector is a universal layer unit:

```text
points, lines, edges, nonedges, pairs, triangles, and Weyl-tail sums
```

all factor through the same hidden layer count 20.

This explains why the Weyl degree tail lands exactly on the complete-pair count of the 40-point W(3,3) carrier.

## 5. Structural slogan

```text
The hidden 20 converts local SRG adjacency data into global W33 pair geometry.
```

This is the SRG-layer version of the hidden-heavy Weyl tail.