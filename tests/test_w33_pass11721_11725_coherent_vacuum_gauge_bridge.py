"""Independent operator, differential and branch controls for11721–11725."""
import hashlib
import json
from pathlib import Path
import sys
from collections import Counter
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11721_11725_coherent_vacuum_gauge_bridge as B


def test_frozen_source_binding_and_five_scoped_interfaces():
    d=json.loads(B.OUT.read_text())
    assert d['source_sha256']==hashlib.sha256(Path(B.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    assert all(d[str(i)]['status']=='PASS' for i in range(11721,11726))
    assert d['11722']['positive_directions']==51 and d['11722']['zero_directions']==5
    assert d['11724']['with_Y6_centralizer_dimension']==12


def test_exact_weyl_convention_matches_independent_tensor_operators():
    for v in B.V.nonzero(2):
        a=B.exact_weyl(v)
        assert np.allclose(B.enum(a),B.V.weyl(v),atol=2e-14)
        assert np.allclose(B.enum(B.edag(a)),B.enum(a).conj().T)


def test_all320_projectors_and_literal_Maschke_zero_projections():
    for row,r,o,e in B.exact_flags():
        pr=B.enum(r)/9;po=B.enum(o)/18;pe=B.enum(e)/18
        p=B.PTS[row['point']]
        assert np.linalg.matrix_rank(pr,tol=1e-10)==1
        assert np.linalg.norm(B.V.weyl(p)@pr-pr)<1e-12
        assert np.linalg.norm(B.PI@po+po)<1e-12 and np.linalg.norm(B.PI@pe-pe)<1e-12
        v=np.linalg.eigh(po)[1][:,-1]
        assert np.linalg.norm(B.N.quartic(B.ON.conj().T@v))<1e-12
        assert B.s4(v)<1e-25


def test_all40_even_tetrahedra_are_actual_qubit_SICs():
    for p in range(40):
        block={B.ekey(e):B.enum(e)/18 for r,_,o,e in B.exact_flags() if r['point']==p}
        es=list(block.values());assert len(es)==4
        Q=sum(es)/2;ev,U=np.linalg.eigh(Q);T=U[:,ev>.5];assert T.shape==(9,2)
        paulis=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]])
        bloch=np.array([[np.trace(T.conj().T@e@T@sigma).real for sigma in paulis] for e in es])
        assert np.allclose(bloch@bloch.T,4*np.eye(4)/3-np.ones((4,4))/3,atol=2e-13)
        assert np.linalg.norm(bloch.sum(0))<1e-12


def test_coherent_phase_law_and_partner_chirality():
    for _,r,_,_ in B.exact_flags()[::31]:
        psi=np.linalg.eigh(B.enum(r)/9)[1][:,-1]
        e=(psi+B.PI@psi)/np.sqrt(2);o=(psi-B.PI@psi)/np.sqrt(2)
        for theta in np.linspace(0,2*np.pi,13):
            q=(e+np.exp(1j*theta)*o)/np.sqrt(2)
            assert abs(B.s4(q)-(27*np.cos(theta)**4+9*np.sin(theta)**4)/8)<1e-12
        a=np.einsum('i,kij,j->k',psi.conj(),B.OPS,psi).imag
        p=B.PI@psi
        assert np.linalg.norm(a+np.einsum('i,kij,j->k',p.conj(),B.OPS,p).imag)<1e-12


def test_joint_action_at_all320_lifts_and_away_from_them():
    rng=np.random.default_rng(11722)
    for _,r,_,_ in B.exact_flags():
        psi=np.linalg.eigh(B.enum(r)/9)[1][:,-1];x=B.parent_lift(psi)
        assert abs(B.coupled_potential(x,psi))<1e-11
    for _ in range(20):
        psi=rng.normal(size=9)+1j*rng.normal(size=9)
        assert B.coupled_potential(rng.normal(size=38),psi)>=0


def test_joint_action_uses_one_common_charge_and_new_even_companion():
    rng=np.random.default_rng(14);x=rng.normal(size=38);psi=rng.normal(size=9)+1j*rng.normal(size=9)
    a=x[::2]+1j*x[1::2];charges=np.r_[np.ones(4),np.ones(10)*2,np.ones(5)*4]
    phase=.371;rot=B.realvec(a*np.exp(1j*phase*charges))
    assert abs(B.coupled_potential(rot,psi*np.exp(1j*phase))-B.coupled_potential(x,psi))<1e-8
    # Charge4 would fail the required phase law for a common9-dimensional state.
    e=B.EN[:,0];o=B.ON[:,0]
    assert np.linalg.norm(e*np.exp(4j*phase)+o*np.exp(1j*phase)-(e+o)*np.exp(1j*phase))>.1


def test_full_chirality_Hessian_against_direct_potential_differences():
    psi=np.eye(9,dtype=complex)[:,1];H=B.chirality_hessian(psi)
    rng=np.random.default_rng(91)
    for _ in range(10):
        v=rng.normal(size=18);v/=np.linalg.norm(v);z=v[::2]+1j*v[1::2]
        def f(t):
            p=psi+t*z;r=np.vdot(p,p).real
            return (r-1)**2+27/8*r**4-B.s4(p)
        h=2e-4;D=(f(h)-2*f(0)+f(-h))/h**2
        assert abs(D-v@H@v)<1e-5


def test_density_commutator_does_not_impose_vector_neutrality():
    psi=np.eye(9)[:,3];rho=np.outer(psi,psi)-np.eye(9)/9
    H=np.diag([0,0,0,1,-1,0,0,0,0])
    assert np.linalg.norm(H@rho-rho@H)==0 and np.linalg.norm(H@psi)==1
    omega=B.V.W
    assert abs(omega**3-1)<1e-14 and abs(omega-1)>1
    # The E8 adjoint center action is identity; the fundamental9 action is not.
    assert abs(np.linalg.det(omega*np.eye(9))-1)<1e-14


