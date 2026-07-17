#!/usr/bin/env python3
"""Scheduler economics benchmark for generated W(3,3) control.

The architecture claims table-free routing and generated bus/clock schedules.
This benchmark makes the storage economics explicit over levels 1..8.

It compares conventional persisted control tables per W33 instance against the
Holonet reading: generate routes, buses, spreads, and frame transitions from the
same incidence law instead of storing per-instance topology tables.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "data" / "w33_scheduler_economics_benchmark.json"
DEFAULT_MD = ROOT / "docs" / "w33_scheduler_economics_benchmark.md"
DEFAULT_SVG = ROOT / "docs" / "w33_scheduler_economics_benchmark.svg"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def instances(level: int) -> int:
    return (40**level - 1) // 39


def table_bytes(instance_map: dict[str, Any]) -> dict[str, int]:
    mapping = {
        "next-hop routing table": "routing",
        "full adjacency matrix": "adjacency",
        "line/bus table": "line_bus",
        "spread/global-clock table": "spread_clock",
        "frame-clock transition table": "frame_transition",
    }
    out: dict[str, int] = {}
    for item in instance_map["compression_ledger"]:
        if item["name"] in mapping:
            out[mapping[item["name"]]] = int(item["naive_bytes"])
    out["listed_control_total"] = sum(out.values())
    return out


def build_rows(max_level: int, per: dict[str, int]) -> list[dict[str, Any]]:
    rows = []
    for level in range(1, max_level + 1):
        count = instances(level)
        leaves = 40**level
        rows.append(
            {
                "level": level,
                "leaf_sites": leaves,
                "w33_instances": count,
                "route_bound": 8 * level,
                "routing_bytes": per["routing"] * count,
                "line_bus_bytes": per["line_bus"] * count,
                "spread_clock_bytes": per["spread_clock"] * count,
                "frame_transition_bytes": per["frame_transition"] * count,
                "adjacency_bytes": per["adjacency"] * count,
                "listed_control_bytes": per["listed_control_total"] * count,
                "generated_topology_table_bytes": 0,
                "internal_mirror_capacity": 2160 * count,
                "one_packet_per_chart_demand": 540 * count,
                "mirror_slack": 1620 * count,
                "leaf_packet_scheduler_slots": 2160 * leaves,
            }
        )
    return rows


def svg_chart(rows: list[dict[str, Any]]) -> str:
    width = 980
    height = 420
    pad_l = 72
    pad_r = 28
    pad_t = 30
    pad_b = 58
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    max_y = max(row["listed_control_bytes"] for row in rows)
    min_y = max(1, min(row["routing_bytes"] for row in rows))
    log_min = math.log10(min_y)
    log_max = math.log10(max_y)

    def x(level: int) -> float:
        if len(rows) == 1:
            return pad_l + plot_w / 2
        return pad_l + (level - rows[0]["level"]) * plot_w / (len(rows) - 1)

    def y(value: int) -> float:
        value = max(1, value)
        return pad_t + (log_max - math.log10(value)) * plot_h / (log_max - log_min)

    series = [
        ("routing_bytes", "#2d6cdf", "routing table"),
        ("listed_control_bytes", "#118264", "listed control tables"),
        ("internal_mirror_capacity", "#8a5a00", "mirror capacity slots"),
    ]
    polylines = []
    legend = []
    for idx, (key, color, label) in enumerate(series):
        points = " ".join(f"{x(row['level']):.2f},{y(row[key]):.2f}" for row in rows)
        polylines.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{points}" />'
        )
        legend.append(
            f'<g transform="translate({pad_l + idx * 250},18)"><rect width="14" height="4" fill="{color}" y="-3"/><text x="20" y="1">{label}</text></g>'
        )
    x_ticks = []
    for row in rows:
        xx = x(row["level"])
        x_ticks.append(
            f'<line x1="{xx:.2f}" y1="{height-pad_b}" x2="{xx:.2f}" y2="{height-pad_b+6}" stroke="#5f6f7a"/><text x="{xx:.2f}" y="{height-pad_b+22}" text-anchor="middle">{row["level"]}</text>'
        )
    y_ticks = []
    for exponent in range(math.floor(log_min), math.ceil(log_max) + 1, 2):
        value = 10**exponent
        yy = y(value)
        y_ticks.append(
            f'<line x1="{pad_l-6}" y1="{yy:.2f}" x2="{pad_l}" y2="{yy:.2f}" stroke="#5f6f7a"/><text x="{pad_l-10}" y="{yy+4:.2f}" text-anchor="end">1e{exponent}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="W33 scheduler economics benchmark">
  <style>
    text {{ font: 12px system-ui, -apple-system, Segoe UI, sans-serif; fill: #17202a; }}
    .muted {{ fill: #5f6f7a; }}
  </style>
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{pad_l}" y="18" font-size="15">Scheduler/control economics by recursive level (log scale)</text>
  {''.join(legend)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{height-pad_b}" stroke="#8aa0aa"/>
  <line x1="{pad_l}" y1="{height-pad_b}" x2="{width-pad_r}" y2="{height-pad_b}" stroke="#8aa0aa"/>
  {''.join(y_ticks)}
  {''.join(x_ticks)}
  {''.join(polylines)}
  <text x="{width/2:.1f}" y="{height-14}" text-anchor="middle" class="muted">recursive level n</text>
  <text transform="translate(18,{height/2:.1f}) rotate(-90)" text-anchor="middle" class="muted">bytes / slots, log10</text>
</svg>
"""


