# BT1041 — Real/chiral finite Dirac candidate

BT1041 constructs the first explicit `J`, `gamma`, and `D_F` candidate for the
BT1038 algebra representation.

## Carrier model

```text
H = C^2_chiral tensor HS(K)
K = C^3_weakslot tensor C^3_color
```

so

```text
dim K     = 9
dim HS(K) = 81
dim H     = 2 * 81 = 162
```

This reinterprets the doubled fermion carrier as a Hilbert-Schmidt bimodule. The
advantage is decisive: left multiplication gives `rho(A_F)`, while `J` turns it
into right multiplication, so the opposite algebra is represented honestly.

## Candidate operators

```text
gamma = sigma_z tensor identity
J     = sigma_x tensor star antiunitary, star(X)=X^*
D_F   = sigma_x tensor (L_Phi + R_Phi), Phi = Phi^*
```

Candidate signs:

```text
J^2       = +1
J gamma   = - gamma J
J D_F     = D_F J
gamma D_F = - D_F gamma
```

## Boundary

This is a candidate finite real/chiral Dirac package. BT1042 verifies the
first-order commutator on generator spans.

## Witnesses

```text
analysis/bt1041_real_chiral_dirac_candidate.py
data/bt1041_real_chiral_dirac_candidate.json
```
