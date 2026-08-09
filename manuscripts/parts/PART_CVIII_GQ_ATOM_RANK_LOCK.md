# Part CVIII — GQ Atom Rank-Lock and Lambda-Spread Hidden Heavy Factor

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Part CVII showed that W33 reconstructs B29/C9.

This part shows the ranks are built from genuine generalized-quadrangle atoms.

For W(3,q),

```text
v = (q+1)(q^2+1),
```

```text
k = q(q+1),
```

```text
lambda = q-1,
mu = q+1.
```

Each point has

```text
h = v - 1 - k = q^3
```

non-neighbors.

A spread has size

```text
s = q^2 + 1.
```

## 1. Rank reconstruction from GQ atoms

The C/B rank pair is

```text
m = q^2,
```

and

```text
n = h + lambda = q^3 + q - 1.
```

Then

```text
n + m + 1 = v - 1
```

for every q.

The hidden gap is

```text
n - m = q^3 - q^2 + q - 1.
```

This factors as

```text
n - m = (q-1)(q^2+1) = lambda * s.
```

So the hidden sector is exactly:

```text
lambda * spread size.
```

## 2. W33 specialization

For q=3,

```text
lambda=2,
s=q^2+1=10.
```

Therefore

```text
lambda*s = 2*10 = 20.
```

Also,

```text
m=q^2=9,
```

and

```text
n=q^3+lambda=27+2=29.
```

Thus

```text
B29/C9
```

is reconstructed as

```text
29 = 27 + 2,
9 = 3^2.
```

## 3. q=3 lock

The hidden gap equals half the carrier exactly when

```text
(q-1)(q^2+1) = ((q+1)(q^2+1))/2.
```

Canceling q^2+1,

```text
2(q-1)=q+1.
```

So

```text
q=3.
```

Equivalently,

```text
lambda = mu/2.
```

For q=3,

```text
lambda/mu = 2/4 = 1/2.
```

Therefore

```text
(lambda * spread) / v = 1/2.
```

## 4. Complete-pair consequence

For q=3,

```text
(n-m)(v-1)=20*39=780=binomial(40,2).
```

So the complete-pair Weyl tail is really

```text
(lambda * spread) * (v-1).
```

## 5. Meaning

The hidden heavy 20-sector is not merely v/2.

It is more structurally:

```text
20 = lambda * spread size = 2 * 10.
```

The miracle is that for q=3,

```text
lambda * spread = v/2.
```

This is the GQ-atom origin of the hidden-heavy Weyl tail.

## 6. Structural slogan

```text
The hidden heavy 20-sector is lambda times a spread.
```

This ties the B29/C9 rank lock to the local SRG parameter lambda and the global spread size q^2+1.