"""Explicit five-frontier maps. EFT inputs are labelled; no TOE completion claimed."""
from pathlib import Path
from itertools import product
from functools import lru_cache
from collections import Counter
import json,sys,hashlib
import numpy as np
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parent))
import w33_pass12189_12193_five_bridges as prior
ROOT=Path(__file__).resolve().parents[1]
w=(-1+s.I*s.sqrt(3))/2

def ml(M):return [[str(s.simplify(x))for x in row]for row in M.tolist()]
def il(M):return [[int(x)for x in row]for row in M.tolist()]
def zero(M):return all(s.simplify(x)==0 for x in M)

def native_narain_weights(H):
    d,Bf,Vf,Gf,aa,bb=prior.graph_inputs();B=s.Matrix(Bf.astype(int));V=s.Matrix(Vf.astype(int))
    C=s.Matrix(d['harmonic_voltages_Q']);points=list(product(range(3),repeat=3));weights=[]
    for i,j in zip(aa,bb):
        g=points[i];h=points[j];inverse=((-g[0])%3,(-g[1])%3,(-g[2]-g[0]*g[1])%3)
        direction=prior.native.mul(inverse,h)
        if direction in ((0,0,1),(0,0,2)):weight=s.Integer(1)
        elif direction in ((0,1,1),(0,2,2)):weight=s.Rational(3,2)
        else:weight=s.Rational(3,4)
        weights.append(weight)
    assert Counter(weights)=={s.Integer(1):27,s.Rational(3,2):27,s.Rational(3,4):81}
    W=s.diag(*weights);L=B.T*W*B;source=B.T*W*C
    Q=s.Matrix.hstack(*source.columnspace());assert Q.cols in (2,4)
    potential=Q*(Q.T*L*Q).inv()*Q.T*source
    h=C-B*potential
    assert B.T*W*h==s.zeros(27,4)
    # Recheck cohomology against primitive integral voltages, independently
    # of the stored harmonic representative's label.
    b=B[:,1:];gauge=(b.T*b).inv()*b.T*(V-C)
    assert b*gauge==V-C
    G=h.T*W*h/27
    assert G==H.inv()/4
    original=s.Matrix(d['exact_acoustic_metric']);P=s.Matrix([[-1,0,-1,1],[-1,1,-1,0],[0,0,1,-2],[0,0,1,1]])
    A=s.Matrix([[2,-1],[-1,2]])
    assert P.T*original.inv()*P==s.diag(3*A,s.Rational(9,2)*A)
    return {'edge_weights':[str(x)for x in weights],'weights_by_generator':'central(0,0,1):1; (0,1,1):3/2; (1,0,1),(1,1,0),(1,2,2):3/4, and inverses',
      'harmonic_corrector_from_old_C':ml(potential),'harmonic_cochains':ml(h),'exact_weighted_acoustic_G':ml(G),
      'relation':'G_weighted=H_Narain^-1/4 exactly',
      'unweighted_inverse_plane_coefficients':['3','9/2'],
      'uniform_weight_obstruction':'The unweighted inverse acoustic metric has unequal Eisenstein-plane coefficients3 and9/2; no common rescaling makes it a generalized metric for eta.',
      'scope':'A supplied positive rational conductance choice on the existing native graph, not a new graph, a dynamically selected action or a Newton/alpha-prime normalization.'}

