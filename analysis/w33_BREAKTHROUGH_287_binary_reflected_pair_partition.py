"""W(3,3) BREAKTHROUGH 287: binary-reflected pair partition.

BT286 proved that the BT273 selector atlas is exactly the coordinate subgroup
preserving the pair partition

    {{1,2}, {4,8}}.

BT287 derives that partition from the binary-reflected Q4 compiler itself.
The BT176 Gray/e-cube step word is

    1,2,1,4, 1,2,1,8, 1,2,1,4, 1,2,1,8.

Partition the four coordinates into two pairs.  There are only three 2+2
partitions.  Exactly one partition has a constant profile on every four-step
Q2 recursion block:

    {1,2} versus {4,8}:  every block has 3 fast steps and 1 slow step.

The other two partitions alternate block profiles.  Therefore the selector
pair partition is not imposed after the fact; it is the unique fast/slow
recursion split of the binary-reflected compiler.

Relative to this split, the scalar-to-now word

    [3,5,3,9,3]

has the exact pattern

    fast-internal, cross, fast-internal, cross, fast-internal.

Deleting the two fast-internal cap edges leaves the selector q-word

    cross, fast-internal, cross = [5,3,9],

which is BT285's selector-7 lift condition.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


BITS = [1, 2, 4, 8]
GRAY_STEP_WORD = [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 8]
TARGET_PAIR_PARTITION = [frozenset({1, 2}), frozenset({4, 8})]
SCALAR_TO_NOW_WORD = [3, 5, 3, 9, 3]
INTERNAL_Q_WORD = [5, 3, 9]


def _artifact(name: str) -> dict:
    path = ROOT / "data" / name
    if not path.exists():
        raise RuntimeError(f"missing prerequisite artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _pair_partitions() -> list[tuple[frozenset[int], frozenset[int]]]:
    partitions = []
    seen = set()
    for first in combinations(BITS, 2):
        left = frozenset(first)
        right = frozenset(set(BITS) - left)
        key = frozenset((left, right))
        if key in seen:
            continue
        seen.add(key)
        partitions.append((left, right))
    return partitions


def _block_profiles(partition: tuple[frozenset[int], frozenset[int]]) -> list[list[int]]:
    left, right = partition
    profiles = []
    for block_index in range(4):
        block = GRAY_STEP_WORD[4 * block_index : 4 * block_index + 4]
        profiles.append(
            [
                sum(1 for step in block if step in left),
                sum(1 for step in block if step in right),
            ]
        )
    return profiles


def _same_unordered_partition(
    partition: tuple[frozenset[int], frozenset[int]],
    target: list[frozenset[int]],
) -> bool:
    return set(partition) == set(target)


def _word_class(step: int, partition: tuple[frozenset[int], frozenset[int]]) -> str:
    bits = [bit for bit in BITS if step & bit]
    left, right = partition
    if all(bit in left for bit in bits):
        return "fast_internal"
    if all(bit in right for bit in bits):
        return "slow_internal"
    return "cross"


def binary_reflected_pair_partition_packet() -> dict:
    bt285 = _artifact("w33_BREAKTHROUGH_285_ecube_pivot_selector_lift.json")
    bt286 = _artifact("w33_BREAKTHROUGH_286_ecube_coordinate_selector_atlas.json")

    partition_rows = []
    constant_profile_rows = []
    for partition in _pair_partitions():
        profiles = _block_profiles(partition)
        is_target = _same_unordered_partition(partition, TARGET_PAIR_PARTITION)
        constant_profile = len({tuple(profile) for profile in profiles}) == 1
        row = {
            "partition": [sorted(block) for block in partition],
            "block_profiles": profiles,
            "profile_is_constant": constant_profile,
            "is_target_pair_partition": is_target,
        }
        partition_rows.append(row)
        if constant_profile:
            constant_profile_rows.append(row)

    target_partition = next(
        partition for partition in _pair_partitions() if _same_unordered_partition(partition, TARGET_PAIR_PARTITION)
    )
    scalar_to_now_classes = [_word_class(step, target_partition) for step in SCALAR_TO_NOW_WORD]
    internal_q_classes = [_word_class(step, target_partition) for step in INTERNAL_Q_WORD]
    cap_classes = [scalar_to_now_classes[0], scalar_to_now_classes[-1]]
    nonconstant_partitions = [
        row for row in partition_rows if not row["profile_is_constant"]
    ]

    checks = {
        "gray_step_word_matches_bt285": bt285["gray_step_word"] == GRAY_STEP_WORD,
        "there_are_three_two_plus_two_partitions": len(partition_rows) == 3,
        "unique_constant_block_profile_partition": len(constant_profile_rows) == 1,
        "constant_partition_is_target_pair_partition": constant_profile_rows[0]["is_target_pair_partition"],
        "target_partition_profile_is_three_one_each_block": constant_profile_rows[0]["block_profiles"]
        == [[3, 1], [3, 1], [3, 1], [3, 1]],
        "nonconstant_partitions_alternate_profiles": all(
            len({tuple(profile) for profile in row["block_profiles"]}) == 2
            for row in nonconstant_partitions
        ),
        "bt286_pair_partition_matches_target": {
            frozenset(block) for block in bt286["pair_partition"]
        }
        == set(TARGET_PAIR_PARTITION),
        "bt286_selector_match_count_is_pair_stabilizer": bt286["selector_match_count"]
        == bt286["pair_stabilizer_count"]
        == 8,
        "scalar_to_now_word_matches_bt285": bt285["scalar_to_now_word"] == SCALAR_TO_NOW_WORD,
        "scalar_to_now_has_fast_cross_fast_cross_fast_pattern": scalar_to_now_classes
        == ["fast_internal", "cross", "fast_internal", "cross", "fast_internal"],
        "cap_edges_are_fast_internal": cap_classes == ["fast_internal", "fast_internal"],
        "cap_deletion_leaves_internal_q_word": SCALAR_TO_NOW_WORD[1:-1] == INTERNAL_Q_WORD
        == bt285["internal_q_word"],
        "internal_q_word_has_cross_fast_cross_pattern": internal_q_classes
        == ["cross", "fast_internal", "cross"],
    }

    return {
        "breakthrough": 287,
        "title": "Binary-reflected pair partition",
        "gray_step_word": GRAY_STEP_WORD,
        "q2_recursion_blocks": [
            GRAY_STEP_WORD[4 * index : 4 * index + 4] for index in range(4)
        ],
        "partition_rows": partition_rows,
        "selected_pair_partition": [sorted(block) for block in TARGET_PAIR_PARTITION],
        "selected_partition_reading": "{1,2}=fast/local Q2 pair; {4,8}=slow/recursive boundary pair",
        "scalar_to_now_word": SCALAR_TO_NOW_WORD,
        "scalar_to_now_classes": scalar_to_now_classes,
        "internal_q_word": INTERNAL_Q_WORD,
        "internal_q_classes": internal_q_classes,
        "architectural_reading": (
            "BT286's coordinate pair partition is forced by the binary-reflected "
            "compiler. Among the three 2+2 coordinate partitions, only {{1,2},{4,8}} "
            "has a constant 3:1 fast/slow profile on every four-step Q2 recursion "
            "block. Relative to that split, the scalar-to-now route is fast-cap, "
            "cross, fast, cross, fast-cap; deleting the two fast cap edges leaves "
            "the cross-fast-cross selector word [5,3,9]. This gives the physical "
            "compiler reason for the BT286 pair stabilizer."
        ),
        "boundary": (
            "This derives the pair partition from the standard binary-reflected "
            "recursion. A coordinate-conjugate physical hardware convention would "
            "conjugate the same fast/slow partition accordingly."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = binary_reflected_pair_partition_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 287: BINARY-REFLECTED PAIR PARTITION")
    print("=" * 78)
    print()
    print(f"selected partition = {packet['selected_pair_partition']}")
    print(f"block profiles     = {packet['partition_rows']}")
    print(f"route classes      = {packet['scalar_to_now_classes']}")
    print(f"verified           = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_287_binary_reflected_pair_partition.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
