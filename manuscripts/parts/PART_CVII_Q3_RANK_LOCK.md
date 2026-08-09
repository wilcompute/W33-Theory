# Part CVII — q=3 Rank-Lock and W33 Reconstruction of B29/C9

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Part CVI showed that the hidden 20 converts local W33 SRG data into global pair geometry.

This part shows something stronger:

```text
W(3,3) reconstructs the ranks 29 and 9.
```

The B29/C9 bridge is not an arbitrary later fit.

## 1. Rank reconstruction from v=40

Let

```text
v = 40.
```

The hidden layer count is

```text
g = v/2 = 20.
```

For a Weyl degree tail from C_m to B_n,

```text
sum_{i=m+1}^{n} 2i = (n-m)(n+m+1).
```

To match the W33 complete-pair count,

```text
binomial(v,2) = (v/2)(v-1),
```

we require

```text
n - m = v/2
```

and

```text
n + m + 1 = v - 1.
```

Equivalently,

```text
n + m = v - 2.
```

Solving gives

```text
n = 3v/4 - 1,
```

and

```text
m = v/4 - 1.
```

For v=40,

```text
n=29, m=9.
```

So W33 reconstructs

```text
B29 and C9.
```

## 2. q=3 lock

For W(3,q),

```text
v = (q+1)(q^2+1).
```

The building ranks found above are also

```text
m = q^2,
```

and

```text
n = q^3 + 2
```

when q=3.

Requiring

```text
n - m = v/2
```

gives

```text
q^3 - 3q^2 - q + 3 = 0.
```

This factors as

```text
(q-3)(q^2-1)=0.
```

For prime powers q > 1, the only solution is

```text
q=3.
```

The companion condition

```text
n + m + 1 = v - 1
```

also reduces to

```text
q=3.
```

## 3. Meaning

The chain is now rigid:

```text
W33 v=40 -> g=v/2=20 -> (n,m)=(29,9) -> B29/C9.
```

In q-language:

```text
m=q^2, n=q^3+2
```

is compatible with the W(3,q) point count only when

```text
q=3.
```

So the hidden-heavy Weyl-tail bridge is q=3-locked.

## 4. Structural slogan

```text
The 40-point W33 carrier does not merely fit B29/C9; it reconstructs B29/C9.
```

This upgrades the complete-pair Weyl tail into a rank-rigidity theorem.