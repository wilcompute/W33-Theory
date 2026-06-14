# BT971 — Nontrivial lane transport maps

BT971 extends the BT968 singleton ABI maps to a nontrivial lane-level transport model.

## Families

```text
light = [0,1]
cache = [2,3]
```

## Family-preserving subgroup

```text
id
light_swap
cache_swap
both_swap
```

This subgroup has order 4. It is the V4 subgroup preserving the present light/cache ABI partition.

## Reading

The full square transport action contains operations that cross the light/cache partition. The current ABI is preserved by the V4 family-preserving subgroup, not by the full D8 square action.

## Boundary

This is a lane-level transport model, not a derivation of the full optical D8/D12 packet action.

## Witness

```text
analysis/bt971_nontrivial_lane_transport_maps.py
data/bt971_nontrivial_lane_transport_maps.json
```
