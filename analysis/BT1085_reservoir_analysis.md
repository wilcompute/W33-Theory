# BT1085 — Reservoir analysis

BT1085 decomposes the 78-dimensional bridge reservoir from BT1082.

## Source

The bridge skeleton embeds

```text
C^162 = S96 direct_sum S66
```

into

```text
C^240 = C96 direct_sum C144,
```

with

```text
S96 -> C96 = E0 direct_sum E16
S66 -> part of C144 = E4 direct_sum E10.
```

The unused chain reservoir has dimension

```text
144 - 66 = 78.
```

## Decompositions

The 78 has several W33-native readings:

```text
78 = 66 + 12
78 = 6 * 13
78 = 3 * 26
78 = 2 * 39
```

The most relevant one is

```text
78 = 66 + 12.
```

Here `66 = 3*22` is a second copy of the BT876 fixed-plus-diagonal complement scale, and `12 = 1+3+8` is the gauge adjoint profile.

## Interpretation

The reservoir is not random slack. It has exactly enough room to hold:

```text
1. a 66-dimensional transvection-grade bookkeeping layer, and
2. one 12-dimensional gauge-module layer.
```

Equivalently, it can be read as six copies of the cyclotomic gauge denominator

```text
13 = Phi_3,
```

or as two copies of the gauge-sector dimension

```text
39 = 3*Phi_3.
```

## Working hypothesis

The reservoir should be treated as the place where the sparse bridge absorbs the data it has not yet made natural: incidence constraints, gauge adjoint action, and the second transvection bookkeeping layer needed to turn the bridge from a partial identity into a W33-native functor.

## Boundary

BT1085 gives structural decompositions and a working interpretation. It does not yet construct the gauge/reservoir action.
