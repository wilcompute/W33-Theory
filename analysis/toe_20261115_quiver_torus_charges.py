"""Match signed quiver tritangents and toroidal momentum, M2, and M5 charges."""

import json
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

from toe_20261115_cubic_quiver_steiner import ARROW_LINES, intersection, line_class
from toe_20261115_quiver_five_checks import simple_roots


DATA = Path(__file__).resolve().parents[1] / "data"


def inversion_sign(values):
    return (-1)**sum(a > b for a, b in combinations(values, 2))


def torus_cubic():
    """The integer Pfaffian and alternating M2–momentum–M5 contraction."""
    pairings = []

    def match(indices, pairs):
        if not indices:
            pairings.append(pairs)
            return
        a = indices[0]
        for b in indices[1:]:
            match(tuple(i for i in indices[1:] if i != b), pairs + ((a, b),))

    match(tuple(range(1, 7)), ())
    terms = {
        frozenset(f"L{a}{b}" for a, b in pairs): inversion_sign(tuple(i for pair in pairs for i in pair))
        for pairs in pairings
    }
    for i, j in combinations(range(1, 7), 2):
        terms[frozenset((f"L{i}{j}", f"E{i}", f"Q{j}"))] = 1
        terms[frozenset((f"L{i}{j}", f"E{j}", f"Q{i}"))] = -1
    return terms


def dickson_cubic():
    blocks = ("123", "456", "789")
    terms = {}
    for a, b in zip(blocks, blocks[1:] + blocks[:1]):
        for column_order in permutations(b):
            terms[frozenset(ARROW_LINES[x+y] for x, y in zip(a, column_order))] = inversion_sign(column_order)
    for a, b, c in product(*blocks):
        terms[frozenset(ARROW_LINES[x] for x in (a+b, b+c, c+a))] = -1
    return terms


def sign_changes(source, target):
    """Find a diagonal sign change matching two signed monomial supports."""
    assert source.keys() == target.keys()
    labels = sorted(set().union(*source))
    basis = {}
    for term in source:
        row = sum(1 << labels.index(label) for label in term)
        value = int(source[term] != target[term])
        while row:
            pivot = row.bit_length()-1
            if pivot not in basis:
                basis[pivot] = row, value
                break
            old_row, old_value = basis[pivot]
            row ^= old_row
            value ^= old_value
        if row == 0:
            assert value == 0
    solution = 0
    for pivot, (row, value) in sorted(basis.items()):
        solution |= (value ^ ((row & solution).bit_count() % 2)) << pivot
    signs = {label: (-1)**bool(solution & (1 << i)) for i, label in enumerate(labels)}
    assert all(source[t]*(-1)**sum(signs[label] == -1 for label in t) == target[t] for t in source)
    return signs


def verify():
    orbit = json.loads((DATA / "toe_20261115_cubic_quiver_steiner.json").read_text(encoding="utf-8"))
    recovery = json.loads((DATA / "toe_20261115_cubic_quiver_ovoid.json").read_text(encoding="utf-8"))
    tritangents = list(map(frozenset, orbit["tritangents_in_line_labels"]))
    support_masks = [int(mask, 16) for mask in orbit["orbit_supports_hex_masks"]]
    supports = [{term for i, term in enumerate(tritangents) if mask >> i & 1} for mask in support_masks]
    torus = torus_cubic()
    dickson = dickson_cubic()
    assert set(tritangents) == set(torus) == set(dickson)
    signs = sign_changes(dickson, torus)
    reference_double_six = sorted(f"{kind}{i}" for kind in ("E", "Q") for i in range(1, 7))
    ovoid = next(row["charts"] for row in recovery["ovoid_charts_by_double_six"]
                 if row["double_six"] == reference_double_six)

    cut_charts = []
    crossing_charge_sets = {}
    for rest in combinations(range(2, 7), 2):
        first = {1, *rest}
        cross = {f"L{i}{j}" for i, j in combinations(range(1, 7), 2) if (i in first) != (j in first)}
        omitted = set()
        for term in torus:
            m2 = {label for label in term if label.startswith("L")}
            if (len(m2) == 3 and m2 <= cross) or (len(m2) == 1 and m2.isdisjoint(cross)):
                omitted.add(term)
        assert len(omitted) == 18
        chart = supports.index(set(torus) - omitted)
        assert chart in ovoid
        retained = supports[chart]
        assert all(len(term & cross) == 1 for term in retained)
        assert all(len(term & cross) != 1 for term in omitted)
        assert sum(all(label.startswith("L") for label in term) for term in retained) == 9
        crossing_charge_sets[chart] = cross
        cut_charts.append({"half_with_direction_1": sorted(first), "chart": chart})
    assert {entry["chart"] for entry in cut_charts} == set(ovoid)

    labels = sorted(set().union(*torus))
    classes = {label: line_class(label) for label in labels}
    by_class = {value: label for label, value in classes.items()}
    signed_reflections = []
    for root in simple_roots():
        action = {label: by_class[tuple(x+intersection(value, root)*r for x, r in zip(value, root))]
                  for label, value in classes.items()}
        permuted = {frozenset(action[label] for label in term): value for term, value in torus.items()}
        correction = sign_changes(permuted, torus)
        signed_reflections.append({"root": root, "permutation": action,
                                   "negated_after_permutation": [label for label in labels if correction[label] == -1]})

    # Transport the momentum/M5 frame and crossing variables to all double-sixes.
    reference = frozenset(reference_double_six)
    frames = {reference: dict(zip(labels, labels))}
    queue = [reference]
    for current in queue:
        for reflection in signed_reflections:
            action = reflection["permutation"]
            image = frozenset(action[label] for label in current)
            if image not in frames:
                frames[image] = {label: action[target] for label, target in frames[current].items()}
                queue.append(image)
    expected = {frozenset(row["double_six"]): set(row["charts"]) for row in recovery["ovoid_charts_by_double_six"]}
    assert frames.keys() == expected.keys()
    chart_sections = {i: Counter() for i in range(40)}
    for frame, action in frames.items():
        chart_ids = set()
        for cross in crossing_charge_sets.values():
            image = frozenset(action[label] for label in cross)
            chart = supports.index({term for term in torus if len(term & image) == 1})
            chart_ids.add(chart)
            chart_sections[chart][image] += 1
        assert chart_ids == expected[frame]
    assert all(sorted(sections.values()) == [3, 3, 3] for sections in chart_sections.values())

    return {
        "charge_lattice_rank": len(labels),
        "momentum_m2_m5_charge_counts": [6, 15, 6],
        "pfaffian_monomials": sum(all(label.startswith("L") for label in term) for term in torus),
        "mixed_monomials": sum(any(label.startswith("E") for label in term) for term in torus),
        "negated_dickson_coordinates": [label for label in labels if signs[label] == -1],
        "standard_double_six_torus_cuts": cut_charts,
        "verified_torus_cut_frames": len(frames),
        "projected_cube_profile": {"pfaffian_terms": 9, "mixed_terms": 18},
        "distinct_crossing_charge_sets_per_chart": 3,
        "frames_per_chart_and_crossing_charge_set": 3,
        "signed_integral_lifts_of_simple_reflections": signed_reflections,
    }


if __name__ == "__main__":
    path = DATA / "toe_20261115_quiver_torus_charges.json"
    path.write_text(json.dumps(verify(), indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified the rank-27 torus charge dictionary, ten torus cuts, and six signed Weyl lifts")
