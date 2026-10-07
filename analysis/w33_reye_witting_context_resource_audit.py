"""User literature leads: Aravind2000, Vlasov2503.18431; scoped resource audit.

Peres24-ray/Reye KS and the Witting coordinates are literature, not new.
4963 owns the exact Witting-to-W33 point graph;11262/1089 own MUB/Hesse;
BT1408/1411 own communications/analyzers. Here the11627 joint-vacuum link
is made objectwise and measurement contextuality is separated from coherent
rank-one queries. No claimed derived hardware or TOE.
"""
import itertools
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass4963_witting_pancharatnam_w33_reaudit import witting_rays,inner,ZERO,numeric_rays,canon3
from w33_pass11615_11619_parent_pairs_constraints import ph
OUT=ROOT/'data/w33_reye_witting_context_resource_audit.json'


def peres_rays():
    a=[tuple(2*int(i==j) for i in range(4)) for j in range(4)]
    a +=[tuple(z)+(1,) for z in itertools.product([-1,1],repeat=3)]
    b=[]
    for i,j in itertools.combinations(range(4),2):
        for sign in [-1,1]:
            v=[0]*4;v[i]=1;v[j]=sign;b.append(tuple(v))
    return a+b


def ray_contexts(rays):
    G=nx.Graph();G.add_nodes_from(range(len(rays)))
    for i,j in itertools.combinations(range(len(rays)),2):
        if sum(a*b for a,b in zip(rays[i],rays[j]))==0:G.add_edge(i,j)
    return G,sorted(tuple(sorted(t)) for t in nx.find_cliques(G) if len(t)==4)


def reye_lines(rays,labels):
    return [t for t in itertools.combinations(labels,3) if s.Matrix([rays[i] for i in t]).rank()==2]


def coloring(G,contexts,present):
    present=set(present);full=[set(c) for c in contexts if set(c)<=present]
    def search(green,excluded):
        remaining=[c for c in full if not c&green]
        if not remaining:return sorted(green)
        options=min((c-excluded for c in remaining),key=len)
        for i in sorted(options):
            result=search(green|{i},excluded|{i}|set(G.neighbors(i)))
            if result is not None:return result
        return None
    return search(set(),set(G)-present)


def peres_audit():
    rays=peres_rays();G,bases=ray_contexts(rays)
    assert len(bases)==24 and set(dict(G.degree()).values())=={9}
    halves=[range(12),range(12,24)];lines=[reye_lines(rays,a) for a in halves]
    assert [len(a) for a in lines]==[16,16]
    critical=[]
    for line in lines[0]:
        mate=tuple(j for j in halves[1] if all(sum(a*b for a,b in zip(rays[i],rays[j]))==0 for i in line))
        assert mate in lines[1]
        removed=set(line+mate);keep=set(range(24))-removed;contexts=[b for b in bases if not set(b)&removed]
        assert len(contexts)==9 and {sum(i in b for b in contexts) for i in keep}=={2}
        assert coloring(G,bases,keep) is None
        deletion=[]
        for i in sorted(keep):
            green=coloring(G,bases,keep-{i});assert green is not None
            deletion.append(dict(deleted=i,green=green))
        critical.append(dict(removed=sorted(removed),contexts=contexts,single_deletion_colorings=deletion))
    # All rays and all contexts admit explicit stabilizer measurement trees.
    alphabet={'I':s.eye(2),'X':s.Matrix([[0,1],[1,0]]),'Y':s.Matrix([[0,-s.I],[s.I,0]]),'Z':s.diag(1,-1)}
    paulis={a+b:s.kronecker_product(alphabet[a],alphabet[b]) for a,b in itertools.product(alphabet,repeat=2) if a+b!='II'}
    vectors=[s.Matrix(v) for v in rays]
    def eigen(P,v):
        if P*v==v:return 1
        if P*v==-v:return -1
        return None
    eig={label:[eigen(P,v) for v in vectors] for label,P in paulis.items()}
    assert all(sum(eig[label][i] is not None for label in paulis)==3 for i in range(24))
    trees=[]
    for b in bases:
        Pname=next(label for label in paulis if all(eig[label][i] is not None for i in b) and sum(eig[label][i]==1 for i in b)==2)
        P=paulis[Pname];branches=[]
        for sign in [-1,1]:
            pair=[i for i in b if eig[Pname][i]==sign]
            Qname=next(label for label,Q in paulis.items() if P*Q==Q*P and all(eig[label][i] is not None for i in pair) and eig[label][pair[0]]==-eig[label][pair[1]])
            Q=paulis[Qname]
            for i in pair:
                v=vectors[i];assert (s.eye(4)+sign*P)*(s.eye(4)+eig[Qname][i]*Q)/4==v*v.T/(v.T*v)[0]
            branches.append(dict(first_sign=sign,second=Qname,rays=pair,second_signs=[eig[Qname][i] for i in pair]))
        trees.append(dict(context=b,first=Pname,branches=branches))
    return dict(status='PASS',prior='Aravind2000/Peres1991: two geometric Reye configurations and16 critical18-ray/9-context parity proofs. No claim of new KS proof.',rays=rays,contexts=bases,Reye_lines=lines,
      critical18=critical,parity='Each selected9 contexts requires one green; all18 rays occur twice, so the count cannot be both odd andeven. All17-ray single deletions have stored colorings, including orthogonal-pair constraints.',
      measurement_trees=trees,stabilizer_rays=24,adaptive_Pauli_contexts=24,
      computational_boundary='Every Peres ray is a two-qubit stabilizer ray andevery context has an exact adaptive Pauli analyzer. These destructive measurements/preparations with Clifford controls remain in the stabilizer model. A KS contradiction alone does not supply a non-Clifford coherent gate. The sign-vs-selection separation inw33_doily_mermin.py is related prior work; its historical CF=1/10 wording is not imported.')


