#!/usr/bin/env python3
"""BT761 — fail-closed phase-duo gluing runner.

BT756 pins the full BT753 local enumeration.  BT757 specifies the global BT741
register gluing test.  This runner performs the second-stage acceptance check
when both artifacts are present:

  data/bt753_phase_duo_candidate_enumerator.json
  data/bt741_global_register_quotient.json

The runner is intentionally fail-closed.  If either artifact is missing or if
row identifiers do not align, no candidate is accepted.  This prevents the
rank-81 local selector from being conflated with a globally glued selector.
"""
from __future__ import annotations

import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
BT753 = ROOT / "data" / "bt753_phase_duo_candidate_enumerator.json"
BT741 = ROOT / "data" / "bt741_global_register_quotient.json"
OUT = ROOT / "data" / "bt761_phase_duo_gluing_results.json"

REQUIRED_LOCAL = {
    "selected_rows": 2160,
    "rank_mod_1000003": 81,
    "root_triples_hit": 540,
}
REQUIRED_DISTRIBUTION = {"4": 540}


def load(path: Path):
    return json.loads(path.read_text())


def local_pass(row: dict) -> bool:
    for k, v in REQUIRED_LOCAL.items():
        if row.get(k) != v:
            return False
    return row.get("root_hit_distribution") == REQUIRED_DISTRIBUTION and row.get("root_uniform_4") is True


def fail(reason: str) -> dict:
    return {
        "theorem": "BT761 phase-duo gluing runner",
        "global_status": reason,
        "accepted_candidates": [],
        "all_tests_pass": False,
        "boundary": "Fail-closed: no global selector is accepted unless BT753 local rows and BT741 register quotient are both present and linked.",
    }


def main():
    if not BT753.exists():
        result = fail("missing_bt753_result")
    elif not BT741.exists():
        result = fail("missing_bt741_register_quotient")
    else:
        local = load(BT753)
        glue = load(BT741)
        candidates = local.get("candidates", {})
        accepted = []
        rejected = []
        quotient = glue.get("candidates", {})
        for label, row in sorted(candidates.items()):
            reasons = []
            if not local_pass(row):
                reasons.append("local_BT754_tests_failed")
            g = quotient.get(label)
            if g is None:
                reasons.append("missing_gluing_record")
            else:
                if g.get("number_of_global_register_classes") != 16:
                    reasons.append("global_register_classes_not_16")
                if g.get("global_register_dimension") != 4:
                    reasons.append("global_register_dimension_not_4")
                if g.get("each_class_nonempty") is not True:
                    reasons.append("empty_register_class")
                if g.get("flat_transport") is not True:
                    reasons.append("transport_not_flat")
            if reasons:
                rejected.append({"label": label, "reasons": reasons})
            else:
                accepted.append(label)
        result = {
            "theorem": "BT761 phase-duo gluing runner",
            "bt753_source": str(BT753.relative_to(ROOT)),
            "bt741_source": str(BT741.relative_to(ROOT)),
            "candidate_count": len(candidates),
            "accepted_candidates": accepted,
            "rejected_candidates": rejected,
            "global_status": "complete" if len(accepted) == len(candidates) == 24 else "failed_or_partial",
            "all_tests_pass": len(accepted) == 24 and not rejected,
            "required_tests": [
                "T1 selected_rows = 2160",
                "T2 rank_mod_1000003 = 81",
                "T3 root_triples_hit = 540",
                "T4 root_hit_distribution = {4: 540}",
                "T5 global_register_dimension = 4 with 16 nonempty classes and flat transport",
            ],
            "boundary": "Acceptance means local BT754 plus global BT741 gluing. Missing or partial gluing records reject candidates.",
        }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result.get("all_tests_pass", False):
        # This is an expected fail-closed state until the full artifacts exist.
        return


if __name__ == "__main__":
    main()
