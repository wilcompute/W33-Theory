#!/usr/bin/env python3
"""Pass 2828: concatenate shortest support observers to obtain distance four."""
from __future__ import annotations

import importlib.util
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "bt2825_2827_support_observer.py"
OUT = ROOT / "data" / "PART_BT2828_DOUBLE_WORD_DISTANCE4_results.json"

SPEC = importlib.util.spec_from_file_location("bt2825", SOURCE)
assert SPEC and SPEC.loader
BT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BT)


def flatten(trajectory):
    return tuple(bit for snapshot in trajectory for bit in snapshot)


def hamming(left, right):
    return sum(a != b for a, b in zip(left, right))


def trajectory_distance(word):
    rows = [flatten(BT.support_trajectory(state, word)) for state in BT.STATES]
    histogram = Counter(
        hamming(rows[left], rows[right])
        for left, right in combinations(range(len(rows)), 2)
    )
    return min(histogram), histogram


def main() -> None:
    open_loop = BT.all_open_loop_words()
    name_to_index = {name: index for index, (name, _) in enumerate(BT.OPERATIONS)}
    short_words = [
        tuple(name_to_index[name] for name in named_word)
        for named_word in open_loop["injective_length6_words"]
    ]

    pair_records = []
    for first, second in product(range(8), repeat=2):
        word = short_words[first] + short_words[second]
        minimum, histogram = trajectory_distance(word)
        pair_records.append(
            {
                "first_word_index": first,
                "second_word_index": second,
                "word": [BT.OPERATIONS[index][0] for index in word],
                "minimum_distance": minimum,
                "nearest_pair_count": histogram[minimum],
            }
        )

    distance_profile = Counter(item["minimum_distance"] for item in pair_records)
    assert distance_profile == Counter({2: 40, 3: 16, 4: 8})

    distance4 = [item for item in pair_records if item["minimum_distance"] == 4]
    assert len(distance4) == 8
    expected_pairs = [(0, 5), (0, 6), (1, 2), (1, 3), (4, 5), (4, 6), (7, 2), (7, 3)]
    assert sorted(
        (item["first_word_index"], item["second_word_index"])
        for item in distance4
    ) == expected_pairs

    canonical = next(
        item
        for item in distance4
        if (item["first_word_index"], item["second_word_index"]) == (0, 5)
    )
    assert canonical["nearest_pair_count"] == 18

    result = {
        "schema": "w33.pass2828.double_word_distance4.v1",
        "status": "COMPLETE_EXACT",
        "check_count": 6,
        "checks": {
            "eight_shortest_seed_words": len(short_words) == 8,
            "ordered_pair_count_64": len(pair_records) == 64,
            "distance_profile_40_16_8": distance_profile == Counter({2: 40, 3: 16, 4: 8}),
            "eight_distance4_words": len(distance4) == 8,
            "canonical_distance4": canonical["minimum_distance"] == 4,
            "canonical_nearest_pairs_18": canonical["nearest_pair_count"] == 18,
        },
        "headline": "Eight concatenations of shortest support observers yield a 12-operation, 52-bit trajectory code of minimum distance four.",
        "ordered_pair_distance_profile": {str(key): value for key, value in sorted(distance_profile.items())},
        "distance4_words": distance4,
        "canonical": canonical,
        "coding_consequence": {
            "trajectory_bits": 52,
            "minimum_distance": 4,
            "guaranteed_detection_bits": 3,
            "guaranteed_correction_bits": 1,
            "decoder": "nearest-neighbor over 81 exact codewords",
        },
        "claim_boundary": "Optimal only inside the 8x8 concatenation family of shortest injective words; no global shortest distance-four theorem is claimed."
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS 6/6")
    print(result["headline"])


if __name__ == "__main__":
    main()
