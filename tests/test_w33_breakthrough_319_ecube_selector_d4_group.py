from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_319_ecube_selector_d4_group import (  # noqa: E402
    IDENTITY,
    R_GENERATOR,
    S_GENERATOR,
    compose,
    ecube_selector_d4_group_packet,
    inverse,
    order,
)


PACKET = ecube_selector_d4_group_packet()


def _elements() -> set[tuple[int, ...]]:
    return {tuple(row) for row in PACKET["elements"]}


def test_bt319_group_count_and_selector_link() -> None:
    assert PACKET["group_order"] == 8
    assert PACKET["group_order_substrate_form"] == "2^q = 8"
    assert PACKET["selector_atlas_link"]["selector_match_count"] == 8
    assert PACKET["selector_atlas_link"]["selector_distribution"] == {index: 1 for index in range(8)}


def test_bt319_closure_identity_and_inverses() -> None:
    elements = _elements()
    assert IDENTITY in elements
    for left in elements:
        assert inverse(left) in elements
        for right in elements:
            assert compose(left, right) in elements


def test_bt319_d4_signature() -> None:
    assert PACKET["group_identification"] == "D4, the order-8 square symmetry group"
    assert PACKET["order_distribution"] == {1: 1, 2: 5, 4: 2}
    assert len(PACKET["center"]) == 2
    assert [2, 1, 8, 4] in PACKET["center"]


def test_bt319_d4_presentation() -> None:
    r = R_GENERATOR
    s = S_GENERATOR
    assert order(r) == 4
    assert order(s) == 2
    assert compose(s, compose(r, s)) == inverse(r)
    assert PACKET["generators"]["srs"] == PACKET["generators"]["r_inverse"]


def test_bt319_nonabelian_witness() -> None:
    witness = PACKET["noncommuting_witness"]
    assert witness["left_after_right"] != witness["right_after_left"]


def test_bt319_hadamard_q4_bridge() -> None:
    link = PACKET["hadamard_q4_link"]
    assert link["reed_muller_at_mu"]["explicit"] == [16, 5, 8]
    assert link["diagonalizes_Q_mu_adjacency"] is True


def test_bt319_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 19
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt319_group_count_and_selector_link()
    test_bt319_closure_identity_and_inverses()
    test_bt319_d4_signature()
    test_bt319_d4_presentation()
    test_bt319_nonabelian_witness()
    test_bt319_hadamard_q4_bridge()
    test_bt319_all_checks_pass()
