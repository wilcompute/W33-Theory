"""Independent physical gates, covariance and Gauss moves for11970-11974."""
from pathlib import Path
import json
import sys
import numpy as np
import sympy as sp
from scipy.linalg import eigvalsh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11970_native_wilson_dirac import construction,operators,Hamiltonian
from w33_pass11971_frustrated_family_vacuum import residuals
from w33_pass11972_native_tetrahedron_link_audit import colouring
from w33_pass11974_coupled_patch_matter import Patch


def certificate(n):
    names={11970:'native_wilson_dirac',11971:'frustrated_family_vacuum',
           11972:'native_tetrahedron_link_audit',11973:'mediation_transmission',
           11974:'coupled_patch_matter'}
    return json.loads((ROOT/'data'/f'w33_pass{n}_{names[n]}.json').read_text())


def test_native_dirac_current_normalizes_actual_deck():
    ed,volts,J,*_=construction();B=np.zeros((160,80))
    for e,(a,b) in enumerate(ed):B[e,a]=-1;B[e,b]=1
    assert np.max(abs(B.T@J))<1e-12
    assert np.max(abs(J.T@volts-80*np.eye(3)))<1e-12


def test_native_dirac_uniform_spinors_and_independent_directions():
    u=np.ones(80)/np.sqrt(80);K,L=operators([0,0,0])
    assert max(np.linalg.norm(x@u) for x in [L,*K])<1e-12
    assert sum(abs(eigvalsh(Hamiltonian([0,0,0])))<1e-10)==4
    for p in ([.3,.7,-.2],[-.8,.1,.5]):
        p=np.array(p);p/=np.linalg.norm(p)
        ev=eigvalsh(Hamiltonian(.001*p));low=np.sort(ev[np.argsort(abs(ev))[:4]])/.001
        assert np.max(abs(low-[-1,-1,1,1]))<1e-4


def test_schur_zero_argument_requires_positive_wilson_coefficient():
    # Independent block equation at a nonnative random positive L with
    # noncommuting S: anticommutativity assumptions are unnecessary.
    rng=np.random.default_rng(19370);x=rng.normal(size=(7,7));L=x.T@x+np.eye(7)
    S=rng.normal(size=(7,7));S=(S+S.T)/2
    H=np.block([[L,S],[S,-L]])
    assert min(abs(np.linalg.eigvalsh(H)))>=min(np.linalg.eigvalsh(L))-1e-12


def test_family_global_zero_and_unfitted_mixing():
    A=np.diag([1,2,4]).astype(complex);B=np.array([[3,1,-1j],[1,4,1],[1j,1,5]])
    assert np.max(abs(residuals(A,B)))==0
    assert abs(np.trace(np.linalg.matrix_power(A@B-B@A,3)).imag)==36
    d=certificate(11971)
    assert min(d['positive_normal_Hessian_eigenvalues'])>0
    assert d['unfitted_CKM_angles_deg'][2]>20
    for direction in (np.diag([1.,0,0]),np.array([[0,0,1],[0,0,0],[1,0,0]])):
        assert np.linalg.norm(residuals(A,B+1e-3*direction))>0


def test_family_basis_and_CP_control():
    A=np.diag([1,2,4]).astype(complex);B=np.array([[3,1,-1j],[1,4,1],[1j,1,5]])
    w=np.exp(2j*np.pi/3);R=np.array([[w**(i*j) for j in range(3)] for i in range(3)])/np.sqrt(3)
    assert np.max(abs(residuals(R@A@R.conj().T,R@B@R.conj().T)))<1e-12
    assert np.max(abs(residuals(A,B.conjugate())))==0
    assert np.trace(np.linalg.matrix_power(A@B.conjugate()-B.conjugate()@A,3)).imag==-36


def test_native_girth_independent_BFS():
    edges,_=colouring(17);adj=[[] for _ in range(80)]
    for e,(a,b) in enumerate(edges):adj[a].append((b,e));adj[b].append((a,e))
    girth=80
    for omit,(a,b) in enumerate(edges):
        seen={a:0};queue=[a]
        for u in queue:
            for v,e in adj[u]:
                if e==omit or v in seen:continue
                seen[v]=seen[u]+1;queue.append(v)
        girth=min(girth,seen[b]+1)
    assert girth==8


def test_all_colouring_link_identity_and_scope():
    d=certificate(11972)
    for row in d['witnesses']:
        V,E,F,T=row['primal_f_vector']
        assert F==160 and T==80 and E<=60 and V>=4
        assert V-E+F-T==sum(x['genus'] for x in row['links'])>=24
        assert all(x['Euler']==2-2*x['genus'] for x in row['links'])
    assert 'Only this specified' in d['scope']


def test_actual_higgsed_mediation_decouples():
    d=certificate(11973)
    for delta,f in zip(d['delta'],d['suppression_f']):
        assert abs(f/(2*(np.log(delta)-1)/delta)-1)<1e-12
    assert min(d['hidden_vector_masses_GeV'])>1e14
    assert max(d['soft_masses_GeV'])<2e-5
    assert d['F_over_M_squared']<.1
    assert abs(d['predicted_radial_shift_numeric'])<1e-8
    assert d['massless_Z_only_negative_control']['critical_unit_Z_soft_GeV']>.03


def test_patch_exact_chord_hop_and_plaquette_gauss():
    c=Patch();bits=sum(1<<i for i in range(c.n) if c.background[i]);l=(1,-1)
    ext=np.zeros(c.n,int);n=c.flux(bits,l,ext)
    for e,(a,b) in enumerate(c.edges):
        oa,ob=(bits>>a)&1,(bits>>b)&1
        if oa==ob:continue
        direction=1 if oa else -1;new=list(l)
        if e in c.chords:new[c.chords.index(e)]-=direction
        delta=c.flux(bits^(1<<a)^(1<<b),new,ext)-n
        expected=np.zeros(c.m,int);expected[e]=-direction
        assert np.array_equal(delta,expected)
    for p in c.P:
        assert np.array_equal(c.flux(bits,np.array(l)+p[c.chords],ext)-n,p)


def test_patch_variational_convergence_and_density_response():
    d=certificate(11974);rows=d['sectors']
    assert d['patch_sites']==11 and d['patch_links']==12
    for kind in ('neutral','charged'):
        assert all(rows[i+1][kind]['E0']<rows[i][kind]['E0'] for i in range(2))
        assert rows[-1][kind]['ground_residual']<1e-7
        assert rows[-1][kind]['boundary_probability']<3e-5
    assert max(abs(x) for x in rows[-1]['induced_density'])>.01
    assert abs(sum(rows[-1]['induced_density']))<1e-10
    assert abs(rows[-1]['static_pair_energy']-rows[-2]['static_pair_energy'])<1e-4
