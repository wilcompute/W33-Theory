"""Exact certificate checks, independent finite group and operator controls."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
import numpy as np
import sympy as s
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261027_native_operator_closure as m
import w33_20261027_certified_rotor_bounds as b


def test_canonical_cubic_under_finite_SU5_transform():
    r=m.canonical_cubic_intertwiner();S=np.array(r['canonical_to_SU5_signed_permutation'])
    rng=np.random.default_rng(17);X=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5))
    X+=X.conj().T;X-=np.trace(X)*np.eye(5)/5;U=expm(.2j*X)
    R=np.zeros((27,27),complex);R[:10,:10]=m.old.wedge2(U)
    R[10:15,10:15]=U.conj();R[15,15]=1;R[16:21,16:21]=U;R[21:26,21:26]=U.conj();R[26,26]=1
    source=json.loads((ROOT/'artifacts/canonical_su3_gauge_and_cubic.json').read_text())['solution']['d_triples']
    def cubic(v):return sum(rec['sign']*np.prod(v[rec['triple']])for rec in source)
    z=rng.normal(size=27)+1j*rng.normal(size=27)
    assert abs(cubic(z)-cubic(S.T@R@S@z))<1e-10
    assert r['all26_infinitesimal_generators_preserve_cubic']


def test_native_overlap_free_operator_and_nonzero_momentum():
    links=np.ones((135,1,1),complex)
    zero=m.overlap_diagnostics(links,np.zeros(4));moving=m.overlap_diagnostics(links,np.array([.1,.2,.3,.4]))
    assert zero['near_zero_D_singular_values']==4 and moving['near_zero_D_singular_values']==0
    assert max(zero['GW_error'],moving['GW_error'],moving['Weyl_intertwining_error'])<1e-10
    assert min(zero['hermitian_kernel_gap'],moving['hermitian_kernel_gap'])>.5


def test_overlap_backgrounds_and_metric_choice_are_explicit():
    r=json.loads((ROOT/'data/w33_20261027_native_operator_closure.json').read_text())['native_overlap']
    assert len(r['corner_controls'])==16 and len(r['random_momentum_kernel_gaps'])==48
    assert min(x['gap']for x in r['random_momentum_kernel_gaps'])>.5
    for name in ('5','bar5','10'):
        x=r['nonabelian_irrep_controls'][name]
        assert x['GW_error']<1e-10 and x['projector_error']<1e-10
    matched=[x for x in r['coframe_controls']if x['metric_matched']]
    assert max(abs(np.array(matched[-1]['four_low_singular_values_over_eps'])-matched[-1]['target']))<1e-6
    raw=next(x for x in r['coframe_controls']if not x['metric_matched'])
    assert abs(raw['target']-matched[-1]['target'])>.1
    # A second integer period basis preserves the matched edge inner products.
    _,V,_,h=m.geometry();G=h.T@h/27
    S=np.array([[1,1,0,0],[0,1,0,0],[0,0,1,1],[0,0,0,1]])
    hp=h@S;Gp=S.T@G@S
    assert np.max(abs(h@np.linalg.solve(G,h.T)-hp@np.linalg.solve(Gp,hp.T)))<1e-10


def test_interacting_cell_current_kernel_and_finite_difference():
    r=m.interacting_native_cell(2)
    B=m.geometry()[0];K=np.array(r['static_link_kernel']);E=np.array(r['regular_electric_link_kernel'])
    assert K.shape==E.shape==(135,135)
    assert np.max(abs(K@B))<1e-10
    assert np.linalg.eigvalsh(E)[0]>-1e-10
    assert r['independent_edge_finite_difference_error']<1e-6
    assert r['double_occupancy']<1/27 and r['gap']>8


def test_reflection_odd_candidate_fails_selection():
    r=m.reflection_selection_probe()
    assert s.Rational(r['exact_one_particle_ground_curvature'])==-s.Rational(112,3645)
    assert all(x['fermion_free_energy_second_derivative']<0 for x in r['thermal_samples'])


def test_exact_infinite_flux_certificates_without_trusting_eigensolver():
    cert=json.loads((ROOT/'data/w33_20261027_certified_rotor_bounds.json').read_text())
    for r in cert['controls']:
        A,den,beta2,c,states=b.integer_operator(r['loops'],r['cutoff'],r['g'])
        psi=[int(x)for x in r['strictly_positive_integer_test_vector']]
        assert min(psi)>0 and len(psi)==A.shape[0]
        hp=[sum(int(A.data[j])*psi[int(A.indices[j])]for j in range(A.indptr[i],A.indptr[i+1]))for i in range(len(psi))]
        lower=min(F(v,den*x)for v,x in zip(hp,psi))
        upper=F(sum(v*x for v,x in zip(hp,psi)),den*sum(x*x for x in psi))
        p=r['finite_block_certificate']
        assert lower==F(p['exact_min_positive_vector_ratio'])and upper==F(p['exact_Rayleigh_quotient'])
        assert s.Rational(str(c))==s.Rational(r['complement_lower_bound_exact'])
        assert beta2==F(r['interface_norm_squared_upper_exact'])
        a=s.Rational(lower.numerator,lower.denominator);bb=s.Rational(beta2.numerator,beta2.denominator)
        exact=(a+c-s.sqrt((a-c)**2+4*bb))/2
        assert exact==s.sympify(r['infinite_ground_lower_exact'])
        assert 0<float(exact)<float(upper)<4
    six=[x for x in cert['controls']if x['loops']==6]
    assert six[1]['interval_width']<six[0]['interval_width']/2


def test_split_threshold_analytic_exclusion():
    r=m.split_thresholds();q=r['exact_analytic_exclusion']
    assert not r['feasible']
    assert F(q['exact_rational_scalar_mass_upper'])<1000
    assert q['scalar_mass_upper_GeV']<747
    assert r['full_Weyl_contributions']==['40/3','14','296/9']
    assert r['full_scalar_contributions']==['14/3','28/3','148/9']


def test_specific_partial_reading_coverage():
    r=json.loads((ROOT/'analysis/2026-10-27_research_intake_coverage.json').read_text())
    assert sum(x['full_text_model_read_this_continuation']for x in r['pdf_pages'])>=47
    assert sum(x['full_patch_model_read']for x in r['historical_week_commits'])>=9
    assert r['reading_increment_20261027_operator']['pages_added']==list(range(111,119))
    assert 'incomplete' in r['completion']
