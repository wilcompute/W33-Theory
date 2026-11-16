"""Determine what torus reflection sectors measure in the E6 kinetic matrix."""

import json
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path

import sympy as sp

from toe_20261115_quiver_torus_charges import torus_cubic


DATA = Path(__file__).resolve().parents[1] / "data"


def character(label):
    i = 1 << (int(label[1]) - 1)
    if label[0] == "E":
        return i
    if label[0] == "Q":
        return 63 ^ i
    return 63 ^ i ^ (1 << (int(label[2]) - 1))


def infinitesimal_operator(entries, terms, transpose_sign):
    """Return the coefficient matrix of D_X N for elementary Lie generators."""
    rows = defaultdict(lambda: [0]*len(entries))
    for column, (i, j) in enumerate(entries):
        directions = [(i, j, 1)]
        if i != j:
            directions.append((j, i, transpose_sign))
        for source, target, multiplier in directions:
            for term, coefficient in terms.items():
                if source in term:
                    image = tuple(sorted([v for v in term if v != source] + [target]))
                    rows[image][column] += multiplier*coefficient
    return sp.Matrix(list(rows.values()))


def minimum_covers(requirements, limit):
    """Branch on a visible entry still lacking a reading."""
    requirements = sorted(set(requirements), key=lambda value: (value.bit_count(), value))
    for size in range(1, limit+1):
        visited = set()
        covers = set()

        def search(selected, remaining):
            if selected in visited:
                return
            visited.add(selected)
            missing = next((mask for mask in requirements if not (selected & mask)), 0)
            if not missing:
                covers.add(selected)
                return
            if remaining:
                while missing:
                    bit = missing & -missing
                    search(selected | bit, remaining-1)
                    missing ^= bit

        search(0, size)
        if covers:
            return covers
    raise ValueError("No cover within the certified bound")


def hidden_cubic_entries(generators, labels, chars, coverage):
    """Count nonzero cubic coefficients absent on every half-maximal fixed locus."""
    indices = {label: i for i, label in enumerate(labels)}
    character_indices = {char: i for i, char in enumerate(chars)}
    actions = {}
    retained = {}
    for charge, entries in generators.items():
        action = {}
        for left, right, sign in entries:
            i, j = indices[left], indices[right]
            action[i], action[j] = (j, sign), (i, sign)
        actions[charge] = action
        retained[charge] = sum(1 << sector for sector, reflection in enumerate(chars)
                               if (reflection & charge).bit_count() % 2 == 0)

    hidden = 0
    witness = None
    for charges in combinations(sorted(generators), 3):
        a, b, c = charges
        possible_sectors = retained[a] & retained[b] & retained[c]
        products = [tuple(actions[charge] for charge in order) for order in permutations(charges)]
        for i, character in enumerate(chars):
            j = character_indices.get(character ^ a ^ b ^ c, -1)
            if j < i or coverage[i, j] & possible_sectors:
                continue
            coefficient = 0
            for x, y, z in products:
                if i not in x:
                    continue
                first, sign_1 = x[i]
                if first not in y:
                    continue
                second, sign_2 = y[first]
                if second in z:
                    target, sign_3 = z[second]
                    assert target == j
                    coefficient += sign_1*sign_2*sign_3
            if coefficient:
                hidden += 1
                if witness is None:
                    witness = {
                        "scalar_characters": charges,
                        "matrix_entry": [labels[i], labels[j]],
                        "coefficient_in_exp_2X": str(sp.Rational(4*coefficient, 3)),
                    }
    assert hidden == 4320
    return {"count": hidden, "witness": witness}


def strong_section_readings(labels, chars, scalar_coverage):
    singular = set(chars)
    compatible = [
        {j for j, other in enumerate(chars) if other != char and (char ^ other) not in singular}
        for char in chars
    ]

    def extend(prefix, candidates):
        for offset, i in enumerate(candidates):
            section = prefix + (i,)
            yield section
            yield from extend(section, [j for j in candidates[offset+1:] if j in compatible[i]])

    profiles = Counter()
    maximal = Counter()
    sixes_by_blind_scalar = defaultdict(list)
    for section in extend((), list(range(len(labels)))):
        selected = sum(1 << i for i in section)
        blind = [c for c, needs in scalar_coverage.items() if not (needs & selected)]
        profile = len(section), len(blind)
        profiles[profile] += 1
        if not set.intersection(*(compatible[i] for i in section)):
            maximal[profile] += 1
        if len(section) == 6:
            assert len(blind) == 1
            sixes_by_blind_scalar[blind[0]].append(set(section))
    assert maximal == {(6, 1): 72, (5, 0): 216}
    assert {size for size, blind in profiles if blind == 0} == {5}
    assert len(sixes_by_blind_scalar) == 36
    for charge, sixes in sixes_by_blind_scalar.items():
        assert len(sixes) == 2 and not sixes[0] & sixes[1]
        assert sixes[0] | sixes[1] == {i for i, char in enumerate(chars) if (char & charge).bit_count() % 2 == 1}
    assert {labels[i] for i in sixes_by_blind_scalar[63][0] | sixes_by_blind_scalar[63][1]} == {
        label for label in labels if label.startswith(("E", "Q"))
    }
    return {
        "all_compatible_sets": [
            {"size": size, "unread_generators": blind, "count": count}
            for (size, blind), count in sorted(profiles.items())
        ],
        "maximal_compatible_sets": [
            {"size": size, "unread_generators": blind, "count": count}
            for (size, blind), count in sorted(maximal.items())
        ],
        "six_direction_sections_per_blind_character": 2,
    }


