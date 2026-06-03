#!/usr/bin/env python3
"""Probe flow-pattern memory primitives for the Witting Reference Fabric.

This is deliberately exploratory. It does not assert a new theorem for the paper.
It tests whether the user's "information as encapsulated repeating flow" idea has
clean finite anchors in the existing WRF/W33 machinery:

1. W(3,3) supplies a 480-state directed-edge nonbacktracking carrier.
2. A deterministic local routing rule turns that carrier into flow attractors.
3. A datum can be represented by the canonical orbit of an attractor, not by a
   static address cell.
4. The existing 7+1 toroidal Markov model and the six-tick closure clock provide
   bounded relaxation and finite-horizon repair analogues.

The script writes wrf_flow_pattern_probe_results.json beside itself.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("wrf_flow_pattern_probe_results.json")
UOR_README = ROOT / "tmp" / "UOR-Framework-main" / "README.md"


def canonical_projective_point(p: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    for x in p:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((c * inv) % 3 for c in p)
    raise ValueError("zero vector has no projective representative")


def symplectic(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3


def build_w33() -> tuple[list[tuple[int, int, int, int]], list[set[int]], list[tuple[int, int]]]:
    points: list[tuple[int, int, int, int]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for raw in product(range(3), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        point = canonical_projective_point(raw)
        if point not in seen:
            seen.add(point)
            points.append(point)

    adjacency = [set() for _ in points]
    edges: list[tuple[int, int]] = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if symplectic(points[i], points[j]) == 0:
                adjacency[i].add(j)
                adjacency[j].add(i)
                edges.append((i, j))

    return points, adjacency, edges


def srg_parameters(adjacency: list[set[int]]) -> dict[str, int | bool]:
    degrees = [len(nbrs) for nbrs in adjacency]
    lambdas: set[int] = set()
    mus: set[int] = set()
    for i in range(len(adjacency)):
        for j in range(i + 1, len(adjacency)):
            common = len(adjacency[i] & adjacency[j])
            if j in adjacency[i]:
                lambdas.add(common)
            else:
                mus.add(common)
    return {
        "regular": len(set(degrees)) == 1,
        "degree": degrees[0],
        "lambda": next(iter(lambdas)),
        "mu": next(iter(mus)),
        "lambda_single": len(lambdas) == 1,
        "mu_single": len(mus) == 1,
    }


def directed_edges(edges: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for a, b in edges:
        out.append((a, b))
        out.append((b, a))
    return out


def stable_choice(seed: int, edge: tuple[int, int], candidates: list[int]) -> int:
    payload = f"{seed}:{edge[0]}:{edge[1]}".encode("ascii")
    digest = hashlib.sha256(payload).digest()
    return candidates[int.from_bytes(digest[:4], "big") % len(candidates)]


def build_functional_flow(
    adjacency: list[set[int]],
    d_edges: list[tuple[int, int]],
    seed: int,
) -> tuple[list[int], dict[tuple[int, int], int]]:
    edge_index = {edge: i for i, edge in enumerate(d_edges)}
    transition = [0] * len(d_edges)
    for idx, (a, b) in enumerate(d_edges):
        candidates = sorted(c for c in adjacency[b] if c != a)
        c = stable_choice(seed, (a, b), candidates)
        transition[idx] = edge_index[(b, c)]
    return transition, edge_index


def reverse_edge_map(d_edges: list[tuple[int, int]], edge_index: dict[tuple[int, int], int]) -> list[int]:
    return [edge_index[(b, a)] for a, b in d_edges]


def rotations(seq: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    for i in range(len(seq)):
        yield seq[i:] + seq[:i]


def canonical_cycle(cycle: list[int], reverse_edges: list[int]) -> tuple[int, ...]:
    forward = tuple(cycle)
    reverse = tuple(reverse_edges[e] for e in reversed(cycle))
    return min([*rotations(forward), *rotations(reverse)])


def cycle_cid(canon: tuple[int, ...]) -> str:
    payload = json.dumps(canon, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(payload).hexdigest()[:24]


def analyze_functional_flow(transition: list[int], reverse_edges: list[int]) -> dict[str, object]:
    n = len(transition)
    cycle_by_node: dict[int, int] = {}
    cycles: list[list[int]] = []
    max_transient = 0

    for start in range(n):
        if start in cycle_by_node:
            continue

        seen_at: dict[int, int] = {}
        path: list[int] = []
        cur = start
        while cur not in seen_at and cur not in cycle_by_node:
            seen_at[cur] = len(path)
            path.append(cur)
            cur = transition[cur]

        if cur in cycle_by_node:
            cid = cycle_by_node[cur]
            transient = len(path)
        else:
            cycle_start = seen_at[cur]
            cycle = path[cycle_start:]
            cid = len(cycles)
            cycles.append(cycle)
            transient = cycle_start
            for node in cycle:
                cycle_by_node[node] = cid

        for node in path:
            cycle_by_node[node] = cid
        max_transient = max(max_transient, transient)

    basin_sizes = Counter(cycle_by_node.values())
    length_histogram = Counter(len(cycle) for cycle in cycles)
    selected_id, selected_basin = max(basin_sizes.items(), key=lambda kv: (kv[1], len(cycles[kv[0]])))
    selected_cycle = cycles[selected_id]
    selected_canon = canonical_cycle(selected_cycle, reverse_edges)
    selected_cid = cycle_cid(selected_canon)

    rotated = selected_cycle[3 % len(selected_cycle) :] + selected_cycle[: 3 % len(selected_cycle)]
    reversed_cycle = [reverse_edges[e] for e in reversed(selected_cycle)]
    rotation_invariant = cycle_cid(canonical_cycle(rotated, reverse_edges)) == selected_cid
    reverse_invariant = cycle_cid(canonical_cycle(reversed_cycle, reverse_edges)) == selected_cid

    return {
        "component_count": len(cycles),
        "cycle_length_histogram": {str(k): v for k, v in sorted(length_histogram.items())},
        "max_transient_steps": max_transient,
        "largest_basin_size": selected_basin,
        "largest_basin_fraction": selected_basin / n,
        "selected_cycle_length": len(selected_cycle),
        "selected_cycle_cid": selected_cid,
        "rotation_invariant_cid": rotation_invariant,
        "reverse_invariant_cid": reverse_invariant,
        "selected_cycle_prefix": selected_cycle[: min(12, len(selected_cycle))],
    }


def toroidal_markov_probe() -> dict[str, object]:
    states = 8
    active = 7
    transition = [[Fraction(0, 1) for _ in range(states)] for _ in range(states)]

    for i in range(active):
        transition[i][i] = Fraction(1, 8)
        transition[i][(i + 1) % active] = Fraction(3, 8)
        transition[i][(i - 1) % active] = Fraction(3, 8)
        transition[i][7] = Fraction(1, 8)
    transition[7][7] = Fraction(1, 8)
    for i in range(active):
        transition[7][i] = Fraction(1, 8)

    row_stochastic = all(sum(row) == 1 for row in transition)
    uniform_stationary = all(
        sum(Fraction(1, states) * transition[i][j] for i in range(states)) == Fraction(1, states)
        for j in range(states)
    )

    rho = max(abs(Fraction(1, 8) + Fraction(3, 4) * math.cos(2 * math.pi * k / 7)) for k in range(1, 7))
    t_active = next(t for t in range(100) if 7 * (rho**t) <= 1)
    t_probability = next(t for t in range(100) if rho**t <= 1 / 24)

    return {
        "states": states,
        "active_states": active,
        "ground_states": 1,
        "row_stochastic": row_stochastic,
        "uniform_stationary": uniform_stationary,
        "stationary_active_mass": "7/8",
        "stationary_ground_mass": "1/8",
        "spectral_radius_bound": round(rho, 9),
        "active_count_horizon": t_active,
        "probability_packet_horizon": t_probability,
    }


def closure_clock_probe() -> dict[str, object]:
    dim = 6
    matrix = [[Fraction(0, 1) for _ in range(dim)] for _ in range(dim)]
    for i in range(dim - 1):
        matrix[i][i + 1] = Fraction(1, 2)

    def multiply(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
        return [
            [sum(a[i][k] * b[k][j] for k in range(dim)) for j in range(dim)]
            for i in range(dim)
        ]

    power = [[Fraction(int(i == j), 1) for j in range(dim)] for i in range(dim)]
    nonzero_powers: list[int] = []
    nilpotence_index = None
    for exponent in range(1, dim + 2):
        power = multiply(power, matrix)
        is_zero = all(cell == 0 for row in power for cell in row)
        if not is_zero:
            nonzero_powers.append(exponent)
        elif nilpotence_index is None:
            nilpotence_index = exponent

    return {
        "dimension": dim,
        "generator": "G=(1/2)S on a 6-state closure clock",
        "nonzero_powers": nonzero_powers,
        "nilpotence_index": nilpotence_index,
        "finite_impulse_response_depth": max(nonzero_powers),
    }


def uor_counts() -> dict[str, object]:
    if not UOR_README.exists():
        return {"available": False}
    text = UOR_README.read_text(encoding="utf-8")
    match = re.search(
        r"Version\s+([0-9.]+):\s+(\d+) namespaces . (\d+) classes . (\d+) properties . (\d+) named individuals",
        text,
    )
    if not match:
        return {"available": True, "parsed": False}
    version, namespaces, classes, properties, individuals = match.groups()
    return {
        "available": True,
        "parsed": True,
        "version": version,
        "namespaces": int(namespaces),
        "classes": int(classes),
        "properties": int(properties),
        "named_individuals": int(individuals),
    }


def main() -> int:
    points, adjacency, edges = build_w33()
    params = srg_parameters(adjacency)
    d_edges = directed_edges(edges)
    transition, edge_index = build_functional_flow(adjacency, d_edges, seed=1728)
    reverse_edges = reverse_edge_map(d_edges, edge_index)
    outdegrees = Counter(len([c for c in adjacency[b] if c != a]) for a, b in d_edges)
    flow = analyze_functional_flow(transition, reverse_edges)
    markov = toroidal_markov_probe()
    closure = closure_clock_probe()
    uor = uor_counts()

    checks = {
        "w33_has_40_vertices": len(points) == 40,
        "w33_has_240_edges": len(edges) == 240,
        "w33_has_480_directed_edges": len(d_edges) == 480,
        "w33_is_srg_40_12_2_4": (
            params["regular"]
            and params["degree"] == 12
            and params["lambda_single"]
            and params["lambda"] == 2
            and params["mu_single"]
            and params["mu"] == 4
        ),
        "nonbacktracking_outdegree_is_11": outdegrees == Counter({11: 480}),
        "flow_pattern_cid_is_rotation_invariant": bool(flow["rotation_invariant_cid"]),
        "flow_pattern_cid_is_reverse_invariant": bool(flow["reverse_invariant_cid"]),
        "markov_chain_has_uniform_stationary_measure": bool(markov["uniform_stationary"]),
        "closure_clock_is_nilpotent_at_6": closure["nilpotence_index"] == 6,
    }

    report = {
        "module": "wrf_flow_pattern_probe",
        "status": "exploratory_not_paper_claim",
        "verified": all(checks.values()),
        "checks": checks,
        "w33_carrier": {
            "vertices": len(points),
            "edges": len(edges),
            "directed_edges": len(d_edges),
            "srg": params,
            "nonbacktracking_outdegree_histogram": dict(outdegrees),
        },
        "functional_flow_cell": flow,
        "toroidal_markov_relaxation": markov,
        "closure_clock": closure,
        "uor_framework_local_anchor": uor,
        "interpretation": [
            "A WRF flow datum can be modeled as the canonical orbit of a closed or attracting trace.",
            "The addressable object is the invariant pattern, while the hardware state keeps moving.",
            "UOR can reference the canonical witness; HLIX can schedule/receipt projections; Oko can finalize pattern transitions; Smart Assets can meter sustained flow.",
            "This is promising as an architecture primitive, but it still needs a noise model, write protocol, and coupling algebra before entering the paper.",
        ],
    }
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
