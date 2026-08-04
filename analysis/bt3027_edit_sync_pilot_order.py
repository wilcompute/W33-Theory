#!/usr/bin/env python3
"""Pass 3027: insertion/deletion indexing without another optical channel.

A cyclic phase word by itself cannot correct one insertion/deletion: adjacent rotations
always have edit distance two. The existing protocol already sends three distinct pilots
in the non-omitted slots, however, so their order supplies one of six symbols at no channel
cost. This file freezes and verifies a finite synchronization-string construction on that
pilot-order alphabet and its product with the omitted-slot word.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3027_EDIT_SYNC_PILOT_ORDER_results.json"
OMITTED = (1,0,2,3,3,2,0,0,1,1,2,3)
PILOT_ORDER = (1,2,4,5,2,3,0,2,1,5,4,1)
PERMUTATIONS = tuple(itertools.permutations((0,1,2)))


def lcs_length(left, right):
    previous = [0] * (len(right) + 1)
    for symbol in left:
        current = [0]
        for index, other in enumerate(right, 1):
            current.append(previous[index-1] + 1 if symbol == other else max(previous[index], current[-1]))
        previous = current
    return previous[-1]


def insertion_deletion_distance(left, right):
    return len(left) + len(right) - 2 * lcs_length(left, right)


def levenshtein(left, right):
    previous = list(range(len(right)+1))
    for i, symbol in enumerate(left, 1):
        current = [i]
        for j, other in enumerate(right, 1):
            current.append(min(previous[j]+1, current[j-1]+1, previous[j-1]+(symbol != other)))
        previous = current
    return previous[-1]


def synchronization_score(sequence):
    """Minimum ED(left,right)/(combined length) over adjacent nonempty intervals."""
    minimum = 1.0
    witness = None
    for begin in range(len(sequence)):
        for middle in range(begin+1, len(sequence)):
            for end in range(middle+1, len(sequence)+1):
                distance = insertion_deletion_distance(sequence[begin:middle], sequence[middle:end])
                ratio = distance / (end-begin)
                if ratio < minimum:
                    minimum = ratio
                    witness = (begin, middle, end, distance)
    return minimum, witness


def shifts(sequence):
    return [sequence[offset:] + sequence[:offset] for offset in range(len(sequence))]


def main():
    omitted_shifts = shifts(OMITTED)
    cyclic_hamming = min(
        sum(a != b for a, b in zip(omitted_shifts[i], omitted_shifts[j]))
        for i in range(12) for j in range(i+1,12)
    )
    cyclic_levenshtein = min(
        levenshtein(omitted_shifts[i], omitted_shifts[j])
        for i in range(12) for j in range(i+1,12)
    )
    assert cyclic_hamming == 9
    assert cyclic_levenshtein == 2

    pilot_score, pilot_witness = synchronization_score(PILOT_ORDER)
    combined = tuple((OMITTED[i], PILOT_ORDER[i]) for i in range(12))
    combined_score, combined_witness = synchronization_score(combined)
    assert abs(pilot_score - 0.5) < 1e-12
    assert abs(combined_score - 0.6) < 1e-12
    assert all(0 <= code < 6 for code in PILOT_ORDER)

    schedule = []
    for tick, (omitted, code) in enumerate(zip(OMITTED, PILOT_ORDER)):
        open_slots = [slot for slot in range(4) if slot != omitted]
        assignment = {str(slot): pilot for slot, pilot in zip(open_slots, PERMUTATIONS[code])}
        schedule.append({"tick":tick,"omitted_slot":omitted,"pilot_permutation_code":code,"slot_to_pilot":assignment})

    payload = {
        "schema": "w33.pass3027.edit_aware_pilot_order_sync.v1",
        "status": "COMPLETE_EXACT_FINITE_SYNCHRONIZATION_CONSTRUCTION",
        "omitted_slot_word": list(OMITTED),
        "substitution_metric": {
            "cyclic_hamming_distance": cyclic_hamming,
            "correctable_substitutions": 4,
        },
        "single_block_edit_obstruction": {
            "minimum_cyclic_levenshtein_distance": cyclic_levenshtein,
            "theorem": "Every nonconstant cyclic word has adjacent rotations related by one deletion and one insertion, so a single isolated cyclic block cannot uniquely correct one insertion/deletion phase error.",
        },
        "pilot_order_word": list(PILOT_ORDER),
        "pilot_order_permutations": [list(row) for row in PERMUTATIONS],
        "pilot_order_synchronization_score": pilot_score,
        "pilot_order_witness": pilot_witness,
        "combined_omission_order_synchronization_score": combined_score,
        "combined_witness": combined_witness,
        "finite_synchronization_epsilon": 1-combined_score,
        "tick_schedule": schedule,
        "extra_optical_channels": 0,
        "design_decision": "Use omitted-slot identity for substitution protection and the ordering of the same three pilots as the insertion/deletion indexing alphabet.",
        "claim_boundary": "Exact finite length-12 insertion/deletion separation score. It is not an asymptotic synchronization-string construction and does not yet include measured optical edit rates or a streaming list-decoder benchmark.",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":payload["status"],"pilot_score":pilot_score,"combined_score":combined_score}, sort_keys=True))


if __name__ == "__main__":
    main()
