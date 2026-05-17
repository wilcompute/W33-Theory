from fractions import Fraction

from scripts.tomotope_toroidal_markov_cubic_recurrence_bridge import build_bridge


def test_cubic_recurrence_summary_values():
    payload = build_bridge(max_power=12)
    summary = payload["summary"]

    assert summary["checked_max_power"] == 12
    assert (summary["recurrence_coeff_a_num"], summary["recurrence_coeff_a_den"]) == (21, 64)
    assert (summary["recurrence_coeff_b_num"], summary["recurrence_coeff_b_den"]) == (7, 512)
    assert (summary["m0_num"], summary["m0_den"]) == (6, 1)
    assert (summary["m1_num"], summary["m1_den"]) == (0, 1)
    assert (summary["m2_num"], summary["m2_den"]) == (21, 16)


def test_trace_reconstruction_rows_match_exactly():
    payload = build_bridge(max_power=10)
    for row in payload["trace_rows"]:
        lhs = Fraction(row["trace_pn"]["numerator"], row["trace_pn"]["denominator"])
        rhs = Fraction(
            row["one_plus_nontrivial_moment"]["numerator"],
            row["one_plus_nontrivial_moment"]["denominator"],
        )
        assert lhs == rhs


def test_all_recurrence_identities_hold():
    payload = build_bridge(max_power=12)
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
