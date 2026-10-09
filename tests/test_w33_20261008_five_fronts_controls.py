"""Regression controls for current curvature, optical loss and finite Levi shells."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261008_current_curvature_thermal as sym
import w33_20261008_photonic_loss_control as opt
import w33_20261008_levi_shell_dimension as geom
def test_antiunitary_curvature():
    x=sym.certificate()
    assert x['noncommuting_edge_pairs']==480 and x['commuting_edge_pairs']==12240
def test_optical_loss_fourth_cumulant():
    a=opt.signal(.05,1,.01)
    b=opt.signal(.05,.5,.01)
    assert abs(b['cumulant4']-a['cumulant4']/4)<1e-12
    assert .10<b['excess_kurtosis']<.11
    assert 50000<b['optimistic_5sigma_gaussian_null_shots']<60000
    assert opt.signal(0,.5,0)['cumulant4']==0
def test_finite_native_shells():
    x=geom.certificate()
    assert x['diameter']==4 and x['distance_shells']==[1,4,12,36,27]
    assert x['ball_sizes']==[1,5,17,53,80]
    assert x['ball_growth_dimension_estimates'][1]>2.8
    assert x['ball_growth_dimension_estimates'][2]<1.5
