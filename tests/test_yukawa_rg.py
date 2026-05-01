"""
test_yukawa_rg.py

Regression tests for the W(3,3) Yukawa RG module.
"""

import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from w33_yukawa_rg import (
    w33_yukawa_gut, run_yukawa_system, yukawa_to_pole_mass,
    w33_fermion_mass_predictions, PDG_MASSES
)
from w33_neutrino_rg_bridge import (
    seesaw_scale, dirac_yukawa_from_seesaw, neutrino_rg_bridge_report,
    PLANCK_SUM_LIMIT, NU_NH_BEST, NU_IH_BEST
)

def close(a, b, rel=0.5):
    """Within 50% relative tolerance."""
    return abs(a - b) / max(abs(b), 1e-30) < rel

# --- Yukawa structure ---

def test_yukawa_gut_keys():
    y = w33_yukawa_gut()
    for k in PDG_MASSES:
        assert k in y, f"Missing Yukawa for {k}"

def test_yukawa_gut_hierarchy():
    """Top Yukawa must be the largest at GUT scale."""
    y = w33_yukawa_gut()
    assert y['top'] == max(y.values())

def test_yukawa_gut_all_positive():
    y = w33_yukawa_gut()
    for k, v in y.items():
        assert v > 0, f"y[{k}] = {v} not positive"

def test_yukawa_to_pole_mass_top():
    """Top mass from y_top(M_Z)~1 should be near 172 GeV."""
    m = yukawa_to_pole_mass(0.993)
    assert 150 < m < 200, f"top mass = {m} GeV"

def test_yukawa_run_finite():
    """Yukawa RG run over 10 GeV -> 100 GeV must be finite."""
    y = w33_yukawa_gut()
    result = run_yukawa_system(y, 0.04, 1e14, 1e15, n_steps=200)
    assert result is not None
    assert all(math.isfinite(v) for v in result.values())

# --- Neutrino bridge ---

def test_nh_planck_consistent():
    assert NU_NH_BEST['sum_eV'] < PLANCK_SUM_LIMIT

def test_ih_planck_consistent():
    assert NU_IH_BEST['sum_eV'] < PLANCK_SUM_LIMIT

def test_seesaw_scale_physical():
    M_R = seesaw_scale(0.05, 0.5)  # 50 meV neutrino, y_D=0.5
    assert 1e10 < M_R < 1e18, f"M_R = {M_R:.2e} not physical"

def test_seesaw_inversion():
    """Seesaw and its inverse should be consistent."""
    m_nu = 0.05  # eV
    M_R  = seesaw_scale(m_nu, 0.3)
    y_back = dirac_yukawa_from_seesaw(m_nu, M_R)
    assert close(y_back, 0.3, rel=0.01)

def test_bridge_report_returns_dict():
    r = neutrino_rg_bridge_report(verbose=False)
    assert isinstance(r, dict)
    assert 'planck_NH' in r
    assert 'seesaw_NH' in r

def test_bridge_nh_stability():
    r = neutrino_rg_bridge_report(verbose=False)
    assert r['stability_NH']['pass']

if __name__ == '__main__':
    tests = [
        test_yukawa_gut_keys, test_yukawa_gut_hierarchy,
        test_yukawa_gut_all_positive, test_yukawa_to_pole_mass_top,
        test_yukawa_run_finite, test_nh_planck_consistent,
        test_ih_planck_consistent, test_seesaw_scale_physical,
        test_seesaw_inversion, test_bridge_report_returns_dict,
        test_bridge_nh_stability,
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
