from exploration.w33_fundamental_moonshine_algebra_bridge import build_summary


def test_fundamental_moonshine_algebra_theorem() -> None:
    summary = build_summary()
    assert all(summary["fundamental_moonshine_algebra_theorem"].values())


def test_fundamental_prime_weight_ladder() -> None:
    summary = build_summary()
    dictionary = summary["fundamental_moonshine_algebra_dictionary"]

    assert dictionary["prime_weight_ladder"] == [24, 12, 6, 4, 2]
    assert dictionary["prime_atkin_lehner_norms"] == [4096, 729, 125, 49, 13]


def test_fundamental_prime_rows_have_exact_trace_norm_and_quadratic_identities() -> None:
    summary = build_summary()
    rows = summary["fundamental_moonshine_algebra_dictionary"]["prime_pA_quadratic_rows"]

    for row in rows:
        assert row["theorems"]["genus_zero_holds"] is True
        assert row["theorems"]["constant_shift_equals_k"] is True
        assert row["theorems"]["trace_identity_holds"] is True
        assert row["theorems"]["norm_identity_holds"] is True
        assert row["theorems"]["quadratic_identity_holds"] is True
        assert row["product_X_p_Y_p_q0_to_q5"][0] == row["norm_p_to_k_over_2"]
        assert row["product_X_p_Y_p_q0_to_q5"][1:] == [0] * row["stable_max_exponent"]
        assert row["quadratic_residual_q_minus_2_to_q5"] == [0] * (row["stable_max_exponent"] + 3)


def test_fundamental_oneA_and_twoA_are_on_the_same_spine() -> None:
    summary = build_summary()
    one_a = summary["fundamental_moonshine_algebra_dictionary"]["oneA_linear_quotient"]
    rows = summary["fundamental_moonshine_algebra_dictionary"]["prime_pA_quadratic_rows"]
    row_2a = next(row for row in rows if row["p"] == 2)

    assert one_a["744_split"]["sum"] == 744
    assert one_a["first_moonshine_split"]["sum"] == 196884
    assert row_2a["norm_p_to_k_over_2"] == 4096
    assert row_2a["hauptmodul_constant_shift"] == 24
