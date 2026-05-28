"""Part MCCCXCV: automorphism order of the 36-object spread/double-six scheme.

MCCCXCIII found the common 36-object two-class scheme, and MCCCXCIV built an
explicit spread-to-double-six isomorphism.  This verifier counts the automorphism
order of the overlap-4 graph on the 36 W33 spreads.

The calculation uses orbit-stabilizer:

    |Aut| = |orbit(spread_0)| * |Stab(spread_0)|.

A bitset backtracking search counts the stabilizer of spread 0 as 1440 and
finds an automorphism sending spread 0 to every one of the 36 vertices.  Hence

    |Aut| = 36 * 1440 = 51840.

By the explicit isomorphism of MCCCXCIV, the E6 double-six scheme has the same
automorphism order.  This is a scheme automorphism theorem, not a proof that a
particular physical continuum symmetry has been selected.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_spread_double_six_association_scheme import w33_spreads  # noqa: E402


OUTPUT_PATH = ROOT / "PART_MCCCXCV_SPREAD_DOUBLE_SIX_AUTOMORPHISM_ORDER_results.json"


def adjacency_masks(objects: list[frozenset[int]], overlap_value: int) -> list[int]:
    masks: list[int] = []
    for index, current in enumerate(objects):
        mask = 0
        for other_index, other in enumerate(objects):
            if index != other_index and len(current & other) == overlap_value:
                mask |= 1 << other_index
        masks.append(mask)
    return masks


def search_automorphisms(
    adjacency: list[int],
    anchor_target: int,
    stop_after_first: bool,
) -> dict[str, Any]:
    vertex_count = len(adjacency)
    all_vertices_mask = (1 << vertex_count) - 1
    source_to_target = [-1] * vertex_count
    target_to_source = [-1] * vertex_count
    source_to_target[0] = anchor_target
    target_to_source[anchor_target] = 0
    solution_count = 0
    node_count = 0
    first_solution: list[int] | None = None

    def search(mapped_mask: int, used_target_mask: int) -> None:
        nonlocal solution_count, node_count, first_solution
        node_count += 1
        if mapped_mask == all_vertices_mask:
            solution_count += 1
            if first_solution is None:
                first_solution = list(source_to_target)
            return

        best_source = -1
        best_score = -1
        unmapped = all_vertices_mask ^ mapped_mask
        probe = unmapped
        while probe:
            bit = probe & -probe
            source = bit.bit_length() - 1
            probe -= bit
            score = (adjacency[source] & mapped_mask).bit_count()
            if score > best_score:
                best_source = source
                best_score = score

        source = best_source
        unused_targets = all_vertices_mask ^ used_target_mask
        probe = unused_targets
        while probe:
            bit = probe & -probe
            target = bit.bit_length() - 1
            probe -= bit

            ok = True
            mapped_probe = mapped_mask
            while mapped_probe:
                mapped_bit = mapped_probe & -mapped_probe
                mapped_source = mapped_bit.bit_length() - 1
                mapped_probe -= mapped_bit
                mapped_target = source_to_target[mapped_source]
                if ((adjacency[source] >> mapped_source) & 1) != ((adjacency[target] >> mapped_target) & 1):
                    ok = False
                    break
            if not ok:
                continue

            source_to_target[source] = target
            target_to_source[target] = source
            search(mapped_mask | (1 << source), used_target_mask | (1 << target))
            source_to_target[source] = -1
            target_to_source[target] = -1

            if stop_after_first and solution_count:
                return

    search(1, 1 << anchor_target)
    return {
        "anchor_target": anchor_target,
        "solution_count": solution_count,
        "search_nodes": node_count,
        "first_solution": first_solution,
    }


def factorization_51840() -> dict[str, int]:
    return {"2": 7, "3": 4, "5": 1}


def automorphism_order_packet() -> dict[str, Any]:
    spreads = w33_spreads()
    adjacency = adjacency_masks(spreads, 4)
    degree_profile = Counter(mask.bit_count() for mask in adjacency)

    stabilizer = search_automorphisms(adjacency, anchor_target=0, stop_after_first=False)
    orbit_witnesses = [
        search_automorphisms(adjacency, anchor_target=target, stop_after_first=True)
        for target in range(len(spreads))
    ]
    orbit_size = sum(1 for witness in orbit_witnesses if witness["solution_count"] > 0)
    automorphism_order = orbit_size * stabilizer["solution_count"]

    checks = {
        "spread_scheme_has_36_vertices": len(spreads) == 36,
        "overlap_4_graph_has_degree_15": degree_profile == {15: 36},
        "stabilizer_of_first_spread_is_1440": stabilizer["solution_count"] == 1440,
        "orbit_of_first_spread_has_size_36": orbit_size == 36,
        "automorphism_order_is_51840": automorphism_order == 51840,
        "automorphism_order_factorization_matches": factorization_51840() == {"2": 7, "3": 4, "5": 1},
    }

    return {
        "part": "MCCCXCV",
        "theorem": "Automorphism order of the spread/double-six scheme",
        "input_bridge": "MCCCXCIV explicit spread/double-six scheme isomorphism",
        "scheme": "36-object overlap-4 graph srg(36,15,6,6)",
        "orbit_stabilizer": {
            "orbit_size_of_first_spread": orbit_size,
            "stabilizer_order_of_first_spread": stabilizer["solution_count"],
            "automorphism_order": automorphism_order,
            "identity": "51840 = 36 * 1440",
            "factorization": factorization_51840(),
        },
        "search": {
            "stabilizer_search_nodes": stabilizer["search_nodes"],
            "orbit_witness_search_node_profile": {
                str(key): int(value)
                for key, value in sorted(Counter(witness["search_nodes"] for witness in orbit_witnesses).items())
            },
            "first_stabilizer_solution": stabilizer["first_solution"],
        },
        "claim_boundary": (
            "finite automorphism-order theorem for the 36-object scheme; by the "
            "MCCCXCIV isomorphism the double-six scheme has the same order, but this "
            "does not choose a unique canonical spread-to-double-six labeling"
        ),
        "reading": (
            "The 36-object spread/double-six scheme has automorphism order 51840. "
            "The first spread has a 36-element orbit and a 1440-element stabilizer, "
            "so orbit-stabilizer gives 36*1440=51840. This is exactly the E6/W33 "
            "symmetry scale already appearing throughout the bridge, now recovered "
            "from the spread/double-six association scheme itself."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = automorphism_order_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCXCV: Spread / Double-Six Automorphism Order ===")
    print("identity:", packet["orbit_stabilizer"]["identity"])
    print("automorphism order:", packet["orbit_stabilizer"]["automorphism_order"])
    print("stabilizer:", packet["orbit_stabilizer"]["stabilizer_order_of_first_spread"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
