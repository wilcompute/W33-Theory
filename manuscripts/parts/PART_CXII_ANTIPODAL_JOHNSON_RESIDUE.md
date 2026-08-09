# Part CXII — Antipodal Johnson Cover and 1+9+5+5 Residue Splitting

Status: theorem-grade structural extension  
Date: April 28, 2026

Part CXI identified the local fixed-spread residue as a six-letter object:

```text
10 bisections,
15 duads,
20 oriented triples.
```

This part studies the 20 oriented triples directly.

They form the Johnson graph

```text
J(6,3),
```

where two triples are adjacent exactly when they differ by one letter.

## Antipodal double cover

Complementation sends each oriented triple to its opposite half:

```text
A -> A^c.
```

This is a fixed-point-free involution pairing the 20 oriented triples into the 10 bisections.

The graph J(6,3) is an antipodal double cover of

```text
K10.
```

The full spectrum is

```text
9^1, 3^5, (-1)^9, (-3)^5.
```

## Even/odd complement split

Under complement parity, the oriented-triple space splits into:

```text
even sector: 10 = 1 + 9,
```

and

```text
odd sector: 10 = 5 + 5.
```

The even sector has spectrum

```text
9^1, (-1)^9.
```

This is exactly the K10 quotient.

The odd sector has spectrum

```text
3^5, (-3)^5.
```

Equivalently, the odd signed quotient squares to

```text
9 I_10.
```

## C9 appears again

The 10 bisections have one constant mode and nine nonconstant modes:

```text
10 = 1 + 9.
```

Thus

```text
C9 = nonconstant even quotient.
```

This is the same 9 that appeared as the nonconstant eigenspace of the 2-(10,4,2) incidence operator.

## Local B29 decomposition

The hidden 20 oriented-triple space refines as

```text
20 = 1 + 9 + 5 + 5.
```

Adding the extra C9 residue eigenspace gives

```text
B29 = 20 + 9.
```

Therefore

```text
B29 = (1+9+5+5)+9 = 1 + 2*9 + 5 + 5.
```

## Structural slogan

```text
The hidden 20 is J(6,3), an antipodal double cover of the ten bisections; its even quotient contains C9 and its odd sector splits 5+5.
```
