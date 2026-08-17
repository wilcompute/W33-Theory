from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def read(p): return (ROOT/p).read_text()


def test_linf_claim_is_not_mc_verified():
    s=read('scripts/w33_linf_bracket_mass_ratios.py')
    assert 'mc_residual = K - LA' in s
    assert 'mc_sum_formal = Y1 + Y2 + Y3' in s
    assert 'not zero' in s


def test_weyl_dimension_inference_is_circular_in_producer():
    s=read('scripts/w33_weyl_law_4volume.py')
    assert 'return n**4 * N1' in s
    assert 'multiplicities scaled by n^4' in s
    assert "dimension_from': 'N ~ n^4" in s


def test_ym_target_is_explicitly_backsolved():
    s=read('scripts/w33_ym_mass_gap_1818.py')
    assert 'Solve for Lambda_QCD_eff that gives exactly 1818 MeV' in s
    assert 'lambda_eff = delta_ym_target / coeff' in s


def test_neutrino_factor_is_repaired_after_target_miss():
    s=read('scripts/w33_neutrino_mass_leech.py')
    assert '40,884,480  (too large!)' in s
    assert 'So: 10,221,120 = 6 * 480 * 13 * 273' in s


def test_inflation_and_scalar_observable_maps_are_assignments():
    i=read('scripts/w33_inflation_r_1_45.py')
    s=read('scripts/w33_scalar_resonance_3215gev.py')
    assert 'r = Fraction(1, N_TRITANGENT_PLANES)' in i
    assert 'm_scalar_gev = M_HIGGS_GEV * float(ratio)' in s
    assert 'ratio = Fraction(tau_O, G_M)' in s


def test_supersession_reports_are_live():
    assert 'SUPERSEDED PHYSICAL-DERIVATION CLAIMS' in read('PASS5913_5932_LINF_BRACKET_ELECTRON_WEYL.md')
    assert 'SUPERSEDED PREDICTION-DERIVATION CLAIMS' in read('PASS5933_5956_HITLIST_PREDICTIONS.md')
