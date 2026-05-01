# Part CI — Local Stabilizers and Orbit Quotients

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Parts XCVIII–C identified the local arithmetic phase symmetries:

```text
O(59,3)
```

on the full 3-primary 59-mode phase space, and

```text
O_I(20,2)
```

on the 2-primary heavy 20-mode phase space.

This part computes the stabilizers of the local phase strata.

## 1. 3-primary stabilizers

The 3-primary phase lines split into three projective orbits:

```text
Q=0: (3^58 - 1)/2,
```

```text
Q=+1: (3^58 - 3^29)/2,
```

```text
Q=-1: (3^58 + 3^29)/2.
```

For each type, the residual symmetry is the corresponding orbit stabilizer:

```text
Stab(line) = |O(59,3)| / |Orbit(line)|.
```

So choosing a 3-primary phase line breaks the full arithmetic symmetry to one of three exact residual groups: null, plus, or minus.

## 2. 2-primary stabilizers

The 2-primary heavy phase space has four orbits:

```text
{0},
```

```text
{Omega},
```

```text
odd vectors: 2^19,
```

and

```text
even nonzero vectors not Omega: 2^19 - 2.
```

The canonical vector

```text
Omega = (1,...,1)
```

has orbit size 1, so

```text
Stab(Omega)=O_I(20,2).
```

Thus selecting Omega breaks no 2-primary heavy symmetry at all.

Odd and even non-Omega vector choices have residual orders

```text
|O_I(20,2)| / 2^19
```

and

```text
|O_I(20,2)| / (2^19 - 2).
```

## 3. Symplectic quotient

The fixed-null structure gives

```text
1 -> U_19 -> O_I(20,2) -> Sp(18,2) -> 1,
```

with

```text
|U_19|=2^19.
```

So after the fixed vector Omega, the moving quotient is symplectic:

```text
Sp(18,2).
```

## 4. Meaning

Prime selection tells us which local phase space is visible.

Orbit-stabilizer tells us what residual symmetry remains after choosing a phase object.

The most rigid object is still

```text
Omega,
```

because it is fixed by the entire 2-primary heavy symmetry.

## 5. Structural slogan

```text
3-primary choices break to null/plus/minus stabilizers; the canonical 2-primary Omega breaks nothing.
```

This is the residual-symmetry layer under the local arithmetic phase spaces.