"""Independent exact and numerical controls for the five continuation maps."""
from pathlib import Path
from itertools import product
import hashlib,json,sys
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12194_12198_native_completion as m
D=json.loads((ROOT/'data/w33_pass12194_12198_native_completion.json').read_text())
w=(-1+s.I*s.sqrt(3))/2

def mat(data):return s.Matrix(data)
def close(a,b,tol=1e-11):assert np.max(abs(np.asarray(a)-np.asarray(b)))<tol

def test_source_bound_certificate_and_actual_dependency_hashes():
    p=D['provenance'];assert p['source_sha256']==hashlib.sha256((ROOT/'analysis/w33_pass12194_12198_native_completion.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    for path,value in p['prior_sources'].items():assert hashlib.sha256((ROOT/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==value
    assert {D[x]['pass']for x in ('flavour','gravity','magic','quantum_normalizer','narain')}==set(range(12194,12199))

def test_narain_integral_even_unimodular_basis_and_glue():
    d=D['narain'];eta=mat(d['eta_original']);C=mat(d['momentum_winding_basis'])
    J=s.zeros(4);J[:2,2:]=s.eye(2);J[2:,:2]=s.eye(2)
    assert C.det() in (-1,1) and C.T*eta*C==J and eta.det()==1
    assert all(x.q==1 for x in eta) and all(eta[i,i]%2==0 for i in range(4))
    P=s.Matrix([[-1,0,-1,1],[-1,1,-1,0],[0,0,1,-2],[0,0,1,1]])
    A=s.Matrix([[2,-1],[-1,2]])
    assert abs(P.det())==3 and P.T*eta*P==s.diag(A,-A)

def test_generalized_metric_torus_parameters_and_complete_root_bound():
    d=D['narain'];eta=mat(d['eta_original']);H=mat(d['positive_generalized_metric']);C=mat(d['momentum_winding_basis'])
    G=mat(d['torus_G']);B=mat(d['torus_B'])
    assert H*eta.inv()*H==eta and G.det()==s.Rational(3,4)
    assert C.T*H*C==s.BlockMatrix([[G.inv(),-G.inv()*B],[B*G.inv(),G-B*G.inv()*B]]).as_explicit()
    assert s.simplify(s.sympify(d['T'])-w)==0 and s.simplify(s.sympify(d['U'])-w)==0
    assert all(2*H.inv()[i,i]<=9 for i in range(4))
    for sector,sign in (('left_roots',1),('right_roots',-1)):
        roots=set()
        for v in product(range(-3,4),repeat=4):
            x=mat(v)
            if (x.T*H*x)[0]==2 and (x.T*eta*x)[0]==2*sign:roots.add(v)
        assert roots==set(map(tuple,d[sector])) and len(roots)==6

def test_infinite_duality_is_not_a_finite_metric_symmetry():
    d=D['narain'];N=mat(d['infinite_duality_generator']);eta=mat(d['eta_original']);H=mat(d['positive_generalized_metric'])
    assert N.T*eta*N==eta and N.T*H*N!=H
    assert N!=s.eye(4) and (N-s.eye(4))**2==s.zeros(4)
    assert N**17==s.eye(4)+17*(N-s.eye(4))
    assert d['finite_normalizer_sign_counts']=={'1':72,'-1':72}

def test_full_native_symmetry_fixes_all_four_narain_moduli():
    _,R=m.prior.native.native();eta=mat(D['narain']['eta_original']);H=mat(D['narain']['positive_generalized_metric'])
    xx=s.symbols('x0:10');V=s.zeros(4);i=0
    for a in range(4):
        for b in range(a,4):V[a,b]=V[b,a]=xx[i];i+=1
    eq=list(V*eta.inv()*H+H*eta.inv()*V)
    for g in ((1,0,0),(0,1,0)):
        N=R[g];assert N.T*eta*N==eta and N.T*H*N==H;eq+=list(N.T*V*N-V)
    assert s.linear_eq_to_matrix(eq,xx)[0].rank()==10

def test_e6_family_operator_covariance_and_central_character():
    d=D['flavour'];M=mat(d['M']);hu=mat(d['h_u']);hd=mat(d['h_d']);X=mat([[0,0,1],[1,0,0],[0,1,0]]);Z=s.diag(1,w,s.conjugate(w))
    tensor=np.zeros((3,3,3),int)
    for i in range(3):tensor[i,i,i]=1
    def Y(h,A):
        T=s.diag(*h);return (A.T*T+T*A)/2
    for W in (X,Z,w*s.eye(3)):
        for h in (hu,hd):assert m.zero(Y(W*h,W*M*W.inv())-W.inv().T*Y(h,M)*W.inv())
    assert m.zero(Y(hu,M)-mat(d['Y_u'])) and m.zero(Y(hd,M)-mat(d['Y_d']))
    # With no triplet h the central action on two matter3 fields is omega²,
    # so an adjoint M alone cannot replace the required family tensor.
    assert s.simplify(w**2-1)!=0 and s.simplify(w**3-1)==0
    assert 'diagonal Z3 quotient' in d['global_group']

def test_exact_flavour_spectra_cp_and_cp_conjugate():
    d=D['flavour'];Yu=mat(d['Y_u']);Yd=mat(d['Y_d']);A=Yu*Yu.conjugate().T;B=Yd*Yd.conjugate().T
    odd=s.simplify(s.im(s.trace((A*B-B*A)**3)))
    assert odd==13122*s.sqrt(3)
    Ac=A.conjugate();Bc=B.conjugate();assert s.simplify(s.im(s.trace((Ac*Bc-Bc*Ac)**3)))==-odd
    lam=s.Symbol('lambda',real=True)
    for H,key in ((A,'Hu_characteristic'),(B,'Hd_characteristic')):
        p=s.Poly(s.simplify((lam*s.eye(3)-H).det().expand(complex=True)),lam)
        assert s.expand(p.as_expr()-s.sympify(d[key].replace('lambda','L'),locals={'L':lam}))==0
        assert s.discriminant(p.as_expr(),lam)>0 and H.det()!=0

def test_flavon_potential_invariant_positive_hessian_and_global_root_count():
    rng=np.random.default_rng(12194);z=rng.normal(size=10)+1j*rng.normal(size=10);omega=np.exp(2j*np.pi/3)
    zx=z.copy();zx[2]*=omega**2;zx[3]*=omega;zx[4:7]=np.roll(zx[4:7],1);zx[7:]=np.roll(zx[7:],1)
    zz=z.copy();zz[0]*=omega;zz[1]*=omega**2;zz[4:7]*=omega**np.arange(3);zz[7:]*=omega**np.arange(3)
    cp=z.conj();cp[[2,3]]=cp[[3,2]]
    assert abs(m.flavon_potential(z)-m.flavon_potential(zx))<1e-8
    assert abs(m.flavon_potential(z)-m.flavon_potential(zz))<1e-8
    assert abs(m.flavon_potential(z)-m.flavon_potential(cp))<1e-8
    base=np.array([1,1,2,2,1,1,1,1,1,omega],complex);assert m.flavon_potential(base)<1e-24
    h=1e-4;basis=np.column_stack((np.eye(10),1j*np.eye(10))).T
    H=np.empty((20,20))
    for i in range(20):
        for j in range(20):
            a=h*basis[i];b=h*basis[j]
            H[i,j]=(m.flavon_potential(base+a+b)-m.flavon_potential(base+a-b)-m.flavon_potential(base-a+b)+m.flavon_potential(base-a-b))/(4*h*h)
    assert np.linalg.eigvalsh(H).min()>17.99
    # M pairs each have3 roots; hu has9 roots; hd has18 roots.
    assert 3*3*9*18==D['flavour']['isolated_flavon_minima']

def test_actual_three_copy_pauli_projection_and_affine_decoder():
    d=D['magic'];z=np.exp(2j*np.pi/9);psi=np.array([1,-1j*np.sqrt(3)*z**4/9,1j*np.sqrt(3)*z**8/9]);psi/=np.linalg.norm(psi)
    checks=np.array(d['Z_check_rows']);outcomes=np.array(d['Z_outcomes']);decoder=np.array(d['affine_Clifford_decoder']);amp=np.zeros(3,complex)
    for word in product(range(3),repeat=3):
        word=np.array(word)
        if np.array_equal(checks@word%3,outcomes):
            out=decoder@word%3;assert tuple(out[1:])==(2,1)
            amp[out[0]]+=np.prod(psi[word])
    assert abs(np.linalg.norm(amp)**2-81/24389)<1e-15
    target=np.exp(-1j*np.pi*np.arange(3)/9)/np.sqrt(3)
    assert abs(abs(np.vdot(target,amp/np.linalg.norm(amp)))-1)<1e-12

def test_six_copy_conversion_and_branch_cost():
    z=np.exp(2j*np.pi/9);psi=np.array([1,-1j*np.sqrt(3)*z**4/9,1j*np.sqrt(3)*z**8/9]);psi/=np.linalg.norm(psi)
    # Independent six-body contraction, not two calls to the three-body map.
    words=np.array(D['magic']['line_words']);out=np.array([np.prod(psi[np.tile(word,2)])for word in words])
    prob=float(np.vdot(out,out).real);out=np.diag([1,z**3,z**3])@out[[0,2,1]]
    assert abs(prob-2187/594823321)<1e-17
    assert abs(abs(np.vdot(z**np.arange(3)/np.sqrt(3),out/np.sqrt(prob)))-1)<1e-12
    expected=40*s.Rational(81,29)*18/s.Rational(81,29**3)*8*243
    assert expected==D['magic']['ideal_expected_physical_U9_uses_with_staged_retries_and_bare_eight_branch']

def test_clifford_twirl_and_all_injection_branches():
    z=np.exp(2j*np.pi/9);omega=z**3;X=np.roll(np.eye(3),1,axis=0);Z=np.diag(omega**np.arange(3));T=np.diag(z**np.arange(3));C=X@np.diag([1,1,omega**-1])
    close(C,z**-1*T@X@T.conj().T)
    paulis=[omega**c*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)for a,b,c in product(range(3),repeat=3)]
    for P in (X,Z):assert any(np.max(abs(C@P@C.conj().T-Q))<1e-12 for Q in paulis)
    for row in D['magic']['injection_corrections']:
        k=row['outcome'];raw=np.diag(z**((np.arange(3)+k)%3));cor=np.diag(omega**np.array(row['correction_omega_exponents']))
        close(cor@raw,z**k*T)
        for P in (X,Z):assert any(np.max(abs(cor@P@cor.conj().T-Q))<1e-12 for Q in paulis)

def test_eight_qutrit_code_error_enumerators_and_target_fixed_point():
    d=D['magic'];H=np.array(d['eight_code_h0']);one=np.ones(8,int);assert np.all(H@H.T%3==0) and np.all(H@one%3==0)
    hist=np.zeros((3,9),int)
    for e in product(range(3),repeat=8):
        if np.any(H@e%3):continue
        hist[sum(e)%3,np.count_nonzero(e)]+=1
    assert hist.tolist()==d['accepted_phase_error_weight_enumerators']
    assert hist[:,1].sum()==0 and hist[1:,2].sum()==8
    z=np.exp(2j*np.pi/9);amp=[]
    for t in range(3):
        total=0j
        for c in product(range(3),repeat=2):
            word=(t*one+np.array(c)@H)%3;total+=z**sum(word)/81/3
        amp.append(total)
    assert abs(np.linalg.norm(amp)**2-1/243)<1e-14
    close(np.array(amp)/np.linalg.norm(amp),z**(-np.arange(3))/np.sqrt(3))

def test_exact_noise_series_and_certified_known_code_basin():
    d=D['magic'];e=s.Symbol('epsilon',real=True);hist=d['accepted_phase_error_weight_enumerators']
    p=[sum(hist[t][j]*(1-e)**(8-j)*(e/2)**j for j in range(9))for t in range(3)];A=s.expand(sum(p));B=s.expand(p[1]+p[2])
    assert s.series(B/A,e,0,4).removeO()==2*e**2+10*e**3
    f=s.sympify(d['perfect_Clifford_phase_noise_threshold_sextic'],locals={'epsilon':e});lo,hi=map(s.Rational,d['threshold_isolating_interval'])
    assert s.expand(B-e*A+e*(3*e-2)*f/128)==0
    assert s.Poly(f,e).count_roots(lo,hi)==1 and s.Poly(f,e).count_roots(0,s.Rational(2,3))==1

def test_physical_fault_chain_first_order_conversion_then_quadratic_detection():
    d=D['magic'];slopes=[s.Rational(x)for x in d['twirled_conversion_phase_error_slopes_in_physical_p']]
    assert slopes==[s.Rational(16,3),s.Integer(8)]
    rows=[[s.Rational(x)for x in row]for row in d['conversion_single_bad_input_relative_twirl_weights']]
    assert [s.simplify(s.Rational(8,29)*sum(row[j]for row in rows))for j in (1,2)]==slopes
    # Accepted weight-two patterns have equal error exponents at antipodal
    # columns: four pairs for Z/Z and four for Z²/Z², none mixed.
    H=np.array(d['eight_code_h0']);a=b=c=0
    for i in range(8):
        for j in range(i+1,8):
            for x,y in product((1,2),repeat=2):
                if np.any((x*H[:,i]+y*H[:,j])%3) or (x+y)%3==0:continue
                if x==y==1:a+=1
                elif x==y==2:b+=1
                else:c+=1
    assert (a,b,c)==(4,4,0) and a*slopes[0]**2+b*slopes[1]**2==s.Rational(3328,9)

def test_all_encoded_weil_matrices_are_exact_unitaries():
    d=D['quantum_normalizer'];assert d['distinct_symplectic_operators']==1338
    for row in d['unitary_matrices']:
        phase=np.array(row['omega_exponents_minus1_means_zero']);den=3**row['denominator_sqrt3_power']
        for i,j in product(range(9),repeat=2):
            mask=(phase[:,i]>=0)&(phase[:,j]>=0);counts=np.bincount((phase[mask,j]-phase[mask,i])%3,minlength=3)
            if i==j:assert counts.tolist()==[den,0,0]
            else:assert counts[0]==counts[1]==counts[2]

def test_all_quantum_arrows_match_actual_integral_normalizer_and_polarities():
    d=D['quantum_normalizer'];P,S,groups=m.prior.native_normalizers();forms=[np.array(m.prior.native.alternating([1,1,c,1,1+c,b]),int)%3 for b in (0,2)for c in range(3)]
    bases=list(map(np.array,d['Darboux_bases']));J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]])%3
    for i,N in enumerate(groups[1]):
        N=np.array(N,int)
        for arrow in d['arrows'][i]:
            a=arrow['source'];b=arrow['target'];sign=2 if arrow['antiunitary']else 1;A=np.array(arrow['phase_space_map'])
            assert np.array_equal(N.T@forms[b]@N%3,sign*forms[a]%3)
            assert np.array_equal(bases[b]@A%3,N@bases[a]%3)
            assert np.array_equal(A.T@J@A%3,sign*J%3)
    assert d['covariance_is_exact_exponent_arithmetic'] and d['all_address_checks']==139968

