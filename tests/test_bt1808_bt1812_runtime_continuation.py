import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1808_td43_edge_scheduler as bt1808  # noqa: E402
import bt1809_page_loader_td43_fusion as bt1809  # noqa: E402
import bt1810_hesse_wigner_td43_coupling as bt1810  # noqa: E402
import bt1812_sixth_ring_claim_firewall as bt1812  # noqa: E402


def test_bt1808_balanced_scheduler_counts():
    summary = bt1808.theorem_summary()
    assert summary["scheduler_rows"] == 1440
    assert summary["directed_fabric_edges"] == 480
    assert summary["directed_edge_cover_multiplicity"] == 3
    assert summary["slot_loads"] == {0: 480, 1: 480, 2: 480}


def test_bt1809_page_loader_profiles():
    summary = bt1809.theorem_summary()
    assert summary["safe_zone_overlap"]["overlap_points"] == 18
    assert summary["edge_move_profile"]["histogram_survivors_per_new_triple"] == {"0": 3, "3": 6}
    assert summary["nonedge_move_profile"]["histogram_survivors_per_new_triple"] == {"2": 9}


def test_bt1810_hesse_phase_dictionary():
    summary = bt1810.theorem_summary()
    assert summary["per_center_phase_space"]["phase_points"] == 9
    assert summary["per_center_phase_space"]["striations"] == 4
    assert summary["checks"]["safe_triad_and_cheap_quad_are_bijective_phase_readings"]


def test_bt1812_firewall_tiers():
    summary = bt1812.theorem_summary()
    assert summary["claim_count"] == 10
    assert summary["demoted_claim_count"] >= 4
    assert summary["checks"]["physics_identifications_demoted_from_exact_where_needed"]
