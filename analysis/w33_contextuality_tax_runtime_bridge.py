#!/usr/bin/env python3
"""Price the Pass 57 point-star tax in S3 admission-controller runtime units.

Pass 57 proves that an optimal classical assignment on W(3,3) fails exactly one
movable point-star: four line contexts through one point, hence 1/10 of the 40
contexts.  The S3 admission controller separately prices the completion frontier
as 4320 ordered paths, three completion probes per path, and four runtime ticks
per probe.

This witness joins those two already-promoted surfaces.  It recomputes the
ordered-path carrier from the W33 line graph and verifies that every line context
is the middle of 108 ordered paths.  Therefore one point-star owns:

    4 line contexts * 108 ordered paths/line = 432 ordered paths
    432 ordered paths * 3 completions/path = 1296 probes
    1296 probes * 4 ticks/probe = 5184 runtime ticks

The contextuality tax is exactly one tenth of the S3 admission supercycle in
contexts, ordered paths, completion probes, and runtime ticks.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from scripts.w33_h4_branch_selection_search import _ordered_nonlocal_paths  # noqa: E402
from scripts.w33_h4_orbital_no_go import _line_intersection_graph  # noqa: E402
import w33_contextuality_tax as tax  # noqa: E402


OUT = ROOT / "data" / "w33_contextuality_tax_runtime_bridge.json"


def _load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def _fraction_row(numerator: int, denominator: int) -> dict[str, Any]:
    value = Fraction(numerator, denominator)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "value": f"{value.numerator}/{value.denominator}",
    }


def _contextuality_tax_classification() -> dict[str, Any]:
    try:
        target, failure_sets, all_stars, star_points = tax.classify_failure_sets(3)
        return {
            "source": "live_ilp_classification",
            "max_sat": target,
            "failure_sets": failure_sets,
            "all_stars": bool(all_stars),
            "star_points": star_points,
            "source_all_pass": True,
        }
    except ModuleNotFoundError as exc:
        if exc.name != "scipy":
            raise
        promoted = _load_json("data/w33_contextuality_tax.json")
        q3 = promoted["q3_classification"]
        return {
            "source": "promoted_json_fallback",
            "fallback_reason": "scipy is not installed in this shell",
            "max_sat": int(q3["max_sat"]),
            "failure_sets": [tuple(row) for row in q3["failure_sets"]],
            "all_stars": bool(q3["all_point_stars"]),
            "star_points": q3["star_centers"],
            "source_all_pass": bool(promoted.get("all_pass")),
        }


def build_certificate() -> dict[str, Any]:
    admission = _load_json("data/w33_s3_completion_admission_controller.json")
    word = admission["admission_word"]

    lines, line_adjacency = _line_intersection_graph()
    ordered_paths = _ordered_nonlocal_paths(lines, line_adjacency)
    paths_by_middle_line = Counter(path[1] for path in ordered_paths)

    incident_lines_by_point: dict[int, list[int]] = defaultdict(list)
    for line_id, line in enumerate(lines):
        for point in line:
            incident_lines_by_point[point].append(line_id)

    star_path_counts = {
        point: sum(paths_by_middle_line[line_id] for line_id in line_ids)
        for point, line_ids in incident_lines_by_point.items()
    }

    classification = _contextuality_tax_classification()
    target = int(classification["max_sat"])
    failure_sets = classification["failure_sets"]
    all_stars = bool(classification["all_stars"])
    star_points = classification["star_points"]

    context_count = len(lines)
    contexts_per_star = 4
    ordered_path_count = len(ordered_paths)
    ordered_paths_per_line = next(iter(paths_by_middle_line.values()))
    star_ordered_paths = contexts_per_star * ordered_paths_per_line
    completions_per_path = int(word["completions_per_path"])
    runtime_slots_per_probe = int(word["runtime_slots_per_probe"])
    path_word_ticks = int(word["path_word_ticks"])
    completion_probes = int(word["ordered_paths"]) * completions_per_path
    star_completion_probes = star_ordered_paths * completions_per_path
    supercycle_ticks = int(word["ordered_paths"]) * path_word_ticks
    star_runtime_ticks = star_ordered_paths * path_word_ticks
    line_context_runtime_ticks = ordered_paths_per_line * path_word_ticks

    tax_fraction = _fraction_row(contexts_per_star, context_count)
    path_fraction = _fraction_row(star_ordered_paths, ordered_path_count)
    probe_fraction = _fraction_row(star_completion_probes, completion_probes)
    runtime_fraction = _fraction_row(star_runtime_ticks, supercycle_ticks)

    checks = {
        "source_admission_controller_verified": admission["verified"] is True,
        "source_contextuality_tax_classification_is_exhaustive": (
            classification["source_all_pass"] is True
            and target == 36
            and len(failure_sets) == 40
            and all_stars is True
            and len({point for point in star_points if point is not None}) == 40
        ),
        "line_graph_has_40_contexts": context_count == 40,
        "ordered_path_count_is_4320": ordered_path_count == 4320,
        "every_line_context_has_108_middle_paths": dict(Counter(paths_by_middle_line.values()))
        == {108: 40},
        "every_point_is_incident_with_4_line_contexts": dict(
            Counter(len(line_ids) for line_ids in incident_lines_by_point.values())
        )
        == {4: 40},
        "every_point_star_owns_432_ordered_paths": dict(Counter(star_path_counts.values()))
        == {432: 40},
        "s3_word_is_3_by_4_equals_12": (
            completions_per_path == 3
            and runtime_slots_per_probe == 4
            and path_word_ticks == 12
        ),
        "point_star_probe_budget_is_1296": star_completion_probes == 1296,
        "point_star_runtime_tax_is_5184": star_runtime_ticks == 5184,
        "runtime_fraction_matches_contextuality_tax": (
            tax_fraction == path_fraction == probe_fraction == runtime_fraction
            and runtime_fraction["value"] == "1/10"
        ),
        "supercycle_runtime_stays_51840": supercycle_ticks == 51840,
    }

    return {
        "theorem": "W33 contextuality tax runtime bridge",
        "verified": all(checks.values()),
        "breakthrough": (
            "The Pass 57 point-star defect is now priced in the S3 admission "
            "controller's own runtime units.  One failed star is four line "
            "contexts, 432 ordered path words, 1296 completion probes, and "
            "5184 runtime ticks: exactly one tenth of the 51840-tick supercycle."
        ),
        "source_certificates": [
            "analysis/w33_contextuality_tax.py",
            "data/w33_contextuality_tax.json",
            "analysis/w33_s3_completion_admission_controller.py",
            "data/w33_s3_completion_admission_controller.json",
        ],
        "contextuality_tax_surface": {
            "q": 3,
            "max_sat_contexts": target,
            "line_contexts": context_count,
            "deficit_contexts": contexts_per_star,
            "optimal_failure_sets": len(failure_sets),
            "all_failure_sets_are_point_stars": bool(all_stars),
            "movable_star_centers": len(
                {point for point in star_points if point is not None}
            ),
            "classification_source": classification["source"],
            "classification_fallback_reason": classification.get("fallback_reason"),
            "context_tax_fraction": tax_fraction,
        },
        "ordered_path_runtime_surface": {
            "ordered_paths": ordered_path_count,
            "ordered_paths_per_line_context": ordered_paths_per_line,
            "line_context_runtime_ticks": line_context_runtime_ticks,
            "completions_per_path": completions_per_path,
            "runtime_slots_per_probe": runtime_slots_per_probe,
            "path_word_ticks": path_word_ticks,
            "completion_probes": completion_probes,
            "supercycle_runtime_ticks": supercycle_ticks,
            "middle_line_distribution": dict(
                sorted(Counter(paths_by_middle_line.values()).items())
            ),
        },
        "point_star_runtime_tax": {
            "contexts_per_star": contexts_per_star,
            "ordered_paths_per_star": star_ordered_paths,
            "completion_probes_per_star": star_completion_probes,
            "runtime_ticks_per_star": star_runtime_ticks,
            "identity": "4 contexts * 108 paths/context * 3 completions/path * 4 ticks/completion = 5184",
            "runtime_tax_fraction": runtime_fraction,
        },
        "fraction_ladder": {
            "contexts": tax_fraction,
            "ordered_paths": path_fraction,
            "completion_probes": probe_fraction,
            "runtime_ticks": runtime_fraction,
        },
        "bridge_reading": (
            "The scheduler does not need to reserve an amorphous quantum budget.  "
            "For each classical assignment it can reserve one movable point-star "
            "window: 5184 runtime ticks, steerable to any of the 40 point centers.  "
            "That is the same 1/10 quantity as the contextual fraction."
        ),
        "checks": checks,
        "claim_boundary": [
            "This is exact finite runtime accounting on the promoted W33/S3 certificates.",
            "It does not supply measured photonic branch evidence.",
            "It does not claim a canonical assignment-to-spread or star-to-lab-channel bijection.",
            "The 540-cover no-go remains active; the bridge prices escalation, not a solved selector.",
        ],
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print("  tax runtime: 4*108*3*4 = 5184 = 1/10 of 51840")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
