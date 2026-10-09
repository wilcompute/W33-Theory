"""Replay the global rational-rank proof and independently check causal geometry."""
from pathlib import Path
import copy,hashlib,itertools as it,json,sys
import numpy as np
import pytest
import sympy as s
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11767_global_current_algebra as A
import w33_pass11768_lorentzian_h4_code_source as B


@pytest.fixture(scope='module')
def frozen():
    return [json.loads((ROOT/f'data/w33_pass{tag}.json').read_text()) for tag in ('11767_global_current_algebra','11768_lorentzian_h4_code_source')]


@pytest.mark.parametrize('which',[0,1])
def test_producer_and_prior_hashes(frozen,which):
    p=frozen[which];module=(A,B)[which]
    assert p['source_sha256']==hashlib.sha256(Path(module.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    for name,digest in p['inputs'].items():assert digest==hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def test_all_6240_lie_membership_and_independence_witnesses(frozen):
    p=frozen[0];rows,digest=A.replay(p['witness'])
    assert len(rows)==6240 and digest==p['replayed_basis_sha256']
    assert len({min(r) for r in rows})==6240
    assert sorted(map(tuple,p['witness']['edges']))==sorted(A.actual_edges())
    for row in rows:
        rs=np.zeros(80,dtype=int);cols=np.zeros(80,dtype=int);tr=0
        for ij,x in row.items():
            i,j=divmod(ij,80);rs[i]+=x;cols[j]+=(1 if i<40 else -1)*x
            if i==j:tr+=x
        assert np.all(rs%101==0) and np.all(cols%101==0) and tr%101==0


def test_replay_rejects_corrupt_membership_normalization(frozen):
    w=copy.deepcopy(frozen[0]['witness']);w['operations'][0][2]=2
    with pytest.raises(AssertionError):A.replay(w)


@pytest.mark.parametrize('n,edges,rank',[(4,[(0,1),(0,2),(0,3)],8),(8,[(i,(i+1)%8) for i in range(8)],34)])
def test_fork_and_cycle_have_distinct_local_lie_types(n,edges,rank):
    w=A.rank_witness(edges,n);rows,_=A.replay(w)
    assert len(rows)==rank


def test_exact_upper_bound_adapted_basis_and_global_center():
    n=80;u=s.ones(n,1);sign=s.Matrix([1]*40+[-1]*40)
    cols=[u]
    for j in range(78):
        v=s.zeros(n,1);v[j]=1;v[79]=sign[j];cols.append(v)
    cols.append(s.eye(n)[:,79]);T=s.Matrix.hstack(*cols)
    assert abs(T.det())==1 and sign.T*u==s.zeros(1)
    assert (78**2-1)+2*78+1==6240
    center=np.ones((80,1),dtype=int)@np.array(sign.T,dtype=int)
    assert np.array_equal(center@center,np.zeros((80,80),dtype=int))
    for i,j in A.actual_edges():
        g=np.zeros((80,80),int);g[i,i]=g[j,i]=1;g[i,j]=g[j,j]=-1
        assert not np.any(g@center-center@g)
    assert (s.Matrix([[1,1,0],[1,0,1],[0,1,1]])).det()!=0 # c1=-c2=-c3 cycle forces zero.


def test_configuration_form_obstruction_does_not_lose_canonical_symplectic_form():
    # The78D configuration quotient lacks an invariant alternating form;
    # T*R80 still has the usual canonical form, for every matrix A.
    omega=np.block([[np.zeros((80,80),int),np.eye(80,dtype=int)],[-np.eye(80,dtype=int),np.zeros((80,80),int)]])
    for i,j in A.actual_edges()[::29]:
        g=np.zeros((80,80),int);g[i,i]=g[j,i]=1;g[i,j]=g[j,j]=-1
        lift=np.block([[g,np.zeros((80,80),int)],[np.zeros((80,80),int),-g.T]])
        assert not np.any(lift.T@omega+omega@lift)


def test_symbolic_product_congruence_for_all_four_staircase_types(frozen):
    a,tau=s.symbols('a tau',positive=True)
    base=s.diag(-tau**2,1,1,1);base[1:4,1:4]=a*a*(s.eye(3)+s.ones(3))/2
    for item in frozen[1]['Lorentzian_slab']['exact_Gram_types']:
        change=s.Matrix(item['product_basis']);G=change.T*base*change
        assert s.factor(G.det())==-a**6*tau**2/2
        assert G.subs({a:1,tau:s.Rational(1,2)})==s.Matrix(item['Gram'])
        assert abs(change.det())==1


def test_actual_2400_simplex_metrics_and_global_time_independently(frozen):
    graph,tets,simplices=B.native_slab();counts={}
    for simplex in simplices:
        # Build by local product coordinate vectors instead of lengths.
        sites=sorted({x%120 for x in simplex});positions={v:np.eye(3)[k-1] if k else np.zeros(3) for k,v in enumerate(sites)}
        coords=np.array([[v//120,*positions[v%120]] for v in simplex])
        base=np.zeros((4,4));base[0,0]=-.25;base[1:,1:]=(np.eye(3)+np.ones((3,3)))/2
        change=(coords[1:]-coords[0]).T;G=change.T@base@change
        assert np.linalg.eigvalsh(G)[0]<0 and np.linalg.eigvalsh(G)[1]>0
        assert np.allclose(G,np.array(B.simplex_gram(simplex),float))
        dt=(coords[1:,0]-coords[0,0])/2
        assert np.isclose(dt@np.linalg.solve(G,dt),-1)
        for edge in it.combinations(simplex,2):counts[tuple(sorted(edge))]=B.squared_length_quarters(*edge)
    assert len(simplices)==2400 and len(counts)==2280
    assert sum(v<0 for v in counts.values())==120
    assert frozen[1]['Lorentzian_slab']['timelike_deficit_max_error']<1e-12


def test_lapse_and_scale_no_go_is_only_reduced_stationarity(frozen):
    a,tau,L,d=s.symbols('a tau L d',positive=True)
    S=tau*(720*a*d-50*s.sqrt(2)*L*a**3)
    lapse=s.solve(s.diff(S,tau),L)[0];scale=s.solve(s.diff(S,a),L)[0]
    assert s.simplify(lapse/scale)==3
    p=frozen[1]['Lorentzian_slab']
    assert p['no_simultaneous_static_scale_and_lapse_stationarity']
    assert 'fixed boundary' in p['boundary_variation_scope']


def test_conditional_ADM_source_constraint_and_instability(frozen):
    a,v,acc,N,L,d,m,E=s.symbols('a v acc N L d m E',positive=True)
    D=50*s.sqrt(2);Bv=3*D;C=720*d
    lag=-Bv*a*v*v/N+N*(C*a-D*L*a**3-m*E)
    constraint=s.diff(lag,N).subs(N,1)
    # EL at proper time: d/dt(dL/dv)-dL/da, with constant lapse.
    euler=(s.diff(s.diff(lag,v),a)*v+s.diff(s.diff(lag,v),v)*acc-s.diff(lag,a)).subs(N,1)
    v2=s.solve(constraint,v*v)[0]
    acceleration=s.simplify(s.solve(euler,acc)[0].subs(v*v,v2))
    assert s.simplify(acceleration-(L*a/3-m*E/(2*Bv*a*a)))==0
    astar=3*m*E/(2*C);lstar=C/(3*D*astar**2)
    assert s.simplify(constraint.subs(v,0).subs({a:astar,L:lstar},simultaneous=True))==0
    assert s.simplify(s.diff(acceleration,a).subs({a:astar,L:lstar},simultaneous=True)-lstar)==0
    p=frozen[1]['conditional_ADM_code_source']
    assert not p['static_excited_solution_stable'] and p['code_lowest_excitation_energy']==4
    assert 'supplied' in p['normalization_boundary'].lower()


@pytest.mark.parametrize('power',[0,1,3])
def test_ordinary_spectral_scalings_all_leave_static_instability(frozen,power):
    a,v,N,L,C,D,m,E=s.symbols('a v N L C D m E',positive=True);Bv=3*D
    energy=m*E*a**(-power)
    lag=-Bv*a*v*v/N+N*(C*a-D*L*a**3-energy)
    replacement={L:(power+1)*C/((power+3)*D*a*a),m:2*C*a**(power+1)/((power+3)*E)}
    assert s.simplify(s.diff(lag,N).subs({N:1,v:0}).subs(replacement,simultaneous=True))==0
    assert s.simplify(s.diff(lag,a).subs({N:1,v:0}).subs(replacement,simultaneous=True))==0
    acceleration=L*a/3-(power+1)*energy/(2*Bv*a*a)
    growth=s.simplify(s.diff(acceleration,a).subs(replacement,simultaneous=True))
    assert s.simplify(growth-(power+1)*C/(Bv*a*a))==0 and growth.is_positive
    assert frozen[1]['conditional_ADM_code_source']['power_law_extension']['all_p_greater_than_minus_one_unstable']
