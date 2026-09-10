#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_heawood_outer_involution_fixed_census import build_result as build_outer  # noqa: E402
from w33_heawood_stabilizer96_presentation_lattice import build_result as build_group  # noqa: E402
from w33_marcelis_trace_schubert_general import build_result as build_schubert  # noqa: E402
from w33_marcelis_observer_quotient_dynamics import build_result as build_observer  # noqa: E402


def test_outer_fixed_c6_spread_pair_census() -> None:
    data = build_outer()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["cycle_histograms"]["Heawood_C6_components"] == {"1": 12, "2": 129}
    assert data["cycle_histograms"]["four_intersection_spread_pairs"] == {"1": 12, "2": 129}
    assert data["fixed_objects"]["fixed_four_intersection_pair_count"] == 12
    assert sum(data["fixed_objects"]["fixed_pair_modes"].values()) == 12
    assert len(data["fixed_pair_rows"]) == 12


def test_order96_presentation_and_normal_lattice() -> None:
    data = build_group()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["structure"]["order"] == 96
    assert data["structure"]["center_order"] == 2
    assert data["structure"]["derived_order"] == 24
    assert data["structure"]["derived_structure"] == "C2 x A4"
    assert data["structure"]["abelianization_structure"] == "C2 x C2"
    assert all(data["presentation"]["relation_checks"].values())
    assert len(data["normal_subgroup_lattice"]["index2_nodes"]) == 3
    assert data["normal_subgroup_lattice"]["normal_subgroup_count"] >= 9


def test_all_n_schubert_trace_laws() -> None:
    data = build_schubert()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["theorem"]["point_fibre_law"] == "|tau_omega^-1(b)|=2^(n-j) for b in F_j\\F_{j+1}"
    assert data["theorem"]["line_lift_law"] == "N_line(ell)=2^(n-1-j) for ell<=F_j and ell not<=F_{j+1}"
    assert [row["n"] for row in data["exhaustive_point_checks"]] == [1, 2, 3, 4, 5, 6]
    assert [row["n"] for row in data["exhaustive_line_checks"]] == [1, 2, 3, 4, 5]
    assert data["exhaustive_line_checks"][2]["line_preserving_GF4_mass"] == 125
    assert data["exhaustive_line_checks"][4]["PGn4_lines"] == 93093
    assert data["exhaustive_line_checks"][4]["binary_line_images"] == 651
    assert data["exhaustive_line_checks"][4]["line_preserving_GF4_mass"] == 9021
    assert data["constructive_line_proof"]["local_solution_table_encoding_0_1_omega_omega2"] == {
        "00": [[0, 0], [3, 0]],
        "01": [[0, 1], [3, 1]],
        "10": [[1, 0], [2, 0]],
        "11": [[1, 1], [2, 1]],
    }


def test_deterministic_global_stochastic_observer_quotient() -> None:
    data = build_observer()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    model = data["n3_one_step_model"]
    assert model["status"] == "PASS"
    assert all(model["checks"].values())
    assert model["observer_kernel"]["deterministic_macro_states"] == 7
    assert model["observer_kernel"]["stochastic_macro_states"] == 8
    assert model["observer_kernel"]["branch_count_histogram"] == {
        "1": 7,
        "5": 4,
        "7": 2,
        "8": 2,
    }
    assert model["observer_kernel"]["row_entropy_histogram"] == {
        "0": 7,
        "11/4": 2,
        "2": 4,
        "3": 2,
    }
    assert model["observer_kernel"]["H_Bprime_given_B_bits_exact"] == "156/85"
    assert model["observer_kernel"]["P_guess_Bprime_given_B"] == "43/85"
    assert model["side_information_key"]["H_K_given_B_bits_exact"] == "228/85"
    assert model["side_information_key"]["P_guess_S_given_B"] == "3/17"
    assert model["side_information_key"]["H_Bprime_given_B_K_bits"] == 0
    assert data["checks"]["flag_horizon_exhaustive_n1_through_n5"] is True


if __name__ == "__main__":
    test_outer_fixed_c6_spread_pair_census()
    test_order96_presentation_and_normal_lattice()
    test_all_n_schubert_trace_laws()
    test_deterministic_global_stochastic_observer_quotient()
    print("Heawood/Schubert/observer continuation tests passed")
