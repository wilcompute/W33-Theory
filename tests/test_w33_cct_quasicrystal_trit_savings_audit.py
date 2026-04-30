from __future__ import annotations

from scripts.w33_cct_quasicrystal_trit_savings_audit import (
    cct_quasicrystal_trit_savings_summary,
)


def test_cct_trit_savings_is_least_change_empire_overlap_rule() -> None:
    summary = cct_quasicrystal_trit_savings_summary()

    assert summary["source_scope"]["chapter"] == 6
    assert summary["quasicrystal_rule_packet"] == {
        "dominant_vertex_type": "K",
        "candidate_same_type_neighbors": 8,
        "perpendicular_space_selection": (
            "same pentagonal area in perpendicular space, forming two pentagons"
        ),
        "E0": "union of the empire fields of all existing dominant vertex types",
        "Ei": "empire field of the ith neighboring vertex type",
        "Ui": "E0 intersect Ei",
        "preferred_move": "argmax_i |Ui|",
        "equivalent_minimization": (
            "minimize the empire-field tiles or cut-window shifts that must change"
        ),
        "tie_rule": "random choice among maximizing neighbors",
        "self_stay_allowed": False,
    }

    packet = summary["trit_savings_packet"]
    assert packet["path_name"] == "maximum trits-saving path"
    assert "changed tiles" in packet["two_dimensional_measure"]
    assert "cut-window shifts" in packet["higher_dimensional_measure"]
    assert "not merely" in packet["not_primary_meaning"]


def test_cct_trit_savings_uses_quasicrystal_windows() -> None:
    summary = cct_quasicrystal_trit_savings_summary()
    windows = summary["quasicrystal_window_packet"]

    assert windows["penrose_mother_lattice"] == "Z5"
    assert windows["fig_mother_lattice"] == "E8"
    assert "forced by a local patch" in windows["empire_window"]
    assert "may coexist" in windows["possibility_space_window"]
    assert "update after each" in windows["dynamic_background"]


def test_w33_bridge_certifies_only_finite_trit_savings_skeleton() -> None:
    summary = cct_quasicrystal_trit_savings_summary()
    bridge = summary["w33_bridge_packet"]

    assert bridge["qutrit_alphabet_owner"] == 3
    assert bridge["neighbor_options"] == bridge["w33_k_minus_mu"] == 8
    assert bridge["clockwise_counterclockwise_split"] == (4, 4)
    assert bridge["clock_split_matches_mu_plus_mu"] is True
    assert bridge["ten_d4_packets_recover_edge_shell"] == bridge["edge_shell"] == 240
    assert bridge["fig_20g_from_five_4g_packet"] == (5, 4, 20)
    assert "source/frontier dynamics" in bridge["frontier_boundary"]
    assert all(summary["theorem"].values())
