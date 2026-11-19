"""Independent topology, graph, charge and interaction controls."""
from pathlib import Path
from itertools import combinations,permutations,product
import sys
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261119_balanced_source_E8_cup_gate as m


def test_sphere_Green_function_and_neutrality():
    x=s.symbols('x',real=True)
    G=(s.pi-x)*s.cot(x)/(4*s.pi**2)
    assert s.trigsimp(s.diff(G,x,2)+2*s.cot(x)*s.diff(G,x))==1/(2*s.pi**2)
    assert np.array_equal(m.Q.sum(0),np.zeros(4))
    assert np.array_equal(m.Q.sum(1),np.zeros(4))
    assert s.Matrix(m.Q).rank()==3
    assert s.limit(G,x,s.pi)==-1/(4*s.pi**2)


def test_relative_complexes_in_small_characteristics():
    chain,holes,bd=m.sphere_and_holes()
    # Include zero-residue filling, two signs, and sign reversal.
    for r in ([2,-1,0,-1],[-2,1,0,1],[1,-1,0,0],[1,1,-1,-1],[-1,-1,-1,3]):
        for prime in (2,3):
            actual=m.relative_betti(chain,holes,r,prime)
            assert actual==[0,sum(v<0 for v in r)-1,sum(v>0 for v in r)-1,0]


def test_graph_classification_by_reachability_not_modular_rank():
    arcs=list(permutations(range(4),2));found=set()
    for edges in combinations(arcs,7):
        A=np.zeros((4,4),dtype=int)
        for i,j in edges:A[i,j]=1
        if not np.array_equal(A.sum(0),A.sum(1)):continue
        reach=np.eye(4,dtype=int)+A
        for _ in range(3):reach=(reach+reach@reach>0).astype(int)
        if np.all(reach):found.add(tuple(A.ravel()))
    A=np.diag(np.diag(m.Q))-m.Q
    orbit={tuple(A[np.ix_(p,p)].ravel()) for p in permutations(range(4))}
    assert len(found)==24 and found==orbit


def test_sparse_support_is_essential_for_odd_index():
    dense=m.Q+4*np.eye(4,dtype=int)-np.ones((4,4),dtype=int)
    assert np.all(dense!=0)
    spin_index=lambda Q:sum(int(sum(Q[:,i]<0)-sum(Q[:,i]>0)) for i in range(4))
    assert spin_index(m.Q)==3 and spin_index(dense)==8
    # The change adds new source poles to charged sectors, changing domains.
    assert sum(sum(m.Q==0))==5


def test_full_E8_root_spectrum_matches_representation_census():
    sectors,fields,census=m.sector_census()
    assert [a['b1'] for a in sectors[:4]]==[1,1,1,0]
    assert all(a['b2']==0 for a in sectors[:4])
    assert sum(d for d,q,label in fields)==106
    control=m.root_and_anomaly_control(census)
    assert control['root_trace_matches_sector_anomaly_sums']
    assert census['gravitational_U1_trace']==[20,10,10]
    assert census['Spin10_squared_U1_trace_T10_1']==[2,1,1]


def test_gauge_invariance_allows_three_off_diagonal_entries():
    for i,j in combinations(range(3),2):
        kl=[k for k in range(4) if k not in (i,j)]
        assert np.array_equal(m.W[i]+m.W[j]+m.W[kl[0]]+m.W[kl[1]],np.zeros(3))
    a,b,c=s.symbols('a b c')
    assert s.Matrix([[0,a,b],[a,0,c],[b,c,0]]).det()==2*a*b*c


def test_cup_zero_survives_allowed_exact_changes():
    chain,holes,_=m.sphere_and_holes();M={t:n for t,n in chain.items() if t not in holes}
    residues=[m.Q[:,0],m.Q[:,1],m.Q[:,2]+m.Q[:,3]]  # 16_1,16_2,10_34
    assert np.all(sum(residues)==0)
    assert all(any(r[j]<0 for r in residues) for j in range(4))
    rng=np.random.default_rng(20261119)
    def integrate(fs):
        return sum(n*np.prod([fs[i][t[i+1]]-fs[i][t[i]] for i in range(3)]) for t,n in M.items())
    for _ in range(12):
        potentials=[]
        for r in residues:
            negative=[j for j in range(4) if r[j]<0]
            f=np.array([int(v in holes[negative[0]]) for v in range(30)])
            exact_change=rng.integers(-5,6,size=30)
            for j in negative:exact_change[list(holes[j])]=0
            f+=exact_change
            potentials.append(f)
        assert integrate(potentials)==0


def test_two_dimensional_Abelian_plane_is_still_anomalous():
    sectors,fields,census=m.sector_census()
    def cubic(t):return sum(d*int(np.dot(q,t))**3 for d,q,label in fields)
    for t in [(-3,5,1),(0,-1,1),(-3,1,5)]:
        assert np.dot([2,1,1],t)==0 and cubic(t)==0
    t=(0,1,-1)
    u=(-3,5,1)
    assert cubic(t)==cubic(u)==0 and cubic(np.array(t)+np.array(u))!=0
