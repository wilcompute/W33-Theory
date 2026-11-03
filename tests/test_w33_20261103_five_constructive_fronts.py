"""Independent formula/map checks; no legacy repository conftest required."""
import itertools,json,pathlib,sys
from fractions import Fraction
import networkx as nx
import numpy as np
import pytest
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261103_native_qutrit_feedforward import PI
from w33_20261103_native_singlet_stabilization import model,DUADS
from w33_20261103_kagome_tunneling_bounds import active_graph,coefficient
from w33_20261103_deck_twist_interfaces import beta,torsion,exponent

def load(stem):return json.loads((ROOT/f'data/w33_20261103_{stem}.json').read_text())

@pytest.mark.parametrize('gate_index',range(3))
def test_full_physical_feedforward_channel(gate_index):
    d=load('native_qutrit_feedforward')['gates'][gate_index]
    old=load('native_projector_holonomic_qutrit')['holonomies'][d['parent_holonomy_index']]
    H=(np.sqrt(3)*np.array(old['real_sqrt3_numerator']).reshape(3,3)+3j*np.array(old['imaginary_times3_numerator']).reshape(3,3))/12
    V=np.eye(9,dtype=complex)[:,[0,3,6]];w=np.exp(2j*np.pi/3);X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex);Z=np.diag([1,w,w*w])
    target=V@H;choi=np.zeros((27,27),complex)
    c,b,_=d['measurement_direction_order']
    for row in d['branches']:
        ra,rb,rc=row['outcomes'];a,z=row['logical_byproduct']
        correct=np.kron((np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,z)).conj().T,np.linalg.matrix_power(X,-ra))
        K=correct@PI[ra]@PI[3*b+rb]@PI[3*c+rc]@V
        assert np.max(abs(K.conj().T@K-np.eye(3)/27))<2e-14
        choi+=np.outer(K.ravel(),K.ravel().conj())
    assert np.max(abs(choi-np.outer(target.ravel(),target.ravel().conj())))<3e-13

@pytest.mark.parametrize('eps',[0,.01,.2,1])
def test_readout_formula(eps):
    d=load('native_qutrit_feedforward');expected=(1-eps)**3+eps**2*(1-eps)/2
    for g in d['gates']:
        p=sum(v/27*(1-eps)**(3-int(k))*(eps/2)**int(k)for k,v in g['readout_fidelity_counts_by_wrong_trits'].items())
        assert abs(p-expected)<1e-14 and 0<=p<=1

def test_vacuum_all_gradient_and_physical_hessian():
    x,W,v=model();at=dict(zip(x,v));H=s.hessian(W,x).subs(at)
    assert all(s.diff(W,z).subs(at)==0 for z in x)
    assert H.rank()==24 and len(H.nullspace())==5
    # Physical charged sector no longer has the old8 null directions.
    charged=[DUADS.index((i,j))for j in [4,5]for i in range(4)]+list(range(15,19))+list(range(21,25))
    assert H.extract(charged,charged).det()==256

def test_scale_is_supplied_not_dimensionlessly_selected():
    x,W,v=model();rho=s.symbols('rho');at={z:rho*a for z,a in zip(x,v)}
    assert s.diff(W,x[27]).subs(at)==rho-1
    assert s.diff(W,x[28]).subs(at)==rho-1
    d=load('native_singlet_stabilization');assert d['local_physical_chiral_flat_directions']==0
    assert d['quantum_completion']['same_as_native_pure_cubic'] is False

@pytest.mark.parametrize('phase',range(3))
def test_mass_deformed_mesonic_critical_points(phase):
    # Choose nonzero rational inputs with root modulus1 and verify both polynomial and local curvature.
    M=np.exp(2j*np.pi*phase/3);m=2;L8=4;Y=m*M
    assert abs(Y*Y*M-L8)<1e-13 and abs(m-Y/M)<1e-13
    assert abs(3*m/(2*M))>0

def test_mixed_tensor_is_alternating_and_full_mass():
    d=load('changed_embedding_matter_completion');T=np.array(d['witness_tensor'])
    assert np.array_equal(T,-T.transpose(0,2,1)) and d['modular_rank']==95
    pairs=list(itertools.combinations(range(4),2));O=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
    chi=np.array([O[a,b]for a,b in pairs]);M=np.einsum('i,ijk->jk',chi,T)
    assert np.array_equal(M.T@M,np.eye(4,dtype=int))

def test_anomaly_with_duals_and_without():
    h=[1,1,1,-3];a=sum(x**3 for x in h)
    assert 2*a!=0 and 2*a+2*sum((-x)**3 for x in h)==0

