from __future__ import annotations

from scripts.w33_exact_flavor_spine_bridge import analyze, classify_exact_flavor_spine


def test_exact_flavor_spine_bridge_closes_the_cabibbo_reconciliation() -> None:
    payload = analyze()
    theorem = payload["exact_flavor_spine_theorem"]

    assert theorem["the_local_cabibbo_generator_is_exactly_q_over_phi3"] is True
    assert theorem["the_global_observable_lambda_is_exactly_q_squared_over_v"] is True
    assert theorem["the_global_lambda_equals_the_local_generator_times_the_w33_visibility_factor"] is True
    assert theorem["the_global_lambda_outperforms_the_raw_local_tangent_projection_against_current_pdg_data"] is True
    assert theorem["the_exact_levi_packet_uses_the_same_lambda_as_the_global_size_bridge"] is True
    assert theorem["the_exact_pmns_packet_is_the_incidence_geometry_ratio_4_13_7_13_2_91"] is True


def test_exact_flavor_spine_bridge_keeps_the_canonical_routes_explicit() -> None:
    records = {record["name"]: record for record in classify_exact_flavor_spine()}

    local = records["local_generator_backbone"]["evidence"]
    global_cabibbo = records["global_cabibbo_visibility_bridge"]["evidence"]
    levi = records["levi_ckm_packet"]["evidence"]
    pmns = records["incidence_pmns_packet"]["evidence"]

    assert local["tan_theta_c"]["exact"] == "3/13"
    assert global_cabibbo["visibility_factor"]["exact"] == "39/40"
    assert global_cabibbo["lambda_global"]["exact"] == "9/40"
    assert global_cabibbo["v_minus_1"] == global_cabibbo["q_phi3"] == 39
    assert global_cabibbo["global_lambda_relative_error"] < global_cabibbo["local_tangent_sine_relative_error"]

    assert levi["levi_packet"]["lambda"]["exact"] == "9/40"
    assert abs(levi["levi_packet"]["A"] - 0.8223750740589154) < 1e-15
    assert round(levi["levi_packet"]["Vcb"], 6) == 0.041633
    assert round(levi["levi_packet"]["Vub"], 6) == 0.003818
    assert levi["Vcb_relative_error"] < 0.01
    assert levi["Vub_relative_error"] < 0.03
    assert levi["J_relative_error"] < 0.03
    assert levi["delta_relative_error"] < 0.02

    assert round(pmns["exact_pmns"]["sin2_theta12"], 6) == 0.307692
    assert round(pmns["exact_pmns"]["sin2_theta23"], 6) == 0.538462
    assert round(pmns["exact_pmns"]["sin2_theta13"], 6) == 0.021978
    assert pmns["solar_relative_error"] < 0.01
    assert pmns["reactor_relative_error"] < 0.03
    assert pmns["atmospheric_relative_error"] > pmns["solar_relative_error"]
