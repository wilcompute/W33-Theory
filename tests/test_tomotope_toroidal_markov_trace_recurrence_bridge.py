from scripts.tomotope_toroidal_markov_trace_recurrence_bridge import build_bridge


def test_trace_recurrence_coefficients_and_seeds():
    payload = build_bridge(max_power=12)
    s = payload["summary"]

    assert (s["coeff_r1_num"], s["coeff_r1_den"]) == (1, 1)
    assert (s["coeff_r2_num"], s["coeff_r2_den"]) == (21, 64)
    assert (s["coeff_r3_num"], s["coeff_r3_den"]) == (-161, 512)
    assert (s["coeff_r4_num"], s["coeff_r4_den"]) == (-7, 512)

    assert (s["seed_t1_num"], s["seed_t1_den"]) == (1, 1)
    assert (s["seed_t2_num"], s["seed_t2_den"]) == (37, 16)


def test_trace_recurrence_identities_hold():
    payload = build_bridge(max_power=12)
    ids = payload["identities"]

    assert ids["denominator_shape_matches_expected"] is True
    assert ids["trace_recurrence_matches_matrix_traces"] is True
    assert payload["summary"]["all_identities_hold"] is True
