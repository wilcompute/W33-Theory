"""Controls for the exact three-mixed-loop native Maxwell compression."""
from analysis.w33_20261028_three_mixed_loop_minimal_maxwell import certificate


def test_native_exact_rank_three_positivity_and_cone():
    c = certificate()
    assert c["H_endpoint_rank"] == 3
    assert c["both_endpoints_positive_semidefinite_rank_three"]
    assert c["minimal_extra_flux_channels"] == 3
    assert c["positive_K_leading_principal_minors"] == ["25/9", "200/27", "16/27"]
    assert c["four_variable_symbol_identity"].startswith("(R*C(n))")


def test_actual_native_bloch_rank_and_ward_at_three_primes():
    c = certificate()
    for sample in c["three_mixed_channel_bloch_controls"]:
        assert sample["short_rank"] == 105
        assert sample["three_mixed_rank"] == 108
        assert sample["gradient_rank"] == 27
        assert sample["Ward_identity_exact"] is True
        assert sample["three_individual_rank_histogram"] == {"107": 4, "108": 16}


def test_compact_positive_nine_harmonics():
    c = certificate()["compact_potential"]
    assert len(c["charge_vectors"]) == 6
    assert len(c["positive_weights"]) == 6
    assert c["number_of_cosine_harmonics"] == 9
    assert c["unit_harmonic_weight"] == "1/10000"
