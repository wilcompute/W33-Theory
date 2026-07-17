#!/usr/bin/env python3
"""Executable eighth-tax scheduler for the W33 contextuality reserve.

The packing law proves that seven point-star tax reserves can be isolated, but
the eighth tax must collide with the active 7-pack.  This script turns that
frontier into a deterministic policy surface:

* one shared line: time-slice only the shared line surface;
* two shared lines: serialize the new star as a whole reserve;
* three or four shared lines: keep the seven-pack isolated and escalate the new
  tax to the holonomy queue.

The output also joins the policy to the existing packet-latency benchmark.  That
benchmark is not a physical throughput claim; it is an already-promoted
control-plane measurement showing that clock-native packet scheduling improves
packet completion while keeping connector count zero.  Here it supplies the
systems context for the tax scheduler: the exception budget is finite, and the
normal packet clock already has a measured policy advantage.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from html import escape
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.w33_h4_orbital_no_go import _line_intersection_graph  # noqa: E402


OUT_JSON = ROOT / "data" / "w33_contextuality_tax_scheduler.json"
OUT_SVG = ROOT / "docs" / "holonet_contextuality_tax_scheduler.svg"


def _load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def _fraction(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": round(float(value), 6),
        "value": f"{value.numerator}/{value.denominator}",
    }


def _star_lines(lines: list[tuple[int, int, int, int]]) -> dict[int, list[int]]:
    star: dict[int, list[int]] = defaultdict(list)
    for line_id, line in enumerate(lines):
        for point in line:
            star[point].append(line_id)
    return {point: sorted(line_ids) for point, line_ids in star.items()}


def _shared_lines(
    center: int, active_centers: list[int], star_lines: dict[int, list[int]]
) -> dict[int, list[int]]:
    center_lines = set(star_lines[center])
    return {
        active: sorted(center_lines & set(star_lines[active]))
        for active in active_centers
        if center_lines & set(star_lines[active])
    }


def _policy_for_overlap(overlap_count: int) -> str:
    if overlap_count <= 1:
        return "TIME_SLICE_SHARED_LINE"
    if overlap_count == 2:
        return "SERIALIZE_WHOLE_STAR"
    return "ESCALATE_HOLONOMY"


def _admission_case(
    center: int,
    active_centers: list[int],
    star_lines: dict[int, list[int]],
    *,
    line_runtime_ticks: int,
    star_runtime_ticks: int,
    supercycle_ticks: int,
) -> dict[str, Any]:
    shared_by_center = _shared_lines(center, active_centers, star_lines)
    shared_line_ids = sorted(
        {line_id for line_ids in shared_by_center.values() for line_id in line_ids}
    )
    overlap_count = len(shared_line_ids)
    decision = _policy_for_overlap(overlap_count)
    active_ticks = len(active_centers) * star_runtime_ticks
    service_ticks_for_8 = (len(active_centers) + 1) * star_runtime_ticks
    unique_union_ticks = active_ticks + (4 - overlap_count) * line_runtime_ticks
    localized_collision_ticks = overlap_count * line_runtime_ticks
    slack_if_served = supercycle_ticks - service_ticks_for_8

    return {
        "center": center,
        "shared_line_count": overlap_count,
        "shared_lines": shared_line_ids,
        "colliding_active_centers": {
            str(active): lines for active, lines in sorted(shared_by_center.items())
        },
        "decision": decision,
        "policy_reason": {
            "TIME_SLICE_SHARED_LINE": (
                "single shared line: duplicate only the shared 1296-tick line surface"
            ),
            "SERIALIZE_WHOLE_STAR": (
                "two shared lines: avoid coupled local edits by serializing the new 5184-tick star"
            ),
            "ESCALATE_HOLONOMY": (
                "three or more shared lines: preserve the isolated 7-pack and escalate the new tax"
            ),
        }[decision],
        "active_isolated_ticks_before_request": active_ticks,
        "unique_union_ticks_without_time_slice": unique_union_ticks,
        "localized_collision_ticks": localized_collision_ticks,
        "service_ticks_if_time_sliced_or_serialized": service_ticks_for_8,
        "slack_ticks_if_eighth_served_this_supercycle": slack_if_served,
        "deferred_ticks_if_escalated": 0
        if decision != "ESCALATE_HOLONOMY"
        else star_runtime_ticks,
    }


def _choose_policy_examples(
    active_centers: list[int],
    star_lines: dict[int, list[int]],
) -> dict[str, int]:
    outside = [center for center in sorted(star_lines) if center not in active_centers]
    by_overlap: dict[int, list[int]] = defaultdict(list)
    for center in outside:
        by_overlap[len(_shared_lines(center, active_centers, star_lines))].append(center)
    return {
        "time_slice_example": by_overlap[1][0],
        "serialize_example": by_overlap[2][0],
        "escalate_example": by_overlap[3][0],
        "hard_escalate_example": by_overlap[4][0],
    }


def _benchmark_bridge(packet_latency: dict[str, Any]) -> dict[str, Any]:
    rows = packet_latency["benchmark_rows"]
    by_label = {row["label"]: row for row in rows}

    def row_summary(label: str) -> dict[str, Any]:
        row = by_label[label]
        packet_count = int(row["packet_count"])
        active_slots = int(row["active_policy"]["total_clock_slots"])
        native_slots = int(row["clock_native_policy"]["total_clock_slots"])
        return {
            "label": label,
            "packet_count": packet_count,
            "active_clock_slots": active_slots,
            "clock_native_slots": native_slots,
            "active_packets_per_slot": _fraction(Fraction(packet_count, active_slots)),
            "clock_native_packets_per_slot": _fraction(
                Fraction(packet_count, native_slots)
            ),
            "native_throughput_multiplier_vs_active": _fraction(
                Fraction(active_slots, native_slots)
            ),
            "native_faster_packet_count": row["packet_delta_summary"][
                "native_faster_packet_count"
            ],
            "native_not_slower_packet_count": row["packet_delta_summary"][
                "native_not_slower_packet_count"
            ],
        }

    certified = row_summary("certified_one_copy")
    deterministic_4x = row_summary("deterministic_4x")
    return {
        "source": "data/w33_packet_latency_benchmark.json",
        "status": packet_latency["status"],
        "certified_one_copy": certified,
        "deterministic_4x": deterministic_4x,
        "reading": (
            "The tax scheduler controls exception-reserve admission; the packet "
            "latency benchmark separately shows that the normal clock-native "
            "packet policy finishes 106/132 packets earlier in the deterministic "
            "4x row while remaining connector-free."
        ),
    }


def _svg_panel(
    active_centers: list[int],
    cases: dict[str, dict[str, Any]],
    path: Path,
) -> None:
    width, height = 920, 600
    cell_x, cell_y = 92, 66
    origin_x, origin_y = 76, 100

    def coord(point: int) -> tuple[int, int]:
        return origin_x + (point % 8) * cell_x, origin_y + (point // 8) * cell_y

    time_center = int(cases["time_slice"]["center"])
    serialize_center = int(cases["serialize"]["center"])
    escalate_center = int(cases["escalate"]["center"])
    hard_center = int(cases["hard_escalate"]["center"])
    color_by_point = {
        **{point: "#2563eb" for point in active_centers},
        time_center: "#f97316",
        serialize_center: "#d97706",
        escalate_center: "#dc2626",
        hard_center: "#7f1d1d",
    }

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Holonet contextuality tax scheduler</title>',
        '<desc id="desc">The seven disjoint point-star reserves and representative eighth-tax decisions.</desc>',
        '<rect width="920" height="600" fill="#f8fafc"/>',
        '<text x="40" y="42" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#111827">Contextuality Tax Scheduler</text>',
        '<text x="40" y="70" font-family="Arial, sans-serif" font-size="14" fill="#374151">Seven reserves stay isolated; the eighth tax is admitted by overlap count.</text>',
    ]

    for case_name, case in cases.items():
        cx, cy = coord(int(case["center"]))
        for active, shared in case["colliding_active_centers"].items():
            ax, ay = coord(int(active))
            stroke = {
                "time_slice": "#f97316",
                "serialize": "#d97706",
                "escalate": "#dc2626",
                "hard_escalate": "#7f1d1d",
            }[case_name]
            width_px = 2 if len(shared) == 1 else 3
            lines.append(
                f'<line x1="{cx}" y1="{cy}" x2="{ax}" y2="{ay}" stroke="{stroke}" stroke-width="{width_px}" stroke-opacity="0.42"/>'
            )

    for point in range(40):
        x, y = coord(point)
        fill = color_by_point.get(point, "#e5e7eb")
        stroke = "#1f2937" if point in active_centers else "#64748b"
        label_fill = "#ffffff" if point in color_by_point else "#111827"
        lines.extend(
            [
                f'<circle cx="{x}" cy="{y}" r="20" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>',
                f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="{label_fill}">{point}</text>',
            ]
        )

    legend = [
        ("#2563eb", "active 7-pack"),
        ("#f97316", "time-slice: 1 shared line"),
        ("#d97706", "serialize: 2 shared lines"),
        ("#dc2626", "escalate: 3 shared lines"),
        ("#7f1d1d", "hard escalate: 4 shared lines"),
    ]
    for index, (fill, text) in enumerate(legend):
        y = 456 + index * 24
        lines.append(f'<rect x="40" y="{y - 14}" width="16" height="16" rx="3" fill="{fill}"/>')
        lines.append(
            f'<text x="66" y="{y}" font-family="Arial, sans-serif" font-size="14" fill="#111827">{escape(text)}</text>'
        )

    callouts = [
        ("single reserve", "5184 ticks"),
        ("max isolated", "7 reserves = 36288 ticks"),
        ("served eighth", "8 reserves = 41472 ticks"),
        ("slack", "10368 ticks"),
        ("hard shortfall", "3 * 5184 = 15552 ticks"),
    ]
    for index, (label, value) in enumerate(callouts):
        x = 380 + (index % 2) * 250
        y = 450 + (index // 2) * 48
        lines.append(f'<rect x="{x}" y="{y - 26}" width="220" height="36" rx="6" fill="#ffffff" stroke="#cbd5e1"/>')
        lines.append(
            f'<text x="{x + 12}" y="{y - 8}" font-family="Arial, sans-serif" font-size="12" fill="#475569">{escape(label)}</text>'
        )
        lines.append(
            f'<text x="{x + 12}" y="{y + 7}" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#111827">{escape(value)}</text>'
        )

    lines.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_certificate() -> dict[str, Any]:
    packing = _load_json("data/w33_contextuality_tax_packing_law.json")
    runtime = _load_json("data/w33_contextuality_tax_runtime_bridge.json")
    packet_latency = _load_json("data/w33_packet_latency_benchmark.json")
    lines, _line_adjacency = _line_intersection_graph()
    star_lines = _star_lines(lines)

    active_centers = packing["seven_reserve_witness"]["centers"]
    examples = _choose_policy_examples(active_centers, star_lines)
    line_runtime_ticks = runtime["ordered_path_runtime_surface"][
        "line_context_runtime_ticks"
    ]
    star_runtime_ticks = runtime["point_star_runtime_tax"]["runtime_ticks_per_star"]
    supercycle_ticks = runtime["ordered_path_runtime_surface"][
        "supercycle_runtime_ticks"
    ]

    cases = {
        "time_slice": _admission_case(
            examples["time_slice_example"],
            active_centers,
            star_lines,
            line_runtime_ticks=line_runtime_ticks,
            star_runtime_ticks=star_runtime_ticks,
            supercycle_ticks=supercycle_ticks,
        ),
        "serialize": _admission_case(
            examples["serialize_example"],
            active_centers,
            star_lines,
            line_runtime_ticks=line_runtime_ticks,
            star_runtime_ticks=star_runtime_ticks,
            supercycle_ticks=supercycle_ticks,
        ),
        "escalate": _admission_case(
            examples["escalate_example"],
            active_centers,
            star_lines,
            line_runtime_ticks=line_runtime_ticks,
            star_runtime_ticks=star_runtime_ticks,
            supercycle_ticks=supercycle_ticks,
        ),
        "hard_escalate": _admission_case(
            examples["hard_escalate_example"],
            active_centers,
            star_lines,
            line_runtime_ticks=line_runtime_ticks,
            star_runtime_ticks=star_runtime_ticks,
            supercycle_ticks=supercycle_ticks,
        ),
    }

    overlap_distribution = Counter(
        len(_shared_lines(center, active_centers, star_lines))
        for center in sorted(star_lines)
        if center not in active_centers
    )
    benchmark = _benchmark_bridge(packet_latency)
    checks = {
        "source_packing_law_verified": packing["verified"] is True,
        "source_runtime_bridge_verified": runtime["verified"] is True,
        "source_packet_latency_benchmark_passed": packet_latency["status"] == "PASS",
        "active_pack_has_seven_centers": len(active_centers) == 7,
        "time_slice_case_has_one_shared_line": cases["time_slice"][
            "shared_line_count"
        ]
        == 1
        and cases["time_slice"]["decision"] == "TIME_SLICE_SHARED_LINE",
        "serialize_case_has_two_shared_lines": cases["serialize"]["shared_line_count"]
        == 2
        and cases["serialize"]["decision"] == "SERIALIZE_WHOLE_STAR",
        "escalation_cases_have_three_or_more_shared_lines": cases["escalate"][
            "shared_line_count"
        ]
        == 3
        and cases["hard_escalate"]["shared_line_count"] == 4
        and cases["escalate"]["decision"] == "ESCALATE_HOLONOMY"
        and cases["hard_escalate"]["decision"] == "ESCALATE_HOLONOMY",
        "served_eighth_fits_with_10368_tick_slack": all(
            case["service_ticks_if_time_sliced_or_serialized"] == 41_472
            and case["slack_ticks_if_eighth_served_this_supercycle"] == 10_368
            for case in cases.values()
        ),
        "eighth_candidate_overlap_distribution_matches_fixture": dict(
            sorted(overlap_distribution.items())
        )
        == {1: 7, 2: 9, 3: 9, 4: 8},
        "packet_benchmark_4x_has_106_of_132_native_faster": benchmark[
            "deterministic_4x"
        ]["native_faster_packet_count"]
        == 106
        and benchmark["deterministic_4x"]["packet_count"] == 132,
        "certified_clock_native_throughput_multiplier_is_22_over_15": benchmark[
            "certified_one_copy"
        ]["native_throughput_multiplier_vs_active"]["value"]
        == "22/15",
    }

    return {
        "theorem": "W33 contextuality tax eighth-admission scheduler",
        "verified": all(checks.values()),
        "breakthrough": (
            "The first forced-collision tax now has a deterministic admission "
            "policy.  One shared line is time-sliced locally, two shared lines "
            "serialize the new star, and three or four shared lines escalate to "
            "the holonomy queue.  Serving an eighth reserve consumes 41472 ticks "
            "and leaves 10368 ticks of supercycle slack; preserving the isolated "
            "7-pack escalates the new 5184-tick tax."
        ),
        "source_certificates": [
            "data/w33_contextuality_tax_packing_law.json",
            "data/w33_contextuality_tax_runtime_bridge.json",
            "data/w33_packet_latency_benchmark.json",
        ],
        "outputs": {
            "json": "data/w33_contextuality_tax_scheduler.json",
            "svg": "docs/holonet_contextuality_tax_scheduler.svg",
        },
        "active_isolated_pack": {
            "centers": active_centers,
            "runtime_ticks": packing["packing_capacity"]["max_disjoint_runtime_ticks"],
            "single_star_ticks": star_runtime_ticks,
            "line_context_runtime_ticks": line_runtime_ticks,
        },
        "eighth_tax_policy": {
            "policy_table": [
                {
                    "shared_line_count": "0",
                    "decision": "ADMIT_ISOLATED",
                    "note": "possible before the 7-pack is full",
                },
                {
                    "shared_line_count": "1",
                    "decision": "TIME_SLICE_SHARED_LINE",
                    "note": "local 1296-tick duplicate of the shared line surface",
                },
                {
                    "shared_line_count": "2",
                    "decision": "SERIALIZE_WHOLE_STAR",
                    "note": "serialize the new 5184-tick star to avoid coupled local edits",
                },
                {
                    "shared_line_count": "3-4",
                    "decision": "ESCALATE_HOLONOMY",
                    "note": "preserve the isolated 7-pack and escalate the new tax",
                },
            ],
            "candidate_overlap_distribution_after_witness_pack": dict(
                sorted(overlap_distribution.items())
            ),
            "cases": cases,
        },
        "throughput_bridge": benchmark,
        "checks": checks,
        "claim_boundary": [
            "This is an admission policy for finite runtime reserves, not measured photonic throughput.",
            "The packet-latency rows are reused as control-plane benchmark context only.",
            "Escalated taxes are deferred to the holonomy queue; this script does not solve that queue.",
            "The SVG is a scheduler panel over point ids, not a physical chip layout.",
        ],
    }


def main() -> int:
    cert = build_certificate()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _svg_panel(
        cert["active_isolated_pack"]["centers"],
        cert["eighth_tax_policy"]["cases"],
        OUT_SVG,
    )
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print("  eighth tax: time-slice / serialize / escalate policy emitted")
    print("  served eighth ticks: 41472, slack: 10368")
    print(f"  wrote {OUT_JSON}")
    print(f"  wrote {OUT_SVG}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