def test_actual_adjoint_SU2_and_full_mass_spectrum():
    C,K,ads,Y=B.adjoint_kinetics()
    assert np.linalg.norm(ads[0]@ads[1]-ads[1]@ads[0]-1j*ads[2])<1e-10
    assert max(np.linalg.norm(Y@a-a@Y) for a in ads)<1e-10
    expected=Counter({0:12,2:3,6:23,7:60,11:12,12:7,16:42,20:9,21:28,22:30,25:12,42:10})
    assert Counter(np.rint(np.linalg.eigvalsh(K)).astype(int))==expected
    assert np.count_nonzero(abs(np.linalg.eigvalsh(C))<1e-9)==24


def test_massless_space_is_literal_visible_SM_algebra():
    _,K,_,_=B.adjoint_kinetics();basis,Sl,_=B.E.e8_basis();Q=np.linalg.qr(Sl)[0]
    mats=[]
    for block in [[0,1,2],[7,8]]:
        for i in block:
            for j in block:
                if i!=j:
                    a=np.zeros((9,9));a[i,j]=1;mats.append(a)
    for i in B.F5[:-1]:
        a=np.zeros((9,9));a[i,i]=1;a[8,8]=-1;mats.append(a)
    cols=np.array([np.r_[Q.conj().T@a.ravel(),np.zeros(168)] for a in mats]).T
    assert np.linalg.matrix_rank(cols)==12 and np.linalg.norm(K@cols)<1e-10


def test_mixed_invariant_reduction_independently_from_SU5_weights():
    x=s.symbols('x0:5');p2=sum(t*t for t in x);p4=sum(t**4 for t in x)
    p10=sum((x[i]+x[j])**4 for i in range(5) for j in range(i+1,5))
    relation=(360*p10+2040*p4-1080*p2*p2-960*p4).subs(x[4],-sum(x[:4]))
    assert s.expand(relation)==0
    C,_,_,Y=B.adjoint_kinetics()
    assert abs(np.trace(C@C@Y@Y@Y@Y).real-1173600)<1e-7
    rng=np.random.default_rng(105)
    # General diagonal Sigma, independently using all240 E8 root weights.
    c2diag=np.diag(C@C).real
    for _ in range(8):
        vals=rng.integers(-3,4,size=4).tolist();vals.append(-sum(vals))
        t=np.zeros(9);t[B.F5]=vals
        charges=[t[i]-t[j] for i in range(9) for j in range(9) if i!=j]+[0]*8
        charges += [sum(t[i] for i in triple) for triple in B.E.TR]
        charges += [-sum(t[i] for i in triple) for triple in B.E.TR]
        actual=c2diag@np.array(charges)**4
        want=1080*sum(a*a for a in vals)**2+960*sum(a**4 for a in vals)
        assert abs(actual-want)<1e-5


def test_exact_shape_extrema_and_bounded_completion_scope():
    d=B.selection_certificate()
    candidates=list(map(s.Rational,[*d['stationary_two_value_ratios'].values(),*d['stationary_three_value_ratios']]))
    assert min(candidates)==s.Rational(7,30)
    assert 1080+960*s.Rational(7,30)==1304
    gg=[-2,-2,-2,3,3]
    shape=lambda a:960*(sum(x**4 for x in a)-s.Rational(7,30)*sum(x*x for x in a)**2)
    assert shape(gg)==shape([-x for x in gg])==0
    assert shape([1,1,1,1,-4])>0
    assert s.Integer(23085000)<s.Integer(d['normalized_Cartan_traces_GG']['8'])


def test_native_clock_Higgs_compatibility_and_class_selection():
    units,Js,_=B.hidden_su5();lam=B.V.W**B.Y0
    D=np.array(B.N.canonical_generators()['D0'].subs(B.N.W,B.V.W),dtype=complex)
    assert np.linalg.norm(np.diag(lam)-B.V.W*D)<1e-12
    for A,x,k in Js:
        assert np.linalg.norm(np.diag(lam)@A@np.diag(lam).conj().T-A)<1e-12
        assert np.linalg.norm(np.array([np.prod(lam[list(t)]) for t in B.E.TR])*x-x)<1e-12
        assert np.linalg.norm(np.array([np.prod(lam[list(t)]).conjugate() for t in B.E.TR])*k-k)<1e-12
    d=B.adjoint_higgs_certificate()
    assert d['clock_Higgs_mass_squared_multiplicities']=={'0':12,'2':15,'3':12,'5':18,'6':15,'9':90,'12':35,'15':42,'20':9}
    assert {tuple(x['SU5_cube_root_multiplicities']) for x in d['all_SU5_cubed_identity_clock_classes'] if x['E8_adjoint_trace']==5}=={(2,3,0),(2,0,3)}


def test_compact_E8_norm_Ward_identity_in_general_trivector_directions():
    rng=np.random.default_rng(11724)
    def random_element():
        A=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
        A-=np.trace(A)/9*np.eye(9)
        return A,rng.normal(size=84)+1j*rng.normal(size=84),rng.normal(size=84)+1j*rng.normal(size=84)
    def inner(a,b):return sum(np.vdot(x,y) for x,y in zip(a,b))
    for _ in range(3):
        t,a,b=random_element(),random_element(),random_element()
        t=B.add(t,B.scale(-1,B.star(t)))
        assert abs(inner(B.E.bracket(t,a),b)+inner(a,B.E.bracket(t,b)))<1e-10
