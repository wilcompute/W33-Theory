#!/usr/bin/env python3
"""Natural selector--Levi cross-orbital bimodule and Steinberg obstruction."""
from __future__ import annotations
import collections, hashlib, itertools, json
import numpy as np
import sympy as sp

P=1000003

def rankmod(A,p=P):
    A=np.array(A,dtype=np.int64)%p; m,n=A.shape; r=0
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if not len(nz): continue
        k=r+int(nz[0]); A[[r,k]]=A[[k,r]]; A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        for i in range(m):
            if i!=r and A[i,c]: A[i]=(A[i]-int(A[i,c])*A[r])%p
        r+=1
        if r==m: break
    return r

def analyze(g):
    pairs=[(s,flag) for s,(flag,_point) in g['seen'].items()]
    unseen=set(range(120*160)); orbits=[]
    while unseen:
        z=min(unseen); x,f=divmod(z,160)
        orbit={s[x]*160+ff[f] for s,ff in pairs}; orbits.append(orbit); unseen-=orbit
    assert len(orbits)==4
    maps=[]
    for orbit in orbits:
        M=np.zeros((160,120),dtype=np.int64)
        for z in orbit:
            x,f=divmod(z,160); M[f,x]=1
        maps.append(M)

    flags=g['flags']; adjacency=np.zeros((160,160),dtype=np.int64)
    for i,(p,l) in enumerate(flags):
        for j,(q,m) in enumerate(flags):
            if i!=j and (p==q or l==m): adjacency[i,j]=1
    distances=np.full((160,160),99,dtype=int); np.fill_diagonal(distances,0)
    for source in range(160):
        queue=collections.deque([source])
        while queue:
            u=queue.popleft()
            for v in np.flatnonzero(adjacency[u]):
                if distances[source,v]==99: distances[source,v]=distances[source,u]+1; queue.append(v)
    assert distances.max()==4 and [int((distances==d).sum(axis=1)[0]) for d in range(5)]==[1,6,18,54,81]

    selector_A=sum(i*g['relations'][i].astype(np.int64) for i in range(5))
    selector_eigs=[371,11,-19,-10,2]; selector_mults=[1,15,24,20,60]
    def projector_mod(A,eigenvalues,target):
        I=np.eye(A.shape[0],dtype=np.int64)%P; out=I.copy(); den=1
        for mu in eigenvalues:
            if mu==target: continue
            out=out@((A-mu*I)%P)%P; den=den*((target-mu)%P)%P
        return out*pow(int(den),-1,P)%P
    SP=[projector_mod(selector_A%P,[x%P for x in selector_eigs],x%P) for x in selector_eigs]
    assert [rankmod(x) for x in SP]==selector_mults
    roots=sp.sqrt_mod(6,P,all_roots=True); root=int(roots[0])
    flag_eigs=[6,(2+root)%P,2,(2-root)%P,(-2)%P]; flag_mults=[1,24,30,24,81]
    FP=[projector_mod(adjacency%P,flag_eigs,x) for x in flag_eigs]
    assert [rankmod(x) for x in FP]==flag_mults

    channels=[]
    for fi in range(5):
        for si in range(5):
            projected=[FP[fi]@(M%P)@SP[si]%P for M in maps]
            hom=rankmod(np.stack([X.reshape(-1) for X in projected]))
            if hom:
                channels.append({'selector_index':si,'flag_index':fi,
                    'selector_sector_dimension':selector_mults[si],
                    'flag_sector_dimension':flag_mults[fi],
                    'hom_dimension':hom,'map_rank':max(rankmod(X) for X in projected)})
    best=(0,None)
    for coefficients in itertools.product(range(-2,3),repeat=4):
        if all(c==0 for c in coefficients): continue
        M=sum((c*X for c,X in zip(coefficients,maps)),start=np.zeros((160,120),dtype=np.int64))
        r=rankmod(M)
        if r>best[0]: best=(r,coefficients)
    selector_comp=[A.T@B for A in maps for B in maps]
    flag_comp=[A@B.T for A in maps for B in maps]
    result={
      'cross_orbits':4,'cross_orbit_sizes':[len(o) for o in orbits],
      'cross_bidegrees':[{'flags_per_selector':int(M.sum(axis=0)[0]),'selectors_per_flag':int(M.sum(axis=1)[0])} for M in maps],
      'hom_G_dimension':4,'channels':channels,'maximum_cross_map_rank':best[0],
      'maximum_rank_coefficients':list(best[1]),
      'selector_composition_span_dimension':rankmod(np.stack([X.reshape(-1) for X in selector_comp])),
      'flag_composition_span_dimension':rankmod(np.stack([X.reshape(-1) for X in flag_comp])),
      'steinberg_81_channel_present':any(c['flag_sector_dimension']==81 for c in channels),
      'conclusion':'The natural 120-selector/160-flag cross-orbital bimodule has four channels but annihilates the flag Steinberg-81 sector. It is not a Morita bridge; the 2160 rectangle/apartment sheets remain the verified route to Levi E4.',
    }
    raw=json.dumps(result,sort_keys=True,separators=(',',':')); result['sha256']=hashlib.sha256(raw.encode()).hexdigest()
    return result
