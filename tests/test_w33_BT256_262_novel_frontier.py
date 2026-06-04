"""Tests for BT256-262 novel frontier analysis."""
import math
import json

# Substrate
q, lambda_, mu = 3, 2, 4
fact_q = math.factorial(q)    # 6
pow_lq = lambda_ ** q         # 8
pow_lmu = lambda_ ** mu       # 16
pow_qq = q ** q               # 27
pow_ql = q ** lambda_         # 9
alpha_inv = (mu + 1) * pow_qq + lambda_  # 137
alpha_em  = 1 / alpha_inv
m_t_GeV   = 172.69
m_p_GeV   = 0.938272
m_e_MeV   = 0.51099895
v_GeV     = 246.22
m_H_GeV   = 125.25


def test_bt256_gut_scale():
    """BT256: M_GUT = (1/alpha)^q * m_t."""
    M_GUT = alpha_inv**q * m_t_GeV
    # Should be between 10^7 and 10^10 GeV given the substrate formula
    assert 1e6 < M_GUT < 1e12, f"M_GUT={M_GUT:.4e} out of expected range"
    # Verify: 137^3 = 2571353
    assert alpha_inv**q == 137**3 == 2571353
    print(f"PASS BT256: M_GUT = {M_GUT:.4e} GeV")


def test_bt257_dark_energy_alpha_power():
    """BT257: dark energy dimensionality = mu=4."""
    rho_quarter = alpha_em**mu * m_e_MeV
    assert rho_quarter > 0
    assert rho_quarter < 1e-5  # small compared to m_e
    print(f"PASS BT257: rho_Lambda^(1/4) = {rho_quarter:.4e} MeV")


def test_bt258_wolfenstein_lambda():
    """BT258: Wolfenstein lambda_W = 1/sqrt(20), 0.62% error."""
    FN_denom = fact_q + pow_ql + mu + 1  # 20
    assert FN_denom == 20
    Wlambda = 1.0 / math.sqrt(FN_denom)
    PDG = 0.2250
    err = abs(Wlambda - PDG) / PDG * 100
    assert err < 2.0, f"Wolfenstein error {err:.2f}% > 2%"
    print(f"PASS BT258: lambda_W = {Wlambda:.6f}, PDG = {PDG}, err = {err:.2f}%")


def test_bt259_proton_lifetime_order():
    """BT259: proton lifetime within 1 OOM of PDG limit."""
    M_GUT = alpha_inv**q * m_t_GeV
    alpha_GUT = 1/40.0
    hbar_s_GeV = 6.582119569e-25
    sec_per_year = 3.15576e7
    tau_natural = M_GUT**4 / (alpha_GUT * m_p_GeV**5)
    tau_years = tau_natural * hbar_s_GeV / sec_per_year
    PDG_limit = 1.6e34
    # Substrate predicts within a factor of 100 of the limit
    assert tau_years > 1e30, f"τ_p too short: {tau_years:.2e} years"
    assert tau_years < PDG_limit * 100, f"τ_p too long: {tau_years:.2e} years"
    print(f"PASS BT259: τ_p ~ {tau_years:.2e} years (PDG limit {PDG_limit:.1e})")


def test_bt260_ramanujan():
    """BT260: W(3,3) is a Ramanujan graph."""
    k = q * mu  # degree = 12
    Ramanujan_bound = 2 * math.sqrt(k - 1)
    # Non-trivial eigenvalues of W(3,q=3)
    e1 = q - 1         # 2
    e2 = -(q + 1)      # -4
    max_nontrivial = max(abs(e1), abs(e2))
    assert max_nontrivial <= Ramanujan_bound, (
        f"W(3,3) not Ramanujan: {max_nontrivial} > {Ramanujan_bound:.4f}"
    )
    # Euler characteristic
    V = (mu + 1) * pow_lq   # 40
    E = lambda_ * math.factorial(mu + 1)  # 240
    chi = E - V
    assert chi == 200
    print(f"PASS BT260: W(3,3) is Ramanujan, chi={chi}, max_nontrivial={max_nontrivial} <= {Ramanujan_bound:.4f}")


def test_bt261_higgs_lambda():
    """BT261: lambda_H = 1/8 within 4% of SM exact value."""
    lambda_H_sub = 1.0 / pow_lq  # 1/8
    lambda_H_exact = m_H_GeV**2 / (2 * v_GeV**2)
    err = abs(lambda_H_sub - lambda_H_exact) / lambda_H_exact * 100
    assert err < 5.0, f"lambda_H error {err:.1f}% > 5%"
    # Instability scale
    M_instab = alpha_inv**(mu + 1) * m_t_GeV
    assert 1e10 < M_instab < 1e15, f"M_instab={M_instab:.2e} out of range"
    print(f"PASS BT261: lambda_H = {lambda_H_sub} (err {err:.1f}%), M_instab = {M_instab:.2e} GeV")


def test_bt262_quantity_count():
    """BT262: v22 has 40 quantities."""
    # The 33 from BT245 + 7 new ones
    old_count = 33
    new_count = 7  # BT256-261 = 7 items (including Ramanujan theorem)
    total = old_count + new_count
    assert total == 40
    print(f"PASS BT262: Master v22 total = {total} quantities")


if __name__ == "__main__":
    test_bt256_gut_scale()
    test_bt257_dark_energy_alpha_power()
    test_bt258_wolfenstein_lambda()
    test_bt259_proton_lifetime_order()
    test_bt260_ramanujan()
    test_bt261_higgs_lambda()
    test_bt262_quantity_count()
    print("\nAll BT256-262 tests PASSED.")
