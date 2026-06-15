#!/usr/bin/env python3
"""BT1191 -- support-pair to BT748 matching obstruction.

BT1187 gives the best available map from a 45-point transport edge to two W33
support sets.  BT748 presentation-pair keys have a different object type:
(center point p, four rectangle points, and a set of gauged rectangle edges).
A direct matcher therefore needs a new incidence reconstruction, not just a key
lookup.  This file records the exact interface mismatch.
"""

import json

payload = {
    "bt": 1191,
    "title": "support-pair to BT748 matching obstruction",
    "transport_side": {
        "vertex_type": "center-quad quotient point",
        "point_count": 45,
        "support_size": 8,
        "edge_count": 720,
        "edge_payload": "two 8-vertex W33 supports",
    },
    "bt748_side": {
        "object_type": "presentation pair key",
        "count": 51840,
        "factorization": "540*2*48",
        "key_shape": "center p, four rectangle points, gauged rectangle-edge set",
    },
    "match_status": "blocked: object types are not the same; support-pair -> presentation-pair reconstruction is required",
    "checks": {
        "transport_edges_720": 720 == 45 * 32 // 2,
        "bt748_count_factorization": 51840 == 540 * 2 * 48,
        "object_type_mismatch_recorded": True,
        "correlation_not_claimed": True,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
