# BT1047 — Generation/fiber symmetry constraint

BT1047 constrains the BT1046 sector amplitudes with the minimal W33
`3 x 3` generation/fiber symmetry form.

## Matrix form

```text
Y = alpha I_3 + beta (J_3 - I_3)
```

This is the `S3`-invariant two-parameter texture on the generation/fiber triple.

## Eigenvalues

```text
singlet eigenvalue = alpha + 2 beta
doublet eigenvalue = alpha - beta
```

with multiplicities `1` and `2`.

## Trace invariants

```text
Tr(Y^2) = 3 alpha^2 + 6 beta^2
Tr(Y^4) = (alpha+2 beta)^4 + 2 (alpha-beta)^4
```

## Constraint on BT1046

The sector amplitudes

```text
a0, a4, a10, a16
```

should be functions of the singlet/doublet invariants rather than arbitrary
numbers.

## Boundary

This is a symbolic symmetry constraint only. No numerical flavor parameter is
inserted.

## Witnesses

```text
analysis/bt1047_generation_fiber_symmetry.py
data/bt1047_generation_fiber_symmetry.json
```
