#!/usr/bin/env python3
"""Electrical-resistance renormalization probe on the mod-3 Pascal support.

This is a *dimensionless network* benchmark, not a derived physical length.
No asserted exact asymptotic resistance factor or spacetime dimension.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"data"/"2026_11_03_pascal_resistance_flow.json"

def lucas_nonzero(n,k):
    while n or k:
        if k%3>n%3: return False
        n//=3; k//=3
    return True

def graph(level, full=False):
    w=3**level
    sites=sorted((n,k) for n in range(w) for k in range(n+1)
                 if full or lucas_nonzero(n,k))
    N=len(sites)
    assert N==(w*(w+1)//2 if full else 6**level)
    ids={point:i for i,point in enumerate(sites)}
    rr=[];cc=[];vv=[]
    E=0
    for i,(n,k) in enumerate(sites):
        for neighbor in ((n,k+1),(n+1,k),(n+1,k+1)):
            j=ids.get(neighbor)
            if j is None:continue
            rr.extend((i,i,j,j));cc.extend((i,j,i,j))
            vv.extend((1,-1,-1,1));E+=1
    lap=coo_matrix((np.asarray(vv,dtype=np.float64),(rr,cc)),
                   shape=(N,N)).tocsr()
    # Tested graph-edge recurrence E_n=6 E_(n-1)+9; it gives:
    if not full: assert E==9*(6**level-1)//5
    return sites,ids,lap,E

def resistance(level, full=False):
    sites,ids,lap,edges=graph(level, full=full)
    source=ids[(0,0)];ground=ids[(3**level-1,0)]
    mask=np.ones(len(sites),dtype=bool)
    mask[ground]=False
    rhs=np.zeros(len(sites));rhs[source]=1;rhs[ground]=-1
    sol=spsolve(lap[mask][:,mask],rhs[mask])
    voltage=np.zeros(len(sites));voltage[mask]=sol
    R=float(voltage[source]-voltage[ground])
    residual=lap@voltage-rhs
    error=float(np.max(np.abs(residual)))
    energy=float(voltage@(lap@voltage))
    assert R>0 and abs(R-energy)<1e-6*max(1,R)
    assert error<3e-6
    return dict(level=level,root_to_corner_graph_distance=3**level-1,
                vertices=len(sites),edges=edges,effective_resistance=R,
                residual_l_infinity=error,energy_identity_error=abs(R-energy))

def run():
    rows=[resistance(j) for j in range(1,7)]
    controls=[resistance(j,full=True) for j in range(1,6)]
    ratios=[rows[i]["effective_resistance"]/rows[i-1]["effective_resistance"]
            for i in range(1,len(rows))]
    assert all(x>1 for x in ratios)
    # Diagnostic only: this nonstandard triangular-cell adjacency differs
    # from standard SG_3 boundary approximants; do not assume renorm=15/7.
    ans=dict(
      status="PASS_SPARSE_LAPLACIAN_KIRCHHOFF_ENERGY",
      construction="First 3^n Pascal rows with binomial(n,k) nonzero mod 3; connect triangular nearest neighbors; one unit conductance per edge.",
      data=rows,observed_consecutive_resistance_ratios=ratios,
      regular_triangular_lattice_negative_control=controls,
      control_interpretation="The same unit-edge network without Pascal deletions has corner resistance growing approximately linearly in refinement depth (logarithmically in side length); this is not the Pascal 15/7 multiplicative scaling.",
      base3_box_dimension=math.log(6)/math.log(3),
      candidate_asymptotic_ratio="unknown; data suggest a ratio around 2.1-2.2, but 15/7 is not established for this graph",
      possible_dynamic_scaling="If a positive limiting resistance multiplier r exists, proposed walk dimension is log_3(6*r), spectral dimension 2 log(6)/log(6*r). Both require proof of r and appropriate random-walk convergence.",
      absolute_scale_boundary="All conductances were set to 1. This yields relative impedance/time ratios only. No absolute physical meter, Planck unit, light speed, graviton or 4D spacetime is selected.",
      independent_checks="Kirchhoff residual and dissipated energy = effective resistance for every n.",
      classifications="Numerical experiment on a specified graph family, not original claim about Pascal fractals or a physical theory."
    )
    OUTPUT.parent.mkdir(exist_ok=True,parents=True)
    OUTPUT.write_text(json.dumps(ans,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASSED_RESISTANCES",[(a["level"],a["vertices"],round(a["effective_resistance"],8)) for a in rows],flush=True)
    print("RATIOS",ratios,flush=True)
    print("FULL_TRIANGLE_CONTROLS",[(a["level"],round(a["effective_resistance"],8)) for a in controls],flush=True)
    return ans
if __name__=="__main__":run()
