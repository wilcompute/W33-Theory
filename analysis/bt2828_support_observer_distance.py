#!/usr/bin/env python3
"""Pass 2828: exact noisy-telemetry distance boundary for the support observer."""
from __future__ import annotations

import importlib.util
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "bt2825_2827_support_observer.py"
OUT = ROOT / "data" / "PART_BT2828_SUPPORT_OBSERVER_DISTANCE_results.json"

SPEC = importlib.util.spec_from_file_location("bt2825", SOURCE)
assert SPEC and SPEC.loader
BT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BT)


def flatten(trajectory):
    return tuple(bit for snapshot in trajectory for bit in snapshot)


def distance(left, right):
    return sum(a != b for a, b in zip(left, right))


def main() -> None:
    open_loop = BT.all_open_loop_words()
    words = []
    for named_word in open_loop["injective_length6_words"]:
        index_word = tuple(
            next(index for index, (name, _) in enumerate(BT.OPERATIONS) if name == operation)
            for operation in named_word
        )
        rows = [
            flatten(BT.support_trajectory(state, index_word))
            for state in BT.STATES
        ]
        histogram = Counter(
            distance(rows[left], rows[right])
            for left, right in combinations(range(len(rows)), 2)
        )
        words.append(
            {
                "word": named_word,
                "minimum_distance": min(histogram),
                "distance_one_pairs": histogram[1],
                "distance_histogram": {str(key): value for key, value in sorted(histogram.items())},
            }
        )

    assert [item["minimum_distance"] for item in words] == [1] * 8
    assert [item["distance_one_pairs"] for item in words] == [45, 36, 45, 45, 45, 36, 36, 36]

    result = {
        "schema": "w33.pass2828.support_observer_distance.v1",
        "status": "COMPLETE_EXACT",
        "check_count": 4,
        "checks": {
            "eight_shortest_words": len(words) == 8,
            "all_full_trajectory_distances_one": all(item["minimum_distance"] == 1 for item in words),
            "distance_one_pair_profile": [item["distance_one_pairs"] for item in words] == [45, 36, 45, 45, 45, 36, 36, 36],
            "no_single_bit_detection_guarantee": True,
        },
        "headline": "Every shortest injective support trajectory code has minimum distance one; exact observability does not supply single-bit error detection.",
        "words": words,
        "architecture_boundary": {
            "noiseless_identification": true,
            "single_arbitrary_bit_detection": false,
            "single_arbitrary_bit_correction": false,
            "required_next_layer": "repetition, longer/joint diagnostic words, checksum, or soft-decision decoding"
        }
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS 4/4")
    print(result["headline"])


if __name__ == "__main__":
    main()
