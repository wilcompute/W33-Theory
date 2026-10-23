"""Exact integer spectral check for the anchored W33 transvection toy Hamiltonian."""
from analysis.w33_20261022_anchored_transvection_hamiltonian import exact_model


def test_anchored_hamiltonian():
    r = exact_model()
    assert r["source_base_walk"].startswith("DCLXVIII")
    assert r["base_H0_spectrum"] == {"0":1,"24":15,"30":24}
    assert r["anchored_H_spectrum"] == {"0":1,"24":9,"27":6,"30":12,"33":12}
    assert r["T_trace_on_E2"] == 6
    assert r["T_trace_on_Eminus4"] == 6
    assert r["trace_H_squared"] == 33426
    assert r["exact_matrix_annihilator_verified"] is True
    assert r["dynamics_selects_anchor"] is False
