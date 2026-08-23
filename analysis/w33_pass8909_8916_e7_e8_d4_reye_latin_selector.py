#!/usr/bin/env python3
"""Pass8909-8916: a ternary E8 residue selects a D4/Reye/Klein-Latin 16-sector inside E7 Pauli space.

Dependencies:
- Pass8489: 63 E7 antipodal root pairs = 63 three-qubit Pauli classes and 336 E7 A2s = 336 closed anticommuting triangles;
- Pass7949: explicit 16-point Q+(3,3) tensor residue through current E8 A2 radicals;
- Pass8561: bare E7 is transitive on all 336 sectors, so it selects none;
- Pass5316-5323: prior repo Latin/D4/tomotope work, including the global split 576=144 Klein-affine + 432 cyclic-nonaffine.

This pass supplies genuinely cross-rung data: relation to the actual ternary residue
splits the 336 E7 A2s as 16+48+128+144. The 16 A2s orthogonal to all 16 residue
A2s are exactly the A2 subsystems of the complementary D4 root system. Their
(12_4,16_3) point-block incidence realizes one specific Klein-V4 Latin square,
with full colored automorphism group 576=W(F4)/{+-I}.
"""
from __future__ import annotations
import itertools,json,sys
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
from analysis.w33_pass7949_7956_literal_qplus33_in_e8_qplus73 import T,qdet
OUT=ROOT/'data/PART_W33_PASS8909_8916_E7_E8_D4_REYE_LATIN_SELECTOR.json'

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError
def rkey(r):
    r=tuple(map(int,r));nr=tuple(-x for x in r);return min(r,nr)
def a2orth(R,A2,i,j):return all(E.dot(R[a],R[b])==0 for a in A2[i] for b in A2[j])

def isotopic(A,B):
    ps=list(itertools.permutations(range(4)))
    for pr in ps:
      X=A[list(pr),:]
      for pc in ps:
        Y=X[:,list(pc)]
        for pv in ps:
          Z=np.vectorize(lambda x:pv[x])(Y)
          if np.array_equal(Z,B):return True
    return False

