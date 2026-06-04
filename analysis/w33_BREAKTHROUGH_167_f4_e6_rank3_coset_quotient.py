"""W(3,3) BREAKTHROUGH 167: F4 -> E6 rank-3 coset quotient.

BT159 proved the forbidden macro pocket generates an F4/24-cell normalizer
N of order 1152.  Since the full compiler group has order 51840,

    |G| / |N| = 51840 / 1152 = 45.

BT167 computes the actual coset action.  The N-orbits on the 45 left cosets
have sizes

    1 + 12 + 32 = 45.

The valency-12 orbital graph is strongly regular:

    srg(45, 12, 3, 3).

That is the parameter profile of GQ(4,2), the 45-object tritangent-plane
scale in the E6 cubic-surface story.  This packet proves the finite rank-3
quotient; it does not claim a canonical tritangent labeling.
"""

from __future__ import annotations

from collections import Counter, deque
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_157_cayley_compiler_macro_depth import (  # noqa: E402
    GROUP_ORDER,
    Q,
    QFACT,
    bfs_from_maps,
    build_group,
    generator_set,
    mat_inv,
    mat_mul,
    right_maps,
)
from analysis.w33_BREAKTHROUGH_158_macro_tail_sieve import (  # noqa: E402
    macro_tail_sieve_packet,
)
from analysis.w33_BREAKTHROUGH_159_forbidden_pocket_f4_normalizer import (  # noqa: E402
    F4_WEYL_ORDER,
    closure_generated_by,
    is_anti_diagonal,
    is_block_diagonal,
)


K = 12
PHI12 = 73
DIM_E6 = 78


def polarization_class(matrix: tuple[tuple[int, ...], ...]) -> str:
    if is_block_diagonal(matrix):
        return "block"
    if is_anti_diagonal(matrix):
        return "anti"
    return "mixed"


def _counter_to_json(counter: Counter) -> dict:
    return {str(key): value for key, value in sorted(counter.items())}


def left_cosets(
    elems: list[tuple[tuple[int, ...], ...]],
    normalizer: set[tuple[tuple[int, ...], ...]],
) -> tuple[
    list[tuple[tuple[int, ...], ...]],
    list[set[tuple[tuple[int, ...], ...]]],
    dict[tuple[tuple[int, ...], ...], int],
]:
    reps = []
    cosets = []
    elem_to_coset = {}

    for elem in elems:
        if elem in elem_to_coset:
            continue
        coset = {mat_mul(n, elem) for n in normalizer}
        coset_id = len(cosets)
        reps.append(elem)
        cosets.append(coset)
        for member in coset:
            elem_to_coset[member] = coset_id
    return reps, cosets, elem_to_coset


def double_coset_orbits(
    reps: list[tuple[tuple[int, ...], ...]],
    elem_to_coset: dict[tuple[tuple[int, ...], ...], int],
    normalizer_generators: list[tuple[tuple[int, ...], ...]],
) -> list[list[int]]:
    visited = set()
    orbits = []
    for coset_id, rep in enumerate(reps):
        if coset_id in visited:
            continue
        queue = deque([coset_id])
        visited.add(coset_id)
        orbit = []
        while queue:
            current = queue.popleft()
            orbit.append(current)
            current_rep = reps[current]
            for generator in normalizer_generators:
                nxt = elem_to_coset[mat_mul(current_rep, generator)]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        orbits.append(sorted(orbit))
    return orbits


def orbital_graph_parameters(
    reps: list[tuple[tuple[int, ...], ...]],
    elem_to_coset: dict[tuple[tuple[int, ...], ...], int],
    coset_to_orbit_size: dict[int, int],
    target_orbit_size: int,
) -> dict:
    n = len(reps)
    adjacency = [[False] * n for _ in range(n)]
    for left_index, left in enumerate(reps):
        left_inv = mat_inv(left)
        for right_index, right in enumerate(reps):
            if left_index == right_index:
                continue
            # For the right action on left cosets, pair type is N * right * left^-1 * N.
            relative = mat_mul(right, left_inv)
            if coset_to_orbit_size[elem_to_coset[relative]] == target_orbit_size:
                adjacency[left_index][right_index] = True

    degrees = [sum(row) for row in adjacency]
    lambda_counts = Counter()
    mu_counts = Counter()
    for i in range(n):
        for j in range(i + 1, n):
            common = sum(adjacency[i][k] and adjacency[j][k] for k in range(n))
            if adjacency[i][j]:
                lambda_counts[common] += 1
            else:
                mu_counts[common] += 1

    return {
        "v": n,
        "degree_distribution": dict(sorted(Counter(degrees).items())),
        "edge_count": sum(degrees) // 2,
        "lambda_distribution": dict(sorted(lambda_counts.items())),
        "mu_distribution": dict(sorted(mu_counts.items())),
        "symmetric": all(adjacency[i][j] == adjacency[j][i] for i in range(n) for j in range(n)),
    }


