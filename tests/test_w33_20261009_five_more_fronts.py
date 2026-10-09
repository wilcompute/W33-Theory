"""Independent tests for five further W33 fronts (2026-10-09)."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_corrected_11state_interval_certificate():
    from w33_20261009_certified11_wick import I,rayleigh
    p=json.loads((ROOT/'data/w33_20261009_certified11_wick.json').read_text())
    h=[[(I(F(re[0]),F(re[1])),I(F(im[0]),F(im[1]))) for re,im in row]
       for row in p['matrix_intervals']]
    trial=[(F(x),F(y)) for x,y in p['trial_coefficients']]
    assert len(h)==11 and all(len(r)==11 for r in h) and len(trial)==11
    value=rayleigh(h,trial)
    assert value.hi<F('127.595507')
    assert [str(value.lo),str(value.hi)]==p['rayleigh_interval']
    assert value.lo>F('127.595506')
def test_corrected_sign_and_vacuum():
    import numpy as np
    import w33_20261009_11state_corrected_ritz as corrected
    h=corrected.ritz(13);g=corrected.ritz(14)
    assert np.max(np.abs(h-g))<2e-9
    eigen=np.linalg.eigvalsh(h)
    assert 127.595506<eigen[0]<127.595507
    assert np.linalg.eigvalsh(h[:9,:9])[0]>eigen[0]
def test_all_order_support_only_Fterm_vanish():
    import w33_20261009_six_vev_F_term_gate as ft
    import gzip
    ledger=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    fields={f['name']:f for f in ledger[ft.MODEL]['left']}
    assert all(F(fields[n]['q'][0])<0 for n in ft.SUPPORT)
    x=ft.certificate(max_degree=9)
    assert x['counts'].get('A_all',0)==0
    assert x['counts']['B_all']==11 and x['counts']['B_point_group']==11
def test_pass11793_full_order_four_character():
    import w33_pass11793_order_four_matter_action as h
    x=h.certificate()
    assert x['field_action_order']==4
    assert not x['operator_selection']['udd']['allowed_by_this_character']
    assert x['operator_selection']['QQQL']['allowed_by_this_character']
def test_curvature_displaced_coherent_exact():
    import w33_20261009_current_curvature_coherent as C
    x=C.certificate()
    assert x['nonzero_current_curvature_pair_count']==480
    assert set(x['distinct_centered_real_gaussian_curvature'])=={'-1/10','1/10'}
def test_intrinsic_universal_abelian_cover_full_rank():
    import w33_20261009_universal_abelian_cover as G
    x=G.certificate()
    assert x['deck_rank']==81
    assert x['incidence_rank']==79
    assert x['reduced_diffusion_min_eigenvalue']>0
    assert x['reduced_diffusion_max_eigenvalue']<0.013
def test_pump_sign_lockin_quadrature_loss():
    import w33_20261009_pump_sign_lockin as P
    x=P.certificate()
    assert len(x['rows'])==8
    assert 26000<x['rows'][2]['approx_5sigma_samples']<27000
    assert x['rows'][3]['mean']==x['rows'][2]['mean']
    assert x['rows'][3]['variance']>x['rows'][2]['variance']
def test_sign_reversal_rejects_quadratic_readout_crosstalk():
    import numpy as np
    rng=np.random.default_rng(1709)
    n=300000
    z=rng.normal(0,np.sqrt(.5),n)
    s=rng.choice(np.array([-1.,1.]),size=n)
    Q=z*z-.5
    # Detector-only nonlinear artifact can mimic a mixed third cumulant.
    cross=0.08*Q
    naive=float(np.mean(cross*Q))
    pump_locked=float(np.mean(s*cross*Q))
    assert naive>.035
    assert abs(pump_locked)<.005
    # True sign-odd simulated nonlinear source survives pump lock-in.
    theta=(39/20)**2*.05;a=1/np.sqrt(39)
    x=rng.normal(0,np.sqrt(.5),n);px=rng.normal(0,np.sqrt(.5),n)
    pout=px-2*s*theta*(x+a)*(z+a)**2+cross
    measured=float(np.mean(s*pout*Q))
    assert abs(measured+theta*a)<.005