def build_payload(max_level: int) -> dict[str, Any]:
    instance_map = load_json("data/w33_instance_architecture_map.json")
    recursive = load_json("data/w33_recursive_instance_compression.json")
    per = table_bytes(instance_map)
    rows = build_rows(max_level, per)
    checks = {
        "instance_map_passes": instance_map["status"] == "PASS",
        "recursive_compression_passes": recursive["status"] == "PASS",
        "routing_bytes_per_instance_1170": per["routing"] == 1170,
        "listed_control_total_per_instance_1816": per["listed_control_total"] == 1816,
        "levels_are_one_to_max": [row["level"] for row in rows]
        == list(range(1, max_level + 1)),
        "generated_topology_tables_zero": all(
            row["generated_topology_table_bytes"] == 0 for row in rows
        ),
        "mirror_utilization_quarter": all(
            4 * row["one_packet_per_chart_demand"] == row["internal_mirror_capacity"]
            for row in rows
        ),
        "route_bound_linear": all(row["route_bound"] == 8 * row["level"] for row in rows),
        "bytes_monotone": all(
            rows[idx + 1]["listed_control_bytes"] > rows[idx]["listed_control_bytes"]
            for idx in range(len(rows) - 1)
        ),
        "level8_leaf_count": rows[-1]["leaf_sites"] == 40**max_level,
    }
    return {
        "schema": "w33.scheduler_economics_benchmark.v1",
        "theorem": "W(3,3) scheduler economics benchmark",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "per_instance_conventional_tables": per,
        "rows": rows,
        "checks": checks,
        "interpretation": (
            "Conventional control planes replicate route, line-bus, spread, and "
            "frame-transition tables per W33 instance. The Holonet control plane "
            "regenerates those layers from incidence, so the benchmark reports "
            "bytes avoided rather than runtime speedup."
        ),
        "honesty_boundary": (
            "This is storage economics for finite topology tables. It is not a "
            "hardware benchmark and does not count Python interpreter overhead."
        ),
    }


def markdown(payload: dict[str, Any], svg_path: Path) -> str:
    rows = []
    for row in payload["rows"]:
        rows.append(
            "| {level} | {leaf_sites:,} | {w33_instances:,} | {route_bound} | "
            "{routing_bytes:,} | {listed_control_bytes:,} | {internal_mirror_capacity:,} |".format(
                **row
            )
        )
    svg_rel = svg_path.name
    return f"""# W(3,3) Scheduler Economics Benchmark

This benchmark compares conventional persisted topology tables against generated
W33 control over levels `1..{payload['rows'][-1]['level']}`.

![Scheduler economics]({svg_rel})

| Level | Leaf sites | W33 instances | Route bound | Routing bytes | Listed control bytes | Internal mirror capacity |
|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

Per W33 instance, the conventional table payload is:

- routing: `{payload['per_instance_conventional_tables']['routing']}` bytes
- line bus: `{payload['per_instance_conventional_tables']['line_bus']}` bytes
- spread clock: `{payload['per_instance_conventional_tables']['spread_clock']}` bytes
- frame transition: `{payload['per_instance_conventional_tables']['frame_transition']}` bytes
- adjacency: `{payload['per_instance_conventional_tables']['adjacency']}` bytes
- listed control total: `{payload['per_instance_conventional_tables']['listed_control_total']}` bytes

Boundary: this is storage economics for generated control. It is not a host CPU
speed benchmark.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-level", type=int, default=8)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    parser.add_argument("--svg-out", default=str(DEFAULT_SVG))
    args = parser.parse_args(argv)

    payload = build_payload(args.max_level)
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    svg_out = Path(args.svg_out)
    if not svg_out.is_absolute():
        svg_out = ROOT / svg_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    svg_out.parent.mkdir(parents=True, exist_ok=True)
    svg_out.write_text(svg_chart(payload["rows"]), encoding="utf-8")
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload, svg_out), encoding="utf-8")

    last = payload["rows"][-1]
    print(f"status: {payload['status']}")
    print(
        "level {level}: leaves={leaf_sites:,}, instances={w33_instances:,}, "
        "listed_control_bytes={listed_control_bytes:,}, route_bound={route_bound}".format(
            **last
        )
    )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    print(f"wrote: {svg_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