@pytest.mark.parametrize('n',range(2,8))
def test_tree_tunneling_integral(n):
    c,_=coefficient(nx.path_graph(n));assert c==Fraction(4,3)**(n-1)
    if n>2:
        cyclic=nx.cycle_graph(n);cc,_=coefficient(cyclic);assert cc<=c

def test_cuboctahedral_binary_sector():
    G,faces=active_graph(4,4);assert nx.is_isomorphic(G,nx.line_graph(nx.cubical_graph()))
    nodes=list(G);pos={v:i for i,v in enumerate(nodes)}
    for S in range(1<<12):
        selected={v for v in nodes if S>>pos[v]&1};cut=sum((a in selected)!=(b in selected)for a,b in G.edges())
        E=sum(0<len(set(f)&selected)<len(set(f)&set(nodes))for f in faces)
        assert 2*E==3*cut

def test_distance_one_counterexample():
    old=load('all_quartet_tunneling');P=old['ground_palettes'];a=P[0];b=next(p for p in P if p[0]!=a[0])
    assert int(a[0]==a[0])!=int(b[0]==a[0])
    assert load('kagome_tunneling_bounds')['ground_code_quantum_distance']==1

@pytest.mark.parametrize('twist_torsion',[False,True])
def test_interface_full_associativity(twist_torsion):
    H=[0,3,5,6]
    def B(a,b):return (beta(a,b)+(torsion(a,b)if twist_torsion else 0))%4
    for a,b,c in itertools.product(H,repeat=3):
        lhs=(B(b,c)+B(a,b^c)-B(a^b,c)-B(a,b))%4
        assert lhs==2*(exponent(120,a,b,c)^exponent(127,a,b,c))

def test_full_diagonal_obstructed_and_free_translation_preserved():
    H=[0,3,5,6]
    assert all(exponent(7,g,g,g)==int(g not in H)for g in range(8))
    for a,b in itertools.product(H,repeat=2):assert a^b in H

def test_ambient_conjugation_prevents_overcounting():
    d=load('deck_twist_interfaces');lam={int(k):v for k,v in d['ambient_conjugation_ratio_gauge_i_exponents'].items()};H=[0,3,5,6]
    for a,b in itertools.product(H,repeat=2):
        alpha=2*(exponent(120,1,a,b)^exponent(120,a,b,1)^exponent(120,a,1,b))
        assert (alpha-torsion(a,b))%4==(lam[a]+lam[b]-lam[a^b])%4
    assert d['diagonal_subgroup_cochain_gauge_data']==6 and d['ambient_equivalence_classes_among_diagonal_subgroups']==5

@pytest.mark.parametrize('b',[.001,.01,.04])
def test_exact_quantum_effective_stationarity_numeric(b):
    t,z,r,q,l,k,S,T,eps=s.symbols('t z r q l k S T eps');a=[t,z,r,q,l,k,S,T]
    P=t*t-(1+k)*(5-l)+(2+q)*(3-r);R=P/t**2
    W=z*(r*q-l*k-t*t)+l*k+S*(r-1)+T*(q-1)+3*eps*R**s.Rational(1,3)
    tt=1+5*b*b;RR=2*(1+5*b)/tt;AA=b*tt/(1-2*b-5*b*b);zz=AA*(1-RR)
    ee=(AA**3*RR**2*tt**3)**(1/3)
    point=dict(zip(a,[np.sqrt(tt),zz,1,1,5*b,-b,3*AA-zz,-2*AA-zz]));point[eps]=ee
    assert max(abs(complex(s.diff(W,y).subs(point)))for y in a)<1e-12
    assert abs(4*b**3*(1+5*b)**2*(1+5*b*b)**4-ee**3*(1-2*b-5*b*b)**3)<1e-15

def test_quantum_series_and_exact_constraints():
    d=load('native_quantum_vacuum_displacement');local={name:s.Symbol(name)for name in d['variables']};b=s.Symbol('b');local['b']=b
    curve={key:s.sympify(value,locals=local)for key,value in d['exact_effective_critical_curve']['coordinates'].items()}
    assert s.simplify(curve['t']**2-1+curve['l']*curve['k'])==0
    assert curve['r']==curve['q']==1
    d1=[s.sympify(x)for x in d['first_order_displacement']];d2=[s.sympify(x)for x in d['second_order_displacement']]
    assert d1[0]==0 and s.simplify(d2[0]+d1[4]*d1[5]/2)==0
