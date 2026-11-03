#!/usr/bin/env python3
"""Dimensionless photonic continuous-time quantum-walk falsifier on Pascal cells.

H=J L physically requires site detunings proportional to vertex degree;
Jt/hbar is one dimensionless control. No real device was built or simulated
at Maxwell/photonic fabrication level.
"""
from __future__ import annotations
from pathlib import Path
import runpy,json
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import expm_multiply
ROOT=Path(__file__).resolve().parents[1]
G=runpy.run_path(str(ROOT/"analysis"/"2026_11_03_pascal_resistance_flow.py"))
OUT=ROOT/"data"/"2026_11_03_pascal_photonic_falsifier.json"

def evolution(L,index,t):
    n=L.shape[0];source=np.zeros(n,dtype=np.complex128);source[index]=1
    psi=expm_multiply((-1j*t)*L.astype(np.complex128),source)
    p=np.abs(psi)**2
    assert abs(sum(p)-1)<2e-10,(n,t,sum(p))
    heat=np.real(expm_multiply(-t*L,source))
    assert min(heat)>-1e-10,(n,t,min(heat))
    assert abs(sum(heat)-1)<2e-10
    return p,heat

def random_disorder(L,sites,frac,seed):
    rng=np.random.default_rng(seed)
    # Symmetric positive nearest-neighbor couplings; preserve continuity.
    ids={u:i for i,u in enumerate(sites)}
    A=lil_matrix(L.shape,dtype=float)
    for u,v in zip(*np.triu_indices(len(sites),k=1)):
        # Avoid O(n²) scans in future large lattices; only n<=216 here.
        if L[u,v]>=0:continue
        weight=-L[u,v]*(1+frac*rng.uniform(-1,1))
        A[u,u]+=weight;A[v,v]+=weight;A[u,v]-=weight;A[v,u]-=weight
    return A.tocsr()

def one(level,full=False):
    sites,ids,L,edges=G["graph"](level,full=full)
    w=3**level
    ix=ids[(0,0)]
    corners=[ids[z] for z in ((0,0),(w-1,0),(w-1,w-1))]
    phases=[]
    for t in (.25,1.,2.,4.,8.):
        prob,heat=evolution(L,ix,t)
        phases.append({"dimensionless_time":t,
           "root_return_quantum":float(prob[ix]),
           "far_corner_quantum_left":float(prob[corners[1]]),
           "far_corner_quantum_right":float(prob[corners[2]]),
           "root_return_classical":float(heat[ix]),
           "far_corner_classical_left":float(heat[corners[1]]),
           "far_corner_classical_right":float(heat[corners[2]]),
           "participation_ratio_quantum":float(1/sum(prob**2)),
           "participation_ratio_classical":float(1/sum(heat**2))})
    return dict(level=level,full=full,vertices=len(sites),edges=edges,phases=phases)

def compare(level,t):
    sites,ids,L,_=G["graph"](level)
    fullsites,fullids,LF,_=G["graph"](level,full=True)
    p,_=evolution(L,ids[(0,0)],t)
    q,_=evolution(LF,fullids[(0,0)],t)
    padded=np.zeros(len(fullsites))
    for v,prob in zip(sites,p):padded[fullids[v]]=prob
    tv=float(sum(abs(padded-q))/2)
    overlap=float(sum(q[fullids[v]] for v in sites))
    assert 0<=tv<=1+1e-8
    return tv,overlap

def run():
    cases=[one(level,full=full) for level in (1,2,3)
           for full in (False,True)]
    controls=[]
    for level in (2,3):
        for t in (1.,2.,4.,8.):
            tv,retained=compare(level,t)
            controls.append({"level":level,"dimensionless_time":t,
                "total_variation_quantum_vs_undeleted_triangle":tv,
                "full_triangle_probability_on_retained_sites":retained})
    assert all(x["total_variation_quantum_vs_undeleted_triangle"]>0.005 for x in controls)
    # Tolerance to fabrication-like symmetric ±5% coupling disorder, with
    # no calibration of absolute couplings and no claim of experimental robustness.
    dcases=[]
    for level in (2,3):
        sites,ids,L,_=G["graph"](level)
        base,_=evolution(L,ids[(0,0)],4.0)
        for seed in range(6):
            perturbed=random_disorder(L,sites,.05,seed)
            test,_=evolution(perturbed,ids[(0,0)],4.0)
            TV=float(np.sum(abs(base-test))/2)
            dcases.append({"level":level,"seed":seed,
                          "relative_coupling_disorder_max":0.05,
                          "distribution_total_variation":TV})
    out={
     "status":"PASS_UNITARY_WALK_MARKOV_CONTROL_AND_DISORDER",
     "hamiltonian":"H=J*L; vertex onsite beta_v=J deg(v); each edge coupling -J. Optical propagation coordinate z produces tau=Jz with hbar set by wave equation; all values dimensionless.",
     "unweighted_graphs":"For n=1,2,3 Pascal Lucas support vs undeleted triangular lattice, identical side length and unit nearest-neighbor coupling.",
     "quantum_unitarity_and_classical_mass_test":True,
     "observable":"Single-site injection; coherent root return, two far-corner probabilities, spatial inverse participation ratio; classical heat-semigroup negative controls. Distinguish quantum interference and deleted-site connectivity.",
     "experimental_interpretation":"Possible 36-site and 216-site laser-written waveguide arrays or programmable optical circuits; requires onsite detunings, coupling calibration, propagation-loss and polarization controls. This is numerical Hamiltonian propagation, not a fabricated or validated device.",
     "absolute_scale_underdetermination":"All distributions depend on tau=J*z only; a ratio of coupling strength to device length must be calibrated externally.",
     "simulation":cases,
     "full_lattice_negative_controls":controls,
     "symmetric_disorder_5pct_tests":dcases,
     "literature":["https://doi.org/10.1038/s41566-021-00845-4","https://doi.org/10.1038/s41566-021-00868-x","https://pmc.ncbi.nlm.nih.gov/articles/PMC5947980/"]
    }
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS PHOTONIC:",len(cases),"walk models",len(controls),"negative controls",
          len(dcases),"disorder cases")
    print("QUANTUM TV",[(x["level"],x["dimensionless_time"],round(x["total_variation_quantum_vs_undeleted_triangle"],4)) for x in controls])
    return out
if __name__=="__main__":run()
