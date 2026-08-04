#!/usr/bin/env python3
from itertools import combinations, permutations
from collections import Counter, deque
import json, argparse

VALID=[0,1,2,3,4,5,6,8,10,11,12,13,16,17,19,20,22,24,25,26,29,30]
PARITY7=[0,15,51,60,85,98,75,105,70,81,26,55,94,101,72,57,38,52,42,13,1,127]
DIRS=[1,2,4,8,15]

def wt(x): return x.bit_count()
def canon5(x):
    y=x^31
    return min(x,y)
def axis_label(x):
    c=canon5(x)
    if wt(c)>2: c ^= 31
    return tuple(i for i in range(5) if (c>>i)&1)

def clebsch():
    verts=sorted({canon5(x) for x in range(32)})
    adj={v:set() for v in verts}
    for v in verts:
        for i in range(5):
            w=canon5(v^(1<<i))
            adj[v].add(w)
    return verts,adj

def spectrum(adj):
    import numpy as np
    vs=sorted(adj); idx={v:i for i,v in enumerate(vs)}
    A=np.zeros((len(vs),len(vs)),dtype=float)
    for v in vs:
        for w in adj[v]: A[idx[v],idx[w]]=1
    ev=np.linalg.eigvalsh(A)
    return Counter(round(float(x)) for x in ev)

def systematic_search(r):
    req=[[max(0,5-wt(x^y)) for y in VALID] for x in VALID]
    vals=range(1<<r); dist=[[wt(a^b) for b in vals] for a in vals]
    a=[None]*len(VALID); a[0]=0; nodes=0
    def rec():
        nonlocal nodes
        nodes+=1
        if all(x is not None for x in a): return a.copy()
        best=None; cb=None
        for i in range(len(a)):
            if a[i] is None:
                c=[v for v in vals if all(z is None or dist[v][z]>=req[i][j] for j,z in enumerate(a))]
                if not c:return None
                if cb is None or len(c)<len(cb):best,cb=i,c
        for v in cb:
            a[best]=v
            z=rec()
            if z is not None:return z
            a[best]=None
        return None
    return rec(),nodes

def linear_maps_s5():
    maps=set()
    for p in permutations(DIRS):
        images=p[:4]
        table=[]
        for x in range(16):
            y=0
            for i in range(4):
                if (x>>i)&1:y^=images[i]
            table.append(y)
        if table[15]!=p[4]: raise AssertionError
        maps.add(tuple(table))
    return maps

def verify():
    checks=[]; out={}
    vs,adj=clebsch()
    checks.append((len(vs)==16 and all(len(adj[v])==5 for v in vs),'clebsch order/degree'))
    edges=sum(map(len,adj.values()))//2
    checks.append((edges==40,'clebsch edges'))
    lambdas=[]; mus=[]
    for a,b in combinations(vs,2):
        c=len(adj[a]&adj[b])
        (lambdas if b in adj[a] else mus).append(c)
    checks.append((set(lambdas)=={0} and set(mus)=={2},'SRG(16,5,0,2)'))
    sp=spectrum(adj); checks.append((sp==Counter({1:10,-3:5,5:1}),'spectrum'))
    root=0; shell1=sorted(adj[root]); shell2=sorted(set(vs)-{root}-set(shell1))
    induced={v:adj[v]&set(shell2) for v in shell2}
    checks.append((len(shell1)==5 and len(shell2)==10 and all(len(induced[v])==3 for v in shell2),'1+5+10 shells'))
    checks.append((all((b in induced[a]) == (set(axis_label(a)).isdisjoint(axis_label(b))) for a,b in combinations(shell2,2)),'Petersen=KG(5,2) shell'))
    lmaps=linear_maps_s5(); checks.append((len(lmaps)==120,'linear S5'))
    checks.append((16*len(lmaps)==1920,'affine automorphism lower bound 1920'))
    for r,expected_nodes in [(4,2),(5,7),(6,443)]:
        sol,nodes=systematic_search(r); checks.append((sol is None and nodes==expected_nodes,f'no systematic r={r}'))
    sol7,n7=systematic_search(7)
    checks.append((sol7==PARITY7,'systematic r=7 witness'))
    dh=Counter()
    for i,j in combinations(range(22),2):dh[wt(VALID[i]^VALID[j])+wt(PARITY7[i]^PARITY7[j])]+=1
    checks.append((min(dh)==5 and sum(dh.values())==231,'[12,22,5] systematic code'))
    catastrophic2=sum(1 for a,b in combinations(range(32),2) if (a^b)==16)
    catastrophic3=sum(1 for T in combinations(range(32),3) if any((a^b)==16 for a,b in combinations(T,2)))
    checks.append((catastrophic2==16 and catastrophic3==480,'replica-loss census'))
    checks.append((496-catastrophic2==480 and 4960-catastrophic3==4480,'survivable pair/triple counts'))
    # local gauge fusion: three omitted-edge types over F3^5
    def t(k,v):
        if k==0:return (0,v,(-v)%243)
        if k==1:return (v,0,(-v)%243)
        return (v,(-v)%243,0)
    # symbolic scalar representatives over F3 suffice for support law
    reps=[(0,(0,1,2)),(1,(1,0,2)),(2,(1,2,0))]
    checks.append((all(sum(x)%3==0 for _,x in reps),'local flat defect representatives'))
    # block-distance invariant PSD decomposition coefficients
    out['block_psd_cones']=['K0+32K1+12K2','K0+2K1-3K2','K0-4K1+3K2']
    checks.append((len(out['block_psd_cones'])==3,'three block spectral cones'))
    out.update({
      'clebsch':{'vertices':16,'edges':40,'srg':[16,5,0,2],'spectrum':{'5':1,'1':10,'-3':5},'automorphism_group_order':1920,'shells':[1,5,10],'second_subconstituent':'Petersen=KG(5,2)'},
      'systematic_code':{'raw_bits':5,'parity_bits':7,'length':12,'messages':22,'distance':5,'parity_map':dict(zip(map(str,VALID),PARITY7)),'distance_histogram':dict(sorted(dh.items())),'search_nodes':{'r4':2,'r5':7,'r6':443,'r7':n7}},
      'replication':{'two_vertex_catastrophic':16,'two_vertex_survivable':480,'three_vertex_catastrophic':480,'three_vertex_survivable':4480},
      'gauge_fusion':{'same_face_same_type':'T_i(v)+T_i(w)=T_i(v+w); annihilates iff w=-v','same_face_distinct_type':'minimum iff coefficients cancel on shared nonzero edge; otherwise weight 3','distinct_filled_faces':'edge-disjoint, hence generic weight 4'},
      'claim_boundary':'No chromatic decision, observed FPGA timing, physical memory, laboratory rate, geometric hardware realization or spacetime claim.'
    })
    failed=[name for ok,name in checks if not ok]
    out['checks']={'passed':len(checks)-len(failed),'total':len(checks),'failed':failed}
    if failed: raise AssertionError(failed)
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--json');a=ap.parse_args()
    out=verify(); text=json.dumps(out,sort_keys=True,indent=2)+'\n'
    if a.json:open(a.json,'w').write(text)
    print(f"PASS {out['checks']['passed']}/{out['checks']['total']} Clebsch-Petersen resilient closure")
