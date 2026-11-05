"""Independent equations/negative controls for the five declared mechanisms."""
import importlib,json,pathlib,sys,math
import numpy as np
import pytest
import sympy as s
from scipy.integrate import solve_ivp
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261103_mechanism_portal_protection as P
import toe_20261103_mechanism_four_dimensional_overlap as O
import toe_20261103_mechanism_neutrino_messengers as N
import toe_20261103_mechanism_gravity_identifiability as G

def cert(stem):return json.loads((ROOT/f'data/toe_20261103_mechanism_{stem}.json').read_text())

@pytest.mark.parametrize('y,L',[(.1,3.),(.3,10.),(.8,2.)])
def test_soft_rg_matches_independent_ode(y,L):
    sol=solve_ivp(lambda t,z:np.full(3,2*y*y*sum(z)/(16*math.pi**2)),[0,-L],[0,0,7.],rtol=1e-11,atol=1e-13)
    d,source=P.running_soft(y,L,7.)
    assert np.allclose(sol.y[:,-1],[d,d,source],rtol=1e-10,atol=1e-12)

def test_pointwise_susy_and_soft_sign():
    assert P.cw_curvature(20,0,.05,100)==0
    assert P.cw_curvature(20,.001,.05,100)>0
    assert P.cw_curvature(20,-.001,.05,100)<0
    assert P.running_soft(.01,10,100)[0]<0

def test_small_soft_curvature_derivation_symbolic():
    x,c,m,d=s.symbols('x c m d',positive=True);u=m*m*s.exp(-2*c*x)
    first=d*u*(s.log(u/m**2)-1)/(8*s.pi**2)
    assert s.simplify(s.diff(first,x,2).subs(x,0)-d*c*c*m*m/(2*s.pi**2))==0
    actual=P.cw_curvature(10,1e-6,.1,100)
    expected=1e-6*.1**2*100/(2*math.pi**2*100**2)
    assert actual==pytest.approx(expected,rel=1e-7)

def test_portal_cap_is_specific_naturalness_condition():
    d=cert('portal_protection');assert d['portal_y_benchmark']<1e-23
    assert d['rows'][2]['absolute_curvature_over_H0_squared']==pytest.approx(1,rel=1e-9)
    assert d['rows'][3]['absolute_curvature_over_H0_squared']>90
    assert 'not an experimental limit'in d['boundary']

def test_nilpotent_uplift_identity_and_eta_hessian():
    k,a,f,q,eta=s.symbols('k a f q eta',positive=True)
    lift=s.exp(a*k)*f/s.exp(a*k+eta*a*q*q)
    assert s.simplify(lift.subs(eta,0)-f)==0
    # q is real component, canonical coordinate=sqrt2*q.
    assert s.simplify(s.diff(lift,q,2).subs(q,0)/2+eta*a*f)==0

def test_spectator_control_from_full_potential_series():
    q,a,w,f=s.symbols('q a w f',real=True)
    base=s.exp(a*q*q)*(a*a*q*q*w*w-3*a*w*w)
    assert s.expand(s.diff(base,q,2).subs(q,0)/2)==-2*a*a*w*w
    assert s.expand(s.diff(base+f*s.exp(a*q*q),q,2).subs(q,0)/2)==-2*a*a*w*w+a*f

def test_uplift_neutral_scope_and_instability_controls():
    d=cert('stationary_uplift')
    assert d['target_positive_energy_input']>0
    assert d['stationary_DW_max']<1e-12
    assert min(d['scalar_mass_squared_neutral_eigenvalues'])>0
    assert d['metric_deformation_controls'][-1]['smallest_mass_squared']<0
    assert d['light_spectator_constant_uplift_mass_squared']<0
    assert d['light_spectator_minimal_uplift_mass_squared']>0
    assert d['largest_neutral_mass_over_goldstino_scale']>1

def test_gamma_clifford_algebra():
    gs,g5=O.gammas()
    for i in range(4):
        assert np.allclose(g5@gs[i]+gs[i]@g5,0)
        for j in range(4):assert np.allclose(gs[i]@gs[j]+gs[j]@gs[i],2*(i==j)*np.eye(4))

def test_flux_holonomy_and_gauge_action():
    L=3;p=O.plaquettes(O.links(L),L)
    assert np.allclose(p[0],np.exp(2j*np.pi/L**2))
    assert np.allclose(p[5],np.exp(2j*np.pi/L**2))
    assert np.allclose(p[[1,2,3,4]],1)
    assert np.sum(1-p.real)==pytest.approx(2*L**4*(1-math.cos(2*math.pi/L**2)))

def test_overlap_free_single_species_and_projector():
    D,G,hat,lam=O.operator(O.links(2,0,0),2)
    assert np.linalg.matrix_rank(D,tol=1e-9)==len(D)-4
    assert np.allclose(hat@hat,np.eye(len(D)),atol=1e-12)
    assert np.allclose(D@((np.eye(len(D))-hat)/2),((np.eye(len(D))+G)/2)@D,atol=1e-12)

def test_topological_certificate_matches_rectangular_map():
    d=cert('four_dimensional_overlap');assert d['gauge_covariance_max_defect']<1e-11
    for row in d['rows']:
        assert row['Weyl_codomain_rank']-row['Weyl_domain_rank']==row['overlap_index']
        if row['flux12'] and row['flux34']:
            assert row['overlap_index']==-row['flux12']*row['flux34']
            assert row['Dirac_zero_modes']==1
    q=d['anomaly_free_chiral_U1_example'];assert sum(q)==sum(x**3 for x in q)==0

