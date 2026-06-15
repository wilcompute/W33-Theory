#!/usr/bin/env python3
"""BT1182 -- compare the transport 2-cover with the BT748 centralizer split.

BT1180 needs a binary sheet coordinate over the 45-point transport graph.  BT748
already found a 96 = 2*48 centralizer/fiber split with chirality half-fibers of
size 48.  The shared structure is a Z2 sheet over an inner 48-object torsor, not
a proof that the two sheets are identical.  This file records the compatible
numerology and the required next objectwise test.
"""

import json

payload = {
    "bt": 1182,
    "title": "Z2 cover and centralizer-96 bridge",
    "transport_cover": {"base_vertices": 45, "cover_vertices": 90, "sheet_group": "Z2"},
    "bt748_centralizer": {"full_order": 96, "half_fiber_order": 48, "sheet_group": "Z2"},
    "shared_pattern": "binary sheet over an inner sector",
    "not_yet_proved": "the transport sheet bit equals the BT748 chirality bit",
    "next_test": "pull raw transport Z2 voltage through root-triple fiber coordinates and test correlation with chirality",
    "checks": {
        "centralizer_split_96": 96 == 2 * 48,
        "transport_cover_binary": 90 == 2 * 45,
        "both_have_z2_sheet": True,
        "identity_not_claimed": True,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
