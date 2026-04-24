from __future__ import annotations

from scripts.w33_toroidal_continuum_seed_audit import (
    analyze,
    classify_toroidal_continuum_seed,
    spectral_continuum_bridge_summary,
    toroidal_continuum_seed_summary,
    toroidal_seed_packet_summary,
)


def test_toroidal_seed_packet_is_exact() -> None:
    summary = toroidal_seed_packet_summary()

    assert summary == {
        "selector_line_dimension": 1,
        "shared_six_channel": 6,
        "q": 3,
        "phi6": 7,
        "phi3": 13,
        "electroweak_master_variable": {"exact": "3/13", "float": 3 / 13},
        "adjacency_spectrum": [6, -1, -1, -1, -1, -1, -1],
        "laplacian_spectrum": [0, 7, 7, 7, 7, 7, 7],
        "toroidal_trace": 42,
        "surface_flag_packet": 84,
        "fano_nontrivial_trace": 12,
        "cartan_packet": 8,
        "topological_packet": 56,
        "exact_factorizations": {
            "selector_plus_phi6_equals_cartan_packet": True,
            "shared_six_plus_phi6_equals_phi3": True,
            "electroweak_master_variable_equals_q_over_phi3": True,
            "electroweak_master_variable_equals_q_over_shared_six_plus_phi6": True,
            "shared_six_times_phi6_equals_toroidal_trace": True,
            "surface_flags_equal_twice_toroidal_trace": True,
            "fano_plus_toroidal_traces_equal_54": True,
        },
    }


def test_toroidal_seed_fixes_live_continuum_coefficients() -> None:
    summary = toroidal_continuum_seed_summary()

    assert summary == {
        "vertex_count": 40,
        "rank39": 39,
        "continuum_eh_coefficient": 320,
        "discrete_eh_coefficient": 12480,
        "topological_coefficient": 2240,
        "cartan_rank": 8,
        "e7_fundamental_dimension": 56,
        "exact_factorizations": {
            "continuum_eh_equals_vertices_times_cartan_packet": True,
            "cartan_packet_equals_cartan_rank": True,
            "topological_packet_equals_phi6_times_cartan_packet": True,
            "topological_packet_equals_e7_fundamental_dimension": True,
            "topological_equals_vertices_times_topological_packet": True,
            "topological_equals_continuum_times_phi6": True,
            "discrete_eh_equals_rank39_times_vertices_times_cartan_packet": True,
            "discrete_eh_equals_rank39_times_continuum": True,
        },
    }


def test_corrected_spectral_core_splices_into_the_toroidal_continuum_packet() -> None:
    summary = spectral_continuum_bridge_summary()

    assert summary == {
        "nontrivial_multiplicity_packet": (24, 15),
        "nontrivial_multiplicity_sum": 39,
        "spectral_negative_weight": 4,
        "total_mode_count": 80,
        "phi6": 7,
        "rank39": 39,
        "continuum_eh_coefficient": 320,
        "topological_coefficient": 2240,
        "discrete_eh_coefficient": 12480,
        "exact_factorizations": {
            "rank39_equals_nontrivial_multiplicity_sum": True,
            "continuum_equals_abs_negative_eigenvalue_times_total_mode_count": True,
            "topological_equals_phi6_times_abs_negative_eigenvalue_times_total_mode_count": True,
            "discrete_equals_nontrivial_multiplicity_sum_times_abs_negative_eigenvalue_times_total_mode_count": True,
        },
    }


def test_analysis_packages_exact_toroidal_continuum_boundary() -> None:
    summary = analyze()
    records = {record["name"]: record for record in classify_toroidal_continuum_seed()}

    assert summary["status"] == "ok"
    assert summary["record_names"] == (
        "toroidal_k7_selector_shell",
        "decimal_surface_phi3_shell",
        "toroidal_continuum_base_packet",
        "toroidal_topological_packet",
        "rank39_dressed_toroidal_continuum_packet",
        "spectral_toroidal_continuum_splice",
    )
    assert records["toroidal_k7_selector_shell"]["support_level"] == "repo-exact toroidal shell"
    assert records["decimal_surface_phi3_shell"]["support_level"] == "repo-exact decimal/toroidal shell"
    assert records["toroidal_continuum_base_packet"]["support_level"] == "repo-exact continuum seed"
    assert records["toroidal_topological_packet"]["support_level"] == "repo-exact continuum seed"
    assert records["rank39_dressed_toroidal_continuum_packet"]["support_level"] == "repo-exact continuum seed"
    assert records["spectral_toroidal_continuum_splice"]["support_level"] == "repo-exact spectral/continuum splice"
    assert summary["toroidal_continuum_theorem"] == {
        "toroidal_seed_fixes_exact_cartan_packet_8": True,
        "decimal_toroidal_seed_fixes_exact_phi3_packet_13": True,
        "decimal_toroidal_seed_fixes_exact_electroweak_selector_3_over_13": True,
        "toroidal_seed_fixes_exact_trace_packet_42": True,
        "surface_flag_packet_is_exactly_84_equals_2_times_42": True,
        "toroidal_seed_fixes_exact_continuum_eh_coefficient_320": True,
        "toroidal_seed_fixes_exact_topological_packet_56": True,
        "toroidal_seed_fixes_exact_topological_coefficient_2240": True,
        "spectral_core_fixes_exact_rank39_bridge_factor": True,
        "spectral_core_fixes_exact_continuum_eh_coefficient_320": True,
        "spectral_core_fixes_exact_topological_coefficient_2240": True,
        "rank39_dresses_toroidal_continuum_base_to_discrete_6_mode_12480": True,
        "spectral_core_fixes_exact_discrete_6_mode_12480": True,
        "remaining_continuum_wall_is_smooth_realization_not_discrete_normalization": True,
    }