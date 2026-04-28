from pathlib import Path

from scripts.w33_representation_triangle_121_audit import (
    build_representation_triangle_121_summary,
)


PART_LXXIX_NOTE = Path("PART_LXXIX_REPRESENTATION_TRIANGLE_121.md")


def test_representation_triangle_121_records_the_three_module_carrier() -> None:
    summary = build_representation_triangle_121_summary()

    assert summary["status"] == "ok"
    assert summary["carrier_dictionary"] == {
        "line_module": "40 = 1 + 15 + 24",
        "spread_module": "36 = 1 + 15 + 20",
        "anti_line_quotient_module": "45 = 1 + 24 + 20",
        "total_dimension_identity": "40 + 36 + 45 = 121 = (k - 1)^2",
        "sector_double_count_identity": "3 + 2(15 + 20 + 24) = 121",
        "nonbacktracking_outdegree": "k - 1 = 11",
        "qutrit_hilbert_dimension_identity": "q^4 = C(q^2,2) + C(q^2+1,2) = 36 + 45 = 81",
        "representation_triangle_uniqueness": "(k-1)^2 = v + q^4 iff q = 3: gap = q(q-3)(q+1)",
    }
    assert summary["sector_sharing_triangle"] == {
        "L_intersect_S": "1 + 15",
        "L_intersect_Q": "1 + 24",
        "S_intersect_Q": "1 + 20",
        "hidden_target_sector": 20,
    }


def test_representation_triangle_121_records_exact_identities_and_spectra() -> None:
    summary = build_representation_triangle_121_summary()

    assert summary["exact_identities"] == {
        "centered_spread_probe": "B_c = B - J/4",
        "centered_anti_line_quotient_probe": "U_c = U - 2J/5",
        "signed_spread_probe": "B_4 = 4B - J",
        "signed_anti_line_quotient_probe": "U_5 = 5U - 2J",
        "spread_projector_identity": "B_c B_c^T = 18 P_15",
        "quotient_projector_identity": "U_c U_c^T = 18 P_24",
        "spread_isometry": "B_c^T / sqrt(18) : L_15 -> S_15",
        "quotient_isometry": "U_c^T / sqrt(18) : L_24 -> Q_24",
        "orthogonality": "B_c^T U_c = 0",
        "full_resolution": "(B_c B_c^T + U_c U_c^T) / 18 = I - J/40",
        "integer_full_resolution": "25 B_4 B_4^T + 16 U_5 U_5^T = 7200 I - 180 J",
        "common_singular_constant": "sqrt(18) = 3sqrt(2)",
    }
    assert summary["spectral_data"] == {
        "line_disjoint_spectrum": {-3: 24, 3: 15, 27: 1},
        "spread_overlap_1_spectrum": {-4: 15, 2: 20, 20: 1},
        "anti_line_quotient_graph_spectrum": {-3: 24, 3: 20, 12: 1},
        "signed_spread_probe_spectrum": {0: 25, 288: 15},
        "signed_anti_line_quotient_probe_spectrum": {0: 16, 450: 24},
    }


def test_representation_triangle_121_theorem_and_checks_all_hold() -> None:
    summary = build_representation_triangle_121_summary()

    assert summary["theorem"] == {
        "the_line_spread_and_anti_line_quotient_modules_form_the_exact_121_representation_triangle": True,
        "the_centered_spread_and_anti_line_quotient_probes_have_the_same_singular_constant_sqrt_18": True,
        "the_spread_and_quotient_channels_are_exactly_the_line_side_15_and_24_sector_projectors": True,
        "the_two_visible_channels_are_orthogonal_and_resolve_the_zero_mean_line_module": True,
        "the_pairwise_sector_sharing_is_exactly_l_intersect_s_equals_1_plus_15_l_intersect_q_equals_1_plus_24_and_s_intersect_q_equals_1_plus_20": True,
    }
    assert all(summary["checks"].values())
    assert "121-dimensional representation-level object" in summary["interpretation"]
    assert "same singular constant sqrt(18)" in summary["interpretation"]
    assert "1+15, 1+24, and 1+20" in summary["interpretation"]


def test_part_lxxix_note_mentions_the_q4_uniqueness_and_executable_surface() -> None:
    note_text = PART_LXXIX_NOTE.read_text(encoding="utf-8")

    assert "|S|+|Q|=q^4=81" in note_text
    assert "121=v+q^4" in note_text
    assert "(k-1)^2-v-q^4=q(q-3)(q+1)" in note_text
    assert "scripts/w33_representation_triangle_121_audit.py" in note_text
    assert "tests/test_w33_representation_triangle_121_audit.py" in note_text