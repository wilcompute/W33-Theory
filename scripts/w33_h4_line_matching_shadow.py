"""Canonical 120-state H4 shadow inside W(3,3).

The 40 isotropic lines of W(3,3) are K4 subgraphs.  Each K4 has three
perfect matchings, so the line/matching states form a canonical 40*3=120
object.  Each state contains two W33 edges, giving an exact 2-cover

    240 W33 edges -> 120 line-matching states.

This is the finite-geometry shadow of the E8 -> H4 root-count collapse:
240 E8 roots project to 120 H4 roots.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "w33_h4_line_matching_shadow_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.w33_algebra_qca import build_w33_geometry


def _edge(a: int, b: int) -> tuple[int, int]:
    return tuple(sorted((a, b)))


def _matching_key(edges: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(sorted((_edge(*edges[0]), _edge(*edges[1]))))


def perfect_matchings(line: tuple[int, int, int, int]) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    """Return the three perfect matchings of the K4 on ``line``."""
    a, b, c, d = line
    return (
        _matching_key(((a, b), (c, d))),
        _matching_key(((a, c), (b, d))),
        _matching_key(((a, d), (b, c))),
    )


def build_lines_from_w33() -> tuple[list[tuple[int, int, int, int]], set[tuple[int, int]], dict[int, set[int]]]:
    """Construct the 40 isotropic lines as maximal K4s in the W33 graph."""
    points, edges, adj, _triangles, _J = build_w33_geometry()
    edge_set = {_edge(a, b) for a, b in edges}
    lines: list[tuple[int, int, int, int]] = []
    for quad in combinations(range(len(points)), 4):
        if all(_edge(a, b) in edge_set for a, b in combinations(quad, 2)):
            lines.append(tuple(quad))
    return sorted(lines), edge_set, adj


def build_h4_shadow() -> dict[str, Any]:
    """Build and verify the 120-state line-matching shadow."""
    lines, edge_set, adj = build_lines_from_w33()

    states: list[dict[str, Any]] = []
    edge_to_state: dict[tuple[int, int], int] = {}
    line_edge_counter: Counter[tuple[int, int]] = Counter()
    state_edge_counter: Counter[tuple[int, int]] = Counter()
    point_line_counter: Counter[int] = Counter()
    point_state_counter: Counter[int] = Counter()
    line_to_states: defaultdict[int, list[int]] = defaultdict(list)

    for line_id, line in enumerate(lines):
        line_edges = {_edge(a, b) for a, b in combinations(line, 2)}
        line_edge_counter.update(line_edges)
        point_line_counter.update(line)

        matchings = perfect_matchings(line)
        assert len(set(matchings)) == 3
        for matching in matchings:
            state_id = len(states)
            matching_edges = tuple(matching)
            endpoints = sorted({x for e in matching_edges for x in e})
            assert tuple(endpoints) == line
            assert matching_edges[0][0] not in matching_edges[1]
            assert matching_edges[0][1] not in matching_edges[1]

            states.append(
                {
                    "state_id": state_id,
                    "line_id": line_id,
                    "line": line,
                    "matching": matching_edges,
                }
            )
            line_to_states[line_id].append(state_id)
            state_edge_counter.update(matching_edges)
            point_state_counter.update(line)
            for e in matching_edges:
                if e in edge_to_state:
                    raise AssertionError(f"edge {e} appears in two matching states")
                edge_to_state[e] = state_id

    line_edges = set(line_edge_counter)
    state_edges = set(state_edge_counter)
    per_line_matchings = sorted(len(v) for v in line_to_states.values())

    checks = {
        "line_count_is_40": len(lines) == 40,
        "edge_count_is_240": len(edge_set) == 240,
        "state_count_is_120": len(states) == 120,
        "three_states_per_line": per_line_matchings == [3] * 40,
        "six_edges_per_line": sorted(line_edge_counter.values()) == [1] * 240,
        "line_edges_cover_w33_edges": line_edges == edge_set,
        "state_edges_cover_w33_edges": state_edges == edge_set,
        "each_edge_in_one_state": sorted(state_edge_counter.values()) == [1] * 240,
        "two_edges_per_state": all(len(s["matching"]) == 2 for s in states),
        "four_lines_per_point": sorted(point_line_counter.values()) == [4] * 40,
        "twelve_states_per_point": sorted(point_state_counter.values()) == [12] * 40,
    }

    constants = {
        "q": 3,
        "v": 40,
        "k": 12,
        "mu": 4,
        "w33_edges": len(edge_set),
        "w33_lines": len(lines),
        "line_matchings": len(states),
        "e8_root_count": 240,
        "h4_root_count": 120,
        "states_times_two": 2 * len(states),
        "lines_times_q": 3 * len(lines),
    }

    theorem = {
        "w33_edges_are_a_two_cover_of_line_matching_states": checks["state_edges_cover_w33_edges"]
        and checks["each_edge_in_one_state"]
        and constants["states_times_two"] == constants["w33_edges"],
        "line_matching_states_match_h4_root_count": constants["line_matchings"] == constants["h4_root_count"],
        "w33_edges_match_e8_root_count": constants["w33_edges"] == constants["e8_root_count"],
        "internal_projection_formula": "40 lines * 3 matchings/line * 2 edges/matching = 240",
    }

    return {
        "constants": constants,
        "checks": checks,
        "theorem": theorem,
        "lines": lines,
        "states": states,
        "edge_to_state": {f"{a}-{b}": sid for (a, b), sid in sorted(edge_to_state.items())},
    }


def write_summary(path: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    summary = build_h4_shadow()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    out = write_summary()
    print(json.dumps(out["theorem"], indent=2))
