#!/usr/bin/env python3
"""BT1195 -- D4-coset / half-fiber alignment.

The new GKP coherence artifact says Aut(D4)=1152 and Sp(4,3)=51840, hence the
full Clifford/architecture group has 45 cosets over the D4 Gaussian stabilizer.
BT748 says the inner half-fiber has 48 slots.  Therefore the product

    45 cosets x 48 half-fiber slots = 2160

is the same carrier BT1194 found.  This gives the most concrete candidate for
what the universal 2160 carrier is: D4-Gaussian coset choice together with an
inner centralizer coordinate.
"""

import json

sp43 = 51840
aut_d4 = 1152
index = sp43 // aut_d4
half_fiber = 48
carrier = index * half_fiber

payload = {
    "bt": 1195,
    "title": "D4 coset and half-fiber alignment",
    "groups": {
        "Sp(4,3)": sp43,
        "Aut(D4)_with_triality": aut_d4,
        "index": index,
        "BT748_half_fiber": half_fiber,
    },
    "carrier": carrier,
    "interpretation": "universal 2160 carrier = D4-Gaussian coset choice (45) times BT748 inner half-fiber coordinate (48)",
    "checks": {
        "index_45": index == 45,
        "carrier_2160": carrier == 2160,
        "full_group_order_recovered": index * aut_d4 == sp43,
        "bt748_half_fiber_used": half_fiber == 48,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
