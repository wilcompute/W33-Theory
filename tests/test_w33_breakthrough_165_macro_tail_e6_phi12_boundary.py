from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_165_macro_tail_e6_phi12_boundary import (  # noqa: E402
    macro_tail_e6_phi12_boundary_packet,
)


PACKET = macro_tail_e6_phi12_boundary_packet()


def test_bt165_tail_splits_as_e6_plus_phi12() -> None:
    assert PACKET["tail_size"] == 151
    assert PACKET["tail_by_polarization"] == {"anti": 73, "mixed": 78}
    assert PACKET["boundary_decomposition"]["outside_f4_normalizer"]["count"] == 78
    assert PACKET["boundary_decomposition"]["inside_f4_normalizer"]["count"] == 73


def test_bt165_f4_boundary_controls_admissibility() -> None:
    assert PACKET["tail_by_f4_boundary_and_diameter"] == {
        "('inside', 6)": 65,
        "('inside', 7)": 8,
        "('outside', 6)": 78,
    }
    assert PACKET["boundary_decomposition"]["inside_f4_normalizer"]["admissible"] == 65
    assert PACKET["boundary_decomposition"]["inside_f4_normalizer"]["forbidden"] == 8


def test_bt165_normalizer_distance_profile() -> None:
    assert PACKET["f4_normalizer_order"] == 1152
    assert PACKET["normalizer_distance_profile"] == {
        0: 1,
        1: 10,
        2: 46,
        3: 117,
        4: 192,
        5: 250,
        6: 463,
        7: 73,
    }


def test_bt165_inside_and_outside_order_distributions() -> None:
    assert PACKET["inside_order_distribution"] == {2: 5, 4: 6, 6: 32, 8: 6, 12: 24}
    assert PACKET["outside_order_distribution"] == {
        5: 6,
        6: 20,
        8: 8,
        9: 14,
        10: 6,
        12: 22,
        18: 2,
    }


def test_bt165_trace_sectors_split_e6_shell() -> None:
    assert PACKET["inside_trace_distribution"] == {0: 73}
    assert PACKET["outside_trace_distribution"] == {0: 28, 1: 26, 2: 24}
    assert PACKET["outside_trace_reading"] == {
        "trace_0": "28 = D4 root count",
        "trace_1": "26 = bosonic string dimension",
        "trace_2": "24 = f",
    }


def test_bt165_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 19
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt165_tail_splits_as_e6_plus_phi12()
    test_bt165_f4_boundary_controls_admissibility()
    test_bt165_normalizer_distance_profile()
    test_bt165_inside_and_outside_order_distributions()
    test_bt165_trace_sectors_split_e6_shell()
    test_bt165_all_checks_pass()
