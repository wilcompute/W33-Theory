#!/usr/bin/env python3
"""Passes 7305--7306: C_spread intrinsically recovers the 36 double-sixes.

Pass7182/7184 constructed the binary spread code C_spread=[45,21,5] from
the 27 ten-D4 spreads.  Pass7225--7248 subsequently put 36 cubic-surface
double-six slices into that code as weight-15 words.  This producer proves
the converse, without using the double-sixes in the selection step.

Enumerate all 2^21 words of C_spread and let M5 be its 27-word minimum shell.
Among the 21,168 words x of weight 15, exactly 36 satisfy

    |{m in M5 : |supp(x) cap supp(m)|=0}| = 12,
    |{m in M5 : |supp(x) cap supp(m)|=3}| = 15.

There are no other intersection sizes for those 36 words.  The selected set
is exactly the 36 current disjoint-tritangent columns N[:,D].  Joining two
selected words when their supports meet in six coordinates reconstructs the
objectwise H36 graph, SRG(36,20,10,12); nonedges meet in three coordinates.

The selection uses only the abstract binary code together with its intrinsic
minimum shell.  Cubic-surface data enters afterward solely to identify the
selected 36-set with the already constructed double-six slices.
"""
from __future__ import annotations

import itertools
import json
import time
from collections import Counter
from pathlib import Path

import numpy as np

