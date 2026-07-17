#!/usr/bin/env python3
"""Schedule Holonet packets across all W(3,3) spread epochs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from w33_uor_runtime_model import ROOT, all_lines, find_spreads, point_id

DEFAULT_INPUTS = [
    ROOT / "data" / "holonet_wrap_demo_factorial.json",
    ROOT / "data" / "holonet_wrap_rule110_demo.json",
]
DEFAULT_OUTPUT = ROOT / "data" / "w33_uor_spread_scheduler.json"


def packet_sites(packet: dict[str, Any]) -> set[str]:
    return set(packet["path"])


def spread_sites(lines: list[tuple[int, ...]], spread: list[int]) -> set[str]:
    from holonet_node import POINTS

    sites = set()
    for line_idx in spread:
        for point_idx in lines[line_idx]:
            sites.add(point_id(POINTS[point_idx]))
    return sites


def packet_fits_epoch(
    packet: dict[str, Any], lines: list[tuple[int, ...]], spread: list[int]
) -> bool:
    return packet_sites(packet).issubset(spread_sites(lines, spread))


def schedule_packets(reports: list[dict[str, Any]]) -> dict[str, Any]:
    lines = all_lines()
    spreads = find_spreads(lines, limit=10000)
    packets = []
    for report_index, report in enumerate(reports):
        for packet in report.get("packets", []):
            packets.append(
                {
                    "report_index": report_index,
                    "packet_id": f"{packet['label']}:{packet['index']}",
                    "sites": sorted(packet_sites(packet)),
                    "hops": packet["hops"],
                    "symplectic": packet["symplectic"],
                }
            )

    epoch_assignments = []
    used_sites_by_epoch: dict[int, set[str]] = {
        idx: set() for idx in range(len(spreads))
    }
    for packet in packets:
        candidates = [
            spread_index
            for spread_index, spread in enumerate(spreads)
            if packet_fits_epoch({"path": packet["sites"]}, lines, spread)
        ]
        assigned_epoch = None
        for spread_index in candidates:
            if used_sites_by_epoch[spread_index].isdisjoint(packet["sites"]):
                assigned_epoch = spread_index
                used_sites_by_epoch[spread_index].update(packet["sites"])
                break
        epoch_assignments.append(
            {
                **packet,
                "candidate_epoch_count": len(candidates),
                "assigned_epoch": assigned_epoch,
            }
        )

    epoch_loads: dict[int, int] = {}
    for row in epoch_assignments:
        if row["assigned_epoch"] is not None:
            epoch_loads[row["assigned_epoch"]] = (
                epoch_loads.get(row["assigned_epoch"], 0) + 1
            )

    all_routable = all(row["assigned_epoch"] is not None for row in epoch_assignments)
    conflict_free = True
    for spread_index in epoch_loads:
        seen: set[str] = set()
        for row in epoch_assignments:
            if row["assigned_epoch"] != spread_index:
                continue
            sites = set(row["sites"])
            if seen & sites:
                conflict_free = False
            seen.update(sites)
    return {
        "schema": "w33.uor.spread_scheduler.v1",
        "status": "PASS" if all_routable and conflict_free and spreads else "FAIL",
        "spread_count": len(spreads),
        "packet_count": len(packets),
        "all_packets_fit_at_least_one_spread_epoch": all_routable,
        "conflict_free_assignment": conflict_free,
        "min_candidate_epoch_count": min(
            (row["candidate_epoch_count"] for row in epoch_assignments), default=0
        ),
        "max_candidate_epoch_count": max(
            (row["candidate_epoch_count"] for row in epoch_assignments), default=0
        ),
        "epoch_loads": dict(sorted(epoch_loads.items())),
        "epoch_used_site_counts": {
            str(epoch): len(sites)
            for epoch, sites in sorted(used_sites_by_epoch.items())
            if sites
        },
        "assignments": epoch_assignments,
        "interpretation": (
            "A spread epoch is a full-site UOR parallel trace: ten disjoint "
            "W(3,3) line synchronization contexts covering all 40 sites. A "
            "packet fits an epoch when every site on its route lies inside that "
            "epoch's site cover."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", default=str(DEFAULT_OUTPUT), help="scheduler output JSON"
    )
    parser.add_argument("inputs", nargs="*", help="Holonet wrapper reports")
    args = parser.parse_args(argv)

    input_paths = [Path(p) for p in args.inputs] if args.inputs else DEFAULT_INPUTS
    reports = []
    for path in input_paths:
        if not path.is_absolute():
            path = ROOT / path
        reports.append(json.loads(path.read_text(encoding="utf-8")))

    result = schedule_packets(reports)
    output = Path(args.out)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"status: {result['status']}")
    print(f"spreads: {result['spread_count']}")
    print(f"packets: {result['packet_count']}")
    print(
        f"candidate epochs: {result['min_candidate_epoch_count']}..{result['max_candidate_epoch_count']}"
    )
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
