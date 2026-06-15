#!/usr/bin/env python3
"""BT1167 -- objectwise 45-layer model for the Boolean relation sector.

Classical cubic-surface bookkeeping gives 45 tritangent planes as 30 incidence
planes plus 15 pairing planes.  After choosing an orientation of the double-six,
30 splits into two oriented 15-layers, so the object count becomes

    45 = 15 + 15 + 15.

This matches the BT1165 relation decomposition 12+18+12+3 = 3*(4+6+4+1) at the
layer/object-count level.  It is not yet a canonical incidence isomorphism; that
requires a specific bijection between Boolean masks and the chosen duad/syntheme
model plus preservation of incidence.
"""

from __future__ import annotations

import itertools
import json

SIX = range(6)
duads = list(itertools.combinations(SIX, 2))
ordered_duads = [(i, j) for i in SIX for j in SIX if i != j]
left_layer = [(i, j) for i, j in ordered_duads if i < j]
right_layer = [(i, j) for i, j in ordered_duads if i > j]

def perfect_matchings(items):
    items = tuple(items)
    if not items:
        yield ()
        return
    first = items[0]
    for k in range(1, len(items)):
        second = items[k]
        rest = items[1:k] + items[k+1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))

matchings = sorted(set(perfect_matchings(SIX)))

payload = {
    "bt": 1167,
    "title": "tritangent 45 layer model for Boolean relation sector",
    "layers": {
        "left_oriented_duads": len(left_layer),
        "right_oriented_duads": len(right_layer),
        "pairing_matchings": len(matchings),
    },
    "total": len(left_layer) + len(right_layer) + len(matchings),
    "boolean_relation_pattern": "45 = 3*(4+6+4+1)",
    "object_bridge_status": "layer-level bridge succeeds; canonical incidence isomorphism remains open",
    "checks": {
        "duads_15": len(duads) == 15,
        "ordered_duads_30": len(ordered_duads) == 30,
        "left_15": len(left_layer) == 15,
        "right_15": len(right_layer) == 15,
        "matchings_15": len(matchings) == 15,
        "total_45": len(left_layer) + len(right_layer) + len(matchings) == 45,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
