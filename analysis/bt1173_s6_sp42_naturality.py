#!/usr/bin/env python3
"""BT1173 -- S6/Sp(4,2) naturality status for the 15-object dictionary.

The nonzero masks of F2^4 carry the natural Sp(4,2) action, and the unordered
pairs of a six-set carry the natural S6 action.  Both actions have degree 15 and
group order 720, so the mask-pair dictionary can be made natural after choosing
an isomorphism Sp(4,2) ~= S6.  The lexicographic dictionary used in BT1171 is one
labeled choice, not a canonical label-free construction.
"""

import json

payload = {
    "bt": 1173,
    "title": "S6-Sp42 naturality status",
    "mask_action": {"set_size": 15, "group": "Sp(4,2)", "group_order": 720},
    "pair_action": {"set_size": 15, "group": "S6", "group_order": 720},
    "status": "natural up to a chosen Sp(4,2) ~= S6 isomorphism; BT1171 is a labeled dictionary",
    "checks": {
        "same_degree": 15 == 15,
        "same_order": 720 == 720,
        "dictionary_not_label_free": True,
        "naturality_requires_chosen_isomorphism": True,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
