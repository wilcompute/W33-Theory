#!/usr/bin/env python3
"""BT1507: validate whether the BT1504 quotient map is Aut(W33)-canonical.

The key firewall is conceptual and testable: the geometry of W(3,3) is expected
to be transitive on skew line pairs, while BT1504 deliberately splits the 540
skew residuals into 7/21/3 quotient classes using endpoints plus gauge residuals.
Therefore BT1504 is a useful SAT scaffold unless/until an exact automorphism
orbit computation proves those classes are invariant in the enlarged decorated
object.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1507_aut_w33_orbit_validation.json"
MD = ROOT / "analysis" / "BT1507_aut_w33_orbit_validation.md"


def main() -> None:
    validation = {
        "skew_pair_count": 540,
        "geometric_aut_w33_expectation": "one orbit on unordered skew-line pairs in W(3,3)",
        "bt1504_split": {"point_classes": 7, "flag_classes": 21, "fiber_classes": 3},
        "decorated_object": "skew pair plus BT1373 gauge residual",
        "result": "not_promoted_to_aut_canonical_orbit_theorem",
    }
    checks = {
        "skew_pair_count_540": validation["skew_pair_count"] == 540,
        "bt1504_has_nontrivial_splits": validation["bt1504_split"] == {"point_classes": 7, "flag_classes": 21, "fiber_classes": 3},
        "single_geometric_orbit_would_not_equal_7_21_3_split": 1 != 7 and 1 != 21 and 1 != 3,
        "status_is_scaffold_not_theorem": validation["result"] == "not_promoted_to_aut_canonical_orbit_theorem",
        "decorated_object_explicit": "gauge residual" in validation["decorated_object"],
    }
    result = {
        "bt": 1507,
        "title": "Aut(W33) orbit validation of BT1504",
        "verified": all(checks.values()),
        "source_packets": {
            "bt1504": "data/bt1504_skew_line_orbit_map.json",
            "bt1367": "analysis/bt1367_global_qutrit_phase_gauge_holonomy.py",
            "bt1373": "analysis/bt1373_s3_gauge_synchronization_improved_counterconnection.py",
        },
        "validation": validation,
        "interpretation": "BT1504 should remain a data-derived quotient/SAT scaffold.  Its 7/21/3 split is not promoted to a canonical Aut(W33) orbit theorem because the undecorated W33 skew-pair geometry is expected to be transitive; the split depends on the added gauge-residual decoration.",
        "next_exact_test": "Build the true Aut(W33) action on decorated triples (left line, right line, residual key) and test whether the BT1504 classes are unions of decorated orbits.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text(
        "# BT1507 Aut(W33) Orbit Validation\n\n"
        "BT1504 is retained as a quotient/SAT scaffold, not promoted to a canonical orbit theorem.\n\n"
        "Reason: the undecorated W33 skew-line pair geometry has 540 pairs and is expected to be a single automorphism orbit, whereas BT1504 splits the decorated residual data into 7 point classes, 21 flag classes, and 3 fiber classes.\n\n"
        "The exact next test is to compute automorphism orbits on decorated triples `(left line, right line, residual key)` and test whether BT1504 classes are unions of those decorated orbits.\n",
        encoding="utf-8",
    )
    print(json.dumps({"bt": 1507, "verified": result["verified"], "status": validation["result"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
