# BT1045 — KO-sign verifier

BT1045 verifies the KO-sign package for the BT1041 candidate.

## Carrier and operators

```text
H     = C^2_chiral tensor HS(K)
gamma = sigma_z tensor identity
J     = sigma_x tensor star antiunitary
D_F   = sigma_x tensor T,  T = L_Phi + R_Phi, Phi = Phi^*
```

## Checks

| identity | target | pass |
| --- | --- | --- |
| `J^2` | `+1` | true |
| `J gamma` | `- gamma J` | true |
| `J D_F` | `D_F J` | true |
| `gamma D_F` | `- D_F gamma` | true |

```text
max identity error = 0.0
```

## Reason

`sigma_x` swaps chirality, `sigma_z` grades chirality, and `star` commutes with
`T=L_Phi+R_Phi` when `Phi` is Hermitian.

## Boundary

This verifies the KO-sign package for the BT1041 candidate. It does not yet fix
the physical Yukawa texture.

## Witnesses

```text
analysis/bt1045_ko_sign_verifier.py
data/bt1045_ko_sign_verifier.json
```
