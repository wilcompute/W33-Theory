from pathlib import Path
import sys,itertools,json
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12186_context_cover_holonomy as m

@pytest.fixture(scope='module')
def cert():return json.loads((ROOT/'data/w33_pass12186_context_cover_holonomy.json').read_text())

def test_native_edges_match_original_builder():
    from w33_pass11991_native_four_period_cover import native_geometry
    _,E,_,_,_=native_geometry();_,e,_,A,_=m.native_data();assert e==E
    assert np.array_equal(A@A,5*np.eye(27,dtype=int)-4*A+5*np.ones((27,27),int))

def test_exhaustive_solver_against_independent_tiny_bruteforce():
    E=[(0,1),(0,2),(1,2)]
    for kind in ['C2','C3','C4','V4','V4_nonregular']:
        order={'C2':2,'C3':3}.get(kind,4)
        for gain in itertools.product(range(order),repeat=3):
            for root in range(4):
                brute=any(all(c[a]!=m.colour_action(kind,c[b],z)for (a,b),z in zip(E,gain))for tail in itertools.product(range(4),repeat=2)for c in [(root,*tail)])
                solved,_=m.solve_colouring(E,gain,kind,root=root)
                assert (solved is not None)==brute,(kind,gain,root)

def test_base_chromatic_certificate(cert):
    _,E,_,A,_=m.native_data();r=cert['base']['six_colour_witness'];assert all(r[a]!=r[b]for a,b in E)
    solved,_=m.solve_colouring(E,[0]*len(E),'identity',q=5);assert solved is None
    # Every independent colour class has size at most6, separately from CSP.
    import networkx as nx
    assert max(map(len,nx.find_cliques(nx.complement(nx.from_numpy_array(A)))))==6

def test_complete_deck_action_census_recomputed(cert):
    _,E,V,_,_=m.native_data();summary,rows=m.enumerate_holonomies(E,V)
    assert summary==cert['action_classification'];assert len(rows)==36
    assert sum(x['homomorphisms']for x in summary.values())==865
    assert [summary[k]['successful']for k in ['C2','C3','C4','V4','V4_nonregular']]==[0,0,0,36,0]

def test_all36_named_cover_maps_and_native_edges(cert):
    _,E,V,_,_=m.native_data()
    for row in cert['binary_successful_maps']:
        edges,colours=m.lifted_graph(E,V,row['coefficients'],row['vertex_colours'])
        assert len(edges)==540 and len(colours)==108
        assert all(colours[a]!=colours[b]for a,b in edges)
        for a in range(4):
            for x in range(4):
                assert all(colours[27*(x^a)+v]==(colours[27*x+v]^a)for v in range(27))

def test_binary_quadric_and_two_reguli(cert):
    q=lambda x:(x[0]+x[1]+x[0]*x[1]+x[0]*x[2]+x[1]*x[3])%2
    vec=list(itertools.product(range(2),repeat=4));Q=cert['binary_quadric'];zeros=[i for i,v in enumerate(vec)if not q(v)];assert zeros==Q['zero_vectors'] and len(zeros)==10
    B=np.array(Q['polar_matrix']);assert round(np.linalg.det(B))%2==1
    for x in vec:
        for y in vec:assert q(np.array(x)^y)==(q(x)+q(y)+np.array(x)@B@np.array(y))%2
    O=Q['H27_orbits'];assert list(map(len,O))==[3,3]
    for i,orbit in enumerate(O):
        for a,b in itertools.combinations(orbit,2):assert len(set(a)&set(b))==1
        for a in orbit:
            for b in O[1-i]:assert len(set(a)&set(b))==2

def test_unimodular_period_change_preserves_witness(cert):
    _,E,V,_,_=m.native_data();row=cert['binary_successful_maps'][0];A=np.array(row['coefficients']).reshape(2,4)
    T=np.array([[1,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,1]]);inv=np.rint(np.linalg.inv(T)).astype(int);AA=A@inv.T%2;VV=V@T
    assert np.array_equal(V@A.T%2,VV@AA.T%2)
    gain=m.matrix_gain(VV,AA.ravel(),'V4');r=row['vertex_colours'];assert all(r[u]!=(r[v]^int(z))for (u,v),z in zip(E,gain))

def test_real_clock_obstruction_is_exact(cert):
    import sympy as s
    for row in cert['binary_quadric']['cover_stabilizers']:
        M=s.Matrix(row['deck_matrix']);assert M*M+M+s.eye(4)==s.zeros(4)
        K=2*M+s.eye(4);assert K*K==-3*s.eye(4);assert (M-s.eye(4)).det()!=0
        z=s.symbols('z0:10');G=s.zeros(4)
        for a,(i,j) in zip(z,itertools.combinations_with_replacement(range(4),2)):G[i,j]=G[j,i]=a
        C,_=s.linear_eq_to_matrix(list(M.T*G*M-G),z);space=C.nullspace();assert len(space)==4
        for v in space:
            g=G.subs(dict(zip(z,v)));assert K.T*g*K==3*g and K.T*g+g*K==s.zeros(4)

