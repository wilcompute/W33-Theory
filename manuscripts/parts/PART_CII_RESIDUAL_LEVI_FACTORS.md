# Part CII — Residual Levi Factors and Parabolic Anatomy

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Part CI computed local orbit-stabilizer orders. This part identifies the residual stabilizers structurally.

## 1. 3-primary residuals

The ambient group is

```text
O(59,3).
```

### Null phase line

A 3-primary isotropic phase line has stabilizer

```text
P_null = 3^57 ⋊ (F3^× × O(57,3)).
```

So the null choice is a maximal parabolic reduction:

```text
O(59,3) -> 3^57 ⋊ (F3^× × O(57,3)).
```

### Anisotropic phase vectors

A norm +1 vector has stabilizer

```text
O^-(58,3).
```

A norm -1 vector has stabilizer

```text
O^+(58,3).
```

For projective anisotropic lines, one gets the extra sign on the line:

```text
Stab(<v_+>) = C2 × O^-(58,3).
```

```text
Stab(<v_->) = C2 × O^+(58,3).
```

## 2. 2-primary residuals

The ambient group is

```text
O_I(20,2).
```

The canonical vector

```text
Omega = (1,...,1)
```

has stabilizer

```text
O_I(20,2).
```

So selecting Omega breaks no 2-primary heavy symmetry.

An odd heavy vector has residual symmetry

```text
Sp(18,2)
```

at the order level.

An even non-Omega heavy vector has residual order

```text
2^35 |Sp(16,2)|.
```

The fixed-null quotient remains

```text
1 -> U_19 -> O_I(20,2) -> Sp(18,2) -> 1.
```

## 3. Meaning

The residual symmetry hierarchy is now:

```text
3-primary null choice -> parabolic.
```

```text
3-primary anisotropic choice -> even orthogonal.
```

```text
2-primary heavy choice -> symplectic quotient residuals.
```

And the fixed heavy vector Omega remains the unique completely rigid object: selecting it breaks nothing.

## 4. Structural slogan

```text
Null 3-primary phases leave a parabolic; anisotropic 3-primary phases leave even orthogonal groups; Omega leaves all 2-primary heavy symmetry intact.
```

This converts residual symmetry from orbit-size data into standard Levi/parabolic group anatomy.