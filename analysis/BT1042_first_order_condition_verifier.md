# BT1042 — First-order condition verifier

BT1042 verifies the first-order condition for the BT1041 Hilbert-Schmidt bimodule
candidate.

## Carrier

```text
HS(K), K = C^3_weakslot tensor C^3_color
```

with `dim HS(K)=81`; the chiral factor is omitted in the numerical matrix test
because the same `sigma_x` factor appears uniformly.

## Test

For

```text
D_F = sigma_x tensor (L_Phi + R_Phi)
```

and algebra generators acting by left multiplication, the opposite algebra acts
by right multiplication. Since left and right multiplication commute on `HS(K)`,
BT1042 checks:

```text
[[D_F, L_a], R_b] = 0
```

on the generator span.

## Result

```text
generator count      = 12
pairs tested         = 144
max commutator norm  = 0.0
tolerance            = 1e-9
first-order pass     = true
```

## Boundary

This verifies the first-order condition for the block candidate generator span
and sample Higgs direction. The full physical Yukawa texture still requires
choosing all `Phi` components and couplings.

## Witnesses

```text
analysis/bt1042_first_order_condition_verifier.py
data/bt1042_first_order_condition_verifier.json
```
