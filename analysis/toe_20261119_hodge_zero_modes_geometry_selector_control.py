#!/usr/bin/env python3
"""Hodge-Dirac zero-mode sign test: topology-selective det may prefer WRONG phase.

Construct square cellular torus versus filled disk, exact incidence
boundary chain, 1-form combinatorial Hodge Laplacian. This is NOT a
spinorial chiral Dirac operator, a causal dynamic, or comparable physical
path-integral weight across complexes with different dimensions.
"""
from pathlib import Path
import numpy as np
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_hodge_zero_modes_geometry_selector_control.json"

def torus_cellular_operators(n):
    V=n*n;E=2*V;F=V
    B1=np.zeros((V,E),dtype=int)
    B2=np.zeros((E,F),dtype=int)
    def v(x,y):return (x%n)*n+y%n
    def h(x,y):return 2*v(x,y)
    def vv(x,y):return 2*v(x,y)+1
    for x in range(n):
        for y in range(n):
            B1[v(x,y),h(x,y)]-=1
            B1[v(x+1,y),h(x,y)]+=1
            B1[v(x,y),vv(x,y)]-=1
            B1[v(x,y+1),vv(x,y)]+=1
            f=v(x,y)
            for e,sgn in ((h(x,y),+1),(vv(x+1,y),+1),
                          (h(x,y+1),-1),(vv(x,y),-1)):
                B2[e,f]+=sgn
    return B1,B2

def filled_square_cellular_operators():
    B1=np.zeros((4,4),dtype=int)
    for i in range(4):
        B1[i,i]-=1
        B1[(i+1)%4,i]+=1
    B2=np.ones((4,1),dtype=int)
    return B1,B2

def analyze(B1,B2):
    assert not np.any(B1@B2)
    V,E=B1.shape;E2,F=B2.shape
    assert E==E2
    ranks=(int(np.linalg.matrix_rank(B1)),int(np.linalg.matrix_rank(B2)))
    betti=(V-ranks[0],E-ranks[0]-ranks[1],F-ranks[1])
    L1=B1.T@B1+B2@B2.T
    eig=np.linalg.eigvalsh(L1.astype(float))
    zero_count=int(np.count_nonzero(abs(eig)<1e-9))
    assert zero_count==betti[1]
    return {"V_E_F":[V,E,F],"cellular_Betti_H0_H1_H2":list(betti),
            "boundary_ranks":list(ranks),
            "Hodge_L1_eigenvalues":eig.tolist(),
            "Hodge_zero_modes":zero_count,
            "positive_nonzero_eigenvalue_min":float(min(x for x in eig if x>1e-9))}

def test():
    torus={str(n):analyze(*torus_cellular_operators(n)) for n in (3,4,5)}
    disk=analyze(*filled_square_cellular_operators())
    assert all(x["cellular_Betti_H0_H1_H2"]==[1,2,1] for x in torus.values())
    assert disk["cellular_Betti_H0_H1_H2"]==[1,0,0]
    assert disk["Hodge_zero_modes"]==0
    ratios=[]
    for mu in (.1,.01,.001):
        # Remove unrelated nonzero spectral factors; isolate the exact
        # topological zero-mode contribution to det(L1+mu I).
        n=3
        B1,B2=torus_cellular_operators(n)
        eig=np.linalg.eigvalsh((B1.T@B1+B2@B2.T).astype(float))
        small=np.linalg.det(B1.T@B1+B2@B2.T+mu*np.eye(2*n*n))
        nonzero_factor=np.prod([x+mu for x in eig if x>1e-9])
        ratio=small/nonzero_factor
        assert abs(ratio-mu**2)<1e-8*mu**2
        ratios.append({"regulator_mu":mu,"torus_normalized_determinant_zero_mode_factor":ratio,
                       "expected_mu_squared":mu*mu,
                       "disk_normalized_zero_mode_factor":1.})
    return {"date":"2026-11-19",
       "status":"PASS conditional topological kernel orientation-of-selection falsifier",
       "topological_torus_complexes":torus,
       "contractible_filled_square_disk_complex":disk,
       "finite_mass_regulator_zero_mode_factors":ratios,
       "exact_mechanism":"By combinatorial Hodge theorem, nullity(L1)=b1. Hence det(L1+mu I) contains mu^b1; torus has b1=2, filled disk b1=0.",
       "physical_caution":"Naively weighting histories by a positive unsaturated 1-form determinant can suppress the smooth torus MORE than a contractible disk as mu->0. These complexes have unequal numbers of cells; the normalized factor isolates only zero modes. This is not a valid comparison of full physical gravitational path-integral weights or a chiral spinor Dirac selection law.",
       "TOE_solved":False}

def main():
    out=test()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"status":"PASS","torus_H1_modes":out["topological_torus_complexes"]["3"]["Hodge_zero_modes"],
       "filled_disk_H1_modes":out["contractible_filled_square_disk_complex"]["Hodge_zero_modes"],
       "output":str(OUT)}))
if __name__=="__main__":main()
