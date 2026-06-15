# BT1087 — Construct the 40-into-54 core inclusion

BT1087 makes the noncanonical inclusion in BT1083 explicit.

## Per-generation carrier

For one generation the slot carrier has dimension

```text
54 = 2_chirality * 3_fiber * 3_weakslot * 3_color.
```

Equivalently it is two 27-dimensional chirality sheets:

```text
G_g = C27_L(g) direct_sum C27_R(g).
```

## Inclusion ansatz

Use the first factorized 40-core inclusion

```text
C40_core(g) = C27_L(g) direct_sum B13_R(g),
```

where `B13_R(g)` is a chosen 13-dimensional subspace inside the right chirality sheet.  The residual is

```text
R14(g) = B13_R(g)^perp inside C27_R(g),
```

so

```text
G_g = C40_core(g) direct_sum R14(g).
```

## Why this is the right shape

The 40-point W33 parabolic anatomy is

```text
40 = 13 + 27,
```

where the 13 is the fixed/gauge-perp plane and the 27 is the matter shell.  The 54-slot generation block naturally supplies two 27-sheets.  Therefore the cleanest dimension-preserving lift is:

```text
matter shell 27  -> one full chirality sheet,
gauge/fixed 13   -> a 13-subspace of the opposite chirality sheet,
residual 14      -> the remaining opposite-chirality directions.
```

## Concrete skeleton

A concrete ordered-basis skeleton chooses `B13_R(g)` as the first 13 right-chirality coordinates.  Then the remaining 14 right-chirality coordinates are `R14(g)`.  This gives a literal inclusion matrix of shape

```text
54 x 40
```

with orthonormal columns.

## Boundary

The skeleton is dimensionally and parabolically natural, but it is not unique.  The true W33-natural version must choose `B13_R(g)` from the gauge-perp plane action, not from an arbitrary ordered-basis convention.
