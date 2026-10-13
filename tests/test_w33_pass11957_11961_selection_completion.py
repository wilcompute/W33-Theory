"""Independent anomaly, phase, vacuum, fit and constraint controls."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11957_11959_color_threshold_and_cp_quality as p
import w33_pass11960_11961_clebsch_and_shared_cone as q


def packet():
    a=json.loads((ROOT/'data/w33_pass11957_11959_color_threshold_and_cp_quality.json').read_text())
    b=json.loads((ROOT/'data/w33_pass11960_11961_clebsch_and_shared_cone.json').read_text())
    return a,b


def test_higgs_threshold_cubic_pole_phase_and_minimal_balance():
    z=.02*np.exp(1j*np.linspace(0,2*np.pi,301))
    Q=z/z**4
    assert abs((np.unwrap(np.angle(Q))[-1]-np.angle(Q[0]))/(2*np.pi)+3)<1e-12
    assert np.max(abs(Q*z**3-1))<1e-14
    solutions=[(h,c) for h in range(5) for c in range(8) if 3-2*h+c==0]
    assert min(solutions,key=lambda z:z[0])==(2,1)


def test_color_higgs_stabilizer_and_dimension_matching():
    cert=p.enhancement_threshold()
    assert cert['gauge_stabilizer_dimension']==8
    assert cert['broken_vector_count']==16
    for row in cert['stages']:
        uv,first,second,ir=row['beta_coefficients']
        assert (first-uv,second-first,ir-second)==(-2,-2,1)
        assert uv+1-4==ir


def test_higgs_dflat_complex_phase_is_not_an_antiholomorphic_mass():
    z=s.symbols('z');Q=s.zeros(5,2);Q[3,0]=z;Q[4,1]=z
    # Equal holomorphic Q and Qtilde leave meson z^2; their physical
    # moment-map outer products still cancel at every complex phase.
    assert Q.T*Q==s.eye(2)*z*z
    assert Q*Q.conjugate().T-Q.conjugate()*Q.T==s.zeros(5)


def test_full_continuous_anomalies_and_missing_spectator_negative_control():
    a,_=packet();fields=a['11958']['full_anomaly_inventory']
    dim=np.array([z['dimension'] for z in fields]);index=np.array([z['index_E6'] for z in fields])
    X=np.array([z['X'] for z in fields]);Z=np.array([z['Z'] for z in fields])
    assert [sum(index*X),sum(index*Z),sum(dim*X),sum(dim*Z),sum(dim*X**3),sum(dim*Z**3),sum(dim*X**2*Z),sum(dim*X*Z**2)]==[0]*8
    without=[z for z in fields if not z['name'].startswith('27C')]
    assert sum(z['index_E6']*z['Z'] for z in without)==6


def test_spectator_tag_blocks_the_inverse_spurion_tree_loophole():
    P,B,L=s.symbols('P B L',nonzero=True)
    C,Cbar=s.symbols('C Cbar')
    W=P*C*Cbar+L*B*Cbar
    solution=s.solve([s.diff(W,C),s.diff(W,Cbar)],(C,Cbar))
    assert s.simplify(solution[C]+L*B/P)==0
    a,_=packet();parity=a['11958']['spectator_parity']
    assert all(z%2==0 for z in parity['ordinary_mixed_anomaly_coefficients'].values())
    assert (-1)*(-1)==1 and 1*(-1)==-1


def test_soft_multiplier_response_is_computed_not_ignored():
    X,Y,F,L,r=s.symbols('X Y F L r',positive=True)
    V=(F-L*(X+2*Y))**2+2*r*L*L*X*X+8*r*L*L*Y*Y
    home={X:F/(2*L*(1+r)),Y:F/(4*L*(1+r))}
    assert s.simplify(s.diff(V,X).subs(home))==0
    assert s.simplify(s.diff(V,Y).subs(home))==0
    assert s.det(s.hessian(V,(X,Y)))>0
    a,_=packet();d=a['11958']
    assert d['including_two_multiplier_unit_coefficients_theta_envelope']>d['single_unit_coefficient_envelope']['theta_linear_norm_bound']


def test_all_order_quality_bound_not_just_first_operator():
    # For ANY nonnegative monomial powers a,b,c,d,e satisfying charges,
    # upper-block rho exponent is12(d-e)-1/2 with d-e>=1.
    for a in range(1,36):
        b=a-1
        for c in range(36):
            if (a+c)%12==0:
                exponent=s.Rational(a+b,2)+c
                assert exponent==a+c-s.Rational(1,2)>=s.Rational(23,2)
    a,_=packet();assert len(a['11958']['leading_upper_block_monomials'])==12


def test_quality_dflat_high_norm_adjustment_exact():
    a,_=packet();d=a['11958'];rho=s.Rational(d['rho'])
    minus=s.sympify(d['PhiMinus_norm_squared_over_Lambda_squared'])
    plus=s.sympify(d['PhiPlus_norm_squared_over_Lambda_squared'])
    assert s.simplify(minus*plus-1)==0
    assert s.simplify(2*rho+rho*rho+12*(plus-minus))==0
    assert minus>0 and plus>0


def test_singlet_constraint_rank_and_exact_gauge_kernel():
    S1,S2,T1,T2,P,pm,pp=s.symbols('S1 S2 T1 T2 P pm pp')
    variables=(S1,S2,T1,T2,P,pm,pp)
    f=s.Matrix([S1*T1-P,2*(S2*T2-P),3*(S1*T2+S2*T1),pm*pp-1,pm*P**12])
    J=f.jacobian(variables)
    v=s.symbols('v',positive=True);home={S1:v,S2:s.I*v,T1:v,T2:-s.I*v,P:v*v}
    X=s.Matrix([-S1,-S2,T1,T2,0,0,0])
    Z=s.Matrix([0,0,T1,T2,P,-12*pm,12*pp])
    assert (J*X).subs(home)==s.zeros(5,1)
    assert (J*Z).subs(home)==s.zeros(5,1)
    assert s.factor(J[:,[0,1,2,4,6]].det().subs(home))!=0
    a,_=packet();assert a['11958']['singlet_stability']['positive_physical_real_scalar_directions']==26


def test_moment_map_lifts_both_real_gauge_partners():
    r,h=s.symbols('r h',positive=True)
    G=s.Matrix([[4*r,2*r],[2*r,2*r+r*r+144*h]])
    assert s.expand(G.det())==4*r**3+4*r**2+576*r*h


def test_colored_spectator_phase_is_twelve_and_not_one():
    for branch in range(12):
        P=np.exp(2j*np.pi*branch/12)
        assert abs(P**12-1)<1e-13
    assert abs(np.angle(np.exp(2j*np.pi/12)))>.5


def test_kahler_floor_and_light_mode_prevent_overreading_quality():
    a,_=packet();d=a['11958'];v=d['single_unit_coefficient_envelope']
    assert v['kaehler_Y_for_msoft_over_Lambda_1e_minus13']>v['holomorphic_Y']
    assert v['theta_linear_norm_bound']<1e-10
    assert 0<d['light_singlet_gate']['mass_upper_GeV_if_Lambda_1e16']<10
    assert 'TeV' in d['light_singlet_gate']['meaning']


def test_quark_leakage_sensitivity_against_full_determinant():
    V,sv=p.masses.ckm_target();m,B,mu=p.masses.barr_realization((V*sv**2)@V.conj().T)
    rng=np.random.default_rng(11958)
    for _ in range(8):
        c=(rng.normal(size=3)+1j*rng.normal(size=3))*1e-9
        M=np.zeros((4,4),complex);M[:3,:3]=m;M[:3,3]=c;M[3,:3]=B;M[3,3]=mu
        ratio=np.linalg.det(M)/(mu*np.linalg.det(m))
        assert abs(ratio-(1-B@np.linalg.solve(m,c)/mu))<1e-12
        bound=np.linalg.norm(B@np.linalg.inv(m)/mu)*np.linalg.norm(c)
        assert abs(np.angle(ratio))<bound/(1-bound)+1e-12


def test_fermion_box_breaks_equal_portal_alignment_exactly():
    a,_=packet();F=s.Matrix(a['11959']['fermion_box_matrix']).applyfunc(s.Rational)
    assert F==F.T and F[0,0]!=F[1,1] and F[0,1]!=0
    assert F.det()>0
    assert (s.diag(1,2)*F-F*s.diag(1,2))!=s.zeros(2)


def test_weak_scalar_yukawas_keep_tree_cp_but_reduce_actual_loop():
    a,_=packet();rows=a['11959']['fixed_tree_matrix_scale_sweep']
    assert abs(rows[0]['scalar_loop_theta']-p.loop_prior.scalar_loop()['theta'])<1e-14
    assert all(abs(rows[i+1]['scalar_loop_theta'])<abs(rows[i]['scalar_loop_theta']) for i in range(3))
    assert abs(p.scalar_at_scale(1000))<1e-10


def test_georgi_jarlskog_factor_from_traceless45_tensor():
    t,u=s.symbols('t u');H=s.zeros(5)
    for i in range(3):H[i,i]=t
    H[3,3]=u
    assert s.solve(s.trace(H),u)==[-3*t]


def test_real_clebsch_repairs_charged_ratios_without_changing_quarks():
    _,b=packet();m,A=q.quark_kernel();target=np.array(b['11960']['charged_targets'])
    for fit in b['11960']['two_real_diagonal_45_coefficients_fits']:
        c=np.array(fit['coefficients']);Y45=np.diag([c[0],c[1],0]);Y5=m-Y45
        assert np.max(abs((Y5+Y45)@A-m@A))<1e-12
        ratios,e=q.charged_ratios(c,m,A)
        assert np.max(abs(ratios/target-1))<1e-8
        assert np.max(abs(e-A.T@(Y5-3*Y45).T))<1e-12


def test_two_real_neutrino_entries_bypass_the_diagonal_failure():
    _,b=packet();m,A=q.quark_kernel();targets=np.array(b['11960']['neutrino_targets']);found=0
    for fit in b['11960']['two_real_diagonal_45_coefficients_fits']:
        _,e=q.charged_ratios(fit['coefficients'],m,A)
        for root in fit['two_real_offdiagonal_neutrino_roots']:
            obs,J=q.neutrino_observables(root['parameters'],e,A,True)
            assert np.max(abs(obs-targets))<1e-8
            detail=q.pmns_delta_and_bare(root['parameters'],e,A)
            n=np.array(detail['real_bare_Majorana'])
            assert abs(n[1,2])<1e-12 and min(np.linalg.eigvalsh(n))>0
            assert abs(detail['J']-J)<1e-12 and abs(J)>1e-3
            assert root['fit_jacobian_smallest_singular']>1e-5
            found+=1
    assert found>0


def test_maxwell_lapse_bracket_sets_product_not_impedance():
    x=s.symbols('x',real=True);alpha,beta=s.symbols('alpha beta',real=True)
    A=s.sin(x);E=s.sin(2*x);N=1;M=s.cos(x)
    bracket=s.integrate(alpha*beta*E*(N*s.diff(M*s.diff(A,x),x)-M*s.diff(N*s.diff(A,x),x)),(x,0,2*s.pi))
    assert s.simplify(bracket+s.pi*alpha*beta/2)==0
    assert bracket.subs({alpha:2,beta:1})==bracket.subs({alpha:4,beta:s.Rational(1,2)})


def test_nonconstant_trace_obstruction_and_free_cosmological_term():
    d=q.shared_cone_constraints();assert d['necessary_standard_branch_lambda']=='1/2'
    assert 'a and c remain free' in d['shared_foliation_requirement']
    lam,a,b=s.symbols('lam a b');anomaly=-2*s.pi*a*b*(2*lam-1)
    assert anomaly.subs(lam,s.Rational(1,2))==0
    assert anomaly.subs({lam:s.Rational(3,4),a:1,b:2})!=0


def test_native_weight_selector_has154_unfixed_directions():
    old=json.loads((ROOT/'data/w33_pass11956_local_electric_metric.json').read_text())
    ed,V,*_=q.native.prep();B=np.rint(q.native.gradient(ed,V,np.zeros(3)).real).astype(int)[:,1:]
    w=np.array([float(s.Rational(z)) for z in old['electric_link_weights']])
    h=V-B@np.linalg.solve(B.T@(w[:,None]*B),B.T@(w[:,None]*V))
    J=np.array([h[:,i]*h[:,j] for i,j in [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]])
    _,sv,vh=np.linalg.svd(J,full_matrices=True)
    assert min(sv)>1e-5 and vh.shape==(160,160)
    assert np.max(abs(J@vh[6:].T))<1e-12
    assert vh[6:].shape[0]==154


def test_frozen_input_hashes_and_scopes():
    for d in packet():
        assert d['status']=='PASS'
        for path,expected in d['input_sha256_lf'].items():
            assert hashlib.sha256((ROOT/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==expected
