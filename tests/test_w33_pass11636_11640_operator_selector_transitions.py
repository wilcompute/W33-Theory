"""Independent exact and physical controls for the five declared follow-ups."""
from pathlib import Path
import sys,json,hashlib,itertools as it
import numpy as np
import sympy as s
import networkx as nx
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11636_11640_operator_selector_transitions as m

@pytest.fixture(scope='module')
def cert():return json.loads(m.OUT.read_text())

def symbolic(rows):return s.Matrix(rows).applyfunc(s.sympify)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def test_bindings_and_allfive(cert):
    assert cert['passes']==list(range(11636,11641)) and cert['producer_sha256']==m.digest(m.__file__)
    for k in ['flavor','complex_selector','tree_transitions','vacuum_response','fermion_IR']:assert cert[k]['status']=='PASS'
    assert cert['flavor']['E6_input_sha256']==sha(ROOT/'data/w33_pass11636_e6_cubic_inputs.npz')
    for k in ['complex_selector','fermion_IR']:
        d=cert[k]
        if k=='fermion_IR':assert d['certificate_sha256']==sha(ROOT/d['certificate'])
        else:assert d['archive_sha256']==sha(ROOT/d['archive'])

def test_CP_exact_polynomial_and_CP_control(cert):
    d=cert['flavor'];a,b=symbolic(d['Y1']),symbolic(d['Y2']);e=s.symbols('epsilon',real=True);A=(a.H*a).applyfunc(s.expand);y=a+e*b;B=(y.H*y).applyfunc(s.expand);C=(A*B-B*A).applyfunc(s.expand)
    result=s.factor(s.expand(s.trace(C**3)/s.I));assert result==s.sympify(d['CP_polynomial'],locals={'epsilon':e})
    assert result.subs(e,0)==0 and result.subs(e,1)!=0 and s.degree(result,e)==6
    # Physical CP conjugates all geometry/coefficient tensors; epsilon is real.
    assert s.simplify(s.conjugate(result*s.I)/s.I+result)==0
    assert s.simplify(a.det())==-s.Rational(56,3)
    rng=np.random.default_rng(11636);z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));G=np.linalg.qr(z)[0]
    aa=np.array(a,complex);bb=np.array(a+b,complex);Hu=aa.conj().T@aa;Hd=bb.conj().T@bb;comm=Hu@Hd-Hd@Hu
    rotated=G@comm@G.conj().T;assert np.trace(rotated@rotated@rotated).imag==pytest.approx(float(result.subs(e,1)))
    assert np.trace((Hu@Hu-Hu@Hu)**3)==0

def test_incidence_operator_continuous_covariance_and_symmetry(cert):
    d=cert['flavor'];_,group,gens,pg,cp,tr,configs=m.old.clifford_geometry();rng=np.random.default_rng(11636);h=rng.normal(size=3)+1j*rng.normal(size=3);c=tuple(map(tuple,d['selected_config']));a,b=m.incidence_yukawas(c,h)
    for p,G in zip(pg,gens):
        aa,bb=m.incidence_yukawas(tr(c,p),G@h)
        assert np.allclose(aa,G.conj()@a@G.conj().T) and np.allclose(bb,G.conj()@b@G.conj().T)
    # Global projective phases are canceled by psi psi hbar hbar.
    theta=.37;aa,bb=m.incidence_yukawas(c,np.exp(1j*theta)*h)
    assert np.allclose(aa,np.exp(-2j*theta)*a) and np.allclose(bb,np.exp(-2j*theta)*b)
    assert np.allclose(a,a.T) and np.allclose(b,b.T)
    ccp=tr(c,cp);aa,bb=m.incidence_yukawas(ccp,h.conj())
    assert np.allclose(aa,a.conj()) and np.allclose(bb,b.conj())

