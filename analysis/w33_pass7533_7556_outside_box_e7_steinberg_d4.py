#!/usr/bin/env python3
"""Pass7533-7556: three outside-box exact probes.

7533-7540: E7 roots descend through the reflection quotient to Sp6(2) on B3(3).
7541-7548: the 360 distinct Steinberg vectors split into 90 regular tetrahedra,
           literally indexed by the 90 J-stable D4 partial-ovoid blocks.
7549-7556: the canonical 45 D4-perp pairs become 45 pairs of orthogonal
           Steinberg tetrahedra, giving 6D packets.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
from analysis.w33_pass7509_7516_steinberg_global_intertwiner import build_T
OUT=ROOT/'data/PART_W33_PASS7533_7556_OUTSIDE_BOX_E7_STEINBERG_D4.json'

def span_rank(R,idx):return np.linalg.matrix_rank(np.array([R[i] for i in idx],float))

def e7_sp6(R,A2,ag,base,leaves,lgens,parity):
    I={r:i for i,r in enumerate(R)};ai={S:i for i,S in enumerate(A2)};plus=sorted(i for i,x in enumerate(parity) if x==0)
    r=E.SIMPLES[0];rp=tuple(I[E.refl(x,r)] for x in R);ap=tuple(ai[frozenset(rp[x] for x in S)] for S in A2)
    li={L:i for i,L in enumerate(leaves)};rleaf=tuple(li[frozenset(ap[x] for x in L)] for L in leaves)
    U=[frozenset(leaves[v]&leaves[rleaf[v]]) for v in plus];assert len(set(U))==1120 and set(map(len,U))=={13};ui={S:i for i,S in enumerate(U)}
    orth=[x for x in R if E.dot(x,r)==0];assert len(orth)==126;reps=[];seen=set()
    for q in orth:
        nq=tuple(-z for z in q);k=min(I[q],I[nq])
        if k not in seen:seen.add(k);reps.append(R[k])
    assert len(reps)==63;perms=[]
    for q in reps:
        qp=tuple(I[E.refl(x,q)] for x in R);aq=tuple(ai[frozenset(qp[x] for x in S)] for S in A2);perms.append(tuple(ui[frozenset(aq[x] for x in S)] for S in U))
    chosen=[];PG=PermutationGroup([Permutation(list(range(1120)))]);growth=[]
    for p in perms:
        H=PermutationGroup([Permutation(x) for x in chosen+[p]]);o=int(H.order())
        if o>int(PG.order()):chosen.append(p);PG=H;growth.append(o)
        if o==1451520:break
    assert int(PG.order())==1451520;stab=PG.stabilizer(0);subs=sorted(len(o) for o in stab.orbits())
    assert sorted(len(o) for o in PG.orbits())==[1120] and int(stab.order())==1296
    return {'E7_roots':126,'distinct_root_reflections':63,'selected_generators':len(chosen),'order_growth':growth,'group_order':1451520,
      'identification':'W(E7)/{+-1}=Sp6(2)','action_degree':1120,'point_stabilizer_order':1296,'point_stabilizer_subdegrees':subs,
      'theorem':'The E7 root reflections orthogonal to the chosen E8 reflection descend to a faithful transitive Sp6(2) action on the 1120 B3(3) maximal singular 3-spaces.'}

def d4_frame(R,A2,base,AO,lab,T):
    bl=sorted(base);D=defaultdict(list)
    for j in np.flatnonzero(np.any(T!=0,axis=0)):D[tuple(int(x) for x in T[:,j])].append(int(j))
    assert len(D)==360 and set(map(len,D.values()))=={3};vecs=list(D);fibres=[D[v] for v in vecs];V=np.asarray(vecs,dtype=np.int64).T;Gram=V.T@V
    comp=[]
    for F in fibres:
        cand=[]
        for a in bl:
            roots=set(A2[a]);
            for f in F:roots.update(A2[f])
            if len(roots)!=24 or span_rank(R,roots)!=4:continue
            ambient=[i for i,r in enumerate(R) if np.linalg.matrix_rank(np.vstack([np.array([R[j] for j in roots],float),np.array(r,float)]))==4]
            if len(ambient)==24:cand.append(a)
        assert len(cand)==1;comp.append(cand[0])
    assert Counter(comp)=={a:9 for a in bl}
    A=(Gram==-3840);np.fill_diagonal(A,False);assert set(map(int,A.sum(1)))=={3};seen=set();tets=[]
    for i in range(360):
        if i in seen:continue
        S={i};dq=[i];seen.add(i)
        while dq:
            u=dq.pop()
            for v in np.flatnonzero(A[u]):
                v=int(v)
                if v not in S:S.add(v);seen.add(v);dq.append(v)
        assert len(S)==4 and all(A[u,v] for u,v in itertools.combinations(S,2));tets.append(tuple(sorted(S)))
    assert len(tets)==90 and all(np.all(V[:,Q].sum(1)==0) for Q in tets)
    supports=[frozenset(comp[i] for i in Q) for Q in tets];d4=set()
    for Q in itertools.combinations(bl,4):
        roots=set().union(*(set(A2[a]) for a in Q))
        if len(roots)==24 and span_rank(R,roots)==4:
            B=np.array([R[i] for i in roots],float);ambient=[i for i,r in enumerate(R) if np.linalg.matrix_rank(np.vstack([B,np.array(r,float)]))==4]
            if len(ambient)==24:d4.add(frozenset(Q))
    assert len(d4)==90 and set(supports)==d4
    return V,Gram,tets,supports,{'vectors':360,'J_orbit_fibre_size':3,'transverse_D4_completions':360,'completions_per_base_A2':9,
      'norm_squared':11520,'tetrahedron_inner_product':-3840,'normalized_tetrahedron_angle':'-1/3','tetrahedra':90,'tetrahedron_graph':'90 K4',
      'tetrahedron_sums_zero':True,'base_supports_equal_J_stable_D4_blocks':True,
      'theorem':'The 360 distinct Steinberg vectors split spectrally into 90 regular tetrahedra; their four base-completion points are literally the 90 J-stable D4 partial-ovoid blocks.'}

def perp_packets(bl,AO,V,Gram,tets,supports):
    sid={S:i for i,S in enumerate(supports)};partner={}
    for i,S in enumerate(supports):
        common=set(bl)
        for a in S:common&={bl[j] for j in np.flatnonzero(AO[a,bl])}
        P=frozenset(common);assert len(P)==4 and P in sid and P!=S;partner[i]=sid[P]
    assert all(partner[partner[i]]==i for i in range(90));pairs=[(i,partner[i]) for i in range(90) if i<partner[i]];assert len(pairs)==45
    types=Counter();ev0=None
    for a,b in pairs:
        X=Gram[np.ix_(tets[a],tets[b])];assert np.all(X==0)
        W=V[:,list(tets[a])+list(tets[b])];assert np.linalg.matrix_rank(W.astype(float))==6
        GG=Gram[np.ix_(list(tets[a])+list(tets[b]),list(tets[a])+list(tets[b]))];ev=tuple(round(float(x),6) for x in np.linalg.eigvalsh(GG.astype(float)));types[ev]+=1;ev0=ev
    assert len(types)==1
    return {'perp_pairs':45,'cross_inner_products':'all 16 are zero','eight_vector_packet_rank':6,'packet_gram_spectrum':'0^2 + 15360^6',
      'theorem':'The canonical 45 perp-pairs of J-stable D4 blocks pair the Steinberg tetrahedra into 45 congruent packets of two orthogonal regular tetrahedra, spanning 3+3 dimensions.',
      'E6_bridge':'These are the same 45 D4-perp quotient points feeding the existing dual-GQ(4,2)/27-line E6 bridge; this pass supplies an H1 realization by orthogonal tetrahedral pairs.'}

def main():
    R,A2,ag,J,base,leaves,lgens,parity=E.build();AO,C,lab=E.a2_scheme(R,A2);R2,A22,J2,base2,bl,AO2,lab2,edges,L,P,T,maps=build_T();assert R==R2 and A2==A22 and base==base2
    e7=e7_sp6(R,A2,ag,base,leaves,lgens,parity);V,Gram,tets,supports,d4=d4_frame(R,A2,base,AO,lab,T);pp=perp_packets(sorted(base),AO,V,Gram,tets,supports)
    out={'schema':'w33.pass7533_7556.outside_box_e7_steinberg_d4.v1','status':'PASS','passes':'7533-7556','outside_box_1_E7_Sp6_2':e7,'outside_box_2_360_Steinberg_D4_tetrahedra':d4,'outside_box_3_45_perp_tetrahedral_packets':pp,
      'claim_boundary':'Three exact finite algebra/geometry probes; none assigns a physical meaning from matching counts alone.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','Sp6_order':e7['group_order'],'tetrahedra':d4['tetrahedra'],'perp_packets':pp['perp_pairs']}))
if __name__=='__main__':main()
