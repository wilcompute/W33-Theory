from __future__ import annotations

from analysis.w33_reye_horizon_symmetry_genus_reciprocity import (
    reye_horizon_symmetry_genus_reciprocity_packet,
)


def test_mcxciv_packets() -> None:
    packet = reye_horizon_symmetry_genus_reciprocity_packet()

    assert packet["horizon_packet"] == {
        "genus": 6,
        "payload": 66,
        "parity": 6,
        "total": 72,
        "identity": "72 = 66 + 6 with genus=6",
    }
    assert packet["symmetry_packet"] == {
        "aut_reye": 576,
        "aut_tomotope": 96,
        "ratio": 6,
        "identity": "576/96 = 6",
    }
    assert packet["reciprocity_lock"] == {
        "identity": "|Aut(Reye)|/|Aut(T)| = genus = parity = 6 and 72 = 66 + 6",
    }


def test_mcxciv_all_checks_pass() -> None:
    packet = reye_horizon_symmetry_genus_reciprocity_packet()

    assert packet["checks"] == {
        "mcxcii_genus_is_6": True,
        "mcxcii_parity_is_6": True,
        "mcxcii_code_splits_as_66_plus_6": True,
        "mcxcii_payload_is_k12_edges": True,
        "mcxciii_symmetry_is_576_over_96": True,
        "symmetry_ratio_is_6": True,
        "symmetry_ratio_equals_genus": True,
        "symmetry_ratio_equals_parity": True,
        "reye_symmetry_equals_genus_times_tomotope_symmetry": True,
        "reye_symmetry_equals_parity_times_tomotope_symmetry": True,
        "total_code_equals_payload_plus_symmetry_ratio": True,
    }
    assert packet["n_verified"] == 11