def witting_vacuum_audit():
    rays=witting_rays();G=nx.Graph();G.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if inner(rays[i],rays[j])==ZERO:G.add_edge(i,j)
    assert G.number_of_edges()==240 and set(dict(G.degree()).values())=={12}
    assert {len(set(G[i])&set(G[j])) for i,j in G.edges()}=={2}
    assert {len(set(G[i])&set(G[j])) for i,j in itertools.combinations(range(40),2) if not G.has_edge(i,j)}=={4}
    numeric=np.array(numeric_rays());numeric/=np.linalg.norm(numeric,axis=1)[:,None]
    vac=json.loads((ROOT/'data/w33_pass11625_11629_composites_joint_vacua.json').read_text())['joint_flavor']
    hs=np.array([np.array([complex(*z) for z in v['h']]) for v in vac['projective_vacua']]);lift=np.column_stack([hs,np.zeros(12)])
    overlap=abs(numeric.conj()@lift.T)**2;mapping=[int(i) for i in np.argmax(overlap,axis=0)]
    assert len(set(mapping))==12 and max(abs(overlap[mapping,range(12)]-1))<1e-12
    assert set(mapping)==set(G[3])
    basis=sorted(tuple(sorted(c)) for c in nx.find_cliques(G) if len(c)==4);assert len(basis)==40
    local=[tuple(mapping.index(i) for i in b if i!=3) for b in basis if 3 in b]
    assert len(local)==4 and all(len(b)==3 for b in local)
    # Existing4963 graph map, now exported for this actual vacuum embedding.
    pts=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],int)
    W=nx.Graph();W.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if (np.array(pts[i])@J@np.array(pts[j]))%3==0:W.add_edge(i,j)
    iso=next(nx.algorithms.isomorphism.GraphMatcher(G,W).isomorphisms_iter())
    for i,j in itertools.combinations(range(40),2):assert G.has_edge(i,j)==W.has_edge(iso[i],iso[j])
    # Local12 MUB rays only: one of3 outcomes in each of4 disjoint bases.
    colors=list(itertools.product(range(3),repeat=4));assert len(colors)==81
    return dict(status='PASS',prior='Vlasov2503.18431 Eq2 and3D-MUB blocks;4963 proves this graph is the W33 POINT graph.11262/1089 own the MUB/dual-Hesse object.',
      embedding='h->(h0,h1,h2,0) is a complex isometry fromC3 intoC4. Its12 joint-vacuum Higgs rays are exactly the neighbors of Witting raye3.',
      Higgs_to_Witting_labels=mapping,local_MUB_contexts=local,Witting_contexts=basis,SRG=[40,12,2,4],
      Witting_to_F3_point=[list(pts[iso[i]]) for i in range(40)],central_point=list(pts[iso[3]]),
      local_colorings=81,local_boundary='The12-ray link alone hasfour disjoint orthogonal triples andis KS-colorable. Noncolorability needs the complete overlapping40-tetrad configuration. The Pauli graph map identifies projective operator classes[v]={v,-v} inF3^4; ququart rank-one projectors live inC4 whereas two-qutrit operators act inC9. It is a graph/incidence map, not a unitary between those Hilbert spaces.',
      communications_scope='BT1408 already separates13/40 delayed-state agreement,1/40 random-basis agreement, exact36/40 approximate marking ceiling andcontextual fraction1. Those numerical distinctions are not re-derived or altered here. Cryptographic security is not proved.')


