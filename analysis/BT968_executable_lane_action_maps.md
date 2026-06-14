# BT968 — Executable ABI lane actions

BT968 commits the first executable selector-backed lane actions satisfying the BT965 contract.

## Assignment

```text
mirror   -> lane 1
schedule -> lane 0
cache_A  -> lane 2
cache_B  -> lane 3
```

## Result

```text
prefix_free = true
all_roles_preserve_assigned_lanes = true
```

## Boundary

This verifies the committed ABI-level actions only. Stronger operation implementations must be encoded and tested separately.

## Witness

```text
analysis/bt968_executable_lane_action_maps.py
data/bt968_executable_lane_action_maps_summary.json
```
