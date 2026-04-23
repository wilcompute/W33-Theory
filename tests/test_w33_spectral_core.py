from __future__ import annotations

from fractions import Fraction

from scripts.w33_spectral_core import (
    W33,
    family_fourth_moment_formula,
    family_fourth_moment_per_vertex,
    get_w33_spectral_core,
    moment_recurrence_coeffs,
    ramanujan_bound_check,
    spec_zeta,
    spectral_moment,
)


def test_w33_spectral_core_self_verifies_exact_kernel_spectrum() -> None:
    core = get_w33_spectral_core()

    assert core.self_verified is True
    assert core.adjacency_eigenpairs == ((12, 1), (2, 24), (-4, 15))
    assert core.bipartite_lift_positive_eigenpairs == ((12, 1), (4, 15), (2, 24))
    assert core.bipartite_lift_negative_eigenpairs == ((-2, 24), (-4, 15), (-12, 1))
    assert core.bipartite_lift_zero_mode_count == 0
    assert core.bipartite_lift_mode_count == 80
    assert core.canonical_hamiltonian_eigenpairs == ((0, 1), (10, 24), (16, 15))


def test_fourth_moment_family_formula_and_q3_specialization_are_exact() -> None:
    expected = {
        2: 114,
        3: 624,
        4: 2180,
        5: 5880,
        7: 27104,
    }
    for q_value, value in expected.items():
        assert family_fourth_moment_per_vertex(q_value) == value
        assert family_fourth_moment_formula(q_value) == value

    core = get_w33_spectral_core()
    assert int(core.adjacency_moment_per_vertex(4)) == 624


def test_even_moment_recurrence_has_roots_144_16_4_and_holds_on_live_sequence() -> None:
    core = get_w33_spectral_core()

    assert core.even_moment_characteristic_roots == (144, 16, 4)
    assert core.even_moment_recurrence_coefficients == (164, -2944, 9216)
    assert core.even_moment_recurrence_formula == "a_n = 164*a_(n-1) - 2944*a_(n-2) + 9216*a_(n-3)"
    assert [core.even_adjacency_moment(index) for index in range(5)] == [
        40,
        480,
        24960,
        3048960,
        430970880,
    ]
    assert core.verify_even_moment_recurrence(8) is True


def test_canonical_hamiltonian_zeta_and_ihara_packets_are_exact() -> None:
    core = get_w33_spectral_core()

    assert core.canonical_hamiltonian_zeta(1) == Fraction(267, 80)
    assert core.canonical_hamiltonian_zeta(2) == Fraction(1911, 6400)
    assert core.canonical_hamiltonian_zeta(-1) == Fraction(480, 1)
    assert core.zeta_regularised_determinant == 10**24 * 16**15

    assert core.ihara_cycle_rank == 200
    assert core.ihara_k_minus_1 == 11
    assert core.ihara_trivial_factor_roots == (Fraction(1, 11), Fraction(1, 1))
    assert core.ihara_nontrivial_discriminants == (-40, -28)


def test_legacy_api_surface_remains_available_for_april_2026_scripts() -> None:
    assert W33.k == 12
    assert W33.v == 40
    assert W33.f == 24
    assert W33.g == 15
    assert W33.Phi3 == 13
    assert W33.Phi4 == 10
    assert W33.Phi6 == 7
    assert spectral_moment(2) == Fraction(12, 1)
    assert spectral_moment(4) == Fraction(624, 1)
    assert abs(spec_zeta(1) - (19 / 48)) < 1e-12
    assert abs(spec_zeta(2) - (25 / 144)) < 1e-12
    assert moment_recurrence_coeffs() == (164, 2944, 9216)
    assert ramanujan_bound_check() is True


def test_summary_surface_matches_the_verified_spectral_packet() -> None:
    summary = get_w33_spectral_core().to_dict()

    assert summary["status"] == "ok"
    assert summary["srg_parameters"] == (40, 12, 2, 4)
    assert summary["fourth_moment"]["sample_values"] == {
        2: 114,
        3: 624,
        4: 2180,
        5: 5880,
        7: 27104,
    }
    assert summary["canonical_hamiltonian_zeta"]["zeta_1"] == {
        "exact": "267/80",
        "float": 267 / 80,
    }
    assert summary["ihara_determinant"] == {
        "cycle_rank": 200,
        "k_minus_1": 11,
        "trivial_factor_roots": ("1/11", "1"),
        "nontrivial_discriminants": (-40, -28),
    }
    assert summary["legacy_api"]["spectral_moment_2"] == "12"
    assert summary["legacy_api"]["spectral_moment_4"] == "624"
    assert abs(summary["legacy_api"]["spec_zeta_1"] - spec_zeta(1)) < 1e-15
    assert abs(summary["legacy_api"]["spec_zeta_2"] - spec_zeta(2)) < 1e-15
    assert abs(summary["legacy_api"]["spec_zeta_11"] - spec_zeta(11)) < 1e-18
    assert summary["self_verified"] is True
