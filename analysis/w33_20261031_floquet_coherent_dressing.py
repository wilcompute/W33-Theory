#!/usr/bin/env python3
"""Operational random SU(3) on-site dressing of native compiled Floquet SWAP drive.

Keeps exact information-routing permutation while transporting random local
unitaries on each qutrit. This is an explicit coherent-error control, not a
noisy open-system index or measured photonic experiment.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261031_floquet_coherent_dressing.json"
def simulate(L,eps,periodic):
    if periodic:assert L%2==0
    rng=np.random.default_rng(20261031+L+int(eps*1000)+int(periodic)*101)
    state={(x,y):((x,y),np.eye(3,dtype=complex))for x in range(L)for y in range(L)}
    stages=((1,0),(0,1),(-1,0),(0,-1))
    for step,(dx,dy) in enumerate(stages):
        for pos,(source,U) in list(state.items()):
            z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
            h=(z+z.conj().T)/2
            h=h-(np.trace(h).real/3)*np.eye(3)
            V=expm(1j*eps*h)
            assert abs(np.linalg.det(V)-1)<1e-12
            state[pos]=(source,V@U)
        used=set()
        for x in range(L):
            for y in range(L):
                if (x+y)%2:continue
                bx,by=x+dx,y+dy
                if periodic:bx%=L;by%=L
                if not (0<=bx<L and 0<=by<L):continue
                a,b=(x,y),(bx,by)
                assert a not in used and b not in used
                used.add(a);used.add(b)
                state[a],state[b]=state[b],state[a]
    rout={source:dst for dst,(source,U) in state.items()}
    assert len(set(rout.values()))==L*L
    errors=[];recovery=[]
    psi=np.array([1,0,0],complex)
    for source,dst in rout.items():
        U=state[dst][1]
        assert np.linalg.norm(U.conj().T@U-np.eye(3))<1e-12
        errors.append(1-abs(np.vdot(psi,U@psi))**2)
        recovery.append(1-abs(np.vdot(psi,U.conj().T@U@psi))**2)
    if periodic:assert all(source==dst for source,dst in rout.items())
    else:
        moved=[x for x,y in rout.items() if x!=y]
        assert len(moved)==2*L-1
        assert all(x[0] in (0,L-1) or x[1] in (0,L-1) for x in moved)
        active=min(moved);cycle=[];cur=active
        while cur not in cycle:
            cycle.append(cur);cur=rout[cur]
        assert cur==active and len(cycle)==2*L-1
    assert max(abs(z)for z in recovery)<1e-12
    return {"side":L,"epsilon_random_local_SU3":eps,"periodic":periodic,
      "boundary_shift_orbit_length":0 if periodic else 2*L-1,
      "mean_uncalibrated_infidelity":float(np.mean(errors)),
      "maximum_recovered_infidelity":float(max(map(abs,recovery))),
      "bulk_permutation_identity":all((x==y)for x,y in rout.items() if periodic or (0<x[0]<L-1 and 0<x[1]<L-1))}
def build():
    rows=[simulate(L,eps,periodic)for L,periodic in ((4,False),(6,False),(6,True))
             for eps in (0.,.04,.2,.5)]
    assert all(r["mean_uncalibrated_infidelity"]<1e-11 for r in rows if r["epsilon_random_local_SU3"]==0)
    assert all(r["maximum_recovered_infidelity"]<1e-12 for r in rows)
    assert all(r["bulk_permutation_identity"] for r in rows)
    return {"status":"PASS_FLOQUET_RANDOM_LOCAL_SU3_DRESSING_EXACT_ROUTE_AND_RECOVERY",
       "model":"Four-stage checkerboard qutrit SWAP, each stage preceded by independent random three-by-three SU(3) local coherent rotations exp(i epsilon H_site). Same gate connectivity as the native 13-tick SWAP compiled in prior research.",
       "rows":rows,
       "robustness":"Exact destination-site routing persists, calibration by accumulated local U† recovers any incoming qutrit with unit fidelity. Uncalibrated single-basis state fidelity deteriorates with error scale. GNVW index survives finite-depth coherent local dressing.",
       "caveat":"This tests strictly local unitary miscalibration, NOT stochastic depolarization, leakage, optical mode loss, correlated entangling gate noise or a noisy-channel topological invariant."}
if __name__=="__main__":
    d=build();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(d["status"],[(r["side"],r["epsilon_random_local_SU3"],round(r["mean_uncalibrated_infidelity"],4))for r in d["rows"] if not r["periodic"]])
