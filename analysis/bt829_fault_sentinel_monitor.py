#!/usr/bin/env python3
"""
BT829 - Fault sentinel monitor for the g=15 sector.

The W33 adjacency spectrum is 12^1, 2^24, (-4)^15.  BT778 identified a
15-dimensional sentinel at the chart-web level.  BT829 gives the point-plane
version exactly: the projector onto the -4 eigenspace has entries

    diagonal     3/8
    adjacent    -1/8
    nonadjacent  1/24

so context-line traffic is invisible to the sentinel, while localized and
shell-like faults activate it with exact rational energy.
"""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

from bt787_rank4_incidence_r11_handle import build_geometry


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open() as f:
        return json.load(f)


def frac(x: Fraction | None) -> str | None:
    if x is None:
        return None
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def build_adjacency(geom: dict) -> list[list[int]]:
    n = len(geom["points"])
    adj = [[0 for _ in range(n)] for _ in range(n)]
    for line in geom["line_sets"]:
        pts = sorted(line)
        for i, a in enumerate(pts):
            for b in pts[i + 1:]:
                adj[a][b] = adj[b][a] = 1
    return adj


def matmul_fraction(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(a)
    out = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k] == 0:
                continue
            aik = a[i][k]
            for j in range(n):
                out[i][j] += aik * b[k][j]
    return out


def sentinel_projector(adj: list[list[int]]) -> list[list[Fraction]]:
    n = len(adj)
    adj_f = [[Fraction(x) for x in row] for row in adj]
    a2 = matmul_fraction(adj_f, adj_f)
    return [
        [
            (a2[i][j] - 14 * adj[i][j] + (24 if i == j else 0)) / 96
            for j in range(n)
        ]
        for i in range(n)
    ]


def subset_energy(projector: list[list[Fraction]], subset: set[int]) -> Fraction:
    return sum(projector[i][j] for i in subset for j in subset)


def centered_norm(v: int, subset: set[int]) -> Fraction:
    m = len(subset)
    return Fraction(m, 1) - Fraction(m * m, v)


def fault_row(name: str, subset: set[int], projector: list[list[Fraction]], v: int) -> dict:
    energy = subset_energy(projector, subset)
    norm = centered_norm(v, subset)
    ratio = None if norm == 0 else energy / norm
    return {
        "fault": name,
        "support_size": len(subset),
        "sentinel_energy": frac(energy),
        "centered_norm": frac(norm),
        "sentinel_fraction": frac(ratio),
        "activates_sentinel": energy > 0,
    }


def main() -> None:
    geom = build_geometry()
    adj = build_adjacency(geom)
    v = len(adj)
    projector = sentinel_projector(adj)
    p2 = matmul_fraction(projector, projector)

    diag_values = {projector[i][i] for i in range(v)}
    adjacent_values = {projector[i][j] for i in range(v) for j in range(v) if adj[i][j]}
    nonadjacent_values = {
        projector[i][j]
        for i in range(v)
        for j in range(v)
        if i != j and not adj[i][j]
    }
    idempotent = all(p2[i][j] == projector[i][j] for i in range(v) for j in range(v))
    trace = sum(projector[i][i] for i in range(v))

    point = 0
    line = set(next(line for line in geom["line_sets"] if point in line))
    neighbors = {j for j in range(v) if adj[point][j]}
    nonneighbors = set(range(v)) - neighbors - {point}
    adjacent_pair = {point, min(neighbors)}
    nonedge_pair = {point, min(nonneighbors)}

    fault_rows = [
        fault_row("uniform_all_points", set(range(v)), projector, v),
        fault_row("context_line_K4", line, projector, v),
        fault_row("single_point_impulse", {point}, projector, v),
        fault_row("adjacent_edge_congestion", adjacent_pair, projector, v),
        fault_row("nonedge_mirror_congestion", nonedge_pair, projector, v),
        fault_row("gauge_neighbor_shell_12", neighbors, projector, v),
        fault_row("matter_nonneighbor_shell_27", nonneighbors, projector, v),
    ]

    bt828 = load_json("data/bt828_holonet_packet_compiler.json")
    compiled_signatures = []
    for program in bt828["compiled_programs"]:
        touched = set(program["source"]) | set(program["target"])
        row = fault_row(f"compiled:{program['program']}", touched, projector, v)
        row["program_level"] = program["level"]
        row["reversible_moves"] = program["reversible_moves"]
        compiled_signatures.append(row)

    recursive_scenarios = []
    for level in range(1, 5):
        instances = (40**level - 1) // 39
        gauge = fault_rows[5]
        point_row = fault_rows[2]
        recursive_scenarios.append({
            "level": level,
            "w33_instances": instances,
            "one_point_fault_per_instance_total_energy": frac(Fraction(point_row["sentinel_energy"]) * instances),
            "one_gauge_shell_per_instance_total_energy": frac(Fraction(gauge["sentinel_energy"]) * instances),
            "sentinel_dimension_per_instance": 15,
            "total_sentinel_channels": 15 * instances,
        })

    checks = {
        "projector_is_idempotent": idempotent,
        "projector_trace_is_g_15": trace == 15,
        "projector_entry_profile": (
            diag_values == {Fraction(3, 8)}
            and adjacent_values == {Fraction(-1, 8)}
            and nonadjacent_values == {Fraction(1, 24)}
        ),
        "uniform_load_is_sentinel_invisible": fault_rows[0]["sentinel_energy"] == "0",
        "context_line_is_sentinel_invisible": fault_rows[1]["sentinel_energy"] == "0",
        "point_impulse_activates_sentinel": fault_rows[2]["sentinel_energy"] == "3/8",
        "nonedge_fault_stronger_than_adjacent_fault": Fraction(fault_rows[4]["sentinel_energy"]) > Fraction(fault_rows[3]["sentinel_energy"]),
        "gauge_shell_is_strongest_tested_fault": Fraction(fault_rows[5]["sentinel_fraction"]) > Fraction(fault_rows[6]["sentinel_fraction"]),
        "compiled_routes_have_sentinel_signatures": all(row["sentinel_energy"] != "0" for row in compiled_signatures),
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT829 check failed: {name}")

    out = {
        "theorem": "BT829 g=15 fault sentinel monitor",
        "projector_profile": {
            "diagonal": "3/8",
            "adjacent": "-1/8",
            "nonadjacent": "1/24",
            "trace": "15",
            "eigen_sector": "adjacency eigenvalue -4, multiplicity g=15",
        },
        "fault_signatures": fault_rows,
        "compiled_route_fault_signatures": compiled_signatures,
        "recursive_scenarios": recursive_scenarios,
        "checks": checks,
    }
    path = ROOT / "data" / "bt829_fault_sentinel_monitor.json"
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
