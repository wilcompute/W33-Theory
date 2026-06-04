from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_169_gap_f4_centerquad_crosswalk import (  # noqa: E402
    gap_f4_centerquad_crosswalk_packet,
)


PACKET = gap_f4_centerquad_crosswalk_packet()


def test_bt169_gap_mapping_basic_counts() -> None:
    assert PACKET["point_count"] == 45
    assert PACKET["line_count"] == 27
    assert PACKET["incidence_count"] == 135
    assert len(PACKET["point_mapping_f4_to_centerquad"]) == 45
    assert len(PACKET["line_mapping_f4_to_centerquad"]) == 27


def test_bt169_gap_mapping_is_permutation() -> None:
    assert sorted(PACKET["point_mapping_f4_to_centerquad"]) == list(range(45))
    assert sorted(PACKET["line_mapping_f4_to_centerquad"]) == list(range(27))


def test_bt169_gap_and_python_checks_agree() -> None:
    checks = PACKET["checks"]
    assert checks["gap_found_isomorphism"] is True
    assert checks["gap_preserved_lines"] is True
    assert checks["python_adjacency_check"] is True
    assert checks["python_line_check"] is True


def test_bt169_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 8
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt169_gap_mapping_basic_counts()
    test_bt169_gap_mapping_is_permutation()
    test_bt169_gap_and_python_checks_agree()
    test_bt169_all_checks_pass()
