"""Classify coordinate Chern–Simons closures and torus-reflection sectors."""

import json
from collections import Counter
from itertools import combinations, combinations_with_replacement
from pathlib import Path

import networkx as nx

from toe_20261115_cubic_quiver_steiner import intersection, line_class
from toe_20261115_quiver_five_checks import simple_roots
from toe_20261115_quiver_torus_charges import torus_cubic


DATA = Path(__file__).resolve().parents[1] / "data"


def closure(mask, terms):
    while True:
        expanded = mask
        for term in terms:
            missing = term & ~expanded
            if missing.bit_count() == 1:
                expanded |= missing
        if expanded == mask:
            return expanded
        mask = expanded


def closed_supports(terms, coordinate_count):
    pending = [0]
    seen = {0}
    for state in pending:
        for coordinate in range(coordinate_count):
            if state & (1 << coordinate):
                continue
            image = closure(state | (1 << coordinate), terms)
            if image not in seen:
                seen.add(image)
                pending.append(image)
    return seen


def verify():
    cubic = torus_cubic()
    labels = sorted(set().union(*cubic))
    index = {label: i for i, label in enumerate(labels)}

    def mask(items):
        return sum(1 << index[label] for label in items)

    full = (1 << 27) - 1
    terms = [mask(term) for term in cubic]
    closed = closed_supports(terms, 27)
    maximal = {state for state in closed if state != full and all(
        state & (1 << i) or closure(state | (1 << i), terms) == full for i in range(27)
    )}
    maximal_counts = Counter(x.bit_count() for x in maximal)
    assert maximal_counts == {6: 72, 11: 27, 15: 36}
    assert len(closed) == 3668

    # Characters encode the effect of reflecting any subset of the 6 circles.
    directions = [1 << i for i in range(6)]
    orientation = (1 << 6) - 1
    vector_characters = {}
    for i, bit in enumerate(directions, start=1):
        vector_characters[f"E{i}"] = bit
        vector_characters[f"Q{i}"] = orientation ^ bit
    for i, j in combinations(range(1, 7), 2):
        vector_characters[f"L{i}{j}"] = orientation ^ directions[i-1] ^ directions[j-1]
    scalar_characters = [i ^ j for i, j in combinations_with_replacement(directions, 2)]
    scalar_characters += [orientation ^ i ^ j ^ k for i, j, k in combinations(directions, 3)]
    scalar_characters.append(orientation)
    characters = [vector_characters[label] for label in labels] + scalar_characters
    assert Counter(characters) == Counter({0: 6, **{i: 1 for i in range(1, 64)}})

    def quadratic(x):
        weight = x.bit_count()
        return (weight*(weight-1)//2) % 2

    assert {value for value in range(1, 64) if quadratic(value) == 0} == set(vector_characters.values())
    assert {term for term in combinations(labels, 3)
            if vector_characters[term[0]] ^ vector_characters[term[1]] ^ vector_characters[term[2]] == 0
            } == {tuple(sorted(term)) for term in cubic}

    fixed_by_reflection = [
        sum(1 << i for i, character in enumerate(characters) if (character & r).bit_count() % 2 == 0)
        for r in range(64)
    ]
    reflections = [(1 << len(characters)) - 1]
    fixed_fields = {reflections[0]: frozenset({0})}
    for state in reflections:
        subgroup = fixed_fields[state]
        for reflection, parity in enumerate(fixed_by_reflection):
            image = state & parity
            if image not in fixed_fields:
                fixed_fields[image] = subgroup | {old ^ reflection for old in subgroup}
                reflections.append(image)
    fixed_vectors = {state & full for state in fixed_fields}
    assert len(fixed_fields) == 2825 and len(fixed_vectors) == 1949
    assert fixed_vectors <= closed
    field_counts = Counter(((state & full).bit_count(), (state >> 27).bit_count()) for state in fixed_fields)
    assert field_counts[9, 12] == 120 and field_counts[11, 26] == 27 and field_counts[15, 22] == 36
    spin_counts = Counter()
    for state, subgroup in fixed_fields.items():
        assert state.bit_count() == 64//len(subgroup) + 5
        if all(quadratic(reflection) == 0 for reflection in subgroup):
            vectors = state & full
            profile = (vectors.bit_count(), (state >> 27).bit_count(), 32//len(subgroup))
            spin_counts[profile] += 1
            if len(subgroup) == 4:
                assert vectors in terms
    assert spin_counts == {(27, 42, 32): 1, (11, 26, 16): 27, (3, 18, 8): 45}

    classes = {label: line_class(label) for label in labels}
    by_class = {value: label for label, value in classes.items()}
    weyl_generators = []
    for root in simple_roots():
        weyl_generators.append([
            1 << index[by_class[tuple(x + intersection(classes[label], root)*r
                                     for x, r in zip(classes[label], root))]]
            for label in labels
        ])

    def weyl_orbit(seed):
        pending = [seed]
        seen = {seed}
        for current in pending:
            for action in weyl_generators:
                image = sum(step for i, step in enumerate(action) if current & (1 << i))
                if image not in seen:
                    seen.add(image)
                    pending.append(image)
        return seen

    momenta = mask(f"E{i}" for i in range(1, 7))
    pure_m2 = mask(label for label in labels if label.startswith("L"))
    # One reflected circle: 5 momenta, 5 cross M2 charges and a single M5 charge.
    one_reflection = fixed_by_reflection[32]
    assert (one_reflection & full).bit_count() == 11 and (one_reflection >> 27).bit_count() == 26
    assert fixed_by_reflection[63] & full == pure_m2
    representatives = {6: momenta, 11: one_reflection & full, 15: pure_m2}
    for size, seed in representatives.items():
        assert weyl_orbit(seed) == {state for state in maximal if state.bit_count() == size}
    assert {sum(term & seed == term for term in terms) for seed in representatives.values()} == {0, 5, 15}

    # Reflecting either triple, with parity on C3, retains the same cross M2 charges.
    cut_state = fixed_by_reflection[7] & fixed_by_reflection[56]
    cross = mask(f"L{i}{j}" for i in range(1, 4) for j in range(4, 7))
    assert cut_state & full == cross and (cut_state >> 27).bit_count() == 12
    cut_orbit = weyl_orbit(cross)
    assert cut_orbit == {state for state in fixed_vectors if state.bit_count() == 9}

    quiver = json.loads((DATA / "toe_20261115_cubic_quiver_steiner.json").read_text(encoding="utf-8"))
    indexed_terms = [mask(term) for term in quiver["tritangents_in_line_labels"]]
    block_masks = set()
    for text in quiver["orbit_supports_hex_masks"]:
        support = int(text, 16)
        graph = nx.Graph()
        for i, triple in enumerate(quiver["tritangents_in_line_labels"]):
            if not (support >> i & 1):
                graph.add_edges_from(combinations(triple, 2))
        blocks = [mask(component) for component in nx.connected_components(graph)]
        assert sorted(x.bit_count() for x in blocks) == [9, 9, 9]
        block_masks.update(blocks)
        for a, b in combinations(blocks, 2):
            retained = a | b
            sources = Counter(term & ~retained for term in indexed_terms if (term & retained).bit_count() == 2)
            assert len(sources) == 9 and set(sources.values()) == {3}
            assert sum(sources) == full ^ retained
    assert block_masks == cut_orbit and len(block_masks) == 120

    return {
        "closed_vector_supports_by_rank": dict(sorted(Counter(x.bit_count() for x in closed).items())),
        "maximal_proper_closed_supports": dict(sorted(maximal_counts.items())),
        "maximal_weyl_orbit_representatives": {
            size: [label for label in labels if state & (1 << index[label])]
            for size, state in representatives.items()
        },
        "sign_fixed_vector_supports": len(fixed_vectors),
        "combined_vector_scalar_reflection_sectors": [
            {"vectors": v, "scalars": s, "sectors": count} for (v, s), count in sorted(field_counts.items())
        ],
        "supersymmetric_flat_torus_reflection_sectors": [
            {"vectors": v, "scalars": s, "supercharges": q, "sectors": count}
            for (v, s, q), count in sorted(spin_counts.items())
        ],
        "rank_nine_quiver_blocks_that_are_consistent_bosonic_sectors": len(block_masks),
        "two_block_truncation_omitted_vectors_sourced": 9,
        "independent_cubic_terms_sourcing_each_omitted_vector": 3,
    }


if __name__ == "__main__":
    path = DATA / "toe_20261115_torus_cs_sectors.json"
    path.write_text(json.dumps(verify(), indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified the toroidal reflection sectors, maximal coordinate closures, and all quiver-block sources")
