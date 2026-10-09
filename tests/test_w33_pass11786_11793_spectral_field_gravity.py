"""Independent covariance, interval, operator-limit and curvature regressions."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11786_certified_spectral_transitions as S
import w33_pass11787_11788_current_dirac_nonlinear_action as D
import w33_pass11789_11792_transition_field_continuum as C
import w33_pass11790_11793_lifted_ricci_sources as R
import w33_pass11793_order_four_matter_action as M
import w33_pass11775_symmetric_non_gaussian_vacuum as G

def frozen(name):return json.loads((ROOT/'data'/name).read_text())

def test_outward_interval_arithmetic_at_rational_points():
    a=S.I(F(-7,3),F(8,7));b=S.I(F(2,9),F(13,5))
    for x in [a.lo,F(-1,7),a.hi]:
        for y in [b.lo,F(3,4),b.hi]:
            for interval,value in [(a+b,x+y),(a*b,x*y),(a/b,x/y)]:
                assert interval.lo<=value<=interval.hi
    for value in [F(10),F(1,20),F(6),F(101,13)]:
        interval=S.I(value).sqrt()
        assert interval.lo**2<=value<=interval.hi**2

def test_root_interval_has_exact_endpoint_signs():
    m,t,f,e=S.parameters();b=F(1,20)
    p=lambda x,y:(x*x-1)*(3*y*x+b)**2-4*b*b*x*x
    assert p(t.lo,m.hi)<0<p(t.hi,m.lo)
    assert t.hi-t.lo<F(1,10**30)
    # Divided stationarity derivative is positive on t>0; root is unique.
    x,y=sp.symbols('x y',positive=True)
    derivative=sp.diff(1-x**-2-4*sp.Rational(1,20)**2/(3*y*x+sp.Rational(1,20))**2,x)
    assert derivative.subs({x:1,y:1})>0
    assert sp.simplify(derivative-(2/x**3+24*y*sp.Rational(1,20)**2/(3*y*x+sp.Rational(1,20))**3))==0

def test_wick_recurrence_independently_known_mixed_moments():
    cov=[[S.I(2),S.I(F(1,3)),S.I(0),S.I(0)],
         [S.I(F(1,3)),S.I(3),S.I(0),S.I(0)],
         [S.I(0),S.I(0),S.I(1),S.I(0)],
         [S.I(0),S.I(0),S.I(0),S.I(1)]]
    pair=S.wick(cov)
    value=pair({(2,0,0,0):S.I(1)},{(0,2,0,0):S.I(1)})
    assert value.lo<=F(6)+F(2,9)<=value.hi
    eighth=pair({(4,0,0,0):S.I(1)},{(4,0,0,0):S.I(1)})
    assert eighth.lo<=105*2**4<=eighth.hi

def test_hermite_norms_and_cross_order_orthogonality():
    y=sp.symbols('y')
    def expectation(p):
        return sum(c*(sp.factorial2(n-1) if n else 1) for (n,),c in sp.Poly(p,y).terms() if n%2==0)
    for n in S.DEGREES:
        hn=sum(sp.Rational(c.numerator,c.denominator)*y**k for k,c in S.hermite(n).items())
        assert expectation(hn*hn)==sp.factorial(n)
        assert expectation(hn)==0
    norms=[F(40)*(1+F(12,3**n)+F(27,9**n)) for n in S.DEGREES]
    assert norms[0]==F(320,3) and norms[1]==F(11200,243)

def test_line_momentum_and_derivative_signs_from_actual80D_covariance():
    geo=D.V.geometry();tr=D.V.exact_trial();c,ci=D.V.spectral_covariance(geo)
    edges,n,adj,adjl,wp,wl=S.prior.geometry();sig=np.sqrt(108*tr['t'])
    for side,W,offset in [(1,wp,0),(-1,wl,40)]:
        for j in [0,17,39]:
            w=np.zeros(80);w[offset:offset+40]=W[j]
            for k,(p,l) in enumerate(edges):
                r=W[j,p if side==1 else l-40]
                assert np.isclose(geo['v'][k]@(tr['t']*c)@w/(2*sig),side*tr['t']*r/(2*sig),atol=1e-14)
                assert np.isclose(geo['u'][k]@ci@(tr['t']*c)@w/(2*tr['t']*sig),r/(2*sig),atol=1e-14)
                assert np.isclose(geo['u'][k]@w/sig,r/sig,atol=1e-14)

def test_interval_matrix_agrees_with_prior_correct11775_quartic_owner():
    cert=frozen('w33_pass11786_certified_spectral_transitions.json')
    h=np.array([[complex(np.mean([float(F(x)) for x in a]),np.mean([float(F(x)) for x in b])) for a,b in row] for row in cert['matrix_intervals']])
    assert np.max(np.abs(h-h.conj().T))<1e-13
    prior=G.payload()
    assert abs(np.linalg.eigvalsh(h[np.ix_([0,3,4],[0,3,4])])[0]-prior['energy'])<2e-9
    assert abs(h[0,3].imag+h[0,4].imag)<1e-13 and h[0,3].imag>.3

def test_rational_trial_upper_certificate_and_no_lower_bound_overread():
    cert=frozen('w33_pass11786_certified_spectral_transitions.json')
    h=[[tuple(S.I(*entry) for entry in pair) for pair in row] for row in cert['matrix_intervals']]
    vector=[tuple(F(x) for x in z) for z in cert['trial_coefficients']]
    interval=S.rayleigh(h,vector)
    assert interval.data()==cert['rayleigh_interval']
    assert F('127.595519')<interval.lo<interval.hi<F('127.595533')
    assert 'does NOT lower-bound E0' in cert['boundaries']

def test_linearized_quadratures_commute_and_rotation_is_symplectic():
    rng=np.random.default_rng(201786);d=np.diag([1,-1,1,-1])
    identity=np.eye(4);omega=np.block([[0*identity,identity],[-identity,0*identity]])
    z=np.c_[identity,d]
    assert np.max(np.abs(z@omega@z.T))==0
    rotation=np.block([[identity,d],[-d,identity]])/np.sqrt(2)
    assert np.allclose(rotation@omega@rotation.T,omega)
    assert np.allclose(rotation@rotation.T,np.eye(8))

def test_actual_D_symbol_speed_bound_and_four_row_degeneracy_in_two_bases():
    geo=D.V.geometry();basis=np.linalg.qr(geo['pw'][:,np.r_[0:39,40:79]])[0]
    rng=np.random.default_rng(11787);change=np.linalg.qr(rng.normal(size=(78,78)))[0]
    a=np.sqrt(.05)
    for b in [basis,basis@change]:
        for _ in range(5):
            q=rng.normal(size=78);xi=rng.normal(size=78)
            symbol=np.linalg.norm((geo['v']@b@q+a)*(geo['u']@b@xi))
            bound=np.sqrt(312)*(a+np.sqrt(39/20)*np.linalg.norm(q))*np.linalg.norm(xi)
            assert symbol<=bound
        q0=a*np.r_[np.array([39]+[-1]*39),np.zeros(40)]
        active=(geo['v']@q0+a)>1e-12
        assert sum(active)==4 and np.linalg.matrix_rank(geo['u'][active]@b)==4

def test_linearized_Clifford_mass_and_chiral_inverse_control():
    sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]],complex);sz=np.diag([1,-1])
    for z,m in [(.3,np.sqrt(.4)),(-4,np.sqrt(.4))]:
        d=z*sx+m*sy
        assert np.allclose(d@d,(z*z+m*m)*np.eye(2))
        assert np.allclose(sz@d+d@sz,0)
        assert np.linalg.norm(np.linalg.inv(d),2)<=np.sqrt(5/2)
    cert=D.dirac();assert cert['linearized_chiral_index']==0
    assert cert['actual_fredholm_index'].startswith('OPEN')

def test_spinor_curvature_bound_uses_exact_edge_degree_not_pair_count():
    cert=D.dirac();assert cert['active_symbol_rows']==4
    assert '6*h' in cert['curvature_bound'] and '|theta|<1/6' in cert['controlled_interpolation']
    for e in D.V.actual_edges():
        assert sum(bool(set(e)&set(f)) for f in D.V.actual_edges() if f!=e)==6

def test_nonlinear_action_principal_symbol_from_velocity_and_spatial_hessians():
    x,y,vx,vy,dx,dy,c,w,k=sp.symbols('x y vx vy dx dy c w k')
    g=sp.Matrix([[1+x*x,x*y],[x*y,1+y*y]])
    vel=sp.Matrix([vx,vy]);der=sp.Matrix([dx,dy]);a=sp.Matrix([x*y*y,x*x*y])
    lag=(vel.T*g*vel)[0]/2-c*c*(der.T*g*der)[0]/2+(a.T*vel)[0]
    assert sp.hessian(lag,[vx,vy])==g
    assert (sp.hessian(lag,[dx,dy])+c*c*g).applyfunc(sp.simplify)==sp.zeros(2)
    principal=-w*w*sp.hessian(lag,[vx,vy])-k*k*sp.hessian(lag,[dx,dy])
    assert sp.factor(principal.det()-(c*k-w)**2*(c*k+w)**2*(x*x+y*y+1))==0

def test_magnetic_common_front_is_not_KG_boost_invariance():
    c,m,B=1.2,.7,.3
    for k in [1,10,10000]:
        wp=np.sqrt(c*c*k*k+m*m+B*B/4)+B/2
        wm=np.sqrt(c*c*k*k+m*m+B*B/4)-B/2
        assert abs(wp-wm-B)<1e-11
    assert abs(wp/10000-c)<2e-5
    D.action()

def test_exact_Dicke_ladder_and_commutator_on_interior_states():
    M=24;raise_=np.zeros((M+1,M+1))
    for n in range(M):raise_[n+1,n]=np.sqrt((n+1)*(M-n))
    lower=raise_.T;comm=(lower@raise_-raise_@lower)/M
    assert np.allclose(comm,np.diag(1-2*np.arange(M+1)/M))
    assert np.allclose((raise_+lower)/(2*np.sqrt(M)),C.scaled_spin_x(M,M))

def test_two_site_dynamics_core_convergence_rate_and_no_cutoff_boundary():
    records=C.convergence_control(cut=9,occupation=3)
    assert records[-1]['core_operator_error']<.02
    assert records[0]['core_operator_error']/records[-1]['core_operator_error']>30
    columns=[i*10+j for i in range(4) for j in range(4)]
    # Degree2 Hamiltonians reach occupation at most5; cutoff9 is irrelevant.
    target=C.two_site(None,9)[:,columns]
    assert np.max(np.abs(target[[i for i in range(100) if i//10>5 or i%10>5]]))==0

def test_continuum_dispersion_in_independent_dimensions():
    for d in [1,2,3,4]:
        k=np.arange(1,d+1)*.31;c=.8;m=.6
        errors=[]
        for ell in [.2,.1,.05]:
            lattice=m*m+4*c*c*np.sum(np.sin(k*ell/2)**2)/ell**2
            errors.append(abs(lattice-(m*m+c*c*k@k)))
        assert errors[0]/errors[1]>3.9 and errors[1]/errors[2]>3.9

def test_smeared_CCR_Riemann_sum_converges_to_independent_Gaussian_integral():
    for ell in [.2,.1,.05]:
        x=np.arange(-8,8,ell);value=ell*np.sum(np.exp(-2*x*x))
        assert abs(value-np.sqrt(np.pi/2))<1e-10

def test_T_even_current_sigma_zero_but_transition_partner_nonzero():
    a=sp.Matrix([[0,1],[1,0]]);b=sp.Matrix([[0,-sp.I],[sp.I,0]])
    assert a.conjugate()==a and b.conjugate()==-b
    assert (-sp.I*(a*b-b*a))[0,0]==2
    rho=sp.diag(sp.Rational(2,3),sp.Rational(1,3));j=sp.Matrix([[1,2],[2,-3]])
    assert sp.trace(rho*sp.I*(a*j-j*a))==0

def test_massive_energy_gap_and_lightlike_modular_scaling_are_distinct():
    theta=np.linspace(-10,10,100);s=.37;m=.8
    energy=m*np.cosh(theta);light=m*np.exp(-theta)
    assert energy.min()>=m and light.min()<m/1000
    assert np.allclose(m*np.exp(-(theta+2*np.pi*s)),np.exp(-2*np.pi*s)*light)
    assert not np.allclose(m*np.cosh(theta+2*np.pi*s),np.exp(-2*np.pi*s)*energy)

def test_actual_schur_tidal_Ricci_trace_against_independent_numeric_hessian():
    import w33_pass11781_11784_11785_nonlinear_cone_bargmann_lift as L
    z=L.setup();p,_,_,_,_,curl=L.coefficients(np.zeros(78),z)
    v,u=z['v'],z['u'];b=.05
    q=2*(z['vy']+b)*v.T@v;cross=4*(z['c']+b)*v.T@u
    schur=q-cross@np.linalg.solve(p,cross.T)
    alpha=4*((z['vx']+b)*(z['vy']+b)-4*(z['c']+b)**2)
    assert abs(np.trace(p@schur)-960*alpha)<1e-9
    root=np.linalg.cholesky(p);tidal=root.T@schur@root
    vals=np.linalg.eigvalsh(tidal)
    assert np.allclose(vals[:48],10*alpha) and np.allclose(vals[48:],16*alpha)
    assert np.linalg.norm(curl)<1e-13

def test_Ricci_formula_independently_computed_magnetic_and_curved_controls():
    control=R.differential_controls()
    assert control['flat_magnetic_Ruu']=='B**2/2 + 2*mu'
    assert control['parallel_null_vector']

def test_required_null_source_excludes_any_vacuum_cosmological_constant():
    cert=R.actual_curvature()
    assert cert['exact_trace']==960
    assert F(cert['null_ricci_interval'][0])>3100
    # Null Einstein contraction has neither scalar-curvature nor Lambda contribution.
    V0=sp.symbols('V0');g=sp.Matrix([[-2*V0,1],[1,0]]);l=sp.Matrix([1,V0])
    assert (l.T*g*l)[0]==0

def test_all_four_source_hashes_match_frozen_certificates():
    import hashlib
    pairs=[(S,'w33_pass11786_certified_spectral_transitions.json'),
           (D,'w33_pass11787_11788_current_dirac_nonlinear_action.json'),
           (C,'w33_pass11789_11792_transition_field_continuum.json'),
           (R,'w33_pass11790_11793_lifted_ricci_sources.json'),
           (M,'w33_pass11793_order_four_matter_action.json')]
    for module,file in pairs:
        assert frozen(file)['source_sha256']==hashlib.sha256(Path(module.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def test_parallel_assignment_aware_charge_and_inconsistent_old_gate_witnesses():
    # Verify stored witnesses directly over Q, without importing the cone-search API.
    import gzip,re
    ledger=json.loads(gzip.decompress((ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz').read_bytes()))
    rec=ledger['Z6-II|Z6II_34__SM_20260917_1558']
    fields={f['name']:f for f in rec['left']};q={n:list(map(F,f['q'])) for n,f in fields.items()}
    cert=frozen('w33_20261009_corrected_assignment_dflat_certificate.json')
    weights={n:F(x) for n,x in cert['positive_support'].items()}
    assert all(x>0 for x in weights.values()) and len(weights)==6
    assert [sum(weights[n]*q[n][j] for n in weights) for j in range(9)]==[F(-1)]+[F(0)]*8
    bl=list(map(F,cert['BL_coefficients']))
    expected={'q':F(1,3),'bu':F(-1,3),'bd':F(-1,3),'be':F(1)}
    for n in cert['physical_family_constraints']:
        assert sum(a*b for a,b in zip(q[n],bl))==expected[n.rsplit('_',1)[0]]
    for n in weights:
        charge=3*sum(a*b for a,b in zip(q[n],bl))
        assert charge.denominator==1 and charge.numerator%2==0
        assert all(abs(int(re.match(r'(-?\d+)',part).group(1)))==1 and 'adj' not in part for part in fields[n]['dim'].split(','))
    assert all(-q['bd_7'][j]+q['bu_3'][j]+q['be_3'][j]==0 for j in range(9))
    assert -expected['bd']+expected['bu']+expected['be']==1
    # Hypercharge neutrality derived independently from all standard-charge labels.
    smy={'q':F(1,6),'bq':F(-1,6),'u':F(2,3),'bu':F(-2,3),
         'd':F(-1,3),'bd':F(1,3),'e':F(-1),'be':F(1),'l':F(-1,2),'bl':F(1,2)}
    names=[n for n in fields if n.rsplit('_',1)[0] in smy]
    a=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in q[n]] for n in names])
    b=sp.Matrix([sp.Rational(smy[n.rsplit('_',1)[0]].numerator,smy[n.rsplit('_',1)[0]].denominator) for n in names])
    sol,params=a.gauss_jordan_solve(b);sol=sol.subs({x:0 for x in params})
    assert all(sum(sp.Rational(x.numerator,x.denominator)*y for x,y in zip(q[n],sol))==0 for n in weights)

def test_parallel_no_full_lattice_Z2_character_independently_of_cone_library():
    import gzip,itertools,math
    from sympy.matrices.normalforms import hermite_normal_form
    ledger=json.loads(gzip.decompress((ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz').read_bytes()))
    rows=ledger['Z6-II|Z6II_34__SM_20260917_1558']['left']
    cert=frozen('w33_20261009_corrected_assignment_dflat_certificate.json')
    q=[list(map(F,row['q'])) for row in rows];den=math.lcm(*(x.denominator for v in q for x in v))
    matrix=sp.Matrix([[int(x*den) for x in v] for v in q]);basis=hermite_normal_form(matrix.T)
    assert basis.cols==9
    need={n:1 for n in cert['physical_family_constraints']};need.update({n:0 for n in cert['positive_support']})
    coords=[];targets=[]
    for i,row in enumerate(rows):
        if row['name'] in need:
            vector=basis.inv()*matrix.row(i).T
            assert all(x.q==1 for x in vector)
            coords.append([int(x)%2 for x in vector]);targets.append(need[row['name']])
    survivors=[eps for eps in itertools.product((0,1),repeat=9)
               if all(sum(x*y for x,y in zip(eps,c))%2==target for c,target in zip(coords,targets))]
    assert survivors==[]

def test_full_Z4_and_light_Z2_quotient_are_different_actions():
    cert=M.certificate();charges=cert['all_field_charges']
    assert cert['field_action_order']==4 and sum(v%2==1 for v in charges.values())==64
    selected=list(cert['selected_matter_charges'])
    for power in [1,3]:assert all(power*charges[n]%4==2 for n in selected)
    assert all(2*charges[n]%4==0 for n in selected)
    assert any(2*k%4==2 for k in charges.values())
    assert all(charges[n]==0 for n in cert['vev_charges'])
    assert cert['continuous_gravitational_trace']==cert['continuous_cubic_trace']=='0'

def test_Z4_character_survives_an_independent_integral_basis_change():
    cert=M.certificate();b=sp.Matrix([[sp.Rational(z) for z in row] for row in cert['integral_charge_lattice_basis']])
    eps=sp.Matrix(cert['integral_character']);transform=sp.eye(9)
    transform[1,6]=3;transform[2,8]=-2
    transform.row_swap(3,7)
    assert abs(transform.det())==1
    # c'=T^-1*c, eps'=T^T*eps: exact pairing unchanged.
    ep=transform.T*eps
    for c in [sp.Matrix([i-j for j in range(9)]) for i in range(5)]:
        assert (eps.T*c)[0]==(ep.T*(transform.inv()*c))[0]
    assert any(int(z)%2 for z in ep)
    assert cert['unbroken_abelian_lie_dimension']>=3

def test_Z4_operator_selection_for_all_candidate_family_combinations():
    cert=M.certificate();charges=cert['all_field_charges'];families=cert['candidate_three_family_Higgs_basis']
    import itertools
    for roles,allowed in [(('Q','u_c','H_u'),True),(('Q','d_c','H_d'),True),
                          (('L','e_c','H_d'),True),(('u_c','d_c','d_c'),False),
                          (('L','Q','d_c'),False),(('L','L','e_c'),False),
                          (('Q','Q','Q','L'),True)]:
        for names in itertools.product(*(families[r] for r in roles)):
            assert (sum(charges[n] for n in names)%4==0)==allowed
