from scripts.tomotope_toroidal_markov_trace_generating_function_bridge import build_bridge


def test_trace_generating_function_denominator_shape():
    payload = build_bridge(max_power=10)
    s = payload["summary"]

    assert (s["denominator_d0_num"], s["denominator_d0_den"]) == (1, 1)
    assert (s["denominator_d1_num"], s["denominator_d1_den"]) == (-1, 1)
    assert (s["denominator_d2_num"], s["denominator_d2_den"]) == (-21, 64)
    assert (s["denominator_d3_num"], s["denominator_d3_den"]) == (161, 512)
    assert (s["denominator_d4_num"], s["denominator_d4_den"]) == (7, 512)


def test_trace_generating_function_identities_hold():
    payload = build_bridge(max_power=10)
    ids = payload["identities"]

    assert ids["trace_rational_series_matches_coefficients"] is True
    assert ids["trace_linear_term_is_one"] is True
    assert payload["summary"]["all_identities_hold"] is True
