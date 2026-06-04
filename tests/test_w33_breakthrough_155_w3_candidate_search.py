from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_155_W3_candidate_search import w3_candidate_packet


PACKET = w3_candidate_packet()


def test_bt155_known_wieferich_primes_verify_directly() -> None:
    known = {row["value"]: row for row in PACKET["known_wieferich"]}

    assert known[1093]["wieferich_base2"] is True
    assert known[3511]["wieferich_base2"] is True
    assert PACKET["gap"] == 2418
    assert known[3511]["value"] + PACKET["gap"] == 5929


def test_bt155_new_substrate_primes_are_not_wieferich() -> None:
    primes = {row["value"]: row for row in PACKET["new_substrate_primes"]}

    assert sorted(primes) == [311, 1951]
    assert primes[311]["fermat_quotient_mod_p"] == 175
    assert primes[1951]["fermat_quotient_mod_p"] == 1786
    assert all(not row["wieferich_base2"] for row in primes.values())


def test_bt155_gap_successor_is_forbidden_square() -> None:
    gap_candidates = {
        row["form"]: row for row in PACKET["candidate_rows"] if row["family"] == "gap"
    }

    square = gap_candidates["W_2 + GAP"]
    assert square["value"] == 5929
    assert square["factors"] == {7: 2, 11: 2}
    assert square["prime"] is False
    assert square["wieferich_base2"] is False


def test_bt155_boundary_is_not_global_no_w3_proof() -> None:
    assert len(PACKET["candidate_rows"]) == 15
    assert all(not row["wieferich_base2"] for row in PACKET["candidate_rows"])
    assert "does not prove global nonexistence" in PACKET["boundary"]


def test_bt155_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt155_known_wieferich_primes_verify_directly()
    test_bt155_new_substrate_primes_are_not_wieferich()
    test_bt155_gap_successor_is_forbidden_square()
    test_bt155_boundary_is_not_global_no_w3_proof()
    test_bt155_all_checks_pass()
