# BT1026 — Incidence shard timing manifest

BT1026 adds timing/memory instrumentation policy for the K3 real-incidence shards.

## Shards

```text
BT1021 degree-2 real incidence shard
BT1022 degree-3 real incidence shard
```

## Safe CI defaults

```text
degree_2 count = 8
degree_3 count = 8
```

## Policy

Start with 8-row real-incidence windows in the smoke workflow. Increase the
window only after surfaced Actions timing data confirms the larger block is safe.

## Boundary

The instrumentation scaffold is committed. Actual timing depends on checkout or
Actions execution because connector sessions do not surface workflow runtime
artifacts.

## Witnesses

```text
analysis/bt1026_incidence_shard_timing.py
data/bt1026_incidence_shard_timing.json
```