from w33_pass4992_4999_common import build_base
from w33_pass7225_7232_spread_code_doily_puncture import (
    center_data,
    coordinate_isomorphism,
    gf2_basis,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS7305_7306_CSPREAD_INTRINSIC_DOUBLE_SIX.json"

EXPECTED_WEIGHT_ENUMERATOR = {
    0: 1,
    5: 27,
    8: 135,
    10: 216,
    11: 1080,
    12: 1200,
    13: 3285,
    14: 10800,
    15: 21168,
    16: 33210,
    17: 59760,
    18: 117000,
    19: 167400,
    20: 167904,
    21: 193230,
    22: 272160,
    23: 272160,
    24: 193230,
    25: 167904,
    26: 167400,
    27: 117000,
    28: 59760,
    29: 33210,
    30: 21168,
    31: 10800,
    32: 3285,
    33: 1200,
    34: 1080,
    35: 216,
    37: 135,
    40: 27,
    45: 1,
}

EXPECTED_WEIGHT15_PROFILES = {
    ((0, 3), (1, 10), (2, 8), (3, 5), (4, 1)): 12960,
    ((1, 12), (2, 12), (3, 3)): 3240,
    ((0, 2), (1, 10), (2, 10), (3, 5)): 2592,
    ((0, 4), (1, 8), (2, 8), (3, 7)): 1620,
    ((0, 6), (1, 9), (2, 6), (3, 3), (5, 3)): 720,
    ((0, 12), (3, 15)): 36,
}

INTRINSIC_SELECTOR = ((0, 12), (3, 15))


def mask_from_coordinates(coordinates) -> int:
    mask = 0
    for coordinate in coordinates:
        mask |= 1 << int(coordinate)
    return mask


def column_masks(matrix) -> list[int]:
    rows, columns = matrix.shape
    return [
        sum((int(matrix[i, j]) & 1) << i for i in range(rows))
        for j in range(columns)
    ]


def enumerate_code(basis: list[int]):
    """Gray-enumerate a binary span while retaining only the two needed shells."""
    rank = len(basis)
    weight_enumerator: Counter[int] = Counter()
    minimum_words: list[int] = []
    weight15_words: list[int] = []
    word = 0
    previous_gray = 0
    for index in range(1 << rank):
        gray = index ^ (index >> 1)
        if index:
            changed = gray ^ previous_gray
            basis_index = (changed & -changed).bit_length() - 1
            word ^= basis[basis_index]
        previous_gray = gray

        weight = word.bit_count()
        weight_enumerator[weight] += 1
        if weight == 5:
            minimum_words.append(word)
        elif weight == 15:
            weight15_words.append(word)
    return weight_enumerator, minimum_words, weight15_words


def profile(word: int, minimum_words: list[int]):
    return tuple(sorted(Counter((word & m).bit_count() for m in minimum_words).items()))


def strongly_regular_parameters(words: list[int]):
    adjacency = [set() for _ in words]
    intersection_counts = Counter()
    for i, j in itertools.combinations(range(len(words)), 2):
        size = (words[i] & words[j]).bit_count()
        intersection_counts[size] += 1
        if size == 6:
            adjacency[i].add(j)
            adjacency[j].add(i)

    degrees = Counter(len(neighbors) for neighbors in adjacency)
    common_adjacent = Counter()
    common_nonadjacent = Counter()
    for i, j in itertools.combinations(range(len(words)), 2):
        common = len(adjacency[i] & adjacency[j])
        if j in adjacency[i]:
            common_adjacent[common] += 1
        else:
            common_nonadjacent[common] += 1
    return adjacency, intersection_counts, degrees, common_adjacent, common_nonadjacent


def main() -> int:
    started = time.perf_counter()
    base = build_base()

    # Independent Pass7182/7184 presentation: 27 ten-D4 spread words.
    supports, packs = center_data(base["W"])
    support_to_tritangent = coordinate_isomorphism(supports, base["tritangents"])
    spread_words = [
        mask_from_coordinates(support_to_tritangent[z] for z in pack)
        for pack in packs
    ]
    assert len(spread_words) == 27
    assert Counter(x.bit_count() for x in spread_words) == Counter({5: 27})
    basis = gf2_basis(spread_words)
    assert len(basis) == 21

    weight_enumerator, minimum_words, weight15_words = enumerate_code(basis)
    assert sum(weight_enumerator.values()) == 2**21
    assert dict(sorted(weight_enumerator.items())) == EXPECTED_WEIGHT_ENUMERATOR
    assert len(minimum_words) == 27
    assert set(minimum_words) == set(spread_words)
    assert len(weight15_words) == 21168

    profiles = Counter(profile(word, minimum_words) for word in weight15_words)
    assert profiles == Counter(EXPECTED_WEIGHT15_PROFILES)
    selected = sorted(word for word in weight15_words if profile(word, minimum_words) == INTRINSIC_SELECTOR)
    assert len(selected) == 36

    # Identification is deliberately downstream of the code-intrinsic selector.
    tritangents = base["tritangents"]
    double_sixes = base["DS"]
    N = np.zeros((45, 36), dtype=np.uint8)
    for t, tritangent in enumerate(tritangents):
        for d, double_six in enumerate(double_sixes):
            N[t, d] = int(set(tritangent).isdisjoint(double_six))
    N_columns = column_masks(N)
    assert Counter(x.bit_count() for x in N_columns) == Counter({15: 36})
    assert set(selected) == set(N_columns)

    # The intrinsic pair-intersection graph is exactly the current H36 labeling.
    adjacency, pair_intersections, degrees, lambdas, mus = strongly_regular_parameters(selected)
    assert pair_intersections == Counter({6: 360, 3: 270})
    assert degrees == Counter({20: 36})
    assert lambdas == Counter({10: 360})
    assert mus == Counter({12: 270})
    selected_index = {word: i for i, word in enumerate(selected)}
    for i, j in itertools.combinations(range(36), 2):
        intrinsic_edge = selected_index[N_columns[j]] in adjacency[selected_index[N_columns[i]]]
        assert intrinsic_edge == base["H36"].has_edge(i, j)

    profile_rows = [
        {
            "count": count,
            "minimum_shell_intersection_histogram": {str(k): v for k, v in signature},
        }
        for signature, count in sorted(profiles.items(), key=lambda item: (-item[1], item[0]))
    ]
    out = {
        "schema": "w33.pass7305_7306.cspread_intrinsic_double_six.v1",
        "status": "PASS",
        "passes": "7305-7306",
        "Cspread": {
            "parameters": "[45,21,5]_2",
            "construction": "span of the 27 ten-D4 spread words in canonical tritangent coordinates",
            "rank": 21,
            "enumerated_words": 2**21,
            "weight_enumerator": {str(k): v for k, v in sorted(weight_enumerator.items())},
            "minimum_shell_size": len(minimum_words),
            "minimum_shell_equals_27_spread_generators": True,
            "weight15_shell_size": len(weight15_words),
        },
        "weight15_minimum_shell_profiles": profile_rows,
        "intrinsic_selector": {
            "definition": "weight 15 and minimum-shell intersection histogram {0:12,3:15}",
            "selected_words": len(selected),
            "unique_profile_class_of_size_36": True,
            "uses_only_Cspread_and_its_minimum_shell": True,
        },
        "double_six_identification": {
            "current_N_columns": len(N_columns),
            "N_column_weight": 15,
            "selected_set_equals_current_N_columns": True,
            "meaning": "N[t,D]=1 iff tritangent t is disjoint from double-six D",
        },
        "intrinsic_pair_intersection_graph": {
            "adjacency_rule": "two selected words are adjacent iff support intersection has size 6",
            "pair_intersections": {"3": 270, "6": 360},
            "parameters": "SRG(36,20,10,12)",
            "degrees": {"20": 36},
            "adjacent_common_neighbors": {"10": 360},
            "nonadjacent_common_neighbors": {"12": 270},
            "equals_current_H36_objectwise_under_N_column_labels": True,
        },
        "theorem": (
            "The abstract code C_spread together with its intrinsic minimum shell canonically selects a 36-set "
            "of weight-15 words.  In the current tritangent realization this set is exactly the double-six slice "
            "family, and support intersection 6 reconstructs H36."
        ),
        "prior_art_boundary": {
            "Pass7182_7184": (
                "analysis/w33_pass7182_d4_glue_spread_code.py, "
                "analysis/BT7171_BT7186_e8_d4_h27_q9.md, and "
                "analysis/w33_pass7184_spread_code_v20_v24_module.py own the [45,21,5] spread code, its 27 "
                "minimum words, and the 1+V20 module statement."
            ),
            "Pass7225_7248": (
                "analysis/w33_pass7225_7232_spread_code_doily_puncture.py and "
                "analysis/w33_pass7241_7248_double_six_slice_generator.py own the external construction of the "
                "36 double-six slice words and the equality col(N)=C_spread."
            ),
            "new_here": (
                "The converse intrinsic characterization: the unique weight-15 profile {0:12,3:15} recovers "
                "exactly those 36 words from C_spread alone, and their pair intersections recover H36."
            ),
            "scope": "Exact finite coding/incidence theorem only; no physical interpretation is asserted.",
        },
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    elapsed = time.perf_counter() - started
    print(json.dumps({"status": "PASS", "enumerated_words": 2**21, "selected": 36, "seconds": round(elapsed, 3)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
