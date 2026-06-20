#!/usr/bin/env python3
"""BT1405: lift Q6 packet-edge addresses to continuous Q6 walks.

BT1374 lowered every packet digit to a Q6/tomotope edge address, but kept an
honest boundary: those addresses were waypoints, not a continuous route.  BT1405
adds the missing path layer.  For each compiled BT828 program, orient the listed
Q6 packet edges and insert shortest Q6 connector walks between consecutive
packet edges.  Every traversed edge is then mapped back through the BT1371
tomotope flag table.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1405_continuous_q6_path_router.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))


def q6_neighbors(vertex: str) -> list[str]:
    out = []
    for bit in range(6):
        chars = list(vertex)
        chars[bit] = "1" if chars[bit] == "0" else "0"
        out.append("".join(chars))
    return out


def q6_shortest_path(source: str, target: str) -> list[str]:
    if source == target:
        return [source]
    parent: dict[str, str | None] = {source: None}
    queue: deque[str] = deque([source])
    while queue:
        vertex = queue.popleft()
        for neighbor in q6_neighbors(vertex):
            if neighbor in parent:
                continue
            parent[neighbor] = vertex
            if neighbor == target:
                queue.clear()
                break
            queue.append(neighbor)
    path = [target]
    while path[-1] != source:
        path.append(parent[path[-1]])  # type: ignore[arg-type]
    return list(reversed(path))


def edge_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))  # type: ignore[return-value]


def edge_direction(a: str, b: str) -> int:
    changed = [idx for idx, (x, y) in enumerate(zip(a, b)) if x != y]
    if len(changed) != 1:
        raise ValueError(f"not a Q6 edge: {a} -> {b}")
    return changed[0]


def choose_packet_edge_orientation(
    packet_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int, int]:
    """Exhaustively orient packet edges to minimize connector length.

    Programs in the current compiler have at most six packet edges, so the
    2^n search is exact and cheaper than introducing another dependency.
    """

    best: tuple[int, int, int, list[dict[str, Any]]] | None = None
    for mask in range(1 << len(packet_rows)):
        oriented = []
        for idx, row in enumerate(packet_rows):
            a = row["q6_endpoint_a"]
            b = row["q6_endpoint_b"]
            if (mask >> idx) & 1:
                a, b = b, a
            oriented.append({**row, "walk_start": a, "walk_end": b})
        connector_steps = sum(
            hamming(oriented[idx]["walk_end"], oriented[idx + 1]["walk_start"])
            for idx in range(len(oriented) - 1)
        )
        total_steps = len(oriented) + connector_steps
        candidate = (total_steps, connector_steps, mask, oriented)
        if best is None or candidate[:3] < best[:3]:
            best = candidate
    assert best is not None
    return best[3], best[0], best[1]


def build_edge_index(
    address_table: list[dict[str, Any]],
) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        edge_key(row["q6_endpoint_a"], row["q6_endpoint_b"]): row
        for row in address_table
    }


def make_step(
    *,
    tick: int,
    source: str,
    target: str,
    edge_table: dict[tuple[str, str], dict[str, Any]],
    kind: str,
    packet_depth: int | None,
) -> dict[str, Any]:
    address = edge_table[edge_key(source, target)]
    tomotope_flag = int(address["tomotope_flag"])
    return {
        "body_tick": tick,
        "kind": kind,
        "packet_depth": packet_depth,
        "source": source,
        "target": target,
        "q6_edge_index": int(address["q6_edge_index"]),
        "q6_direction": int(address["q6_direction"]),
        "walk_bit_axis": edge_direction(source, target),
        "tomotope_flag": tomotope_flag,
        "tomotope_block": tomotope_flag // 4,
        "transversal_index": tomotope_flag % 4,
    }


def continuous_route_for_program(
    program: dict[str, Any],
    edge_table: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    packet_rows = list(program["packet_rows"])
    oriented, total_steps, connector_steps = choose_packet_edge_orientation(packet_rows)
    steps: list[dict[str, Any]] = []

    for idx, row in enumerate(oriented):
        steps.append(
            make_step(
                tick=len(steps),
                source=row["walk_start"],
                target=row["walk_end"],
                edge_table=edge_table,
                kind="packet",
                packet_depth=int(row["depth"]),
            )
        )
        if idx + 1 == len(oriented):
            continue
        connector_path = q6_shortest_path(
            row["walk_end"], oriented[idx + 1]["walk_start"]
        )
        for source, target in zip(connector_path, connector_path[1:]):
            steps.append(
                make_step(
                    tick=len(steps),
                    source=source,
                    target=target,
                    edge_table=edge_table,
                    kind="connector",
                    packet_depth=None,
                )
            )

    packet_depth_to_tick = {
        int(step["packet_depth"]): int(step["body_tick"])
        for step in steps
        if step["kind"] == "packet"
    }
    edge_keys = [edge_key(step["source"], step["target"]) for step in steps]
    vertices = (
        [steps[0]["source"]] + [step["target"] for step in steps] if steps else []
    )
    used_blocks = sorted({int(step["tomotope_block"]) for step in steps})

    return {
        "program": program["program"],
        "level": int(program["level"]),
        "route_bound": int(program["route_bound"]),
        "bt828_reversible_moves": int(program["reversible_moves"]),
        "q6_walk_steps": len(steps),
        "packet_edge_steps": len(packet_rows),
        "connector_steps": connector_steps,
        "body_slack_ticks": int(program["route_bound"]) - len(steps),
        "start_vertex": vertices[0] if vertices else None,
        "end_vertex": vertices[-1] if vertices else None,
        "vertices": vertices,
        "steps": steps,
        "packet_depth_to_body_tick": {
            str(depth): tick for depth, tick in sorted(packet_depth_to_tick.items())
        },
        "direction_histogram": {
            str(k): v
            for k, v in sorted(Counter(step["q6_direction"] for step in steps).items())
        },
        "used_tomotope_blocks": used_blocks,
        "checks": {
            "continuous_vertices_match_steps": len(vertices) == len(steps) + 1,
            "each_step_is_q6_edge": all(
                hamming(step["source"], step["target"]) == 1 for step in steps
            ),
            "table_direction_matches_walk_axis": all(
                step["walk_bit_axis"] == 5 - step["q6_direction"] for step in steps
            ),
            "all_traversed_edges_are_in_bt1371_table": all(
                edge_key(step["source"], step["target"]) in edge_table for step in steps
            ),
            "packet_edges_preserved_in_order": [
                step["q6_edge_index"] for step in steps if step["kind"] == "packet"
            ]
            == program["q6_edge_indices"],
            "no_repeated_q6_edge": len(set(edge_keys)) == len(edge_keys),
            "walk_fits_program_route_bound": len(steps) <= int(program["route_bound"]),
            "walk_fits_48_tick_tomotope_body": len(steps) <= 48,
            "body_ticks_are_contiguous": [step["body_tick"] for step in steps]
            == list(range(len(steps))),
        },
    }


def build_result() -> dict[str, Any]:
    bt1371 = load_json("data/bt1371_q6_tomotope_explicit_orbit_address_table.json")
    bt1374 = load_json("data/bt1374_q6_tomotope_packet_route_compiler.json")
    edge_table = build_edge_index(bt1371["address_table"])
    routes = [
        continuous_route_for_program(program, edge_table)
        for program in bt1374["compiled_programs"]
    ]
    stress = next(route for route in routes if route["program"] == "six_digit_stress")

    checks = {
        "bt1371_address_table_verified": bt1371["verified"] is True,
        "bt1374_packet_compiler_verified": bt1374["verified"] is True,
        "all_programs_became_continuous_q6_walks": all(
            all(route["checks"].values()) for route in routes
        ),
        "stress_route_preserves_six_packet_edges": stress["packet_edge_steps"] == 6,
        "stress_route_has_ten_connector_steps": stress["connector_steps"] == 10,
        "stress_route_is_sixteen_q6_steps": stress["q6_walk_steps"] == 16,
        "stress_route_leaves_32_body_ticks_slack": stress["body_slack_ticks"] == 32,
        "stress_route_still_fits_48_tick_body": stress["q6_walk_steps"] <= 48,
    }

    return {
        "bt": 1405,
        "title": "Continuous Q6 path router for holonet packet programs",
        "verified": all(checks.values()),
        "breakthrough": (
            "BT1374 packet addresses are not isolated waypoints: every compiled "
            "program now lifts to a continuous Q6 walk.  The six-digit stress "
            "route preserves its six Q6 packet edges, inserts ten connector "
            "edges, and occupies only 16 of the 48 tomotope-body ticks."
        ),
        "routing_rule": (
            "Orient packet edges to minimize total Hamming connector length; "
            "insert lexicographic shortest Q6 connector walks; map every "
            "traversed edge back through the BT1371 tomotope flag table."
        ),
        "routes": routes,
        "stress_summary": {
            "program": stress["program"],
            "packet_edges": [
                step["q6_edge_index"]
                for step in stress["steps"]
                if step["kind"] == "packet"
            ],
            "q6_walk_steps": stress["q6_walk_steps"],
            "connector_steps": stress["connector_steps"],
            "body_slack_ticks": stress["body_slack_ticks"],
            "start_vertex": stress["start_vertex"],
            "end_vertex": stress["end_vertex"],
            "direction_histogram": stress["direction_histogram"],
            "used_tomotope_blocks": stress["used_tomotope_blocks"],
        },
        "boundary": (
            "This is still a Q6/tomotope ABI router, not an optical waveguide "
            "layout or detector timing calibration.  It proves continuous "
            "hypercube path routing inside the existing packet body budget."
        ),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    ns = parser.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "stress_q6_steps": result["stress_summary"]["q6_walk_steps"],
                "stress_slack": result["stress_summary"]["body_slack_ticks"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
