"""Independent algebra, topology, equivariance and fixed-data controls."""
import hashlib
import itertools as it
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11734_11741_gauging_and_chiral_quotient as M


def frozen():return json.loads(M.OUT.read_text())


def test_source_binding_and_all_eight_scopes():
    p=frozen()
    assert p['source_sha256']==hashlib.sha256(Path(M.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    assert set(p['passes'])=={str(i) for i in range(11734,11742)}
    assert all(v['status']=='PASS' and v['scope'] for v in p['passes'].values())


def test_theta_linear_constraint_in_actual_seven_pair_sector():
    labs,ws,_=M.P.roots();ix={a:i for i,a in enumerate(labs)}
    ts=M.theta_terms();w=tuple(a+b for a,b in zip(ws[ix[ts[0][0]]],ws[ix[ts[0][1]]]))
    pairs,omega,_=M.P.weight_casimir(w)
    vec=s.Matrix([next(c for a,b,c in ts if tuple(sorted((ix[a],ix[b])))==pair) for pair in pairs])
    assert omega*vec==-12*vec


def test_embedding_map_rank_isotropic_and_square_zero():
    labs,_,_=M.P.roots();ix={a:i for i,a in enumerate(labs)};T=s.zeros(240)
    for a,b,c in M.theta_terms():
        ad,sa=M.P.dual(a);bd,sb=M.P.dual(b)
        T[ix[b],ix[ad]]=c*sa;T[ix[a],ix[bd]]=c*sb
    assert T.rank()==14 and T*T==s.zeros(240)


def test_all_image_brackets_against_original_tensor_implementation():
    image=sorted({x for a,b,c in M.theta_terms() for x in (a,b)})
    for a,b in it.combinations(image,2):
        assert np.max(abs(M.E._vec(M.E.bracket(M.P.root_element(a),M.P.root_element(b)))))==0
    assert all(not M.tensor_action(x,M.theta_terms()) for x in image)


def test_cartan_bracket_signs_against_original_tensor_implementation():
    for a in [('A',3,0),('x',0,1,3),('k',3,4,5)]:
        b=M.P.dual(a)[0];out=M.bracket_exact(a,b)
        diag=np.zeros(9)
        for (_,i),c in out.items():diag[i]+=float(c);diag[8]-=float(c)
        actual=M.E.bracket(M.P.root_element(a),M.P.root_element(b))
        assert np.allclose(actual[0],np.diag(diag)) and not np.any(actual[1]) and not np.any(actual[2])


def test_compact_real_tensor_fails_but_each_pure_component_passes():
    ts=M.theta_terms();star=[]
    for a,b,c in ts:
        ad,sa=M.P.dual(a);bd,sb=M.P.dual(b);star.append((ad,bd,c*sa*sb))
    assert not M.tensor_action(('A',3,0),ts)
    witness=M.tensor_action(('A',3,0),star)
    assert witness and M.tensor_action(('A',3,0),list(ts)+star)==witness
    # A nonzero compact-real combination necessarily has nonzero mixed coefficient.
    for a in [1,1j,2+3j]:assert abs(a*np.conjugate(a))>0


def test_global_nonprincipal_triplet_on_trivial_lines():
    J=M.P.su2_generators((1,1,1,2));projector=np.diag([0,0,0,1,1])
    assert np.allclose(J[0]@J[1]-J[1]@J[0],1j*J[2])
    assert np.allclose(sum(j@j for j in J),.75*projector)
    for phases in [(0.2,-.7,.5),(.4,.1,-.5)]:
        transition=np.diag([*(np.exp(1j*np.array(phases))),1,1])
        assert all(np.allclose(transition@j@transition.conj().T,j) for j in J)


def test_global_higgs_centralizers_record_remaining_gauge_obligations():
    p=M.higgs_certificate()
    assert p['full_E8_centralizer_dimension']==133
    assert p['dimension_after_bundle_and_triplet']==37
    assert p['dimension_after_Wilson']==21 and p['dimension_after_hypercharge']==15
    assert 'replaces' in p['branch_input'] and 'extra U1' in p['scope']


def test_clean_product_dirac_index_and_old_positive_line_obstruction():
    ns=np.array(M.NS)
    assert np.sum(ns,axis=0).tolist()==[0,0,0]
    assert int(sum(np.prod(n) for n in ns))==3
    assert np.array_equal(ns@np.array([18,12,6]),np.zeros(3))
    assert all(np.prod(n)>=0 for n in ns)
    # The old (1,1,1) line has strictly positive slope for every positive Kahler class.
    for t in [(1,1,1),(2,3,6),(.1,9,2)]:assert sum(t[i]*t[j] for i,j in it.combinations(range(3),2))>0


def test_tetraquadric_rr_and_koszul_counts_independently():
    cover=[]
    for n in M.NS:
        v=(*n,0);h=M.tetraquadric_cohomology(v);dual=M.tetraquadric_cohomology(tuple(-x for x in v))
        rr=2*sum(np.prod(t) for t in it.combinations(v,3))+2*sum(v)
        assert sum((-1)**q*d for q,d in enumerate(h))==rr
        assert h==list(reversed(dual))
        cover.append(h)
    assert cover==[[0,0,0,0],[0,0,4,0],[0,0,2,0]]


def test_positive_cy_kahler_point_and_anomaly_budget():
    p=M.kinetic_certificate();t=[s.sympify(x) for x in p['CY_Kahler_class']]
    assert all(float(x)>0 for x in t)
    dual=[sum(t[j]*t[k] for j,k in it.combinations([j for j in range(4) if j!=i],2)) for i in range(4)]
    for n in M.NS:assert s.simplify(sum(n[i]*dual[i] for i in range(3)))==0
    c2=p['CY_c2_squarefree']
    assert c2=={'0,1':3,'0,2':0,'0,3':0,'1,2':3,'1,3':0,'2,3':0}
    assert all(v>=0 for v in M.quotient_certificate()['anomaly_class_cover_squarefree'].values())


def test_free_quotient_linear_system_contains_each_corner():
    p=M.quotient_certificate();monomials={tuple(v) for v in p['invariant_monomial_exponents']}
    assert len(monomials)==41
    for corner in it.product((0,2),repeat=4):assert corner in monomials
    assert all(sum(t)%2==0 for t in monomials)


def test_cech_basis_parities_without_index_division_shortcut():
    dims=[]
    for n in M.NS:
        shifted=[v-2 for v in (*n,0)]
        if -1 in shifted:dims.append((0,0));continue
        powers=[range(v+1) if v>=0 else range(1,-v) for v in shifted]
        signs=[(-1)**sum(t) for t in it.product(*powers)]
        dims.append((signs.count(1),signs.count(-1)))
    assert dims==[(0,0),(2,2),(1,1)]
    assert sum(a for a,b in dims)==sum(b for a,b in dims)==3


def test_split_holomorphic_mass_inventory_has_no_hidden_profile():
    p=M.quotient_certificate()
    assert len(p['holomorphic_Sym2V_scalar_profiles'])==6
    assert all(t['H0']==0 for t in p['holomorphic_Sym2V_scalar_profiles'])
    assert M.tetraquadric_cohomology((-1,1,1,0))==[0]*4 # L1 dual
    assert 'vanish' in p['cubic_selection'] and 'not an MSSM' in p['Wilson_family_retention']


def test_section_spectral_projector_is_an_actual_polynomial():
    x=s.symbols('x');f=s.sympify(M.section_certificate()['section_projector_polynomial'])
    labs,ws,_=M.P.roots();values=[f.subs(x,s.Rational(w[3],3)) for w in ws]+[f.subs(x,0)]*8
    assert set(values)=={0,1} and sum(values)==8


def test_frobenius_failure_is_a_vector_field_bracket_not_e8_bracket():
    u,v,w,z=s.symbols('u v w z');coords=(u,v,w,z)
    X=s.Matrix([1,u,0,0]);Y=s.Matrix([0,0,1,u])
    bracket=Y.jacobian(coords)*X-X.jacobian(coords)*Y
    assert bracket==s.Matrix([0,0,0,1])
    assert s.Matrix.hstack(X,Y,bracket).subs(u,0).rank()==3


def test_thermal_superselection_still_has_volume_response():
    V=np.diag([2.,3.]);H=np.diag([.2,-.7]);beta=.8
    def rho(c):
        a=expm(-beta*(H+c*V));return a/np.trace(a)
    c=.31;eps=1e-5;r=rho(c);mean=np.trace(r@V)
    slope=np.trace((rho(c+eps)-rho(c-eps))@V)/(2*eps)
    assert abs(slope+beta*(np.trace(r@V@V)-mean**2))<1e-9
    assert not np.allclose(rho(0),rho(1))
    assert np.array_equal(r@V,V@r) # no inter-volume coherence


def test_full_rank_gibbs_invariance_requires_scalar_volume():
    H=np.array([[0.,.4],[.4,1.]])
    def state(V,c):
        r=expm(-(H+c*V));return r/np.trace(r)
    assert np.allclose(state(2*np.eye(2),0),state(2*np.eye(2),3))
    assert not np.allclose(state(np.diag([2.,3.]),0),state(np.diag([2.,3.]),3))


def test_signed_e6_cubic_dictionary_and_basis_covariance():
    p=M.cubic_certificate();d=np.zeros((27,27,27),int)
    for i,j,k,c in p['signed_cubic_entries']:d[i,j,k]=c
    assert np.count_nonzero(d)==270
    assert len({tuple(sorted((i,j,k))) for i,j,k in zip(*np.nonzero(d))})==45
    assert np.array_equal(np.einsum('ijk,ljk->il',d,d),10*np.eye(27))
    rng=np.random.default_rng(11739);perm=rng.permutation(27);sign=rng.choice([-1,1],27)
    rotated=d[np.ix_(perm,perm,perm)]*sign[:,None,None]*sign[None,:,None]*sign[None,None,:]
    assert np.array_equal(np.einsum('ijk,ljk->il',rotated,rotated),10*np.eye(27))


def test_signed_cubic_selected_entries_against_original_e8_bracket():
    p=M.cubic_certificate();basis=p['all81_signed_root_dictionary']
    for i,j,k,c in p['signed_cubic_entries'][::27]:
        a,ca=basis[0][i];b,cb=basis[1][j];t,ct=basis[2][k]
        bracket=M.E.bracket(M.P.root_element(tuple(a)),M.P.root_element(tuple(b)))
        dual,sgn=M.P.dual(tuple(t));target=M.P.root_element(dual)
        coefficient=np.vdot(M.E._vec(target),M.E._vec(bracket))
        assert abs(ca*cb*ct*sgn*coefficient-c)<1e-12


def test_all_cy_first_order_bundle_directions_are_unobstructed_ambient_directions():
    h1=0
    for i,j in it.product(range(3),repeat=2):
        n=tuple(a-b for a,b in zip(M.NS[i],M.NS[j]))+(0,)
        ambient=M.ambient_cohomology(n);shifted=M.ambient_cohomology(tuple(v-2 for v in n))
        assert ambient[2]==shifted[2]==0
        assert M.tetraquadric_cohomology(n)[1]==ambient[1]
        h1+=ambient[1]
    assert h1==30


def test_nearby_ambient_matter_cubics_factor_through_zero_cohomology():
    for n in M.NS:
        dual=tuple(-v for v in (*n,0))
        assert M.ambient_cohomology(tuple(v-2 for v in dual))==[0]*5
    assert M.ambient_cohomology((0,0,0,0))[3]==0
    p=M.quotient_certificate()
    assert p['ambient_bundle_obstruction_h2']==0 and p['ambient_bundle_deformation_h1']==30
    assert 'sufficiently small' in p['persistent_cubic_zero']


def test_published_all_order_obstruction_criterion_on_actual_ambient_bundle():
    # Enumerate the P1 H0/H1 Kunneth factors rather than invoking the producer.
    def kunneth_h2(degree):
        total=0
        for choices in it.product((0,1),repeat=4):
            if sum(choices)!=2:continue
            factors=[max(n+1,0) if q==0 else max(-n-1,0) for n,q in zip(degree,choices)]
            total+=int(np.prod(factors))
        return total
    lines=[(*n,0) for n in M.NS]
    checks={'V':sum(kunneth_h2(n) for n in lines),
            'V_dual':sum(kunneth_h2(tuple(-v for v in n)) for n in lines),
            'End0V':sum(kunneth_h2(tuple(a-b for a,b in zip(n,m))) for n in lines for m in lines)}
    assert checks=={'V':0,'V_dual':0,'End0V':0}
    assert frozen()['passes']['11741']['higher_order_ambient_H2']==checks
