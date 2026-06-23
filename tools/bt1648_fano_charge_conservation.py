#!/usr/bin/env python3
"""BT1648: expose the hidden charge law behind the 80x9 + 88x10 bin profile."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1648_fano_charge_conservation.json"
MD = ROOT / "analysis" / "BT1648_fano_charge_conservation.md"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def classify_bin(role_counts: Counter[str]) -> str:
    if role_counts == {"FUEL_GATE_LINE": 9}:
        return "UNANCHORED_FUEL_BIN"
    if role_counts == {"FUEL_GATE_LINE": 9, "SAME_RAY_CONTROL_ANCHOR": 1}:
        return "SAME_ANCHORED_FUEL_BIN"
    if role_counts == {"COMPATIBLE_CONTROL_RESERVE_LINE": 10}:
        return "COMPATIBLE_RESERVE_BIN"
    raise ValueError(f"unexpected role counts: {dict(role_counts)}")


def main() -> None:
    bt1602 = load_json("data/bt1602_fano_witting_detector_bin_synthesis.json")
    rows = bt1602["detector_bin_rows"]

    role_by_bin: dict[int, Counter[str]] = defaultdict(Counter)
    line_bin_roles: dict[int, dict[int, Counter[str]]] = defaultdict(
        lambda: defaultdict(Counter)
    )
    line_frame_counts: Counter[int] = Counter()
    point_frame_counts: Counter[int] = Counter()
    for row in rows:
        detector_bin = row["detector_bin"]
        role = row["bin_role"]
        fano_line = row["fano_line"]
        fano_point = row["fano_point"]
        role_by_bin[detector_bin][role] += 1
        line_bin_roles[fano_line][detector_bin][role] += 1
        line_frame_counts[fano_line] += 1
        point_frame_counts[fano_point] += 1

    class_by_bin = {
        detector_bin: classify_bin(role_counts)
        for detector_bin, role_counts in sorted(role_by_bin.items())
    }
    class_hist = Counter(class_by_bin.values())
    usage_hist = Counter(
        sum(role_counts.values()) for role_counts in role_by_bin.values()
    )

    line_profiles = {}
    for line, bins in sorted(line_bin_roles.items()):
        local_class_hist = Counter(classify_bin(counts) for counts in bins.values())
        line_profiles[line] = {
            "bins": len(bins),
            "frames": line_frame_counts[line],
            "class_histogram": dict(sorted(local_class_hist.items())),
        }

    high_bins = {
        detector_bin
        for detector_bin, role_counts in role_by_bin.items()
        if sum(role_counts.values()) == 10
    }
    low_bins = {
        detector_bin
        for detector_bin, role_counts in role_by_bin.items()
        if sum(role_counts.values()) == 9
    }
    same_anchor_bins = {
        detector_bin
        for detector_bin, role_counts in role_by_bin.items()
        if role_counts.get("SAME_RAY_CONTROL_ANCHOR") == 1
    }
    compatible_bins = {
        detector_bin
        for detector_bin, role_counts in role_by_bin.items()
        if role_counts.get("COMPATIBLE_CONTROL_RESERVE_LINE") == 10
    }

    charge_equation_lhs = (
        class_hist["UNANCHORED_FUEL_BIN"] * 9
        + class_hist["SAME_ANCHORED_FUEL_BIN"] * (9 + 1)
        + class_hist["COMPATIBLE_RESERVE_BIN"] * 10
    )
    line_equation_lhs = 5 * (16 * 9 + 8 * 10) + 2 * (24 * 10)

    checks = {
        "bt1602_verified": bt1602["verified"] is True,
        "all_168_bins_classified": len(class_by_bin) == 168,
        "class_histogram_is_80_40_48": dict(sorted(class_hist.items()))
        == {
            "COMPATIBLE_RESERVE_BIN": 48,
            "SAME_ANCHORED_FUEL_BIN": 40,
            "UNANCHORED_FUEL_BIN": 80,
        },
        "usage_profile_is_80x9_88x10": dict(sorted(usage_hist.items()))
        == {9: 80, 10: 88},
        "high_bins_are_same_anchors_plus_compatible_reserve": high_bins
        == same_anchor_bins | compatible_bins
        and same_anchor_bins.isdisjoint(compatible_bins)
        and len(high_bins) == 88,
        "low_bins_are_exactly_unanchored_fuel": low_bins
        == {
            detector_bin
            for detector_bin, cls in class_by_bin.items()
            if cls == "UNANCHORED_FUEL_BIN"
        },
        "five_gate_lines_have_16_low_8_anchor_bins": all(
            line_profiles[line]["class_histogram"]
            == {"SAME_ANCHORED_FUEL_BIN": 8, "UNANCHORED_FUEL_BIN": 16}
            and line_profiles[line]["frames"] == 224
            for line in range(5)
        ),
        "two_reserve_lines_are_24_compatible_bins_each": all(
            line_profiles[line]["class_histogram"] == {"COMPATIBLE_RESERVE_BIN": 24}
            and line_profiles[line]["frames"] == 240
            for line in (5, 6)
        ),
        "charge_equation_sums_to_1600": charge_equation_lhs == 1600,
        "line_equation_sums_to_1600": line_equation_lhs == 1600,
        "point_mass_vector_exposes_fixed_witting_gauge_tilt": dict(
            sorted(point_frame_counts.items())
        )
        == {0: 240, 1: 232, 2: 224, 3: 232, 4: 224, 5: 224, 6: 224},
    }

    result = {
        "bt": 1648,
        "title": "Fano charge-conservation law for Witting detector usage",
        "verified": all(checks.values()),
        "source_packets": {
            "fano_witting_bins": "data/bt1602_fano_witting_detector_bin_synthesis.json"
        },
        "charge_identity": {
            "bin_identity": "80*9 + 40*(9+1) + 48*10 = 1600",
            "line_identity": "5*(16*9 + 8*10) + 2*(24*10) = 1600",
            "reading": (
                "The 88 high-usage bins are exactly the 40 same-ray anchors plus "
                "the 48 compatible-control reserve bins; the 80 low bins are the "
                "unanchored contextual-fuel bins."
            ),
        },
        "counts": {
            "active_detector_bins": len(class_by_bin),
            "low_usage_bins": len(low_bins),
            "high_usage_bins": len(high_bins),
            "same_anchor_bins": len(same_anchor_bins),
            "compatible_reserve_bins": len(compatible_bins),
        },
        "histograms": {
            "class": dict(sorted(class_hist.items())),
            "usage": dict(sorted(usage_hist.items())),
            "line_frames": dict(sorted(line_frame_counts.items())),
            "point_frames": dict(sorted(point_frame_counts.items())),
        },
        "line_profiles": line_profiles,
        "sample_bins": [
            {
                "detector_bin": detector_bin,
                "class": class_by_bin[detector_bin],
                "role_counts": dict(sorted(role_by_bin[detector_bin].items())),
            }
            for detector_bin in list(range(12)) + list(range(156, 168))
        ],
        "interpretation": (
            "BT1648 shows the 80x9 + 88x10 detector profile is a conserved charge, "
            "not an empirical-looking histogram. Five Fano gate lines carry fuel plus "
            "same-ray anchors; two reserve lines carry compatible controls. The line "
            "loads are exact while the point loads retain the chosen Witting gauge tilt."
        ),
        "honesty_boundary": (
            "This is an exact incidence and usage theorem. It does not claim detector "
            "efficiency, measured rates, or Standard Model numerical correctness."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1648 Fano Charge-Conservation Law\n\n"
        "BT1648 explains the `80x9 + 88x10 = 1600` usage profile as a conserved "
        "Fano charge:\n\n"
        "```text\n"
        "80 unanchored fuel bins * 9\n"
        "+ 40 same-anchored fuel bins * (9 fuel + 1 same-ray control)\n"
        "+ 48 compatible reserve bins * 10\n"
        "= 1600 frames\n"
        "```\n\n"
        "Equivalently, the seven Fano lines split as `5` gate lines and `2` "
        "reserve lines:\n\n"
        "```text\n"
        "5*(16*9 + 8*10) + 2*(24*10) = 1600.\n"
        "```\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1648,
                "verified": result["verified"],
                "bins": result["counts"]["active_detector_bins"],
                "frames": charge_equation_lhs,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
