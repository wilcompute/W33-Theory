from scripts.tomotope_toroidal_markov_generating_function_bridge import build_bridge


def test_generating_function_coefficients():
    payload = build_bridge(max_power=16)
    s = payload["summary"]

    assert s["numerator_c0_num"] == 6
    assert s["numerator_c0_den"] == 1
    assert s["numerator_c1_num"] == 0
    assert s["numerator_c1_den"] == 1
    assert (s["numerator_c2_num"], s["numerator_c2_den"]) == (-21, 32)

    assert (s["denominator_d0_num"], s["denominator_d0_den"]) == (1, 1)
    assert (s["denominator_d1_num"], s["denominator_d1_den"]) == (0, 1)
    assert (s["denominator_d2_num"], s["denominator_d2_den"]) == (-21, 64)
    assert (s["denominator_d3_num"], s["denominator_d3_den"]) == (-7, 512)


def test_generating_function_core_identities_hold():
    payload = build_bridge(max_power=16)
    ids = payload["identities"]

    assert ids["numerator_is_6_minus_21_over_32_z2"] is True
    assert ids["denominator_is_1_minus_21_over_64_z2_minus_7_over_512_z3"] is True
    assert ids["rational_function_matches_series"] is True
    assert ids["trace_series_equals_one_plus_moments"] is True
    assert payload["summary"]["all_identities_hold"] is True
