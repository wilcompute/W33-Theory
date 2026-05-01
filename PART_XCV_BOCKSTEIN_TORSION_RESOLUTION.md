# Part XCV — Bockstein Torsion Resolution

**Status:** theorem-grade structural extension  
**Date:** April 28, 2026

Part XCIV found the integral Smith form

```text
coker(partial_Z) ≅ Z^3 ⊕ (Z/3)^39 ⊕ (Z/6)^20.
```

Using the Chinese remainder decomposition

```text
Z/6 ≅ Z/2 ⊕ Z/3,
```

this becomes

```text
coker(partial_Z) ≅ Z^3 ⊕ (Z/3)^59 ⊕ (Z/2)^20.
```

This part computes the Bockstein maps resolving that torsion.

## 1. Mod 2

Over F2,

```text
3 != 0,
6 = 0.
```

So only the heavy arrow dies. The first-page homology is

```text
H^-_F2 = 20,
H^+_F2 = 23,
H_total = 43.
```

The Bockstein

```text
beta_2 : H^-_F2 -> H^+_F2
```

has rank

```text
20.
```

It maps the heavy negative sector isomorphically onto the heavy positive torsion image.

After this Bockstein differential,

```text
E2(F2)=3.
```

## 2. Mod 3

Over F3,

```text
3 = 0,
6 = 0.
```

Both arrows die, so all 121 states are homological on the first page.

The Bockstein beta_3 has rank

```text
59.
```

It maps all 59 negative nonzero modes onto all 59 positive nonzero modes.

After this Bockstein differential,

```text
E2(F3)=3.
```

## 3. Other primes

For p not equal to 2 or 3, both 3 and 6 are invertible. The complex is already exact away from the harmonic sector:

```text
H_Fp = 3.
```

## 4. Arithmetic law

```text
2-primary torsion detects exactly the hidden heavy 20-sector.
```

```text
3-primary torsion detects the full 59 nonzero complex-mode sector.
```

All other primes see only the harmonic index.

## 5. Meaning

The mod-p homology explosions are not new sectors. They are first-page torsion shadows. The Bockstein differential resolves them back to the same rank-3 harmonic index.

## 6. Structural slogan

```text
2 sees the heavy shell; 3 sees the whole nonzero carrier; all other primes see only the index.
```

This gives the integral torsion object a dynamic spectral-sequence resolution.