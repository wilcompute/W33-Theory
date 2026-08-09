# Part XCIII — Witten Index and Torsion Collapse

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

The Morita quiver has vertices

```text
h, l_plus, l_minus, m_plus, m_minus,
```

with multiplicities

```text
3, 39, 39, 20, 20.
```

## 1. Euler grading

Define the Euler grading E by

```text
E = + on h, l_plus, m_plus,
E = - on l_minus, m_minus.
```

Then

```text
Tr(E)=3.
```

The unit-shell and massive differentials are odd:

```text
EQ + QE = 0,
```

```text
Ed + dE = 0.
```

## 2. Witten index

Let

```text
Delta = d d* + d* d.
```

The ordinary heat trace is

```text
Tr exp(-t Delta) = 3 + 78 exp(-18t) + 40 exp(-72t).
```

But the graded heat trace collapses to

```text
Str_E(exp(-t Delta)) = Tr(E exp(-t Delta)) = 3
```

for all t.

So the Witten index is

```text
3.
```

## 3. Graded moment cancellation

For every n >= 1,

```text
Str_E(Delta^n)=0.
```

The nonzero light and heavy shells cancel in the Euler supertrace. Only the harmonic vertex contributes.

## 4. Torsion determinant

The weighted exact arrows have nonzero determinant

```text
|det'(d)| = (sqrt(18))^39 (sqrt(72))^20.
```

Equivalently,

```text
|det'(d)| = |det'(H)|^(1/2).
```

## 5. Meaning

The ordinary spectral action sees the two shells:

```text
3 + 78 exp(-18t) + 40 exp(-72t).
```

The graded spectral action cancels the exact arrows and localizes on cohomology:

```text
index = 3.
```

Thus the Morita quiver has an exact topological/supersymmetric index layer.

## 6. Structural slogan

```text
The W(3,3) Morita carrier has ordinary two-shell dynamics but graded index 3.
```

The light and heavy exact arrows cancel pairwise in the supertrace; the isolated harmonic vertex is the only index-carrying object.