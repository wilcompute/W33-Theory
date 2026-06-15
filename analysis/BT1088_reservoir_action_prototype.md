# BT1088 — Reservoir action prototype

BT1088 builds the first block-action prototype on the 78-dimensional bridge reservoir.

## Reservoir split

BT1085 identified the preferred decomposition

```text
78 = 66 + 12.
```

Use

```text
R78 = T66 direct_sum A12,
```

where

```text
T66 = P22(0) direct_sum P22(1) direct_sum P22(2)
```

is the three-generation transvection bookkeeping layer, and

```text
A12 = A1 direct_sum A3 direct_sum A8
```

is the gauge-adjoint packet layer.

## Prototype action

The first reservoir action is block diagonal:

```text
rho_res = rho_T66 direct_sum rho_A12.
```

On the transvection bookkeeping layer, the generation transvection is grade-zero, so the first action is the identity on each lifted `P22` block:

```text
rho_T66(R) = I_66.
```

On the gauge-adjoint layer use the module profile

```text
rho_A12 = rho_1 direct_sum rho_3 direct_sum rho_8.
```

Here `rho_1` is the U1 scalar line, `rho_3` is the weak triplet module, and `rho_8` is the color octet module.

## Dimensions

```text
rank T66 = 3*22 = 66
rank A12 = 1+3+8 = 12
rank R78 = 78.
```

## First coupling boundary

The prototype deliberately sets the off-diagonal reservoir coupling to zero:

```text
K_{66,12} = 0.
```

The next physical step is to construct a nonzero intertwiner between the transvection bookkeeping layer and the gauge-adjoint layer, if W33 incidence or the centralizer action forces one.

## Interpretation

This action makes the reservoir legible: the 66-block remembers the true BT876 grade-zero bookkeeping in each generation, while the 12-block carries the Standard-Model adjoint packet profile.  The reservoir is therefore a structured runtime layer, not discarded dimension.

## Boundary

BT1088 is a prototype representation on the reservoir. It is not yet the final gauge/reservoir dynamics.