def coherent_query_audit():
    I=s.eye(4);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
    p=s.diag(0,0,0,1);T=s.kronecker_product(p,X)+s.kronecker_product(I-p,s.eye(2))
    expected=s.eye(8);expected[6,6]=expected[7,7]=0;expected[6,7]=expected[7,6]=1
    assert T==expected and T*s.kronecker_product(I,Z)*T.T==s.kronecker_product(I-2*p,Z)
    # Trace obstruction applies to every rank-one projector, independent ofbasis.
    assert s.trace(I-2*p)==2
    # Binary Lüders query retains coherence in the three-dimensional complement.
    v=s.Matrix([1,1,0,0])/s.sqrt(2);rho=v*v.T
    assert p*rho*p+(I-p)*rho*(I-p)==rho
    return dict(status='PASS',source='Vlasov2503.18431 Eq7 explicitly gives this coherent delayed query andits computational-ray Toffoli example.',
      query='T_P=P tensorX+(I-P) tensorI for rank-one P ontheququart. It is a supplied data/ancilla coupling, not implied bythe40-ray graph.',
      Toffoli_matrix=[[int(z) for z in row] for row in T.tolist()],
      exact_non_Clifford_proof='T_P(I tensorZ)T_P†=(I-2P) tensorZ. Tr(I-2P)=2, while any nonidentity two-qubit Pauli hastrace0 andidentity hastrace+/-4. Thus no rank-one ququart query is a Clifford gate inthefixed two-qubit-plus-ancilla encoding. This uses exact projector rank, not overlap tolerances.',
      universality='If coherent computational-ray T_P is available on arbitrary inputs together with Clifford control, it supplies Toffoli. The standard Toffoli/Hadamard universality theorem then applies with its ancillary/rebit conventions; Clifford phase control supplies complex phase operations. This is conditional on actual coherent gate availability, not a claim that contextuality or destructive measurements implement it.',
      measurement_boundary='Separate computational Z measurements reveal extra information anderase complement coherences, so they are not the same binary Lüders projector query. A coherent delayed query is a stronger operation than acquiring a yes/no outcome.',
      physical_boundary='No coherent W33 Hamiltonian orphysical interaction realizing T_P, error budget oruniversalhardware is derived.')


def produce():
    c=dict(status='PASS',reservation_packet='90099d605:11625-11629 extra literature/resource control',Peres_Reye=peres_audit(),Witting_vacuum=witting_vacuum_audit(),coherent_query=coherent_query_audit())
    sources=['analysis/w33_pass4963_witting_pancharatnam_w33_reaudit.py','analysis/w33_pass11625_11629_composites_joint_vacua.py','data/w33_pass11625_11629_composites_joint_vacua.json','analysis/BT1408_witting_contextual_communication_bridge.md','analysis/BT1411_witting_basis_analyzer_unitaries.md']
    c['source_sha256']={p:ph(ROOT/p) for p in sources};c['producer_sha256']=ph(Path(__file__))
    OUT.write_text(json.dumps(c,indent=2)+'\n');print('Peres/Reye, Witting vacuum, coherent query: PASS');return c

if __name__=='__main__':produce()