def test_clock_completion_requires16sheets(cert):
    Q=cert['binary_quadric'];prior=set(map(tuple,Q['prior_clock_subgroup']))
    for row in Q['cover_stabilizers']:
        st=set(map(tuple,row['subgroup']));assert len(st)==9 and len(st&prior)==3
    for row in Q['clock_symmetry_completion']:
        assert len(row['clock_orbit'])==3 and set.intersection(*(set(k)for k in row['clock_orbit']))=={0}
        assert row['completed_binary_cover_index']==16

def test_all_native_pair_kernels_and_rank1_overlap():
    K=(m.HS[:,None]+m.HS[None,:])/2;ev=np.linalg.eigvalsh(K);compatible=np.kron(m.ADJ,np.ones((3,3),int)).astype(bool)
    assert np.all(np.sum(abs(ev[compatible])<1e-9,axis=1)==1)
    assert np.min(ev[compatible][:,1])>=.5-1e-12
    bad=~compatible&~np.eye(120,dtype=bool);delta=(1-1/np.sqrt(3))/2
    assert np.min(ev[bad])>=delta-1e-12
    contexts=m.stabilizer_contexts();P=np.array(list(contexts.values()));over=np.einsum('aij,bji->ab',P,P).real;np.fill_diagonal(over,0);assert over.max()==pytest.approx(1/3,abs=1e-12)
    a,b=np.unravel_index(np.argmax(over),over.shape);L=(2*np.eye(9)-P[a]-P[b])/2
    assert np.linalg.eigvalsh(L)[0]==pytest.approx(delta,abs=1e-12)

def test_star_parent_native_cover_and_inconsistent_star(cert):
    _,E,V,_,_=m.native_data();r=cert['binary_successful_maps'][0];edges,c=m.lifted_graph(E,V,r['coefficients'],r['vertex_colours']);d=m.star_certificate(edges,c)
    assert d['ground_energy_error']<1e-10 and d['minimum_site_gap_for_displayed_cover']>=.5
    # Locally compatible edges sharing one tick but choosing different pure contexts.
    contexts=m.stabilizer_contexts();pairs=[(C,P)for C,P in contexts.items()if 0 in C];C,P=pairs[0]
    D,Q=next((D,Q)for D,Q in pairs if np.trace(P@Q).real<.5)
    a=next(x for x in C if x!=0);b=next(x for x in D if x!=0)
    L=(m.HS[0]+m.HS[a])/2+(m.HS[0]+m.HS[b])/2
    assert np.linalg.eigvalsh(L)[0]>=(1-1/np.sqrt(3))/2-1e-12

def test_no_binary_to_real_Lorentz_or_TOE_overread(cert):
    assert 'not a real Lorentz signature' in cert['binary_quadric']['identification']
    assert 'No selection of one of6covers' in cert['boundary']
    assert 'No SWAP exchange' in cert['star_parent']['proof'][-1]

def test_explicit_affine_group_and_clock_group_nonisomorphism(cert):
    G=cert['period_affine_group'];assert G['order']==432
    assert len(G['center'])==3 and sum(G['element_orders'].values())==432
    assert '4' not in G['element_orders']
    assert G['element_orders']['2']==15
    assert 'A4 x A4' in G['faithful_period_affine_image']
    _,_,_,_,d=m.native_data();M={tuple(g['h']):np.array(g['matrix'])%2 for g in d['exact_deck_actions']}
    for a,b in itertools.product(M,repeat=2):assert np.array_equal(M[m.mul(a,b)],M[a]@M[b]%2)

def test_six_binary_pairings_have_two_parities(cert):
    G=cert['period_affine_group'];W1,W2=map(lambda w:set(map(tuple,w)),G['binary_character_planes'])
    assert len(W1)==len(W2)==4 and W1&W2=={(0,0,0,0)}
    P=G['six_GL2_pairings'];assert {tuple(x['permutation'])for x in P}==set(itertools.permutations(range(3)))
    assert sorted(x['parity']for x in P)==[0,0,0,1,1,1]
    O=cert['binary_quadric']['H27_orbits']
    for orbit in O:
        parities={x['parity']for x in P if x['kernel']in orbit};assert len(parities)==1

def test_certificate_source_fingerprint_and_frustration_boundary(cert):
    import hashlib
    assert cert['source_sha256']==hashlib.sha256((ROOT/'analysis/w33_pass12186_context_cover_holonomy.py').read_bytes()).hexdigest()
    assert 'not a spacing bound' in cert['star_parent']['gap_scope']
