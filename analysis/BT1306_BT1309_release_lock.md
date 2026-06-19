# BT1306--BT1309 -- Release Lock

## Purpose

This pass adds the release lock layer on top of the v1.0.0 gate matrix.

## New verifier

```text
tools/bt1306_verify_release_lock.py
```

It reads:

```text
data/bt1303_v1_release_source_of_truth_index.json
```

and checks that the indexed release target, strict target, readiness flag, and referenced entrypoint files are present.

## New runner

```text
tools/bt1307_run_v1_release_lock.sh
```

It runs the BT1299 release gates and then the BT1306 lock verifier.

## Workflow wiring

```text
.github/workflows/recovery-packet.yml
```

now runs the BT1307 lock wrapper and includes the BT1305 release closure tests.

## Regression

```text
tests/test_bt1306_bt1308_release_lock.py
```

protects the verifier, wrapper runner, and workflow wiring.
