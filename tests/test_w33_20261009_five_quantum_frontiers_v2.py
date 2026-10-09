"""Five follow-on W33 tests: spectral, heterotic, quantum, optical, geometry."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_all_degree_F_candidates_exact():
    import w33_20261009_all_order_one_outsider_F_gate as f
    d=f.main()
    assert d['support_charge_rank']==6
    assert d['outside_tested']==170
    assert d['all_order_candidates']==11
    assert d['max_observed_degree']==5
    assert d['point_group_sector_zero']==11
    assert [x['total_degree'] for x in d['monomials']]==[2]*5+[3]*2+[4]*2+[5]*2
def test_second_ordered_interval_enclosure():
    import w33_20261009_second_ordered_upper_certificate as f
    d=f.certificate()
    assert 139.6653<d['decimal_upper']<139.666
    assert d['theorem'].startswith('E1=minmax')
def test_PSp_no_equivariant_three():
    import w33_20261009_no_equivariant_three_space as f
    d=f.certificate()
    assert d['group_order']==25920
    assert d['deck_rank']==81
    assert d['character_norm_square']=='25920/25920=1'
def test_adjacent_curvature_full_group_orbits():
    import w33_20261009_group_curvature_twirl as f
    d=f.main()
    assert d['adjacent_pair_orbit_sizes']=={'shared_point':240,'shared_line':240}
    assert len(d['edge_swap_witnesses'])==2
def test_sharp_randomization_null_under_correlated_drift():
    import w33_20261009_finite_shot_homodyne_randomization as f
    d=f.certificate()
    assert d['null_trials']==400
    assert d['null_rejections']<=15
    assert d['alternative_rejections']>=104
    assert d['pump_odd_detector_confound_rejections']>=80
