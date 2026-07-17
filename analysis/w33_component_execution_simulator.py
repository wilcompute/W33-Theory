#!/usr/bin/env python3
"""Executable W(3,3) component simulator.

The architecture map says:

    address -> route -> K4 line bus -> spread clock -> durable commit.

This script makes that sequence literal.  It builds the W(3,3) points, lines,
spreads, and spread-clock graph from the existing runtime primitives, routes a
direct packet and a two-hop packet, assigns every hop to its unique line bus,
embeds those buses into spread-clock frames, inserts connector frames when the
spread graph requires them, and emits an auditable JSON/Markdown trace.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_spread_clock_graph import (
    adjacency_from_overlap,
    build_overlap_matrix,
    shortest_path,
)
from w33_uor_runtime_model import ROOT, all_lines, find_spreads, point_id


DEFAULT_JSON = ROOT / "data" / "w33_component_execution_simulator.json"
DEFAULT_MD = ROOT / "docs" / "w33_component_execution_simulator.md"


def commit_ticks(level: int) -> int:
    return 4 * (7**level - 1)


def line_lookup(lines: list[tuple[int, ...]]) -> dict[tuple[int, int], int]:
    lookup: dict[tuple[int, int], int] = {}
    for line_id, line in enumerate(lines):
        for left_pos, left in enumerate(line):
            for right in line[left_pos + 1 :]:
                lookup[(left, right)] = line_id
                lookup[(right, left)] = line_id
    return lookup


def choose_spreads_for_lines(
    line_ids: list[int], spreads: list[list[int]], graph: dict[int, set[int]]
) -> tuple[list[int], list[dict[str, Any]]]:
    carriers: list[int] = []
    choices: list[dict[str, Any]] = []
    for line_id in line_ids:
        candidate_spreads = [
            spread_id for spread_id, spread in enumerate(spreads) if line_id in spread
        ]
        if not candidate_spreads:
            raise AssertionError(f"line {line_id} is in no spread")
        if not carriers:
            spread_id = candidate_spreads[0]
            clock_distance = 0
            connector_path = [spread_id]
        else:
            ranked = []
            for candidate in candidate_spreads:
                path = shortest_path(graph, carriers[-1], candidate)
                ranked.append((len(path) - 1, candidate, path))
            clock_distance, spread_id, connector_path = min(ranked)
        carriers.append(spread_id)
        choices.append(
            {
                "line_id": line_id,
                "candidate_spreads": candidate_spreads,
                "chosen_spread": spread_id,
                "clock_distance_from_previous": clock_distance,
                "clock_path_from_previous": connector_path,
            }
        )
    return carriers, choices


def clock_walk_for_carriers(carriers: list[int], graph: dict[int, set[int]]) -> list[dict[str, Any]]:
    if not carriers:
        return []
    slots = [{"kind": "active", "hop_index": 0, "spread": carriers[0]}]
    for hop_index, (left, right) in enumerate(zip(carriers, carriers[1:]), start=1):
        path = shortest_path(graph, left, right)
        for connector in path[1:-1]:
            slots.append(
                {
                    "kind": "connector",
                    "between_hops": [hop_index - 1, hop_index],
                    "spread": connector,
                }
            )
        slots.append({"kind": "active", "hop_index": hop_index, "spread": right})
    return slots


def packet_trace(
    label: str,
    src_idx: int,
    dst_idx: int,
    lines: list[tuple[int, ...]],
    lookup: dict[tuple[int, int], int],
    spreads: list[list[int]],
    graph: dict[int, set[int]],
) -> dict[str, Any]:
    src = hn.POINTS[src_idx]
    dst = hn.POINTS[dst_idx]
    route_points = hn.route(src, dst)
    route_indices = [hn.POINTS.index(point) for point in route_points]
    line_ids = []
    hop_rows = []
    for hop_index, (left, right) in enumerate(
        zip(route_indices, route_indices[1:])
    ):
        if hn.symplectic(hn.POINTS[left], hn.POINTS[right]) != 0:
            raise AssertionError("route hop is not an isotropic edge")
        line_id = lookup[(left, right)]
        line_ids.append(line_id)
        hop_rows.append(
            {
                "hop_index": hop_index,
                "from": point_id(hn.POINTS[left]),
                "to": point_id(hn.POINTS[right]),
                "line_bus": line_id,
                "line_bus_points": [point_id(hn.POINTS[p]) for p in lines[line_id]],
            }
        )

    carrier_spreads, spread_choices = choose_spreads_for_lines(line_ids, spreads, graph)
    clock_walk = clock_walk_for_carriers(carrier_spreads, graph)
    for row, choice in zip(hop_rows, spread_choices):
        row["spread_clock_frame"] = choice["chosen_spread"]
        row["spread_contains_line"] = choice["line_id"] in spreads[choice["chosen_spread"]]
        row["candidate_spread_frames"] = choice["candidate_spreads"]

    level = max(1, len(route_indices) - 1)
    commit = {
        "level": level,
        "formula": "4*(7^level - 1)",
        "durable_commit_ticks": commit_ticks(level),
        "route_tick_budget": 8 * level,
        "microframe_ticks": 72,
        "body_ticks": 48,
        "guard_ticks": 24,
        "commit_after_route_budget": commit_ticks(level) >= 8 * level,
        "frame_locked": commit_ticks(level) % 72 == 0,
    }

    return {
        "label": label,
        "source": point_id(src),
        "destination": point_id(dst),
        "symplectic": int(hn.symplectic(src, dst)),
        "route_points": [point_id(point) for point in route_points],
        "hops": len(route_points) - 1,
        "hop_rows": hop_rows,
        "spread_choices": spread_choices,
        "clock_walk": clock_walk,
        "commit": commit,
    }


def build_payload() -> dict[str, Any]:
    lines = all_lines()
    spreads = find_spreads(lines, limit=10000)
    lookup = line_lookup(lines)
    graph = adjacency_from_overlap(build_overlap_matrix(spreads))

    src_idx = 0
    src = hn.POINTS[src_idx]
    direct_idx = hn.POINTS.index(hn.neighbors(src)[0])
    two_hop_idx = next(
        idx
        for idx, point in enumerate(hn.POINTS)
        if point != src and hn.symplectic(src, point) != 0
    )

    packets = [
        packet_trace("direct_one_hop", src_idx, direct_idx, lines, lookup, spreads, graph),
        packet_trace("nonlocal_two_hop", src_idx, two_hop_idx, lines, lookup, spreads, graph),
    ]

    hop_hist = Counter(packet["hops"] for packet in packets)
    checks = {
        "forty_lines": len(lines) == 40,
        "thirty_six_spreads": len(spreads) == 36,
        "direct_packet_is_one_hop": packets[0]["hops"] == 1,
        "nonlocal_packet_is_two_hop": packets[1]["hops"] == 2,
        "all_hops_have_line_buses": all(
            "line_bus" in hop for packet in packets for hop in packet["hop_rows"]
        ),
        "all_spreads_contain_assigned_line": all(
            hop["spread_contains_line"] for packet in packets for hop in packet["hop_rows"]
        ),
        "all_clock_walks_have_active_slot_per_hop": all(
            sum(1 for slot in packet["clock_walk"] if slot["kind"] == "active")
            == packet["hops"]
            for packet in packets
        ),
        "all_commit_ticks_cover_route_budget": all(
            packet["commit"]["commit_after_route_budget"] for packet in packets
        ),
    }

    payload = {
        "schema": "w33.component_execution_simulator.v1",
        "theorem": "W(3,3) component execution simulator",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "component_pipeline": [
            "projective address",
            "symplectic route",
            "unique K4 line bus per hop",
            "spread clock frame per bus",
            "spread-clock connector walk",
            "durable commit marker",
        ],
        "instance_counts": {
            "points": len(hn.POINTS),
            "lines": len(lines),
            "spreads": len(spreads),
            "spread_clock_vertices": len(graph),
            "spread_clock_degree_histogram": {
                str(key): value for key, value in sorted(Counter(len(v) for v in graph.values()).items())
            },
        },
        "packet_hop_histogram": {str(key): value for key, value in sorted(hop_hist.items())},
        "packets": packets,
        "checks": checks,
        "interpretation": (
            "The same finite object supplies address decoding, packet routing, "
            "bus selection, clock-frame scheduling, and commit timing. A host "
            "can emulate this trace today; a qutrit fabric would implement the "
            "same typed steps directly."
        ),
        "honesty_boundary": (
            "This simulates the finite control plane and commit markers. It does "
            "not simulate calibrated optical loss, detector electronics, or "
            "physical non-Clifford acceleration."
        ),
    }
    return payload


def markdown(payload: dict[str, Any]) -> str:
    packet_sections = []
    for packet in payload["packets"]:
        rows = []
        for hop in packet["hop_rows"]:
            rows.append(
                "| {hop_index} | `{from}` | `{to}` | {line_bus} | {spread_clock_frame} |".format(
                    **hop
                )
            )
        clock = ", ".join(
            f"{slot['kind']}:{slot['spread']}" for slot in packet["clock_walk"]
        )
        packet_sections.append(
            f"""### {packet['label']}

- Source: `{packet['source']}`
- Destination: `{packet['destination']}`
- Route: {' -> '.join(f"`{p}`" for p in packet['route_points'])}
- Clock walk: `{clock}`
- Commit: `{packet['commit']['durable_commit_ticks']}` ticks, route budget `{packet['commit']['route_tick_budget']}` ticks

| Hop | From | To | K4 line bus | Spread frame |
|---:|---|---|---:|---:|
{chr(10).join(rows)}
"""
        )
    return f"""# W(3,3) Component Execution Simulator

This is the executable trace behind the component dictionary.  A packet passes
through:

`address -> route -> K4 line bus -> spread clock -> durable commit`.

{chr(10).join(packet_sections)}

## Boundary

This is a finite control-plane simulator.  It proves that the architecture can
name a site, route a packet, select a bus, place the operation on the spread
clock, and attach a commit marker using only W(3,3) incidence.  It does not
claim a calibrated photonic hardware implementation.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload()
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")

    print(f"status: {payload['status']}")
    for packet in payload["packets"]:
        print(
            f"{packet['label']}: {packet['hops']} hops, "
            f"{len(packet['clock_walk'])} clock slots, "
            f"commit={packet['commit']['durable_commit_ticks']}"
        )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
