from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_170_gap_projective_e6_stabilizer_cascade import (  # noqa: E402
    gap_projective_e6_stabilizer_cascade_packet,
)


PACKET = gap_projective_e6_stabilizer_cascade_packet()


def test_bt170_projective_order_and_kernel() -> None:
    assert PACKET["full_compiler_group_order"] == 51_840
    assert PACKET["projective_image_order"] == 25_920
    assert PACKET["central_kernel_size"] == 2
    assert PACKET["normalizer_order"] == 1_152


def test_bt170_point_and_line_stabilizers() -> None:
    assert PACKET["point_count"] == 45
    assert PACKET["line_count"] == 27
    assert PACKET["point_stabilizer"] == 576
    assert PACKET["line_stabilizer"] == 960
    assert PACKET["point_stabilizer_suborbits"] == [1, 12, 32]


def test_bt170_generators_and_gap_geometry() -> None:
    assert PACKET["generator_count"] == 16
    assert set(PACKET["generator_orders"]) == {3}
    checks = PACKET["checks"]
    assert checks["compiler_generators_preserve_gq_lines"] is True
    assert checks["line_action_is_faithful_same_order"] is True


def test_bt170_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 18
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt170_projective_order_and_kernel()
    test_bt170_point_and_line_stabilizers()
    test_bt170_generators_and_gap_geometry()
    test_bt170_all_checks_pass()
