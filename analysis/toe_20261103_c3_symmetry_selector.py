#!/usr/bin/env python3
"""C3-equivariant independent 81-apartment cycle basis; finite math only.

An explicit 27-orbit GF(2) basis, with maximum flag load 6, yields a
non-scalar Hamiltonian exactly invariant under one symplectic transvection.
No subgroup, cosmological mechanism or continuum is dynamically selected.
"""
from __future__ import annotations
from collections import Counter
from itertools import product
from pathlib import Path
import importlib.util, json, math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"analysis"/"2026_11_03_optimal_5load_apartment_hamiltonian.py"
spec=importlib.util.spec_from_file_location("base",BASE)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
OUT=ROOT/"data"/"toe_20261103_c3_symmetry_selector.json"

def reduce_mask(mask,pivots):
    for k in sorted(pivots,reverse=True):
        if (mask>>k)&1:mask ^= pivots[k]
    return mask

def certificate(seed=2,save=True):
    D,C,flags=mod.build()
    supports=sorted(tuple(int(k) for k in np.flatnonzero(C[:,j])) for j in range(C.shape[1]))
    by_support={tuple(np.flatnonzero(C[:,j])):C[:,j] for j in range(C.shape[1])}
    points=sorted({mod.canon(v) for v in product(range(3),repeat=4) if any(v)})
    pidx={p:i for i,p in enumerate(points)}
    lines=[[] for _ in range(40)]
    for p,l in flags:lines[l].append(p)
    lines=[tuple(sorted(x)) for x in lines]
    lidx={x:i for i,x in enumerate(lines)}
    fidx={x:i for i,x in enumerate(flags)}
    vector=points[0]
    pointperm=[pidx[mod.canon(tuple((x[k]+mod.symp(x,vector)*vector[k])%3 for k in range(4)))] for x in points]
    lineperm=[lidx[tuple(sorted(pointperm[p] for p in line))] for line in lines]
    fp=np.array([fidx[(pointperm[p],lineperm[l])] for p,l in flags],dtype=int)
    index={s:i for i,s in enumerate(supports)}
    cp=[index[tuple(sorted(int(fp[k]) for k in supp))] for supp in supports]
    seen=set();orbits=[]
    for i in range(len(supports)):
        if i in seen:continue
        o=[];j=i
        while j not in seen:
            seen.add(j);o.append(j);j=cp[j]
        assert j==i
        orbits.append(o)
    assert len(orbits)==540 and all(len(o)==3 for o in orbits)
    fixedpoints=sum(i==p for i,p in enumerate(pointperm))
    fixedlines=sum(i==l for i,l in enumerate(lineperm))
    fixedflags=int(sum(i==e for i,e in enumerate(fp)))
    chartrace=int(fixedflags-fixedpoints-fixedlines+1)
    assert (fixedpoints,fixedlines,fixedflags,chartrace)==(13,4,16,0)
    bits=[sum(1<<k for k in supp) for supp in supports]
    incidence=np.zeros((len(orbits),160),dtype=np.int8)
    for o,ids in enumerate(orbits):
        for j in ids:incidence[o,list(supports[j])]+=1
    tie=np.random.default_rng(seed).random(len(orbits))
    load=np.zeros(160,dtype=int);pivots={};chosen=[]
    for step in range(27):
        candidates=sorted(range(len(orbits)),key=lambda j:(
            int(max(load+incidence[j])),
            int(np.maximum(load+incidence[j]-4,0).sum()),
            int(np.sum((load+incidence[j])**2)),float(tie[j])))
        for j in candidates:
            trial=pivots.copy()
            for k in orbits[j]:
                mask=reduce_mask(bits[k],trial)
                if mask:trial[mask.bit_length()-1]=mask
            if len(trial)-len(pivots)==3:
                pivots=trial;chosen.append(j);load+=incidence[j]
                break
        else:raise AssertionError("C3 orbit selection stalled")
    assert len(chosen)==27 and len(pivots)==81 and max(load)==6
    picked=[i for o in chosen for i in orbits[o]]
    B=np.stack([by_support[supports[i]] for i in picked],axis=1).astype(np.int64)
    H=B@B.T
    moved=np.zeros_like(H);moved[np.ix_(fp,fp)]=H
    assert not np.any(D@B) and np.array_equal(H,moved)
    assert not np.allclose(H,np.trace(H)/81.0*(C@C.T)/160.0)
    A=np.abs(D).T@np.abs(D)-2*np.eye(160,dtype=np.int64)
    assert not np.any(A@H+2*H) and not np.any(D@H)
    eig=np.linalg.eigvalsh((B.T@B).astype(float))
    assert min(eig)>0
    out=dict(status="PASS_EXACT_C3_EQUIVARIANT_81_APARTMENT_BASIS",
        points=40,lines=40,flags=160,apartments=1620,apartment_orbits=540,
        transvection_fixed_points=fixedpoints,transvection_fixed_lines=fixedlines,
        transvection_fixed_flags=fixedflags,cycle_character_trace=chartrace,
        chosen_orbits=27,chosen_cycles=81,cycle_GF2_rank=81,
        selected_orbit_indices=chosen,selected_apartment_flag_supports=[list(supports[j]) for j in picked],
        max_flag_load=int(max(load)),load_histogram={str(k):int(v) for k,v in sorted(Counter(load).items())},
        edge_hoppings=int(np.count_nonzero(np.triu(H,1))),
        C3_H_invariant=True,cut_leakage_exact_zero=True,
        positive_eigen_min=float(eig[0]),positive_eigen_max=float(eig[-1]),
        condition_number=float(eig[-1]/eig[0]),
        limitation="Noncanonical cyclic subgroup anchored at projective point 0; max-load-six existence only, no load-five impossibility or dynamical selection.")
    if save:
        OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
        print(out["status"],out["edge_hoppings"],round(out["condition_number"],2),flush=True)
    return out

if __name__=="__main__":certificate()