@lru_cache(None)
def narain():
    P,S,groups=prior.native_normalizers(); A=s.Matrix([[2,-1],[-1,2]])
    eta=P.inv().T*s.diag(A,-A)*P.inv()
    H=P.inv().T*s.diag(A,A)*P.inv()
    E=s.eye(4);C=s.Matrix.hstack(E[:,2],E[:,3],E[:,0]-E[:,2],E[:,1]+E[:,2]-E[:,3])
    standard=s.zeros(4);standard[:2,2:]=s.eye(2);standard[2:,:2]=s.eye(2)
    assert C.det() in (-1,1) and C.T*eta*C==standard
    assert eta.det()==1 and all(x.q==1 for x in eta) and all(eta[i,i]%2==0 for i in range(4))
    assert H*eta.inv()*H==eta and all(H[:i,:i].det()>0 for i in range(1,5))
    HC=C.T*H*C;G=HC[:2,:2].inv();B=-G*HC[:2,2:]
    assert B.T==-B
    rebuilt=s.BlockMatrix([[G.inv(),-G.inv()*B],[B*G.inv(),G-B*G.inv()*B]]).as_explicit()
    assert rebuilt==HC
    T=s.simplify(B[0,1]+s.I*s.sqrt(G.det()));U=s.simplify((G[0,1]+s.I*s.sqrt(G.det()))/G[0,0])
    _,R=prior.native.native()
    assert all(M.T*eta*M==eta and M.T*H*M==H for M in R.values())
    signs=Counter()
    for M in groups[0]:
        assert M.T*H*M==H
        sign=1 if M.T*eta*M==eta else -1
        assert M.T*eta*M==sign*eta;signs[sign]+=1
    assert all(2*H.inv()[i,i]<=9 for i in range(4))  # complete coordinate root bound
    roots=[]
    for sig in (1,-1):
        sector=[]
        for v in product(range(-3,4),repeat=4):
            x=s.Matrix(v)
            if (x.T*H*x)[0]==2 and (x.T*eta*x)[0]==2*sig:sector.append(list(v))
        assert len(sector)==6;roots.append(sector)
    # Explicit SL(2,Z) x SL(2,Z) determinant action on M(y).
    # eta norm=2(y0*y2+y1*y3)=2 det [[y0,y1],[-y3,y2]].
    def toM(y):return s.Matrix([[y[0],y[1]],[-y[3],y[2]]])
    def fromM(Q):return s.Matrix([Q[0,0],Q[0,1],Q[1,1],-Q[1,0]])
    def spin(L,V):return s.Matrix.hstack(*[fromM(L*toM(E[:,j])*V.inv())for j in range(4)])
    L=s.Matrix([[1,1],[0,1]]);D=spin(L,s.eye(2));nativeD=C*D*C.inv()
    assert nativeD.T*eta*nativeD==eta and all(x.q==1 for x in nativeD)
    assert nativeD!=s.eye(4) and (nativeD-s.eye(4))**2==s.zeros(4) and nativeD.T*H*nativeD!=H
    # Conditional uniqueness: among native-invariant EVEN UNIMODULAR
    # integral symmetric forms, the two signs of eta are the only options.
    aa,bb=s.symbols('a b',real=True)
    family=P.inv().T*s.diag(aa*A,bb*A)*P.inv()
    expected=s.Matrix([[2*aa,-aa,aa,0],[-aa,2*aa,0,aa],[aa,0,2*(aa+bb)/3,(aa+bb)/3],[0,aa,(aa+bb)/3,2*(aa+bb)/3]])
    assert family==expected and s.factor(family.det())==aa**2*bb**2
    # Integer(0,1) entry implies a integral; integer(2,3) implies
    # a+b divisible by3, hence b integral. Unimodular -> a,b in{+1,-1}.
    choices=[(a,b)for a,b in product((1,-1),repeat=2)if (a+b)%3==0]
    assert choices==[(1,-1),(-1,1)]
    # Full-C3^2 invariant infinitesimal Narain deformations.
    params=s.symbols('h0:10');dH=s.zeros(4);k=0
    for i in range(4):
        for j in range(i,4):dH[i,j]=dH[j,i]=params[k];k+=1
    eq=list(dH*eta.inv()*H+H*eta.inv()*dH)
    for M in prior.set_matrices(R.values()):eq+=list(M.T*dH*M-dH)
    mat=s.linear_eq_to_matrix(eq,params)[0]
    assert len(mat.nullspace())==0
    return {'pass':12198,'native_conductance_bridge':native_narain_weights(H),'eta_original':il(eta),'positive_generalized_metric':ml(H),
      'momentum_winding_basis':il(C),'eta_standard':il(standard),'torus_G':ml(G),'torus_B':ml(B),
      'T':str(T),'U':str(U),'invariant_symmetric_form_family':ml(family),'invariant_family_determinant':'a^2*b^2',
      'even_unimodular_invariant_choices':[list(x)for x in choices],
      'conditional_uniqueness':'Native symmetry fixes a two-parameter symmetric-form space. Integrality is a,b in Z with a+b=0 mod3; det=a^2 b^2. Requiring even unimodular leaves only plus/minus eta, both signature(2,2). Unimodularity is an added mathematical admissibility condition, not a derived physical law.','left_roots':roots[0],'right_roots':roots[1],
      'finite_normalizer_sign_counts':{str(k):v for k,v in signs.items()},
      'infinite_duality_generator':il(nativeD),'fixed_generalized_metric_tangent_dimension':0,
      'scope':'Explicit II(2,2) Narain-lattice interpretation of the native period module. A compact two-boson CFT interpretation is conditional, not four-dimensional Lorentzian spacetime, a string vacuum, a mass hierarchy or an action-scale prediction.'}


def flavon_potential(z):
    z=np.array(z,dtype=complex);r=np.array([1,1,2,2,1,1,1,1,1,1],float)
    value=float(np.sum(abs(z**3-r**3)**2))
    value+=abs(z[0]*z[1]-1)**2+abs(z[2]*z[3]-4)**2
    value+=abs(np.prod(z[4:7])-1)**2
    product_d=np.prod(z[7:10]);value+=abs(product_d**2+product_d+1)**2
    return float(value)