def test_independent_quantum_weyl_covariance_and_schur_composition():
    d=D['quantum_normalizer'];lookup={tuple(row['key']):row for row in d['unitary_matrices']}
    def operator(key):
        row=lookup[tuple(key)];phase=np.array(row['omega_exponents_minus1_means_zero']);U=np.zeros((9,9),complex);mask=phase>=0
        U[mask]=3**(-row['denominator_sqrt3_power']/2)*np.exp(2j*np.pi*phase[mask]/3);return U
    # All addresses on an independent spread of positive/negative arrows.
    for i in (0,1,4,12,48,119,287):
        for arrow in d['arrows'][i]:
            U=operator(arrow['symplectic_key']);A=np.array(arrow['phase_space_map'])
            for v in product(range(3),repeat=4):
                P=m.weyl(v);left=U@(P.conj()if arrow['antiunitary']else P)@U.conj().T
                close(left,m.weyl(A@np.array(v)%3))
    assert d['projective_composition_cases']==6912 and d['max_projective_composition_error']<1e-11

def test_nonlinear_adm_refinement_and_kinetic_obstruction():
    d=D['gravity'];r16=m.bracket(16);r32=m.bracket(32)
    for old,new in zip(d['nonlinear_bracket_rows'][:2],(r16,r32)):
        assert abs(old['defect']-new['defect'])<1e-10
    assert .24<r32['defect']/r16['defect']<.27
    assert all(.24<x<.27 for x in d['successive_defect_ratios'])
    old=json.loads((ROOT/'data/w33_pass11999_native_adm_weights.json').read_text());J=mat(old['exact_selected_edge_ADM_jacobian'])
    assert J.det()!=0 and (J*J.T).det()==J.det()**2>0
    assert old['edge_velocity_Hessian_inertia']=={'positive':5,'negative_conformal':1,'lapse_shift_zero':4}
    a,k,l=s.symbols('a k l',real=True);symbol=(s.sin(a*(k+l))-s.sin(a*k)-s.sin(a*l))/a
    assert s.simplify(s.limit(symbol/a**2,a,0)+k*l*(k+l)/2)==0


