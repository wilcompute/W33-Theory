# BT1378--BT1380 -- Runtime Contract and Optimization Frontier

## Commit-read basis

After BT1346, master advanced by 29 commits.  The important new chain is BT1362--BT1377:

```text
BT1362 symmetric Q4 gauge quotient
BT1363 Q4 clock to tomotope medial descent
BT1364--BT1366 Q6, phase, 2160 clock lifts
BT1367--BT1369 phase gauge, Q6 equivariance, scheduler
BT1370--BT1372 counterconnection, address table, three-epoch scheduler
BT1373--BT1375 synchronization, packet routes, Steinberg operator
BT1376 radius-3 S3 gauge local optimum
BT1377 physical universal-computation contract
```

## BT1378 -- Runtime contract verifier

Added:

```text
tools/bt1378_verify_runtime_contract.py
data/bt1378_runtime_contract_verification.json
```

It verifies the active physical-runtime spine:

```text
BT1362 symmetric Q4 [[32,4,4]] quotient with C2^4:C4 clock
BT1374 packet compiler to single-bit Q6/tomotope edges
BT1375 central C3 Steinberg scheduler
BT1377 protected Clifford runtime plus explicit non-Clifford port
```

## BT1379 -- S3 gauge Max-2CSP frontier

Added:

```text
tools/bt1379_verify_s3_gauge_max2csp_spec.py
data/bt1379_s3_gauge_max2csp_spec.json
```

It turns BT1376 into an optimization problem:

```text
variables = 40 W33 lines
labels = 6 S3 labels
constraints = 540 skew-line edges
objective = maximize identity residuals
current score = 210 identity, 330 corrections
local radius = 3
root-fixed search space = 6^39
```

## BT1380 -- Post-BT1377 bridge index

Added:

```text
tools/bt1380_verify_post_1377_bridge_index.py
data/bt1380_post_1377_bridge_index.json
tex/bt1380_post_1377_claim_table.tex
```

This gives the claim-stratified paper a compact insertion table for the current physical-runtime spine.

## Regression

Added:

```text
tests/test_bt1378_bt1380_runtime_contracts.py
```
