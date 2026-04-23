from __future__ import annotations

from scripts.w33_q3_master_lock_audit import (
    analyze,
    classify_q3_master_lock,
    q3_continuum_seed_summary,
    q3_local_kernel_summary,
    q3_spectral_uniqueness_summary,
    symbolic_q3_lock_summary,
)


def test_symbolic_q3_lock_summary_has_exact_gap_factors() -> None:
    summary = symbolic_q3_lock_summary()

    assert summary["n_zero_gap"] == "(q - 3)*(q + 1)*(q**2 + 1)"
    assert summary["m2_minus_k_gap"] == "-q*(q - 3)*(q + 1)/(q - 1)"
    assert summary["disc_r_plus_4phi4_gap"] == "(q - 3)**2"
    assert summary["disc_s_plus_4phi6_gap"] == "(q - 3)**2"
    assert summary["q3_evaluations"] == {
        "n_zero_gap_at_3": 0,
        "m2_minus_k_gap_at_3": 0,
        "disc_r_gap_at_3": 0,
        "disc_s_gap_at_3": 0,
    }
    assert summary["exact_factors"] == {
        "n_zero_gap_factor_is_exact": True,
        "m2_minus_k_gap_factor_is_exact": True,
        "disc_r_gap_factor_is_exact": True,
        "disc_s_gap_factor_is_exact": True,
        "all_symbolic_gaps_vanish_at_q3": True,
    }


def test_q3_local_kernel_summary_matches_finite_qutrit_packet() -> None:
    summary = q3_local_kernel_summary()

    assert summary["q"] == 3
    assert summary["phi3"] == 13
    assert summary["phi4"] == 10
    assert summary["phi6"] == 7
    assert summary["visible_shell_size"] == 27
    assert summary["fiber_count"] == 9
    assert summary["fiber_size"] == 3
    assert summary["line_size"] == 4
    assert summary["lines_per_point"] == 4
    assert summary["projective_point_count"] == 40
    assert summary["edge_count"] == 240
    assert summary["e8_root_count"] == 240
    assert summary["cartan_rank_candidate"] == 8
    assert all(summary["exact_factorizations"].values())


def test_q3_spectral_uniqueness_summary_matches_corrected_live_packet() -> None:
    summary = q3_spectral_uniqueness_summary()

    assert summary["q"] == 3
    assert summary["srg_parameters"] == (40, 12, 2, 4)
    assert summary["adjacency_eigenpairs"] == ((12, 1), (2, 24), (-4, 15))
    assert summary["bipartite_zero_mode_count"] == 0
    assert summary["canonical_hamiltonian_eigenpairs"] == ((0, 1), (10, 24), (16, 15))
    assert summary["fourth_moment_per_vertex"] == 624
    assert summary["even_moment_characteristic_roots"] == (144, 16, 4)
    assert summary["even_moment_recurrence_coefficients"] == (164, -2944, 9216)
    assert summary["ihara_nontrivial_discriminants"] == (-40, -28)
    assert summary["expected_discriminants"] == (-40, -28)
    assert summary["zeta_regularised_determinant"] == 10**24 * 16**15
    assert all(summary["exact_factorizations"].values())


def test_q3_continuum_seed_summary_matches_exact_coefficient_seed() -> None:
    summary = q3_continuum_seed_summary()

    assert summary["q"] == 3
    assert summary["phi3"] == 13
    assert summary["phi6"] == 7
    assert summary["cartan_packet"] == 8
    assert summary["topological_packet"] == 56
    assert summary["continuum_eh_coefficient"] == 320
    assert summary["topological_coefficient"] == 2240
    assert summary["discrete_eh_coefficient"] == 12480
    assert summary["rank39"] == 39
    assert all(summary["exact_factorizations"].values())


def test_q3_master_lock_analysis_keeps_the_boundary_honest() -> None:
    records = {record["name"]: record for record in classify_q3_master_lock()}
    summary = analyze()
    theorem = summary["q3_master_lock_theorem"]

    assert records["q3_local_qutrit_kernel_lock"]["support_level"] == "repo-exact finite kernel"
    assert records["q3_spectral_ihara_uniqueness_lock"]["support_level"] == "repo-exact spectral uniqueness"
    assert records["q3_toroidal_continuum_seed_lock"]["support_level"] == "repo-exact continuum seed"
    assert records["q3_full_physical_realization_theorem"]["support_level"] == "not-yet-exact smooth realization theorem"

    assert summary["status"] == "ok"
    assert summary["record_names_exact_or_boundary"] == (
        "q3_local_qutrit_kernel_lock",
        "q3_spectral_ihara_uniqueness_lock",
        "q3_toroidal_continuum_seed_lock",
    )
    assert summary["record_names_open"] == ("q3_full_physical_realization_theorem",)
    assert theorem["the_local_kernel_exactly_realizes_the_q3_packet_1_3_9_27_40_240"] is True
    assert theorem["the_corrected_spectral_core_exactly_realizes_the_q3_lock"] is True
    assert theorem["the_continuum_seed_exactly_realizes_the_q3_packet_8_56_320_2240_12480"] is True
    assert theorem["the_q3_lock_is_now_overdetermined_across_local_spectral_and_continuum_seed_layers"] is True
    assert theorem["the_remaining_wall_is_not_finite_q_selection_but_smooth_realization"] is True
    assert "smooth continuum and dynamical realization" in summary["boundary_note"]
