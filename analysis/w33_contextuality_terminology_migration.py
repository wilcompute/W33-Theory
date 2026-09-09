#!/usr/bin/env python3
"""Freeze the contextuality terminology boundary used by the Witting protocol.

Two exact quantities coexist for the W(3,3) Witting/KS support model:

  Abramsky-Barbosa contextual fraction = 1
      because there is no global section/ovoid at all (strong contextuality),

  KS satisfiability defect = (40-36)/40 = 1/10
      because an optimal global Boolean marking can satisfy 36 of 40 contexts.

Older repository material used "contextual fraction" for the second quantity.
Pass 1080 and Pass 1099 corrected that terminology.  This certificate gates the
current BT1408/BT1409 Witting communication chain so the stale name cannot
re-enter those generated packets or their executable source.

Scope: this is a migration gate for the active Witting communication chain, not
a claim that every historical archive file has been rewritten.  Legacy files
are deliberately listed rather than silently erased.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_contextuality_terminology_migration.json"


def load(relpath: str):
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def build_result():
    p1080 = load("data/w33_pass1080_contextual_fraction_audit.json")
    p1099 = load("data/w33_pass1099_exact_ks_maximum.json")
    bt1408 = load("data/bt1408_witting_contextual_communication_bridge.json")
    bt1409 = load("data/bt1409_witting_duplex_admission_scheduler.json")

    b8 = bt1408["contextuality_budget"]
    b9 = bt1409["contextuality_quantities"]
    q1080 = p1080["contextual_fraction"]["W33"]
    q1099 = p1099["two_quantities_that_coexist"]

    source1408 = (ROOT / "tools" / "bt1408_witting_contextual_communication_bridge.py").read_text(encoding="utf-8")
    source1409 = (ROOT / "tools" / "bt1409_witting_duplex_admission_scheduler.py").read_text(encoding="utf-8")

    checks = {
        "pass1080_AB_contextual_fraction_is_one": q1080["value"] == 1.0 and q1080["ovoids"] == 0,
        "pass1099_KS_defect_is_one_tenth": (
            p1099["exact_maximum_satisfiable_contexts"] == 36
            and p1099["total_contexts"] == 40
            and p1099["defect"] == "1/10"
        ),
        "pass1099_names_both_quantities": q1099 == {
            "abramsky_barbosa_contextual_fraction": 1,
            "ks_satisfiability_defect": "1/10",
            "why_both": q1099["why_both"],
        },
        "bt1408_uses_precise_names": (
            b8["abramsky_barbosa_contextual_fraction"] == 1
            and b8["ks_satisfiability_defect"] == "1/10"
            and "contextual_fraction" not in b8
        ),
        "bt1409_uses_precise_names": (
            b9["abramsky_barbosa_contextual_fraction"] == 1
            and b9["ks_satisfiability_defect"] == "1/10"
            and "contextual_fraction" not in b9
        ),
        "bt1408_source_contains_both_precise_names": (
            '"ks_satisfiability_defect"' in source1408
            and '"abramsky_barbosa_contextual_fraction"' in source1408
        ),
        "bt1409_source_contains_both_precise_names": (
            '"ks_satisfiability_defect"' in source1409
            and '"abramsky_barbosa_contextual_fraction"' in source1409
        ),
    }

    legacy = [
        {
            "path": "analysis/w33_contextual_fraction.py",
            "issue": (
                "Historical producer uses the name contextual_fraction for the "
                "36/40 exactly-one satisfiability defect. Do not interpret that "
                "field as the Abramsky-Barbosa contextual fraction."
            ),
            "authoritative_replacement": [
                "data/w33_pass1080_contextual_fraction_audit.json",
                "data/w33_pass1099_exact_ks_maximum.json",
            ],
        },
        {
            "path": "data/w33_contextual_fraction.json",
            "issue": (
                "Historical frozen schema retains the old field name for backward "
                "compatibility. Its numerical 1/10 belongs to the KS satisfiability "
                "defect observable, not AB contextual fraction."
            ),
            "authoritative_replacement": [
                "data/w33_pass1080_contextual_fraction_audit.json",
                "data/w33_pass1099_exact_ks_maximum.json",
            ],
        },
    ]

    return {
        "schema": "w33.contextuality-terminology-migration.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "authoritative_values": {
            "abramsky_barbosa_contextual_fraction": 1,
            "ks_satisfiability_defect": "1/10",
            "maximum_satisfiable_contexts": "36/40",
            "global_sections_ovoids": 0,
        },
        "active_chain": {
            "bt1408": "data/bt1408_witting_contextual_communication_bridge.json",
            "bt1409": "data/bt1409_witting_duplex_admission_scheduler.json",
            "reading": (
                "The 13/40 Witting communication admission rate, the 1/10 KS "
                "satisfiability defect/witness aperture, and AB contextual fraction "
                "1 are three different quantities and are never interchangeable."
            ),
        },
        "legacy_misnamed_artifacts": legacy,
        "scope_boundary": (
            "PASS means the current BT1408/BT1409 Witting communication chain is "
            "terminologically migrated and cross-checked against Passes 1080 and "
            "1099. Historical files elsewhere in the repository can retain old "
            "names and are not silently rewritten by this certificate."
        ),
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "AB_contextual_fraction": 1,
        "KS_satisfiability_defect": "1/10",
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
