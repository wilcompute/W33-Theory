#!/usr/bin/env python3
"""C3 symmetry-equivariant orbit-frame spectral sparsification (finite W33).

Select whole length-three symplectic transvection orbits of eight-cycle
apartments via a deterministic Frobenius discrepancy design. Start with an
already certified GF2-independent 81-cycle seed. Verify exact divergence-free
identities and C3 symmetry; numeric 81D eigenvalues are only benchmarks.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
from collections import Counter
import importlib.util,json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_c3_orbit_sparsification.json"

def imp(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
c3=imp("c3_orbit_prev","analysis/toe_20261103_c3_symmetry_selector.py")
base=c3.mod

def orbit_data(C,flags):
    pts=sorted({base.canon(v) for v in product(range(3),repeat=4) if any(v)})
    pidx={p:i for i,p in enumerate(pts)}
    lines=[[] for _ in range(40)]
    for p,l in flags:lines[l].append(p)
    lines=[tuple(sorted(x)) for x in lines]
    lidx={line:i for i,line in enumerate(lines)}
    fidx={fl:i for i,fl in enumerate(flags)}
    v=pts[0]
    pointperm=[pidx[base.canon(tuple((x[k]+base.symp(x,v)*v[k])%3 for k in range(4)))] for x in pts]
    lineperm=[lidx[tuple(sorted(pointperm[p] for p in line))] for line in lines]
    fp=np.array([fidx[(pointperm[p],lineperm[l])] for p,l in flags],dtype=int)
    supports=[tuple(np.flatnonzero(C[:,j]).tolist()) for j in range(C.shape[1])]
    smap={s:i for i,s in enumerate(supports)}
    order=sorted(range(len(supports)),key=lambda j:supports[j])
    cp=[smap[tuple(sorted(int(fp[k]) for k in supports[j]))] for j in range(C.shape[1])]
    done=set();orbits=[]
    for j in order:
        if j in done:continue
        o=[];u=j
        while u not in done:
            done.add(u);o.append(u);u=cp[u]
        assert u==j and len(o)==3
        orbits.append(o)
    assert len(orbits)==540 and len(done)==1620
    return orbits,fp

def run():
    D,C,flags=base.build()
    orbits,fp=orbit_data(C,flags)
    initial=c3.certificate(seed=2,save=False)["selected_orbit_indices"]
    assert len(initial)==27
    selected=list(initial)
    flat_ids=np.array([i for orbit in orbits for i in orbit],dtype=np.int64)
    Cflat=C[:,flat_ids].astype(float)
    cross=Cflat.T@Cflat
    # (orbit_a,component,orbit_b,component), squared Gram inner products.
    G=(cross.reshape(540,3,540,3)**2).sum(axis=(1,3))
    assert G.shape==(540,540) and np.allclose(G,G.T)
    diag=G.diagonal().copy()
    score=diag+2*G[:,selected].sum(axis=1)
    chosen=np.zeros(540,dtype=bool);chosen[selected]=True
    targets=(27,36,54,81,108,135,162,216,270,405,540)
    controls=[]
    Q,_=np.linalg.qr(C[:,base.choose(C,seed=33)[0]].astype(float))
    K=C@C.T
    assert np.array_equal(K@K,160*K)
    def snapshot(m):
        picks=np.array([i for o in selected for i in orbits[o]],dtype=int)
        B=C[:,picks].astype(np.int64)
        H=B@B.T
        assert np.array_equal(D@H,np.zeros((80,160),dtype=np.int64))
        conjugate=np.zeros_like(H);conjugate[np.ix_(fp,fp)]=H
        assert np.array_equal(H,conjugate)
        ev=np.linalg.eigvalsh(Q.T@H@Q)
        assert ev[0]>1e-8
        mean=24*m/81
        support=(H!=0)
        np.fill_diagonal(support,False)
        degree=support.sum(axis=1)
        return dict(orbit_count=m,cycle_count=3*m,
          full_basis_protected_rank=81,
          nonzero_positive_min=float(ev[0]),nonzero_positive_max=float(ev[-1]),
          condition_number=float(ev[-1]/ev[0]),
          normalized_frame_max_eigen_error=float(max(abs(ev-mean))/mean),
          normalized_frame_rms_eigen_error=float(np.sqrt(np.mean((ev-mean)**2))/mean),
          undirected_hoppings=int(np.count_nonzero(np.triu(support,1))),
          max_flag_neighbors=int(max(degree)),
          max_flag_cycle_load=int(max(np.diag(H))),
          selected_orbit_indices=list(selected) if m in (27,81,108,216,540) else None)
    controls.append(snapshot(27))
    for m in range(28,541):
        score[chosen]=np.inf
        k=int(np.argmin(score))
        assert not chosen[k]
        selected.append(k);chosen[k]=True
        score+=2*G[:,k]
        if m in targets:controls.append(snapshot(m))
    assert controls[-1]["condition_number"]<1+1e-9
    assert controls[-1]["undirected_hoppings"]==12720
    out=dict(status="PASS_EXACT_C3_ORBIT_FRAME_SPARSIFICATION",
      orbit_count=540,total_apartment_cycles=1620,seed_basis_orbits=27,
      full_frame_identity="C C^T=160 P_cycle, exact integer identity",
      method="GF2 independent C3-seed 2 followed by greedy minimization of Frobenius frame discrepancy, selecting complete 3-cycle orbits",
      comparison=controls,
      limitation="Spectral numbers are numerical and stages after 27 are heuristic. C3 symmetry does not choose itself; H is nonlocal in edge modes. Spectral sparsification is established prior art, not a new theorem.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for c in controls:
        print("STAGE",c["orbit_count"],"cond",round(c["condition_number"],4),
             "hoppings",c["undirected_hoppings"],"neighbors",c["max_flag_neighbors"],flush=True)
    return out
if __name__=="__main__":run()
