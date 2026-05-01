# Part XCIX — Witt Strata and Local Orbit Anatomy

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Part XCVIII identified the local arithmetic symmetry groups

```text
Aut(T,L) ≅ O(59,3) × O_I(20,2).
```

This part decomposes their local phase modules into Witt and orbit strata.

## 1. 3-primary Witt decomposition

The 3-primary module is

```text
V_3 = F3^59
```

with quadratic form

```text
(+1)^39 ⊕ (-1)^20.
```

Since

```text
59 = 2*29 + 1,
```

and the determinant square class is +1, the Witt decomposition is

```text
V_3 ≅ H^29 ⊕ <-1>.
```

So the Witt index is

```text
29
```

with one anisotropic line of norm -1.

## 2. 3-primary orbit counts

The nonzero vector strata under O(59,3) are:

```text
Q=0: 3^58 - 1
```

nonzero isotropic vectors,

```text
Q=+1: 3^58 - 3^29
```

positive norm vectors, and

```text
Q=-1: 3^58 + 3^29
```

negative norm vectors.

## 3. 2-primary orbit anatomy

The 2-primary module is

```text
V_2 = F2^20
```

with the nonalternating identity form I_20.

There is a canonical fixed null vector

```text
Omega = (1,1,...,1).
```

It is fixed by O_I(20,2), because

```text
q(v)=v·v=Omega·v.
```

The even hyperplane is

```text
Omega^perp
```

with radical

```text
<Omega>.
```

The quotient

```text
Omega^perp/<Omega>
```

is a symplectic space of dimension

```text
18.
```

## 4. 2-primary orbit counts

The O_I(20,2)-orbits are:

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

## 5. Meaning

The 3-primary full phase space has a single anisotropic Witt line.

The 2-primary heavy phase space has a canonical fixed null vector Omega.

This Omega is a new rigid object inside the hidden heavy 20-sector.

## 6. Structural slogan

```text
The 3-primary side has a Witt core; the 2-primary heavy side has a fixed null vector.
```

This is the orbit anatomy behind the local arithmetic phase symmetries.