# BT1338--BT1340 -- Stabilizer Extraction, Optical Budget, and Extended Release Lock

## BT1338 -- Q4 chain check extraction

Added:

```text
tools/bt1338_extract_q4_chain_checks.py
data/bt1338_q4_chain_check_matrices.json
proofs/BT1338_q4_chain_check_matrix_audit.md
```

Result:

```text
rank(partial_1) = 15
rank(partial_2) = 17
k_naive = 32 - 15 - 17 = 0
```

This means the literal cubical Q4 chain complex is not yet the claimed [[32,4,4]] object. The missing object is now sharply identified: a toroidal/gauge quotient or check-rank reduction preserving distance 4.

## BT1339 -- Optical budget

Added:

```text
tools/bt1339_optical_loss_crosstalk_budget.py
data/bt1339_optical_loss_crosstalk_budget.json
proofs/BT1339_optical_loss_crosstalk_budget.md
```

Conservative scenario:

```text
total loss = 2.52 dB
transmission = 0.559
aggregate crosstalk = -24.21 dB
```

This passes the first explicit loss/crosstalk budget while remaining a parametric gate, not a PDK simulation.

## BT1340 -- Extended release lock

Added:

```text
tools/bt1340_run_extended_release_lock.sh
data/bt1340_extended_release_lock_index.json
```

Updated:

```text
.github/workflows/recovery-packet.yml
```

The direct replacement of BT1303 was blocked by the connector filter, so BT1340 records an additive extended-release index.

## Regression

Added:

```text
tests/test_bt1338_bt1340_stabilizer_optical_release.py
```

This protects the Q4 chain check extraction, optical budget, and extended release-lock runner.
