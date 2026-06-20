# BT1381--BT1383 -- S3 Solver, Non-Clifford ABI, Runtime Frontier Integration

## BT1381 -- S3 gauge global solver probe

Added:

```text
tools/bt1381_s3_gauge_global_solver_probe.py
data/bt1381_s3_gauge_global_solver_probe.json
```

This imports the exact BT1376 Max-2CSP score tables and runs deterministic random-restart coordinate ascent. It found no witness above the BT1373 score:

```text
best identity-edge score = 210
best source = BT1373 witness
```

Boundary: this is not a proof of global optimality. It is a solver probe.

## BT1382 -- Non-Clifford port ABI

Added:

```text
tools/bt1382_non_clifford_port_abi.py
data/bt1382_non_clifford_port_abi.json
```

It records two ABI-compatible non-Clifford port options:

```text
Hesse-SIC/T measurement port
Fibonacci braiding port
```

Boundary: this certifies the ABI, not the resource factory or hardware implementation.

## BT1383 -- Runtime frontier integration

Added:

```text
tex/bt1381_bt1383_runtime_frontier_insert.tex
tools/bt1383_verify_runtime_frontier_integration.py
data/bt1383_runtime_frontier_integration.json
```

The claim-stratified master paper can now absorb the runtime contract, S3 optimization frontier, and non-Clifford port ABI without changing claim classes.

## Regression

Added:

```text
tests/test_bt1381_bt1383_runtime_frontier.py
```
