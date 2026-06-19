#!/usr/bin/env python3
"""BT1301 - Full chart-atlas ISA compiler.

BT1300 gave the 72-lane oscillator instruction frame.  BT1301 checks that the
8-tick word is not only a sample-program format: it can cover the full
540-chart atlas.

For each chart c in {0,...,539}, there are five canonical all-XOR ingress
digits 7,15,23,31,39.  They have identical ternary XOR mask 111, and their
depth choices give apartment-hop costs 1,2,3,4,5 in some order.  Choosing one
candidate per chart with a rotating schedule gives:

    540 chart routes,
    all three XOR axes active on every route,
    apartment-hop costs 1..5 exactly 108 times each,
    active ticks 4..8 exactly 108 times each.

So the complete atlas compiles into the BT1300 word, and the word really uses
the whole tick budget rather than hiding in shortest no-op routes.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from bt828_holonet_packet_compiler import chart_id, compile_digit
from bt1300_oscillator_instruction_isa import micro_op_for_tick

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1301_full_chart_atlas_isa_compiler.json"

CHART_COUNT = 540
ROUTE_TICKS = 8
ALL_XOR_DIGITS = (7, 15, 23, 31, 39)


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def tick_rows_from_digit(row: dict[str, Any]) -> list[dict[str, Any]]:
    ticks = []
    for tick in range(ROUTE_TICKS):
        if tick < 3:
            active = tick in row["xor_axes"]
            reason = "xor_axis_present" if active else "xor_axis_idle"
        else:
            active = (tick - 3) < row["apartment_hops"]
            reason = "apartment_hop_budget" if active else "apartment_hop_idle"
        ticks.append(
            {
                "tick": tick,
                "micro_op": micro_op_for_tick(tick),
                "active": active,
                "reason": reason,
            }
        )
    return ticks


def slim_route(row: dict[str, Any]) -> dict[str, Any]:
    active_ticks = [
        tick["tick"] for tick in tick_rows_from_digit(row) if tick["active"]
    ]
    return {
        "source_digit": row["source_digit"],
        "target_digit": row["target_digit"],
        "depth": row["depth"],
        "source_chart": row["source_chart"],
        "target_chart": row["target_chart"],
        "xor_axes": row["xor_axes"],
        "xor_hops": row["xor_hops"],
        "apartment_hops": row["apartment_hops"],
        "active_ticks": active_ticks,
        "active_tick_count": row["reversible_moves"],
        "idle_tick_count": ROUTE_TICKS - row["reversible_moves"],
        "mirror_slot": row["mirror_slot"],
        "tomotope_block": row["tomotope_block"],
        "clock_phase_c12": row["clock_phase_c12"],
    }


def candidate_palette_for_chart(chart: int) -> list[dict[str, Any]]:
    candidates = []
    for target_digit in ALL_XOR_DIGITS:
        for depth in range(CHART_COUNT):
            if chart_id(target_digit, depth) == chart:
                row = compile_digit(0, target_digit, depth)
                candidates.append(row)
                break
        else:  # pragma: no cover - guarded by verifier checks
            raise AssertionError(
                f"missing atlas ingress for chart {chart}, digit {target_digit}"
            )
    candidates.sort(key=lambda row: row["target_digit"])
    return candidates


def chosen_route_for_chart(chart: int) -> dict[str, Any]:
    palette = candidate_palette_for_chart(chart)
    return palette[chart % len(palette)]


def build_payload() -> dict[str, Any]:
    bt827 = load_json("data/bt827_holonet_fractal_architecture.json")
    bt828 = load_json("data/bt828_holonet_packet_compiler.json")
    bt1300 = load_json("data/bt1300_oscillator_instruction_isa.json")

    palette_rows = []
    chosen_routes = []
    palette_hop_profiles = []
    for chart in range(CHART_COUNT):
        palette = candidate_palette_for_chart(chart)
        palette_hop_profiles.append(sorted(row["apartment_hops"] for row in palette))
        palette_rows.append(
            {
                "chart": chart,
                "candidate_count": len(palette),
                "target_digits": [row["target_digit"] for row in palette],
                "apartment_hops": [row["apartment_hops"] for row in palette],
                "depths": [row["depth"] for row in palette],
            }
        )
        chosen = chosen_route_for_chart(chart)
        chosen_routes.append({"chart": chart, **slim_route(chosen)})

    move_hist = Counter(route["active_tick_count"] for route in chosen_routes)
    hop_hist = Counter(route["apartment_hops"] for route in chosen_routes)
    target_digit_hist = Counter(route["target_digit"] for route in chosen_routes)
    checks = {
        "bt827_chart_count_loaded": bt827["single_core"]["charts"] == CHART_COUNT,
        "bt828_compiler_verified": all(bt828["checks"].values()),
        "bt1300_isa_verified": bt1300["verified"] is True,
        "all_540_charts_covered_once": len(chosen_routes) == CHART_COUNT
        and sorted(route["target_chart"] for route in chosen_routes)
        == list(range(CHART_COUNT)),
        "each_chart_has_five_all_xor_candidates": all(
            row["candidate_count"] == 5 for row in palette_rows
        ),
        "each_palette_has_hop_profile_1_to_5": all(
            profile == [1, 2, 3, 4, 5] for profile in palette_hop_profiles
        ),
        "all_routes_activate_three_xor_axes": all(
            route["xor_axes"] == [0, 1, 2] for route in chosen_routes
        ),
        "balanced_target_digits": sorted(target_digit_hist.values()) == [108] * 5,
        "balanced_apartment_hops": dict(sorted(hop_hist.items()))
        == {1: 108, 2: 108, 3: 108, 4: 108, 5: 108},
        "balanced_active_tick_counts": dict(sorted(move_hist.items()))
        == {4: 108, 5: 108, 6: 108, 7: 108, 8: 108},
        "all_routes_fit_one_bt1300_word": all(
            0 < route["active_tick_count"] <= ROUTE_TICKS for route in chosen_routes
        ),
        "all_routes_are_nontrivial_chart_moves": all(
            route["source_chart"] != route["target_chart"] for route in chosen_routes
        ),
        "all_headers_live_in_runtime_spaces": all(
            0 <= route["mirror_slot"] < 2160
            and 0 <= route["tomotope_block"] < 48
            and 0 <= route["clock_phase_c12"] < 12
            for route in chosen_routes
        ),
    }

    payload = {
        "theorem": "BT1301 full chart-atlas ISA compiler",
        "verified": all(checks.values()),
        "checks": checks,
        "contract": {
            "chart_routes": CHART_COUNT,
            "ticks_per_word": ROUTE_TICKS,
            "candidate_digits": list(ALL_XOR_DIGITS),
            "candidate_digit_meaning": "all have low three-bit mask 111, so every route activates all q=3 XOR axes",
            "schedule_rule": "choose candidate index chart mod 5",
            "active_tick_histogram": dict(sorted(move_hist.items())),
            "apartment_hop_histogram": dict(sorted(hop_hist.items())),
            "target_digit_histogram": dict(sorted(target_digit_hist.items())),
        },
        "palette_summary": palette_rows,
        "atlas_routes": chosen_routes,
        "architecture_reading": (
            "The 540-chart fabric compiles into BT1300's 8-tick route word. "
            "Each chart has a five-candidate all-XOR palette with apartment-hop "
            "costs 1..5. The rotating schedule balances active tick counts 4..8 "
            "exactly 108 times each, so the ISA covers the full atlas while "
            "exercising the whole micro-op budget."
        ),
        "honesty_boundary": (
            "BT1301 is a deterministic atlas ingress table. It proves bounded "
            "ISA coverage and balanced tick use, not a globally shortest path "
            "solver for arbitrary chart-to-chart traffic."
        ),
    }
    return payload


def main() -> None:
    payload = build_payload()
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "theorem": payload["theorem"],
                "verified": payload["verified"],
                "checks_passed": sum(payload["checks"].values()),
                "checks_total": len(payload["checks"]),
                "out": str(OUT.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not payload["verified"]:
        failed = [name for name, passed in payload["checks"].items() if not passed]
        raise SystemExit(f"BT1301 failed checks: {failed}")


if __name__ == "__main__":
    main()
