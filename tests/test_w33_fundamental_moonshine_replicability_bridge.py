from exploration.w33_fundamental_moonshine_replicability_bridge import build_summary


def test_fundamental_moonshine_replicability_theorem() -> None:
    summary = build_summary()
    assert all(summary["fundamental_moonshine_replicability_theorem"].values())


def test_fundamental_moonshine_replicability_prime_rows() -> None:
    summary = build_summary()
    rows = summary["fundamental_moonshine_replicability_dictionary"]["prime_rows"]
    by_name = {row["class_name"]: row for row in rows}

    assert by_name["2A"]["faber_coeffs"] == [-8744, 0]
    assert by_name["3A"]["faber_coeffs"] == [-26016, -2349, 0]
    assert by_name["2A"]["theorems"]["faber_top_lower_coefficient_is_minus_p_times_a1"] is True
    assert by_name["3A"]["theorems"]["faber_top_lower_coefficient_is_minus_p_times_a1"] is True
    assert by_name["3A"]["theorems"]["faber_next_lower_coefficient_is_minus_p_times_a2"] is True


def test_fundamental_moonshine_replicability_rhs_is_1A_sourced() -> None:
    summary = build_summary()
    rows = summary["fundamental_moonshine_replicability_dictionary"]["prime_rows"]
    by_name = {row["class_name"]: row for row in rows}

    # RHS combines J(q^p) and p * (T_pA | U_p). At q^(-p) the U_p piece
    # vanishes and J(q^p) contributes its q^{-1} pole, so RHS[-p] = 1.
    rhs_2a = by_name["2A"]["rhs_q_exponents"]
    assert rhs_2a["-2"] == 1
    # At q^2 for p=2: 196884 (from J(q^p) q-coefficient of q^2)
    # plus 2 * a_4(T_2A) = 2 * 10698752 = 21397504, giving 21594388.
    assert rhs_2a["2"] == 196884 + 2 * 10698752

    rhs_3a = by_name["3A"]["rhs_q_exponents"]
    assert rhs_3a["-3"] == 1
    # At q^3 for p=3: 196884 (from J(q^p) at q^3) + 3 * a_9(T_3A).
    # We pin the total as computed from the full identity.
    assert rhs_3a["3"] == 864431487
