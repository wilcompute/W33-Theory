# BT965 — Packet lane preservation audit

BT965 tests how far the BT964 Holonet packet ABI rail attachment can be promoted from convention to theorem.

## Verified today

```text
prefixes = [0, 10, 110, 111]
prefix_free = true
lanes = mirror, schedule, cache_A, cache_B
identity_lane_preservation = true
```

## Blocker

Executable lane-action maps are not yet encoded for:

```text
mirror
schedule
cache_A
cache_B
```

So full mirror/schedule/cache lane preservation is not currently provable from repository artifacts.

## Test contract

Future operation maps should have shape:

```text
role -> {source_lane: target_lane or set[target_lanes]}
```

Pass condition: every target lane remains within the packet role's assigned allowed lane set.

## Boundary

BT964 remains a selector-backed ABI convention until these operation maps are committed and verified.

## Witness

```text
analysis/bt965_packet_lane_preservation_audit.py
data/bt965_packet_lane_preservation_audit.json
```
