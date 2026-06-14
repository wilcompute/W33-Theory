# BT961 — Final selector physics/packet gauge map

BT961 feeds the final E8 selector back into the downstream physics and Holonet packet pipeline as a gauge-fixing artifact.

## Final selector

```text
[[3,68], [4,42], [38,65], [90,144]]
```

## Canonical rails

```text
rail_support_sums = [12, 12, 14, 22]
rail_xor_masks    = [71, 46, 91, 234]
```

## Reading

This does not claim a new physical prediction. It turns the final selector into a canonical coordinate system for downstream tests:

1. recompute the 27+27+27 generation labels in this rail basis;
2. score CKM/PMNS phase candidates by selector rail support and xor slots;
3. attach the four rails to the Holonet packet ABI and test durable packet alignment.

## Witness

```text
analysis/bt961_final_selector_physics_packet_map.py
data/bt961_final_selector_physics_packet_map.json
```
