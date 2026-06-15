# BT1089 — Natural B13_R(g) from the antipodal odd subspace

BT1089 replaces the ordered-basis `B13_R(g)` skeleton from BT1087 by a W33-native construction on the right-chirality matter cube.

## Right-chirality matter cube

Identify the right chirality sheet in one generation with the regular matter-shell address cube

```text
C27_R(g) = C[ F3^3 ].
```

Choose the shell origin supplied by the Bell/point parabolic torsor.  The antipodal involution is

```text
A : x -> -x.
```

It has one fixed point, the origin, and thirteen two-point orbits on the nonzero vectors.

## Natural 13-plane

Define

```text
B13_R(g) = { f in C[F3^3] : f(-x) = -f(x) }.
```

Equivalently, for each projective direction `{x,-x}` choose the antisymmetric vector

```text
e_x - e_{-x}.
```

There are exactly thirteen projective directions in `PG(2,3)`, hence

```text
rank B13_R(g) = 13.
```

The residual is the even subspace

```text
R14(g) = { f : f(-x)=f(x) },
```

with basis the origin plus thirteen pair-sums, so

```text
rank R14(g) = 14.
```

## Updated core inclusion

The W33-natural core inclusion is therefore

```text
C40_core(g) = C27_L(g) direct_sum B13_R(g),
```

and the residual is the antipodal-even right-chirality block.

## Why this improves BT1087

BT1087 used the first thirteen ordered coordinates as a skeleton.  BT1089 replaces that arbitrary convention with the canonical odd subspace of the matter torsor.  The number `13=Phi_3` is now literally the number of projective directions in `PG(2,3)`.

## Boundary

The construction still depends on the chosen shell origin in the torsor.  Once the Bell/point parabolic seed is fixed, the odd/even decomposition is canonical.
