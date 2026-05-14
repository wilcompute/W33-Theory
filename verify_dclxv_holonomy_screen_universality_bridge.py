#!/usr/bin/env python3
"""Part DCLXV: holonomy screen universality bridge.

After DCLXIV, the next honest question is whether the qutrit transvection witness
is a single lucky representative or a universal family on the exact W(3,3)
carrier. This verifier proves the stronger statement.

For every projective point x in W(3,3), the repo transvection anchored at x:

* is symplectic and has order 3,
* has the same projective orbit decomposition 40 = 13 + 9*3,
* fixes exactly the hyperplane x^perp,
* and that fixed hyperplane is exactly the closed W(3,3) neighborhood {x} U N(x).

So the remaining mixed-plane witness is not one isolated operator. It is the full
40-point universal family of canonical qutrit transvections already encoded by
the W(3,3) graph itself.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from w33_h1_decomposition import J_matrix, apply_matrix_projective, transvection_matrix
from w33_homology import build_w33

OUT_PATH = ROOT / "data" / "dclxv_holonomy_screen_universality_bridge.json"
MODULUS = 3


@dataclass(frozen=True)
class UniversalitySummary:
    field_order: int
    anchor_count: int
    transvection_order: int
    fixed_screen_size: int
    mobile_bulk_size: int
    three_cycle_count: int
    distinct_fixed_screens: int
    point_screen_incidence_count: int
    all_identities_hold: bool


def _mat_mod3(matrix: np.ndarray) -> np.ndarray:
    return np.array(matrix, dtype=int) % MODULUS


def _canon_point(point: Any) -> tuple[int, int, int, int]:
    values = [int(x) % MODULUS for x in point]
    for value in values:
        if value != 0:
            if value == 2:
                values = [(2 * x) % MODULUS for x in values]
            return tuple(values)
    raise ValueError("zero vector is not a projective point")


def _symplectic_form(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    a, b, c, d = u
    a2, b2, c2, d2 = v
    return (a * b2 - b * a2 + c * d2 - d * c2) % MODULUS


def _compute_order(matrix: np.ndarray) -> int:
    identity = np.eye(matrix.shape[0], dtype=int)
    power = identity.copy()
    for order in range(1, 20):
        power = _mat_mod3(power @ matrix)
        if np.array_equal(power, identity):
            return order
    raise ValueError("matrix order exceeded search bound")


def _build_projective_action(matrix: np.ndarray, vertices: list[tuple[int, int, int, int]], adjacency_sets: list[set[int]]) -> dict[str, Any]:
    index_by_vertex = {vertex: index for index, vertex in enumerate(vertices)}
    permutation = [index_by_vertex[_canon_point(apply_matrix_projective(matrix, vertex))] for vertex in vertices]

    seen: set[int] = set()
    orbit_indices: list[list[int]] = []
    for start in range(len(vertices)):
        if start in seen:
            continue
        orbit: list[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            orbit.append(current)
            current = permutation[current]
        orbit_indices.append(orbit)

    orbits = [[vertices[index] for index in orbit] for orbit in orbit_indices]
    orbit_size_counts = dict(sorted(Counter(len(orbit) for orbit in orbits).items()))
    adjacency_preserved = all(
        ((j in adjacency_sets[i]) == (permutation[j] in adjacency_sets[permutation[i]]))
        for i in range(len(vertices))
        for j in range(len(vertices))
        if i != j
    )

    return {
        "permutation": permutation,
        "orbits": orbits,
        "orbit_size_counts": orbit_size_counts,
        "adjacency_preserved": adjacency_preserved,
    }


def build_bridge() -> dict[str, Any]:
    _, raw_vertices, adj, _ = build_w33()
    vertices = list(dict.fromkeys(_canon_point(vertex) for vertex in raw_vertices))
    adjacency_sets = [set(row) for row in adj]
    J = J_matrix()

    anchor_records: list[dict[str, Any]] = []
    fixed_screen_signatures: set[tuple[tuple[int, int, int, int], ...]] = set()
    screen_membership_counter: Counter[int] = Counter()

    for anchor in vertices:
        matrix = _mat_mod3(transvection_matrix(np.array(anchor, dtype=int), J))
        action = _build_projective_action(matrix, vertices, adjacency_sets)
        fixed_points = sorted(orbit[0] for orbit in action["orbits"] if len(orbit) == 1)
        mobile_point_count = sum(len(orbit) for orbit in action["orbits"] if len(orbit) == 3)
        perp_hyperplane = sorted(point for point in vertices if _symplectic_form(point, anchor) == 0)
        closed_neighborhood = sorted([anchor, *[vertices[index] for index in adjacency_sets[vertices.index(anchor)]]])

        fixed_signature = tuple(fixed_points)
        fixed_screen_signatures.add(fixed_signature)
        for point in fixed_points:
            screen_membership_counter[vertices.index(point)] += 1

        anchor_records.append(
            {
                "anchor": anchor,
                "order": _compute_order(matrix),
                "orbit_size_counts": action["orbit_size_counts"],
                "fixed_count": len(fixed_points),
                "mobile_count": mobile_point_count,
                "fixed_screen_matches_perp_hyperplane": fixed_points == perp_hyperplane,
                "fixed_screen_matches_closed_neighborhood": fixed_points == closed_neighborhood,
                "anchor_lies_in_fixed_screen": anchor in fixed_points,
                "adjacency_preserved": action["adjacency_preserved"],
                "sample_three_cycle": next((orbit for orbit in action["orbits"] if len(orbit) == 3), []),
            }
        )

    orbit_profiles = {tuple(sorted(record["orbit_size_counts"].items())) for record in anchor_records}
    fixed_counts = {record["fixed_count"] for record in anchor_records}
    mobile_counts = {record["mobile_count"] for record in anchor_records}
    membership_profile = dict(sorted(Counter(screen_membership_counter.values()).items()))

    identities = {
        "all_40_projective_points_define_a_transvection_witness": len(anchor_records) == 40,
        "every_anchor_transvection_is_symplectic": all(
            np.array_equal(
                _mat_mod3(_mat_mod3(transvection_matrix(np.array(record["anchor"], dtype=int), J)).T @ J @ _mat_mod3(transvection_matrix(np.array(record["anchor"], dtype=int), J))),
                J,
            )
            for record in anchor_records
        ),
        "every_anchor_transvection_has_order_3": all(record["order"] == 3 for record in anchor_records),
        "every_anchor_has_the_same_13_plus_9_times_3_shell": orbit_profiles == {((1, 13), (3, 9))},
        "every_fixed_screen_has_size_13": fixed_counts == {13},
        "every_mobile_bulk_has_size_27": mobile_counts == {27},
        "every_fixed_screen_is_exactly_the_anchor_perp_hyperplane": all(
            record["fixed_screen_matches_perp_hyperplane"] for record in anchor_records
        ),
        "every_fixed_screen_is_exactly_the_closed_w33_neighborhood": all(
            record["fixed_screen_matches_closed_neighborhood"] for record in anchor_records
        ),
        "each_anchor_lies_in_its_own_screen": all(record["anchor_lies_in_fixed_screen"] for record in anchor_records),
        "each_anchor_action_preserves_w33_adjacency": all(record["adjacency_preserved"] for record in anchor_records),
        "there_are_40_distinct_fixed_screens": len(fixed_screen_signatures) == 40,
        "each_projective_point_lies_in_13_screens": membership_profile == {13: 40},
        "therefore_the_open_holonomy_witness_is_a_universal_40_point_qutrit_transvection_family": (
            len(anchor_records) == 40
            and orbit_profiles == {((1, 13), (3, 9))}
            and fixed_counts == {13}
            and mobile_counts == {27}
            and all(record["fixed_screen_matches_closed_neighborhood"] for record in anchor_records)
            and len(fixed_screen_signatures) == 40
            and membership_profile == {13: 40}
        ),
    }

    summary = UniversalitySummary(
        field_order=MODULUS,
        anchor_count=len(anchor_records),
        transvection_order=3,
        fixed_screen_size=13,
        mobile_bulk_size=27,
        three_cycle_count=9,
        distinct_fixed_screens=len(fixed_screen_signatures),
        point_screen_incidence_count=13,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "carrier_statistics": {
            "uniform_orbit_profiles": [dict(profile) for profile in sorted(orbit_profiles)],
            "fixed_screen_size_set": sorted(fixed_counts),
            "mobile_bulk_size_set": sorted(mobile_counts),
            "point_screen_membership_histogram": membership_profile,
        },
        "anchor_records": anchor_records,
        "interpretation": {
            "witness_family": "40 projective anchors in W(3,3)",
            "fixed_screen": "13-point closed neighborhood = anchor perp hyperplane",
            "mobile_shell": "27-point complement split into 9 three-cycles",
            "breakthrough": (
                "The mixed-plane holonomy witness is not a one-off matrix. Every W(3,3) projective point carries the same canonical order-3 qutrit transvection shell, and its fixed screen is already the closed neighborhood of that point in the existing graph."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()