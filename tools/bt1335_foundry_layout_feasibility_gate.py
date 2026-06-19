#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def evaluate(pitch_um: float, bend_radius_um: float, chart_side_um: float, die_side_mm: float) -> dict:
    charts = 540
    modes_per_chart = 8
    base_channels = charts * modes_per_chart
    die_area_um2 = (die_side_mm * 1000.0) ** 2
    chart_area_um2 = chart_side_um ** 2
    total_chart_area_um2 = charts * chart_area_um2
    channel_area_budget_um2 = die_area_um2 / base_channels
    min_bus_width_um = base_channels * pitch_um
    chart_linear_width_um = modes_per_chart * pitch_um
    return {
        "charts": charts,
        "modes_per_chart": modes_per_chart,
        "base_channels": base_channels,
        "die_side_mm": die_side_mm,
        "die_area_um2": die_area_um2,
        "pitch_um": pitch_um,
        "bend_radius_um": bend_radius_um,
        "chart_side_um": chart_side_um,
        "chart_area_um2": chart_area_um2,
        "total_chart_area_um2": total_chart_area_um2,
        "area_fill_fraction": total_chart_area_um2 / die_area_um2,
        "area_fits": total_chart_area_um2 <= die_area_um2,
        "channel_area_budget_um2": channel_area_budget_um2,
        "min_parallel_bus_width_um": min_bus_width_um,
        "chart_linear_width_um": chart_linear_width_um,
        "chart_can_hold_modes_linearly": chart_linear_width_um <= chart_side_um,
        "chart_can_hold_two_bends": 2 * bend_radius_um <= chart_side_um,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1335_foundry_layout_feasibility_gate.json")
    ns = ap.parse_args()
    conservative = evaluate(pitch_um=10.0, bend_radius_um=50.0, chart_side_um=200.0, die_side_mm=5.0)
    aggressive = evaluate(pitch_um=5.0, bend_radius_um=20.0, chart_side_um=120.0, die_side_mm=5.0)
    checks = {
        "base_channel_count_4320": conservative["base_channels"] == 4320,
        "conservative_area_fits": conservative["area_fits"],
        "conservative_fill_below_one": conservative["area_fill_fraction"] < 1.0,
        "conservative_chart_holds_modes": conservative["chart_can_hold_modes_linearly"],
        "conservative_chart_holds_bends": conservative["chart_can_hold_two_bends"],
        "aggressive_area_fits": aggressive["area_fits"],
    }
    result = {
        "bt": 1335,
        "title": "Foundry layout feasibility gate",
        "verified": all(checks.values()),
        "interpretation": "The 4320 base-channel claim is area-plausible on a 5mm by 5mm die under explicit chart-cell assumptions, but the 70.8M concatenated-mode claim is not a single-die layout claim and requires hierarchy/time/fiber/memory multiplexing.",
        "checks": checks,
        "scenarios": {
            "conservative_cell": conservative,
            "aggressive_cell": aggressive
        },
        "engineering_caveats": [
            "does not model waveguide crossings",
            "does not model thermal phase shifter footprint",
            "does not model grating or edge coupler fanout",
            "does not model loss or crosstalk accumulation",
            "does not place the 70.8M concatenated modes on one die"
        ]
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1335, "verified": result["verified"], "base_channels": conservative["base_channels"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