def test_even_unimodularity_selects_only_the_two_split_signs():
    d=D['narain'];aa,bb=s.symbols('a b',real=True)
    F=s.Matrix([[2*aa,-aa,aa,0],[-aa,2*aa,0,aa],[aa,0,2*(aa+bb)/3,(aa+bb)/3],[0,aa,(aa+bb)/3,2*(aa+bb)/3]])
    assert s.factor(F.det())==aa**2*bb**2
    # F01=-a and F23=(a+b)/3 are necessary AND sufficient for
    # integral/even entries, so determinant1 reduces to four sign pairs.
    valid=[]
    for a,b in product((1,-1),repeat=2):
        Q=F.subs({aa:a,bb:b})
        if all(x.q==1 for x in Q)and all(Q[i,i]%2==0 for i in range(4)):valid.append([a,b])
    assert valid==d['even_unimodular_invariant_choices']==[[1,-1],[-1,1]]
    _,R=m.prior.native.native();parameters=s.symbols('s0:10');V=s.zeros(4);k=0
    for i in range(4):
        for j in range(i,4):V[i,j]=V[j,i]=parameters[k];k+=1
    eq=[]
    for g in ((1,0,0),(0,1,0)):eq+=list(R[g].T*V*R[g]-V)
    assert s.linear_eq_to_matrix(eq,parameters)[0].rank()==8