@lru_cache(None)
def flavour():
    X=s.Matrix([[0,0,1],[1,0,0],[0,1,0]]);Z=s.diag(1,w,s.conjugate(w))
    M=X+X.T+2*Z+2*Z.conjugate();M=M.applyfunc(s.simplify)
    hu=s.Matrix([1,1,1]);hd=s.Matrix([1,1,w])
    def y(h,M):
        D=s.diag(*h);return ((M.T*D+D*M)/2).applyfunc(s.simplify)
    Yu=y(hu,M);Yd=y(hd,M);Hu=Yu*Yu.conjugate().T;Hd=Yd*Yd.conjugate().T
    lam=s.Symbol('lambda',real=True)
    cp=s.simplify(s.im(s.trace((Hu*Hd-Hd*Hu)**3)))
    polys=[s.Poly(s.simplify((lam*s.eye(3)-H).det().expand(complex=True)),lam)for H in (Hu,Hd)]
    assert cp==13122*s.sqrt(3) and all(s.discriminant(p.as_expr(),lam)>0 for p in polys)
    assert Yu.det()!=0 and s.simplify(Yd.det())!=0
    # E6 d_ABC is independent of the family tensor. Check family covariance
    # of T_iii=1 and of its flavon-dressed symmetric matrix for generators.
    for W in (X,Z):
        for h in (hu,hd):
            assert zero(y(W*h,W*M*W.inv())-W.inv().T*y(h,M)*W.inv())
    # Supplied, positive, real-coefficient H27 invariant flavon potential:
    # each complex field has a cubic root pin; all cross terms vanish here.
    # Full real Hessian is at least diag(18 |v_i|^4)>0.
    values=[1,1,2,2,1,1,1,1,1,w]
    assert flavon_potential([complex(s.N(v))for v in values])<1e-24
    lower=[s.simplify(18*abs(v)**4)for v in values for _ in (0,1)]
    # Every zero of the sum of squares is counted exactly by phase exponents.
    branches=[]
    for a,b,u0,u1,d0,d1,d2 in product(range(3),repeat=7):
        ue=[u0,u1,(-u0-u1)%3];de=[d0,d1,d2]
        if sum(de)%3==0:continue
        branches.append(([a,(-a)%3,b,(-b)%3],ue,de))
    assert len(branches)==1458
    return {'pass':12194,'M':il(M),'h_u':['1','1','1'],'h_d':['1','1',str(w)],
      'Y_u':ml(Yu),'Y_d':ml(Yd),'Hu_characteristic':str(polys[0].as_expr()),
      'Hd_characteristic':str(polys[1].as_expr()),'CP_odd_invariant':str(cp),
      'det_Yu':str(Yu.det()),'det_Yd':str(s.simplify(Yd.det())),
      'flavon_real_hessian_lower_bound_diagonal':[str(x)for x in lower],
      'isolated_flavon_minima':1458,
      'operator':'d_ABC H_E^C T_ijk (M Psi^A)_i Psi_j^B h_k / Lambda^2, symmetrized in the two matter fields',
      'extra_fields':'Four independent chiral E6-singlet adjoint-character coefficients a+,a-,b+,b-; two E6-singlet H27 triplets h_u,h_d; two family-neutral E6 Higgs-27 channels. Hermitian M is a VEV branch, not an antiholomorphic superpotential.',
      'global_group':'E6 x H27 direct product EFT. Added family-neutral Higgs27 and E6-singlet family3 do not automatically descend through the diagonal Z3 quotient of an E8 parent; this UV/global-group issue is not solved.',
      'scope':'Constructed nonrenormalizable E6/H27 invariant family EFT and isolated flavon-sector minimum. Gauge/Higgs breaking and light-doublet selection, anomaly/UV completion, observed spectra and coupling values are not derived. The potential is a supplied non-supersymmetric EFT, not the full E6 vacuum.'}

