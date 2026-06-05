"""W(3,3) BREAKTHROUGH 286: e-cube coordinate selector atlas.

BT285 showed that the standard LSB-first e-cube pivot convention selects
BT273 selector 7.  BT286 classifies every coordinate-conjugate e-cube
convention.

Start with the binary-reflected e-cube word on Q4.  Its cap-deleted internal
q-word is

    [1^4, 1^2, 1^8] = [5,3,9].

Conjugate the four coordinate bits {1,2,4,8} by all 4! = 24 permutations.
Exactly eight conjugates produce a prefix word in the BT273 selector atlas.
Those eight conjugates are exactly the coordinate permutations preserving the
two-pair partition

    {{1,2}, {4,8}},

possibly swapping the two pairs.  This group has order

    (2!)^2 * 2! = 8 = 2^q.

The eight selected conjugates hit the eight BT273 selectors exactly once.  The
remaining sixteen coordinate permutations produce valid e-cube schedules, but
not Mobius-Kantor selector-prefix schedules.

Thus the BT273 selector atlas is precisely the pair-stabilizing coordinate
subgroup of the e-cube compiler.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import permutations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_273_selector_phase_clock_atlas import (  # noqa: E402
    ALL_ONES,
    Q,
    selector_phase_clock_atlas_packet,
)


BITS = [1, 2, 4, 8]
STANDARD_INTERNAL_WORD_SOURCE = [4, 2, 8]
PAIR_PARTITION = [frozenset({1, 2}), frozenset({4, 8})]


def _cyclic_directions(cycle: list[int]) -> list[int]:
    return [cycle[index] ^ cycle[(index + 1) % len(cycle)] for index in range(len(cycle))]


def _preserves_pair_partition(mapping: dict[int, int]) -> bool:
    image_partition = {frozenset(mapping[bit] for bit in block) for block in PAIR_PARTITION}
    return image_partition == set(PAIR_PARTITION)


def ecube_coordinate_selector_atlas_packet() -> dict:
    bt273 = selector_phase_clock_atlas_packet()
    selector_prefix_to_row = {}
    for row in bt273["selector_rows"]:
        direction_word = _cyclic_directions(row["moving_cycle"])
        selector_prefix_to_row[tuple(direction_word[:Q])] = {
            "selector_index": row["selector_index"],
            "base_direction": row["base_direction"],
            "omitted_coordinate_axis": row["omitted_coordinate_axis"],
            "moving_cycle": row["moving_cycle"],
            "direction_word": direction_word,
        }

    rows = []
    matched_rows = []
    unmatched_rows = []
    for permutation in permutations(BITS):
        mapping = dict(zip(BITS, permutation))
        pivot = mapping[1]
        internal_q_word = [pivot ^ mapping[source] for source in STANDARD_INTERNAL_WORD_SOURCE]
        matched_selector = selector_prefix_to_row.get(tuple(internal_q_word))
        row = {
            "coordinate_permutation": list(permutation),
            "mapping": {str(key): value for key, value in sorted(mapping.items())},
            "pivot": pivot,
            "base_direction": ALL_ONES ^ pivot,
            "internal_q_word": internal_q_word,
            "preserves_pair_partition": _preserves_pair_partition(mapping),
            "matched_selector": matched_selector,
        }
        rows.append(row)
        if matched_selector is None:
            unmatched_rows.append(row)
        else:
            matched_rows.append(row)

    selector_distribution = Counter(row["matched_selector"]["selector_index"] for row in matched_rows)
    pivot_distribution = Counter(row["pivot"] for row in matched_rows)
    base_distribution = Counter(row["base_direction"] for row in matched_rows)
    unmatched_pivot_distribution = Counter(row["pivot"] for row in unmatched_rows)
    selector_by_pivot = defaultdict(list)
    for row in matched_rows:
        selector_by_pivot[row["pivot"]].append(row["matched_selector"]["selector_index"])

    pair_stabilizer_rows = [row for row in rows if row["preserves_pair_partition"]]
    selector_atlas_rows = [
        {
            "coordinate_permutation": row["coordinate_permutation"],
            "pivot": row["pivot"],
            "base_direction": row["base_direction"],
            "internal_q_word": row["internal_q_word"],
            "selector_index": row["matched_selector"]["selector_index"],
            "selector_direction_word": row["matched_selector"]["direction_word"],
        }
        for row in matched_rows
    ]

    checks = {
        "coordinate_conjugates_are_4_factorial": len(rows) == 24,
        "pair_stabilizer_has_2_to_q_elements": len(pair_stabilizer_rows) == 2**Q == 8,
        "selector_matching_conjugates_are_2_to_q": len(matched_rows) == 2**Q == 8,
        "selector_matching_equals_pair_stabilizer": {
            tuple(row["coordinate_permutation"]) for row in matched_rows
        }
        == {tuple(row["coordinate_permutation"]) for row in pair_stabilizer_rows},
        "unmatched_conjugates_are_16": len(unmatched_rows) == 16,
        "all_eight_selectors_hit_once": selector_distribution == {index: 1 for index in range(8)},
        "each_pivot_has_two_selector_conjugates": pivot_distribution == {bit: 2 for bit in BITS},
        "each_base_has_two_selector_conjugates": base_distribution
        == {ALL_ONES ^ bit: 2 for bit in BITS},
        "unmatched_have_four_per_pivot": unmatched_pivot_distribution == {bit: 4 for bit in BITS},
        "base_is_all_ones_xor_pivot_for_all_rows": all(
            row["base_direction"] == ALL_ONES ^ row["pivot"] for row in rows
        ),
        "omitted_axis_equals_pivot_for_matches": all(
            row["matched_selector"]["omitted_coordinate_axis"] == row["pivot"]
            for row in matched_rows
        ),
        "selector_pairs_by_pivot_are_bt273_base_pairs": {
            pivot: sorted(selectors) for pivot, selectors in selector_by_pivot.items()
        }
        == {1: [6, 7], 2: [4, 5], 4: [2, 3], 8: [0, 1]},
        "standard_coordinate_convention_is_selector_7": any(
            row["coordinate_permutation"] == [1, 2, 4, 8]
            and row["matched_selector"]["selector_index"] == 7
            for row in matched_rows
        ),
    }

    return {
        "breakthrough": 286,
        "title": "E-cube coordinate selector atlas",
        "coordinate_bits": BITS,
        "standard_internal_word_source": STANDARD_INTERNAL_WORD_SOURCE,
        "pair_partition": [sorted(block) for block in PAIR_PARTITION],
        "coordinate_conjugate_count": len(rows),
        "pair_stabilizer_count": len(pair_stabilizer_rows),
        "selector_match_count": len(matched_rows),
        "unmatched_count": len(unmatched_rows),
        "selector_distribution": dict(sorted(selector_distribution.items())),
        "pivot_distribution": dict(sorted(pivot_distribution.items())),
        "base_distribution": dict(sorted(base_distribution.items())),
        "unmatched_pivot_distribution": dict(sorted(unmatched_pivot_distribution.items())),
        "selector_pairs_by_pivot": {
            str(pivot): sorted(selectors) for pivot, selectors in sorted(selector_by_pivot.items())
        },
        "selector_atlas_rows": selector_atlas_rows,
        "unmatched_rows": [
            {
                "coordinate_permutation": row["coordinate_permutation"],
                "pivot": row["pivot"],
                "base_direction": row["base_direction"],
                "internal_q_word": row["internal_q_word"],
            }
            for row in unmatched_rows
        ],
        "architectural_reading": (
            "BT285 is the standard-coordinate member of a complete atlas. Among "
            "the 24 coordinate-conjugate binary-reflected e-cube conventions, "
            "exactly the 8 preserving the coordinate pair partition {{1,2},{4,8}} "
            "produce BT273 Mobius-Kantor selector prefixes. They hit the eight "
            "selectors exactly once, with pivot p selecting base 15 xor p. The "
            "selector atlas is therefore the 2^q pair-stabilizing coordinate "
            "subgroup of the e-cube compiler."
        ),
        "boundary": (
            "This classifies coordinate-conjugate e-cube schedules at the prefix "
            "selector level. It does not yet attach a physical reason for the "
            "{{1,2},{4,8}} pair partition beyond the binary-reflected compiler "
            "convention."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = ecube_coordinate_selector_atlas_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 286: E-CUBE COORDINATE SELECTOR ATLAS")
    print("=" * 78)
    print()
    print(f"coordinate conjugates = {packet['coordinate_conjugate_count']}")
    print(f"pair stabilizer       = {packet['pair_stabilizer_count']}")
    print(f"selector matches      = {packet['selector_match_count']}")
    print(f"selector distribution = {packet['selector_distribution']}")
    print(f"verified              = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_286_ecube_coordinate_selector_atlas.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
