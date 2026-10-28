"""Exact tensor replay, Ward identities, radial vacuum and Einstein controls."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
import numpy as np
import sympy as s
from scipy.special import expit
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261027_acoustic_density_backreaction as core
import w33_20261027_shared_singlet_masses as mass

def data():return json.loads((ROOT/'data/w33_20261027_acoustic_density_backreaction.json').read_text())
def masses():return json.loads((ROOT/'data/w33_20261027_shared_singlet_masses.json').read_text())

def test_exact_harmonic_tensor_and_second_basis():
    r=core.harmonic_response_identity()
    assert r['current_block_tensor_coefficients']==[['0','0','0'],['0','5/3','1/6'],['0','1/6','0']]
    M=s.Matrix([[s.Rational(x)for x in row]for row in r['metric_exact']])
    assert M.det()>0 and M==s.Matrix([[10,5,-6,0],[5,10,0,-6],[-6,0,12,-6],[0,-6,-6,12]])
    assert r['gapped_zero_temperature']['ratio_static_to_electric']=='108'

def test_entire_thermal_response_matches_exact_closed_form():
    M=np.array(data()['exact_harmonic_response']['metric_exact'],float)
    for r in data()['density']:
        T,mu=r['T'],r['mu'];fg,fm,fp=expit((mu-np.array([-10.,-1.,5.]))/T)if T else(np.array([-10.,-1.,5.])<mu).astype(float)
        electric=(fm-fp)/648
        static=(4*fg+5*fm-9*fp)/54-(5/(3*T))*fm*(1-fm)if T else(4*fg+5*fm-9*fp)/54
        assert np.max(abs(np.array(r['electric_harmonic'])-electric*M))<1e-12
        assert np.max(abs(np.array(r['static_harmonic'])-static*M))<1e-11

def test_gapped_filling_21_and_thermal_jump():
    d=data()['density'];r=d[-1]
    assert r['T']==0 and r['mean_particles']==21
    assert abs(r['static_metric_scale']-1/6)<1e-12
    assert abs(r['electric_metric_scale']-1/648)<1e-12
    assert r['zero_Matsubara_vs_dynamic_limit_norm']==0
    half=next(x for x in d if x['T']==.25 and x['mu']==-1)
    assert half['zero_Matsubara_vs_dynamic_limit_norm']>40 and half['static_metric_scale']<0

def test_exact_inertia_excludes_cover_band_insulator():
    r=data()['cover_filling'];cert=[core.verify_inertia_certificate(x)for x in r['certificates']]
    assert [x['negative']for x in cert]==[20,22]
    assert all(x['negative']+x['positive']==27 and F(x['normalized_margin_exact'])>0 for x in cert)

def test_density_current_frequency_Ward_including_contact():
    for r in data()['density']:
        assert r['static_gauge_Ward_error']<1e-9
        for x in r['frequency_samples']:
            w=x['omega'];chi=x['density_response'];mixed=x['mixed_spatial_density']
            assert x['Ward_error']<1e-9
            assert abs(x['pure_spatial_gauge_response']+w*w*chi)<1e-9
            assert abs(mixed[0]+w*chi)<1e-9 and abs(mixed[1]-w*chi)<1e-9

def test_acoustic_Frechet_derivative_recomputed():
    H,ders,_=core.acoustic_operators(representation='5');P,(Pt,Pa,Pb),gap=core.spectral_projector(H,ders)
    assert gap>.5 and np.max(abs(P@P-P))<1e-12
    eps=1e-5
    Hp=core.acoustic_operators(a=eps)[0];Hm=core.acoustic_operators(a=-eps)[0]
    diff=(core.spectral_projector(Hp)[0]-core.spectral_projector(Hm)[0])/(2*eps)
    assert np.max(abs(diff-Pa))<1e-8

def test_finite_acoustic_current_curvature_and_closed_loop():
    for r in data()['acoustic']:
        assert r['curvature_identity_error']<1e-7
        assert r['quadrature_8_vs_16_error']<1e-10
        assert r['projector_tangent_identity_error']<1e-12
        assert r['free_reference_local_gauge_commutator']>.1
        assert r['finite_rectangle_phase_error']<1e-8
        assert r['finite_rectangle_phase_error']<r['Kato_discretization_change']
        assert abs(r['finite_rectangle_current_integral'])>1e-5

def test_correlated_radial_minimum_exact_stationarity():
    r=masses();p=r['potential'];Q=s.Matrix([[s.Rational(x)for x in row]for row in p['charge_matrix']]);t=s.Matrix(list(map(s.Rational,p['exact_squared_vevs'])))
    A=s.eye(25)+s.Rational(p['kappa'])*Q.T*Q
    assert all(x>0 for x in t)and A*t==s.ones(25,1)
    assert p['squared_modulus_coordinate_Hessian_lower']==1 and Q.rank()==4
    assert r['independent_complex_singlets']==25 and r['raw_scalar_records']==50
    assert len(set(x for pair in r['scalar_conjugate_pairs']for x in pair))==50

def test_all_selected_pair_witnesses_and_correlated_masses():
    r=masses();raw={x['id']:x for x in mass.records()};conj=dict(r['scalar_conjugate_pairs']);t=list(map(s.Rational,r['potential']['exact_squared_vevs']));ids=[]
    for pair in r['matched_pairs']:
        a,b=[raw[i]for i in pair['fermion_ids']];ids+=pair['fermion_ids'];fields=[a,b]
        expected=.1**pair['degree']
        for atom in pair['singlet_monomial']:
            field_id=conj[atom['field_id']]if atom['conjugated']else atom['field_id'];fields.append(raw[field_id]);expected*=np.sqrt(float(t[atom['coordinate']]))
        assert len(fields)==2+pair['degree'] and pair['degree']in(1,2)
        assert all(sum(x['q'][j]for x in fields)==0 for j in range(5))
        assert sum(x['n']for x in fields)%6==sum(x['mm']for x in fields)%2==0
        translated=sum((mass.TH**k*s.Matrix(x['lat'])for x,k in zip(fields,pair['point_group_rotations'])),s.zeros(6,1))
        assert mass.translation_allowed(tuple(translated),tuple(x['n']for x in fields))
        assert abs(expected-pair['mass_over_cutoff'])<1e-14 and 0<expected<1
    assert len(ids)==len(set(ids))==48 and r['paired_Weyl_gauge_components']==148
    assert r['shifted_e5_allowed_edges']==0

def test_graviton_loop_changes_minimum_existence():
    r=data()['backreaction'];a,b,c=r['samples'][:3]
    assert r['graviton_physical_polarizations']==5
    assert a['has_minimum']and not b['has_minimum']and c['has_minimum']
    assert float(c['mR'])<float(a['mR'])
    assert not r['samples'][3]['has_minimum']and r['samples'][4]['has_minimum']
    assert r['massless_SU5_gauge_polarizations']==72

def test_Einstein_stress_and_radion_stability():
    for r in data()['backreaction']['samples']:
        if not r['has_minimum']:continue
        rho=F(r['rho5']);pressure=F(r['pressure5'])
        assert abs(float(pressure+2*rho))<1e-35 and rho<0
        assert float(r['ell_over_R'])>1e5 and float(r['M5_R'])>100
        assert float(r['radion_mass_squared_times_ell_squared'])>0

def test_content_review_is_partial_and_provenanced():
    r=json.loads((ROOT/'analysis/2026-10-27_research_intake_coverage.json').read_text())
    assert sum(x['full_text_model_read_this_continuation']for x in r['pdf_pages'])==64<210
    assert sum(x['full_patch_model_read']for x in r['historical_week_commits'])==19<481
    assert r['reading_increment_20261027_acoustic']['visual_pages_checked']==[132]
    assert r['live_pdf_edition']['frozen_git_ref'].startswith('a03ff9dc0')
    assert r['live_pdf_edition']['live_full_text_pages_read']==[86,204]
