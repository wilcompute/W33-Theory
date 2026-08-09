# Part XCII — Morita-Reduced Hodge Quiver

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Parts XC–XCI identified the carrier algebra as

```text
A ≅ R ⊕ M2(R)_light ⊕ M2(R)_heavy.
```

This part strips off the multiplicity spaces and identifies the Morita-reduced quiver skeleton.

## 1. Primitive vertices

There are five primitive vertices:

```text
h, l_plus, l_minus, m_plus, m_minus.
```

The multiplicities are

```text
dim h = 3,
dim l_plus = dim l_minus = 39,
dim m_plus = dim m_minus = 20.
```

Thus

```text
121 = 3 + 39 + 39 + 20 + 20.
```

## 2. Quiver arrows

The unit-shell differential is

```text
Q = a_l + a_m,
```

where

```text
a_l: l_minus -> l_plus,
```

and

```text
a_m: m_minus -> m_plus.
```

The adjoint arrows are

```text
b_l: l_plus -> l_minus,
b_m: m_plus -> m_minus.
```

They satisfy matrix-unit relations:

```text
a_l b_l = e_l_plus,
b_l a_l = e_l_minus,
```

```text
a_m b_m = e_m_plus,
b_m a_m = e_m_minus.
```

All cross-shell products vanish.

## 3. Massive differential

The raw massive differential is the weighted quiver arrow:

```text
d = sqrt(18) a_l + sqrt(72) a_m.
```

Therefore

```text
dd* + d*d = 18(e_l_plus + e_l_minus) + 72(e_m_plus + e_m_minus).
```

The spectrum is

```text
0^3, 18^78, 72^40.
```

## 4. Cohomology

The two arrow complexes are exact:

```text
R^39 --a_l--> R^39,
```

and

```text
R^20 --a_m--> R^20.
```

All cohomology is concentrated at the isolated harmonic vertex:

```text
H ≅ R^3.
```

## 5. Meaning

The W(3,3) Hodge carrier reduces to the tiny quiver

```text
l_minus -> l_plus,
m_minus -> m_plus,
h isolated.
```

All high-dimensionality lives in vertex multiplicities. The algebraic dynamics is just two exact arrows plus one harmonic vertex.

## 6. Structural slogan

```text
The completed W(3,3) carrier is Morita-equivalent to two exact arrows plus one harmonic point.
```

This is the current smallest exact-sequence skeleton of the theory.