from __future__ import annotations

from fractions import Fraction

from scripts.w33_normalization_bridge_audit import (
    adjacency_even_moment_per_vertex,
    analyze,
    lift_even_moment,
    normalization_bridge_record,
    normalization_factor,
    symbolic_bridge_summary,
    zero_mode_count,
)


def test_symbolic_bridge_theorem_is_exact() -> None:
    symbolic = symbolic_bridge_summary()
    theorem = symbolic["bridge_theorem_exact"]

    assert theorem["lift_modes_equal_q_minus_1_times_vertex_count"] is True
    assert theorem["zero_modes_equal_q_minus_3_times_vertex_count"] is True
    assert theorem["rho_nonzero_is_2_over_q_minus_1"] is True
    assert theorem["rho_zero_is_q_minus_3_over_q_minus_1"] is True
    assert theorem["m2_bridge_holds"] is True
    assert theorem["m4_bridge_holds"] is True
    assert theorem["m2_gap_is_exactly_zero_fraction_times_k"] is True


def test_q3_is_exactly_the_zero_mode_free_factor_one_case() -> None:
    record = normalization_bridge_record(3)

    assert record["point_graph_vertex_count"] == 40
    assert record["lift_mode_count"] == 80
    assert record["zero_mode_count"] == 0
    assert record["rho_nonzero"]["exact"] == "1"
    assert record["rho_zero"]["exact"] == "0"
    assert record["normalization_factor"]["exact"] == "1"
    assert record["moments"]["adjacency_m2"]["exact"] == "12"
    assert record["moments"]["lift_m2"]["exact"] == "12"
    assert record["moments"]["adjacency_m4"]["exact"] == "624"
    assert record["moments"]["lift_m4"]["exact"] == "624"


def test_bridge_scales_even_moments_by_the_nonzero_mode_fraction() -> None:
    assert normalization_factor(4) == Fraction(2, 3)
    assert zero_mode_count(4) == 85
    assert adjacency_even_moment_per_vertex(4, 1) == 20
    assert lift_even_moment(4, 1) == Fraction(40, 3)
    assert adjacency_even_moment_per_vertex(5, 2) == 5880
    assert lift_even_moment(5, 2) == 2940
    assert adjacency_even_moment_per_vertex(7, 1) == 56
    assert lift_even_moment(7, 1) == Fraction(56, 3)


def test_audit_packages_the_bridge_as_the_explanation_of_the_q3_uniqueness_gap() -> None:
    payload = analyze()
    theorem = payload["bridge_theorem"]

    assert theorem["the_lift_normalization_is_exactly_the_nonzero_mode_fraction"] is True
    assert theorem["the_zero_mode_fraction_is_exactly_one_minus_the_nonzero_fraction"] is True
    assert theorem["q3_is_the_unique_zero_mode_free_case_in_the_sample"] is True
    assert theorem["q3_is_the_unique_factor_1_case_in_the_sample"] is True
    assert theorem["the_april_m2_uniqueness_gap_is_exactly_the_normalization_gap"] is True
