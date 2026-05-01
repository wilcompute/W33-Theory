def test_rg_flow_sanity():
    from scripts.w33_mass_synthesis import derive_yukawas_from_triads
    from scripts.w33_rg_flow import integrate_rg

    yuk = derive_yukawas_from_triads()
    out = integrate_rg(yuk, steps=1000)

    # Sanity checks (order-of-magnitude / hierarchy)
    assert 1.0 < out["m_t_MZ_GeV"] < 1000.0
    assert 0.1 < out["m_b_MZ_GeV"] < 50.0
    assert 0.1 < out["m_tau_MZ_GeV"] < 10.0

    # Yukawa hierarchy preserved qualitatively
    assert out["y_t_MZ"] >= out["y_b_MZ"] if "y_b_MZ" in out else True
