"""
test_rg_gut.py

Regression tests for the W(3,3) RG/GUT conversion fix.
Locks in the physical requirements from RG_MGUT_ISSUE.md.
"""

import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from w33_rg_gut_conversion import (
    beta_qcd_2loop, run_alpha_s, w33_alpha_s_mz,
    threshold_match_top, su3_embedding_factor,
    w33_m_gut, w33_alpha_unified_gut
)

def test_beta_asymptotic_freedom_nf5():
    """QCD is asymptotically free for nf<=16: beta must be negative."""
    for nf in range(1, 7):
        assert beta_qcd_2loop(0.1, nf) < 0, f"beta not negative for nf={nf}"

def test_beta_zero_coupling():
    """At alpha_s=0, beta=0 (trivial fixed point)."""
    assert beta_qcd_2loop(0.0, 5) == 0.0

def test_run_alpha_s_finite():
    """Running from M_Z to 100 GeV must be finite and positive."""
    a = run_alpha_s(0.1180, 91.19, 100.0, nf=5)
    assert a is not None and math.isfinite(a) and a > 0

def test_run_alpha_s_decreases_uv():
    """UV running: alpha_s must decrease from M_Z to 1000 GeV."""
    a = run_alpha_s(0.1180, 91.19, 1000.0, nf=6)
    assert a is not None and a < 0.1180

def test_run_alpha_s_increases_ir():
    """IR running: alpha_s must increase from M_Z toward 1 GeV."""
    a = run_alpha_s(0.1180, 91.19, 5.0, nf=5)
    assert a is not None and a > 0.1180

def test_threshold_matching_small():
    """Top threshold correction must be < 1%."""
    a_above = 0.108
    a_below = threshold_match_top(a_above, 172.57)
    assert abs(a_below - a_above) / a_above < 0.01

def test_su3_embedding_factor_positive():
    k3 = su3_embedding_factor()
    assert k3 > 0

def test_m_gut_in_range():
    M = w33_m_gut()
    assert 1e14 < M < 1e18, f"M_GUT={M:.2e} out of physical range"

def test_alpha_unified_gut_in_range():
    a = w33_alpha_unified_gut()
    assert 0.01 < a < 0.1, f"alpha_unified={a} out of range"

def test_w33_alpha_s_mz_returns_dict():
    result = w33_alpha_s_mz(verbose=False)
    assert isinstance(result, dict)
    assert 'status' in result

def test_w33_alpha_s_mz_physical():
    """The final alpha_s(M_Z) must be in a physically meaningful range."""
    result = w33_alpha_s_mz(verbose=False)
    if result['status'] == 'ok':
        a = result['alpha_s_mz']
        assert 0.05 < a < 0.5, f"alpha_s(M_Z)={a} is not physical"

def test_run_up_from_mz_to_gut_range():
    """Running alpha_s UP from PDG M_Z value to M_GUT should give ~1/25."""
    M_GUT = w33_m_gut()
    a_gut = run_alpha_s(0.1180, 91.19, M_GUT, nf=6, n_steps=8000)
    assert a_gut is not None and 0.01 < a_gut < 0.1

if __name__ == '__main__':
    tests = [
        test_beta_asymptotic_freedom_nf5, test_beta_zero_coupling,
        test_run_alpha_s_finite, test_run_alpha_s_decreases_uv,
        test_run_alpha_s_increases_ir, test_threshold_matching_small,
        test_su3_embedding_factor_positive, test_m_gut_in_range,
        test_alpha_unified_gut_in_range, test_w33_alpha_s_mz_returns_dict,
        test_w33_alpha_s_mz_physical, test_run_up_from_mz_to_gut_range
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f'  PASS  {t.__name__}')
            passed += 1
        except Exception as e:
            print(f'  FAIL  {t.__name__}: {e}')
    print(f'\n{passed}/{len(tests)} passed.')
