from __future__ import annotations

from fractions import Fraction

from scripts.w33_zeta_loop_equilibrium_audit import (
    closed_histories_per_directed_edge,
    hashimoto_power_sum,
    hashimoto_root_modulus_squared,
    loop_closure_probability,
    loop_partition_trace,
    ramanujan_equilibrium_noise,
    w33_loop_packet,
    zeta_log_coefficient,
    zeta_loop_equilibrium_summary,
)


def test_cxxix_hashimoto_packet_matches_w33_loop_carrier() -> None:
    packet = w33_loop_packet()

    assert packet == {
        "vertex_count": 40,
        "degree": 12,
        "undirected_edge_count": 240,
        "directed_edge_count": 480,
        "branch_count": 11,
        "ihara_prefactor_exponent": 200,
    }


def test_cxxix_hashimoto_trace_values_match_remote_part_cxxviii() -> None:
    assert [loop_partition_trace(n) for n in range(7)] == [
        480,
        0,
        0,
        960,
        13920,
        181440,
        1818240,
    ]


def test_cxxix_loop_condition_first_closes_on_triangle_probability() -> None:
    assert closed_histories_per_directed_edge(1) == 0
    assert closed_histories_per_directed_edge(2) == 0
    assert closed_histories_per_directed_edge(3) == 2
    assert loop_closure_probability(3) == Fraction(2, 11**3)


def test_cxxix_zeta_log_coefficients_are_hashimoto_traces_over_n() -> None:
    assert zeta_log_coefficient(3) == Fraction(960, 3) == 320
    assert zeta_log_coefficient(4) == Fraction(13920, 4) == 3480
    assert zeta_log_coefficient(5) == Fraction(181440, 5)
    assert zeta_log_coefficient(6) == Fraction(1818240, 6) == 303040


def test_cxxix_probability_splits_into_uniform_equilibrium_plus_noise() -> None:
    equilibrium = Fraction(1, 480)

    for n in range(1, 13):
        assert loop_closure_probability(n) == (
            equilibrium + ramanujan_equilibrium_noise(n)
        )

    assert ramanujan_equilibrium_noise(3) == Fraction(2, 11**3) - equilibrium
    assert abs(ramanujan_equilibrium_noise(12)) < abs(ramanujan_equilibrium_noise(3))


def test_cxxix_ramanujan_noise_is_supported_by_nontrivial_hashimoto_circle() -> None:
    assert hashimoto_power_sum(2, 2) == 2 * 2 - 2 * 11
    assert hashimoto_power_sum(-4, 2) == (-4) * (-4) - 2 * 11
    assert hashimoto_root_modulus_squared(2) == 11
    assert hashimoto_root_modulus_squared(-4) == 11


def test_cxxix_summary_packages_remote_zeta_loop_equilibrium_theorem() -> None:
    summary = zeta_loop_equilibrium_summary(max_n=12)
    theorem = summary["theorem"]

    assert summary["ihara_determinant_packet"] == {
        "prefactor": "(1-u^2)^200",
        "trivial_factor": "(1-u)(1-11u)",
        "positive_sector_factor": "(1-2u+11u^2)^24",
        "negative_sector_factor": "(1+4u+11u^2)^15",
    }
    assert summary["first_trace_values_Z0_to_Z6"] == (
        480,
        0,
        0,
        960,
        13920,
        181440,
        1818240,
    )
    assert theorem["zeta_log_coefficients_are_trace_over_n"] is True
    assert theorem["first_nonzero_loop_length"] == 3
    assert theorem["first_nonzero_loop_probability"] == "2/1331"
    assert theorem["equilibrium_term"] == "1/480"
    assert theorem["nontrivial_roots_lie_on_hashimoto_ramanujan_circle"] is True
    assert theorem["loop_probability_splits_as_uniform_plus_noise"] is True
