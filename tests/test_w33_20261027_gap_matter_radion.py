"""Independent arithmetic, Ward, finite-difference and mechanism checks."""
import json
from fractions import Fraction as F
import numpy as np
import sympy as s
from scipy.sparse import coo_matrix, kron, eye, diags
from scipy.sparse.linalg import eigsh
from analysis import w33_20261027_gap_matter_radion as f

def result():return json.loads((f.ROOT/'data/w33_20261027_gap_matter_radion.json').read_text())

def test_exact_gap_certificates_replay():
    for d in (3,6):
        r=f.gap_certificate(d)
        assert r['shortest_norm']==12 and F(r['outside_box_norm_lower'])>12
        assert F(r['gap_lower_exact'])>F('2.31')
        assert r['first_excited_interval'][0]==6
        assert r['gap_interval'][0]<=r['gap_interval'][1]

def test_two_cell_ground_and_static_Ward():
    r=result()['translated_matter'];K=f.kinetic(2)
    assert np.max(abs(K.sum(axis=1).A.ravel()+10))<1e-12
    assert r['dimension']==2916 and r['ground_residual']<1e-9
    assert r['static_Ward_error']<1e-8 and max(r['resolvent_residuals'])<1e-8
    assert np.linalg.eigvalsh(np.array(r['static_twist_and_gauge_kernel'])[:4,:4]).min()>0
    static=np.array(r['static_twist_and_gauge_kernel'])
    assert np.max(abs(static[:4,:4]-static[4:8,4:8]))<1e-8
    assert r['electric_harmonic_metric_fit']['relative_Frobenius_error']>.5
    free=result()['translated_matter_controls'][0]
    assert np.max(abs(np.array(free['electric_twist_and_gauge_kernel'])[4:8,4:8]))<1e-20

def test_two_cell_twist_curvature_independent_finite_difference():
    B,V,edges,_=f.native.geometry();n=54;U=2
    def ground(t):
        rr=[];cc=[];vv=[]
        for c in range(2):
            for e,(a,b)in enumerate(edges):
                u=c*27+a;v=((c+int(V[e,0]))%2)*27+b;z=-np.exp(1j*t*V[e,0])
                rr.extend((v,u));cc.extend((u,v));vv.extend((z,z.conjugate()))
        K=coo_matrix((vv,(rr,cc)),shape=(n,n)).tocsr()
        H=kron(K,eye(n))+kron(eye(n),K)+diags([U*(a==b)for a in range(n)for b in range(n)],dtype=float)
        return eigsh(H,k=1,which='SA',tol=1e-12,v0=np.ones(n*n),return_eigenvectors=False)[0]
    eps=.001;curvature=(ground(eps)+ground(-eps)-2*ground(0))/eps**2
    assert abs(curvature-result()['translated_matter']['static_twist_and_gauge_kernel'][0][0])<2e-5

def test_larger_sector_degeneracy_is_not_hidden():
    r=result()['larger_particle_sector'];e=np.array(r['lowest_24_energies'])
    assert r['dimension']==9477 and r['max_Ritz_residual']<1e-8
    assert sum(abs(e-e[0])<1e-7)>1
    assert 'not applied' in r['response_status']

def test_nonabelian_heavy_covariance_and_uniform_radius():
    r=result()['heavy_measure']
    assert [x['representation']for x in r['samples']]==['5','10','canonical27']
    # Canonical27 has invariant singlets with exact gap3; floating eigh may
    # return3 minus a few ulps. The analytic lower bound is not inferred here.
    assert all(x['gap']>=3-1e-11 and x['projector_error']<1e-10 and x['gauge_covariance_error']<1e-10 for x in r['samples'])
    assert 0<F(r['weak_fundamental_SU5_link_norm_radius_for_all27_exact'])==F(r['weak_representation_link_norm_radius_exact'])/2
    assert r['native_range']>1 and r['uniform_weak_field_gap_lower']==.75
    assert r['native_transport_links_tested']==135
    assert max(r['native_SU5_transport_factorization_error'],r['native_SU5_tree_factorization_error'])<1e-11
    a=r['acoustic_measure_representation_checks'];t=s.Symbol('t',nonzero=True)
    assert s.sympify(a['SU2_character'],locals={'t':t})==6*t+6/t+15
    assert a['doublet_multiplicity']==6 and a['total_cubic_trace']==0

def test_massive_radion_stationarity_from_direct_sum():
    for r in result()['massive_radion']['samples']:
        x=float(r['x_root']);p=r['power'];n=np.arange(1,100,dtype=float);y=n*x
        D=np.sum(np.exp(-y)*(p+p*y+(p+1)*y*y/3+y**3/3)/n**5)
        assert abs(D-p*float(f.mp.zeta(5))/2)<1e-12
        assert float(r['positive_second_derivative'])>0 and float(r['dimensionless_potential'])<0

def test_representation_threshold_matching_is_exact():
    r=result()['representation_thresholds'];x=list(map(s.Rational,r['exact_log_thresholds']));beta=[s.Matrix(list(map(s.Rational,z['beta'])))for z in r['groups']]
    inv=s.Matrix([1/s.Rational('.118'),s.Rational('127.95')*s.Rational('.2312'),s.Rational('127.95')*(1-s.Rational('.2312'))])-s.Matrix([7,16,s.Rational(148,3)])*x[0]
    for b,t in zip(beta,x[1:]):inv+=b*t
    assert inv[0]==inv[1] and inv[2]==s.Rational(8,3)*inv[1] and inv[1]>1
    assert all(1<t<4 for t in x[1:])and 4<x[0]<5
    assert r['LP_margin']>1 and all(1e3<m<r['crossing_GeV']for m in r['thresholds_GeV'])
    assert r['prior_pairing']['liftable']==48

def test_partial_reading_count_and_provenance():
    r=json.loads((f.ROOT/'analysis/2026-10-27_research_intake_coverage.json').read_text())
    assert 55<=sum(x['full_text_model_read_this_continuation']for x in r['pdf_pages'])<210
    assert 14<=sum(x['full_patch_model_read']for x in r['historical_week_commits'])<481
    assert r['reading_increment_20261027_gap']['pages_added']==list(range(119,127))
