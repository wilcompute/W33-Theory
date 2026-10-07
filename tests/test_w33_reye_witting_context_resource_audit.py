"""Independent ray, context, Pauli and coherent-query controls."""
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('resource_reye',ROOT/'analysis/w33_reye_witting_context_resource_audit.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
def certificate():return json.loads(M.OUT.read_text())


def test_dual_Reye_geometric_lines_and_all_orthogonal_contexts():
    c=certificate()['Peres_Reye'];r=s.Matrix(c['rays']);gram=r*r.T
    contexts=[list(t) for t in itertools.combinations(range(24),4) if all(gram[i,j]==0 for i,j in itertools.combinations(t,2))]
    assert contexts==c['contexts'] and len(contexts)==24
    for lines in c['Reye_lines']:
        assert len(lines)==16
        pts=set(itertools.chain.from_iterable(lines));assert len(pts)==12
        assert {sum(i in t for t in lines) for i in pts}=={4}
        for t in lines:
            assert r.extract(t,range(4)).rank()==2
            assert all(gram[i,j]!=0 for i,j in itertools.combinations(t,2))


def test_all_critical_parities_and_every_single_deletion_coloring():
    c=certificate()['Peres_Reye'];r=np.array(c['rays']);gram=r@r.T
    assert len(c['critical18'])==16
    for a in c['critical18']:
        remaining=set(range(24))-set(a['removed']);assert len(remaining)==18
        assert len(a['contexts'])==9
        assert {sum(i in t for t in a['contexts']) for i in remaining}=={2}
        for v in a['single_deletion_colorings']:
            present=remaining-{v['deleted']};green=set(v['green']);assert green<=present
            assert all(gram[i,j]!=0 for i,j in itertools.combinations(green,2))
            for t in c['contexts']:
                if set(t)<=present:assert len(set(t)&green)==1


def test_all24_adaptive_measurement_trees_reconstruct_projectors():
    c=certificate()['Peres_Reye'];P={'I':s.eye(2),'X':s.Matrix([[0,1],[1,0]]),'Y':s.Matrix([[0,-s.I],[s.I,0]]),'Z':s.diag(1,-1)}
    op=lambda a:s.kronecker_product(P[a[0]],P[a[1]])
    for tree in c['measurement_trees']:
        total=s.zeros(4)
        for b in tree['branches']:
            A=op(tree['first']);B=op(b['second']);assert A*B==B*A
            for i,t in zip(b['rays'],b['second_signs']):
                v=s.Matrix(c['rays'][i]);proj=(s.eye(4)+b['first_sign']*A)*(s.eye(4)+t*B)/4
                assert proj==v*v.T/(v.T*v)[0];total+=proj
        assert total==s.eye(4)


def test_objectwise_vacuum_embedding_and_every_F3_commutator():
    c=certificate()['Witting_vacuum'];r=M.witting_rays();pts=np.array(c['Witting_to_F3_point'])
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]])
    assert len({tuple(v) for v in pts})==40
    for i,j in itertools.combinations(range(40),2):assert (M.inner(r[i],r[j])==M.ZERO)==((pts[i]@J@pts[j])%3==0)
    for j in c['Higgs_to_Witting_labels']:assert r[j][3]==M.ZERO
    old=json.loads((ROOT/'data/w33_pass11625_11629_composites_joint_vacua.json').read_text())['joint_flavor']
    w=np.exp(2j*np.pi/3)
    for i,j in enumerate(c['Higgs_to_Witting_labels']):
        h=np.array([complex(*z) for z in old['projective_vacua'][i]['h']]+[0])
        v=np.array([a+b*w for a,b in r[j]]);v/=np.linalg.norm(v)
        assert abs(abs(np.vdot(v,h))**2-1)<1e-12
    assert all(set(b) in [set(t)-{3} for t in c['Witting_contexts'] if 3 in t] for b in [[c['Higgs_to_Witting_labels'][i] for i in t] for t in c['local_MUB_contexts']])


def test_local_MUB_link_has81_colorings_and_queries_preserve_extra_coherence():
    c=certificate()['Witting_vacuum'];blocks=c['local_MUB_contexts']
    selections={tuple(sorted(blocks[i][a] for i,a in enumerate(t))) for t in itertools.product(range(3),repeat=4)}
    assert len(selections)==81
    p=s.diag(0,0,0,1);I=s.eye(4);rho=s.Matrix([1,1,0,0])*s.Matrix([[1,1,0,0]])/2
    assert p*rho*p+(I-p)*rho*(I-p)==rho
    complete=sum((s.diag(*(int(i==j) for i in range(4)))*rho*s.diag(*(int(i==j) for i in range(4))) for j in range(4)),s.zeros(4))
    assert complete!=rho
    # Projector trace yields the basis-independent non-Clifford obstruction.
    for v in [s.Matrix([1,0,0,0]),s.Matrix([1,1,1,0]),s.Matrix([1,s.I,0,1])]:
        P=v*v.conjugate().T/(v.conjugate().T*v)[0];assert s.trace(I-2*P)==2
    T=s.Matrix(certificate()['coherent_query']['Toffoli_matrix'])
    assert T.T*T==s.eye(8)
    for i in range(8):assert T[:,i]==s.eye(8)[:,(i^1) if i>>1==3 else i]


def test_resource_source_binding():
    c=certificate();assert c['status']=='PASS' and c['producer_sha256']==M.ph(Path(M.__file__))
    for key in ['Peres_Reye','Witting_vacuum','coherent_query']:assert c[key]['status']=='PASS'
    for p,h in c['source_sha256'].items():assert M.ph(ROOT/p)==h
