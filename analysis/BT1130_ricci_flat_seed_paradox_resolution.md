# BT1130 — Ricci-flat seed paradox resolution

BT1130 records the paper-facing theorem extracted from BT1129.

## Frontier used

The recent frontier created three pieces that look contradictory until the
heat-product algebra is written explicitly:

1. BT1116 says the finite W33 ratios are seed-independent at the finite-factor
   level, while gravitational scales are seed-dependent.
2. BT1120 creates the K3 spectral-action interface and asks for `A0`, `A2`,
   and `A4`.
3. BT1127 validates a K3 fixture with the standard topological checks
   `chi=24`, `signature=-16`, `b2=22`, and intersection signature `(3,19)`.

The apparent paradox is that a genuine Ricci-flat K3 seed has scalar curvature
zero, so the pure manifold `A2` slot vanishes.  Does that destroy the finite
W33 `a2/a0` prefactor?  No.

## Product heat expansion

Write the heat traces as

```text
Theta_M(t)=A0*t^-2 + A2*t^-1 + A4 + O(t)
```

and

```text
Theta_F(t)=N - F2*t + (F4/2)*t^2 + O(t^3).
```

Then the product coefficient extraction gives

```text
C0 = A0*N
C2 = A2*N - A0*F2
C4 = A4*N - A2*F2 + A0*F4/2.
```

For Ricci-flat K3,

```text
A2=0,
```

so

```text
C0 = A0*N
C2 = -A0*F2
C4 = A4*N + A0*F4/2.
```

## The theorem

```text
Ricci-flat K3 kills the pure manifold A2 term, but it does not kill the
Lambda^2 coefficient of the almost-commutative product.  The finite W33
second heat moment F2 fills that slot.
```

So the BT1116 finite ratios should be read as finite-factor moment ratios, not
as pure K3 heat-coefficient ratios.

## Topological normalization hook

For Ricci-flat K3 the topological checks stay fixed:

```text
chi=24,
signature=-16,
b2=22,
intersection_signature=(3,19).
```

The Chern--Gauss--Bonnet normalization gives the curvature-energy hook

```text
Integral |Rm|^2/(8*pi^2)=24,
```

or equivalently

```text
Integral |Rm|^2=192*pi^2.
```

This attaches the `A4` slot to topology/curvature, but does **not** set the
physical volume or gravitational scale.

## Interface correction

The BT1120 interface should distinguish four quantities:

```text
A0_M     pure manifold volume coefficient
A2_M     pure manifold scalar-curvature coefficient, zero for Ricci-flat K3
A4_M     pure manifold curvature/topology coefficient
F2,F4    finite W33 heat moments
```

The product coefficients are then derived values:

```text
C0,C2,C4.
```

This prevents the common mistake of comparing the finite `a2/a0` prefactor
directly to `A2_M/A0_M`.

## Boundary

BT1130 is a symbolic bookkeeping theorem.  It does not compute a K3 metric,
volume, eigenvalue list, or physical Newton/cosmological scale.  It sharpens
the schema so that the real K3 computation has the right target.
