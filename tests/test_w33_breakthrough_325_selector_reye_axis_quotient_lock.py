from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_325_selector_reye_axis_quotient_lock import (  # noqa: E402
    selector_reye_axis_quotient_lock_packet,
)


PACKET = selector_reye_axis_quotient_lock_packet()


def test_bt325_axis_sheets_match_selector_fibers() -> None:
    assert PACKET["axis_model"]["even_pointwise_fixed_axes"] == [0, 3, 5, 6]
    assert PACKET["axis_model"]["odd_endpoint_swapped_axes"] == [1, 2, 4, 7]
    assert PACKET["selector_axis_lock"]["linear_part_fibers"] == {
        "linear_0": [0, 3, 5, 6],
        "linear_1": [1, 2, 4, 7],
    }


def test_bt325_kernel_cosets_are_even_reye_axes() -> None:
    assert PACKET["selector_axis_lock"]["kernel_coset_axis_indices"] == [0, 6, 5, 3]
    assert sorted(PACKET["selector_axis_lock"]["kernel_coset_axis_indices"]) == [0, 3, 5, 6]


def test_bt325_cross_fiber_graph_is_reye_quotient_graph() -> None:
    graph = PACKET["graph_lock"]
    assert graph["bt324_two_overlap_edges"] == graph["reye_quotient_edges"]
    assert graph["reye_quotient_graph"] == {
        "0": [1, 2, 4, 7],
        "1": [0, 3, 5, 6],
        "2": [0, 3, 5, 6],
        "3": [1, 2, 4, 7],
        "4": [0, 3, 5, 6],
        "5": [1, 2, 4, 7],
        "6": [1, 2, 4, 7],
        "7": [0, 3, 5, 6],
    }


def test_bt325_coordinate_matching_decomposition() -> None:
    decomposition = PACKET["coordinate_matching_decomposition"]
    assert decomposition["axis_xor_to_q4_lift_bit"] == {
        "1": [1],
        "2": [2],
        "4": [4],
        "7": [8],
    }
    assert decomposition["same_translation_pairs"] == [[0, 1], [2, 3], [4, 5], [6, 7]]
    assert decomposition["now_axis_xor"] == 1
    assert decomposition["now_q4_lift_bit"] == 1
    assert decomposition["now_direction_label"] == [0, 0]


def test_bt325_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 14
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt325_axis_sheets_match_selector_fibers()
    test_bt325_kernel_cosets_are_even_reye_axes()
    test_bt325_cross_fiber_graph_is_reye_quotient_graph()
    test_bt325_coordinate_matching_decomposition()
    test_bt325_all_checks_pass()
