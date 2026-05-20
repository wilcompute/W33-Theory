"""Tests for W(3,3) Kirchhoff index and spanning tree count (MCLI)."""
from fractions import Fraction
from analysis.w33_kirchhoff_spanning_tree import kirchhoff_spanning_tree_packet


def _frac(entry):
    return Fraction(int(entry["numerator"]), int(entry["denominator"]))


def test_kirchhoff_index_value():
    p = kirchhoff_spanning_tree_packet()
    Kf = _frac(p["kirchhoff_index"]["K_f"])
    assert Kf == Fraction(267, 2)


def test_kirchhoff_kemeny_bridge():
    p = kirchhoff_spanning_tree_packet()
    br = p["kemeny_kirchhoff_bridge"]
    assert br["K_f_equals_vK_k"]
    Kf = _frac(br["K_f"])
    Kf2 = _frac(br["K_f_from_Kv_k"])
    assert Kf == Kf2 == Fraction(267, 2)


def test_kirchhoff_volume_identity():
    """K_f * k = v^2 + r = Kv = 1602"""
    p = kirchhoff_spanning_tree_packet()
    br = p["kemeny_kirchhoff_bridge"]
    assert br["kirchhoff_volume_identity"]
    assert _frac(br["Kf_k"]) == Fraction(1602, 1)
    assert br["v2_plus_r"] == 1602


def test_normalized_bridge():
    """K_f/v = K/k"""
    p = kirchhoff_spanning_tree_packet()
    br = p["kemeny_kirchhoff_bridge"]
    assert br["normalized_bridge_Kf_v_equals_K_k"]
    assert _frac(br["K_f_norm"]) == _frac(br["K_norm"]) == Fraction(267, 80)


def test_foster_theorem():
    """Foster: K_f = v * Σ_{j>=2} 1/mu_j"""
    p = kirchhoff_spanning_tree_packet()
    ls = p["laplacian_spectral_sum"]
    assert ls["equals_Kf"]
    assert _frac(ls["sum_times_v"]) == Fraction(267, 2)


def test_spanning_tree_factorization():
    """tau = 2^81 * 5^23"""
    p = kirchhoff_spanning_tree_packet()
    sp = p["spanning_trees"]
    assert sp["tau_only_2_and_5"]
    assert sp["tau_power_of_2"] == 81
    assert sp["tau_power_of_5"] == 23


def test_spanning_tree_compact_formula():
    """tau = (q^2+1)^(m_r-1) * (q+1)^(2*m_s-1) = 10^23 * 4^29"""
    p = kirchhoff_spanning_tree_packet()
    sp = p["spanning_trees"]
    assert sp["tau_compact_match"]


def test_spectral_sum_squared():
    """Σ lambda_j^2 = kv = 2|E|"""
    p = kirchhoff_spanning_tree_packet()
    sc = p["spectral_checks"]
    assert sc["spectral_sum_sq_equals_kv"]
    assert sc["spectral_sum_sq"] == sc["kv"]


def test_all_master_identities():
    p = kirchhoff_spanning_tree_packet()
    ids = p["master_identities_summary"]
    for name, val in ids.items():
        assert val, f"MCLI master identity failed: {name}"
