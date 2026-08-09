# Part CIII — Arithmetic Buildings and Generator Counts

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Part CII identified residual Levi/parabolic anatomy. This part turns that residual symmetry into the associated finite buildings.

## 1. 3-primary building

The 3-primary phase module is

```text
V_3 = F3^59
```

with Witt decomposition

```text
V_3 ≅ H^29 ⊕ <-1>.
```

Thus the 3-primary side carries the orthogonal polar building

```text
B_29(3),
```

or equivalently the parabolic quadric geometry

```text
Q(58,3).
```

The maximal totally singular generators have vector dimension

```text
29.
```

Their count is

```text
product_{i=1}^{29}(3^i+1).
```

The isotropic line count is

```text
(3^58 - 1)/2.
```

## 2. 2-primary building

The 2-primary heavy module has the fixed vector

```text
Omega = (1,...,1).
```

The moving quotient is

```text
Omega^perp / <Omega> ≅ F2^18.
```

This carries the symplectic building

```text
C_9(2).
```

The Lagrangian generators have dimension

```text
9
```

in the quotient, and lift to 10-dimensional even flats in F2^20 containing Omega.

Their count is

```text
product_{i=1}^{9}(2^i+1).
```

## 3. Rank identity

The full 3-primary building rank is

```text
29.
```

The heavy 2-primary symplectic rank is

```text
9.
```

The difference is

```text
29 - 9 = 20,
```

exactly the hidden heavy-sector dimension.

Also,

```text
59 = 2*29 + 1,
```

and

```text
20 = 2*9 + 2.
```

## 4. Meaning

The full nonzero 59-mode carrier supports a rank-29 orthogonal building.

The hidden heavy 20-mode carrier supports a rank-9 symplectic building after quotienting by Omega.

The bridge

```text
29 - 9 = 20
```

is a new structural link between the 3-primary full phase space and the 2-primary heavy phase space.

## 5. Structural slogan

```text
The full 59-mode phase space is a B_29(3) building; the hidden 20-mode heavy phase space hides a C_9(2) building; their rank gap is the heavy sector itself.
```

This gives the local arithmetic phase spaces their finite-building interpretation.