#!/usr/bin/env python3
"""Optimal five-load W33 apartment Hamiltonian: exact finite certificates.

Construct 81 GF(2)-independent oriented Levi octagons, with at most five
selected octagons through each flag. The 160x160 matrix H=BB^T is sparse,
positive semidefinite, non-scalar on the 81D Levi cycle subspace, and
exactly cut-decoupled. No physical continuum or TOE claim is made.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
import numpy as np

def canon(v):
    lead=next(x for x in v if x)
    return tuple((a*pow(lead,-1,3))%3 for a in v)

def symp(x,y):
    return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3

def build():
    points=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    assert len(points)==40
    point_idx={p:i for i,p in enumerate(points)}
    adj=[{j for j,y in enumerate(points) if i!=j and symp(x,y)==0}
         for i,x in enumerate(points)]
    lines=set()
    for i,x in enumerate(points):
        for j in sorted(adj[i]):
            if j<=i:continue
            y=points[j]
            L={point_idx[canon(tuple((a*x[k]+b*y[k])%3 for k in range(4)))]
               for a,b in itertools.product(range(3),repeat=2) if a or b}
            lines.add(tuple(sorted(L)))
    lines=sorted(lines)
    assert len(lines)==40 and all(len(L)==4 for L in lines)
    pairline={}
    for j,L in enumerate(lines):
        for a,b in itertools.combinations(L,2):
            pairline[a,b]=pairline[b,a]=j
    flags=sorted((i,j) for j,L in enumerate(lines) for i in L)
    index={f:i for i,f in enumerate(flags)}
    D=np.zeros((80,160),dtype=np.int64)
    for i,(p,j) in enumerate(flags):
        D[p,i]=-1
        D[40+j,i]=1
    cycles={}
    for p in range(40):
        for q in range(p+1,40):
            if q in adj[p]:continue
            common=sorted(adj[p]&adj[q])
            assert len(common)==4
            for a,b in itertools.combinations(common,2):
                walk=[p,40+pairline[p,a],a,40+pairline[a,q],q,
                      40+pairline[q,b],b,40+pairline[b,p],p]
                col=np.zeros(160,dtype=np.int64)
                for u,v in zip(walk,walk[1:]):
                    e=index[(u,v-40)] if u<40 else index[(v,u-40)]
                    col[e]=1 if u<40 else -1
                cycles.setdefault(tuple(np.flatnonzero(col).tolist()),col)
    C=np.stack(list(cycles.values()),axis=1)
    assert C.shape==(160,1620) and not np.any(D@C)
    return D,C,flags

def choose(C,seed=1):
    supports=[np.flatnonzero(C[:,j]) for j in range(C.shape[1])]
    masks=[sum(1<<int(e) for e in s) for s in supports]
    tie=np.random.default_rng(seed).random(len(supports))
    load=np.zeros(160,dtype=np.int64)
    pivots={}
    picked=[]
    for _ in range(81):
        order=sorted(range(len(supports)),key=lambda j:(
            int(max(load[supports[j]]+1)),
            int(sum(load[supports[j]])),
            int(sum((load[supports[j]]+1)**2)),
            float(tie[j])))
        for j in order:
            mask=masks[j]
            for b in pivots.values():
                mask=min(mask,mask^b)
            if mask:
                pivots[mask.bit_length()-1]=mask
                picked.append(j)
                load[supports[j]]+=1
                break
        else:raise RuntimeError("81-cycle spanning failed")
    return picked,load

def verify():
    D,C,flags=build()
    K=C@C.T
    assert np.array_equal(K@K,160*K)
    assert np.all(np.diag(K)==81)
    picked,load=choose(C)
    B=C[:,picked]
    H=B@B.T
    A=np.abs(D).T@np.abs(D)-2*np.eye(160,dtype=np.int64)
    assert len(picked)==81 and int(load.sum())==648
    assert int(max(load))==5==(648+159)//160
    assert not np.any(D@B) and not np.any(D@H)
    assert not np.any(A@H+2*H) and not np.any(H@A+2*H)
    assert np.any(160*H!=8*K)  # cannot be a scalar on protected H1
    assert np.array_equal(H,H.T) and np.array_equal(np.diag(H),load)
    off=np.count_nonzero(H,axis=1)-1
    assert int(off.max())<=35
    ev=np.linalg.eigvalsh(H.astype(float))
    assert ev[-81]>0 and abs(ev[-82])<1e-9
    witness=[list(map(int,np.flatnonzero(B[:,j]))) for j in range(81)]
    hashval=hashlib.sha256(json.dumps(witness,separators=(',',':')).encode()).hexdigest()
    return {
      "status":"PASS_EXACT_OPTIMAL_FIVE_LOAD_APARTMENT_BASIS",
      "scope":"Finite W(3,3) incidence construction; not emergent spacetime or physical quantum gravity",
      "flags":160,"levi_vertices":80,"apartments_all":1620,
      "apartments_selected":81,"apartment_support_size":8,
      "GF2_independent":True,"Q_independent":True,
      "max_flag_load":int(max(load)),
      "optimal_lower_bound":"ceil(81*8/160)=5",
      "load_histogram":{str(k):int(v) for k,v in sorted(Counter(load.tolist()).items())},
      "H_definition":"B B^T on flag edges",
      "boundary_zero":bool(not np.any(D@H)),
      "A_H_equals_minus2_H":bool(not np.any(A@H+2*H)),
      "H_non_scalar_in_H1":bool(np.any(160*H!=8*K)),
      "H_nnz":int(np.count_nonzero(H)),
      "H_max_offdiagonal_neighbors":int(max(off)),
      "H_numerical_active_eigenvalue_range":[float(ev[-81]),float(ev[-1])],
      "H_numerical_distinct_active_eigenvalues_round7":len(set(np.round(ev[-81:],7))),
      "supports_sha256":hashval,
      "witness_apartment_flag_supports":witness,
      "limitations":"GF2 and Q bases are not claimed unimodular over Z; symmetry is broken by basis selection; arbitrary onsite disorder leaks; a finite sparse matrix is not a physical dispersion/continuum law."
    }

def main():
    result=verify()
    target=Path(__file__).resolve().parents[1]/"data"/"2026_11_03_optimal_5load_apartment_hamiltonian.json"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("CERTIFIED",result["status"],"hash",result["supports_sha256"])
    return result

if __name__=="__main__":
    main()
