# Part LXXXV — Two Spectral Shells of the Raw Triangle Operator

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

Parts LXXXI–LXXXIV normalized the completed L,S,Q triangle into a Dirac/Hodge complex.  This part studies the raw centered triangle operator before shell normalization.

Define

```text
H = [[0,    Bc,   Uc],
     [Bc^T, 0,    Mc],
     [Uc^T, Mc^T, 0 ]].
```

## 1. Exact spectrum

The raw operator has exact spectrum

```text
0^3,  (+/-sqrt(18))^39,  (+/-sqrt(72))^20.
```

Equivalently,

```text
Spec(H^2) = 0^3, 18^78, 72^40.
```

## 2. Shell projectors

The square decomposes as

```text
H^2 = 18 P_light + 72 P_heavy.
```

The light shell is

```text
P_light = P_{L15 + S15} + P_{L24 + Q24},
rank(P_light)=78=2(15+24).
```

The heavy shell is

```text
P_heavy = P_{S20 + Q20},
rank(P_heavy)=40=2*20.
```

The remaining shell is the three-dimensional mean sector.

Thus

```text
78 + 40 + 3 = 121.
```

## 3. Exact ratios

For q=3,

```text
18 = 2 q^2,
72 = 8 q^2 = 4*18.
```

So the nonzero shell scale ratio is exactly

```text
sqrt(72)/sqrt(18) = 2.
```

The complex mode split is

```text
59 = 39_light + 20_heavy.
```

## 4. Recovery of the normalized operator

The normalized triangle Dirac operator is recovered by shell-normalizing H:

```text
D = H( P_light/sqrt(18) + P_heavy/sqrt(72) ).
```

Thus the involutive/Hodge carrier is the unit-shell version of the raw two-shell operator.

## 5. Minimal polynomial

The raw operator satisfies

```text
H(H^2 - 18I)(H^2 - 72I)=0.
```

## 6. Structural slogan

```text
The completed W(3,3) triangle has an exact two-shell spectrum before normalization:
(15+24)_light + 20_heavy + 3_zero.
```

## Audit Implementation

See scripts/w33_two_spectral_shells_audit.py and
tests/test_w33_two_spectral_shells_audit.py for the executable audit surface.
