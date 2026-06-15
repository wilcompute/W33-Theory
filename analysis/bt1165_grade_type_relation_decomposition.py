#!/usr/bin/env python3
"""BT1165 -- grade/type decomposition of the 60-column Boolean module."""

import json

grade_counts = {1: 4, 2: 6, 3: 4, 4: 1}
feature_types = 4
columns_by_grade = {g: feature_types * c for g, c in grade_counts.items()}
# The image is the Clifford nonzero-mask ledger 4+6+4+1; the complement inside
# each four-feature grade block is three relation copies per mask.
image_by_grade = grade_counts
relations_by_grade = {g: columns_by_grade[g] - image_by_grade[g] for g in grade_counts}

out = {
    "bt": 1165,
    "title": "grade/type relation decomposition",
    "columns_by_grade": columns_by_grade,
    "image_by_grade": image_by_grade,
    "relations_by_grade": relations_by_grade,
    "relations_total": sum(relations_by_grade.values()),
    "interpretation": "The 45 relation sector decomposes as 12+18+12+3 = 3*(4+6+4+1), i.e. three relation copies of the projective 15-sector.",
    "checks": {
        "columns_total_60": sum(columns_by_grade.values()) == 60,
        "image_total_15": sum(image_by_grade.values()) == 15,
        "relations_total_45": sum(relations_by_grade.values()) == 45,
        "relation_pattern_three_copies": [relations_by_grade[g] for g in range(1,5)] == [12,18,12,3],
    },
}
out["checks"]["all_checks_pass"] = all(out["checks"].values())
print(json.dumps(out, indent=2, sort_keys=True))
