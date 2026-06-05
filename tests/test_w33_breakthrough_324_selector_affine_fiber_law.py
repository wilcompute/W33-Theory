from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_324_selector_affine_fiber_law import (  # noqa: E402
    selector_affine_fiber_law_packet,
)


PACKET = selector_affine_fiber_law_packet()


def test_bt324_linear_fibers_and_translations() -> None:
    assert PACKET["linear_part_fibers"] == {
        "linear_0": [0, 3, 5, 6],
        "linear_1": [1, 2, 4, 7],
    }
    assert PACKET["translations_by_linear_part"] == {
        "linear_0": [[0, 0], [0, 1], [1, 0], [1, 1]],
        "linear_1": [[0, 0], [0, 1], [1, 0], [1, 1]],
    }


def test_bt324_selector_affine_rows() -> None:
    expected = {
        0: ("linear_0", [1, 1]),
        1: ("linear_1", [1, 1]),
        2: ("linear_1", [0, 1]),
        3: ("linear_0", [0, 1]),
        4: ("linear_1", [1, 0]),
        5: ("linear_0", [1, 0]),
        6: ("linear_0", [0, 0]),
        7: ("linear_1", [0, 0]),
    }
    for row in PACKET["selector_rows"]:
        linear_part, translation = expected[row["selector_index"]]
        assert row["linear_part_id"] == linear_part
        assert row["translation"] == translation
        assert row["rank"] == 2
        assert row["kernel"] == [[0, 0, 0], [1, 1, 1]]
        assert len(row["direction_outputs"]) == 8


def test_bt324_kernel_quotient_routes() -> None:
    model = PACKET["even_subspace_model"]
    assert model["basis_words"] == [3, 5, 9]
    assert model["common_kernel"] == [[0, 0, 0], [1, 1, 1]]
    assert len(model["kernel_cosets"]) == 4
    for row in PACKET["selector_rows"]:
        routes = row["quotient_routes"]
        assert len(routes) == 4
        assert all(route["constant_on_coset"] for route in routes)
        assert all(len(route["coset"]) == 2 for route in routes)
        assert sorted(route["direction_word"] for route in routes) == [1, 2, 4, 8]


def test_bt324_linear_parts_explain_bt323_graphs() -> None:
    explanation = PACKET["pair_intersection_explanation"]
    assert len(explanation["equal_linear_part_pairs"]) == 12
    assert len(explanation["different_linear_part_pairs"]) == 16
    assert explanation["equal_linear_part_intersection_size"] == 0
    assert explanation["different_linear_part_intersection_size"] == 2
    assert explanation["disjointness_graph_from_linear_parts"] == {
        "0": [3, 5, 6],
        "1": [2, 4, 7],
        "2": [1, 4, 7],
        "3": [0, 5, 6],
        "4": [1, 2, 7],
        "5": [0, 3, 6],
        "6": [0, 3, 5],
        "7": [1, 2, 4],
    }
    assert all(len(neighbors) == 4 for neighbors in explanation["two_overlap_graph_from_linear_parts"].values())


def test_bt324_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 21
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt324_linear_fibers_and_translations()
    test_bt324_selector_affine_rows()
    test_bt324_kernel_quotient_routes()
    test_bt324_linear_parts_explain_bt323_graphs()
    test_bt324_all_checks_pass()
