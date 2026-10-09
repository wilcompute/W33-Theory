"""Reproducibility regression: five October 9 physics and heterotic fronts."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_e8_explicit_weyl_and_lattice():
    import w33_20261009_e8_explicit_weyl_congruence as w
    d=w.certify()
    assert d['status']=='PASS' and d['gauge_isometry']==2
    assert all(len(f['mapped_root_index_permutation'])==240 for f in d['witnesses'])
def test_frozen_paper_BL_source_gauge_weights():
    import w33_20261009_portable_benchmark_BL as p
    r=p.certificate()
    assert r['anchors']==24 and r['rank']==7 and r['U1_nullity']==2
    assert r['assignments']['bd_7']=='2/3'
    assert r['assignments']['bd_9']=='-1/3'
def test_exact_no_BL_for_overstrict_all_labels():
    import w33_20261009_bl_assignment_inconsistency as b
    r=b.main()
    assert r['weighted_BminusL_residual']=='1'
    assert len(r['minimal_unsatisfiable_rows'])==3
    assert set(x['name'] for x in r['minimal_unsatisfiable_rows'])=={'bd_7','bu_3','be_3'}
def test_assignment_aware_even_dflat_support():
    import w33_20261009_corrected_assignment_dflat_certificate as d
    r=d.character_probe(d.proof())
    assert r['all_vev_threeBL_even']
    assert len(r['positive_support'])==6
    assert r['charge_balance']==['-1']+['0']*8
    assert r['selected_matter_odd_VEV_even_Z2_characters']==0
    assert r['integer_3BL_fields']==112
def test_new_eleven_state_ritz_and_minmax_counting():
    import numpy as np
    import w33_20261009_11state_ritz as r
    a=r.ritz(13);b=r.ritz(14)
    assert np.max(np.abs(a-b))<2e-9
    vals=np.linalg.eigvalsh(a)
    assert abs(vals[0]-127.5954926734291)<2e-8
    assert vals[0]<np.linalg.eigvalsh(a[:9,:9])[0]
    assert vals[1]<142.617 and vals[-1]<233.0
def test_joint_homodyne_vs_kurtosis_and_loss():
    import w33_20261009_joint_homodyne_cumulant as j
    import w33_20261009_joint_homodyne_loss as loss
    a=j.certificate();b=loss.certificate()
    assert 16000<a['alternative_asymptotic_5sigma_N']<18000
    assert 25_000<b['samples'][2]['alternative_approx_5sigma_N']<27_000
    assert 900_000<b['samples'][-1]['alternative_approx_5sigma_N']<1_000_000
def test_real_antiunitary_ground_split():
    import w33_20261009_ground_antiunitary_response as t
    r=t.certificate()
    assert r['simple_second_derivative']=='-2/3'
def test_w33_only_product_dimension_obstruction():
    import w33_20261009_w33_cartesian_power_spectral as s
    result=s.certificate()
    assert result['status']=='PASS'
    assert abs(s.spectral_power(1000,.375,True)['spectral_dimension']-3)<.002
    assert abs(s.spectral_power(1000,.5,True)['spectral_dimension']-4)<.003
