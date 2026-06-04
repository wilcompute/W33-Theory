from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_157_cayley_compiler_macro_depth import (
    cayley_compiler_macro_packet,
)


PACKET = cayley_compiler_macro_packet()


def test_bt157_raw_compiler_diameters() -> None:
    assert PACKET["group_order"] == 51840
    assert PACKET["diameters"] == {
        "8_forward_lanes": 9,
        "16_inverse_complete_pulses": 7,
        "18_with_macro_pair": 6,
    }


def test_bt157_distance_distributions() -> None:
    assert PACKET["forward_distribution"] == {
        0: 1,
        1: 8,
        2: 50,
        3: 257,
        4: 1165,
        5: 4464,
        6: 13297,
        7: 22292,
        8: 9996,
        9: 310,
    }
    assert PACKET["symmetric_distribution"][7] == 151
    assert PACKET["macro_distribution"] == {
        0: 1,
        1: 18,
        2: 224,
        3: 2255,
        4: 16112,
        5: 32013,
        6: 1217,
    }


def test_bt157_macro_data() -> None:
    macro = PACKET["macro"]

    assert macro["order"] == 9
    assert macro["word"] == ["T1^1", "T2^1", "T1^2", "T6^1", "T4^2", "T5^1", "T6^2"]
    assert macro["matrix"] == [
        [2, 2, 0, 2],
        [0, 0, 1, 0],
        [2, 1, 2, 0],
        [0, 2, 2, 0],
    ]


def test_bt157_architecture_boundary() -> None:
    correction = PACKET["architectural_correction"]

    assert "does not have raw q! depth" in correction
    assert "restores exact q!=6 global dispatch" in correction


def test_bt157_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt157_raw_compiler_diameters()
    test_bt157_distance_distributions()
    test_bt157_macro_data()
    test_bt157_architecture_boundary()
    test_bt157_all_checks_pass()