@lru_cache(None)
def magic():
    z=np.exp(2j*np.pi/9);k=np.array([1,-1j*np.sqrt(3)*z**4/9,1j*np.sqrt(3)*z**8/9]);psi=k/np.linalg.norm(k)
    u=np.array([0,1,1]);v=np.array([1,1,2]);words=np.array([(u+t*v)%3 for t in range(3)])
    # These are two commuting Z checks. Rows span v-perp, outcome is row.u.
    checks=np.array([[1,2,0],[1,0,1]]);assert np.all(checks@v%3==0)
    amp=np.array([np.prod(psi[word])for word in words]);p3=float(np.vdot(amp,amp).real)
    phase18=np.exp(-1j*np.pi/9*np.arange(3))/np.sqrt(3)
    assert abs(abs(np.vdot(amp/np.linalg.norm(amp),phase18))-1)<1e-12
    assert abs(p3-81/29**3)<1e-14
    pair=phase18**2;ppair=float(np.vdot(pair,pair).real);mminus=pair/np.linalg.norm(pair)
    parity=np.eye(3)[[0,2,1]];Q=np.diag([1,z**3,z**3]);mplus=Q@parity@mminus
    target=z**np.arange(3)/np.sqrt(3)
    assert np.allclose(mplus,target,atol=1e-12) and abs(ppair-1/3)<1e-14
    # Punctured RM(1,2) code, standard [[8,1,2]]_3, not a new code.
    columns=np.array([x for x in product(range(3),repeat=2)if x!=(0,0)],int)
    h0=columns.T;h1=np.ones(8,dtype=int)
    cosets=np.array([(r*h1+c@h0)%3 for r in range(3)for c in np.array(list(product(range(3),repeat=2))) ]).reshape(3,9,8)
    ideal=np.array([sum(np.prod(target[word])for word in sector)/3 for sector in cosets])
    p8=float(np.vdot(ideal,ideal).real)
    assert np.allclose(ideal/np.linalg.norm(ideal),mminus,atol=1e-12)
    assert abs(p8-1/243)<1e-14
    # Enumerate all independent phase-error patterns, exact accepted weights.
    hist=np.zeros((3,9),dtype=int);rejected=0;single=[]
    for e in product(range(3),repeat=8):
        e=np.array(e,int);wt=int(np.count_nonzero(e))
        if np.any(h0@e%3):rejected+=1;continue
        logical=int(sum(e)%3);hist[logical,wt]+=1
    assert hist[:,1].sum()==0 and hist[:,0].tolist()==[1,0,0]
    for j in range(8):
        for power in (1,2):
            e=np.zeros(8,int);e[j]=power
            amp8=np.array([sum(np.prod(target[word])*z**(3*int(word@e))for word in sector)/3 for sector in cosets])
            single.append(float(np.linalg.norm(amp8)))
    assert max(single)<1e-13
    eps=s.Symbol('epsilon',real=True)
    weights=[sum(int(hist[t,j])*(1-eps)**(8-j)*(eps/2)**j for j in range(9))for t in range(3)]
    accepted=s.expand(sum(weights));bad=s.expand(weights[1]+weights[2]);error=s.series(bad/accepted,eps,0,4).removeO()
    fixedpoint=s.factor(bad-eps*accepted)
    sextic=81*eps**6+54*eps**5-972*eps**4+1848*eps**3-1488*eps**2+544*eps-64
    assert s.expand(fixedpoint+eps*(3*eps-2)*sextic/128)==0
    interval=(s.Rational(21100119,10**8),s.Rational(21100120,10**8))
    assert s.Poly(sextic,eps).count_roots(*interval)==1 and s.Poly(sextic,eps).count_roots(0,s.Rational(2,3))==1
    samples=[]
    for e in (.001,.01,.05,.1,.2):
        probs=np.array([sum(hist[t,j]*(1-e)**(8-j)*(e/2)**j for j in range(9))for t in range(3)])
        samples.append({'input_total_phase_error':e,'accepted_relative_to_ideal':float(sum(probs)),
                        'output_total_phase_error':float(sum(probs[1:])/sum(probs))})
    # Verify the previous physical-fault certificate, rather than assuming
    # its branch phase from the fidelity alone.
    frozen=json.loads((ROOT/'data/w33_pass12189_12193_five_bridges.json').read_text())['magic']
    zz=s.Symbol('z');phi9=zz**6+zz**3+1
    ideal_exact=[prior.phase_sum(c)for c in frozen['phase_counts_mod9']]
    for site in range(4):
        fault_exact=[prior.phase_sum(c)for c in frozen['single_Z_after_gate_controls'][site]['phase_counts']]
        assert fault_exact[0]==0
        for j in (1,2):assert s.rem(fault_exact[j]-zz**(3*j)*ideal_exact[j],phi9,zz)==0
    # Clifford twirl: C is T9 X T9^dagger up to a scalar. Its three
    # eigenspaces are exactly the orthonormal M_j=Z^j M9 basis.
    X=np.roll(np.eye(3),1,axis=0);Ct=X@np.diag([1,1,z**(-3)])
    basis=np.column_stack([z**(3*j*np.arange(3))*target for j in range(3)])
    assert np.allclose(basis.conj().T@basis,np.eye(3),atol=1e-12)
    for j in range(3):assert np.allclose(Ct@basis[:,j],z**(-1-3*j)*basis[:,j],atol=1e-12)
    # Named affine Clifford decoder: coordinates (x0, x0+2x1, x0+x2).
    decoder=np.array([[1,0,0],[1,2,0],[1,0,1]])
    assert round(np.linalg.det(decoder))%3 and np.array_equal(words@decoder.T%3,np.array([[0,2,1],[1,2,1],[2,2,1]]))
    # All three T9 injection branches have Clifford corrections.
    injection=[]
    for outcome in range(3):
        raw=(np.arange(3)+outcome)%3
        correction=(np.arange(3)-raw+outcome)%9
        assert np.all(correction%3==0)
        assert np.all((raw+correction-np.arange(3)-outcome)%9==0)
        injection.append({'outcome':outcome,'correction_omega_exponents':(correction//3).tolist()})
    # Round9 identifies the four accepted physical-Z faults: their exact
    # branch is (0,omega*b,omega^2*c). Each conditional factory input has
    # bad-state probability (8/29)p+O(p^2). Propagate six positions.
    a,b,c=s.symbols('a b c',nonzero=True);om=s.Symbol('om')
    ideal=[a,b,c];fault=[0,om*b,om**2*c]
    # After conditioning on the herald, phi/psi normalization is sqrt(29/2).
    # Ratios before final Clifford; input words have zero in each position.
    relative=[]
    for pos in range(6):
        ratio=[]
        for word in words:
            j=int(word[pos%3]);ratio.append(0 if j==0 else w**j)
        ratio=s.sqrt(s.Rational(29,2))*s.Matrix(ratio)
        # Equality and QP are diagonal/permutation; final parity swaps1,2.
        ratio=s.Matrix([ratio[0],ratio[2],ratio[1]])
        masses=[s.simplify(abs(sum(w**(-j*t0)*ratio[t0]for t0 in range(3))/3)**2)for j in range(3)]
        assert sorted(masses)==[s.Rational(29,18),s.Rational(29,18),s.Rational(58,9)]
        relative.append(masses)
    slopes=[s.simplify(s.Rational(8,29)*sum(r[j]for r in relative))for j in range(3)]
    assert slopes==[s.Rational(8,3),s.Rational(16,3),s.Integer(8)]
    # Independently verify every weight-two Z pattern with its logical class.
    leading=[0,0]
    for e in product(range(3),repeat=8):
        e=np.array(e,int)
        if np.count_nonzero(e)!=2 or np.any(h0@e%3) or sum(e)%3==0:continue
        if np.count_nonzero(e==1)==2:leading[0]+=1
        elif np.count_nonzero(e==2)==2:leading[1]+=1
        else:raise AssertionError('unexpected mixed weight-two phase error')
    assert leading==[4,4]
    final_coefficient=s.simplify(4*(slopes[1]**2+slopes[2]**2))
    assert final_coefficient==s.Rational(3328,9)
    return {'pass':12196,'affine_Clifford_decoder':decoder.tolist(),'line_words':words.tolist(),'Z_check_rows':checks.tolist(),'Z_outcomes':(checks@u%3).tolist(),
      'three_copy_success':'81/24389','first_output':'(1,exp(-i*pi/9),exp(-2i*pi/9))/sqrt(3)',
      'two_copy_equality_success':'1/3','converted_resource':'M9+=(1,zeta9,zeta9^2)/sqrt(3)',
      'phase_minus_to_plus_Clifford':'diag(1,omega,omega) followed on input by |j> -> |-j>',
      'six_input_fixed_tree_success':'2187/594823321',
      'eight_code_h0':h0.tolist(),'code_cosets':cosets.tolist(),'bare_eight_projection_success':'1/243',
      'accepted_phase_error_weight_enumerators':hist.tolist(),'rejected_phase_patterns':rejected,
      'single_Z_errors_checked':16,'single_Z_amplitude_max':max(single),
      'perfect_Clifford_phase_noise_threshold_sextic':str(sextic),'threshold_isolating_interval':[str(x)for x in interval],
      'accepted_relative_probability_polynomial':str(accepted),'output_error_series':str(error),'noise_samples':samples,
      'magic_basis_Clifford_twirl':'Random powers of C=X diag(1,1,omega^-1); C is T9 X T9^dagger up to the scalar zeta9^-1.',
      'injection_corrections':injection,'conversion_single_bad_input_relative_twirl_weights':[[str(x)for x in row]for row in relative],
      'twirled_conversion_phase_error_slopes_in_physical_p':['16/3','8'],
      'after_eight_code_physical_fault_error':'(3328/9)*p^2+O(p^3)',
      'noise_chain_assumptions':'Independent physical Z-after-U9 faults with probability p at every site; independent factories; exact accepted branch data from12189/round9; perfect Clifford checks, decoding and M9-basis Clifford twirl. No other faults. Multiple faults affect O(p^3) and higher here after eight-code filtering.',
      'ideal_expected_physical_U9_uses_with_staged_retries_and_bare_eight_branch':1177130880,
      'injection':'Measure data/resource Z parity and decode. Each branch implements a cyclic permutation of T9 phases with probability1/3; differences from T9 are diagonal Clifford phases. Standard T9 injection uses feed-forward.',
      'scope':'Exact ideal Clifford/postselection conversion plus a published distance-two phase-error-detecting distiller. Ideal stabilizer operations and independent input phase errors are assumed for the noise curve. No end-to-end physical fault-tolerance threshold or magic creation from Clifford inputs.'}

# Modular symplectic compiler used by the full normalizer below.
def invmod(A,p=3):
    return np.array(s.Matrix(A.tolist()).inv_mod(p),dtype=int)%p

def darboux(F):
    # deterministic symplectic Gram-Schmidt, ordered (q0,p0,q1,p1)
    vectors=[np.array(v,int)for v in product(range(3),repeat=4)if any(v)]
    basis=[]
    for a in vectors:
        if any(int(x@F@a)%3 for x in basis):continue
        for b in vectors:
            if any(int(x@F@b)%3 for x in basis):continue
            if int(a@F@b)%3==1:
                basis.extend([a,b]);break
        if len(basis)==4:break
    B=np.column_stack(basis);assert round(np.linalg.det(B))%3!=0
    return B

def weyl(v):
    omega=np.exp(2j*np.pi/3);out=np.array([[1]],complex)
    X=np.roll(np.eye(3),1,axis=0);Z=np.diag(omega**np.arange(3))
    for q,p in np.array(v,int).reshape(-1,2):
        out=np.kron(out,omega**(int(q*p)%3)*np.linalg.matrix_power(X,int(q))@np.linalg.matrix_power(Z,int(-p)%3))
    return out

@lru_cache(None)
def weil_tuple(key):
    S=np.array(key,int).reshape(4,4)%3;eye=np.eye(4,dtype=int)
    xs=[weyl(S@eye[:,2*j]%3)for j in range(2)]
    zs=[weyl(S@eye[:,2*j+1]%3)for j in range(2)]
    P=np.eye(9,dtype=complex)
    for Z in zs:P=P@(np.eye(9)+Z+Z@Z)/3
    col=next(j for j in range(9)if np.linalg.norm(P[:,j])>1e-8);base=P[:,col]/np.linalg.norm(P[:,col])
    cols=[]
    for a,b in product(range(3),repeat=2):cols.append(np.linalg.matrix_power(xs[0],a)@np.linalg.matrix_power(xs[1],b)@base)
    U=np.column_stack(cols)
    assert np.allclose(U.conj().T@U,np.eye(9),atol=1e-11)
    return U


def encode_weil(U):
    magnitude=abs(U[np.abs(U)>1e-8][0]);rank=int(round(-2*np.log(magnitude)/np.log(3)))
    phase=np.full((9,9),-1,dtype=int)
    for i,j in product(range(9),repeat=2):
        if abs(U[i,j])>1e-8:
            exponent=int(round(np.angle(U[i,j])*3/(2*np.pi)))%3
            assert abs(U[i,j]-3**(-rank/2)*np.exp(2j*np.pi*exponent/3))<1e-11
            phase[i,j]=exponent
    for i,j in product(range(9),repeat=2):
        mask=(phase[:,i]>=0)&(phase[:,j]>=0);counts=np.bincount((phase[mask,j]-phase[mask,i])%3,minlength=3)
        if i==j:assert counts.tolist()==[3**rank,0,0]
        else:assert counts[0]==counts[1]==counts[2]
    return rank,phase

def exact_weyl_covariance(phases,A,v,anti):
    labels=np.array(list(product(range(3),repeat=2)),int)
    def monomial(v):
        q=np.array(v)[::2];p=np.array(v)[1::2]
        perm=np.array([3*x[0]+x[1]for x in (labels+q)%3])
        exp=(q@p-labels@p)%3
        return perm,exp
    perm,exp=monomial(v);perm2,exp2=monomial(A@np.array(v)%3)
    lhs=phases[:,perm].copy();mask=lhs>=0
    shift=np.tile((-exp if anti else exp),(9,1))
    lhs[mask]=(lhs[mask]+shift[mask])%3
    rhs=np.full((9,9),-1,int);source=phases.copy();mask=source>=0
    shift=np.repeat(exp2[:,None],9,axis=1);source[mask]=(source[mask]+shift[mask])%3
    rhs[perm2,:]=source
    assert np.array_equal(lhs,rhs)

@lru_cache(None)
def quantum_normalizer():
    P,S,groups=prior.native_normalizers();mats=[np.array(M,dtype=int)for M in groups[1]]
    addresses=list(product(range(3),repeat=4));weyls={v:weyl(v)for v in addresses}
    forms=[np.array(prior.native.alternating([1,1,c,1,1+c,b]),dtype=int)%3 for b in (0,2)for c in range(3)]
    bases=[darboux(F)for F in forms];bi=[invmod(B)for B in bases]
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]])%3
    assert all(np.array_equal(B.T@F@B%3,J)for B,F in zip(bases,forms))
    C=np.diag([1,2,1,2]);arrows=[];cache={};codes={};worst=0.
    idx={tuple(np.array(M,dtype=int).ravel()):i for i,M in enumerate(groups[1])}
    for ni,N in enumerate(mats):
        rows=[]
        for target,F in enumerate(forms):
            raw=N.T@F@N%3
            source,sign=next((j,sg)for j,E in enumerate(forms)for sg in (1,2)if np.array_equal(raw,sg*E%3))
            A=bi[target]@N@bases[source]%3
            assert np.array_equal(A.T@J@A%3,sign*J%3)
            linear=A if sign==1 else A@C%3
            key=tuple(linear.ravel());U=weil_tuple(key);cache[key]=U
            if key not in codes:codes[key]=encode_weil(U)
            # Check ALL 81 Weyl addresses on this arrow, including antiunitary K.
            residual=0.
            for v in addresses:
                exact_weyl_covariance(codes[key][1],A,v,sign==2)
                D=weyls[v];lhs=U@(D if sign==1 else D.conj())@U.conj().T
                residual=max(residual,float(np.max(abs(lhs-weyls[tuple(A@np.array(v)%3)]))))
            worst=max(worst,residual);assert residual<1e-10
            rows.append({'source':source,'target':target,'antiunitary':sign==2,'phase_space_map':A.tolist(),'symplectic_key':list(key)})
        arrows.append(rows)
    # Composition as a groupoid: N acts from source to target; N*M takes
    # M:source->middle then N:middle->target. Projective phase is allowed.
    generators=[];closure={idx[tuple(np.eye(4,dtype=int).ravel())]}
    for g in range(288):
        if g in closure:continue
        generators.append(g);todo=list(closure)
        while todo:
            a=todo.pop()
            for b in generators:
                c=idx[tuple((mats[a]@mats[b]).ravel())]
                if c not in closure:closure.add(c);todo.append(c)
        if len(closure)==288:break
    worst_comp=0.;cases=0
    for g in generators:
        for h in range(288):
            gh=idx[tuple((mats[g]@mats[h]).ravel())]
            for t in range(6):
                a=arrows[g][t];b=arrows[h][a['source']];c=arrows[gh][t]
                assert b['source']==c['source'] and (a['antiunitary']!=b['antiunitary'])==c['antiunitary']
                Ua=weil_tuple(tuple(a['symplectic_key']));Ub=weil_tuple(tuple(b['symplectic_key']));Uc=weil_tuple(tuple(c['symplectic_key']))
                comp=Ua@(Ub.conj()if a['antiunitary']else Ub)
                phase=np.trace(Uc.conj().T@comp)/9
                err=float(np.max(abs(comp-phase*Uc)));worst_comp=max(worst_comp,err);assert err<1e-10
                cases+=1
    return {'pass':12197,'normalizer_order':288,'polarity_objects':6,'arrows':arrows,'Darboux_bases':[B.tolist()for B in bases],
      'distinct_symplectic_operators':len(cache),'unitary_matrices':[{'key':list(k),'denominator_sqrt3_power':codes[k][0],'omega_exponents_minus1_means_zero':codes[k][1].tolist()}for k in cache],
      'max_Weyl_covariance_error':worst,'all_address_checks':288*6*81,'covariance_is_exact_exponent_arithmetic':True,'generator_indices':generators,
      'projective_composition_cases':cases,'max_projective_composition_error':worst_comp,
      'scope':'Explicit unitary/antiunitary intertwiners between six two-qutrit quantizations of repaired mod-three period phase spaces. Projective composition, not a chosen globally phase-linearized representation, a single original-discriminant qutrit, or physical time reversal.'}

