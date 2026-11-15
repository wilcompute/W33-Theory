"""Check Fermat residue characters and the symmetric gauge-pair channels."""

import json
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path


def verify():
    coordinates = range(4)
    pairs = [frozenset(pair) for pair in combinations(coordinates, 2)]
    weights = {pair: tuple(1+int(i in pair) for i in coordinates) for pair in pairs}
    pair_products = list(combinations_with_replacement(pairs, 2))
    counts = Counter()
    product_weights = {}
    for left, right in pair_products:
        weight = tuple((a+b) % 3 for a, b in zip(weights[left], weights[right]))
        kind = "same" if left == right else "complement" if not left & right else "overlap"
        counts[kind, weight] += 1
        product_weights[frozenset((left, right))] = weight
    same = {weight for kind, weight in counts if kind == "same"}
    cross = {weight for kind, weight in counts if kind == "overlap"}
    projective = {tuple((int(i == a)-int(i == b)) % 3 for i in coordinates)
                  for a, b in permutations(coordinates, 2)}
    assert same == set(weights.values()) and cross == projective
    assert len(same) == 6 and len(cross) == 12 and not same & cross
    assert counts["complement", (0, 0, 0, 0)] == 3
    assert all(value == 1 for (kind, _), value in counts.items() if kind != "complement")

    for family in (same, cross):
        seed = next(iter(family))
        assert {tuple(seed[i] for i in p) for p in permutations(coordinates)} == family
    partitions = [frozenset((left, right)) for left, right in pair_products if not left & right]
    actions = set()
    for perm in permutations(coordinates):
        action = tuple(partitions.index(frozenset(frozenset(perm[i] for i in pair) for pair in part))
                       for part in partitions)
        actions.add(action)
    assert len(actions) == 6

    # Verify the stabilizer fixing the nonzero labels acts trivially on
    # the corresponding pair product, just as on a projective off-diagonal function.
    for product, weight in product_weights.items():
        if weight not in cross:
            continue
        for perm in permutations(coordinates):
            if all(weight[perm[i]] == weight[i] for i in coordinates):
                assert frozenset(frozenset(perm[i] for i in pair) for pair in product) == product

    return {
        "fermat_diagonal_group_order": 27,
        "primitive_residue_dimension": len(weights),
        "symmetric_pair_dimensions": [1, 2, len(same), len(cross)],
        "off_diagonal_projective_character_matches": len(projective),
        "forced_neutral_massive_eigenspace_multiplicity_lower_bound": 12,
        "diagonal_projective_standard_triplet_overlap": 0,
    }


if __name__ == "__main__":
    report = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261115_fermat_betti_selection.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