def main():
    R,A2,ag,J,base,leaves,lgens,parity=E.build()
    # Global A2 radical map and explicit Q+(3,3) residue from Pass7949 coordinates.
    radicals=[]
    for S in A2:
        vals=set()
        for i,j in itertools.combinations(sorted(S),2):
            if E.dot(R[i],R[j])==-4:vals.add(E.canon3(tuple(R[i][k]-R[j][k] for k in range(8))))
        assert len(vals)==1;radicals.append(next(iter(vals)))
    ri={v:i for i,v in enumerate(radicals)}
    rank1=sorted({canon(x) for x in itertools.product(range(3),repeat=4) if any(x) and qdet(x)==0})
    U=set()
    for x in rank1:
        y4=tuple(int(z) for z in (T.astype(np.int64)@np.array(x,dtype=np.int64))%3)
        U.add(ri[E.canon3(y4+(0,0,0,0))])
    assert len(U)==16

    # E7 = roots orthogonal to the simple root (2,2,0,...); exactly 336 A2 subsystems.
    r0=np.array(E.SIMPLES[1],dtype=int)
    e7roots={i for i,r in enumerate(R) if int(np.dot(np.array(r),r0))==0};assert len(e7roots)==126
    e7a2=[i for i,S in enumerate(A2) if set(S)<=e7roots];assert len(e7a2)==336
    oc={i:sum(a2orth(R,A2,i,u) for u in U) for i in e7a2}
    split=Counter(oc.values());assert split==Counter({4:144,1:128,0:48,16:16})
    selected=[i for i in e7a2 if oc[i]==16];assert len(selected)==16

    # Selected radicals exhaust the singular points of the complementary 4-space.
    sr=[radicals[i] for i in selected]
    assert len(set(sr))==16 and all(tuple(x[:4])==(0,0,0,0) for x in sr)
    comp_sing={E.canon3((0,0,0,0)+tuple(x)) for x in itertools.product(range(3),repeat=4)
               if any(x) and sum(int(y)*int(y) for y in x)%3==0}
    assert set(sr)==comp_sing and len(comp_sing)==16

    # Twelve antipodal root pairs = the D4 roots in the complementary coordinates.
    blocks=[]
    for i in selected:
        P=sorted({rkey(R[x]) for x in A2[i]});assert len(P)==3;blocks.append(P)
    pts=sorted(set().union(*map(set,blocks)));assert len(pts)==12
    mult=Counter(p for B in blocks for p in B);assert set(mult.values())=={4}
    signed={v for p in pts for v in (p,tuple(-x for x in p))};assert len(signed)==24
    d4={tuple([0,0,0,0]+list(v)) for i,j in itertools.combinations(range(4),2)
        for a in (2,-2) for b in (2,-2)
        for v in [tuple(a if k==i else b if k==j else 0 for k in range(4))]}
    assert signed==d4

    pi={p:i for i,p in enumerate(pts)};BS=[frozenset(pi[p] for p in B) for B in blocks]
    AP=np.zeros((12,12),dtype=np.uint8)
    for B in BS:
        for i,j in itertools.combinations(B,2):AP[i,j]=AP[j,i]=1
    assert set(map(int,AP.sum(1)))=={8}
    comp=(1-np.eye(12,dtype=np.uint8)-AP).astype(np.uint8)
    Gc=nx.from_numpy_array(comp);parts=[sorted(c) for c in nx.connected_components(Gc)]
    assert sorted(map(len,parts))==[4,4,4]

    AB=np.zeros((16,16),dtype=np.uint8)
    for i,j in itertools.combinations(range(16),2):
        if BS[i]&BS[j]:AB[i,j]=AB[j,i]=1
    assert set(map(int,AB.sum(1)))=={9}
    la=set();mu=set()
    for i,j in itertools.combinations(range(16),2):
        c=int(AB[i]@AB[j]);(la if AB[i,j] else mu).add(c)
    assert la=={4} and mu=={6}

    Inc=nx.Graph()
    for i in range(12):Inc.add_node(('p',i),kind='p')
    for j in range(16):Inc.add_node(('b',j),kind='b')
    for j,B in enumerate(BS):
        for i in B:Inc.add_edge(('p',i),('b',j))
    nm=nx.algorithms.isomorphism.categorical_node_match('kind',None)
    aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(Inc,Inc,node_match=nm).isomorphisms_iter())
    assert aut==576

    # The three K4 parts give row/column/symbol classes, hence an order-4 Latin square.
    rows,cols,syms=parts;rpos={x:i for i,x in enumerate(rows)};cpos={x:i for i,x in enumerate(cols)};spos={x:i for i,x in enumerate(syms)}
    L=np.full((4,4),-1,dtype=int)
    for B in BS:
        r=next(x for x in B if x in rpos);c=next(x for x in B if x in cpos);s=next(x for x in B if x in spos)
        L[rpos[r],cpos[c]]=spos[s]
    assert sorted(L.ravel())==[0]*4+[1]*4+[2]*4+[3]*4
    V4=np.array([[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]])
    C4=np.array([[(i+j)%4 for j in range(4)] for i in range(4)])
    assert isotopic(L,V4) and not isotopic(L,C4)

    out={'schema':'w33.pass8909_8916.e7_e8_d4_reye_latin_selector.v1','status':'PASS','passes':'8909-8916',
      'E7_A2_total':336,'orthogonality_profile_to_residue':{'16':16,'0':48,'1':128,'4':144},
      'selected_A2':16,'selected_rule':'orthogonal to all 16 A2s of the explicit ternary Q+(3,3) residue',
      'selected_radicals':'all 16 singular projective points of the complementary Q+(3,3)',
      'root_pairs':12,'signed_roots':24,'root_subsystem':'D4 in the complementary four coordinates',
      'incidence':'(12_4,16_3) transversal/Reye-type configuration','point_graph':'K4,4,4','block_graph':'SRG(16,9,4,6) = complement of R(4,4)','colored_automorphism_order':576,'automorphism_identification':'W(F4)/{+-I}',
      'latin_square':L.tolist(),'latin_isotopy':'Klein V4, not cyclic C4',
      'prior_art_boundary':'Pass5316-5323 already classified all 576 order-4 Latin squares and D4/tomotope actions; new here is the objectwise cross-rung selection of one Klein square from the actual E7 Pauli sectors by the explicit ternary E8 residue.',
      'theorem':'Adding the explicit ternary Q+(3,3) residue breaks the otherwise transitive 336 E7/Pauli sectors and canonically selects the 16 A2 subsystems of a complementary D4. Their 12-point/16-block incidence is a 576-symmetric Klein-V4 Latin-square configuration.',
      'claim_boundary':'Exact E8/E7 root, finite-incidence and Latin-square theorem; no physical sector selection is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','split':'16+48+128+144','selected':'D4 A2s','Aut':576,'Latin':'V4'}))
if __name__=='__main__':main()
