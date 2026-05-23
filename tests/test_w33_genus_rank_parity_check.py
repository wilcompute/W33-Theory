from __future__ import annotations

from analysis.w33_genus_rank_parity_check import genus_rank_parity_check_packet


def test_mccx_packet() -> None:
    packet = genus_rank_parity_check_packet()

    assert packet["packet"] == {
        "q": 3,
        "n": 72,
        "k_code": 66,
        "rank_H": 6,
        "genus": 6,
        "k_val": 12,
        "N_M": 36,
    }
    assert packet["identity"] == {
        "statement": "rank(H)=n-k=72-66=6=g=k_val/2=N_M/(2q)",
    }


def test_mccx_all_checks_pass() -> None:
    packet = genus_rank_parity_check_packet()

    assert packet["checks"] == {
        "packet_is_72_66": True,
        "rank_is_n_minus_k": True,
        "rank_is_6": True,
        "rank_equals_genus": True,
        "rank_equals_k_over_2": True,
        "rank_equals_nm_over_2q": True,
        "genus_is_6": True,
        "k_is_12": True,
        "nm_is_36": True,
        "all_rank_forms_match": True,
    }
    assert packet["n_verified"] == 10
