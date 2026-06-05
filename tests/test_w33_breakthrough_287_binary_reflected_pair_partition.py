from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_287_binary_reflected_pair_partition import (  # noqa: E402
    binary_reflected_pair_partition_packet,
)


PACKET = binary_reflected_pair_partition_packet()


def test_bt287_unique_constant_recursion_partition() -> None:
    constant = [row for row in PACKET["partition_rows"] if row["profile_is_constant"]]
    assert len(constant) == 1
    assert constant[0]["partition"] == [[1, 2], [4, 8]]
    assert constant[0]["block_profiles"] == [[3, 1], [3, 1], [3, 1], [3, 1]]


def test_bt287_nonconstant_partitions_alternate() -> None:
    nonconstant = [row for row in PACKET["partition_rows"] if not row["profile_is_constant"]]
    assert len(nonconstant) == 2
    assert all(len({tuple(profile) for profile in row["block_profiles"]}) == 2 for row in nonconstant)


def test_bt287_scalar_to_now_class_pattern() -> None:
    assert PACKET["scalar_to_now_word"] == [3, 5, 3, 9, 3]
    assert PACKET["scalar_to_now_classes"] == [
        "fast_internal",
        "cross",
        "fast_internal",
        "cross",
        "fast_internal",
    ]
    assert PACKET["internal_q_word"] == [5, 3, 9]
    assert PACKET["internal_q_classes"] == ["cross", "fast_internal", "cross"]


def test_bt287_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 13
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt287_unique_constant_recursion_partition()
    test_bt287_nonconstant_partitions_alternate()
    test_bt287_scalar_to_now_class_pattern()
    test_bt287_all_checks_pass()