def test_actual_native_conductance_corrector_realizes_narain_metric():
    d=D['narain'];bridge=d['native_conductance_bridge'];old,Bf,Vf,Gf,aa,bb=m.prior.graph_inputs();B=s.Matrix(Bf.astype(int));V=s.Matrix(Vf.astype(int))
    C=mat(old['harmonic_voltages_Q']);f=mat(bridge['harmonic_corrector_from_old_C']);h=mat(bridge['harmonic_cochains']);weights=list(map(s.Rational,bridge['edge_weights']));W=s.diag(*weights)
    assert all(x>0 for x in weights) and sorted(set(weights))==[s.Rational(3,4),1,s.Rational(3,2)]
    assert h==C-B*f and B.T*W*h==s.zeros(27,4)
    # Stored old cochain is cohomologous to primitive voltages; the new one
    # consequently has the same periods. Verify with an independent solve.
    gauge=B[:,1:].gauss_jordan_solve(V-h)[0]
    assert B[:,1:]*gauge==V-h
    G=h.T*W*h/27;H=mat(d['positive_generalized_metric'])
    assert G==mat(bridge['exact_weighted_acoustic_G'])==H.inv()/4
    # Every face from the earlier carrier still closes: correction is exact.
    assert B.T*W*(V-B[:,1:]*gauge)==s.zeros(27,4)


def test_unweighted_acoustic_metric_needs_a_real_shape_change():
    old=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text());G=mat(old['exact_acoustic_metric']);P=s.Matrix([[-1,0,-1,1],[-1,1,-1,0],[0,0,1,-2],[0,0,1,1]])
    A=mat([[2,-1],[-1,2]]);eta=mat(D['narain']['eta_original'])
    assert P.T*G.inv()*P==s.diag(3*A,s.Rational(9,2)*A)
    Q=G.inv()*eta.inv()*G.inv();factor=Q[0,0]/eta[0,0]
    assert Q!=factor*eta
    rows=D['gravity']['nonlinear_bracket_rows']
    assert all(.24<abs(rows[i+1]['canonical_defect']/rows[i]['canonical_defect'])<.27 for i in range(4))
