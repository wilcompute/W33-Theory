#!/usr/bin/env python3
"""E6 27 -> SU5 branching, anomaly checks, and H27-Schur mass degeneracy.

Prior-art representation theory and model-independent obstruction, not an E6
vacuum or a predicted Standard Model fermion spectrum.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from toe_20261122_discrete_witting_dense_su4 import rank_mod,commutant_equations
from toe_20261122_witting_minimal_lie_control import primitive_cube_root
OUT=Path(__file__).resolve().parents[1]/"data/toe_20261122_e6_h27_chirality_gate.json"

def branch(n):
    # E6 27 -> SO10 16_1 + 10_-2 + 1_4
    # SO10 16 -> 10 + 5bar + 1; 10 -> 5 + 5bar.
    reps={"10":n,"5":n,"5bar":2*n,"singlet":2*n}
    dim=10*reps["10"]+5*(reps["5"]+reps["5bar"])+reps["singlet"]
    anomaly=reps["10"]+reps["5"]-reps["5bar"]
    assert dim==27*n and anomaly==0
    return dict(E6_27_copies=n,SU5_multiplicities=reps,total_dimension=dim,
                SU5_cubic_anomaly=anomaly,
                net_chiral_10s=n,net_chiral_5bars=reps["5bar"]-reps["5"],
                vectorlike_5_5bar_pairs=n)

def schrodinger(p):
    w=primitive_cube_root(p)
    Z=np.diag([1,w,w*w%p]).astype(np.int64)
    X=np.zeros((3,3),dtype=np.int64)
    for j in range(3):X[(j+1)%3,j]=1
    assert np.array_equal(Z@X%p,w*(X@Z)%p)
    return X,Z

def verify():
    contents=[branch(n) for n in (1,2,3,4,5)]
    assert contents[2]["SU5_multiplicities"]=={"10":3,"5":3,"5bar":6,"singlet":6}
    ranks=[]
    for p in (7,13,19,31,37,43):
        X,Z=schrodinger(p)
        rank=rank_mod(np.vstack([commutant_equations(X,p),
                                  commutant_equations(Z,p)]),p)
        assert rank==8
        ranks.append(dict(prime=p,H27_triplet_commutant_rank=rank,
                          H27_triplet_commutant_dimension=1))
    return dict(status="PASS_E6_BRANCHING_AND_H27_SCHUR_NO_GENERATION_SELECTOR",
      date="2026-11-22",E6_branching="27=16(1)+10(-2)+1(4)",
      SU5_branching="27=10+5+2*(5bar)+2*1",
      normalized_anomaly="A(10)=+1,A(5)=+1,A(5bar)=-1",
      finite_generation_census=contents,
      generation_three_selected_by_group_or_anomaly_alone=False,
      reason="Every number n of 27 copies is anomaly-free under SU5 and yields n net chiral families if n vectorlike 5+5bar pairs obtain mass.",
      Schur_triplet_hierarchy_no_go="H27 acts irreducibly on a 3D Schrodinger family triplet. Exact commuting mass/endormorphism algebra is scalars; unbroken H27 with one such triplet cannot produce three nondegenerate masses.",
      symmetry_breaking_needed_for_triplet_hierarchies=True,
      modular_Schur_certificates=ranks,
      negative_controls={"remove_one_5_from_single_27_anomaly":-1,
                         "remove_one_10_from_single_27_anomaly":-1},
      caveat="No anomaly-free complete UV vacuum, three-family selector, heavy vectorlike mass construction, Yukawa hierarchy, physical E6 local model, or TOE derived.")

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS SU5 anomaly, E6 27 branch, H27 mass degeneracy no-go")
if __name__=="__main__":main()
