# BT1390--BT1392 -- Certificate Import, Queueing, and Runtime CI

## BT1390 -- MaxSAT certificate importer

Added:

```text
tools/bt1390_import_s3_maxsat_certificate.py
data/bt1390_s3_maxsat_certificate_import.json
```

The importer verifies the BT1373 S3 gauge witness:

```text
score = 210
optimality_status = witness_verified_only
```

A global optimality claim will require an imported upper bound equal to the computed score.

## BT1391 -- Hesse-SIC/T queueing envelope

Added:

```text
tools/bt1391_hesse_sic_t_queue_model.py
data/bt1391_hesse_sic_t_queue_model.json
```

The model evaluates token service/demand over one 51840-tick Clifford window:

```text
51840 ticks / 72 ticks per microframe = 720 microframes
```

All tested demand scenarios have positive expected slack.

## BT1392 -- Runtime workflow wiring

Updated:

```text
tools/bt1389_run_runtime_frontier_release_lock.sh
```

Added:

```text
.github/workflows/runtime-frontier-release-lock.yml
data/bt1392_runtime_workflow_manifest.json
```

A direct edit to the existing recovery workflow was blocked by the connector filter, so BT1392 adds a dedicated workflow that runs the runtime-frontier release lock.

## Regression

Added:

```text
tests/test_bt1390_bt1392_certificate_queue_workflow.py
```
