# Part CIV — Weyl-Tail Hidden-Heavy Theorem

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Part CIII found the building pair

```text
B_29(3)
```

on the full 3-primary 59-mode phase space, and

```text
C_9(2)
```

on the 2-primary heavy quotient.

This part identifies the hidden 20-sector as the Coxeter/Weyl tail from C9 to B29.

## 1. Rank gap

```text
29 - 9 = 20.
```

So the heavy 20-sector is the rank gap between the full 3-primary building and the heavy 2-primary symplectic building.

## 2. Exponent tail

The B_n/C_n Weyl exponents are

```text
1, 3, 5, ..., 2n-1.
```

Thus

```text
B_29: 1, 3, ..., 57,
```

while

```text
C_9: 1, 3, ..., 17.
```

The tail is

```text
19, 21, 23, ..., 57.
```

It has exactly

```text
20
```

entries.

## 3. Coxeter gap

The Coxeter numbers are

```text
h(B_29)=58,
h(C_9)=18.
```

So

```text
58 - 18 = 40 = 2*20.
```

## 4. Positive-root gap

The number of positive roots in type B_n/C_n is

```text
n^2.
```

Therefore

```text
29^2 - 9^2 = 841 - 81 = 760.
```

But the tail exponent sum is

```text
19 + 21 + ... + 57 = 760.
```

So

```text
sum(tail exponents) = #Phi^+_B29 - #Phi^+_C9.
```

Equivalently,

```text
760 = 20(29+9).
```

## 5. Weyl group ratio

The Weyl group order is

```text
|W(B_n)| = |W(C_n)| = 2^n n!.
```

Therefore

```text
|W(B_29)| / |W(C_9)| = 2^20 * (29!/9!).
```

The factor

```text
2^20
```

is exactly the 2-primary hidden-heavy torsion order.

## 6. Meaning

The hidden 20-sector is simultaneously:

```text
rank gap,
```

```text
number of missing Weyl exponents/degrees,
```

```text
half the Coxeter-number gap,
```

```text
the 2^20 Weyl sign-tail factor,
```

and

```text
positive-root gap divided by 29+9.
```

This is the Coxeter-tail interpretation of the hidden heavy sector.

## 7. Structural slogan

```text
The hidden heavy 20-sector is the Weyl tail between C9 and B29.
```

This makes the heavy sector visible simultaneously in ranks, exponents, Coxeter numbers, positive roots, and Weyl sign factors.