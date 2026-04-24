"""PSp(4,3)-invariant obstruction for a 600-cell graph on M_120.

Supplement L constructs the 120 line-matching states M_120.  A tempting
next step is to declare a 600-cell graph on these states.  The 600-cell
skeleton is 12-regular, so a fully W(3,3)-canonical construction would
need a PSp(4,3)-invariant 12-regular relation on M_120.

This script computes the unordered pair orbitals of the full PSp(4,3)
action on M_120.  Their degrees are:

    2, 27, 36, 54.

No subset of these degrees sums to 12, so no full-symmetry invariant
600-cell adjacency exists on M_120.  Any H4/600-cell adjacency must
therefore choose extra structure, i.e. break PSp(4,3) to a smaller
icosahedral/golden subgroup.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, deque
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.w33_algebra_qca import build_w33_geometry
from scripts.w33_h4_line_matching_shadow import (
    _matching_key,
    build_h4_shadow,
    build_lines_from_w33,
)


DEFAULT_OUTPUT = ROOT / "data" / "w33_h4_orbital_no_go_summary.json"


def _symplectic_matrix_for_w33() -> np.ndarray:
    """Matrix S with B(x,y)=x^T S y for build_w33_geometry's symplectic form."""
    S = np.zeros((4, 4), dtype=int)
    S[0, 3] = 1
    S[1, 2] = -1
    S[2, 1] = 1
    S[3, 0] = -1
    return S % 3


def _normalize_projective(v: np.ndarray) -> tuple[int, int, int, int]:
    vals = [int(x) % 3 for x in v]
    for x in vals:
        pass
    for x in vals:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in vals)
    raise ValueError("zero vector has no projective representative")


def _transvection_matrix(u: tuple[int, int, int, int], S: np.ndarray) -> np.ndarray:
    """Symplectic transvection T_u(v)=v+B(v,u)u over F3."""
    col = np.array(u, dtype=int).reshape((4, 1))
    return (np.eye(4, dtype=int) + col @ (S @ col).T) % 3


def _vertex_permutation(M: np.ndarray, points: list[tuple[int, int, int, int]]) -> tuple[int, ...]:
    out: list[int] = []
    for point in points:
        image = _normalize_projective(M @ np.array(point, dtype=int))
        out.append(points.index(image))
    return tuple(out)


def build_state_generators() -> list[tuple[int, ...]]:
    """Return PSp(4,3) transvection generators acting on M_120 states."""
    summary = build_h4_shadow()
    states = summary["states"]
    lines, _edge_set, _adj = build_lines_from_w33()
    points, _edges, _adj0, _triangles, _J = build_w33_geometry()

    state_lookup = {
        (tuple(state["line"]), tuple(tuple(e) for e in state["matching"])): state["state_id"]
        for state in states
    }

    def map_state_perm(vperm: tuple[int, ...]) -> tuple[int, ...]:
        out: list[int] = []
        for state in states:
            img_line = tuple(sorted(vperm[x] for x in state["line"]))
            img_matching = _matching_key(
                (
                    tuple(vperm[x] for x in state["matching"][0]),
                    tuple(vperm[x] for x in state["matching"][1]),
                )
            )
            out.append(state_lookup[(img_line, img_matching)])
        return tuple(out)

    S = _symplectic_matrix_for_w33()
    generators: list[tuple[int, ...]] = []
    for point in points:
        vertex_perm = _vertex_permutation(_transvection_matrix(point, S), points)
        state_perm = map_state_perm(vertex_perm)
        if state_perm not in generators:
            generators.append(state_perm)
    return generators


def compute_pair_orbitals() -> dict[str, Any]:
    """Compute unordered pair orbitals for PSp(4,3) on M_120."""
    summary = build_h4_shadow()
    states = summary["states"]
    generators = build_state_generators()

    unseen = {(i, j) for i in range(120) for j in range(i + 1, 120)}
    orbitals: list[set[tuple[int, int]]] = []
    while unseen:
        seed = unseen.pop()
        orbit = {seed}
        queue = deque([seed])
        while queue:
            a, b = queue.popleft()
            for gen in generators:
                x, y = gen[a], gen[b]
                if x > y:
                    x, y = y, x
                pair = (x, y)
                if pair not in orbit:
                    orbit.add(pair)
                    queue.append(pair)
                    unseen.discard(pair)
        orbitals.append(orbit)

    records: list[dict[str, Any]] = []
    for orbital in sorted(orbitals, key=len):
        degree_counter: Counter[int] = Counter()
        same_line = intersecting_line = disjoint_line = 0
        for i, j in orbital:
            degree_counter[i] += 1
            degree_counter[j] += 1
            li, lj = states[i]["line_id"], states[j]["line_id"]
            if li == lj:
                same_line += 1
            elif set(states[i]["line"]) & set(states[j]["line"]):
                intersecting_line += 1
            else:
                disjoint_line += 1
        degrees = sorted(set(degree_counter.values()))
        assert len(degrees) == 1
        records.append(
            {
                "size": len(orbital),
                "degree": degrees[0],
                "same_line_pairs": same_line,
                "intersecting_line_pairs": intersecting_line,
                "disjoint_line_pairs": disjoint_line,
            }
        )

    orbital_degrees = [r["degree"] for r in records]
    possible_invariant_degrees = sorted(
        {
            sum(deg for bit, deg in enumerate(orbital_degrees) if mask & (1 << bit))
            for mask in range(1 << len(orbital_degrees))
        }
    )

    checks = {
        "state_count_is_120": len(states) == 120,
        "generator_count_is_40": len(generators) == 40,
        "pair_orbital_count_is_4": len(records) == 4,
        "orbital_degrees_are_2_27_36_54": orbital_degrees == [2, 27, 36, 54],
        "pair_sizes_sum_to_all_pairs": sum(r["size"] for r in records) == 120 * 119 // 2,
        "no_invariant_degree_12_relation": 12 not in possible_invariant_degrees,
    }

    theorem = {
        "no_full_psp43_invariant_600_cell_skeleton_on_M120": checks[
            "no_invariant_degree_12_relation"
        ],
        "reason": "The only invariant orbital degrees are 2, 27, 36, and 54; no subset sums to 12.",
        "required_next_structure": "A 600-cell/H4 adjacency must break PSp(4,3) to a smaller icosahedral or golden-ratio subgroup.",
    }

    return {
        "orbitals": records,
        "orbital_degrees": orbital_degrees,
        "possible_invariant_degrees": possible_invariant_degrees,
        "checks": checks,
        "theorem": theorem,
    }


def write_summary(path: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    summary = compute_pair_orbitals()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(write_summary()["theorem"], indent=2))