def test_messenger_schur_complement_by_eliminating_heavy_equations():
    rng=np.random.default_rng(12);Y=rng.normal(size=(3,3));lam=rng.normal(size=(3,2));k=rng.normal(size=3);xi=rng.normal(size=3)
    m,F,K=N.effective(Y,lam,k,xi,1.3,.1+.07j,v=.05)
    n=K.shape[0];B=F[3:,:3];A=F[:3,3:]
    for light in np.eye(3):
        heavy=np.linalg.solve(K,-B@light)
        assert np.allclose(F@np.r_[light,heavy],np.r_[m@light,np.zeros(n)],atol=1e-14)

def test_messenger_exact_determinant_and_reverse_vertex():
    d=cert('neutrino_messengers');e=s.Symbol('epsilon')
    M=s.Matrix([[s.sympify(z,locals={'epsilon':e})for z in row]for row in d['exact_dimensionless_Dirac_matrix']])
    assert s.factor(M.det()+10*e**4/(9*e**2-10))==0
    assert 'Bc_Phistar_Nc'in d['vertex_charge_sums']
    assert set(d['vertex_charge_sums'].values())=={0}
    assert d['above_all_thresholds_total_BL_beta']=='59'

def test_two_entry_rank_control_and_three_entry_spectrum():
    d=cert('neutrino_messengers');assert set(d['two_entry_messenger_random_ranks'])=={2}
    for row in d['rows']:
        assert row['rank']==3 and row['full_vs_Schur_relative_error']<.002
    assert d['illustrative_threshold_over_125GeV_squared']>1e25

def test_finite_range_force_derivative_and_phase():
    a2=.7;lam=.0003;r=.0002;step=1e-8
    potential=lambda x:-(1+a2*math.exp(-x/lam))/x
    numerical=(potential(r+step)-potential(r-step))/(2*step)
    force=(1+a2*(1+r/lam)*math.exp(-r/lam))/r**2
    assert numerical==pytest.approx(force,rel=1e-8)
    assert G.pair_J(r,.00025,1.,a2,lam)!=G.pair_J(r,.00025,1.,0.,lam)

def test_scalar_optical_cancellation_symbolic():
    a,r,l,g,m=s.symbols('a r l g m',positive=True)
    phi=-g*m*(1+a*s.exp(-r/l))/r;psi=-g*m*(1-a*s.exp(-r/l))/r
    assert s.simplify(phi+psi+2*g*m/r)==0

def test_mass_only_degeneracy_and_photon_null_direction():
    d=cert('gravity_identifiability');a=np.array(d['extended_tensor_scalar_photon_response']);n=np.array(d['extended_null_direction'])
    assert np.linalg.matrix_rank(a)==2 and np.allclose(a@n,0)
    assert d['ray_integral_bending_rad']==pytest.approx(d['analytic_bending_rad'],rel=1e-11,abs=0)
    rows=[r for r in d['rows']if r['scalar_range_m']==1e6]
    assert max(r['J_per_second']for r in rows)-min(r['J_per_second']for r in rows)<1e-10
    assert rows[-1]['lensing_over_GR_with_same_force_calibration']<.01

def test_holomorphic_bridge_F_and_D_branch():
    d=cert('holomorphic_bridge');v,lam=s.symbols('v lam',real=True)
    H=s.Matrix([[s.sympify(z,locals={'v':v,'lam':lam})for z in row]for row in d['breaking_Hessian']])
    assert H*s.Matrix([v,-v,0])==s.zeros(3,1)
    assert s.factor((H*H).trace()-4*lam**2*v**2)==0
    assert d['F_at_supplied_real_branch']==['0','0','0'] and d['D_at_branch']==0

def test_holomorphic_bridge_charge_and_beta_cost():
    d=cert('holomorphic_bridge');q=d['left_handed_BL_charges']
    assert all(sum(q[f]for f in term)==0 for term in d['charge_neutral_holomorphic_vertices'])
    assert q['PhiPlus']==-q['PhiMinus']==3
    b=d['SUSY_BL_beta_breakdown'];assert sum(b[k]for k in b if k!='total')==b['total']==102

def test_sector_reference_dimension_obstruction():
    d=cert('sector_reference')
    assert d['free_positive_projector_rank']==162 and d['flux_positive_projector_rank']==163
    assert d['projected_free_reference_rank']<=162
    assert d['missing_target_dimensions']>=1
    assert d['endpoint_frame_projector_operator_error']==pytest.approx(1,rel=1e-10)

def test_sector_comparison_kernel_independent_assembly():
    import toe_20261103_mechanism_sector_reference as S
    U=O.links(2,0,0);H=S.kernel(U,2);D,G,hat,e=O.operator(U,2)
    assert np.allclose(np.linalg.eigvalsh(H),e,atol=1e-12)
    assert np.allclose(H,H.conj().T)

def test_affine_comparison_gap_closure_scope():
    d=cert('sector_reference');a,b=d['affine_gap_closure_bracket']
    assert 0<a<b<1 and b-a<1e-7
    assert d['near_crossing_gap']<1e-6
    assert min(d['endpoint_kernel_gaps'])>.1
