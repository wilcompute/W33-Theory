"""Independent controls on five declared physical constructions."""
import functools,itertools,json,math,pathlib,sys
import mpmath as mp
import numpy as np
import pytest
import sympy as s
from scipy.linalg import expm
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from toe_20261103_gravity_entanglement_models import density,pt,feedback_density
from toe_20261103_supergravity_vacuum_completion import setup,global_point,values,WEIGHTS

def data(stem):return json.loads((ROOT/f'data/toe_20261103_{stem}.json').read_text())

def test_null_primitive_charge_preserving_mirror():
    K=s.diag(1,1,-1,-1);q=s.Matrix([3,4,5,0]);L=s.Matrix([[1,-2,-1,2],[2,1,2,1]])
    assert L*K*L.T==s.zeros(2) and L*K*q==s.zeros(2,1)
    gcd=math.gcd(*(int(L[:,cols].det())for cols in itertools.combinations(range(4),2)))
    assert gcd==1
    assert math.gcd(*(int((2*L)[:,cols].det())for cols in itertools.combinations(range(4),2)))==4

@pytest.mark.parametrize('a',[s.Integer(1),s.Rational(5,2),s.Integer(3)])
def test_relevance_and_causal_characteristics(a):
    K=s.diag(1,1,-1,-1);L=s.Matrix([[1,-2,-1,2],[2,1,2,1]]);P=L.T*L/10;V=a*P+(s.eye(4)-P)/a
    assert V*K*V==K
    assert (L[0,:]*V.inv()*L[0,:].T)[0]/2==5/a
    assert (5/a<2)==(a>s.Rational(5,2))
    assert (K*V).charpoly().as_expr().expand()==s.Symbol('lambda')**4-2*s.Symbol('lambda')**2+1

def test_full_quark_normalized_anomaly_search_control():
    found=set()
    for a in range(-40,41):
        for b in range(a,41):
            c=9-a-b
            if c<b or c>40:continue
            if a**3+b**3+c**3==81:found.add((a,b,c))
    assert found=={(-18,10,17),(-15,12,12),(3,3,3)}
    assert found==set(map(tuple,data('sterile_anomaly_operators')['all_quark_normalized_integer_sectors']))

@pytest.mark.parametrize('charges,allowed',[( [-18,10,17],False),([-15,12,12],True),([3,3,3],True)])
def test_operator_selection_is_stronger_than_anomalies(charges,allowed):
    assert sum(charges)==9 and sum(q**3 for q in charges)==81
    assert all((q-3)%9==0 for q in charges)==allowed
    assert all(q%3==0 for q in charges)==allowed

@pytest.mark.parametrize('charges',[[1,1,1],[-5,4,4]])
def test_no_majorana_operator_from_single_breaking_scalar(charges):
    for power in range(-20,21):
        assert -6+9*power!=0
        assert all(3*(a+b)+9*power!=0 for a,b in itertools.combinations_with_replacement(charges,2))

def test_generic_exotic_dirac_mass_hierarchy():
    Y=np.array([[1,2,1],[2,1,3],[1,1,1]],float)
    roots=[]
    for eps in [1e-3,1e-4]:
        M=Y@np.diag([eps,eps,eps**2]);sv=np.linalg.svd(M,compute_uv=False);roots.append(sv)
        assert abs(np.linalg.det(M)/eps**4-1)<1e-12
    assert np.max(abs(roots[1][:2]/roots[0][:2]-.1))<1e-6
    assert abs(roots[1][-1]/roots[0][-1]-.01)<1e-6

@pytest.mark.parametrize('row',range(6))
def test_radiative_cap_and_mass_scaling(row):
    p=data('dark_radiative_stability')['rows'][row];m=p['MS_no_curvature_cancellation_DM_mass_cap_eV'];Mpl=2.435e27
    curvature=4*p['cp']**2*m**4/(8*math.pi**2*Mpl**2)
    assert abs(curvature/p['H0_eV']**2-1)<2e-14
    scan=p['mass_scan'];assert abs(scan[-1]['MS_curvature_over_H0_squared']/scan[-2]['MS_curvature_over_H0_squared']-1e12)<.01

def test_twice_subtracted_residual_is_quartic_not_cubic():
    mp.mp.dps=60;a=mp.mpf('.05')
    def residual(x):return mp.exp(-4*a*x)*(2*a*x+mp.mpf('1.5'))-(mp.mpf('1.5')-4*a*x+4*a*a*x*x)
    x=mp.mpf('0.0001');ratio=residual(x)/residual(x/2)
    assert abs(ratio-16)<mp.mpf('.001')
    assert abs(residual(x)/x**4+mp.mpf(16)/3*a**4)<mp.mpf('1e-9')