def f4_e6_rank3_coset_quotient_packet() -> dict:
    tail_packet = macro_tail_sieve_packet()
    forbidden = [
        tuple(tuple(entry for entry in row) for row in item["matrix"])
        for item in tail_packet["forbidden_macros"]
    ]
    forbidden_set = set(forbidden)
    normalizer = closure_generated_by(forbidden)

    generators, _labels = generator_set(include_inverses=True)
    elems, index, _parent, _parent_gen = build_group(generators)
    base_maps = right_maps(elems, index, generators)
    symmetric_dist = bfs_from_maps(base_maps, len(elems))
    tail = [elem for elem in elems if symmetric_dist[index[elem]] == QFACT + 1]

    reps, cosets, elem_to_coset = left_cosets(elems, normalizer)
    orbits = double_coset_orbits(reps, elem_to_coset, forbidden)
    coset_to_orbit_size = {
        coset_id: len(orbit) for orbit in orbits for coset_id in orbit
    }

    orbital_12 = orbital_graph_parameters(
        reps, elem_to_coset, coset_to_orbit_size, target_orbit_size=K
    )
    orbital_32 = orbital_graph_parameters(
        reps, elem_to_coset, coset_to_orbit_size, target_orbit_size=2**5
    )

    tail_by_orbit_size_polarization_diameter = Counter()
    for matrix in tail:
        orbit_size = coset_to_orbit_size[elem_to_coset[matrix]]
        diameter = QFACT + 1 if matrix in forbidden_set else QFACT
        tail_by_orbit_size_polarization_diameter[
            (orbit_size, polarization_class(matrix), diameter)
        ] += 1

    group_distance_by_orbit_size = {}
    for orbit_size in sorted({len(orbit) for orbit in orbits}):
        members = [
            member
            for coset_id, coset in enumerate(cosets)
            if coset_to_orbit_size[coset_id] == orbit_size
            for member in coset
        ]
        group_distance_by_orbit_size[orbit_size] = dict(
            sorted(Counter(symmetric_dist[index[member]] for member in members).items())
        )

    checks = {
        "group_order_is_51840": len(elems) == GROUP_ORDER == 51_840,
        "normalizer_order_is_f4": len(normalizer) == F4_WEYL_ORDER == 1152,
        "index_is_45": len(cosets) == GROUP_ORDER // F4_WEYL_ORDER == 45,
        "double_coset_suborbits_are_1_12_32": sorted(len(orbit) for orbit in orbits)
        == [1, K, 2**5],
        "suborbit_sum_is_45": sum(len(orbit) for orbit in orbits) == 45,
        "orbital_12_is_regular_degree_12": orbital_12["degree_distribution"] == {K: 45},
        "orbital_12_is_srg_45_12_3_3": orbital_12["lambda_distribution"] == {3: 270}
        and orbital_12["mu_distribution"] == {3: 720},
        "orbital_12_edge_count_is_270": orbital_12["edge_count"] == 270,
        "orbital_32_is_complementary_regular": orbital_32["degree_distribution"] == {32: 45},
        "orbital_32_is_complement_srg": orbital_32["lambda_distribution"] == {22: 720}
        and orbital_32["mu_distribution"] == {24: 270},
        "tail_distribution_matches_rank3_split": tail_by_orbit_size_polarization_diameter
        == {
            (1, "anti", QFACT): 65,
            (1, "anti", QFACT + 1): 2**Q,
            (K, "mixed", QFACT): 4,
            (2**5, "mixed", QFACT): PHI12 + 1,
        },
        "outside_tail_still_dim_e6": (4 + PHI12 + 1) == DIM_E6,
        "identity_orbit_tail_is_phi12": 65 + 2**Q == PHI12,
    }

    return {
        "breakthrough": 167,
        "title": "F4 to E6 rank-3 coset quotient",
        "group_order": len(elems),
        "normalizer_order": len(normalizer),
        "index": len(cosets),
        "double_coset_suborbit_sizes": sorted(len(orbit) for orbit in orbits),
        "orbital_12_graph": orbital_12,
        "orbital_32_graph": orbital_32,
        "group_distance_by_orbit_size": group_distance_by_orbit_size,
        "tail_by_orbit_size_polarization_diameter": _counter_to_json(
            tail_by_orbit_size_polarization_diameter
        ),
        "architectural_reading": (
            "The forbidden-pocket F4 normalizer is an index-45 subgroup of the "
            "full compiler group. Its action on the 45 cosets has rank 3 with "
            "suborbits 1, 12, and 32; the valency-12 orbital graph is "
            "srg(45,12,3,3), the GQ(4,2) parameter profile. The macro tail "
            "lands on this quotient as Phi_12 in the identity/F4 cell, four "
            "mixed admissibles in the 12-cell, and Phi_12+1 mixed admissibles "
            "in the 32-cell. This proves the quotient structure while leaving "
            "canonical tritangent-plane labeling as a separate target."
        ),
        "boundary": (
            "Finite rank-3 coset quotient and SRG parameters are proved. "
            "No canonical identification with a named tritangent labeling is asserted here."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = f4_e6_rank3_coset_quotient_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 167: F4 -> E6 RANK-3 COSET QUOTIENT")
    print("=" * 78)
    print()
    print("COSET ACTION:")
    print(f"  |G|               = {packet['group_order']}")
    print(f"  |N_F4|            = {packet['normalizer_order']}")
    print(f"  index             = {packet['index']}")
    print(f"  suborbit sizes    = {packet['double_coset_suborbit_sizes']}")
    print()
    print("VALENCY-12 ORBITAL GRAPH:")
    print(f"  {packet['orbital_12_graph']}")
    print()
    print("TAIL INTERSECTION WITH RANK-3 QUOTIENT:")
    print(f"  {packet['tail_by_orbit_size_polarization_diameter']}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_167_f4_e6_rank3_coset_quotient.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")
    print(f"verified {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
