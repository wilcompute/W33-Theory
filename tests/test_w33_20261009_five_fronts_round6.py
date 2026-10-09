"""Regression: all five W33 theory independent frontiers, 2026-10-09."""
import sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_affine_current_coefficient_spectral_identity():
    import w33_20261009_affine_coefficient_coercivity as m
    d=m.certificate()
    assert d['raw_matrix_rank']==78
    assert d['eigenmultiplicities']=={'0':2,'4-sqrt6':24,'4':30,'4+sqrt6':24}
    assert d['integer_matrix_minimal_polynomial'].startswith('K*')
    assert all(t['sum_w_square']>=t['radial_lower']-1e-8 for t in d['samples'])
def test_heterotic_field_corrected_R_six_bilinears():
    import w33_20261009_field_corrected_six_bilinears as m
    d=m.certificate()
    assert len(d['six_bilinears'])==6
    assert d['six_correctedR_veto_count']==6
    assert all(not c['original_gauge_nonR_correctedR_necessary'] for c in d['six_bilinears'])
    assert d['cubic_n81_n17_n82_necessary_passes']
    assert 'Pass11797' in d['prior']
def test_symmetry_mixed_he2_he4_exact_intervals():
    import w33_20261009_he24_symmetry_exact_wick as m
    d=m.certificate()
    assert set(d['sectors'])=={'24','15_p','15_l'}
    for k,v in d['sectors'].items():
        assert F(v['lower_ritz_rayleigh_interval'][0]) <= F(v['rigorous_sector_lowest_energy_upper_endpoint'])
        assert len(v['matrix_intervals'])== (4 if k=='24' else 2)
    assert F(d['sectors']['24']['rigorous_sector_lowest_energy_upper_endpoint']) < F('142.719336')
    assert F(d['sectors']['15_p']['rigorous_sector_lowest_energy_upper_endpoint'])<F('143.611080')
def test_calibrated_finite_shot_mismatch_bound():
    import w33_20261009_sham_calibration_tolerance as m
    d=m.certificate()
    assert 0.014<d['exactly_signal_equivalent_mismatch']<0.015
    assert .004<d['idealized_max_mismatch_for_mean_above_threshold']<.005
    assert d['trial_results']['plus_boundary_null_rejections']<=7
    assert d['trial_results']['minus_boundary_null_rejections']<=7
def test_finite_coupled_spatial_contexts():
    import w33_20261009_coupled_finite_selector_cells as m
    d=m.certificate()
    assert len(d['results'])==6
    r=d['results']
    assert r[3]['mean_neighbor_line_agreement']>r[0]['mean_neighbor_line_agreement']
    assert r[5]['mean_neighbor_line_agreement']>r[4]['mean_neighbor_line_agreement']
    assert all(z['max_error_from_uniform_onesite_marginal']<2e-5 for z in r)
    assert abs(r[0]['first_ordered_gap']-2.0)<1e-6
