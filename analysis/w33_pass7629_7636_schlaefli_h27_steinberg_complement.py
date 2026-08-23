#!/usr/bin/env python3
"""Pass7629-7636: Schlaefli and H27 are complementary transports on one 9x3 quotient.

Choose the anchor A2 from the live Eisenstein W33 leaf.  Its valency-81 global
A2 suborbit has the canonical 27 K3 fibres of Pass7621.  Restrict the global
Steinberg intertwiner T to those 81 A2s: exactly 27 distinct T-columns occur,
each three times.  The two 27x3 partitions are transverse; their incidence graph
is 9 disjoint K3,3's.  Hence the 27 Schlaefli vertices acquire nine canonical
triples.  Between every two triples Schlaefli is K3,3 minus one perfect matching.
The 36 missing matchings form exactly the H27 distance-transitive graph.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
from analysis.w33_pass7509_7516_steinberg_global_intertwiner import build_T
OUT=ROOT/'data/PART_W33_PASS7629_7636_SCHLAEFLI_H27_STEINBERG_COMPLEMENT.json'

def components(A):
    seen=set();out=[]
    for i in range(len(A)):
        if i in seen:continue
        q=[i];seen.add(i);cc=[]
        while q:
            u=q.pop();cc.append(u)
            for v in np.flatnonzero(A[u]):
                v=int(v)
                if v not in seen:seen.add(v);q.append(v)
        out.append(tuple(sorted(cc)))
    return out

def main():
    R,A2,J,base,bl,AO,lab,edges,L,P,T,maps=build_T();anchor=bl[0]
    S=[int(x) for x in np.flatnonzero(lab[anchor]==4)];assert len(S)==81
    sub=lab[np.ix_(S,S)];A4=(sub==4).astype(np.int16);CN=A4@A4
    X=np.zeros((81,81),dtype=np.int8)
    for i,j in itertools.combinations(range(81),2):
        if A4[i,j] and CN[i,j]==1:X[i,j]=X[j,i]=1
    tri=components(X);assert len(tri)==27 and set(map(len,tri))=={3}

    # Second partition: equality of restricted Steinberg columns.
    D=defaultdict(list)
    for i,a in enumerate(S):D[tuple(int(x) for x in T[:,a])].append(i)
    tfib=[tuple(sorted(v)) for v in D.values()]
    assert len(tfib)==27 and set(map(len,tfib))=={3}
    inc=np.zeros((27,27),dtype=np.int8)
    for i,A in enumerate(tri):
        SA=set(A)
        for j,B in enumerate(tfib):inc[i,j]=len(SA&set(B))
    assert Counter(map(int,inc.ravel()))==Counter({0:648,1:81})
    assert set(map(int,inc.sum(0)))==set(map(int,inc.sum(1)))=={3}
    bip=np.block([[np.zeros((27,27),dtype=np.int8),inc],[inc.T,np.zeros((27,27),dtype=np.int8)]])
    cc=components(bip);assert Counter(map(len,cc))==Counter({6:9})
    assert all(np.all(bip[np.ix_(C,C)].sum(1)==3) for C in cc)
    # Each component is K3,3; record the induced grouping of Schlaefli vertices.
    cid={v:i for i,C in enumerate(cc) for v in C};grp=[cid[i] for i in range(27)]
    assert Counter(grp)==Counter({i:3 for i in range(9)})

    # Schlaefli quotient from Pass7621 relation pattern.
    Q=np.zeros((27,27),dtype=np.int8)
    for i,j in itertools.combinations(range(27),2):
        pat=Counter(int(sub[a,b]) for a in tri[i] for b in tri[j])
        if pat==Counter({2:6,4:3}):Q[i,j]=Q[j,i]=1
    assert set(map(int,Q.sum(1)))=={16}
    QQ=Q@Q;assert {int(QQ[i,j]) for i,j in itertools.combinations(range(27),2) if Q[i,j]}=={10};assert {int(QQ[i,j]) for i,j in itertools.combinations(range(27),2) if not Q[i,j]}=={8}
    # Nine triples are cocliques.  Between any two, Q is K3,3 minus a perfect matching.
    for g in range(9):
        I=[i for i in range(27) if grp[i]==g];assert np.sum(Q[np.ix_(I,I)])==0
    H=np.zeros((27,27),dtype=np.int8)
    for g,h in itertools.combinations(range(9),2):
        I=[i for i in range(27) if grp[i]==g];Jj=[j for j in range(27) if grp[j]==h];B=Q[np.ix_(I,Jj)]
        assert int(B.sum())==6 and set(map(int,B.sum(0)))==set(map(int,B.sum(1)))=={2}
        for i in I:
            for j in Jj:
                if not Q[i,j]:H[i,j]=H[j,i]=1
    assert set(map(int,H.sum(1)))=={8}
    # Exact edge partition of the complete 9-partite graph K_{3,...,3}.
    K=np.ones((27,27),dtype=np.int8)-np.eye(27,dtype=np.int8)
    for g in range(9):
        I=[i for i in range(27) if grp[i]==g];K[np.ix_(I,I)]=0
    assert np.array_equal(Q+H,K) and np.all((Q*H)==0)
    spec=Counter(round(float(x),8) for x in np.linalg.eigvalsh(H.astype(float)));assert spec==Counter({2.0:12,-1.0:8,-4.0:6,8.0:1})
    # Distance regularity {8,6,1;1,3,8}.
    def dist(s):
        d=[-1]*27;d[s]=0;q=deque([s])
        while q:
            u=q.popleft()
            for v in np.flatnonzero(H[u]):
                v=int(v)
                if d[v]<0:d[v]=d[u]+1;q.append(v)
        return d
    for s in range(27):
        d=dist(s);assert Counter(d)==Counter({0:1,1:8,2:16,3:2});lay={r:{i for i,x in enumerate(d) if x==r} for r in range(4)}
        expected={0:(0,0,8),1:(1,1,6),2:(3,4,1),3:(8,0,0)}
        for r in range(4):
            for v in lay[r]:
                N=set(map(int,np.flatnonzero(H[v])));got=(len(N&lay.get(r-1,set())),len(N&lay[r]),len(N&lay.get(r+1,set())))
                assert got==expected[r]
    out={
      'schema':'w33.pass7629_7636.schlaefli_h27_steinberg_complement.v1','status':'PASS','passes':'7629-7636',
      'A2_suborbit':81,'canonical_Schlaefli_fibres':[27,3],'restricted_T_distinct_columns':27,'restricted_T_column_multiplicity':3,
      'two_partition_incidence':'9 disjoint K3,3','nine_packets':9,'points_per_packet':9,
      'Schlaefli':{'parameters':[27,16,10,8],'nine_tripartition':'9 cocliques of size 3','between_two_parts':'K3,3 minus one perfect matching'},
      'H27':{'degree':8,'spectrum':{'8':1,'2':12,'-1':8,'-4':6},'distance_spheres':[1,8,16,2],'intersection_array':'{8,6,1;1,3,8}'},
      'edge_partition':'On the same 27 vertices, the complete 9-partite graph K_{3,3,...,3} decomposes edge-disjointly as Schlaefli (degree 16) plus H27 (degree 8).',
      'novelty_boundary':'Pass7181/7186 already constructed the Schlaefli 27 and the H27 3-cover of K9 from the E8 A2 shell. New here is their objectwise complementarity produced by the global Steinberg intertwiner: the T-column partition and the scheme-triangle partition meet as 9 K3,3 and force the common 9x3 coordinate system.',
      'theorem':'The E6 minuscule Schlaefli graph and the qutrit H27 Cayley graph are complementary transports on a single canonical nine-triple quotient cut out inside the E8 global A2/Steinberg data.',
      'claim_boundary':'Exact finite graph/intertwiner theorem only; no particle interpretation is assigned.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','incidence':'9K3,3','Schlaefli_degree':16,'H27_degree':8}))
if __name__=='__main__':main()
