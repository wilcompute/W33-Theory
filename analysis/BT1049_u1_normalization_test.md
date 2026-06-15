# BT1049 — U(1) normalization test

BT1049 derives the U(1) normalization from trace/unimodularity on the BT1038
carrier, rather than treating the singlet as only a dimension count.

## Carrier

```text
K = C^3_weakslot tensor C^3_color
C^3_weakslot = C_singlet + C^2_doublet
```

Let

```text
P_s = diag(1,0,0)
```

on the weakslot. The unimodular generator is:

```text
Y0 = (P_s - (1/3) I_weak) tensor I_color
   = diag(2/3, -1/3, -1/3) tensor I_3
```

## Checks

```text
Tr_K(Y0)   = 0
Tr_K(Y0^2) = 2
```

Therefore the normalized generator is:

```text
Yhat = Y0 / sqrt(2)
```

so that

```text
Tr_K(Yhat^2) = 1.
```

## Charge pattern before normalization

```text
weak singlet slot :  2/3
weak doublet slots: -1/3, -1/3
ratio             : -2 : 1
```

## Reading

The finite singlet in `C[12]` is trace-corrected over the full weakslot/color
carrier, producing a unimodular traceless U(1) direction. This is stronger than a
bare dimension-count identification.

## Boundary

The normalization is derived for the BT1038 carrier. The full physical charge
assignment still requires the complete fermion representation ledger.

## Witnesses

```text
analysis/bt1049_u1_normalization_test.py
data/bt1049_u1_normalization_test.json
```