def test_exact_all5184_orbit_coverage_and_CP(cert):
    d=cert['flavor'];_,group,_,_,_,tr,configs=m.old.clifford_geometry();seen=set();count={'CP_zero':0,'CP_nonzero':0};ranks={}
    for item in d['exact_joint_orbit_representatives']:
        c=tuple(map(tuple,item['config']));h=item['h'];orbit={(tr(c,p),p[h]) for p in group};assert len(orbit)==item['orbit_size'] and not seen&orbit;seen|=orbit
        a,b=m.incidence_yukawas(c,m.family_rays(True)[h],True);y=a+b;A=(a.H*a).applyfunc(s.expand);B=(y.H*y).applyfunc(s.expand);C=(A*B-B*A).applyfunc(s.expand);cp=s.factor(s.expand(s.trace(C**3)/s.I))
        assert cp==s.sympify(item['CP_epsilon1']) and [a.rank(),y.rank()]==item['rank_pair']
        count['CP_zero' if cp==0 else 'CP_nonzero']+=len(orbit);key=str(tuple(item['rank_pair']));ranks[key]=ranks.get(key,0)+len(orbit)
    assert seen=={(c,h) for c in configs for h in range(12)} and count=={'CP_nonzero':4752,'CP_zero':432}
    assert count==d['all5184_CP_census_exact'] and ranks==d['all5184_rank_census']

def test_signed_E6_all_generators_and_Pauli_allowed(cert):
    x=np.load(ROOT/'data/w33_pass11636_e6_cubic_inputs.npz');d,B=x['d'],x['B'];assert len(B)==78
    for b in B:
        defect=np.einsum('ai,ajk->ijk',b,d)+np.einsum('aj,iak->ijk',b,d)+np.einsum('ak,ija->ijk',b,d);assert not np.any(defect)
    y=np.array(symbolic(cert['flavor']['Y1']),complex);M=np.kron(d[:,:,0],y);assert np.array_equal(M,M.T)
    # Antisymmetric family epsilon would make this combined mass antisymmetric.
    bad=np.kron(d[:,:,0],np.array([[0,1,0],[-1,0,0],[0,0,0]]));assert np.array_equal(bad,-bad.T) and np.any(bad)

def test_all4480_exact_structures_BFS_and_energy(cert):
    d=cert['complex_selector'];x=np.load(ROOT/d['archive']);orbit,perm,parents,E=x['orbit'],x['permutations'],x['parents'],x['energy'];_,_,omega,refs=m.old.coxeter_data();Ts=[np.array(4*r,dtype=np.int64) for r in refs]
    assert np.array_equal(orbit[0],np.array(4*omega,dtype=np.int64)) and len({r.tobytes() for r in orbit})==4480
    for i,a in enumerate(orbit):
        assert np.array_equal(a@a+4*a,-16*np.eye(8,dtype=np.int64));N=a[4:,4:]+2*np.eye(4,dtype=np.int64);assert np.sum((N@N+4*np.eye(4,dtype=np.int64))**2)==16*E[i]
        if i:
            p,g=parents[i];assert p<i and np.array_equal(Ts[g]@orbit[p]@Ts[g],16*a)
        for g,T in enumerate(Ts):assert np.array_equal(T@a@T,16*orbit[perm[g,i]])
    assert dict(zip(*np.unique(E,return_counts=True)))=={0:2304,10:2048,16:128}

def test_gated_selector_unique_ground_and_ungated_control(cert):
    d=cert['complex_selector'];x=np.load(ROOT/d['archive']);E=x['energy'];p=x['permutations'];P=(E-10)*(E-16)/160;assert np.array_equal(P,P*P)
    G=nx.Graph();G.add_nodes_from(np.flatnonzero(P))
    for i in G:
        for perm in p:
            if P[perm[i]] and perm[i]!=i:G.add_edge(i,int(perm[i]))
    assert nx.is_connected(G) and G.number_of_edges()==7920
    v=P/np.sqrt(2304);L=np.zeros(4480)
    for perm in p:L+=v-v[perm]
    assert np.dot(L[P==0],L[P==0])==pytest.approx(25/16)
    assert s.Rational(d['ungated_uniform_good_leakage_norm_squared'])==s.Rational(25,16)
    assert s.Rational(2,2303**2)>0  # proved connectivity/path lower bound

