#!/usr/bin/env python3
"""Passes 2825-2827: support-only observer and telemetry decoder.

The binary support shell is not an execution quotient, but it is observable.
This script proves two exact forms:

1. Adaptive/all-word observability index 3:
   16 -> 40 -> 78 -> 81 refinement classes.
2. Fixed open-loop observability index 6:
   no instruction word of length <=5 gives an injective support trajectory,
   while exactly eight words of length 6 do.

For the canonical six-operation diagnostic word, eight sampled support bits are
necessary and sufficient to identify all 81 ternary frame states.  There are
exactly 48 minimal eight-tap selectors.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT2825_BT2827_SUPPORT_OBSERVER_results.json"

Vector = tuple[int, int, int, int]
Mask = tuple[int, int, int, int]
Matrix = tuple[tuple[int, int, int, int], ...]
Operation = Callable[[Vector], Vector]

COORDINATES = ("x_p", "z_p", "x_f", "z_f")

F_P: Matrix = (
    (0, 2, 0, 0),
    (1, 0, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
)
CX_PF: Matrix = (
    (1, 0, 0, 0),
    (0, 1, 0, 2),
    (1, 0, 1, 0),
    (0, 0, 0, 1),
)
CX_FP: Matrix = (
    (1, 0, 1, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 2, 0, 1),
)


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(matrix[row][col] * vector[col] for col in range(4)) % 3
        for row in range(4)
    )  # type: ignore[return-value]


def z_p(vector: Vector) -> Vector:
    return (vector[0], (vector[1] + 1) % 3, vector[2], vector[3])


OPERATIONS: tuple[tuple[str, Operation], ...] = (
    ("F_p", lambda vector: matvec(F_P, vector)),
    ("CX_p->f", lambda vector: matvec(CX_PF, vector)),
    ("CX_f->p", lambda vector: matvec(CX_FP, vector)),
    ("Z_p", z_p),
)
STATES: tuple[Vector, ...] = tuple(product(range(3), repeat=4))


def support(vector: Vector) -> Mask:
    return tuple(int(value != 0) for value in vector)  # type: ignore[return-value]


def apply_word(vector: Vector, word: tuple[int, ...]) -> Vector:
    for operation in word:
        vector = OPERATIONS[operation][1](vector)
    return vector


def support_trajectory(vector: Vector, word: tuple[int, ...]) -> tuple[Mask, ...]:
    result = [support(vector)]
    for operation in word:
        vector = OPERATIONS[operation][1](vector)
        result.append(support(vector))
    return tuple(result)


def canonical_groups(partition: dict[Vector, int | Mask]) -> set[frozenset[Vector]]:
    groups: dict[int | Mask, set[Vector]] = defaultdict(set)
    for state, label in partition.items():
        groups[label].add(state)
    return {frozenset(group) for group in groups.values()}


def class_histogram(partition: dict[Vector, int | Mask]) -> dict[str, int]:
    return {
        str(size): count
        for size, count in sorted(
            Counter(map(len, canonical_groups(partition))).items()
        )
    }


def unresolved_pairs(partition: dict[Vector, int | Mask]) -> int:
    return sum(len(group) * (len(group) - 1) // 2 for group in canonical_groups(partition))


def refine(partition: dict[Vector, int | Mask]) -> dict[Vector, int]:
    signatures: dict[tuple[int | Mask, tuple[int | Mask, ...]], int] = {}
    result: dict[Vector, int] = {}
    for state in STATES:
        signature = (
            partition[state],
            tuple(partition[operation(state)] for _, operation in OPERATIONS),
        )
        result[state] = signatures.setdefault(signature, len(signatures))
    return result


def adaptive_observer() -> dict:
    partition: dict[Vector, int | Mask] = {state: support(state) for state in STATES}
    class_counts: list[int] = []
    histograms: list[dict[str, int]] = []
    unresolved: list[int] = []
    partitions: list[dict[Vector, int | Mask]] = []

    while True:
        partitions.append(partition)
        class_counts.append(len(set(partition.values())))
        histograms.append(class_histogram(partition))
        unresolved.append(unresolved_pairs(partition))
        next_partition = refine(partition)
        if canonical_groups(next_partition) == canonical_groups(partition):
            break
        partition = next_partition

    assert class_counts == [16, 40, 78, 81]
    assert unresolved == [272, 53, 3, 0]
    total_pairs = len(STATES) * (len(STATES) - 1) // 2
    resolved_by_depth = [
        total_pairs - unresolved[0],
        unresolved[0] - unresolved[1],
        unresolved[1] - unresolved[2],
        unresolved[2] - unresolved[3],
    ]
    assert resolved_by_depth == [2968, 219, 50, 3]

    penultimate = [
        sorted(group)
        for group in canonical_groups(partitions[-2])
        if len(group) == 2
    ]
    penultimate.sort()
    expected_pairs = [
        [(0, 0, 1, 0), (0, 0, 2, 0)],
        [(0, 0, 1, 1), (0, 0, 2, 1)],
        [(0, 0, 1, 2), (0, 0, 2, 2)],
    ]
    assert penultimate == expected_pairs

    distinguishing_words: list[list[str]] = []
    common_words: set[tuple[int, ...]] | None = None
    for pair in penultimate:
        words = {
            word
            for word in product(range(4), repeat=3)
            if support(apply_word(pair[0], word))
            != support(apply_word(pair[1], word))
        }
        common_words = words if common_words is None else common_words & words
    assert common_words is not None
    assert len(common_words) == 3
    for word in sorted(common_words):
        distinguishing_words.append([OPERATIONS[index][0] for index in word])

    return {
        "class_counts": class_counts,
        "class_size_histograms": histograms,
        "unresolved_pair_counts": unresolved,
        "newly_resolved_pair_counts": resolved_by_depth,
        "adaptive_observability_index": 3,
        "penultimate_residual_pairs": [
            [list(pair[0]), list(pair[1])] for pair in penultimate
        ],
        "common_length3_distinguishing_words": distinguishing_words,
    }


def all_open_loop_words(max_length: int = 6) -> dict:
    best_counts: list[int] = []
    injective_words: list[tuple[int, ...]] = []

    for length in range(1, max_length + 1):
        best = 0
        current_injective: list[tuple[int, ...]] = []
        for word in product(range(4), repeat=length):
            count = len({support_trajectory(state, word) for state in STATES})
            best = max(best, count)
            if count == len(STATES):
                current_injective.append(word)
        best_counts.append(best)
        if current_injective:
            injective_words = current_injective
            break

    assert best_counts == [25, 40, 45, 68, 77, 81]
    assert len(injective_words) == 8

    named_words = [
        [OPERATIONS[index][0] for index in word] for word in injective_words
    ]
    canonical_word = injective_words[0]
    assert named_words[0] == [
        "CX_p->f",
        "F_p",
        "Z_p",
        "F_p",
        "Z_p",
        "CX_p->f",
    ]

    return {
        "best_distinct_trajectories_by_word_length": best_counts,
        "fixed_word_observability_index": 6,
        "injective_length6_word_count": len(injective_words),
        "injective_length6_words": named_words,
        "canonical_word_indices": list(canonical_word),
        "canonical_word": named_words[0],
    }


def flatten_trajectory(trajectory: tuple[Mask, ...]) -> tuple[int, ...]:
    return tuple(bit for snapshot in trajectory for bit in snapshot)


def tap_name(column: int) -> dict[str, int | str]:
    return {"time": column // 4, "coordinate": COORDINATES[column % 4]}


def minimal_taps(canonical_word: tuple[int, ...]) -> dict:
    rows = [
        flatten_trajectory(support_trajectory(state, canonical_word))
        for state in STATES
    ]
    assert len(rows[0]) == 28
    assert len(set(rows)) == 81

    state_pairs = tuple(combinations(range(len(STATES)), 2))
    full_cover = (1 << len(state_pairs)) - 1
    column_covers: list[int] = []
    for column in range(28):
        cover = 0
        for pair_index, (left, right) in enumerate(state_pairs):
            if rows[left][column] != rows[right][column]:
                cover |= 1 << pair_index
        column_covers.append(cover)

    seven_tap_count = 0
    for selector in combinations(range(28), 7):
        cover = 0
        for column in selector:
            cover |= column_covers[column]
        if cover == full_cover:
            seven_tap_count += 1
    assert seven_tap_count == 0

    eight_tap_selectors: list[tuple[int, ...]] = []
    for selector in combinations(range(28), 8):
        cover = 0
        for column in selector:
            cover |= column_covers[column]
        if cover == full_cover:
            eight_tap_selectors.append(selector)
    assert len(eight_tap_selectors) == 48

    canonical_selector = eight_tap_selectors[0]
    assert canonical_selector == (0, 1, 2, 5, 13, 21, 25, 26)
    selected_codes = {
        tuple(rows[state_index][column] for column in canonical_selector): STATES[state_index]
        for state_index in range(81)
    }
    assert len(selected_codes) == 81

    mandatory = set.intersection(*(set(selector) for selector in eight_tap_selectors))
    assert mandatory == {1, 2, 21, 25, 26}
    assert all(column % 4 != 3 for selector in eight_tap_selectors for column in selector)

    lookup = [
        {
            "code": "".join(str(rows[index][column]) for column in canonical_selector),
            "state": list(state),
        }
        for index, state in enumerate(STATES)
    ]
    assert len({item["code"] for item in lookup}) == 81

    return {
        "raw_support_trace_bits": 28,
        "information_lower_bound_bits": 7,
        "minimal_tap_count": 8,
        "seven_tap_selector_count": seven_tap_count,
        "minimal_eight_tap_selector_count": len(eight_tap_selectors),
        "canonical_selector_columns": list(canonical_selector),
        "canonical_selector_taps": [tap_name(column) for column in canonical_selector],
        "mandatory_columns": sorted(mandatory),
        "mandatory_taps": [tap_name(column) for column in sorted(mandatory)],
        "z_f_taps_required": False,
        "lookup_table": lookup,
    }


def build_result() -> dict:
    adaptive = adaptive_observer()
    open_loop = all_open_loop_words()
    canonical_word = tuple(open_loop["canonical_word_indices"])
    telemetry = minimal_taps(canonical_word)

    checks = {
        "adaptive_profile_16_40_78_81": adaptive["class_counts"] == [16, 40, 78, 81],
        "adaptive_index_3": adaptive["adaptive_observability_index"] == 3,
        "residual_pairs_exactly_3": len(adaptive["penultimate_residual_pairs"]) == 3,
        "three_common_length3_words": len(adaptive["common_length3_distinguishing_words"]) == 3,
        "no_fixed_word_through_length5": open_loop["best_distinct_trajectories_by_word_length"][:5] == [25, 40, 45, 68, 77],
        "fixed_word_index_6": open_loop["fixed_word_observability_index"] == 6,
        "eight_minimal_diagnostic_words": open_loop["injective_length6_word_count"] == 8,
        "eight_taps_minimal": telemetry["minimal_tap_count"] == 8,
        "forty_eight_minimal_tap_sets": telemetry["minimal_eight_tap_selector_count"] == 48,
        "no_zf_sensor_needed": telemetry["z_f_taps_required"] is False,
        "lookup_has_81_codes": len(telemetry["lookup_table"]) == 81,
    }
    assert all(checks.values())

    return {
        "schema": "w33.pass2825_2827.support_observer.v1",
        "status": "COMPLETE_EXACT",
        "check_count": len(checks),
        "checks": checks,
        "headline": (
            "Binary support is a finite-delay observer for the full ternary frame: "
            "adaptive depth 3, fixed open-loop word length 6, and eight sampled "
            "support bits suffice to recover all 81 states."
        ),
        "adaptive_observer": adaptive,
        "open_loop_observer": open_loop,
        "telemetry_decoder": telemetry,
        "architecture": {
            "internal_state": "four ternary frame coordinates",
            "external_telemetry": "binary support only",
            "diagnostic_cycles": 6,
            "support_snapshots": 7,
            "raw_trace_bits": 28,
            "minimal_sampled_bits": 8,
            "decoder_entries": 81,
            "claim_boundary": (
                "exact noiseless state identification; no noisy-channel robustness "
                "or laboratory readout fidelity is claimed"
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-frozen", action="store_true")
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.verify_frozen:
        if OUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"frozen certificate drift: {OUT}")
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(f"PASS {result['check_count']}/{result['check_count']}")
    print(result["headline"])


if __name__ == "__main__":
    main()