def bracket(n):
    a=2*np.pi/n;x=np.arange(n)*a
    D=(np.roll(np.eye(n),1,axis=1)-np.roll(np.eye(n),-1,axis=1))/(2*a)
    # D f = f_(i+1)-f_(i-1)
    assert np.allclose(D@np.sin(x),np.sin(a)/a*np.cos(x))
    q=np.array([1+.1*np.cos(x),1+.15*np.sin(2*x),1+.07*np.cos(3*x)])
    p=np.array([.2+.05*np.sin(x),-.1+.03*np.cos(2*x),.15+.04*np.sin(3*x)])
    N=1+.2*np.cos(2*x);M=np.sin(x)+.1*np.cos(3*x)
    def ham(q,p,lapse):
        A,B,C=q;A1,B1,C1=q@D.T;A2,B2,C2=q@(D@D).T
        root=np.sqrt(A*B*C);t=q*p
        R=-B2/(A*B)-C2/(A*C)+A1*B1/(2*A*A*B)+A1*C1/(2*A*A*C)+B1**2/(2*A*B*B)+C1**2/(2*A*C*C)-B1*C1/(2*A*B*C)
        K=(np.sum(t*t,axis=0)-.5*np.sum(t,axis=0)**2)/root
        return a*np.sum(lapse*(K-root*R))
    def grad(q,p,lapse):
        gq=np.zeros_like(q);gp=2*a*lapse*q*(q*p-.5*np.sum(q*p,axis=0))/np.sqrt(np.prod(q,axis=0))
        for i in range(3):
            for j in range(n):
                z=q.astype(complex);z[i,j]+=1j*1e-25;gq[i,j]=ham(z,p,lapse).imag/1e-25
        return gq,gp
    qn,pn=grad(q,p,N);qm,pm=grad(q,p,M)
    PB=np.sum(qn*pm-pn*qm)/a
    beta=(N*(D@M)-M*(D@N))/q[0]
    dh=-2*q[0]*(D@p[0])-p[0]*(D@q[0])+p[1]*(D@q[1])+p[2]*(D@q[2])
    rhs=a*beta@dh
    canonical_density=-2*(D@(q[0]*p[0]))+p[0]*(D@q[0])+p[1]*(D@q[1])+p[2]*(D@q[2])
    canonical_rhs=a*beta@canonical_density
    lie_variation=np.array([beta*(D@q[0])+2*q[0]*(D@beta),beta*(D@q[1]),beta*(D@q[2])])
    assert abs(canonical_rhs-a*np.sum(p*lie_variation))<1e-12
    return {'sites':n,'spacing':a,'Hamiltonian_Poisson_bracket':float(PB),'diffeomorphism_rhs':float(rhs),'defect':float(PB-rhs),'canonical_diffeomorphism_rhs':float(canonical_rhs),'canonical_defect':float(PB-canonical_rhs)}


