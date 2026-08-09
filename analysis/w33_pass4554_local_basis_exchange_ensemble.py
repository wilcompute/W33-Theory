#!/usr/bin/env python3
"""Pass 4554 -- exact 108-basis exchange/fault-tolerance ensemble in one Borel cell.

Pass 4543 found 108 full H10 bases: center line-star plus nine of the twelve
neighbors in K1 join 4K3, where the omitted triple is independent across three
pencils.  This pass studies the whole ensemble rather than one basis.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry,build_line_perm,perm_group,point_perm_from_matrix,transvection_matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4554_LOCAL_BASIS_EXCHANGE_ENSEMBLE.json'

def spectrum(A):
    return dict(sorted(Counter(int(round(float(x))) for x in np.linalg.eigvalsh(A.astype(float))).items()))
def main():
    pts,pidx,lines,lidx,_Ap,A,*_=build_geometry();center=0
    neigh=list(map(int,np.flatnonzero(A[center])));assert len(neigh)==12
    # Four K3 pencil components.
    unseen=set(neigh);pencils=[]
    while unseen:
        v=min(unseen);C={v};q=[v];unseen.remove(v)
        while q:
            x=q.pop()
            for y in list(unseen):
                if A[x,y]:unseen.remove(y);C.add(y);q.append(y)
        pencils.append(sorted(C))
    pencils=sorted(pencils);assert pencils==[[1,2,3],[4,5,6],[7,8,9],[28,32,36]]
    omitted=[];bases=[]
    for ps in itertools.combinations(range(4),3):
        for ch in itertools.product(range(3),repeat=3):
            O=frozenset(pencils[p][a] for p,a in zip(ps,ch));omitted.append(O)
            bases.append(frozenset({center}|(set(neigh)-set(O))))
    assert len(set(bases))==108
    overlaps=Counter();X=np.zeros((108,108),dtype=np.uint8)
    for i,j in itertools.combinations(range(108),2):
        o=len(bases[i]&bases[j]);overlaps[o]+=1
        if o==9:X[i,j]=X[j,i]=1
    assert overlaps==Counter({8:2592,7:2376,9:810}) and set(map(int,X.sum(1)))=={15}
    assert spectrum(X)=={-3:56,0:16,3:27,9:8,15:1}
    # Uniform distance partition 1,15,48,44 and diameter three.
    for s in range(108):
        d=[-1]*108;d[s]=0;q=deque([s])
        while q:
            u=q.popleft()
            for v in np.flatnonzero(X[u]):
                v=int(v)
                if d[v]<0:d[v]=d[u]+1;q.append(v)
        assert Counter(d)==Counter({3:44,2:48,1:15,0:1})
    # Borel action: exact canonical flag stabilizer (point 0 on line 0).
    trans=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    chosen=[];G={tuple(range(40))}
    for i,g in enumerate(trans):
        T=perm_group([trans[j] for j in chosen]+[g],40)
        if len(T)>len(G):chosen.append(i);G=T
        if len(G)==25920:break
    pencilsets=[frozenset(i for i,L in enumerate(lines) if p in L) for p in range(40)];pi={S:i for i,S in enumerate(pencilsets)}
    def induced_point(g):return tuple(pi[frozenset(g[i] for i in S)] for S in pencilsets)
    H={g for g in G if g[0]==0 and induced_point(g)[0]==0};assert len(H)==162
    bidx={B:i for i,B in enumerate(bases)};un=set(range(108));orbs=[]
    while un:
        i=min(un);O={bidx[frozenset(g[x] for x in bases[i])] for g in H};orbs.append(sorted(O));un-=O
    orbs=sorted(orbs,key=len,reverse=True);assert list(map(len,orbs))==[81,27]
    quotient=[]
    for O in orbs:
        vals={tuple(sum(int(X[i,j]) for j in Q) for Q in orbs) for i in O};assert len(vals)==1;quotient.append(list(vals.pop()))
    assert quotient==[[12,3],[9,6]]
    # Erasure coverage: a basis survives an erased spoke set iff it omits every erased spoke.
    one={v:sum(v in O for O in omitted) for v in neigh};assert set(one.values())=={27}
    pair=Counter();triple=Counter()
    pencil_of={v:p for p,C in enumerate(pencils) for v in C}
    for a,b in itertools.combinations(neigh,2):pair['same_pencil' if pencil_of[a]==pencil_of[b] else 'distinct_pencils']+=sum({a,b}<=O for O in omitted)
    # normalize by number of erased sets: all same-pairs have 0; all distinct have 6.
    assert all(sum({a,b}<=O for O in omitted)==(0 if pencil_of[a]==pencil_of[b] else 6) for a,b in itertools.combinations(neigh,2))
    good3=0
    for E in itertools.combinations(neigh,3):
        n=sum(set(E)<=O for O in omitted);ind=len({pencil_of[x] for x in E})==3
        assert n==(1 if ind else 0);good3+=ind
    assert good3==108
    out={'pass':4554,'bases':108,'basis_rule':'center line-star plus nine neighbors; omitted triple independent across three of four K3 pencils',
      'pairwise_basis_overlap_counts':{'9':810,'8':2592,'7':2376},
      'basis_exchange_graph':{'vertices':108,'degree':15,'edges':810,'diameter':3,'distance_distribution':[1,15,48,44],'spectrum':{'15':1,'9':8,'3':27,'0':16,'-3':56}},
      'Borel_action':{'order':162,'orbit_sizes':[81,27],'orbit_reading':'81 bases omit one line in the fixed flag pencil and two other pencils; 27 bases omit only the three nonfixed pencils','equitable_quotient':quotient},
      'erasure_resilience':{'single_spoke':'27 of 108 bases avoid any specified spoke','two_spokes_distinct_pencils':6,'two_spokes_same_pencil':0,'three_spokes':'exactly one surviving basis iff the three erased spokes lie in three distinct pencils; 108 such triples'},
      'center_boundary':'All 108 bases use the parity-odd center line-star, so erasing that anchor kills this center-anchored ensemble.',
      'theorem':'The 108 local H10 bases form a connected 15-regular diameter-3 exchange graph with two Borel orbits 81+27 and exact spoke-erasure switching statistics.',
      'boundary':'This is finite representable-matroid redundancy; it is not a physical fault-tolerance threshold or noise model.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
