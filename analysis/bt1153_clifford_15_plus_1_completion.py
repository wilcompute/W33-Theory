#!/usr/bin/env python3
"""BT1153 -- Clifford/Boolean 15+1 completion.

The 16-dimensional completion is the Boolean/Clifford monomial basis on four
generators.  It splits as the scalar empty-mask line plus the 15 nonempty masks.
The grade-4 pseudoscalar/orientation monomial is one of the 15 nonempty masks,
not the extra scalar line.
"""

from __future__ import annotations

import json
from collections import Counter

masks = list(range(16))
grades = {m: bin(m).count("1") for m in masks}
counts = Counter(grades.values())
scalar = [m for m, g in grades.items() if g == 0]
nonempty = [m for m, g in grades.items() if g > 0]
pseudoscalar = [m for m, g in grades.items() if g == 4]

payload = {
    "bt": 1153,
    "title": "Clifford/Boolean 15+1 completion",
    "grade_counts": dict(sorted(counts.items())),
    "scalar_empty_mask_count": len(scalar),
    "nonempty_mask_count": len(nonempty),
    "pseudoscalar_mask_count": len(pseudoscalar),
    "resolution": "The extra 1 in 16=1+15 is the scalar/vacuum empty mask.  The orientation pseudoscalar is the grade-4 full mask and lies inside the 15-sector.",
    "checks": {
        "total_16": len(masks) == 16,
        "scalar_plus_nonempty": len(scalar) + len(nonempty) == 16,
        "nonempty_15": len(nonempty) == 15,
        "pseudoscalar_inside_15": pseudoscalar[0] in nonempty,
        "grade_pattern_14641": [counts[i] for i in range(5)] == [1, 4, 6, 4, 1],
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
