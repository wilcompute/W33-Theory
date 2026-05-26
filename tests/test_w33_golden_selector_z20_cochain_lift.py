from __future__ import annotations

from analysis.w33_golden_selector_z20_cochain_lift import golden_selector_z20_cochain_lift_packet


PACKET = golden_selector_z20_cochain_lift_packet()


def test_mccxlvi_draft_obstruction_counts_are_substrate() -> None:
    obstruction = PACKET["draft_obstruction"]

    assert obstruction["line_count"] == 40
    assert obstruction["directed_transport_edges"] == 480
    assert obstruction["undirected_transport_edges"] == 240
    assert obstruction["ordered_quadrangles"] == 12960
    assert obstruction["ordered_violations"] == 864
    assert obstruction["local_violations"] == 0
    assert obstruction["nonlocal_violations"] == 864
    assert obstruction["violation_rate"] == "1/15"
    assert obstruction["substrate_identities"]["ordered_violations"] == "2^(mu+1)*q^3 = 32*27 = 864"


def test_mccxlvi_unique_cycle_system() -> None:
    system = PACKET["cochain_system"]

    assert system["variables"] == 240
    assert system["unique_quadrangles"] == 1620
    assert system["unique_failures"] == 108
    assert system["rank"] == 200
    assert system["free_dimension"] == 40
    assert system["consistent"] is True


def test_mccxlvi_z20_half_period_lift_corrects_flatness() -> None:
    lift = PACKET["z20_lift"]

    assert lift["pisano_period_pi_5"] == 20
    assert lift["phase_values"] == [0, 10]
    assert lift["phase_sum_mod20_profile"] == {"0": 1512, "10": 108}
    assert lift["corrected_unique_failures"] == 0
    assert lift["corrected_ordered_failures"] == 0


def test_mccxlvi_gauge_fixed_solution_profile() -> None:
    lift = PACKET["z20_lift"]

    assert lift["selected_edge_count"] == 54
    assert lift["selected_edge_formula"] == "2*q^3 = 54 for this deterministic gauge-fixed solution"
    assert lift["selected_sigma_profile"] == {"-1": 27, "1": 27}
    assert lift["selected_line_degree_profile"] == {"0": 7, "2": 27, "9": 6}


def test_mccxlvi_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 16
    assert all(PACKET["checks"].values())
