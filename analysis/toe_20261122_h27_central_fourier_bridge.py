#!/usr/bin/env python3
"""Witting H27 regular-address vs E6 operator-character bridge.

Direct 27-to-27 equivariance fails by center spectrum. Three regular
copies have a 27D central-character sector abstractly equivalent to nine
three-dimensional Schrodinger H27 representations. The corresponding
obstruction and the general Fourier principle predate this calculation
in the repository; this verifies them on the explicit new Witting orbit.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
import toe_20261122_witting_one_phase_three_fixed as W
from toe_20261122_discrete_witting_dense_su4 import rank_mod,commutant_equations
OUT=Path(__file__).resolve().parents[1]/"data/toe_20261122_h27_central_fourier_bridge.json"

def action():
    p=W.permutations();R={j:Permutation(p[j]) for j in W.FIXED}
    x=R[5]*R[33]**-1
    y=R[26]*x*R[26]**-1
    z=x*y*x**-1*y**-1
    N=PermutationGroup([x,y])
    assert N.order()==27 and z.order()==3
    assert z in N.center().generate_schreier_sims()
    orbit=sorted(N.orbit(W.TUNABLE))
    assert len(orbit)==27
    return N,x,y,z,orbit

def fibers(z,orbit):
    unseen=set(orbit);out=[]
    while unseen:
        a=min(unseen);f=(a,int(z(a)),int((z**2)(a)))
        assert len(set(f))==3
        out.append(f);unseen-=set(f)
    assert len(out)==9
    return out

def sector_action(g,fibers,omega,p):
    lookup={x:(i,k) for i,f in enumerate(fibers) for k,x in enumerate(f)}
    M=np.zeros((9,9),dtype=np.int64)
    for col,f in enumerate(fibers):
        row,k=lookup[int(g(f[0]))]
        M[row,col]=pow(omega,k,p)
    return M%p

def verify():
    N,x,y,z,orbit=action()
    cyc=fibers(z,orbit)
    assert all(sum(g(k)==k for k in orbit)==(27 if g.is_identity else 0)
               for g in N.generate_schreier_sims())
    checks=[]
    for p in (7,13,19,31,37,43):
        w=W.lie.primitive_cube_root(p)
        X=sector_action(x,cyc,w,p)
        Y=sector_action(y,cyc,w,p)
        Z=sector_action(z,cyc,w,p)
        assert np.array_equal(Z,w*np.eye(9,dtype=np.int64)%p)
        rank=rank_mod(np.vstack([commutant_equations(A,p) for A in (X,Y)]),p)
        assert rank==72,(p,rank)
        checks.append(dict(prime=p,omega=w,central_sector_dimension=9,
                           sector_commutant_rank=rank,sector_commutant_dimension=9,
                           three_copies_projected_dimension=27))
    return dict(status="PASS_EXACT_H27_CENTRAL_FOURIER_BRIDGE",date="2026-11-22",
      regular_address_order=27,regular_address_orbit=orbit,
      center_cycles=[list(c) for c in cyc],
      center_trace_on_address27=0,
      assumed_operator_model="9 copies of 3D Schrodinger with scalar center omega",
      operator_center_trace="27*omega",
      invertible_direct_equivariant_intertwiner=False,
      max_rank_direct_intertwiner=9,
      reason="Regular central spectrum 9 each of 1,omega,omega^2; operator center scalar omega on all 27.",
      projector="P_omega=(I+omega^-1 Z+omega^-2 Z^2)/3, rank 9 on C[H27]",
      three_address_copies_projected_dimension=27,
      Fourier_irrep_lift="3 regular copies project to 9 Schrodinger copies, giving an abstract 27D isomorphism after choosing a center character.",
      exact_field_checks=checks,
      prior_art="w33_address_operator_h27_intertwiner_obstruction.py and toe_20261118_H27_Fourier_minimal7_E6_tensor_embedding.py already derived general obstruction and Fourier isometries; this is a canonical Witting-index verification.",
      physical_boundary="C27 is a formal ray-label module, not 27 physically orthogonal modes; no E6 cubic invariant, field embedding, gauge dynamics or actual hardware coupling is built.")

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS explicit Witting H27 central-character obstruction and Fourier projection")
if __name__=="__main__":main()