@lru_cache(None)
def gravity():
    rows=[bracket(n)for n in (16,32,64,128,256)]
    ratios=[abs(rows[i+1]['defect']/rows[i]['defect'])for i in range(4)]
    assert all(.24<r<.27 for r in ratios)
    assert all(.24<abs(rows[i+1]['canonical_defect']/rows[i]['canonical_defect'])<.27 for i in range(4))
    # The exact native chart is owned by11999. A positive momentum form
    # remains positive under its nonsingular canonical transformation.
    path=ROOT/'data/w33_pass11999_native_adm_weights.json'
    old=json.loads(path.read_text());J=s.Matrix(old['exact_selected_edge_ADM_jacobian'])
    assert J.det()!=0
    positive=J*J.T
    assert all(positive[:i,:i].det()>0 for i in range(1,11))
    inertia=old['edge_velocity_Hessian_inertia']
    assert inertia=={'positive':5,'negative_conformal':1,'lapse_shift_zero':4}
    # Exact mixed-Fourier Leibniz obstruction of the supplied local loop
    # derivative. The leading term cannot be identically zero for all fields.
    a,k,l=s.symbols('a k l',real=True)
    defect=(s.sin(a*(k+l))-s.sin(a*k)-s.sin(a*l))/a
    coefficient=s.simplify(s.limit(defect/a**2,a,0))
    assert s.expand(coefficient+k*l*(k+l)/2)==0
    return {'pass':12195,'benchmark':'Nonlinear diagonal two-Killing spatial ADM fields, three canonical metric/momentum pairs; smooth periodic profiles at finite amplitude.',
      'native_interface':'The central difference is compiled by the prior12000 primitive native period loops. The actual11999 invertible edge-to-ADM Jacobian supplies local weight coordinates. Neither derivative ordering nor ADM Hamiltonian is selected by native combinatorics.',
      'native_chart_determinant':str(J.det()),'naive_positive_edge_kinetic_conclusion':'J J^T is strictly positive. No real invertible field redefinition, nor positive Schur elimination, yields the DeWitt negative conformal channel or four lapse/shift null directions. This excludes this naive kinetic ansatz only.',
      'supplied_ADM_inertia':inertia,'nonlinear_bracket_rows':rows,'successive_defect_ratios':ratios,
      'central_loop_Leibniz_leading_coefficient':str(coefficient),
      'scope':'A nonlinear finite-field constraint restoration benchmark with observed second-order convergence, not an exact finite-lattice first-class algebra, uniform convergence theorem, or derived microscopic Einstein action. Previous11976 pointwise obstruction and11999 conditional continuum pullback remain valid.'}

if __name__=='__main__':
    result={}
    for name in ('narain','flavour','magic','quantum_normalizer','gravity'):
        print(name,flush=True);result[name]=globals()[name]()
    result['provenance']={'digest_convention':'SHA256 with CRLF normalized to LF, matching committed text across Windows and Linux','source_sha256':hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        'prior_sources':{name:hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()for name in (
            'analysis/w33_pass12189_12193_five_bridges.py',
            'analysis/w33_pass12188_native_period_symplectic_repair.py',
            'data/w33_pass11999_native_adm_weights.json',
            'data/w33_pass11991_native_four_period_cover.json',
            'data/w33_pass12189_12193_five_bridges.json')}}
    print({k:('done'if isinstance(v,dict)else v)for k,v in result.items()},flush=True)
    (ROOT/'data/w33_pass12194_12198_native_completion.json').write_text(json.dumps(result,indent=2,default=lambda x:int(x) if isinstance(x,np.integer) else float(x))+'\n')
