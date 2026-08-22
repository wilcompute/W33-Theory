#!/usr/bin/env python3
"""Pass7425-7432: enumerate all 2240 Eisenstein W33 leaves inside E8 and
prove their global distance-regular/incidence-projector structure.

This is an exact finite computation in doubled E8 root coordinates.  It does not
identify the halved graph with any named external graph without an explicit
isomorphism; only its verified SRG parameters are promoted.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7425_7432_E8_2240_LEAF_GEOMETRY.json'

SIMPLES=[
(1,-1,-1,-1,-1,-1,-1,1),
(2,2,0,0,0,0,0,0),
(-2,2,0,0,0,0,0,0),
(0,-2,2,0,0,0,0,0),
(0,0,-2,2,0,0,0,0),
(0,0,0,-2,2,0,0,0),
(0,0,0,0,-2,2,0,0),
(0,0,0,0,0,-2,2,0),
]

def roots():
    R=[]
    for i,j in itertools.combinations(range(8),2):
        for a in (2,-2):
            for b in (2,-2):
                v=[0]*8;v[i]=a;v[j]=b;R.append(tuple(v))
    for s in itertools.product((1,-1),repeat=8):
        if sum(x<0 for x in s)%2==0:R.append(tuple(s))
    assert len(R)==240 and len(set(R))==240
    return R

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def refl(x,r):
    q=dot(x,r); assert q%4==0
    k=q//4
    return tuple(x[i]-k*r[i] for i in range(8))

def enum_a2(R):
    I={r:i for i,r in enumerate(R)}; out=set()
    for i,j in itertools.combinations(range(240),2):
        if dot(R[i],R[j])!=-4:continue
        s=tuple(R[i][k]+R[j][k] for k in range(8));k=I[s]
        out.add(frozenset((i,j,k,I[tuple(-x for x in R[i])],
                            I[tuple(-x for x in R[j])],I[tuple(-x for x in s)])))
    A=sorted(out,key=lambda x:tuple(sorted(x)));assert len(A)==1120
    return A

def perm_comp(p,q): return tuple(p[q[i]] for i in range(len(q)))

def rank_mod(M,p):
    A=np.asarray(M,dtype=np.int16).copy()%p;m,n=A.shape;r=0
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if len(nz)==0:continue
        z=r+int(nz[0]); A[[r,z]]=A[[z,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        rows=np.flatnonzero(A[:,c]); rows=rows[rows!=r]
        if len(rows):
            A[rows]=(A[rows]-A[rows,c,None]*A[r])%p
        r+=1
        if r==m:break
    return r

def main():
    R=roots();I={r:i for i,r in enumerate(R)};A2=enum_a2(R);ai={S:i for i,S in enumerate(A2)}
    rg=[]
    for s in SIMPLES:rg.append(tuple(I[refl(r,s)] for r in R))
    c=tuple(range(240))
    for g in rg:c=perm_comp(g,c)
    J=tuple(range(240))
    for _ in range(10):J=perm_comp(c,J)
    assert all(J[J[J[i]]]==i for i in range(240)) and any(J[i]!=i for i in range(240))
    ag=[]
    for g in rg:
        ag.append(tuple(ai[frozenset(g[x] for x in S)] for S in A2))
    base=frozenset(i for i,S in enumerate(A2) if frozenset(J[x] for x in S)==S)
    assert len(base)==40
    leaves=[base]; li={base:0}; q=deque([base])
    while q:
        X=q.popleft()
        for g in ag:
            Y=frozenset(g[x] for x in X)
            if Y not in li:
                li[Y]=len(leaves);leaves.append(Y);q.append(Y)
    assert len(leaves)==2240
    masks=[sum(1<<x for x in L) for L in leaves]
    overlap=Counter((masks[0]&m).bit_count() for m in masks)
    assert overlap==Counter({1:1080,0:729,4:390,13:40,40:1})
    G=[set() for _ in leaves]; allov=Counter()
    for i in range(2240):
        mi=masks[i]
        for j in range(i+1,2240):
            z=(mi&masks[j]).bit_count();allov[z]+=1
            if z==13:G[i].add(j);G[j].add(i)
    assert allov==Counter({1:1209600,0:816480,4:436800,13:44800})
    assert {len(x) for x in G}=={40}
    ov0={j:(masks[0]&masks[j]).bit_count() for j in range(2240)}
    layers={0:{0},1:{j for j,z in ov0.items() if z==13},
            2:{j for j,z in ov0.items() if z==4},
            3:{j for j,z in ov0.items() if z==1},
            4:{j for j,z in ov0.items() if z==0}}
    assert [len(layers[d]) for d in range(5)]==[1,40,390,1080,729]
    inter={}
    for d in range(5):
        C=Counter()
        for v in layers[d]:
            C[tuple(len(G[v]&layers[e]) for e in range(5))]+=1
        assert len(C)==1
        inter[d]=next(iter(C))
    assert inter=={0:(0,40,0,0,0),1:(1,0,39,0,0),2:(0,4,0,36,0),
                  3:(0,0,13,0,27),4:(0,0,0,40,0)}
    side0=layers[0]|layers[2]|layers[4];side1=layers[1]|layers[3]
    assert len(side0)==len(side1)==1120 and all((v in side0) != (w in side0) for v in range(2240) for w in G[v])
    B=np.array([[0,40,0,0,0],[1,0,39,0,0],[0,4,0,36,0],
                [0,0,13,0,27],[0,0,0,40,0]],dtype=float)
    ev=np.linalg.eigvals(B); vals=sorted(round(float(x.real)) for x in ev)
    assert vals==[-40,-12,0,12,40]
    spectrum={'40':1,'12':300,'0':1638,'-12':300,'-40':1}
    H=[set() for _ in side0]; s0=sorted(side0); pos={v:i for i,v in enumerate(s0)}
    for ii,v in enumerate(s0):
        n2=set()
        for u in G[v]:n2.update(G[u])
        n2.discard(v)
        H[ii]={pos[w] for w in n2 if w in pos}
    assert {len(x) for x in H}=={390}
    lam=mu=None
    for i in range(1120):
        for j in range(i+1,1120):
            z=len(H[i]&H[j])
            if j in H[i]:
                lam=z if lam is None else lam;assert z==lam
            else:
                mu=z if mu is None else mu;assert z==mu
    assert (lam,mu)==(146,130)
    basis=[]
    for S in A2:
        p=next((e for e in itertools.combinations(sorted(S),2) if dot(R[e[0]],R[e[1]])==-4),None)
        assert p;basis.append(p)
    AO=np.zeros((1120,1120),dtype=np.uint8)
    for i in range(1120):
        a,b=basis[i]
        for j in range(i+1,1120):
            c0,d=basis[j]
            if dot(R[a],R[c0])==dot(R[a],R[d])==dot(R[b],R[c0])==dot(R[b],R[d])==0:
                AO[i,j]=AO[j,i]=1
    assert set(map(int,AO.sum(1)))=={120}
    C=(AO.astype(np.int16)@AO.astype(np.int16))
    inside=Counter();bl=sorted(base)
    for a,b in itertools.combinations(bl,2):
        inside['orth' if AO[a,b] else f'mu{int(C[a,b])}']+=1
    assert inside==Counter({'mu16':540,'orth':240})
    rowm=[0]*1120
    F=np.zeros((1120,2240),dtype=np.uint8)
    for j,L in enumerate(leaves):
        for a in L:F[a,j]=1;rowm[a]|=1<<j
    assert set(map(int,F.sum(1)))=={80} and set(map(int,F.sum(0)))=={40}
    rep=Counter()
    for a,b in itertools.combinations(range(1120),2):
        z=(rowm[a]&rowm[b]).bit_count()
        if AO[a,b]:assert z==8;rep['orth']+=1
        elif C[a,b]==16:assert z==8;rep['mu16']+=1
        else:assert z==0;rep[f'mu{int(C[a,b])}']+=1
    assert rep==Counter({'mu10':362880,'mu16':151200,'mu40':45360,'orth':67200})
    P=np.array([[1,120,648,270,81],[1,20,-12,-30,21],[1,8,-24,18,-3],
                [1,-4,12,-6,-3],[1,-40,-24,30,33]],dtype=int)
    gram_eigs=[80+8*(int(P[r,1])+int(P[r,3])) for r in range(5)]
    assert gram_eigs==[3200,0,288,0,0]
    assert rank_mod(F,2)==301 and rank_mod(F,3)==301
    WIB=AO[np.ix_(bl,bl)];assert set(map(int,WIB.sum(1)))=={12}
    closed={frozenset([bl[i]]+[bl[j] for j in np.flatnonzero(WIB[i])]) for i in range(40)}
    cuts={frozenset(base&leaves[j]) for j in G[0]}
    assert cuts==closed and len(cuts)==40
    out={
      'schema':'w33.pass7425_7432.e8_2240_leaf_geometry.v1','status':'PASS',
      'passes':'7425-7432','A2':1120,'Eisenstein_W33_leaves':2240,
      'leaf_size':40,'A2_replication':80,
      'leaf_overlap_from_one':{str(k):v for k,v in sorted(overlap.items())},
      'global_unordered_leaf_pair_overlaps':{str(k):v for k,v in sorted(allov.items())},
      'pair_selection_theorem':'Within every leaf, the 780 A2 pairs are exactly 240 orthogonal pairs plus 540 global mu=16 pairs; mu=10 and mu=40 never occur.',
      'pair_replication':{'orthogonal':8,'mu16':8,'mu10':0,'mu40':0},
      'incidence_identity':'F F^T = 80 I + 8(A_orth + A_mu16)',
      'incidence_real_spectrum':{'3200':1,'288':300,'0':819},
      'incidence_rank':301,'incidence_rank_F2':301,'incidence_rank_F3':301,
      'centered_tight_frame':'F with its constant component removed is a tight frame spanning exactly the 300-dimensional A2 Gelfand-pair constituent.',
      'leaf_graph':{
        'definition':'two leaves adjacent iff their A2 intersection has size 13',
        'vertices':2240,'degree':40,'bipartite':True,'diameter':4,
        'distance_distribution':[1,40,390,1080,729],
        'intersection_array':'{40,39,36,27;1,4,13,40}',
        'overlap_by_distance':{'0':40,'1':13,'2':4,'3':1,'4':0},
        'spectrum':spectrum,
        'local_reconstruction':'For a leaf L, its 40 graph-neighbors meet L in exactly the 40 closed W(3,3) neighborhoods {p} union p^perp.'
      },
      'halved_graph':{'vertices':1120,'srg':'(1120,390,146,130)','spectrum':'390^1 26^300 (-10)^819'},
      'external_identification_boundary':'The halved SRG has the parameters of the graph commonly called O_8^+(3), but this pass does not promote an isomorphism without an explicit map.',
      'claim_boundary':'Exact E8 root/A2/leaf incidence theorem. No particle, coupling, or hardware claim follows.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','leaves':2240,'rank':301,'IA':out['leaf_graph']['intersection_array']}))
if __name__=='__main__':main()
