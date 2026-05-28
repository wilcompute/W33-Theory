"""Part MDCLXXXIII: Clifford antipodal A5 selector group.

MDCLXXXII showed that the raw Clifford L/R selector is a 36-block incidence
design on the 60 antipodal pairs of the 600-cell.  This verifier identifies
the hidden algebraic object behind that design.

Each antipodal address lies in exactly one cell of every L row and every R
column.  Therefore it is a permutation of the six L-fibrations onto the six
R-fibrations.  The 60 such permutations close under composition and have the
conjugacy/order profile of A5:

    1 identity, 15 order-2 elements, 20 order-3 elements, 24 order-5 elements.

Thus the raw Clifford selector is the degree-six action of the icosahedral
rotation group A5.  The remaining W33 selector problem is the transport from
this A5 torsor to the W33 spread scheme.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_clifford_antipodal_spread_incidence_bridge import antipodal_pair_index  # noqa: E402
from analysis.w33_clifford_lr_spread_scheme_boundary import clifford_lr_pairs  # noqa: E402


OUTPUT_PATH = ROOT / "PART_MDCLXXXIII_CLIFFORD_ANTIPODAL_A5_SELECTOR_GROUP_results.json"


Permutation = tuple[int, ...]


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Return left after right, as functions on {0,...,5}."""

    return tuple(left[right[index]] for index in range(len(right)))


def inverse(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def permutation_order(permutation: Permutation) -> int:
    identity = tuple(range(len(permutation)))
    current = identity
    for order in range(1, 13):
        current = compose(permutation, current)
        if current == identity:
            return order
    raise AssertionError(f"unexpected order for permutation {permutation}")


def parity(permutation: Permutation) -> int:
    return sum(
        1
        for left, right in combinations(range(len(permutation)), 2)
        if permutation[left] > permutation[right]
    ) % 2


def clifford_antipodal_permutations() -> dict[int, Permutation]:
    pair_index = antipodal_pair_index()
    pairs = clifford_lr_pairs()
    cell_supports: dict[int, list[tuple[int, int]]] = {address: [] for address in range(60)}

    for cell_index, pair in enumerate(pairs):
        row, column = divmod(cell_index, 6)
        for address in {pair_index[vertex] for vertex in pair["vertex_union"]}:
            cell_supports[address].append((row, column))

    permutations: dict[int, Permutation] = {}
    for address, support in cell_supports.items():
        rows = {row for row, _ in support}
        columns = {column for _, column in support}
        assert rows == set(range(6))
        assert columns == set(range(6))
        permutations[address] = tuple(column for _, column in sorted(support))

    return permutations


def two_transitivity_profile(permutations: set[Permutation]) -> Counter[int]:
    return Counter(
        sum(1 for permutation in permutations if permutation[source_1] == target_1 and permutation[source_2] == target_2)
        for source_1 in range(6)
        for source_2 in range(6)
        if source_2 != source_1
        for target_1 in range(6)
        for target_2 in range(6)
        if target_2 != target_1
    )


def cell_preimage_profile(permutations: set[Permutation]) -> Counter[int]:
    return Counter(
        sum(1 for permutation in permutations if permutation[row] == column)
        for row in range(6)
        for column in range(6)
    )


def fixed_point_profile(permutations: set[Permutation]) -> Counter[int]:
    return Counter(
        sum(1 for index, image in enumerate(permutation) if index == image)
        for permutation in permutations
    )


def clifford_antipodal_a5_selector_group_packet() -> dict[str, Any]:
    address_to_permutation = clifford_antipodal_permutations()
    permutations = set(address_to_permutation.values())
    identity = tuple(range(6))

    checks = {
        "there_are_60_distinct_permutations": len(address_to_permutation) == 60 and len(permutations) == 60,
        "identity_is_present": identity in permutations,
        "closed_under_composition": all(
            compose(left, right) in permutations for left in permutations for right in permutations
        ),
        "closed_under_inverse": all(inverse(permutation) in permutations for permutation in permutations),
        "all_permutations_are_even": Counter(parity(permutation) for permutation in permutations) == {0: 60},
        "order_profile_is_a5": Counter(permutation_order(permutation) for permutation in permutations)
        == {1: 1, 2: 15, 3: 20, 5: 24},
        "fixed_point_profile_matches_degree_6_a5": fixed_point_profile(permutations)
        == {6: 1, 2: 15, 0: 20, 1: 24},
        "action_is_two_transitive_with_two_lifts": two_transitivity_profile(permutations) == {2: 900},
        "each_lr_cell_has_10_group_elements": cell_preimage_profile(permutations) == {10: 36},
    }

    return {
        "part": "MDCLXXXIII",
        "theorem": "Clifford antipodal A5 selector group",
        "input_bridge": "MDCLXXXII Clifford antipodal / W33 spread incidence bridge",
        "selector_group_identity": "60 antipodal Clifford addresses = A5 in its degree-six action",
        "permutation_count": len(permutations),
        "order_profile": counter_to_json(Counter(permutation_order(permutation) for permutation in permutations)),
        "parity_profile": counter_to_json(Counter(parity(permutation) for permutation in permutations)),
        "fixed_point_profile": counter_to_json(fixed_point_profile(permutations)),
        "two_transitivity_profile": counter_to_json(two_transitivity_profile(permutations)),
        "cell_preimage_profile": counter_to_json(cell_preimage_profile(permutations)),
        "sample_address_permutations": {
            str(address): list(permutation)
            for address, permutation in list(sorted(address_to_permutation.items()))[:12]
        },
        "claim_boundary": (
            "identifies the raw Clifford antipodal selector as an A5 torsor; "
            "it does not yet construct the W33 spread selector"
        ),
        "reading": (
            "Every antipodal 600-cell address chooses one R-fibration in each "
            "of the six L rows, and every R-fibration is chosen once. Hence each "
            "address is a permutation of six letters. The 60 permutations close "
            "under composition, are all even, and have order profile 1,15,20,24 "
            "for orders 1,2,3,5, exactly the icosahedral rotation group A5. The "
            "L/R cells are the 36 action fibers i -> j, each containing 10 group "
            "elements. The raw Clifford selector is therefore an A5 degree-six "
            "torsor. The remaining selector problem is to twist this A5 torsor "
            "into the W33 spread association scheme."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = clifford_antipodal_a5_selector_group_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MDCLXXXIII: Clifford Antipodal A5 Selector Group ===")
    print("identity:", packet["selector_group_identity"])
    print("order profile:", packet["order_profile"])
    print("cell preimage profile:", packet["cell_preimage_profile"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} checks")


if __name__ == "__main__":
    main()