def verify():
    cubic = torus_cubic()
    labels = sorted(set().union(*cubic))
    index = {label: i for i, label in enumerate(labels)}
    terms = {tuple(sorted(index[label] for label in term)): value for term, value in cubic.items()}
    chars = [character(label) for label in labels]
    scalar_chars = set(range(1, 64)) - set(chars)
    assert len(scalar_chars) == 36 and len(set(chars)) == 27

    entries_by_charge = defaultdict(list)
    for i, j in combinations_with_replacement(range(27), 2):
        entries_by_charge[chars[i] ^ chars[j]].append((i, j))
    assert len(entries_by_charge[0]) == 27
    assert all(len(entries_by_charge[c]) == 5 for c in chars)
    assert all(len(entries_by_charge[c]) == 6 for c in scalar_chars)

    diagonal = infinitesimal_operator(entries_by_charge[0], terms, 1)
    torus_radii = sp.Matrix([
        [((-2 if label[0] == "Q" else 1)
          + (-3 if label[0] == "L" else 3)*int(str(i) in label[1:]))
         for i in range(1, 7)]
        for label in labels
    ])
    assert diagonal.rank() == 21
    assert torus_radii.rank() == 6 and diagonal * torus_radii == sp.zeros(diagonal.rows, 6)
    off_diagonal_generators = {}
    for charge in range(1, 64):
        entries = entries_by_charge[charge]
        symmetric = infinitesimal_operator(entries, terms, 1).nullspace()
        skew = infinitesimal_operator(entries, terms, -1).nullspace()
        if charge in scalar_chars:
            assert len(symmetric) == len(skew) == 1
            vector = symmetric[0] / symmetric[0][0]
            assert all(abs(value) == 1 for value in vector)
            off_diagonal_generators[charge] = [
                [labels[i], labels[j], int(value)] for (i, j), value in zip(entries, vector)
            ]
        else:
            assert not symmetric and not skew

    def fixed_vector_indices(reflection):
        return {i for i, char in enumerate(chars) if (char & reflection).bit_count() % 2 == 0}

    half_maximal = [fixed_vector_indices(reflection) for reflection in chars]
    assert all(len(indices) == 11 for indices in half_maximal)
    assert all(torus_radii[sorted(indices), :].rank() == 6 for indices in half_maximal)

    stu_vectors = set()
    for a, b, _ in terms:
        vectors = half_maximal[a] & half_maximal[b]
        assert tuple(sorted(vectors)) in terms
        assert torus_radii[sorted(vectors), :].rank() == 2
        assert sum((charge & chars[a]).bit_count() % 2 == (charge & chars[b]).bit_count() % 2 == 0
                   for charge in scalar_chars) == 12
        stu_vectors.add(tuple(sorted(vectors)))
    assert stu_vectors == terms.keys()
    stu_entries = {entry for vectors in stu_vectors for entry in combinations_with_replacement(vectors, 2)}
    assert len(stu_entries) == 162
    assert all(chars[i] ^ chars[j] not in scalar_chars for i, j in stu_entries)
    assert all((i, i) in stu_entries for i in range(27))

    coverage = {
        (i, j): sum(1 << sector for sector, indices in enumerate(half_maximal) if i in indices and j in indices)
        for entries in entries_by_charge.values() for i, j in entries
    }
    assert Counter(mask.bit_count() for mask in coverage.values()) == {11: 27, 3: 135, 5: 216}
    scalar_coverage = {}
    for charge in scalar_chars:
        counts = [sum(bool(coverage[entry] & (1 << sector)) for entry in entries_by_charge[charge])
                  for sector in range(27)]
        assert Counter(counts) == {0: 12, 2: 15}
        scalar_coverage[charge] = sum(1 << sector for sector, count in enumerate(counts) if count)
    requirements = list(scalar_coverage.values())
    triple_covers = {
        indices for indices in combinations(range(27), 3)
        if all(sum(1 << i for i in indices) & requirement for requirement in requirements)
    }
    assert triple_covers == terms.keys()
    tangent_covers = minimum_covers(requirements, 3)
    full_covers = minimum_covers(coverage.values(), 11)
    tangent_minimum = min(tangent_covers)
    full_minimum = min(full_covers)
    assert tangent_minimum.bit_count() == 3 and full_minimum.bit_count() == 11
    assert len(tangent_covers) == 45
    assert full_covers == {sum(1 << i for i in indices) for indices in half_maximal}
    cubic_invisibility = hidden_cubic_entries(off_diagonal_generators, labels, chars, coverage)
    strong_readings = strong_section_readings(labels, chars, scalar_coverage)

    return {
        "stu_kinetic_entries_covered": len(stu_entries),
        "stu_hidden_scalar_generators": len(off_diagonal_generators),
        "stu_visible_radial_generators": 6,
        "symmetric_generators_by_scalar_character": off_diagonal_generators,
        "radial_generators_times_three": {label: list(map(int, torus_radii.row(i))) for i, label in enumerate(labels)},
        "minimum_half_maximal_sectors_for_all_scalar_generators": 3,
        "minimum_triples_are_exactly_tritangents": len(triple_covers),
        "three_sector_witness": [label for i, label in enumerate(labels) if tangent_minimum & (1 << i)],
        "minimum_half_maximal_sectors_for_all_symmetric_entries": 11,
        "minimum_eleven_sector_covers_are_exactly_perp_sets": len(full_covers),
        "eleven_sector_witness": [label for i, label in enumerate(labels) if full_minimum & (1 << i)],
        "first_hidden_nonlinear_order": 3,
        "hidden_nonzero_cubic_entries": cubic_invisibility,
        "strong_section_compatible_readings": strong_readings,
    }


if __name__ == "__main__":
    path = DATA / "toe_20261115_torus_kinetic_reconstruction.json"
    path.write_text(json.dumps(verify(), indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified the STU kinetic obstruction, all 42 generators, and the optimal 3- and 11-sector covers")