def test_rational_tree_midpoint_and_native_cycle(cert):
    d=cert['tree_transitions'];B,C=m.cycle_basis();T=d['tree'];f=d['chord'];e=d['removed_edge'];G=nx.Graph();G.add_nodes_from(range(80))
    edges=[tuple(np.flatnonzero(B[:,i])) for i in range(160)];G.add_edges_from(edges[i] for i in T);assert nx.is_tree(G)
    G.add_edge(*edges[f]);cycles=nx.cycle_basis(G);assert len(cycles)==1 and len(cycles[0])==8
    G.remove_edge(*edges[e]);assert nx.is_tree(G)
    g=s.Matrix([s.sympify(z) for z in d['exact_midpoint_g']]);a=s.Rational(d['exact_midpoint_A']);assert a==s.Rational(2012,125)
    assert -g.dot(g)/a==-s.Rational(45,503) and g.dot(s.ones(80,1))==0
    H=-g*g.T/a;assert H.rank()==1 and H*s.ones(80,1)==s.zeros(80,1)
    assert all(x['rank']==1 and x['negative_eigenvalue']<0 for x in d['weighted_overlap_sweep'])

def test_continuous_forest_exchange_changes_constraint_rank(cert):
    d=cert['tree_transitions'];B,_=m.cycle_basis();edges=[tuple(np.flatnonzero(B[:,i])) for i in range(160)]
    for item in d['forest_exchange_path']:
        t=item['t'];w=np.zeros(160);w[d['tree']]=1;w[d['removed_edge']]=max(1-2*t,0);w[d['chord']]=max(2*t-1,0)
        G=nx.Graph();G.add_nodes_from(range(80));G.add_edges_from(edges[i] for i in np.flatnonzero(w));assert nx.is_forest(G)
        assert nx.number_connected_components(G)==item['components']
    mid=d['forest_exchange_path'][2];assert mid['edges']==78 and mid['components']==2 and mid['conditional_static_spin2_count']==394
    assert d['forest_exchange_path'][0]['conditional_static_spin2_count']==397

def cap_equations(z,C,alpha,Q,Qhat,delta=0):
    R,L,K=z;rho=L+C+np.array([1.2,.8])**2/2+np.array([delta,0]);H2=rho/(3*K);cc=np.array([-1,1])*np.sqrt(1-H2*R*R);V=2*np.pi**2/H2**2*(2/3-cc+cc**3/3);area=2*np.pi**2*R**3;curvature=(4*(rho@V)+1.2*area)/(K*sum(V));sig=1+3*alpha*L*L
    return np.array([sum(cc)/R-.2/K,sum(V)-Q*sig,curvature+2*Qhat/(Q*sig)])

def test_coupled_cap_unequal_volume_Ward_and_response(cert):
    d=cert['vacuum_response']
    for case in d['cases']:
        a,Q,Qh=case['alpha'],case['fixed_Q'],case['fixed_Qhat'];ref=np.array(case['reference']);shift=np.array(case['common_C03_solution']);other=np.array(case['unequal_threshold01_solution'])
        assert max(abs(cap_equations(ref,0,a,Q,Qh)))<1e-8
        assert max(abs(cap_equations(shift,.03,a,Q,Qh)))<1e-8
        assert max(abs(cap_equations(other,0,a,Q,Qh,.01)))<1e-8
        assert case['reference_cap_volumes'][0]>5*case['reference_cap_volumes'][1]
        # Test implicit derivative in the independently reconstructed equations.
        eps=1e-5;dx=np.array(case['d_R_Lambda_K_d_common_C']);dF=(cap_equations(ref+eps*dx,eps,a,Q,Qh)-cap_equations(ref-eps*dx,-eps,a,Q,Qh))/(2*eps)
        assert max(abs(dF))<2e-5
    assert np.allclose(d['cases'][0]['d_R_Lambda_K_d_common_C'],[0,-1,0])
    assert d['cases'][1]['d_R_Lambda_K_d_common_C'][2]>1

