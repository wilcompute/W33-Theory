#!/usr/bin/env python3
"""Conflict-free frame scheduler for the balanced W33 route selector.

The line-and-relay balanced selector chooses one two-hop route for each of the
540 unordered nonlocal W33 point pairs.  Each chosen route uses two W33 line
buses, and the selector has already proved the aggregate bus law

    every one of the 40 line buses is used exactly 27 times.

This verifier promotes the aggregate law into a timetable.  It factors the
540 selected two-line routes into 27 frames, each containing 20 disjoint
line-pairs.  In every frame all 40 line buses fire exactly once.

So the 135-byte selector is not merely balanced over time; it is schedulable as

    27 frames * 20 simultaneous two-hop transfers = 540 routes.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

from w33_line_relay_balanced_route_selector import (
    DEFAULT_JSON as DEFAULT_SELECTOR_JSON,
    build_payload as build_selector_payload,
)
from w33_uor_runtime_model import ROOT


DEFAULT_JSON = ROOT / "data" / "w33_line_pair_factorization_scheduler.json"
DEFAULT_MD = ROOT / "docs" / "w33_line_pair_factorization_scheduler.md"
FRAME_COUNT = 27
FRAME_WIDTH = 20
LINE_COUNT = 40


def load_or_build_selector(path: Path) -> dict[str, Any]:
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("status") == "PASS":
                return data
        except json.JSONDecodeError:
            pass
    return build_selector_payload()


def edge_instances(selector: dict[str, Any]) -> list[tuple[int, int, int]]:
    edges = []
    for row in selector["certificate"]:
        a, b = sorted(int(line_id) for line_id in row["line_pair"])
        edges.append((a, b, int(row["route_index"])))
    return edges


def residual_index(
    edges: list[tuple[int, int, int]], edge_ids: set[int]
) -> tuple[list[set[int]], dict[int, tuple[int, int]]]:
    incidence = [set() for _ in range(LINE_COUNT)]
    edge_map = {}
    for edge_id in edge_ids:
        a, b, _route = edges[edge_id]
        edge_map[edge_id] = (a, b)
        incidence[a].add(edge_id)
        incidence[b].add(edge_id)
    return incidence, edge_map


def degree_histogram(edges: list[tuple[int, int, int]], edge_ids: set[int]) -> Counter:
    degrees = Counter()
    for edge_id in edge_ids:
        a, b, _route = edges[edge_id]
        degrees[a] += 1
        degrees[b] += 1
    return Counter(degrees.values())


def find_perfect_matching(
    edges: list[tuple[int, int, int]],
    edge_ids: set[int],
    rng: random.Random,
    *,
    node_limit: int = 250_000,
) -> list[int] | None:
    """Find one 20-edge perfect matching of the current 40-line multigraph."""

    incidence, edge_map = residual_index(edges, edge_ids)
    unmatched = set(range(LINE_COUNT))
    chosen: list[int] = []
    nodes = 0

    def rec() -> list[int] | None:
        nonlocal nodes
        nodes += 1
        if nodes > node_limit:
            return None
        if not unmatched:
            return chosen.copy()

        best_vertex = -1
        best_candidates: list[int] | None = None
        vertices = list(unmatched)
        rng.shuffle(vertices)
        for vertex in vertices:
            candidates = [
                edge_id
                for edge_id in incidence[vertex]
                if edge_map[edge_id][0] in unmatched and edge_map[edge_id][1] in unmatched
            ]
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_vertex = vertex
                best_candidates = candidates
                if not candidates:
                    break

        if not best_candidates:
            return None

        scored = []
        for edge_id in best_candidates:
            a, b = edge_map[edge_id]
            other = b if a == best_vertex else a
            other_degree = sum(
                1
                for candidate in incidence[other]
                if edge_map[candidate][0] in unmatched and edge_map[candidate][1] in unmatched
            )
            scored.append((other_degree, rng.random(), edge_id, other))
        scored.sort()

        for _degree, _jitter, edge_id, other in scored:
            if best_vertex not in unmatched or other not in unmatched:
                continue
            unmatched.remove(best_vertex)
            unmatched.remove(other)
            chosen.append(edge_id)
            out = rec()
            if out is not None:
                return out
            chosen.pop()
            unmatched.add(best_vertex)
            unmatched.add(other)
        return None

    return rec()


def factor_selected_routes(
    edges: list[tuple[int, int, int]], *, seed: int = 7331
) -> list[list[int]]:
    """Construct the 27 conflict-free line frames."""

    rng = random.Random(seed)
    residual = set(range(len(edges)))
    frames: list[list[int]] = []

    for frame_index in range(FRAME_COUNT):
        matching = find_perfect_matching(edges, residual, rng)
        if matching is None:
            raise RuntimeError(f"could not factor residual at frame {frame_index}")
        frames.append([edges[edge_id][2] for edge_id in matching])
        residual.difference_update(matching)
        expected_degree = FRAME_COUNT - frame_index - 1
        if expected_degree > 0:
            observed = degree_histogram(edges, residual)
            if observed != Counter({expected_degree: LINE_COUNT}):
                raise RuntimeError(
                    f"non-regular residual after frame {frame_index}: {dict(observed)}"
                )

    if residual:
        raise RuntimeError(f"factorization left {len(residual)} route edges unused")
    return frames


def route_line_pair_map(selector: dict[str, Any]) -> dict[int, tuple[int, int]]:
    out = {}
    for row in selector["certificate"]:
        out[int(row["route_index"])] = tuple(sorted(int(line_id) for line_id in row["line_pair"]))
    return out


def frame_rows(
    frames: list[list[int]], route_lines: dict[int, tuple[int, int]]
) -> list[dict[str, Any]]:
    rows = []
    for frame_index, routes in enumerate(frames):
        lines = []
        for route_index in routes:
            lines.extend(route_lines[route_index])
        rows.append(
            {
                "frame": frame_index,
                "route_count": len(routes),
                "routes": routes,
                "line_histogram": {
                    str(k): v for k, v in sorted(Counter(lines).items())
                },
                "line_count": len(set(lines)),
                "line_sum": sum(lines),
            }
        )
    return rows


def build_payload() -> dict[str, Any]:
    selector = load_or_build_selector(DEFAULT_SELECTOR_JSON)
    edges = edge_instances(selector)
    frames = factor_selected_routes(edges)
    route_lines = route_line_pair_map(selector)
    rows = frame_rows(frames, route_lines)

    used_routes = [route for frame in frames for route in frame]
    total_line_hits = Counter()
    frame_checks = []
    for frame in frames:
        line_hits = Counter()
        for route_index in frame:
            line_hits.update(route_lines[route_index])
        total_line_hits.update(line_hits)
        frame_checks.append(line_hits == Counter({line_id: 1 for line_id in range(LINE_COUNT)}))

    checks = {
        "selector_pass": selector["status"] == "PASS",
        "frame_count_27": len(frames) == FRAME_COUNT,
        "frame_width_20": Counter(len(frame) for frame in frames) == {FRAME_WIDTH: FRAME_COUNT},
        "all_540_routes_used_once": sorted(used_routes) == list(range(FRAME_COUNT * FRAME_WIDTH)),
        "each_frame_uses_all_40_lines_once": all(frame_checks),
        "aggregate_line_loads_remain_27": total_line_hits == Counter(
            {line_id: FRAME_COUNT for line_id in range(LINE_COUNT)}
        ),
        "factor_identities": FRAME_COUNT * FRAME_WIDTH == 540 and FRAME_WIDTH * 2 == LINE_COUNT,
    }
    return {
        "schema": "w33.line_pair_factorization_scheduler.v1",
        "theorem": "the balanced 135-byte selector factors into 27 conflict-free 20-route frames",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "parameters": {
            "route_count": len(used_routes),
            "frame_count": len(frames),
            "frame_width": FRAME_WIDTH,
            "line_count": LINE_COUNT,
            "frame_identity": "540 = 27 * 20",
            "line_identity": "40 = 20 * 2",
            "qutrit_clock_reading": "27 = q^3 frames",
        },
        "scheduler": {
            "frame_route_indices": frames,
            "frame_rows": rows,
        },
        "line_usage": {
            "aggregate_histogram": {
                str(k): v for k, v in sorted(Counter(total_line_hits.values()).items())
            },
            "per_line": [total_line_hits[line_id] for line_id in range(LINE_COUNT)],
        },
        "checks": checks,
        "interpretation": (
            "The unordered selector is a real bus scheduler.  Each of the 27 qutrit-clock "
            "frames contains 20 simultaneous two-hop transfers, and no W33 line bus is "
            "used twice inside a frame.  Across all frames every line bus appears 27 times."
        ),
        "honesty_boundary": (
            "This factors the selected two-line route multigraph.  It does not yet attach "
            "the frames to an experimentally timed photonic pulse train or prove that this "
            "particular factorization is unique under symmetry."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    params = payload["parameters"]
    return f"""# W(3,3) Line-Pair Factorization Scheduler

