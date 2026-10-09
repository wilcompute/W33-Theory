"""October 9 additional five-front W33 theory regression suite."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_13vev_quadratic_F_obstruction():
    import w33_20261009_new_higgs_13vev_F_filter as f
    import w33_20261009_doublet_quadratic_F_obstruction as b
    x=f.main();y=b.certificate()
    assert x['candidate_counts']['candidate_s2']==6
    assert x['candidate_counts']['candidate_s4']==20
    assert y['spinor_gradient_det']=='-1'
    assert y['gauge_eligible_bilinears']==6
def test_quantum_classical_flatdirections_mod_prime_exact():
    import w33_20261009_classical_zero_hessian_rank as m
    x=m.certificate()
    assert (x['gradient_jacobian_rank'],x['Hessian_nullity'])==(82,74)
    assert (x['q_gradient_rank'],x['p_gradient_rank'])==(78,4)
def test_nontrivial_24_and_15_ritz():
    import w33_20261009_nontrivial_he2_ritz as m
    x=m.certificate(13);y=m.certificate(14)
    h=x['irreps']['24_point_line_doublet']
    z=x['irreps']['15_point_and_line_singlets']
    assert len(h)==2 and len(z)==2
    assert 142.7193<h[0]<142.7194
    assert abs(z[0]-143.6110807403)<1e-7
    assert abs(h[0]-y['irreps']['24_point_line_doublet'][0])<1e-8
def test_full_triple_orbit_symmetry():
    import w33_20261009_all_triple_orbit_breaking as m
    d=m.certificate()
    assert d['total_orbits']==5
    assert sorted(x['orbit_size'] for x in d['orbit_types'])==[160,360,2160,2880,4320]
    rank3=[x for x in d['orbit_types'] if x['pointwise_H1_invariant_rank']==3]
    assert len(rank3)==2
    assert all(x['orbit_size']>1 for x in d['orbit_types'])
def test_threeway_randomized_bypass_and_controls():
    import w33_20261009_three_control_photonic_causal as m
    d=m.certificate()
    assert d['rejection_counts']['null']<=8
    assert d['rejection_counts']['signal']>=40
    assert d['rejection_counts']['route_dependent_detector']>=50
    assert abs(d['mean_4x_GSR_score']['signal']-d['predicted_4x_GSR_signal'])<.01
