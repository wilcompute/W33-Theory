# Part XCVIII — Local Arithmetic Automorphism Groups

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Part XCVII identified the torsion character module

```text
T^ ≅ (Z/3)^59 ⊕ (Z/2)^20.
```

This part computes the local isometry groups of the finite linking/phase module.

The full arithmetic phase symmetry splits as

```text
Aut(T,L) ≅ O(59,3) × O_I(20,2).
```

Here O_I(20,2) is the isometry group of the nonalternating identity form over F2.

## 1. 3-primary form

The light Z/3 factors contribute diagonal +1.

The heavy Z/6 factors contribute diagonal 2=-1 over F3.

So the 3-primary form is

```text
(+1)^39 ⊕ (-1)^20
```

on

```text
F3^59.
```

Since the dimension is odd, the isometry group is

```text
O(59,3).
```

Its order is

```text
2 * 3^841 * product_{i=1}^{29}(3^(2i)-1).
```

## 2. 2-primary form

Only the heavy Z/6 factors contribute to the 2-primary module.

The 2-primary form is the nonalternating identity form

```text
I_20
```

on

```text
F2^20.
```

Its isometry group is

```text
O_I(20,2).
```

At the order level,

```text
|O_I(20,2)| = 2^100 * product_{i=1}^{9}(2^(2i)-1).
```

## 3. Selection-rule refinement

The 3-primary phase symmetry acts on the full nonzero character space:

```text
59 = 39_light + 20_heavy.
```

The 2-primary phase symmetry acts only on

```text
20_heavy.
```

The heavy 20-sector is exactly the overlap where both 2- and 3-primary character supports exist.

## 4. Meaning

Prime selection now has symmetry groups:

```text
3-primary phases -> O(59,3).
```

```text
2-primary phases -> O_I(20,2).
```

So the torsion character duality is not only a group-counting result; it carries local arithmetic orthogonal symmetry.

## 5. Structural slogan

```text
The full 59-mode nonzero carrier is the 3-primary orthogonal phase space; the hidden 20-sector is the 2-primary orthogonal phase space.
```

This is the local symmetry refinement of the arithmetic fracture.