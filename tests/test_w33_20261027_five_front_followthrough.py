"""Checks of the new native maps, compact dynamics, and constitutive freedom."""
from pathlib import Path
import sys
import json
import numpy as np
import sympy as s

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import w33_20261027_five_front_followthrough as f


def test_four_form_is_invisible_to_plane_wave_symbol_but_bounds_positivity():
    d=f.metric_classification();*_,periods,comm,H,M=f.inputs()
    W=s.Matrix(periods);J=s.Matrix(d['J'])
    n=s.Matrix([2,-3,1,4]);u=W*n
    C=s.Matrix([[u[i]*W[j,a]-u[j]*W[i,a] for a in range(4)] for i,j in f.PAIRS])
    assert C.T*J*C==s.zeros(4)
    for theta in (-1,1):
        assert np.linalg.eigvalsh(np.array(H+theta*J,dtype=float)).min()>0
    assert np.linalg.eigvalsh(np.array(H+3*J,dtype=float)).min()<0


def test_integer_reflection_and_native_symmetry_obstruction():
    d=f.dimensional_reduction();*_,H,M=f.inputs()
    R=s.Matrix(d['integral_metric_reflection']['matrix'])
    assert R.det()==-1 and R.T*M*R==M and R**2==s.eye(4)
    assert (R-s.eye(4)).rank()==1
    assert d['native_symmetry_invariant_rational_projector_ranks']==[0,2,4]
    assert not d['integral_metric_reflection']['commutes_with_native_group']


def test_compact_harmonics_exact_hessian_and_periodicity():
    d=f.compact_metric_completion();*_,H,M=f.inputs()
    found=s.zeros(6)
    phi=np.array([.17,-.31,.7,1.1,-.2,.8]);integer=np.array([1,-2,3,0,-1,1])
    values=[]
    for x in (phi,phi+2*np.pi*integer):
        values.append(sum(float(s.Rational(h['weight']))*(1-np.cos(np.dot(h['q'],x)))for h in d['harmonics']))
    for h in d['harmonics']:
        q=s.Matrix(h['q']);assert max(map(abs,h['q']))==1
        found+=s.Rational(h['weight'])*q*q.T
    assert found==H and abs(values[0]-values[1])<1e-12


def test_lifted_loops_and_charge_transfer_obey_exact_gauss():
    C,B,keys,endpoints=f.lifted_patch()
    assert B.shape==(20,19) and np.array_equal(C@C.T,[[12,4],[4,12]])
    assert not (C@B).any()
    for m in ([1,2],[-2,3],[0,0]):
        for charge in (1,-2,4):
            before=np.array(m)@C;after=before.copy();after[0]+=charge
            n_delta=charge*B[0]
            assert np.array_equal(after@B-before@B,n_delta)


def test_rotor_variational_convergence_and_wilson_bounds():
    a=f.rotor_matrix(2,.5);b=f.rotor_matrix(4,.5)
    assert b['ground_energy']<a['ground_energy']
    assert b['boundary_probability']<a['boundary_probability']
    assert b['gap']>0 and all(abs(w)<=1+1e-12 for w in b['Wilson_cosines'])


def test_cubic_gauge_charge_map_and_center_trace_identities():
    d=f.matter_interface();q=np.array(d['internal_Qpsi'])
    assert np.all(q%3==1)
    assert q.sum()==(q**3).sum()==0
    assert (q**2).sum()==72 and (q**4).sum()==432
    assert d['all45_signed_cubic_terms_U1_invariant']
    assert max(x['edge_phase_coboundary_max']for x in f.central_link_gauge_equivalence()['controls'])<1e-12


def test_regenerated_induction_witness_is_not_target_metric():
    d=json.loads((f.ROOT/'data/w33_20261027_five_front_followthrough.json').read_text())
    for x in d['microscopic_induction_probe']['samples']:
        H=np.array(x['hessian'])
        assert abs(H[0,0]-H[1,1])<1e-11
        assert x['central_flux_gradient_max']<1e-11
        assert min(x['zero_flux_hessian_eigenvalues'])<0
        assert x['relative_shape_residual']>.3


def test_intake_archives_match_their_full_patch_and_page_hashes():
    import gzip,hashlib
    import pytest
    d=json.loads((f.ROOT/'analysis/2026-10-27_research_intake_coverage.json').read_text())
    assert len(d['historical_week_commits'])==481 and len(d['pdf_pages'])==210
    if not all((f.ROOT/c['archive']).exists() for c in d['historical_week_commits']):
        pytest.skip('Scratch duplicates of Git objects are local; run the intake producer to regenerate them.')
    for c in d['historical_week_commits']:
        with gzip.open(f.ROOT/c['archive'],'rb') as src:
            raw=src.read()
        assert len(raw)==c['patch_bytes']
        assert hashlib.sha256(raw).hexdigest()==c['patch_sha256']
        assert isinstance(c['full_patch_model_read'],bool)
    for p in d['pdf_pages']:
        raw=(f.ROOT/p['archive']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==p['text_sha256']


def test_paper_reference_resolution_is_not_confused_with_validation():
    d=json.loads((f.ROOT/'analysis/2026-10-27_research_intake_coverage.json').read_text())
    r=d['certificate_references']
    assert r['total']==1216 and not r['unresolved']
    assert sum(p['full_text_model_read_this_continuation']for p in d['pdf_pages'])>=23
    assert 'remains incomplete' in d['completion']
