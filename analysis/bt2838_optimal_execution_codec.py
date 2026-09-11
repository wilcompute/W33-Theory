#!/usr/bin/env python3
"""Pass 2838: optimal execution storage and support non-lumpability."""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

State = tuple[int, int, int, int]


def support_mask(state: State) -> int:
    mask = 0
    for index, value in enumerate(state):
        if value:
            mask |= 1 << (3 - index)
    return mask


def phase_word(state: State) -> tuple[int, ...]:
    return tuple(value - 1 for value in state if value)


def decode_support_phase(mask: int, phase: tuple[int, ...]) -> State:
    assert len(phase) == mask.bit_count()
    cursor = iter(phase)
    return tuple(
        next(cursor) + 1 if mask & (1 << (3 - index)) else 0
        for index in range(4)
    )  # type: ignore[return-value]


def rank7(state: State) -> int:
    value = 0
    for trit in state:
        value = 3 * value + trit
    return value


def unrank7(code: int) -> State:
    assert 0 <= code < 81
    output = [0, 0, 0, 0]
    for index in range(3, -1, -1):
        output[index] = code % 3
        code //= 3
    return tuple(output)  # type: ignore[return-value]


def fp(state: State) -> State:
    xp, zp, xf, zf = state
    return ((-zp) % 3, xp, xf, zf)


def cx_pf(state: State) -> State:
    xp, zp, xf, zf = state
    return (xp, (zp - zf) % 3, (xf + xp) % 3, zf)


def cx_fp(state: State) -> State:
    xp, zp, xf, zf = state
    return ((xp + xf) % 3, zp, xf, (zf - zp) % 3)


def zp(state: State) -> State:
    xp, z, xf, zf = state
    return (xp, (z + 1) % 3, xf, zf)


OPS = {"F_p": fp, "CX_p_to_f": cx_pf, "CX_f_to_p": cx_fp, "Z_p": zp}


def groups(partition: dict[State, int]) -> set[frozenset[State]]:
    buckets: dict[int, set[State]] = defaultdict(set)
    for state, label in partition.items():
        buckets[label].add(state)
    return {frozenset(bucket) for bucket in buckets.values()}


def histogram(partition: dict[State, int]) -> dict[str, int]:
    sizes = Counter(Counter(partition.values()).values())
    return {str(size): count for size, count in sorted(sizes.items())}


def refine(states: list[State], partition: dict[State, int]) -> dict[State, int]:
    labels: dict[tuple[int, tuple[int, ...]], int] = {}
    output = {}
    for state in states:
        signature = (partition[state], tuple(partition[op(state)] for op in OPS.values()))
        output[state] = labels.setdefault(signature, len(labels))
    return output


def main() -> None:
    states = list(product(range(3), repeat=4))
    assert len(states) == 81
    for state in states:
        assert decode_support_phase(support_mask(state), phase_word(state)) == state
        assert unrank7(rank7(state)) == state
    assert {rank7(state) for state in states} == set(range(81))

    fibers = Counter(support_mask(state) for state in states)
    fiber_histogram = Counter(fibers.values())
    assert fiber_histogram == Counter({1: 1, 2: 4, 4: 6, 8: 4, 16: 1})

    partition = {state: support_mask(state) for state in states}
    counts, histograms = [], []
    while True:
        counts.append(len(set(partition.values())))
        histograms.append(histogram(partition))
        refined = refine(states, partition)
        if groups(refined) == groups(partition):
            break
        partition = refined
    assert counts == [16, 40, 78, 81]
    assert histograms == [
        {"1": 1, "2": 4, "4": 6, "8": 4, "16": 1},
        {"1": 7, "2": 29, "4": 4},
        {"1": 75, "2": 3},
        {"1": 81},
    ]

    left, right = (0, 1, 0, 0), (0, 2, 0, 0)
    assert support_mask(left) == support_mask(right) == 0b0100
    assert support_mask(zp(left)) == 0b0100
    assert support_mask(zp(right)) == 0b0000

    transitions = {
        name: [rank7(op(unrank7(code))) for code in range(81)]
        for name, op in OPS.items()
    }
    assert all(len(table) == 81 and all(0 <= value < 81 for value in table) for table in transitions.values())

    bits = math.ceil(math.log2(len(states)))
    assert bits == 7
    result = {
        "schema": "w33.pass2838.optimal_execution_codec.v1",
        "status": "COMPLETE_EXACT",
        "check_count": 7,
        "checks": {
            "support_phase_bijection_81": True,
            "rank7_bijection_81": True,
            "support_fiber_law": True,
            "refinement_16_40_78_81": True,
            "explicit_non_lumpability_witness": True,
            "seven_bit_lower_bound": True,
            "four_total_transition_tables": True,
        },
        "state_count": 81,
        "support_class_count": 16,
        "support_fiber_histogram": {str(key): value for key, value in sorted(fiber_histogram.items())},
        "support_phase_law": "fiber size = 2^support_weight; residual phase width = support_weight",
        "deterministic_refinement_counts": counts,
        "deterministic_refinement_histograms": histograms,
        "non_lumpability_witness": {
            "states": [list(left), list(right)],
            "shared_support": "0100",
            "operation": "Z_p",
            "next_supports": ["0100", "0000"],
        },
        "optimal_fixed_width_bits": bits,
        "rank_code_range": [0, 80],
        "unused_7bit_words": 47,
        "current_register_bits": 8,
        "potential_register_saving_bits": 1,
        "transition_table_entries": 81 * len(OPS),
        "transition_table_payload_bits": 81 * len(OPS) * bits,
        "claim_boundary": "Information-theoretic storage optimum only; synthesis and placement decide hardware merit."
    }
    out = Path(__file__).resolve().parents[1] / "data" / "PART_BT2838_OPTIMAL_EXECUTION_CODEC_results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS 7/7", counts, "optimal bits", bits)


if __name__ == "__main__":
    main()
