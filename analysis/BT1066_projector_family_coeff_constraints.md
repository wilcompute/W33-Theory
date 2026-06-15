# BT1066 — Coefficient constraints for `Q=sum c_lambda P_lambda`

BT1066 derives symbolic constraints on the leading scalar search family from BT1063:

```text
Q = c0 P0 + c4 P4 + c10 P10 + c16 P16.
```

## Trace formulas

Using the BT1046 sector trace densities, define

```text
S2 = 54 c0^2 + 80 c4^2 + 16 c10^2 + 10 c16^2
S4 = 54 c0^4 + 80 c4^4 + 16 c10^4 + 10 c16^4
M2 = 320 c4^2 + 160 c10^2 + 160 c16^2.
```

Then

```text
tr_240(Phi^2)          = S2 h2
tr_240(Phi^4)          = S4 h2^2
tr_240(Delta_1 Phi^2) = M2 h2.
```

## 96-submodule constraint

BT1065 suggests a physical projector of rank 96 with complement rank 66. With the same trace density used in BT1046, a unit-amplitude scalar supported only on the 96-dimensional physical submodule has expected quadratic coefficient

```text
(2/3) * 96 = 64.
```

So the first scalar-support normalization is

```text
S2 = 64.
```

If the scalar is a true unit projector on that submodule, the quartic coefficient should also satisfy

```text
S4 = 64.
```

Equivalently, the coefficient vector should behave idempotently on the selected physical support.

## Generation/fiber invariant constraint

From BT1050, the coefficients are not arbitrary constants. They should be functions of

```text
ys = alpha + 2 beta,
yd = alpha - beta.
```

Therefore

```text
c_lambda = C_lambda(ys, yd),
```

and the constraints become

```text
S2(C_lambda(ys,yd)) = 64,
S4(C_lambda(ys,yd)) = 64,
```

for the unit-support normalization.

## Boundary

BT1066 constrains the spectral-projector family. It does not solve the coefficients because the physical 96-projector matrix from BT1065 is not yet built.