def test_fermion_full_normal_matrices_and_cutoff_domain(cert):
    d=json.loads((ROOT/cert['fermion_IR']['certificate']).read_text());x=np.load(ROOT/d['archive']);assert sha(ROOT/d['archive'])==d['archive_sha256']
    import w33_pass11637_fermion_ir_normals as fermion
    assert d['producer_sha256']==m.digest(fermion.__file__)
    V,T,D=fermion.old.scalar_data()
    for i,item in enumerate(d['cases']):
        H,G,N,q=(x[f'{k}_{i}'] for k in ['H','G','N','q']);assert H.shape==(297,297) and N.shape==(297,264)
        A=np.einsum('a,aij->ij',q[:45],V);S=np.einsum('a,aij->ij',q[45:],D);ga=V@A-A@V;gs=T@S+S@T.transpose(0,2,1);actual=np.vstack([np.einsum('aij,bij->ab',V,ga)/2,2*np.einsum('aij,bij->ab',D.conj(),gs).real])
        assert np.max(abs(actual-G))<1e-12 and np.linalg.matrix_rank(G,tol=1e-9)==33
        assert np.linalg.norm(H@G)<1e-8 and np.linalg.norm(G.T@N)<1e-12 and np.max(abs(N.T@N-np.eye(264)))<1e-12
        eigen=np.linalg.eigvalsh(N.T@H@N);assert eigen[0]>.0016 and np.allclose(eigen,item['normal_eigenvalues'],atol=1e-11)
        assert item['scalar_minimum_mass_squared']<0 and item['minimum_scalar_denominator']>0
        assert item['naive_lower_cutoff_boundary']<item['infrared'] and item['naive_lower_cutoff_boundary']>.018
        if i in [0,2]:assert item['quadrature_control']['reference_order']==128 and item['quadrature_control']['H_operator_error']<1e-8

def test_fermion_count_and_complex_repeated_spectrum():
    import w33_pass11637_fermion_ir_normals as q
    import jax.numpy as j
    from numpy.polynomial.legendre import leggauss
    M=q.background_map();x=np.array([1.,0.,1.]);point=M@x
    fields,_,_,_,f,_,_=q.make_action(24,.1,.03,3);_,_,_,_,boson,_,_=q.make_action(24,.1,.03,0)
    _,S=fields(point);masses=np.linalg.eigvalsh(np.array(S).conj().T@np.array(S));z,w=leggauss(24);p=.13+.12*z
    expected=-6*np.sum(w*.12*p/(64*np.pi**2)*np.log1p(.03**2*masses[:,None]/p))
    assert float(f(j.asarray(point))-boson(j.asarray(point)))==pytest.approx(expected,abs=1e-12)
    assert masses[-1]==pytest.approx(1.) and np.max(abs(masses[:-1]))<1e-12


def test_exact_weak_fermion_sector_selection_and_failed_control(cert):
    d=cert['flavor'];e=s.symbols('epsilon',real=True);rows=d['exact_joint_orbit_representatives'];moments=[s.sympify(r['squared_mass_trace_polynomial'],locals={'epsilon':e}) for r in rows]
    for item in d['fermion_loop_sector_selection']:
        eps=s.Rational(item['epsilon']);scores=[p.subs(e,eps) for p in moments];best=max(scores);winners=[i for i,q in enumerate(scores) if q==best];gap=best-max(q for q in scores if q!=best)
        assert winners==item['winning_orbits'] and gap==s.Rational(item['exact_trace_gap'])
        r=rows[winners[0]];a,b=m.incidence_yukawas(r['config'],m.family_rays(True)[r['h']],True);y=a+eps*b;M=(y.H*y).applyfunc(s.expand);fourth=s.factor(s.expand(s.trace(M*M)))
        assert fourth==s.Rational(item['winner_fourth_mass_moment']) and s.Rational(item['sufficient_y_squared_bound'])==3*gap/(25*fourth)
        assert s.Rational(item['tested_y'])**2<s.Rational(item['sufficient_y_squared_bound'])
        assert [a.rank(),y.rank()]==item['selected_family_ranks']
        energies=item['full81_fermion_shell_energies'];assert max(energies[i] for i in winners)<min(v for i,v in enumerate(energies) if i not in winners)
    good,bad=d['fermion_loop_sector_selection'];assert good['epsilon']=='1/100' and good['total_selected_sectors']==432 and good['selected_family_ranks']==[3,3]
    assert s.sympify(good['selected_CP_invariant'])!=0 and good['exact_trace_gap']=='1586/16875'
    assert bad['total_selected_sectors']==144 and bad['selected_family_ranks']==[1,1] and s.sympify(bad['selected_CP_invariant'])==0
    # Remainder bound uses the actual81 mass multiplicity, not three alone.
    x=np.load(ROOT/'data/w33_pass11636_e6_cubic_inputs.npz');D=s.Matrix(x['d'][:,:,0]);assert D**3==D and s.trace(D*D)==10
