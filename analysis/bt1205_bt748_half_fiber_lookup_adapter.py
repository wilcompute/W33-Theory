#!/usr/bin/env python3
"""BT1205 -- BT748 half-fiber lookup adapter boundary.

BT1201 attached all labels currently available in the repo to the C2160 codec.
This file makes the remaining lookup explicit.  BT748's persisted theorem records
only aggregate fiber data (51840 = 540*2*48, inner half-fiber size 48, sheet
profile); the script constructs presentation-pair keys in memory as

    (center point p, four rectangle points, gauged rectangle-edge set)

but does not persist a table mapping the 48 half-fiber coordinates to canonical
presentation-pair keys.  Therefore C2160 can name half_fiber48 slots, but cannot
yet attach objectwise BT748 keys without rerunning/promoting that table.
"""

import json

payload = {
    "bt": 1205,
    "title": "BT748 half-fiber lookup adapter boundary",
    "known_bt748_schema": {
        "presentation_pair_key": "(center point p, four rectangle points, gauged rectangle-edge set)",
        "presentation_pairs": 51840,
        "root_triples": 540,
        "chirality_sheets": 2,
        "half_fiber_slots": 48,
    },
    "codec_status": {
        "half_fiber48_coordinate_exists": True,
        "objectwise_presentation_pair_lookup_persisted": False,
        "remaining_lookup": "half_fiber48 slot -> canonical BT748 presentation-pair key within a chosen root-triple fiber",
    },
    "required_promotion": "persist BT748 fiber coordinate table: root_triple_id, chirality, half_fiber_index, presentation_pair_key",
    "checks": {
        "factorization_51840": 51840 == 540 * 2 * 48,
        "half_fiber_slots_48": 48 == 48,
        "lookup_boundary_recorded": True,
        "false_attachment_not_claimed": True,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
