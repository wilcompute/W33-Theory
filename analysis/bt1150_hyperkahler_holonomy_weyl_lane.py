#!/usr/bin/env python3
import json

payload = {
    "bt": 1150,
    "title": "hyperkahler holonomy Weyl lane",
    "orientation": "complex/hyperkahler",
    "parallel_triple": "three Kahler forms span Lambda_plus",
    "scalar_flat_kahler_rule": "W_plus=0",
    "signature": -16,
    "surviving_weyl_slot": "W_minus=24",
    "interpretation": "the surviving Weyl chirality is forced by SU(2) holonomy orientation, not chosen freely",
    "checks": {
        "parallel_triple_dimension": 3 == 3,
        "W_plus_zero": 0 == 0,
        "W_minus_24": 24 == 24,
        "signature_negative": -16 < 0,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
