# BT1387--BT1389 -- Solver Harness, Factory Model, Runtime Release Lock

## BT1387 -- S3 MaxSAT solver harness

Added:

```text
tools/bt1387_s3_maxsat_solver_harness.py
data/bt1387_s3_maxsat_solver_harness.json
```

The harness regenerates the exact BT1384 WCNF, verifies the 210-score BT1373 witness, records recommended external solver commands, and leaves optimality unresolved unless a real MaxSAT backend is available and its certificate is imported.

## BT1388 -- Hesse-SIC/T resource factory envelope

Added:

```text
tools/bt1388_hesse_sic_t_factory_model.py
data/bt1388_hesse_sic_t_factory_model.json
```

Baseline model:

```text
p_success = 0.8763201
expected attempts = 1.1411
expected ticks = 82.16
```

Boundary: stochastic ABI envelope only, not a physical factory certificate.

## BT1389 -- Runtime frontier release lock

Added:

```text
tools/bt1389_run_runtime_frontier_release_lock.sh
data/bt1389_runtime_release_lock_index.json
```

The runner extends BT1340 and executes the runtime frontier gates through BT1388.

## Regression

Added:

```text
tests/test_bt1387_bt1389_runtime_release_lock.py
```