The balanced selector is schedulable as conflict-free line-bus frames:

```text
{params['frame_identity']}
{params['line_identity']}
```

Every frame contains `{params['frame_width']}` two-hop routes.  Because each
two-hop route uses two W33 line buses, every frame touches all `{params['line_count']}`
line buses exactly once.

| Quantity | Value |
|---|---:|
| Frames | `{params['frame_count']}` |
| Routes per frame | `{params['frame_width']}` |
| Total routes | `{params['route_count']}` |
| Aggregate line-load histogram | `{payload['line_usage']['aggregate_histogram']}` |

Interpretation: the 135-byte reversal-symmetric selector is not just a balanced
choice vector.  It is a qutrit-clock timetable: `27 = q^3` conflict-free frames,
each firing 20 simultaneous two-hop transfers.

Boundary: the factorization is an exact finite scheduler for the selected
route multigraph.  It is not yet a uniqueness theorem and it does not yet assign
physical pulse timings.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload()
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    Path(args.md_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.md_out).write_text(markdown(payload), encoding="utf-8")

    print(f"status: {payload['status']}")
    print(f"frames: {payload['parameters']['frame_count']}")
    print(f"routes/frame: {payload['parameters']['frame_width']}")
    print(f"aggregate line histogram: {payload['line_usage']['aggregate_histogram']}")
    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
