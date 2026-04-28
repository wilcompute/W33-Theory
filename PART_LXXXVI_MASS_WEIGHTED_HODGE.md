# Part LXXXVI — Mass-Weighted Hodge Factorization

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

Part LXXXV found the raw two-shell operator

```text
H^2 = 18 P_light + 72 P_heavy.
```

This part shows that the raw shell structure is itself a Hodge complex.

## 1. Raw phase operator

Let Gamma be the sector grading from the Clifford carrier and define

```text
K = Gamma H.
```

Then

```text
K^2 = -H^2,
```

and K is skew-symmetric.

## 2. Mass-weighted supercharge

Define the raw, mass-weighted supercharge

```text
d = (H + K)/2,
```

and

```text
d* = (H - K)/2 = d^T.
```

Then

```text
d^2 = 0,
(d*)^2 = 0,
```

and

```text
d d* + d* d = H^2.
```

Thus the raw two-shell operator is a massive Hodge Laplacian.

## 3. Weighted exact complexes

The differential d has exactly three forward blocks:

```text
S15 -> L15,
```

with shell value

```text
18,
```

```text
Q24 -> L24,
```

with shell value

```text
18,
```

and

```text
Q20 -> S20,
```

with shell value

```text
72.
```

So the light shell is

```text
15 + 24,
```

and the heavy shell is

```text
20.
```

## 4. Massive Laplacian

```text
Delta_H = d d* + d* d = 18 P_light + 72 P_heavy.
```

Its spectrum is

```text
0^3, 18^78, 72^40.
```

## 5. Cohomology

The rank and nullity of d are

```text
rank(d)=59,
nullity(d)=62.
```

So

```text
dim H_d = 62 - 59 = 3.
```

The harmonic sector remains exactly the three module means.

## 6. Normalized recovery

The normalized supercharge is the unit-shell rescaling of d:

```text
Q = d( P_light/sqrt(18) + P_heavy/sqrt(72) ).
```

So the normalized Hodge complex is the unit-shell version of the massive Hodge complex.

## 7. Meaning

The raw completed W(3,3) triangle is not merely a two-shell operator. It is a two-shell massive Hodge complex:

```text
(15+24)_light + 20_heavy + 3_harmonic.
```

The shell hierarchy is inside the differential itself, not just inside the squared operator.

## Audit Implementation

See `scripts/w33_mass_weighted_hodge_audit.py` and `tests/test_w33_mass_weighted_hodge_audit.py` for the detailed audit of mass-weighted Hodge factorization and shell spectrum verification.
