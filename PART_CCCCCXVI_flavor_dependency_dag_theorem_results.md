# Part CCCCCXVI — Results

## Status

All verifier checks pass.

## DAG audit

```text
DAG is acyclic: true
all observables reachable from primitives: true
no observable is primitive: true
expected values match: true
```

## Primitive operator nodes

```text
O1_PerronDet = 41
O2_E6Mean = 160/13
O2_GapRatio = 8/5
O3_BottomUnit = 5
O3_CKMCPUnit = 7
O3_PMNSCPUnit = 11
```

## Intermediate nodes

```text
D_t = 41
D_b = 125
D_c = 137
lambda_H = 13/100
M_vac = 1111
Delta_M = 3/22
alpha_slip = 880/24445
```

## Final observables

```text
y_t_cubed = 40/41
lambda_CKM = 9/40
compactified_CKM = 9/41
y_b = 3/125
y_c = 1/137
y_tau = 16029/1562500
A_CKM = 81/100
PMNS_theta13 = 9/400
rho_bar = 4/25
eta_bar = 343/1000
PMNS_delta_over_pi = 11/10
PMNS_solar = 4/13
PMNS_atmospheric = 4/7
alpha_inverse_refined = 669969/4889
```

## Interpretation

The three-operator flavor basis forms an explicit acyclic dependency graph. All final flavor observables are reachable from the primitive W(3,3) atoms plus the three operator nodes, while none of the final observables is primitive. This makes the generative structure non-circular and auditable.