@functools.lru_cache(None)
def functions():return setup()

@pytest.mark.parametrize('row',range(9))
def test_actual_covariant_supergravity_vacua(row):
    p=data('supergravity_vacuum_completion')['rows'][row];phi=np.array([complex(*z)for z in p['scalar_VEV_complex_pairs']]);eps=complex(*p['epsilon']);Mp=p['Planck_mass_in_input_units']
    W,F,H=values(functions(),phi,eps);D=F+WEIGHTS*phi.conj()*W/Mp**2
    assert np.max(abs(D))<3e-12
    assert p['potential']<0 and abs(p['potential']+3*p['gravitino_mass']**2*Mp**2)<1e-17
    assert min(p['neutral_scalar_mass_squared'])>0

def test_tuned_constant_has_a_real_cost():
    p=data('supergravity_vacuum_completion');eps=.001+0j;phi=global_point(eps);wc=complex(*p['tuned_constant_complex_pair'])
    W,F,H=values(functions(),phi,eps,wc)
    assert abs(W)<1e-13 and np.max(abs(F))<3e-13
    assert p['single_constant_control'][1]['potential']<0 and p['single_constant_control'][2]['potential']<0
    assert all(r['naive_uplift_holomorphic_gradient_max']>0 for r in p['rows'])

@pytest.mark.parametrize('gamma',[0.,.5,1.,1.5])
def test_entanglement_closed_form_against_full_liouvillian(gamma):
    I=np.eye(4);Z1=np.diag([1,1,-1,-1]);Z2=np.diag([1,-1,1,-1]);H=Z1@Z2;t=.37
    generator=-1j*(np.kron(H,I)-np.kron(I,H.T))+gamma*(np.kron(Z1,Z1)+np.kron(Z2,Z2)-2*np.eye(16))
    evolved=(expm(t*generator)@np.ones(16)/4).reshape(4,4)
    assert np.max(abs(evolved-density(1,gamma,t)))<2e-15
    if gamma>=1:assert np.linalg.eigvalsh(pt(evolved))[0]>-2e-15
    else:assert np.linalg.eigvalsh(pt(evolved))[0]<0

def test_local_feedback_map_is_not_silently_unitary():
    feedback=feedback_density(1,.7,800);unitary=density(1,0,.7)
    assert np.linalg.eigvalsh(pt(feedback))[0]>=-1e-14
    assert np.linalg.eigvalsh(pt(unitary))[0]<-.4
    assert np.max(abs(feedback-density(1,1,.7)))<.001

def test_abelian_beta_coefficients_and_mixing():
    p=data('abelian_uv_matching');rows={tuple(r['sterile_Q']):r for r in p['rows']}
    assert s.sympify(rows[(3,3,3)]['beta_matrix'][1][1])==s.Rational(41,3)
    assert s.sympify(rows[(-15,12,12)]['beta_matrix'][1][1])==s.Rational(149,3)
    for row in p['rows']:
        B=s.Matrix([[s.sympify(x)for x in r]for r in row['beta_matrix']])
        assert B[0,1]==s.Rational(16,3) and B.det()>0

def test_coupled_landau_scale_and_operator_cutoff():
    p=data('abelian_uv_matching');scale=p['operator_scale_example'];logcut=math.log(scale['operator_cutoff_GeV']/scale['matching_scale_GeV']);gy=scale['gY_input']
    for row in p['rows']:
        B=np.array([[float(s.sympify(x))for x in r]for r in row['beta_matrix']]);cap=row['gBL_upper_bound_no_one_loop_pole_through_cutoff']
        boundary=np.diag([1/gy**2,1/cap**2])-logcut*B/(8*math.pi**2)
        assert abs(np.linalg.det(boundary))<1e-11
        for r in row['scans']:
            K=np.diag([1/gy**2,1/r['gBL_input']**2])-r['log_Landau_scale_over_matching']*B/(8*math.pi**2)
            assert abs(np.linalg.eigvalsh(K)[0])<2e-13

def test_complete_fermions_do_not_cancel_light_Higgs_mixing():
    p=data('abelian_uv_matching')['orthogonality_control']
    assert p['fermion_Y_X_trace']==0 and p['light_Higgs_Y_X_scalar_trace']==-2
    assert s.sympify(p['total_mixed_one_loop_trace_coefficient'])==-s.Rational(2,3)
    assert p['complete_Higgs5_scalar_trace']==0
