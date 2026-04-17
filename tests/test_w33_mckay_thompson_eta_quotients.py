from exploration.w33_mckay_thompson_eta_quotients import (
    ETA_QUOTIENT_PARAMS,
    T_pA_REFERENCE_COEFFS,
    derive_all,
    mckay_thompson_T_pA,
)


def test_mckay_thompson_summary_chain() -> None:
    summary = derive_all()
    assert all(summary["summary_chain"].values())


def test_mckay_thompson_has_unit_pole_and_zero_constant() -> None:
    for p, _ in ETA_QUOTIENT_PARAMS:
        coefs, _ = mckay_thompson_T_pA(p, N=6)
        assert int(coefs[0]) == 1
        assert int(coefs[1]) == 0


def test_mckay_thompson_constant_offsets_equal_k() -> None:
    for p, k in ETA_QUOTIENT_PARAMS:
        _, c_p = mckay_thompson_T_pA(p, N=6)
        assert int(c_p) == k


def test_mckay_thompson_first_five_reference_coefficients() -> None:
    for p, expected in T_pA_REFERENCE_COEFFS.items():
        coefs, _ = mckay_thompson_T_pA(p, N=6)
        got = [int(coefs[2 + j]) for j in range(len(expected))]
        assert got == expected


def test_mckay_thompson_13A_fifth_coefficient_is_258() -> None:
    coefs, _ = mckay_thompson_T_pA(13, N=6)
    assert int(coefs[6]) == 258
